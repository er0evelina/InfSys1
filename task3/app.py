from flask import Flask, render_template
from config import *
from models.repositories import TeacherRepJson

app = Flask(__name__)

# Создаем репозиторий
repo = TeacherRepJson(JSON_FILE_PATH)


@app.route('/')
def teachers_list():
    try:
        all_teachers = repo.get_k_n_short_list(repo.get_count(), 1)
    except IndexError:
        all_teachers = []

    return render_template('teachers.html', teachers=all_teachers)


if __name__ == '__main__':
    app.run(debug=True)
