AI-Powered Real-Time Spell Checker and Suggestion System

Project Overview

This is a Python-based desktop application that provides real-time spell-checking and correction suggestions, mimicking the functionality of modern word processors like Google Docs or MS Word.

The system flags misspelled words with a red underline as the user types, and provides intelligent, probabilistic correction suggestions via a right-click context menu.

Features

Real-Time Detection: Words are checked immediately upon key release using event binding.

Visual Highlighting: Misspelled words are tagged with a red underline using Tkinter's text tags.

Intelligent Suggestions: Uses the pyspellchecker library, which relies on Levenshtein distance and word frequency to offer the most probable correction.

Quick Correction: Right-click a misspelled word to select a suggested replacement.

Custom Dictionary: Option to "Add to Dictionary" for session-based inclusion of new or proper nouns.

Undo/Redo: Supports standard Ctrl+Z and Ctrl+Y functionality.

Technical Requirements

The application is built using the following components:

Component

Role

Technology/Concept

GUI

User Interface

Python Tkinter

Intelligence

Spell Check Logic & Suggestions

pyspellchecker Library

Speed

Dictionary Lookup

Hash Map (Internal to pyspellchecker)

Core Logic

Real-Time Response

Event-Driven Programming (<KeyRelease>)

Installation and Setup

Prerequisites

You must have Python 3.6 or newer installed on your system.

1. Install Dependencies

Open your terminal or command prompt and install the required library:

pip install pyspellchecker


2. Run the Application

Save the main project file as spell_checker_app.py. Then, execute it from your terminal:

python spell_checker_app.py


Usage

Start Typing: Begin entering text into the main window.

Misspelling: Any word not found in the dictionary will be immediately underlined in red.

Get Suggestions: Right-click on the misspelled word. A menu will appear with up to 7 correction candidates.

Correct Word: Click the desired suggestion to instantly replace the misspelled word.

Exit: Close the application using the "X" button or the menu. A confirmation box will appear.

Project Report

A detailed project report (Spell_Checker_Project_Report.md) is also included, covering the abstract, objectives, algorithm description, and data structures used.
