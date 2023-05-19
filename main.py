# -*- coding: utf-8 -*-
"""程序入口"""

from imgui.integrations.glfw import GlfwRenderer
import OpenGL.GL as gl
import glfw
import imgui
import sys
from framework import fontmgr
from framework import slot
from framework import memory
import ui

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from imgui.integrations.base import BaseOpenGLRenderer

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1000

impl = None  # type:  imgui.integrations.base.BaseOpenGLRenderer
window = None


def Init():
    imgui.get_io().config_flags &= ~imgui.CONFIG_NO_MOUSE
    # 初始化字体管理器
    fontmgr.GetMgr().Init(impl)
    memory.Init()
    initCB()


def initCB():
    """初始化回调"""
    glfw.set_drop_callback(window, dropCB)


def dropCB(window, fileList):
    memory.DragFileList.SetData(fileList)
    slot.DRAG_FILE.Emit()


def Loop():
    """主循环"""
    glfw.poll_events()
    impl.process_inputs()

    imgui.new_frame()

    if not memory.IsMousePassthrough.GetData() or imgui.get_io().want_capture_mouse:
        glfw.set_window_attrib(window, glfw.MOUSE_PASSTHROUGH, glfw.FALSE)
    elif memory.IsMousePassthrough.GetData():
        glfw.set_window_attrib(window, glfw.MOUSE_PASSTHROUGH, glfw.TRUE)
    # 显示界面
    ui.Start(WINDOW_WIDTH, WINDOW_HEIGHT)

    gl.glClearColor(0, 0, 0, 0)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    imgui.render()
    impl.render(imgui.get_draw_data())
    glfw.swap_buffers(window)


def main():
    """入口"""
    global window, impl
    imgui.create_context()
    window = impl_glfw_init()
    impl = GlfwRenderer(window)
    Init()
    while not glfw.window_should_close(window):
        Loop()
    impl.shutdown()
    glfw.terminate()


def impl_glfw_init():
    """主窗口创建"""
    width, height = WINDOW_WIDTH, WINDOW_HEIGHT
    window_name = "DownOne Imgui"

    if not glfw.init():
        print("Could not initialize OpenGL context")
        sys.exit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    # 透明化与鼠标穿透
    glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, glfw.TRUE)
    glfw.window_hint(glfw.DECORATED, glfw.FALSE)
    glfw.window_hint(glfw.MOUSE_PASSTHROUGH, glfw.TRUE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(int(width), int(height), window_name, None, None)
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        sys.exit(1)

    return window


if __name__ == "__main__":
    main()
