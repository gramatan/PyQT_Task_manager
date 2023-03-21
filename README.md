## Task Tracker

Task Tracker is a simple, yet powerful desktop application that helps you manage your daily and weekly tasks, and monitor the time spent on each task. It is designed to improve your productivity and time management skills by providing an intuitive interface to create, edit, and delete tasks, as well as a built-in stopwatch to track the time spent on each task.
Features

* Easily add, edit, and delete tasks
* Set daily and weekly targets for each task
* Built-in stopwatch to track time spent on tasks
* Automatically logs time spent on tasks to a local SQLite database
* Provides a summary of time spent on each task
* Clean and intuitive user interface

Usage

1. Clone the repository or download the source code.
2. Make sure you have Python 3.11 installed on your system.
3. Install PyQt6 using pip install PyQt6.
4. Run main_window.py to start the application.

Dependencies

* Python 3.11
* PyQt6

Application Structure

* main_window.py: Contains the main window of the application, which includes the stopwatch and task table widgets.
* task_table_widget.py: Implements the task table widget for adding, editing, and deleting tasks.
* stopwatch_widget.py: Implements the stopwatch widget to track time spent on tasks.
* database.py: Contains functions for creating and initializing the SQLite database.

License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0).