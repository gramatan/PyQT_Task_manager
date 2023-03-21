import sys

from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QApplication, QMessageBox
from PyQt6.QtGui import QIcon

from database import init_database
from stopwatch_widget import StopwatchWidget
from task_table_widget import TaskTableWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Task Tracker")
        self.setWindowIcon(QIcon("images/logo.png"))

        self.stopwatch_widget = StopwatchWidget()
        self.task_table_widget = TaskTableWidget()

        self.stopwatch_widget.task_started.connect(self.task_table_widget.start_task)
        self.stopwatch_widget.task_stopped.connect(self.task_table_widget.load_tasks)
        self.stopwatch_widget.task_paused.connect(self.task_table_widget.edit_task)
        self.task_table_widget.task_added.connect(self.stopwatch_widget.load_tasks)
        self.task_table_widget.task_updated.connect(self.stopwatch_widget.load_tasks)
        self.task_table_widget.task_deleted.connect(self.stopwatch_widget.load_tasks)

        self.task_table_widget.load_tasks()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stopwatch_widget)
        main_layout.addWidget(self.task_table_widget)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)

    def closeEvent(self, event):
        if self.stopwatch_widget.timer.isActive():
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Timer is running")
            msg_box.setText("The timer is currently running. Are you sure you want to close the application?")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            result = msg_box.exec()

            if result == QMessageBox.StandardButton.Yes:
                self.stopwatch_widget.stop_stopwatch()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


if __name__ == "__main__":
    init_database()
    app = QApplication([])

    window = MainWindow()
    window.resize(350, 700)

    screen = window.screen().availableSize()
    position = window.screen().availableSize()
    x = (screen.width() - window.frameSize().width()) - 20
    y = 80
    window.move(x, y)

    window.show()

    sys.exit(app.exec())
