def get_folder_status(folder):
    """
    Gets the status of each project.

    Args:
        folder (str): The folder to get the status of.

    Returns:
        str: The status of the folder. ('Incomplete', 'Complete', 'Unknown')
    """

    try:
        # Try to get the status of the project
        with open(folder + '/complete.txt', 'r') as file:
            return file.read()

    except FileNotFoundError:
        # If we fail, create the file, write and return incomplete
        with open(folder + '/complete.txt', 'w') as file:
            file.write('Incomplete')
            return 'Incomplete'
