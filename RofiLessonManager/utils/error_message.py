from rofi import Rofi


def error_message(message):
    """
    Displays an error message in red and bold.

    Args:
        message (str): The message to display.
        rofi (object): The rofi object from the rofi.Rofi.
    """

    rofi = Rofi()
    rofi.error('<span color="red"><b>{}</b></span>'.format(message),
               ['-markup'])
