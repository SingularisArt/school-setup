Managing LaTeX Lecture Notes
============================

<!-- vim-markdown-toc GFM -->

* [Demos](#demos)
* [Features](#features)
* [Directory Structure Explained](#directory-structure-explained)
  * [The `assignments` folder](#the-assignments-folder)
  * [The `books` folder](#the-books-folder)
  * [The `figures` folder](#the-figures-folder)
  * [The `papers` folder](#the-papers-folder)
  * [The `UltiSnips` folder](#the-ultisnips-folder)
  * [The `info.yaml` file](#the-infoyaml-file)
  * [The `master.tex` file](#the-mastertex-file)
* [How to use](#how-to-use)
  * [Stand alone Commands](#stand-alone-commands)
    * [`lesson-manager -h/--help`](#lesson-manager--h--help)
    * [`lesson-manager calendar`](#lesson-manager-calendar)
    * [`lesson-manager init-courses`](#lesson-manager-init-courses)
    * [`lesson-manager source-notes`](#lesson-manager-source-notes)
    * [`lesson-manager sync-notes`](#lesson-manager-sync-notes)
    * [`lesson-manager strip-notes`](#lesson-manager-strip-notes)
  * [Rofi Commands](#rofi-commands)
    * [`lesson-manager rofi assignments`](#lesson-manager-rofi-assignments)
    * [`lesson-manager rofi books`](#lesson-manager-rofi-books)
    * [`lesson-manager rofi courses`](#lesson-manager-rofi-courses)
  * [`lesson-manager rofi notes`](#lesson-manager-rofi-notes)
  * [Figure Commands](#figure-commands)
    * [`lesson-manager figures create <name> [path]`](#lesson-manager-figures-create-name-path)
    * [`lesson-manager figures edit [path/name]`](#lesson-manager-figures-edit-pathname)
    * [`lesson-manager figures watch [--kill]`](#lesson-manager-figures-watch---kill)
    * [`lesson-manager figures shortcut-manager [--kill]`](#lesson-manager-figures-shortcut-manager---kill)
  * [Figures](#figures)
* [Shortcuts](#shortcuts)
  * [SXHKD](#sxhkd)
* [Setup](#setup)
  * [Install](#install)
  * [Example Setup](#example-setup)
  * [Config file](#config-file)
    * [Calendar ID and Drive Folder ID](#calendar-id-and-drive-folder-id)
    * [Editor, Terminal, and PDF Viewer](#editor-terminal-and-pdf-viewer)
    * [Create Readme File and Highlight Current Course](#create-readme-file-and-highlight-current-course)
    * [Notes Directory, Root, Templates Directory, and Current Course](#notes-directory-root-templates-directory-and-current-course)
    * [Books Directory, Figures Directory, Assignments Directory, and Assignment Folders](#books-directory-figures-directory-assignments-directory-and-assignment-folders)
    * [Rofi Options](#rofi-options)
    * [Folders and Files](#folders-and-files)

<!-- vim-markdown-toc -->

## Demos

![assignments-display-1](https://github.com/SingularisArt/media/blob/master/school-setup/assignments-01.png?raw=true)
![assignments-display-2](https://github.com/SingularisArt/media/blob/master/school-setup/assignments-02.png?raw=true)
![courses](https://github.com/SingularisArt/media/blob/master/school-setup/courses.png?raw=true)
![notes](https://github.com/SingularisArt/media/blob/master/school-setup/notes.png?raw=true)
![source](https://github.com/SingularisArt/media/blob/master/school-setup/source.png?raw=true)
![sync](https://github.com/SingularisArt/media/blob/master/school-setup/sync.png?raw=true)

## Features

- Switch between courses with ease.
- Create lecture notes and assignments one keybinding.
- View the latex code, yaml code and all the pdf files for any assignment in a
  split second.
- Open any lecture note with a twinkle of an eye.
- Sync your notes to the cloud.
- Get notifications when your next class/lab starts.
- Source all lecture notes, the current one, the last two, specific lecture
  notes, or a range of lecture notes.
- Insane keymappings already setup for you.
- Beautiful UI, via Rofi.
- Easy to install.
- Will take about 5 minutes to setup after installation.

## Directory Structure Explained

Here's a quick overview of how the directory structure of a course looks like:
```
.
├── assignments
│   ├── graded-assignments
│   │   ├── written-homework-01.pdf
│   │   └── ...
│   ├── my-assignments
│   │   ├── bibtex-files
│   │   │   ├── homework-01.bib
│   │   │   └── ...
│   │   ├── image-files
│   │   │   ├── homework-01
│   │   │   │   ├── image-01.png
│   │   │   │   └── ...
│   │   │   └── ...
│   │   ├── latex-files
│   │   │   ├── homework-01.tex
│   │   │   └── ...
│   │   ├── Makefile
│   │   ├── master.tex
│   │   ├── pdf-files
│   │   │   ├── homework-01.pdf
│   │   │   └── ...
│   │   ├── preamble.tex -> /home/singularis/Documents/school-notes/University/_files/assignments/my-assignments/preamble.tex
│   │   └── yaml-files
│   │       ├── homework-01.yaml
│   │       └── ...
│   ├── online-assignments
│   │   ├── homework-01.pdf
│   │   └── ...
│   └── solution-keys
│       ├── written-homework-01.pdf
│       └── ...
├── books
│   ├── book-01.pdf
│   ├── book-02
│   │   ├── master.pdf
│   │   └── solutions
│   ├── book-03
│   │   ├── master.pdf
│   │   └── solutions
│   │       ├── chap-01.pdf
│   │       └── ...
│   └── ...
├── figures
│   ├── figure-01.pdf
│   ├── figure-01.pdf_tex
│   ├── figure-01.svg
│   └── ...
├── info.yaml
├── intro.tex
├── lectures
│   ├── lec-01.tex
│   └── ...
├── Makefile -> /home/singularis/Documents/school-notes/University/_files/Makefile
├── master.pdf
├── master.tex
├── notes.md
├── professor-notes
│   ├── lec-01-annotated.pdf
│   ├── lec-01-blank.pdf
│   └── ...
├── papers
│   ├── paper-01.pdf
│   └── ...
├── preamble.tex -> /home/singularis/Documents/school-notes/University/_files/preamble.tex
└── UltiSnips
    └── tex.snippets
```

### The `assignments` folder

This folder contains all the assignments for the course. You can break it up however you want. Just make sure you keep all the filetypes away from each other, i.e., all the `latex` files are in a folder, all the `yaml` files are in a folder, etc. For example, you can't do something like this:
```
.
└── assignments
    ├── graded-assignments
    │   ├── assignment-01.pdf
    │   └── ...
    └── my-assignments
        ├── files
        │   ├── assignment-01.bib
        │   ├── assignment-01.tex
        │   ├── assignment-01.yaml
        │   ├── assignment-01.pdf
        │   ├── assignment-01.py
        │   └── ...
        ├── Makefile
        ├── master.pdf
        └── master.tex
```
This will not work. For an idea of how I break up my assignments, take a look at the [example setup](./example-setup/current-course/assignments/). Once you break up your files, you then pass the location of those folders to the `config.yaml` file. Take a look [here](#configuration) for more information.

What's great about this setup is that it's so dynamic. Say, you use a bunch of `sympy` scripts or jupyter notebooks for your assignments. You can create a folder, call it `python-scripts` or something, and then pass the location of that folder to the `config.yaml` file:
```yaml
assignment_folders:
  ...
  python_scripts: "my-assignments/python-scripts"
  ...
```
Then, the program will automatically pick it up and display it in the rofi menu when you run the `lesson-manager rofi assignments` command.

### The `books` folder

If you have a pdf version of your book and you don't have any solutions, then place the book in the `books` folder by itself, as such:
```
.
└── book-01.pdf
```

If you have the solutions to the book as one single pdf, create a folder inside the `books` folder and place both the pdf of the book and the solutions inside as such:
```
.
└── book-02
    ├── master.pdf
    └── solutions.pdf
```

If your solutions are broken up into multiple pdf files, create a sub-folder titled `solutions` and place them in there as such:
```
.
└── book-03
    ├── master.pdf
    └── solutions
        ├── chap-01.pdf
        └── ...
```
You can give the solution files any name you want.

### The `figures` folder

I use inkscape to create my figures. When you want to save your figure, save it as a `pdf`, `pdf_tex`, and `svg`. I store figures in `figure` folder (duh). Here's an example
```
.
└── figures
    ├── figure-01.pdf
    ├── figure-01.pdf_tex
    ├── figure-01.svg
    └── ...
```
I then use the `\incfig` command I defined to include the figure:
```latex
\usepackage{import}
\newcommand\incfig[2][1]{
  \def\svgwidth{#1\columnwidth}
  \import{figures}{#2.pdf_tex}
}
```

### The `papers` folder

A lot of times, my courses require me to read research papers. So, I download them and store them in this folder.

### The `UltiSnips` folder

I use neovim to take notes along with the UltiSnips plugin. I store my custom course specific snippets in this folder.

### The `info.yaml` file

Here's an example `info.yaml` file:
```yaml
---
title: "Differential Geometry"
topic: "Mathematics"
class_number: 33103
short: "MTH-433"
author: "Hashem A. Damrah"
term: "Spring 2025"
faculty: "Faculty of Mathematics"
college: "University of Oregon"
location: "Peterson Hall 103"
year: 2025
start_date: "Mar 31 2025 Mon (00:00:00)"
end_date: "Jun 09 2025 Mon (00:00:00)"
start_time: "11:00"
end_time: "11:50"
days: "MO,TU,WE,TH,FR,SA,SU"
url: "URL"
professor:
  name: "Professor Name"
  email: "Professor Email"
  phone_number: "Professor Number"
  office: "Professor Office"
```

### The `master.tex` file

Here's an example `master.tex` file:
```latex
\documentclass[notitlepage]{report}

\input{preamble.tex}

\title{Differential Geometry}
\date{March 31, 2025}

\def\nlecturer{F. Last}
\def\nterm{Spring}
\def\nyear{$2025$}

\def\othernotes{singularisart.github.io/notes}
\def\faculty{Faculty of Mathematics}
\def\location{University of Oregon}

\begin{document}
  \createintro
  \newpage

  \chapter*{0 Introduction}
  \addcontentsline{toc}{chapter}{\numberline{0}Introduction}
  INTRODUCTION

  LECTURE NOTES
\end{document}
```

## How to use

To understand how the program actually works, take a look at the README located in the [root directory](./lesson-manager/) of the code. It explains how the program works, what each file is doing, and how to use it as an API. This README is more of a user guide, so you can get started quickly.

Once you have everything setup, here are the following commands you can use:

### Stand alone Commands

#### `lesson-manager -h/--help`

Shows the help menu.

#### `lesson-manager calendar`

This script hooks into your calendar, which you can configure in the `~/.config/lesson-manager/config.yaml`.

To get it working, follow step 1 and 2 of the [Google Calendar Python Quickstart](https://developers.google.com/calendar/quickstart/python), and place `credentials.json` in the `~/.config/lesson-manager/credentials/` directory.

I use the following polybar module:
```ini
[module/class-info]
type = custom/script
exec = TZ="America/Vancouver" lesson-manager calendar
click-left = sensible-browser "https://calendar.google.com/calendar/" -- &
interval = 60
tail = true
```

#### `lesson-manager init-courses`

This command initializes all the courses. Just make sure you have the `info.yaml` file in the root directory of each course, and that you have the `templates` folder all setup correctly. The script will then create all the necessary folders and files for you.

#### `lesson-manager source-notes`

This command will let you select which lecture notes you want to include in your `master.tex` file. Rofi will provide you with a few options to choose from:
- `current`: This will source the latest lecture note you took in the current course.
- `last two`: This will source the last two lecture notes you took in the current course.
- `previous`: This will source the previous lecture note you took in the current course.
- `all`: This will source all the lecture notes you took in the current course.
- `range`: If you want, you could specify a range of lecture notes, like `1-3`, or `1-8,10`, or `1-4,8,10-15`, etc.

One important thing is that, say, the first 3 lecture notes where on chapter 1, then the next few where on chapter 2, and so on. The program will automatically which lecture belongs to which chapter, and will source them accordingly. Here's an example of the content of the document in the `master.tex` file:
```latex
% notes start 0
\input{./lectures/lec-00.tex}
% notes end 0

\chapter{Curves}
\label{chap:curves}

% notes start 1-3
\input{./lectures/lec-01.tex}
\input{./lectures/lec-02.tex}
\input{./lectures/lec-03.tex}
% notes end 1-3

\chapter{Regular Surfaces}
\label{chap:regular_surfaces}

% notes start 4-6
\input{./lectures/lec-04.tex}
\input{./lectures/lec-05.tex}
\input{./lectures/lec-06.tex}
% notes end 4-6

\chapter{Gauss Maps}
\label{chap:gauss_maps}

% notes start 7-10
\input{./lectures/lec-07.tex}
\input{./lectures/lec-08.tex}
\input{./lectures/lec-09.tex}
\input{./lectures/lec-10.tex}
% notes end 7-10

\chapter{The Intrinsic Geometry of Surfaces}
\label{chap:the_intrinsic_geometry_of_surfaces}

% notes start 11-16
\input{./lectures/lec-11.tex}
\input{./lectures/lec-12.tex}
\input{./lectures/lec-13.tex}
\input{./lectures/lec-14.tex}
\input{./lectures/lec-15.tex}
\input{./lectures/lec-16.tex}
% notes end 11-16
```
It's important to keep the `notes start a-b` and `notes end a-b` comments, so the program can automatically source the lecture notes correctly. If you don't have those comments, the program will not be able to source the lecture notes correctly. If you don't want to include chapters, you can just do something like:
```latex
% notes start 0-16
\input{./lectures/lec-01.tex}
\input{./lectures/lec-02.tex}
\input{./lectures/lec-03.tex}
\input{./lectures/lec-04.tex}
\input{./lectures/lec-05.tex}
\input{./lectures/lec-06.tex}
\input{./lectures/lec-07.tex}
\input{./lectures/lec-08.tex}
\input{./lectures/lec-09.tex}
\input{./lectures/lec-10.tex}
\input{./lectures/lec-11.tex}
\input{./lectures/lec-12.tex}
\input{./lectures/lec-13.tex}
\input{./lectures/lec-14.tex}
\input{./lectures/lec-15.tex}
\input{./lectures/lec-16.tex}
% notes end 0-16
```

#### `lesson-manager sync-notes`

This command will sync your notes to the cloud. First, it will include all the lecture notes to your `master.tex` file, then it will compile the `master.tex` file to a pdf, and finally, it will upload the pdf to your Google Drive folder. You can configure the Google Drive folder in the `~/.config/lesson-manager/config.yaml` file.

#### `lesson-manager strip-notes`



### Rofi Commands

#### `lesson-manager rofi assignments`

This command will list all your assignments in the current course, via rofi. You can then select the assignment you want to view, and it will then list the latex, yaml, your submitted pdf, the professor's graded pdf, and the solution key for that assignment (if it doesn't exist, it will not show up). You can then select the file you want to view, and it will open it in your preferred editor or viewer, which, again, you can configure in the `~/.config/lesson-manager/config.yaml` file.

#### `lesson-manager rofi books`

This command will list all the books in the current course, via rofi. You can then select the book you want to view. If you only have the textbook, it will open it up in your preferred pdf viewer. If you have the textbook and along with the solutions. If your solutions are broken up into multiple pdf files, once you select the `solutions` option, it will then list all the solution files in a rofi menu, and you can select the one you want to view. If you have the solutions as one single pdf file, it will open that up directly.

#### `lesson-manager rofi courses`

This command will list all the courses you have, via rofi. You can then select the course you want to view, and it will set that as the current course, via symlinking the chose course to the `current_course` path in the `~/.config/lesson-manager/config.yaml` file. This will then allow you to use all the other commands, such as `lesson-manager rofi assignments`, `lesson-manager rofi books`, etc. I use the following `polybar` module to list the current course:
```ini
[module/current-course]
type = custom/script
exec = cat "/home/singularisart/.local/share/current_course" | sed 's/_/ /g' | sed 's/-/ /g'
click-left = lesson-manager rofi course
click-right = lesson-manager rofi notes
click-middel = lesson-manager rofi assignments
```

### `lesson-manager rofi notes`

This command will list all the lecture notes in the current course, via rofi. You can then select the lecture note you want to view, and it will open it in your preferred editor or viewer.

### Figure Commands

#### `lesson-manager figures create <name> [path]`

This command has a few options you could pass to it.

This will create a new figure with the name provided (something with `<...>` means it's mandatory, while something with `[<...>]` means it's optional), in the path provided (if not provided, it will just create the file in the current directory).

#### `lesson-manager figures edit [path/name]`

This will open a rofi menu with all the figures in the directory provided (if not provided, it will just open the current directory). If you pass it a file, it will automatically open it in inkscape, so you can edit it.

#### `lesson-manager figures watch [--kill]`

This will create a process in the background that will watch as you edit figures in inkscape, and when you save, it will automatically create a `pdf`, `pdf_tex`, and `svg` file for you, so you can use it in your latex documents. To kill the process, just pass `--kill` to the `watch` command, like so: `lesson-manager figures watch --kill`.

#### `lesson-manager figures shortcut-manager [--kill]`

This will create a process in the background that will monitor your keystrokes while you are in inkscape and will apply the styles based on your keystrokes. For example, if you type `d` `a`, you get a **d**otted **a**row, or if you type `d` `l`, you get a **d**ashed **l**ine, and so on. See [figures](#figures) for more information on how it works and how you can customize the keystrokes. To kill the process, just pass `--kill` to the `shortcut-manager` command, like so: `lesson-manager figures shortcut-manager --kill`.

### Figures

## Shortcuts

Instead of typing out the full command every time, I've created [shortcuts](./shortcut-manager.sh) for you. They come with all the commands you can run directly from the `lesson-manager` file, along with a bunch of other nice ones. They are as follows (run like `./shortcut-manager.sh LETTER`):

### SXHKD

Instead of manually running `./shortcut-manager.sh a` every time, I use `sxhkd` to manage my shortcuts. Here's how I do it:
```conf
alt + {a-z}
  bash /path/to/shortcut-manager.sh {a-z}
alt + {A-Z}
  bash /path/to/shortcut-manager.sh {A-Z}
```
Therefore, I just have to press `alt + a` to run `lesson-manager rofi assignments`, or `alt + b` to run `lesson-manager rofi books`, and so on. You can find how all the shortcut works in the [shortcut-manager.sh](./shortcut-manager.sh) file. Here's a quick overview of the shortcuts:
- `a`: List all assignments in the current course.
- `b`: List all books in the current course.
- `c`: List all courses you have.
- `n`: List all lecture notes in the current course.
- `f`: List all figures in the current course.
- `F`: Create a new figure in the current course.
- `s`: Source the lecture notes in the current course.
- `S`: Sync all the lecture notes in the current course to the cloud.
- `o`: Open the current course in your preferred editor.
- `O`: List all the professor's notes in the current course.
- `w`: Open the url of the current course in your browser.
- `y`: Open the `info.yaml` file of the current course in your preferred editor.
- `k`: Open the `notes.md` file of the current course in your preferred editor.
- `K`: Open the global `notes.md` file in your preferred editor.
- `m`: Open the `master.tex` file of the current course in your preferred editor.

## Setup

### Install

To install the program, run the following:
```bash
git clone https://github.com/SingularisArt/school-setup/
cd ./school-setup/lesson-manager/
pip3 install --user .
```
Now, you can run the program by typing `lesson-manager` in your terminal.

### Example Setup

I've already created an example setup [here](./example-setup) to understand how everything fits together better. If you want to use the provided example, run the command:
```bash
./install-example
```

### Config file

The config file for the program is located at `$HOME/.config/lesson-manager/config.yaml`. You can edit it to change the paths to your files and folders, as well as the editor/viewer you want to use for opening files. Here's an example of what the config file looks like:
```yaml
---
calendar_id: "primary"              # Your Google Calendar ID, usually "primary"
drive_folder_id: "notes_folder_id"  # Your Google Drive folder ID, where you want to sync your notes

editor: "nvim"
terminal: "kitty"
pdf_viewer: "zathura"

create_readme_file: true
highlight_current_course: true

notes_dir: "~/Documents/school-notes"
root: "~/Documents/school-notes/University/Year-1/spring"
templates_dir: "~/Documents/school-notes/University/_files"
current_course: "~/Documents/school-notes/current-course"
sourcing_notes_template: "\\input{#1}"

date_format: "%b %d %Y %a (%H:%M:%S)"
home: "/home/singularisart"
user: "singularisart"

# relative to current_course
books_dir: "books"
figures_dir: "figures"
assignments_dir: "assignments"
assignment_folders:
  bib_folder: "my-assignments/bibtex-files"
  tex_folder: "my-assignments/latex-files"
  yaml_folder: "my-assignments/yaml-files"
  pdf_folder: "my-assignments/pdf-files"
  graded_assignment: "graded-assignments"
  online_assignment: "online-assignments"
  solution_key: "solution-keys"

rofi_options:
  - "-markup-rows"
  - "-kb-row-down"
  - "Down"
  - "-kb-custom-1"
  - "Ctrl+n"
  - "-no-fixed-num-lines"

folders:
  - "assignments"
  - "assignments/graded-assignments"
  - "assignments/online-assignments"
  - "assignments/solution-keys"
  - "assignments/my-assignments"
  - "assignments/my-assignments/bibtex-files"
  - "assignments/my-assignments/image-files"
  - "assignments/my-assignments/latex-files"
  - "assignments/my-assignments/pdf-files"
  - "assignments/my-assignments/sympy-scripts"
  - "assignments/my-assignments/yaml-files"
  - "books"
  - "figures"
  - "papers"
  - "sympy-scripts"
  - "UltiSnips"

files:
  "assignments/my-assignments/preamble.tex": "symlink"
  "assignments/my-assignments/Makefile": "symlink"
  "Makefile": "symlink"
  "preamble.tex": "symlink"
  "UltiSnips/tex.snippets": "symlink"
  "assignments/my-assignments/master.tex": "copy"
  "intro.tex": "copy"
  "master.tex": "copy"
```

I know that this may look daunting, but it all makes perfect sense. I'll go in detail about each variable below. If you want to see an example of how the config file looks like, take a look at the [example setup](./example-setup/config.yaml).

#### Calendar ID and Drive Folder ID

These are just the IDs of your Google Calendar that has your classes, and the ID of the Google Drive folder, where you want to sync your notes to. You can find those IDs yourself, cause you're a big boi now.

#### Editor, Terminal, and PDF Viewer

These are pretty self explanatory. You can set them to whatever you want. The program will then use those programs to open the files you select in the rofi menu. For example, if you set the `editor` to `nvim`, then when you select a file in the rofi menu, it will open it in neovim.

#### Create Readme File and Highlight Current Course

These are just two boolean variables. If you set `create_readme_file` to `true`, then the program will create a `README.md` file in the root directory of the course. If you set `highlight_current_course` to `true`, then the program will highlight the current course in the rofi menu.

#### Notes Directory, Root, Templates Directory, and Current Course

- The `notes directory` is the root directory for all your notes. This maybe something like `~/Documents/school-notes`, or something.
- The `root` is the path to the folder where your courses are located. I have mine set to like `~/Documents/school-notes/University/Year-1/{fall,winter,spring}`, and I store all my course folders in there.
- The `templates directory` is the path to the folder where all your templates are located. This is where you can place the `the templates folder` I mentioned earlier. You'd place things that you use consistently throughout all your courses, such as the `premable.tex`, template of your `master.tex`, the `Makefile`, etc.
- The `current course` is the path to the folder where your current course is located. This is where the program will create all the symlinks to the files you need for the current course, such as the `master.tex`, `preamble.tex`, etc. You should place this folder somewhere that's easily accessible for you, such as `~/Documents/school-notes/current-course`. The program will then create all the necessary symlinks to the files in the `templates directory` and the `current course` folder.

#### Books Directory, Figures Directory, Assignments Directory, and Assignment Folders

All these variables are paths relative to the `current course` directory, i.e., where you store your `books`, `figures`, and `assignments`. Here's a quick overview of what each variable means:

- The `books directory` is the path to the folder where all your books are located.
- The `figures directory` is the path to the folder where all your figures are located.
- The `assignments directory` is the path to the folder where all your assignments are located. This is where you place everything that's related to your assignments, such as the `graded-assignments`, `my-assignments`, `online-assignments`, `solution-keys`, `python-files`, folders.
- The `assignments folders` is a list of all the items that you want to show up in the rofi menu when you select an assignment when running the `lesson-manager rofi assignments` command. You can add as many folders as you want, and the program will automatically pick them up and display them in the rofi menu. Just make sure to keep the naming consistent, i.e., if you have a latex file called `homework-01.tex`, then, it's solution key should be called `homework-01.pdf` placed in the `solution-keys` folder, its yaml file should be called `homework-01.yaml` placed in the `yaml-files` folder, and so on. This way, the program will automatically pick up the files and display them in the rofi menu when you select the assignment.

#### Rofi Options

These are the options that will be passed to rofi when you run the `lesson-manager rofi assignments`, `lesson-manager rofi books`, etc. commands. You can add any rofi options you want, and they will be passed to rofi when you run the command.

#### Folders and Files

- The `folders` variable is the list of all the folders that you want to create in the course directory when you run `lesson-manager init-courses` command. You can add as many folders as you want, and the program will automatically create them for you.

- The `files` variable is the list of all the files that you want to be created or symlinked in the course directory when you run `lesson-manager init-courses` command. You have a few options for each file:
  - If you set it to `symlink`, then the program will create a symlink to the file in the `templates directory`. This is useful for things that you want to stay consistent across all your courses, and when you modify one, you want it to be reflected in all the courses.
  - If you set it to `copy`, then the program will copy the file from the `templates directory` to the course directory. This is useful for creating templates, like the `master.tex`. You can even pass variables, like `TITLE`, or `DATE`, and the program will automatically replace them with the values you set in the `info.yaml` file.
  - If you set it to `create`, and the program will create the file in the course directory.
