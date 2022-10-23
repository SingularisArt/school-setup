#!/usr/bin/env python3

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from RofiLessonManager import utils as utils
from RofiLessonManager.courses import Courses as Courses
from config import my_assignments_pdf_folder as pdf_folder


def get_files(id):
    return (
        service.files()
        .list(
            q=f"'{id}' in parents",
            spaces="drive",
            fields="files(id, name)",
        )
        .execute()
    )


def sync_file(file, name, course_name, id):
    try:
        file_metadata = {
            "name": name,
            "parents": [id],
        }

        media = MediaFileUpload(
            file,
            mimetype="application/pdf",
        )

        service.files().create(
            body=file_metadata, media_body=media, fields="id"
        ).execute()
    except HttpError:
        utils.rofi.msg(
            f"Failed to sync {name} for course {course_name}",
            err=True,
        )

        return False

    return True


def sync_notes(course):
    notes_folder = course.info["folder"]["notes_folder"]

    drive_notes = get_files(notes_folder)
    if len(drive_notes["files"]) > 2:
        for note in drive_notes["files"]:
            if note["name"] == "Notes":
                service.files().delete(fileId=note["id"]).execute()

    lectures = course.lectures

    r = lectures.parse_range_string("all")
    lectures.update_lectures_in_master(r)
    lectures.compile_master()

    path = f"{course.path}/master.pdf"

    if not sync_file(path, "Notes", course.name, notes_folder):
        return


def sync_assignments(course):
    assignments_folder = course.info["folder"]["assignments_folder"]
    files = utils.get_files(pdf_folder)
    named_files = sorted(
        [utils.replace_str(f, [".pdf", ""], ["-", " "]).title() for f in files]
    )

    drive_assignments = get_files(assignments_folder)
    if len(drive_assignments["files"]) > 1:
        for assignment in drive_assignments["files"]:
            if assignment["name"] in named_files:
                service.files().delete(fileId=assignment["id"]).execute()

    for file in files:
        if "pdf" not in file:
            continue

        path = f"{pdf_folder}/{file}"
        name = f"Week {utils.filename_to_number(file)}"

        if not sync_file(path, name, course.name, assignments_folder):
            return


service = utils.authenticate(
    "drive",
    ["https://www.googleapis.com/auth/drive"],
    "credentials/sync.json",
)


def main():
    courses = Courses()
    current = courses.current
    index = 0

    options = ["Sync Notes", "Sync Assignments", "Sync Notes and Assignments"]
    _, op_index, _ = utils.rofi.select("Select", options)

    if op_index < 0:
        exit(1)

    for x, course in enumerate(courses):
        if course.name == current:
            index = x

        courses.current = course

        if op_index == 0 or op_index == 2:
            sync_notes(course)
        if op_index == 1 or op_index == 2:
            sync_assignments(course)

        stuff = ""
        if op_index == 0:
            stuff = "notes"
        elif op_index == 1:
            stuff = "assignments"
        elif op_index == 2:
            stuff = "notes and assignments"

        utils.rofi.msg(
            f"Successfully synced your {stuff} to the cloud for "
            + f"the course {utils.folder_to_name(course.name)}"
        )
    courses.current = courses[index]


if __name__ == "__main__":
    main()
