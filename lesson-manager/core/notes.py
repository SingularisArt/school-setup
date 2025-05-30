import os
import re
from datetime import datetime
from pathlib import Path

from lesson_manager import config
from lesson_manager import cc_info as info
import utils


class Note:
    def __init__(self, file_path):
        self.file_path = file_path
        self.number = None
        self.date = None
        self.week = None
        self.title = None
        self.path = file_path

        self._parse_note_file()

    def _parse_note_file(self):
        with open(self.file_path, "r") as file:
            for line in file:
                match = re.search(r"\\lecture\[(.+)\]{(\d+)}{(.+)}{(.+)}", line)
                if match:
                    self.number = int(match.group(2))
                    self.date = datetime.strptime(match.group(3), config.date_format)
                    self.title = match.group(4)
                    self.week = (
                        utils.get_week(self.date)
                        - utils.get_week(
                            datetime.strptime(info.start_date, config.date_format)
                        )
                        + 1
                    )
                    break

    def edit(self):
        listen_location = "/tmp/nvim.pipe"
        args = (
            ["--server", listen_location, "--remote"]
            if os.path.exists(listen_location)
            else ["--listen", listen_location]
        )

        number = utils.convert_number(self.number, display=True)
        note_file = Path("lectures") / f"lec-{number}.tex"

        cmd = (
            f"sudo -u singularisart kitty --directory={config.current_course} {config.editor} "
            f"{' '.join(args)} {note_file}"
        )
        os.system(cmd)

    def __len__(self):
        return len(self.title or "")


class Notes(list):
    def __init__(self, course):
        self.root = Path(course.root)
        self.master_file = self.root / "master.tex"
        self.notes_path = self.root / "lectures"
        super().__init__(self._read_files())

    def _read_files(self):
        notes = [Note(f) for f in self.notes_path.glob(f"lec-*.tex")]
        return sorted(
            (note for note in notes if note.number is not None),
            key=lambda note: note.number,
        )

    def _parse_note_spec(self, spec):
        all_numbers = [note.number for note in self]
        if not all_numbers:
            return []

        if spec.isdigit():
            return [int(spec)]
        if spec == "last":
            return [all_numbers[-1]]
        if spec == "prev_last":
            return all_numbers[-2:]
        if spec == "all":
            return all_numbers
        if spec == "prev":
            return all_numbers[:-1]

    def parse_range_string(self, arg):
        result = []
        parts = arg.split(",")

        for part in parts:
            part = part.strip()
            if "-" in part:
                try:
                    start, end = map(int, part.split("-"))
                    if start <= end:
                        result.extend(range(start, end + 1))
                    else:
                        result.extend(range(start, end - 1, -1))
                except ValueError:
                    continue
            else:
                try:
                    result.append(int(part))
                except ValueError:
                    continue

        if not result:
            return self._parse_note_spec(arg)

        return result

    def _filter_body(self, numbers):
        with open(self.master_file, "r") as file:
            lines = file.readlines()

        filtered_body = []
        in_notes_block = False
        lowest, highest = 0, 0

        for line in lines:
            stripped = line.strip()

            if stripped.startswith(r"\chapter"):
                filtered_body.append(line)

            elif "% notes start" in stripped:
                match = re.search(r"% notes start (\d+)-(\d+)", stripped)
                if match:
                    lowest, highest = map(int, match.groups())
                    in_notes_block = True
                filtered_body.append(line)

                for num in numbers:
                    if lowest <= num <= highest:
                        filtered_body.append(f"  \\input{{lectures/lec-{num:02}.tex}}\n")

            elif "% notes end" in stripped:
                in_notes_block = False
                filtered_body.append(line)

            elif not in_notes_block:
                filtered_body.append(line)

        return "".join(filtered_body)

    def update_notes_in_master(self, numbers):
        body = self._filter_body(numbers)
        self.master_file.write_text(body)

    def compile_master(self):
        os.chdir(config.current_course)
        os.system("make")
