# PP_LABS_2021

to start the project
  - clone repository(git clone)
  - сd pp
  - set python 3.6.8(pyenv local 3.6.8)
  - create virtual environment(python -m venv)
  - activate venv(venv\Scripts\activate.bat)
  - pip install -r requirements.txt
  - open project and run app.py
  
migrations:
  - to create migration: alembic revision -- autogenerate -m "commit name"
  - to run: alembic upgrade head
 
(Before using alembic: change db urls in alembic.ini and alembic\env.py)

# Project of other team members:
https://github.com/olehratinskiy/ap_simple_store

https://github.com/yuliamarkiv/pp_labs

https://github.com/yarynabeida/AP
