Managing LaTeX Lecture Notes
============================

<!-- vim-markdown-toc GFM -->

* [Demos](#demos)
* [Features](#features)
* [Directory Structure Explained](#directory-structure-explained)
  * [The `assignments` folder](#the-assignments-folder)
  * [The `books` folder](#the-books-folder)
  * [The `figures` folder](#the-figures-folder)
  * [The `chapters` and `lectures` folder](#the-chapters-and-lectures-folder)
  * [The `papers` folder](#the-papers-folder)
  * [The `UltiSnips` folder](#the-ultisnips-folder)
  * [The `info.yaml` file](#the-infoyaml-file)
  * [The `master.tex` file](#the-mastertex-file)
  * [Getting everything ready](#getting-everything-ready)
* [How to use](#how-to-use)
* [Shortcuts](#shortcuts)
  * [SXHKD](#sxhkd)
* [Setup](#setup)
  * [Install](#install)
  * [Example Setup](#example-setup)
  * [Configuration](#configuration)

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

I take two types of notes.
1. Lecture notes
2. Chapter notes

When I'm taking notes during a lecture or over zoom, I use the first option, but when I'm taking notes from a book, I use the second option. In my `master.tex`, I always have the following at the very top (before including the preamble file):
```latex
% If I'm taking chapter notes
\def\lecorchap{Chapter}
\def\figloc{figures/lec}
\def\noteloc{lectures/lec}
% If I'm taking lecture notes
\def\lecorchap{Lecture}
\def\figloc{figures/chap}
\def\noteloc{chapters/chap}
```

Here's a quick overview of how the directory structure of a course looks like:
```
.
├── assignments
│   ├── graded-assignments
│   │   ├── written-homework-02.pdf
│   │   └── ...
│   ├── my-assignments
│   │   ├── bibtex-files
│   │   │   ├── written-homework-01.bib
│   │   │   └── ...
│   │   ├── image-files
│   │   │   ├── written-homework-01.png
│   │   │   └── ...
│   │   ├── latex-files
│   │   │   ├── written-homework-01.tex
│   │   │   └── ...
│   │   ├── Makefile
│   │   ├── master.tex
│   │   ├── pdf-files
│   │   │   ├── written-homework-01.pdf
│   │   │   └── ...
│   │   ├── preamble.tex
│   │   ├── sympy-scripts
│   │   │   ├── written-homework-01.py
│   │   │   └── ...
│   │   └── yaml-files
│   │       ├── written-homework-01.yaml
│   │       └── ...
│   ├── online-assignments
│   │   ├── written-homework-01.pdf
│   │   └── ...
│   └── solution-keys
│       ├── latex-files
│       │   ├── written-homework-01.tex
│       │   └── ...
│       ├── Makefile
│       ├── master.tex
│       ├── pdf-files
│       │   ├── written-homework-01.pdf
│       │   └── ...
│       └── preamble.tex
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
├── chapters
│   ├── chap-01.tex
│   └── ...
├── exams
│   ├── info.yaml
│   ├── review
│   │   ├── answers
│   │   │   ├── answer-sheet-01.pdf
│   │   │   └── ...
│   │   └── practice
│   │       ├── practice-sheet-01.pdf
│   │       └── ...
│   └── solution-keys
│       ├── latex-files
│       │   ├── exam-01.tex
│       │   └── ...
│       └── pdf-files
│           ├── exam-01.pdf
│           └── ...
├── figures
│   ├── lec-01
│   │   ├── figure-01.pdf
│   │   ├── figure-01.pdf_tex
│   │   ├── figure-01.svg
│   │   └── ...
│   ├── chap-01
│   │   ├── figure-01.pdf
│   │   ├── figure-01.pdf_tex
│   │   ├── figure-01.svg
│   │   └── ...
│   └── ...
├── info.yaml
├── intro.tex
├── lectures
│   ├── lec-01.tex
│   └── ...
├── Makefile -> /home/singularis/Documents/school-notes/College/Year-2/fall/_files/Makefile
├── master.aux
├── master.pdf
├── master.tex
├── notes.md
├── online-lecture-notes
│   ├── lec-01-annotated.pdf
│   ├── lec-01-blank.pdf
│   └── ...
├── papers
│   ├── paper-01.pdf
│   └── ...
├── preamble.tex
├── sympy-scripts
│   ├── script-01.py
│   └── ...
└── UltiSnips
    └── tex.snippets
```

### The `assignments` folder

This folder contains all the assignments for the course. You can break it up however you want. Just make sure you keep all the filetypes away from each other. For example, you can't do something like this:
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
It might work, but it's not recommended. For an idea of how I break up my assignments, take a look at the [example setup](./example-setup/current-course/assignments/). Once you break up your files, you then pass the location of those folders to the `config.yaml` file. Take a look [here](#configuration) for more information.

**NOTE:** You don't need to have all of these stuff exactly. If some of your notes are even in `html`, you can create a folder for that and pass it to the `config.yaml` file. An example of that would be:
```yaml
html_folder: "my-assigments/html-files"
```

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

I use inkscape to create my figures. When you want to save your figure, save it as a `pdf`, `pdf_tex`, and `svg`. I store the figure in folders based on the lecture/chapter number. Here's an example
```
.
└── figures
    ├── lec-01
    │   ├── figure-01.pdf
    │   ├── figure-01.pdf_tex
    │   ├── figure-01.svg
    │   └── ...
    ├── chap-01
    │   ├── figure-01.pdf
    │   ├── figure-01.pdf_tex
    │   ├── figure-01.svg
    │   └── ...
    └── ...
```
I then use the `\incfig` command I defined to include the figure ([link]()).

### The `chapters` and `lectures` folder

If I'm taking an online course, I use the `chapters` folder to store all my notes. If I'm taking an in-person or remote course, I'll use the `lectures` folder to store my notes. What ever you use, make sure to provide that information in the [`info.yaml`](#the-info.yaml-file) file. Here's the basic template I use for my notes ([link]()):
```latex
\nte[Side Notes]{Apr 04 2023 Mon (11:00:53)}{Title Goes Here}



\newpage
```

Which produces the following:

### The `papers` folder

A lot of times, my courses require me to read research papers. So, I download them and store them in this folder.

### The `UltiSnips` folder

I use neovim to take notes along with the UltiSnips plugin. I store my custom course specific snippets in this folder.

### The `info.yaml` file

Here's an example `info.yaml` file:
```yaml
---
title: "Applied Linear Algebra I"
topic: "Mathematics"
class_number: 1234
short: "MTH-261"
author: "Hashem A. Damrah"
term: "Fall 2023"
faculty: "Mathematics"
college: "Portland Community College"
location: "Sylvania Campus, SS 114"
year: 2023
start_date: "Sep 26 2023 Tue (12:00:00)"
end_date: "Dec 14 2023 Thu (12:00:00)"
start_time: "14:00:00"
end_time: "16:20:00"
days: "TU,TH"
url: "URL"
type: "In-person" # or Online/Remote
notes_type: "lectures" # or chapters
professor:
  name: "NAME"
  email: "EMAIL"
  phone-number: "PHONE NUMBER"
  office: "OFFICE"
```

### The `master.tex` file

Here's an example `master.tex` file:
```latex
\documentclass[working]{report}

\def\class{report}
\def\lecorchap{Chapter}
\def\figloc{figures/lec}
\def\noteloc{lectures/lec}

\setcounter{tocdepth}{2}

\input{preamble.tex}

\title{Title}
\author{Author}
\date{Date}

\newcommand{\linktootherpages}{https://singularisart.github.io/notes}
\newcommand{\shortlinkname}{singularisart.github.io/notes}
\newcommand{\term}{TERM}
\newcommand{\academicyear}{$YEAR$}
\newcommand{\faculty}{FACULTY}
\newcommand{\location}{LOCATION}
\newcommand{\lecturer}{LECTURER}

\setlength{\tabcolsep}{16pt}
\renewcommand\arraystretch{1.8}

\begin{document}
  \createintro
  \newpage

  % start notes
  \includenote{1}
  \includenote{2}
  \includenote{3}
  ...
  \includenote{n}
  % or \includenotes{1}{n}
  % end notes

  \listnotes
\end{document}
```
I use the `\includenote` command to load the note file in addition to setting up a few settings ([link]()). If I'm loading notes between a range, like 2 to 6, I use the `\includenotes` command ([link]()).

### Getting everything ready

Before you start manually setting up all the files and folders yourself, I've already done that for you. You need something called `the templates folder`. You can find an example [here](./example-setup/template_files). This folder contains all the files and folders required, which you can then use distribute to all your future courses. I created a script for that. All you need to do is setup the `info.yaml` file for all courses, then run the `./main.py -ic` or `./main.py --init-courses`. It will then generate and fill in everything missing.

**NOTE:** You must first read the [setup](#setup) section to make sure you've
got the links to everything working.

## How to use

Once you have everything setup, here are the following commands you can use:

- **`./main.py -h`**: Shows the help menu.
- **`./main.py -ca`**: Parses your google calendar and shows you the next class.
- **`./main.py -gc "12345,6789"`**: Gets the courses' info from the CRN number (only works for PCC courses so far).
- **`./main.py -ic`**: Initializes all the courses. Only run this once you've completed the `info.yaml` file for each course.
- **`./main.py -ra`**: Shows you all the assignments for the current course via rofi.
- **`./main.py -rb`**: Shows you all the books for the current course via rofi.
- **`./main.py -rc`**: Shows you all the courses via rofi.
- **`./main.py -rn`**: Shows you all the notes for the current course via rofi.
- **`./main.py -rsn`**: Strips all the notes for the current course via rofi.
- **`./main.py -sn`**: Sources all the notes for the current course via rofi.
- **`./main.py -yn`**: Syncs all the notes for the current course to google drive.

## Shortcuts

Instead of typing out the full command every time, I've created [shortcuts](./shortcut-manager.sh) for you. They come with all the commands you can run directly from the `./main.py` file, along with a bunch of other nice ones. They are as follows (run like `./shortcut-manager.sh LETTER`)`):

- **`o`**: Open my class notes.
- **`O`**: List all online notes from professor.
- **`i`**: List all inkscape figures.
- **`I`**: Create inkscape figure with template.
- **`w`**: Open current course in browser.
- **`y`**: Open the current course's yaml file.
- **`p`**: Search through all the papers.
- **`k`**: Open the `notes.md` file for the current course.
- **`K`**: Open the `notes.md` file from the root directory.
- **`m`**: Open the `master.tex` file.
- **`a`**: Lists all the current course's assignments.
- **`b`**: Lists all the current course's books.
- **`c`**: Lists all the courses.
- **`n`**: Lists all the current course's notes.
- **`s`**: Lets you source specific notes.
- **`S`**: Syncs your notes to the drive.

### SXHKD

Instead of manually running `./shortcut-manager.sh a` every time, I use `sxhkd` to manage my shortcuts. Here's how I do it:
```conf
alt + {a-z}
  bash ~/school-setup/shortcut-manager.sh {a-z}
alt + {A-Z}
  bash ~/school-setup/shortcut-manager.sh {A-Z}
```

## Setup

### Install

Run the following commands:
```bash
git clone https://github.com/SingularisArt/school-setup/
cd school-setup
./install
```

### Example Setup

I've already created an example setup [here](./example-setup) you can use to understand what's going on. If you want to use the provided example, run the following commands:
```bash
cd ~/
git clone https://github.com/SingularisArt/school-setup/
cd school-setup
./install
```

### Configuration

The configuration file's located at `$HOME/.config/lesson-manager/config.yaml`. Here are all the variable meanings:

- **`calendar_id`**: The Google Calendar ID for syncing events. Replace "primary" with your actual Google Calendar ID.
- **`drive_folder_id`**: The Google Drive folder ID for syncing notes. Replace "ID" with the appropriate folder ID in your Google Drive.

- **`editor`**: Your preferred text editor, such as "nvim" or "vim". Modify this field based on your editor of choice.
- **`terminal`**: Your preferred terminal emulator, like "kitty" or "gnome-terminal". Adjust this parameter to your terminal preference.
- **`pdf_viewer`**: Your preferred PDF viewer, such as "zathura" or "evince". Change this based on your preferred PDF application.

- **`create_readme_file`**: Set to `true` to automatically create README files for each course.
- **`highlight_current_course`**: Set to `true` to highlight the current course in the Rofi menu.

- **`notes_dir`**: Root directory for storing notes. Modify this path to your preferred notes directory.
- **`root`**: Root directory for courses. Adjust this path to your preferred courses directory.
- **`templates_dir`**: Directory containing template files. Modify this path if your templates are stored elsewhere.
- **`current_course`**: Path to the file tracking the current course.

- **`books_dir`**: Directory for storing books related to the current course.
- **`figures_dir`**: Directory for storing figures related to the current course.

- **`date_format`**: Set the format for displaying dates. Adjust according to your preferred date format.

- **`home`**: Your home directory. Usually detected automatically but can be set manually if needed.
- **`user`**: Your username. Similar to `home`, this is often automatically detected.

- **`trash_dir`**: Directory for the trash bin. Deleted files will be moved here.

- **`assignments_dir`**: Directory for storing assignments.
- **`assignment_folders`**: Subfolders for different types of assignments (e.g., Bibtex files, LaTeX files).

- **`exams_dir`**: Directory for storing exams.
- **`exam_solution_keys`**: Subfolders for exam solution keys.
- **`exam_review`**: Subfolders for exam review materials.

- **`rofi_options`**: Customize Rofi options for a better interactive experience. Modify this list as needed.

- **`folders`**: List all the folders you want to be created when you initiate your courses.
- **`files`**: List all files you want to be either symlinked or copied from the templates folder when you initiate your courses.
