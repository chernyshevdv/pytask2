import sqlite3
import sys
from PyQt5 import QtGui, QtCore, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QAbstractScrollArea, QComboBox, QMessageBox
from PyQt5.QtGui import QFont, QPalette, QStandardItemModel
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
import mainwindow_ui

class TaskTableModel(QtCore.QAbstractTableModel):
    DB = "pytask.sqlite"
    TASKS_SQL_BASE = """
        SELECT t.id, p.title as project, `when`, u.name as delegate, t.estimate, t.priority, t.title 
        FROM tasks t LEFT JOIN projects p ON t.project_id=p.id 
        LEFT JOIN users u ON t.delegate_id=u.id
        """
    TASKS_SQL_COUNT = "SELECT count() FROM tasks"
    TASKS_HEADERS = ["id", "project", "when", "delegate", "estimate", "priority", "title"]

    def __init__(self):
        QAbstractTableModel.__init__(self)
        self._db = sqlite3.connect(TaskTableModel.DB)
        self._tasks_sql = TaskTableModel.TASKS_SQL_BASE
        self._task_count_sql = TaskTableModel.TASKS_SQL_COUNT
    
    def data(self, index: QModelIndex, role: int):
        l_row, l_col = index.row(), index.column()
        l_rs = self._db.execute(self._tasks_sql).fetchall()
        l_value = l_rs[l_row][l_col]
        if role == Qt.DisplayRole:
            return l_value
        elif role == Qt.TextAlignmentRole:
            if isinstance(l_value, int):
                return Qt.AlignRight
            else:
                return Qt.AlignLeft
    
    def rowCount(self, index: QModelIndex) -> int:
        return self._db.execute(self._task_count_sql).fetchone()[0]
    
    def columnCount(self, parent: QModelIndex) -> int:
        return len(TaskTableModel.TASKS_HEADERS)
    
    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if role == Qt.DisplayRole: 
            if orientation == Qt.Horizontal:
                return TaskTableModel.TASKS_HEADERS[section]
            else:
                return str(section+1)


class MainWindow(QMainWindow, mainwindow_ui.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        mainwindow_ui.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.task_model = TaskTableModel()
        self.tasks_table.setModel(self.task_model)
        self.tasks_table.resizeColumnsToContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()