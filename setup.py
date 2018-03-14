import sys
from cx_Freeze import setup, Executable


base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="TICleaner",
      version="0.1",
      description="Программа комментирует строоки с ТУ в файлах TI.ASM.",
      executables=[Executable("TICleaner.py", base=base)])
