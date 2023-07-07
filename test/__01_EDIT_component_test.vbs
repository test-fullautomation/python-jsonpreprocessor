Dim oWShell
Dim sEditor
Set oWShell = CreateObject("WScript.Shell")
sEditor = "D:\PCControl\Editor\NotepadPP\Notepad++Portable.exe"
oWShell.Run sEditor & " -lpython " & """D:\ROBFW\components\python-jsonpreprocessor\test\component_test.py""", 5, False
