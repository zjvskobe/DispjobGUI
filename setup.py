import os
import sys
from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY']=r"C:\Users\zhangjian\Anaconda3\tcl\tcl8.6"
os.environ['TK_LIBRARY']=r"C:\Users\zhangjian\Anaconda3\tcl\tk8.6"

base = 'Win32GUI' if sys.platform == 'win32' else None

includes = ["numpy.core._methods",
            "numpy.lib.format",
            "matplotlib.backends.backend_qt5",
            "matplotlib.backends.backend_qt5agg",
            "matplotlib.backends.qt_compat",
            "matplotlib.backends.qt_editor.figureoptions",
            "matplotlib.backends.qt_editor.formlayout",
            "matplotlib.backends.qt_editor.formsubplottool",
            "matplotlib.legend_handler"]
include_files = [r'C:\Users\zhangjian\Anaconda3\DLLs\tcl86t.dll',
                 r'C:\Users\zhangjian\Anaconda3\DLLs\tk86t.dll']

executables = [Executable('DispjobGUI.py', base=base)]

build_exe_options = {"includes": includes, "include_files": include_files}

setup(name = 'DispjobGUI',
      version = '0.1',
      description = 'my gui',
      options = {"build_exe": build_exe_options},
      executables = executables)