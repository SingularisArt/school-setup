from daemonize import Daemonize
import os
import platform

from RofiLessonManager.inkscape_figures import InkscapeFigure as InkscapeFigure
from RofiLessonManager.inkscape_figures import log as log
from utils.rofi import select as select


def watch():
    fig = InkscapeFigure()
    if platform.system() == "Linux":
        watcher = fig.watch_inotify
    else:
        watcher = fig.watch_fswatch

    Daemonize(app="inkscape-figures", pid="/tmp/inkscape-figures.pid", action=watcher).start()
    log.info("Watching figures.")


def create(title, root):
    fig = InkscapeFigure()
    fig.create_figure(title, root)


def edit(root):
    fig = InkscapeFigure()
    fig.edit_figure(root)


def main(parser, args):
    command = args[0] if args else None

    if not command or len(command) == 0 or command not in ["create", "edit", "watch"]:
        parser.error("Unknown subcommand for --rofi-figures. Use 'create', 'edit', or 'watch'.")
    if command == "create" and len(args) < 2:
        parser.error("The 'create' command requires a figure title.")

    if command == "create":
        title = args[1]
        root = os.getcwd() if len(args) < 3 else args[2]
        create(title, root)
    elif command == "edit":
        root = os.getcwd() if len(args) < 2 else args[1]
        edit(root)
    elif command == "watch":
        watch()
