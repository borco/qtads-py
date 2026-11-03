"""Smoke test: the extension imports and QtAds docks a widget in a main window."""

from PySide6.QtWidgets import QLabel, QMainWindow
from pytestqt.qtbot import QtBot

import pyside6_qtads_borco as QtAds


def test_version() -> None:
    assert QtAds.__version__.startswith("5.1.1.")


def test_dock_manager_in_main_window(qtbot: QtBot) -> None:
    window = QMainWindow()
    qtbot.addWidget(window)

    # With a QMainWindow parent, the dock manager makes itself the central widget.
    dock_manager = QtAds.CDockManager(window)
    assert window.centralWidget() is dock_manager

    label = QLabel("Lorem ipsum")
    dock_widget = QtAds.CDockWidget(dock_manager, "Label 1")
    dock_widget.setWidget(label)

    dock_area = dock_manager.addDockWidget(QtAds.TopDockWidgetArea, dock_widget)

    assert isinstance(dock_area, QtAds.CDockAreaWidget)
    assert dock_widget.widget() is label
    assert dock_widget.dockManager() is dock_manager
    assert dock_manager.findDockWidget("Label 1") is dock_widget

    window.show()
    qtbot.waitExposed(window)
    assert dock_widget.isVisible()
