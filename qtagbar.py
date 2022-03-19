# -*- coding: utf-8 -*-
# 
# Copyright (C) 20222 RyanGarciaLI. All rights reserved.
#
# Created on March 13, 20222s
#
# @author: Ryan Garcia LI

""" This is a custom tag bar.

This tag bar receive user input from a line edit and show them in terms of tags. Tag names can be preset and
auto-filled in the line edit. Every tag can be deleted by clicking the X button on it. The tag bar can expand
if too many tags are created.
"""

import sys
from functools import partial
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFrame, QHBoxLayout, QLineEdit, QSizePolicy, QSpacerItem, QLabel,
                            QPushButton, QCompleter, QApplication)
from PyQt5.QtCore import QStringListModel, Qt

class QTagBar(QWidget):
    """ A tag bar with input area.

    A tag bar consists of a frame and a line edit in vertical. The frame contains all created tags in horizontal. Each
    tag has a text label and a push button with a red text "X" within a frame. 
    """

    def __init__(self, parent=None):
        super(QTagBar, self).__init__(parent)
        self.setWindowTitle('Tag Bar')
        self.tags = []
        self.vbox = QVBoxLayout()
        self.vbox.setSpacing(4)
        self.setLayout(self.vbox)

        # tags
        self.hspacer = QSpacerItem(10, 5, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.hbox_tag = QHBoxLayout()
        self.hbox_tag.setSpacing(8)
        self.hbox_tag.addItem(self.hspacer)
        self.f_tag_bar = QFrame()
        self.f_tag_bar.setLayout(self.hbox_tag)
        self.vbox.addWidget(self.f_tag_bar)

        # line edit
        self.le_tag = QLineEdit()
        self.le_tag.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.vbox.addWidget(self.le_tag)

        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.setContentsMargins(0, 0, 0, 0)
        self.f_tag_bar.setContentsMargins(0, 0, 0, 0)
        self.hbox_tag.setContentsMargins(0, 0, 0, 0)
        self.vbox.setContentsMargins(4, 4, 4, 4)
        self.refresh()
        self._setup_ui()


    def _setup_ui(self):
        self.le_tag.returnPressed.connect(partial(self._create_tags))

    
    def _create_tags(self):
        new_tags = self.le_tag.text().split(', ')
        if new_tags == [""]:
            # ignore empty input
            return

        self.le_tag.setText('')
        self.tags.extend(new_tags)
        self.tags = list(set(self.tags))
        self.tags.sort(key=lambda x: x.lower())
        self.refresh()


    def refresh(self):
        for i in reversed(range(self.hbox_tag.count())):
            item = self.hbox_tag.takeAt(i)
            if item is self.hspacer:
                self.hbox_tag.removeItem(item) # trick here
                continue

            item.widget().setParent(None)

        self.le_tag.setParent(None)
        for tag in self.tags:
            self._add_tag_to_bar(tag)

        self.hbox_tag.addItem(self.hspacer)
        self.vbox.addWidget(self.le_tag)
        self.le_tag.setFocus()


    def _add_tag_to_bar(self, text):
        # label
        label = QLabel(text)
        label.setStyleSheet("border:0px;")
        label.setFixedHeight(24)

        # x button 
        btn = QPushButton('✕')
        btn.setFixedSize(24, 24)
        btn.setStyleSheet("border:0px; font-weight:bold; color:red;")
        btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        btn.clicked.connect(partial(self.delete_tag, text))

        # horizontal layout
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        hbox.addWidget(label)
        hbox.addWidget(btn)

        # tag frame
        tag_frame = QFrame()
        tag_frame.setStyleSheet('border:1px solid rgb(192,192,192); border-radius:4px;')
        tag_frame.setContentsMargins(2, 0, 2, 2)
        tag_frame.setFixedHeight(24)
        tag_frame.setLayout(hbox)
        tag_frame.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.hbox_tag.addWidget(tag_frame)


    def delete_tag(self, tag_name):
        self.tags.remove(tag_name)
        self.refresh()


    def clear(self):
        self.tags.clear()
        self.le_tag.setText('')
        self.refresh()


    def add_tag(self, tag_name):
        self.tags.append(tag_name)
        self.refresh()


    def add_tags(self, tag_names):
        self.tags.extend(tag_names)
        self.refresh()


    def name_list(self):
        return self.tags


    def set_completer(self, str_list):
        model = QStringListModel()
        model.setStringList(str_list)
        
        completer = QCompleter()
        completer.setModel(model)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.activated.connect(partial(self._create_tags))
        self.le_tag.setCompleter(completer)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    names = ['Alice', 'Bob', 'Charle', 'David', 'Evageline', 'Frank', 'Gray', 'Herry', 'Ryan']
    tag_bar = QTagBar()
    tag_bar.set_completer(names)
    tag_bar.show()
    app.exec_()


    

