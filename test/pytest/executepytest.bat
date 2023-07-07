@echo off
"%RobotPythonPath%/python.exe" "./executepytest.py" --pytestcommandline="--junit-prefix=JsonPreprocessor"
echo --------------------------------------
echo executepytest returned ERRORLEVEL : %ERRORLEVEL%
echo --------------------------------------

