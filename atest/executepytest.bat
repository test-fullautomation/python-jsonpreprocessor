@echo off
"%RobotPythonPath%/python.exe" "./executepytest.py" --logfile="./aiotest/aiotestlog.xml"
REM "%RobotPythonPath%/python.exe" "./executepytest.py" --logfile="./aiotest/aiotestlog.xml" --pytestcommandline="-k \"not _Linux_\""
REM "%RobotPythonPath%/python.exe" "./executepytest.py" --logfile="./aiotest/aiotestlog.xml" --pytestcommandline="-k 'not _Linux_'"
echo --------------------------------------
echo executepytest returned ERRORLEVEL : %ERRORLEVEL%
echo --------------------------------------

