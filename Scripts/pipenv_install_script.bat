@setlocal

@for %%i in ("%~dp0..") do SET "PROJECT_DIR=%%~fi"
@echo "##########Directory of project root is"
@echo "PROJECT_DIR=%PROJECT_DIR%"
@echo "##########Getting environment variables from .env file in PROJECT_DIR"
@for /F "usebackq eol=# delims=" %%A in ("%PROJECT_DIR%\.env") do @set %%A
@for /F "usebackq eol=# delims=" %%A in ("%PROJECT_DIR%\.env") do @echo %%A
@echo "##########Environment variables from .env successfully added to local env"
@echo "##########Syncronizing pipenv environment"
@cd %PROJECT_DIR%
@pipenv install
@echo "##########Syncronizing requirements.txt"
@cd %PROJECT_DIR%
@pipenv run pip freeze > requirements.txt
@echo "########## -_- END -_-"


@endlocal
