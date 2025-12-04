from flask import Flask, request
from config import REPO_TYPES, DEFAULT_REPO_TYPE
from controllers.create_repo import CreateRepoFactory
from controllers.controllers import TeacherController
from views.views import TeacherView

app = Flask(__name__)

controller = TeacherController(None)
view = TeacherView()

controller.attach(view)


@app.route('/')
def teachers_list():
    repo_type = request.args.get('repo_type', DEFAULT_REPO_TYPE)

    repository = CreateRepoFactory.create_repo(repo_type)

    controller.repository = repository
    controller.load_teachers(repo_type)

    return view.render()


if __name__ == '__main__':
    app.run(debug=True)
