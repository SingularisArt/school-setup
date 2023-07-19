Managing LaTeX Lecture Notes
============================

<!-- vim-markdown-toc GFM -->

* [Demos](#demos)
* [Features](#features)
* [Directory Structure Explained](#directory-structure-explained)
  * [The `assignments` folder](#the-assignments-folder)
    * [The `graded-assignments` folder](#the-graded-assignments-folder)
    * [The `my-assignments` folder](#the-my-assignments-folder)
      * [The `bibtex-files` folder](#the-bibtex-files-folder)
      * [The `image-files` folder](#the-image-files-folder)
      * [The `latex-files` folder](#the-latex-files-folder)
      * [The `pdf-files` folder](#the-pdf-files-folder)
      * [The `yaml-files` folder](#the-yaml-files-folder)
    * [The `online-assignments` folder](#the-online-assignments-folder)
  * [The `books` folder](#the-books-folder)
  * [The `figures` folder](#the-figures-folder)
  * [The `chapters` and `lectures` folder](#the-chapters-and-lectures-folder)
  * [The `papers` folder](#the-papers-folder)
  * [The `UltiSnips` folder](#the-ultisnips-folder)
  * [The `info.yaml` file](#the-infoyaml-file)
  * [The `master.tex` file](#the-mastertex-file)
  * [Getting everything ready](#getting-everything-ready)
* [Setup](#setup)
  * [Example Setup](#example-setup)
  * [Configuration](#configuration)

<!-- vim-markdown-toc -->

## Demos

GO HERE

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

When I'm taking notes during a lecture or over zoom, I use the first option, but
when I'm taking notes from a book, I use the second option. In my `master.tex`,
I always have the following at the very top (before including the preamble
file):
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
│   ├── graded-assignments
│   │   ├── assignment-01.pdf
│   │   └── ...
│   ├── my-assignments
│   │   ├── bibtex-files
│   │   │   ├── assignment-01.bib
│   │   │   └── ...
│   │   ├── image-files
│   │   │   ├── assignment-01.png
│   │   │   └── ...
│   │   ├── latex-files
│   │   │   ├── assignment-01.tex
│   │   │   └── ...
│   │   ├── Makefile
│   │   ├── master.pdf
│   │   ├── master.tex
│   │   ├── pdf-files
│   │   │   ├── assignment-01.pdf
│   │   │   └── ...
│   │   ├── preamble.tex
│   │   └── yaml-files
│   │       ├── assignment-01.yaml
│   │       └── ...
│   └── online-assignments
│       ├── assignment-01.pdf
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
├── chapters
│   ├── chap-01.pdf
│   └── ...
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
│   ├── lec-01.tex
│   └── ...
├── Makefile
├── master.pdf
├── master.tex
├── notes.md
├── papers
│   ├── paper-01.pdf
│   └── ...
├── preamble.tex
└── UltiSnips
    └── tex.snippets
```

### The `assignments` folder

The `assignments` folder is broken up into 3 folders for organization.

#### The `graded-assignments` folder

Place all your graded assignments in this folder.

#### The `my-assignments` folder

This folder's broken up into multiple folders for organization purposes.

##### The `bibtex-files` folder

Place all your bibliography files in this folder.

##### The `image-files` folder

Place all your images in this folder. If you have multiple images for one
assignment, you can create a folder with the same name as your assignments and
place them all in there as such:
```
.
└── my-assignments
    └── image-files
        ├── image-01.png
        ├── image-02.png
        └── ...
```

##### The `latex-files` folder

Place all your latex files in this folder. Here's an example latex assignment
file ([link]()):
```latex
\begin{problem}
  ...
\end{problem}

\begin{probsolution}
  ...
\end{probsolution}

\newpage

\begin{problem}
  ...
\end{problem}

\begin{probsolution}
  ...
\end{probsolution}
```

##### The `pdf-files` folder

Place your final pdf files in this folder.

##### The `yaml-files` folder

Place all your yaml files in this folder. Here's the yaml template you need
to use:
```yaml
title: Any Title you want
due_date: 12-31-10
url: URL
submitted: true/false
grade: 100.0
number: 1
```

**NOTE:** Make sure to keep all your file names consistent. Here's an example:
```
.
├── graded-assignments
│   └── assignment-01.pdf
├── my-assignments
│   ├── bibtex-files
│   │   └── assignment-01.bib
│   ├── image-files
│   │   └── assignment-01.png
│   ├── latex-files
│   │   └── assignment-01.tex
│   ├── Makefile
│   ├── master.tex
│   ├── pdf-files
│   │   └── assignment-01.pdf
│   ├── preamble.tex
│   └── yaml-files
│       └── assignment-01.yaml
└── online-assignments
    └── assignment-01.pdf
```

And here's what the `assignment-01.yaml` might look like:
```yaml
title: Graded Assignment 1
due_date: 10-15-23
url: https://google.com
submitted: true
grade: 97.5
number: 1
```

#### The `online-assignments` folder

Place all your assignment files given to you by your instructor in this folder.

### The `books` folder

If you have a pdf version of your book and you don't have any solutions, then
place the book in the `books` folder by itself, as such:
```
.
└── book-title.pdf
```

If you have the solutions to the book as one single pdf, create a folder inside
the `books` folder and place both the pdf of the book and the solutions inside
as such:
```
.
└── book-title
    ├── master.pdf
    └── solutions.pdf
```

If your solutions are broken up into multiple pdf files, create a sub-folder
titled `solutions` and place them in there as such:
```
.
└── book-title
    ├── master.pdf
    └── solutions
        ├── chap-01.pdf
        ├── chap-02.pdf
        └── ...
```
You can give the solution files any name you want.

### The `figures` folder

I use inkscape to create my figures. When you want to save your figure, save it
as a `pdf`, `pdf_tex`, and `svg`. I store the figure in folders based on the
lecture/chapter number. Here's an example
```
.
└──figures
    ├── lec-01
    │   ├── figure-01.pdf
    │   ├── figure-01.pdf_tex
    │   ├── figure-01.svg
    │   └── ...
    ├── ...
    ├── chap-01
    │   ├── figure-01.pdf
    │   ├── figure-01.pdf_tex
    │   ├── figure-01.svg
    │   └── ...
    └── ...
```
I then use the `\incfig` command I defined to include the figure ([link]()).

### The `chapters` and `lectures` folder

If I'm taking an online course, I use the `chapters` folder to store all my
notes. If I'm taking an in-person or remote course, I'll use the `lectures`
folder to store my notes. What ever you use, make sure to provide that
information in the [`info.yaml`](#the-info.yaml-file) file. Here's the basic
template I use for my notes ([link]()):
```latex
\nte[Side Notes]{Apr 04 2023 Mon (11:00:53)}{Title Goes Here}
\label{note_01:title_goes_here}



\newpage
```

Which produces the following:

### The `papers` folder

A lot of times, my courses require me to read research papers. So, I download
them and store them in this folder.

### The `UltiSnips` folder

TODO

### The `info.yaml` file

Here's an example `info.yaml` file:
```yaml
title: "Calculus 3"
topic: "Mathematics"
class_number: 12345
short: "MTH-253"
author: "YOUR NAME"
term: "NAME Term"
faculty: "Faculty of NAME"
college: "COLLEGE NAME"
location: "LOCATION Campus, BUILDING ROOM"
year: 2023
start_date: "Apr 04 2023 Tue (12:00:00)"
end_date: "Jun 15 2023 Thu (12:00:00)"
start_time: "11:00:00" # 24 hour
end_time: "13:20:00" # 24 hour
days: "MO,TU,WE,TH,FR,SA,SUN"
url: "URL"
type: "In Person" # or Remote/Online
notes_type: "lectures" # or chapters
professor:
  name: "Name"
  email: "Email"
  phone-number: "Phone Number"
  office: "Office"
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
  % end notes

  \listnotes
\end{document}
```
The `working` parameter passed to the document class is important. If you're
still working on taking notes, keep that there so you can use the note commands
I've defined ([link]()). I then use the `\includenote` command to load the note
file in addition to setting up a few settings ([link]()).

### Getting everything ready

Before you start manually setting up all the files and folders yourself, I've
already done that for you. You need something called `the templates folder`. You
can find an example [here](./example-setup/template_files). This folder contains
all the files and folders required, which you can then use distribute to all
your future courses. I created a script for that. All you need to do is setup
the `info.yaml` file, then run the `./main.py -ic` or `./main.py
--init-courses`. It will then generate and fill in everything missing.

**NOTE:** You must first read the [setup](#setup) section to make sure you've
got the links to everything working.

## Setup

Run the following install commands:
```bash
git https://github.com/SingularisArt/school-setup/
cd school-setup
./install
```

### Example Setup

I've already created an example setup [here](./example-setup) you can use to
understand what's going on.

### Configuration

TODO

The configuration file's located at `$HOME/.config/lesson-manager/config.yaml`.
Here are all the variable meanings:

- `calendar_id`: The id of the calendar. By default, it's `primary`.
- `drive_folder_id`: The id of the google drive folder that you want to use to
  sync your notes to.
- `code_dir`: Where you cloned the code to.
- `editor`: The text editor you want to use.
- `terminal`: The terminal you want to use.
- `pdf_viewer`: The pdf viewer you want to use.
- `create_readme_file`: If you want README.md files created when initializing
  the courses.
- `highlight_current_course`: If you want the currently selected course to be
  highlighted.
- `notes_dir`: The root directory of your notes.
- `root`: The root directory of your current course notes.
- `templates_dir`: The location to the templates folder.
- `current_course`: The directory you want to use to store the current course.
- `books_dir`: Where you store your books in regards to the current course.
- `figures_dir`: Where you store your figures in regards to the current course.
- `assignments_dir`: The root directory where you store all your assignments in
  regards to the current course.
- `graded_assignments_folder`:
- `my_assignments_folder`: 
- `online_assignments_folder`:
- `my_assignments_image_folder`:
- `my_assignments_bibtex_folder`:
- `my_assignments_latex_folder`:
- `my_assignments_yaml_folder`:
- `my_assignments_pdf_folder`:
- `date_format`:
- `home`:
- `user`:
- `rofi_options`:
- `folders`:
- `files`:
