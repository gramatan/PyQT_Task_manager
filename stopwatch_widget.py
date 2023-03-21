from PyQt6.QtCore import QTime, QTimer, Qt, QElapsedTimer, pyqtSignal
from PyQt6.QtGui import QFontDatabase, QFont, QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel, QHBoxLayout, QPushButton

from database import create_connection


class StopwatchWidget(QWidget):
    task_started = pyqtSignal(int)
    task_paused = pyqtSignal(int)
    task_stopped = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        self.task_combo = QComboBox()
        layout.addWidget(self.task_combo)

        self.load_tasks()

        self.time_label = QLabel("00:00:00")
        layout.addWidget(self.time_label)

        font_id = QFontDatabase.addApplicationFont("fonts/bruce-forever.regular.ttf")
        families = QFontDatabase.applicationFontFamilies(font_id)
        self.time_label.setFont(QFont(families[0], 20))
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.timer = QTimer()
        self.elapsed_timer = QElapsedTimer()
        self.timer.timeout.connect(self.update_stopwatch)
        self.start_time = None

        button_layout = QHBoxLayout()

        play_button = QPushButton('&Start')
        play_button.setIcon(QIcon("images/play.png"))
        play_button.clicked.connect(self.start_stopwatch)
        button_layout.addWidget(play_button)

        pause_button = QPushButton('&Pause')
        pause_button.setIcon(QIcon("images/pause.png"))
        pause_button.clicked.connect(self.pause_stopwatch)
        button_layout.addWidget(pause_button)

        stop_button = QPushButton('S&top')
        stop_button.setIcon(QIcon("images/stop.png"))
        stop_button.clicked.connect(self.stop_stopwatch)
        button_layout.addWidget(stop_button)

        layout.addLayout(button_layout)

        self.time = QTime(0, 0)

    def load_tasks(self):
        self.task_combo.clear()

        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()

        for task in tasks:
            self.task_combo.addItem(task[1], task[0])

        conn.close()

    def start_stopwatch(self):
        if not self.timer.isActive():
            self.timer.start(1000)
            self.elapsed_timer.start()
            self.start_time = QTime.currentTime()
            task_id = self.task_combo.currentData()
            if task_id is not None:
                self.task_started.emit(task_id)

    def pause_stopwatch(self):
        if self.timer.isActive():
            self.timer.stop()
            task_id = self.task_combo.currentData()
            if task_id is not None:
                self.task_paused.emit(task_id)

    def stop_stopwatch(self):
        if not self.timer.isActive():
            return

        self.timer.stop()

        elapsed_time = self.elapsed_timer.elapsed() // 1000
        task_id = self.task_combo.currentData()

        if task_id is None:
            return

        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM tasks WHERE id=?", (task_id,))
        task_name = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO logs (task_id, name, start_timestamp, stop_timestamp)
            VALUES (?, ?, datetime('now', 'localtime', '-' || ? || ' seconds'), datetime('now', 'localtime'))
        """, (task_id, task_name, elapsed_time))
        conn.commit()

        conn.close()
        self.reset_stopwatch()
        self.task_stopped.emit(task_id)

    def update_stopwatch(self):
        self.time = self.time.addSecs(1)
        self.update_stopwatch_display()

    def update_stopwatch_display(self):
        self.time_label.setText(self.time.toString('hh:mm:ss'))

    def reset_stopwatch(self):
        self.time = QTime(0, 0)
        self.update_stopwatch_display()