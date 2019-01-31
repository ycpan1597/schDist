from cx_Freeze import setup, Executable

setup(name = 'JRgrapher', 
	version = '0.1', 
	description = 'allows users to select files of accelerometry data and generates jerk ratio graphs',
	executables = [Executable("client.py")])