#!/usr/bin/env python3

import os

import config


class Book:
    def __init__(self, root):
        self.root = root
        self.master_file = self.get_master_file()
        self.has_solutions = self.check_solutions()

        if self.has_solutions:
            (
                self.solutions_as_files,
                self.solutions_for_display,
            ) = self.get_solutions()

        self.name = root.name
        self.display_name = self.name.replace("-", " ").replace("_", " ")
        self.display_name = self.display_name.title()

    def get_master_file(self):
        if os.path.isfile(self.root):
            return self.root

        return self.root / "master.pdf"

    def check_solutions(self):
        if os.path.isdir(self.root):
            solutions_folder = os.path.join(self.root, "solutions")
            solutions_pdf = os.path.join(self.root, "solutions.pdf")

            if os.path.exists(solutions_folder) or os.path.exists(
                solutions_pdf,
            ):
                return True

        return False

    def get_solutions(self):
        solutions_path = self.root / "solutions"

        if os.path.exists(f"{solutions_path}.pdf"):
            return solutions_path
        else:
            if os.path.exists(solutions_path):
                solutions_as_files = sorted([
                    solution.name for solution in solutions_path.iterdir()
                ])
                solutions_for_display = [
                    solution.replace("chap", "Chapter")
                    .replace("-", " ")
                    .replace(".pdf", "")
                    for solution in solutions_as_files
                ]

                return solutions_as_files, solutions_for_display


class Books(list):
    def __init__(self):
        super().__init__(self.read_files())

    def read_files(self):
        books = config.books_dir.iterdir()
        return [Book(book) for book in books if book.name != "README.md"]
