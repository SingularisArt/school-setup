import os


def get_flash_drives(r, project_name):
    """
    Get the flash drives that are connected to the laptop/pc/etc.

    Args:
        r (object): Rofi object.
        project_name (str): Name of the project.

    Returns:
        drives (list): List of drives.
        drives_names (list): List of drives with rofi design.
    """
    # List all flash drives
    # drives = [x for x in os.listdir('/run/media/{}'.format(self.user))]
    drives = [x for x in os.listdir('/run/media/hashem/')]

    if not drives:
        r.error('No Flash Drives Found')
        exit(1)

    drives_with_style = []

    for drive in drives:
        new_drive = '<span color="brown">{}</span>'.format(drive)
        drives_with_style.append(new_drive)

    return drives, drives_with_style
