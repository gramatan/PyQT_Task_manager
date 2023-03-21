from PyQt6.QtCore import QTime, pyqtSignal
from PyQt6.QtWidgets import QTableWidgetItem, QInputDialog, QAbstractItemView

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QHBoxLayout

from database import create_connection


class TaskTableWidget(QWidget):
    task_added = pyqtSignal()
    task_updated = pyqtSignal()
    task_deleted = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Task", "Day", "Week", "Spent"])
        self.table.hideColumn(0)
        self.table.setColumnWidth(1, 160)
        self.table.setColumnWidth(2, 20)
        self.table.setColumnWidth(3, 20)
        self.table.setColumnWidth(4, 40)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.load_tasks()

        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_task)

        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(self.edit_task)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_task)

        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)

        layout = QVBoxLayout(self)
        layout.addWidget(self.table)
        layout.addLayout(button_layout)

    def load_tasks(self):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT tasks.id, tasks.name, tasks.daily_target, tasks.weekly_target, COALESCE(SUM(strftime('%s', logs.stop_timestamp) - strftime('%s', logs.start_timestamp)), 0) as time_spent
            FROM tasks
            LEFT JOIN logs ON tasks.id = logs.task_id
            GROUP BY tasks.id
        """)
        tasks = cursor.fetchall()

        self.table.setRowCount(0)

        for i, task in enumerate(tasks):
            self.table.insertRow(i)
            for j, value in enumerate(task):
                if j == 4:
                    value = QTime(0, 0).addSecs(value).toString('hh:mm:ss')
                item = QTableWidgetItem(str(value))
                self.table.setItem(i, j, item)
        conn.close()

    def start_task(self, task_id):
        pass    # there were some thoughts about what to do when timer starts, but finally i decide to skip it

    def add_task(self):
        task_name, ok = QInputDialog.getText(self, "Add Task", "Task name:")
        if ok and task_name:
            daily_target, ok = QInputDialog.getInt(self, "Add Task", "Daily target (minutes):", value=0, min=0)
            if not ok:
                return
            weekly_target, ok = QInputDialog.getInt(self, "Add Task", "Weekly target (minutes):", value=0, min=0)
            if not ok:
                return

            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (name, daily_target, weekly_target) VALUES (?, ?, ?)",
                           (task_name, daily_target, weekly_target))
            conn.commit()
            conn.close()

            self.load_tasks()
            self.task_added.emit()

    def edit_task(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return

        selected_item = selected_items[0]
        selected_row = self.table.row(selected_item)

        task_id = int(self.table.item(selected_row, 0).text())
        task_name = self.table.item(selected_row, 1).text()
        daily_target = int(self.table.item(selected_row, 2).text())
        weekly_target = int(self.table.item(selected_row, 3).text())

        new_task_name, ok = QInputDialog.getText(self, "Edit Task", "Task name:", text=task_name)
        new_daily_target, ok = QInputDialog.getInt(self, "Edit Task", "Daily target (minutes):", value=daily_target, min=0)
        if not ok:
            return
        new_weekly_target, ok = QInputDialog.getInt(self, "Edit Task", "Weekly target (minutes):", value=weekly_target, min=0)
        if not ok:
            return

        if ok and new_task_name:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE tasks SET name=?, daily_target=?, weekly_target=? WHERE id=?",
                           (new_task_name, new_daily_target, new_weekly_target, task_id))
            conn.commit()
            conn.close()

            self.load_tasks()
            self.task_updated.emit()

    def delete_task(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return

        selected_item = selected_items[0]
        selected_row = self.table.row(selected_item)

        task_id = int(self.table.item(selected_row, 0).text())

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        conn.close()

        self.load_tasks()
        self.task_deleted.emit()
