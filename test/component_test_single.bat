@echo off

"%RobotPythonPath%/python.exe" "./component_test.py" --testid="JPP_0251"

REM "%RobotPythonPath%/python.exe" "./component_test.py"
REM "%RobotPythonPath%/python.exe" "./component_test.py" --codedump
REM "%RobotPythonPath%/python.exe" "./component_test.py" --configdump

echo ---------------------------------------
echo component_test returned ERRORLEVEL : %ERRORLEVEL%
echo ---------------------------------------

