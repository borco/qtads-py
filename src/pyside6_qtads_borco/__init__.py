"""PySide6 bindings for Qt Advanced Docking System (QtAds).

Re-exports the public API of the compiled ``_pyside6_qtads_borco`` extension
module, which shiboken6 generates from
``src/pyside6_qtads_borco/bindings/bindings.xml``.

The module-level names below are the same as PyPI ``pyside6-qtads``'
(mborgerson/pyside6_qtads' ``init.py``), so that switching is an import-line
change: ``import pyside6_qtads_borco as QtAds``. Everything else is reached
through ``ads``, as there. Enum values are taken from their enum
(``ads.DockWidgetArea.TopDockWidgetArea``), not shiboken's old-style
``ads.TopDockWidgetArea``: the same object, but one type checkers can see.
"""

from importlib import metadata as __metadata

# the binding will not load if we don't explicitly import PySide6.QtWidgets
import PySide6.QtWidgets  # noqa: F401

from ._pyside6_qtads_borco import ads as ads  # explicit re-export (py.typed)

# DockWidgetArea
DockWidgetArea = ads.DockWidgetArea
NoDockWidgetArea = ads.DockWidgetArea.NoDockWidgetArea
LeftDockWidgetArea = ads.DockWidgetArea.LeftDockWidgetArea
RightDockWidgetArea = ads.DockWidgetArea.RightDockWidgetArea
TopDockWidgetArea = ads.DockWidgetArea.TopDockWidgetArea
BottomDockWidgetArea = ads.DockWidgetArea.BottomDockWidgetArea
CenterDockWidgetArea = ads.DockWidgetArea.CenterDockWidgetArea
InvalidDockWidgetArea = ads.DockWidgetArea.InvalidDockWidgetArea
OuterDockAreas = ads.DockWidgetArea.OuterDockAreas
AllDockAreas = ads.DockWidgetArea.AllDockAreas

# eTabIndex
TabDefaultInsertIndex = ads.eTabIndex.TabDefaultInsertIndex
TabInvalidIndex = ads.eTabIndex.TabInvalidIndex

# SideBarLocation
SideBarLeft = ads.SideBarLocation.SideBarLeft
SideBarTop = ads.SideBarLocation.SideBarTop
SideBarBottom = ads.SideBarLocation.SideBarBottom
SideBarRight = ads.SideBarLocation.SideBarRight
SideBarNone = ads.SideBarLocation.SideBarNone

# eBitwiseOperator
BitwiseAnd = ads.eBitwiseOperator.BitwiseAnd
BitwiseOr = ads.eBitwiseOperator.BitwiseOr

# eDragState
DraggingInactive = ads.eDragState.DraggingInactive
DraggingMousePressed = ads.eDragState.DraggingMousePressed
DraggingTab = ads.eDragState.DraggingTab
DraggingFloatingWidget = ads.eDragState.DraggingFloatingWidget

# eIcon
TabCloseIcon = ads.eIcon.TabCloseIcon
AutoHideIcon = ads.eIcon.AutoHideIcon
DockAreaMenuIcon = ads.eIcon.DockAreaMenuIcon
DockAreaUndockIcon = ads.eIcon.DockAreaUndockIcon
DockAreaCloseIcon = ads.eIcon.DockAreaCloseIcon
DockAreaMinimizeIcon = ads.eIcon.DockAreaMinimizeIcon
IconCount = ads.eIcon.IconCount

# TitleBarButton
TitleBarButtonTabsMenu = ads.TitleBarButton.TitleBarButtonTabsMenu
TitleBarButtonUndock = ads.TitleBarButton.TitleBarButtonUndock
TitleBarButtonClose = ads.TitleBarButton.TitleBarButtonClose
TitleBarButtonAutoHide = ads.TitleBarButton.TitleBarButtonAutoHide
TitleBarButtonMinimize = ads.TitleBarButton.TitleBarButtonMinimize

# Classes
CDockAreaTabBar = ads.CDockAreaTabBar
CDockAreaTitleBar = ads.CDockAreaTitleBar
CDockAreaWidget = ads.CDockAreaWidget
CDockComponentsFactory = ads.CDockComponentsFactory
CDockContainerWidget = ads.CDockContainerWidget
CDockFocusController = ads.CDockFocusController
CDockManager = ads.CDockManager
CDockSplitter = ads.CDockSplitter
CDockOverlay = ads.CDockOverlay
CDockOverlayCross = ads.CDockOverlayCross
CDockWidget = ads.CDockWidget
CDockWidgetTab = ads.CDockWidgetTab
CDockingStateReader = ads.CDockingStateReader
CElidingLabel = ads.CElidingLabel
CFloatingDockContainer = ads.CFloatingDockContainer
CFloatingDragPreview = ads.CFloatingDragPreview
IFloatingWidget = ads.IFloatingWidget
CIconProvider = ads.CIconProvider
CSpacerWidget = ads.CSpacerWidget
CTitleBarButton = ads.CTitleBarButton

# [project].version in pyproject.toml is the only copy (see the comment above [tool.uv] there)
__version__ = __metadata.version("pyside6-qtads-borco")
