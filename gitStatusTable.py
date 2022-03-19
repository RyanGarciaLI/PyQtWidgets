# -*- coding: utf-8 -*-
# 
# Copyright (C) 20222 RyanGarciaLI. All rights reserved.
#
# Created on March 13, 20222s
#
# @author: Ryan Garcia LI

import sys
from abc import abstractmethod
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFrame, QHBoxLayout, QLineEdit, QSizePolicy, QSpacerItem, QLabel,
                            QPushButton, QCompleter, QApplication, QHeaderView, QTableView, QGroupBox)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFontMetrics
from PyQt5.QtCore import Qt


class QAbstractFileTable(QWidget):

    @abstractmethod
    def __init__(self, parent=None):
        super(QAbstractFileTable, self).__init__(parent)

    @abstractmethod
    def _setup_ui(self):
        pass

    @abstractmethod
    def set_col_size(self, size_list):
        pass


class QFileHoritonalHeader(QAbstractFileTable):

    def __init__(self, headers, parent=None):
        super(QFileHoritonalHeader, self).__init__(parent)
        self.headers = headers
        self.model = QStandardItemModel(1, len(headers))
        self.model.setHorizontalHeaderLabels(headers)
        self.header_view = QHeaderView(Qt.Orientation.Horizontal, self)
        self.header_view.setModel(self.model)
        self.header_view.setSectionsMovable(False) # TODO: doesn't work
        self._setup_ui()

    def _setup_ui(self):
        super(QFileHoritonalHeader, self)._setup_ui()
        vbox = QVBoxLayout()
        vbox.addWidget(self.header_view)
        self.setLayout(vbox)
        self.vbox = vbox
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.header_view.setFixedHeight(50)
        self.header_view.setStyleSheet("QHeaderView{ font: bold 8pt;}")
        self.setFixedHeight(50)

    def set_col_size(self, size_list):
        for i in range(self.model.columnCount()):
            self.header_view.resizeSection(i, size_list[i])


class QFileTable(QGroupBox):

    def __init__(self, file_list, title, headers, check_all=False, parent=None):
        super(QFileTable, self).__init__(title, parent)
        self.files = file_list
        self.type = title
        self.headers = headers
        self.default_cheked = check_all
        self.table_view = QTableView()
        self._set_data()
        self._setup_ui()

    def _setup_ui(self):
        # super(QFileTable, self)._setup_ui()
        # self.setStyleSheet("backgroud-color: white;")
        self.setContentsMargins(0, 0, 0, 0)
        self.table_view.setStyleSheet("QTableView { border: 0px solid white}")
        height_ = self._get_table_height()
        self.table_view.setMaximumHeight(height_)
        self.table_view.setMinimumHeight(height_)

        # layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.table_view)
        self.setLayout(vbox)
        self.vbox = vbox
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.table_view.verticalHeader().hide()
        self.table_view.horizontalHeader().hide()

        self.setFixedHeight(height_ + 30)

    def _set_data(self):
        row = len(self.files)
        col = len(self.headers)
        longest = [""] * col
        self.model = QStandardItemModel(row, col)
        for i, file_info in enumerate(self.files):
            # file checkbox
            file_path = file_info[0]
            check_box = QStandardItem(file_path)
            check_box.setCheckable(True)
            if self.default_cheked:
                check_box.setCheckState(Qt.CheckState.Checked)
            
            self.model.setItem(i, 0, check_box)
            # record max length of path
            if len(file_path) > len(longest[0]):
                longest[0] = file_path

            # other item
            for j in range(1, col):
                self.model.setItem(i, j, QStandardItem(file_info[j]))
                # record max col
                if len(file_info[j]) > len(longest[j]):
                    longest[j] = file_info[j]

        self.longest = longest
        self.table_view.setModel(self.model)

    def _get_table_height(self):
        h = 4
        for i in range(self.model.rowCount()):
            h += self.table_view.rowHeight(i)
        return h

    def get_checked_files(self):
        files = []
        for i in range(self.model.rowCount()):
            item = self.model.item(i, 0)
            if item.checkState() == Qt.CheckState.Checked:
                files.append(item.text())
        return files

    def uncheck_file(self, row):
        self.model.item(row, 0).setCheckState(Qt.CheckState.Unchecked)

    def uncheck_all_files(self):
        for i in range(self.model.rowCount()):
            self.uncheck_file(i)
    
    def set_col_size(self, size_list):
        for i in range(self.model.columnCount()):
            self.table_view.setColumnWidth(i, size_list[i])
    

class QGitStatusTable(QWidget):

    def __init__(self, all_files_info, headers, parent=None):
        super(QGitStatusTable, self).__init__(parent)
        self.all_files = all_files_info
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)
        # self.setStyleSheet("background-color: white;")
        self.header = QFileHoritonalHeader(headers)
        self.types = ["staged", "unstaged", "untracked"]
        self.tb_staged = QFileTable(self.all_files["staged"], "Staged", headers, check_all=True)
        self.tb_unstaged = QFileTable(self.all_files["unstaged"], "Unstaged", headers)
        self.tb_untracked = QFileTable(self.all_files["untracked"], "Untracked", headers)
        self.vspacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.vbox.addWidget(self.header)
        self.vbox.addWidget(self.tb_staged)
        self.vbox.addWidget(self.tb_unstaged)
        self.vbox.addWidget(self.tb_untracked)
        self.vbox.addItem(self.vspacer)
        self._setup_ui()

    def _setup_ui(self):
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.set_col_size()

    def collect_checked_files(self):
        staged_checked_files = self.tb_staged.get_checked_files()
        unstaged_checked_files = self.tb_unstaged.get_checked_files()
        untracked_checked_files = self.tb_untracked.get_checked_files()
        checked = staged_checked_files + unstaged_checked_files + untracked_checked_files
        unstaged_checked = unstaged_checked_files + untracked_checked_files
        return checked, unstaged_checked

    def uncheck_all_files(self):
        self.tb_staged.uncheck_all_files()
        self.tb_unstaged.uncheck_all_files()
        self.tb_untracked.uncheck_all_files()

    def set_col_size(self):
        longest = [max(self.tb_staged.longest[i], self.tb_unstaged.longest[i], self.tb_untracked.longest[i], key=len) for i in range(len(self.tb_staged.longest))]
        font_ = self.tb_staged.font()
        metrics = QFontMetrics(font_)
        width_ = [metrics.width(l) + 20 for l in longest]
        width_[0] += 50
        for widget in [self.header, self.tb_staged, self.tb_unstaged, self.tb_untracked]:
            widget.set_col_size(width_)

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    files = {
        "staged": [
            ("Resource/file1.txt", ".txt", "Modified"), 
            ("file2.cs", ".cs", "Added"), 
            ("Prefab/file3.py", ".py", "Deleted"), 
            ("file4.bat", ".bat", "Renamed")
            ],
        "unstaged": [],
        "untracked": [
            ("Scripts/thisfilehasaverylongfilename.config", ".config", "Added"),
            ('file5.prefab', ".prefab", "Modified")
        ]
    }
    headers = ["Path", "Ext", "Type"]
    table = QGitStatusTable(files, headers)
    table.show()
    app.exec_()