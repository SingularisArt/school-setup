import os
from pathlib import Path
import config
import utils


class Assignment:
    def __init__(self, root):
        self.root = root
        self.name = self.root.stem
        self.file_paths = {}

        # Initialize file paths for different extensions
        for key in config.my_assignment_folders:
            if key == "root":
                continue
            newKey = key.replace("_folder", "_file")
            ext = key.split("_")[0]
            path = config.my_assignment_folders[key] / f"{self.name}.{ext}"
            newPath = Path(path)
            self.file_paths[newKey] = {
                "path": newPath,
                "exists": newPath.exists(),
            }

        # Initialize file paths for PDFs
        for key in config.assignment_folders:
            path = config.assignment_folders[key] / f"{self.name}.pdf"
            newPath = Path(path)
            self.file_paths[key] = {
                "path": path,
                "exists": newPath.exists(),
            }

        # Create options for available files
        self.options = {
            f"View {key.split('_')[0]} File": f"{key}"
            for key in self.file_paths
            if self.file_paths[key]["exists"]
        }

        self.progress_options = ["not started", "pending", "done"]

        # Load assignment info from YAML file
        self.info = utils.load_data(
            self.file_paths["yaml_file"]["path"],
            "yaml",
        )
        if not self.info:
            self.info = False

        try:
            self.title = self.info["title"]
            self.grade = self.info["grade"]
            self.submitted = self.info["submitted"]
            self.number = self.info["number"]
            self.due_date, self.days_left = self.get_due_date()
        except Exception:
            pass

    def get_due_date(self):
        due_date = self.info["due_date"]
        days_left, due_date = utils.check_if_assignment_is_due(
            due_date,
            self.submitted,
        )
        due_date = utils.generate_short_title(due_date, 28)
        return due_date, days_left

    def parse_command(self, cmd):
        path = self.file_paths[cmd]["path"]
        if ".pdf" in str(path):
            self.edit(path, "pdf")
        else:
            self.edit(path)

    def edit(self, root, cmd="file"):
        if cmd == "pdf":
            os.system(f"{config.pdf_viewer} {root}")
        else:
            listen_location = "/tmp/nvim.pipe"
            arguments = []

            if os.path.exists(listen_location):
                arguments = ["--server", "/tmp/nvim.pipe", "--remote"]
            elif not os.path.exists(listen_location):
                arguments = ["--listen", "/tmp/nvim.pipe"]

            arguments = " ".join(str(e) for e in arguments if e)

            os.system(f"{config.terminal} {config.editor} {arguments} {root}")

    def __repr__(self):
        return f"<Assignment #{self.number}: {self.name}>"


class Assignments(list):
    def __init__(self):
        super().__init__(self.read_files())
        self.titles = [assignment.name for assignment in self]

    def read_files(self):
        latex_assignments = []
        for yaml_file in config.my_assignment_folders["yaml_folder"].glob("*.yaml"):
            yaml_file = Assignment(yaml_file)
            if yaml_file.info:
                latex_assignments.append(yaml_file)

        return sorted(
            latex_assignments,
            key=lambda assignment: assignment.number,
        )
