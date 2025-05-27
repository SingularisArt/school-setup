#!/usr/bin/env python3

import argparse
import os
import pwd


# === STANDALONE COMMANDS ===

def handle_calendar(args):
    import src.countdown as ca
    print("Waiting for connection")
    ca.check_internet()
    ca.main()


def handle_init_courses(args):
    import src.init_courses as ic
    ic.main()


def handle_strip_notes(args):
    import src.rofi_strip_notes as rsn
    rsn.main(args.output)


def handle_source_notes(args):
    import src.source_notes as sn
    sn.main()


def handle_sync_notes(args):
    import src.sync_notes as sy
    sy.main()


# === ROFI ===

def handle_rofi_assignments(args):
    import src.rofi_assignments as ra
    ra.main()


def handle_rofi_books(args):
    import src.rofi_books as rb
    rb.main()


def handle_rofi_courses(args):
    import src.rofi_courses as rc
    rc.main()


def handle_rofi_notes(args):
    import src.rofi_notes as rn
    rn.main()


# === FIGURES ===

def handle_figures_create(args):
    import src.rofi_figures as rf

    path = rf.get_default_path(args.path)
    rf.create(args.name, path)


def handle_figures_edit(args):
    import src.rofi_figures as rf

    path = rf.get_default_path(args.path)
    rf.edit(path)


def handle_figures_watch(args):
    import src.rofi_figures as rf
    rf.watch(kill=args.kill)


def handle_figures_shortcut_manager(args):
    import src.shortcut_manager as sm
    sm.main(kill=args.kill)


def main():
    user = pwd.getpwnam("singularisart")

    os.environ["HOME"] = user.pw_dir
    os.environ["USER"] = user.pw_name
    os.environ["LOGNAME"] = user.pw_name
    os.environ["XDG_CONFIG_HOME"] = os.path.join(user.pw_dir, ".config")

    parser = argparse.ArgumentParser(description="Lesson Manager CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Standalone commands
    subparsers.add_parser("calendar", help="Parse Google Calendar").set_defaults(func=handle_calendar)
    subparsers.add_parser("init-courses", help="Initialize all courses").set_defaults(func=handle_init_courses)
    subparsers.add_parser("source-notes", help="Source notes").set_defaults(func=handle_source_notes)
    subparsers.add_parser("sync-notes", help="Sync notes to Google Drive").set_defaults(func=handle_sync_notes)

    strip_parser = subparsers.add_parser("strip-notes", help="Strip LaTeX notes")
    strip_parser.add_argument("-o", "--output", default="output.tex", help="Output file (default: output.tex)")
    strip_parser.set_defaults(func=handle_strip_notes)

    # === ROFI Command Group ===
    rofi_parser = subparsers.add_parser("rofi", help="Rofi Interfaces")
    rofi_subparsers = rofi_parser.add_subparsers(dest="rofi_command", required=True)

    rofi_subparsers.add_parser("assignments", help="View assignments").set_defaults(func=handle_rofi_assignments)
    rofi_subparsers.add_parser("books", help="View books").set_defaults(func=handle_rofi_books)
    rofi_subparsers.add_parser("courses", help="View courses").set_defaults(func=handle_rofi_courses)
    rofi_subparsers.add_parser("notes", help="View notes").set_defaults(func=handle_rofi_notes)

    # === FIGURES Command Group ===
    figures_parser = subparsers.add_parser("figures", help="Manage LaTeX figures")
    figures_subparsers = figures_parser.add_subparsers(dest="figures_command", required=True)

    create = figures_subparsers.add_parser("create", help="Create a new figure")
    create.add_argument("name", help="Name of the figure")
    create.add_argument("path", nargs="?", help="Optional path to create figure in")
    create.set_defaults(func=handle_figures_create)

    edit = figures_subparsers.add_parser("edit", help="Edit a figure")
    edit.add_argument("path", nargs="?", help="Optional path to the figure")
    edit.set_defaults(func=handle_figures_edit)

    watch = figures_subparsers.add_parser("watch", help="Watch figures for changes")
    watch.add_argument("--kill", action="store_true", help="Kill the watch process")
    watch.add_argument("path", nargs="?", help="Optional path to watch")
    watch.set_defaults(func=handle_figures_watch)

    shortcut = figures_subparsers.add_parser("shortcut-manager", help="Manage shortcuts for figures")
    shortcut.set_defaults(func=handle_figures_shortcut_manager)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
