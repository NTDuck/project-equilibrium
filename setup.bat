@echo off

if not defined VIRTUAL_ENV (

    call venv\Scripts\activate
    set FLASK_APP=main
    set FLASK_DEBUG=1
)