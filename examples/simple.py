"""A main window with a dock manager and one dock widget (the smoke test, shown)."""

import sys

from PySide6.QtWidgets import QApplication, QLabel, QMainWindow

import pyside6_qtads_borco as QtAds


def main() -> int:
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("pyside6_qtads_borco")
    window.resize(640, 480)

    dock_manager = QtAds.CDockManager(window)
    dock_widget = QtAds.CDockWidget(dock_manager, "Label 1")
    dock_widget.setWidget(QLabel("Lorem ipsum dolor sit amet."))
    dock_manager.addDockWidget(QtAds.TopDockWidgetArea, dock_widget)

    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
