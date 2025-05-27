from daemonize import Daemonize
import os
import signal
import platform

from core.inkscape_figures import InkscapeFigure as InkscapeFigure
from core.inkscape_figures import log as log
from lesson_manager import config
from utils.rofi import select as select
from lesson_manager.config import PID_FILE


def get_default_path(path):
    if not path:
        return config.current_course / "figures"

    return os.path.abspath(path)


def watch(kill=False):
    if kill:
        if os.path.exists(PID_FILE):
            with open(PID_FILE, "r") as f:
                pid = int(f.read())
            try:
                os.kill(pid, signal.SIGTERM)
                log.info(f"Killed watcher process with PID {pid}.")
                os.remove(PID_FILE)
            except ProcessLookupError:
                log.warning(f"No process with PID {pid} found. Removing stale PID file.")
                os.remove(PID_FILE)
        else:
            log.warning("Watcher is not running (PID file not found).")
        return

    fig = InkscapeFigure()
    if platform.system() == "Linux":
        watcher = fig.watch_inotify
    else:
        watcher = fig.watch_fswatch

    Daemonize(app="inkscape-figures", pid=PID_FILE, action=watcher).start()
    log.info("Watching figures.")


def create(title, root):
    fig = InkscapeFigure()
    fig.create_figure(title, root)


def edit(root):
    fig = InkscapeFigure()
    fig.edit_figure(root)
