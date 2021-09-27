from flask import Blueprint


STUDENT_ID = 9
api = Blueprint('api', __name__)


@api.route(f'/hello-world-{STUDENT_ID}')
def hello_student():
    return f'Hello World {STUDENT_ID}'
