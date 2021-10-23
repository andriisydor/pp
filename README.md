# PP_LABS_2021

clone repository(git clone)

сd pp_labs

set python 3.6.8(pyenv local 3.6.8)

create virtual environment using requirements.txt(python -m venv)

avtivate venv(venv\Scripts\activate.bat)

pip install -r requirements.txt

open project and run app.py

to create migration: alembic revision -- autogenerate -m "add create_models"
to run: alembic upgrade head
