@echo off
REM Create Conda environment
conda create --name pna python=3.12 -y

REM Activate the environment
CALL conda activate pna

REM Install requirements using pip
pip install -r requirements.txt

REM Keep the window open after the script is done
pause
