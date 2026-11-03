cmake_minimum_required(VERSION 3.25)

# scikit-build-core sets SKBUILD/SKBUILD_PROJECT_NAME when building via
# `uv sync`/`pip install`. Default it so `cmake --preset venv` also works for
# local iteration (e.g. re-running shiboken without a full reinstall).
if(NOT SKBUILD)
    message(STATUS "Running CMake directly.")
    set(SKBUILD_PROJECT_NAME pyside6_qtads_borco)
endif()

project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets)

if(UNIX AND NOT APPLE AND TARGET WrapOpenGL::WrapOpenGL)
    # Qt6::Gui links OpenGL (libOpenGL/libGLX) into everything that uses it,
    # through this imported target, but nothing here calls OpenGL. Keep them
    # off our link lines, so the wheels don't hard-depend on libOpenGL.so.0
    # (missing on e.g. a minimal Ubuntu 26.04) or graft private copies of it.
    set_target_properties(WrapOpenGL::WrapOpenGL PROPERTIES INTERFACE_LINK_LIBRARIES "")
endif()

# qtadvanceddocking-qt6: QtAds from our fork (extern/qtads, see
# docs/patches.md), as a shared library. Its own CMake adds Qt6::GuiPrivate
# and xcb on Linux. Only the library is wanted, not its examples and demo.
set(BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
set(BUILD_STATIC OFF CACHE BOOL "" FORCE)
add_subdirectory(extern/qtads EXCLUDE_FROM_ALL)

# _pyside6_qtads_borco: shiboken6-generated Python bindings for QtAds
add_subdirectory(src/pyside6_qtads_borco/bindings)
