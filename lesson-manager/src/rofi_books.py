import os

from core.books import Books
from lesson_manager.config import rofi_options
from lesson_manager import config
import utils


def main():
    books = Books()
    options = [book.display_name for book in books]

    if not books:
        utils.rofi.msg("You don't have any books.", err=True)
        exit(1)

    _, index, _ = utils.rofi.select(
        "Select Assignment",
        options,
        rofi_options,
    )

    if index < 0:
        exit(1)

    selected = books[index]

    if selected.has_solutions:
        options_with_solutions = ["Book", "Solution"]

        _, index, _ = utils.rofi.select(
            "Select",
            options_with_solutions,
            rofi_options,
        )

        if index < 0:
            exit(1)

        if index == 0:
            os.system(f"{config.pdf_viewer} {selected.master_file}")
            return
        else:
            if not isinstance(selected.solutions_as_files, list):
                os.system(f"{config.pdf_viewer} {selected.solutions}")
                return

            _, index, _ = utils.rofi.select(
                "Select Solution",
                selected.solutions_for_display,
                rofi_options,
            )

            solution_path = selected.solutions_as_files[index]
            full_path = f"{selected.root}/solutions/{solution_path}"

            os.system(f"{config.pdf_viewer} {full_path}")
    else:
        os.system(f"{config.pdf_viewer} {selected.master_file}")


if __name__ == "__main__":
    main()
