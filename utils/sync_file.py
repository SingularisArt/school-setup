from typing import Optional

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

import utils


def sync_file(
    service,
    file: str,
    name: str,
    course_name: str,
    id: str,
    mimetype: Optional[str] = "application/pdf",
) -> Optional[bool]:
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
