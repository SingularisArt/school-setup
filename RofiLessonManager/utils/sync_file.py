from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from RofiLessonManager import utils as utils


def sync_file(
    service,
    file,
    name,
    course_name,
    id,
    mimetype="application/pdf",
):
    try:
        file_metadata = {
            "name": name,
            "parents": [id],
        }

        media = MediaFileUpload(
            file,
            mimetype=mimetype,
        )

        service.files().create(
            body=file_metadata, media_body=media, fields="id"
        ).execute()
    except HttpError:
        utils.rofi.msg(
            f"Failed to sync {name.lower()} for course {course_name}",
            err=True,
        )

        return False
