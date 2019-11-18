@setlocal

@for /F "delims=" %%I in ("%~dp0.") do @set myRoot=%%~fI

@cmd /C  "gi python,pycharm > %myRoot%\.gitignore"
@cmd /C  "echo Pipfile.lock >> %myRoot%\.gitignore"
@cmd /C  "echo .venv >> %myRoot%\.gitignore"


@endlocal
