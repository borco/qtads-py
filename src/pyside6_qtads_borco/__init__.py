"""PySide6 bindings for Qt Advanced Docking System (QtAds).

Re-exports the public API of the compiled ``_pyside6_qtads_borco`` extension
module, which shiboken6 generates from
``src/pyside6_qtads_borco/bindings/bindings.xml``. As in PyPI
``pyside6-qtads``, the classes and enums of QtAds' ``ads`` namespace are also
available at module level.
"""

from importlib.metadata import version

# the binding will not load if we don't explicitly import PySide6.QtWidgets
import PySide6.QtWidgets  # noqa: F401

from ._pyside6_qtads_borco import ads

CDockAreaWidget = ads.CDockAreaWidget
CDockContainerWidget = ads.CDockContainerWidget
CDockManager = ads.CDockManager
CDockWidget = ads.CDockWidget

DockWidgetArea = ads.DockWidgetArea
NoDockWidgetArea = ads.DockWidgetArea.NoDockWidgetArea
LeftDockWidgetArea = ads.DockWidgetArea.LeftDockWidgetArea
RightDockWidgetArea = ads.DockWidgetArea.RightDockWidgetArea
TopDockWidgetArea = ads.DockWidgetArea.TopDockWidgetArea
BottomDockWidgetArea = ads.DockWidgetArea.BottomDockWidgetArea
CenterDockWidgetArea = ads.DockWidgetArea.CenterDockWidgetArea

# [project].version in pyproject.toml is the only copy (see the comment above [tool.uv] there)
__version__ = version("pyside6-qtads-borco")


__all__ = [
    "BottomDockWidgetArea",
    "CDockAreaWidget",
    "CDockContainerWidget",
    "CDockManager",
    "CDockWidget",
    "CenterDockWidgetArea",
    "DockWidgetArea",
    "LeftDockWidgetArea",
    "NoDockWidgetArea",
    "RightDockWidgetArea",
    "TopDockWidgetArea",
    "__version__",
    "ads",
]
