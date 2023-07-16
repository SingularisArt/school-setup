from RofiLessonManager.courses import Courses as Courses
import utils
import config


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
    notes_folder = config.drive_folder_id

    drive_notes = get_files(notes_folder)
    pdf_file_name = f"{course.info['short']}: {course.info['title']}.pdf"
    for note in drive_notes["files"]:
        if note["name"] == pdf_file_name:
            service.files().delete(fileId=note["id"]).execute()

    notes = course.notes

    r = notes.parse_range_string("all")
    if r != 0:
        notes.update_notes_in_master(r)
    notes.compile_master()

    path = f"{course.root}/master.pdf"
    utils.sync_file(service, path, pdf_file_name, course.name, notes_folder)


service = utils.authenticate(
    "drive",
    ["https://www.googleapis.com/auth/drive"],
    "credentials/sync.json",
)


def main():
    courses = Courses()
    current_tmp_course_file = "/tmp/tmp-current-course.txt"
    current_course = courses.current

    course_names = [course.name for course in courses]
    courses_to_display = [course.upper() for course in course_names]
    # courses_to_display.append("All")

    _, index, _ = utils.rofi.select(
        "Select course to sync notes",
        courses_to_display,
    )

    if index < 0:
        return

    with open(current_tmp_course_file, "w") as f:
        f.write(str(course_names.index(current_course.name)))

    msg = "Successfully synced your notes to the cloud for "
    selected_course = courses[index]

    courses.current = selected_course
    sync_notes(courses.current)
    course_display_name = utils.folder_to_name(courses[index].name)
    utils.rofi.msg(msg + course_display_name)

    # for course in courses:
    #     sync_notes(course)
    #     course_display_name = utils.folder_to_name(course.name)
    #     utils.rofi.msg(msg + course_display_name)

    previous_current_course_index = int(open(current_tmp_course_file, "r").read())
    courses.current = courses[previous_current_course_index]


if __name__ == "__main__":
    main()
