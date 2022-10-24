#!/usr/bin/env python3

from RofiLessonManager import utils as utils
from RofiLessonManager.courses import Courses as Courses
from RofiLessonManager.courses import Course as Course


def get_files(id: str) -> dict[list[dict[str, str]], None]:
    """
    Get all files from a folder in google drive.

    Parameters
    ----------
    id (str): The id of the folder to recieve all files from.

    Returns
    -------
    dict: Example: {"files": [{"id": "ID", "name": "NAME"}, ...]}
    """

    return (
        service.files()
        .list(
            q=f"'{id}' in parents",
            spaces="drive",
            fields="files(id, name)",
        )
        .execute()
    )


def sync_notes(course: Course) -> None:
    # Get the notes_folder_id from the info.yaml from the current course.
    notes_folder = course.info["notes_folder_id"]

    # Get all files within the notes_folder.
    drive_notes = get_files(notes_folder)
    for note in drive_notes["files"]:
        # If any of the files' name is Notes, then remove it.
        if note["name"] == "Notes":
            service.files().delete(fileId=note["id"]).execute()

    # Get all the lecture notes.
    lectures = course.lectures

    # Compile all lecture notes for the current course.
    r = lectures.parse_range_string("all")
    lectures.update_lectures_in_master(r)
    lectures.compile_master()

    # Path to the master.pdf.
    path = f"{course.path}/master.pdf"
    # Sync the master.pdf file.
    utils.sync_file(service, path, "Notes", course.name, notes_folder)


def run_course(course, msg):
    sync_notes(course)
    course_display_name = utils.folder_to_name(course.name)
    utils.rofi.msg(msg + course_display_name)


service = utils.authenticate(
    "drive",
    ["https://www.googleapis.com/auth/drive"],
    "credentials/sync.json",
)


def main():
    courses = Courses()
    current = courses.current
    index = 0

    for x, course in enumerate(courses):
        if course.name == current:
            index = x

    courses_to_display = [utils.folder_to_name(c.name) for c in courses]
    courses_to_display.append("All")

    _, course_index, selected = utils.rofi.select(
        "Select course to sync notes",
        courses_to_display,
    )

    if course_index < 0:
        return

    msg = "Successfully synced your notes to the cloud for "

    if selected != "All":
        courses.current = courses[course_index]
        run_course(courses[course_index], msg)
        return

    for course in courses:
        courses.current = course

        run_course(course, msg)

    courses.current = courses[index]


if __name__ == "__main__":
    main()
