import os
import sys
from cx_Freeze import setup, Executable

includes = []
include_files = [r"c:\Python36\DLLs\tcl86t.dll",
                 r"c:\Python36\DLLs\tk86t.dll",
                 r"c:\Python\table\icon.ico"]
os.environ['TCL_LIBRARY'] = r'C:\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Python36\tcl\tk8.6'

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="TICleaner",
      version="0.0.2",
      description="Программа комментирует строоки с ТУ в файлах TI.ASM.",
      author="Манжак С.С.",
      options={"build_exe": {"includes": includes, "include_files": include_files}},
      executables=[Executable("TICleaner.py", base=base, icon="icon.ico")])
