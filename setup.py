from cx_Freeze import setup, Executable
import sys, os


curr = os.path.join(os.path.dirname(sys.argv[0]), 'sounds')
build_exe_options = {'include_files' : [curr]}

setup(name='Ping Pong',
      version='1.0.0',
      description='The ping-pong game on python!',
      options = { 'build_exe': build_exe_options},
      executables=[Executable('start.py', base='Win32GUI')]
)