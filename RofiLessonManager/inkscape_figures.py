import logging
import os
import re
import subprocess
import warnings
from pathlib import Path
from shutil import copy
import yaml
import pyperclip
from appdirs import user_config_dir

from config import rofi_options
import config
from utils.rofi import select as select


logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger("inkscape-figures")


class InkscapeFigure:
    def __init__(self):
        self.user_dir = Path(user_config_dir("lesson-manager"))
        self.roots_file = self.user_dir / "roots"
        self.config_file_path = self.user_dir / "config.yaml"
        self.ensure_dirs()

        self.config = yaml.safe_load(self.config_file_path.read_text())
        self.current_course_dir = Path(self.config["current_course"])
        self.template = self.get_template_path()

    def ensure_dirs(self):
        self.user_dir.mkdir(parents=True, exist_ok=True)
        if not self.roots_file.is_file():
            self.roots_file.touch()

    def get_template_path(self):
        course_template = self.current_course_dir / "figures" / "template.svg"

        if course_template.is_file():
            return course_template

        template = config.config_path / "template.svg"
        return template

    def add_root(self, path):
        path = str(path)
        roots = self.get_roots()
        if path not in roots:
            roots.append(path)
            self.roots_file.write_text("\n".join(roots))

    def get_roots(self):
        return [r for r in self.roots_file.read_text().splitlines() if r]

    def latex_template(self, name, caption):
        label = caption.replace("-", "_").replace(" ", "_").lower()
        caption = caption.replace("-", " ").replace("_", " ").title()

        return "\n".join([
            r"\begin{figure}[H]",
            r"    \centering",
            rf"    \incfig{{{name}}}",
            rf"    \caption{{{caption}}}",
            rf"    \label{{fig:{label}}}",
            r"\end{figure}",
        ])

    def beautify(self, name):
        return name.replace("_", " ").replace("-", " ").title()

    def indent(self, text, spaces):
        return "\n".join(" " * spaces + line for line in text.splitlines())

    def inkscape(self, path):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            subprocess.Popen(["inkscape", str(path)])

    def maybe_recompile_figure(self, filepath):
        filepath = Path(filepath)
        if filepath.suffix != ".svg":
            log.debug("File has changed, but is not an svg: %s", filepath.suffix)
            return

        log.info("Recompiling %s", filepath)
        pdf_path = filepath.parent / (filepath.stem + ".pdf")
        name = filepath.stem

        version = subprocess.check_output(["inkscape", "--version"], universal_newlines=True)
        version_number = [int(x) for x in re.findall(r"\d+", version)[:3]]
        version_number += [0] * (3 - len(version_number))

        if version_number < [1, 0, 0]:
            cmd = ["inkscape", "--export-area-page", "--export-dpi", "300", "--export-pdf", pdf_path, "--export-latex", filepath]
        else:
            cmd = ["inkscape", filepath, "--export-area-page", "--export-dpi", "300", "--export-type=pdf", "--export-latex", "--export-filename", pdf_path]

        log.debug("Running command:\n  %s", " ".join(str(e) for e in cmd))
        result = subprocess.run(cmd)

        if result.returncode == 0:
            template = self.latex_template(name, self.beautify(name))
            pyperclip.copy(template)
            log.debug("Copied LaTeX template:\n%s", self.indent(template, 4))
        else:
            log.error("Recompilation failed with return code %s", result.returncode)

    def watch_inotify(self):
        import inotify.adapters
        from inotify.constants import IN_CLOSE_WRITE

        while True:
            roots = self.get_roots()
            watcher = inotify.adapters.Inotify()
            watcher.add_watch(str(self.roots_file), mask=IN_CLOSE_WRITE)

            for root in roots:
                try:
                    watcher.add_watch(root, mask=IN_CLOSE_WRITE)
                except Exception:
                    log.debug("Could not add root %s", root)

            for event in watcher.event_gen(yield_nones=False):
                _, _, path, filename = event
                if Path(path) == self.roots_file:
                    break
                self.maybe_recompile_figure(Path(path) / filename)

    def watch_fswatch(self):
        while True:
            roots = self.get_roots()
            p = subprocess.Popen(["fswatch", *roots, str(self.user_dir)],
                                 stdout=subprocess.PIPE, universal_newlines=True)
            while True:
                if not p.stdout:
                    return
                filepath = p.stdout.readline().strip()
                if filepath == str(self.roots_file):
                    p.terminate()
                    break
                self.maybe_recompile_figure(filepath)

    def create_figure(self, title, root):
        title = title.strip()
        file_name = title.replace(" ", "-").lower() + ".svg"
        figures = Path(root).absolute()
        figures.mkdir(parents=True, exist_ok=True)
        figure_path = figures / file_name

        if figure_path.exists():
            print(f"{title} 2")
            return

        copy(str(self.template), str(figure_path))
        self.add_root(figures)
        self.inkscape(figure_path)

        leading_spaces = len(title) - len(title.lstrip())
        print(self.indent(self.latex_template(figure_path.stem, title), leading_spaces))

    def edit_figure(self, root):
        figures = Path(root).absolute()
        files = sorted(figures.glob("*.svg"), key=lambda f: f.stat().st_mtime, reverse=True)
        names = [self.beautify(f.stem) for f in files]

        _, index, selected = select("Select figure", names, rofi_options)
        if selected:
            path = files[index]
            self.add_root(figures)
            self.inkscape(path)

            template = self.latex_template(path.stem, self.beautify(path.stem))
            pyperclip.copy(template)
            log.debug("Copied LaTeX template:\n%s", self.indent(template, 4))
