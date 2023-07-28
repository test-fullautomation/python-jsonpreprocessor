@echo off

"%RobotPythonPath%/python.exe" "./component_test.py"
REM "%RobotPythonPath%/python.exe" "./component_test.py" --recreateinstance


echo ---------------------------------------
echo component_test returned ERRORLEVEL : %ERRORLEVEL%
echo ---------------------------------------

pause

