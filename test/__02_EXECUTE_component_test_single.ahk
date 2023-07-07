SetTitleMatchMode, 2

Run, %comspec% /k, ./
WinWait, cmd.exe
WinWaitActive, cmd.exe

Sleep, 500

SendInput "D:\ROBFW\components\python-jsonpreprocessor\test\component_test_single.bat"
