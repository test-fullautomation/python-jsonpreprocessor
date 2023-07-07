@echo off

"%RobotPythonPath%/python.exe" "./component_test.py" --codedump

echo ---------------------------------------
echo component_test returned ERRORLEVEL : %ERRORLEVEL%
echo ---------------------------------------

pause

