#!/usr/bin/env python3

import utils
from RofiLessonManager.courses import Courses as Courses


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


def sync_notes(course):
    notes_folder = course.info["notes_folder_id"]

    drive_notes = get_files(notes_folder)
    for note in drive_notes["files"]:
        if note["name"] == "Notes":
            service.files().delete(fileId=note["id"]).execute()

    lectures = course.lectures

    r = lectures.parse_range_string("all")
    lectures.update_lectures_in_master(r)
    lectures.compile_master()

    path = f"{course.root}/master.pdf"
    utils.sync_file(service, path, "Notes", course.name, notes_folder)


service = utils.authenticate(
    "drive",
    ["https://www.googleapis.com/auth/drive"],
    "credentials/sync.json",
)


def main():
    courses = Courses()

    courses_to_display = [c.name.upper() for c in courses]
    courses_to_display.append("All")

    _, index, selected = utils.rofi.select(
        "Select course to sync notes",
        courses_to_display,
    )

    if index < 0:
        return

    msg = "Successfully synced your notes to the cloud for "

    if selected != "All":
        sync_notes(courses[index])
        course_display_name = utils.folder_to_name(courses[index].name)
        utils.rofi.msg(msg + course_display_name)
        return

    for course in courses:
        sync_notes(course)
        course_display_name = utils.folder_to_name(course.name)
        utils.rofi.msg(msg + course_display_name)


if __name__ == "__main__":
    main()
