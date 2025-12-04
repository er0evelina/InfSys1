from flask import Flask, request
from config import REPO_TYPES, DEFAULT_REPO_TYPE
from controllers.create_repo import CreateRepoFactory
from controllers.controllers import TeacherController
from controllers.add_controller import AddTeacherController
from views.views import TeacherView
from views.add_view import AddTeacherView

app = Flask(__name__)

# Создаем глобальные объекты
main_controller = TeacherController(None)
main_view = TeacherView()
main_controller.attach(main_view)

@app.route('/')
def teachers_list():
    repo_type = request.args.get('repo_type', DEFAULT_REPO_TYPE)
    repository = CreateRepoFactory.create_repo(repo_type)
    
    main_controller.repository = repository
    main_controller.load_teachers(repo_type)
    
    return main_view.render()

@app.route('/add', methods=['GET', 'POST'])
def add_teacher():
    # Создаем контроллер и представление для добавления
    add_controller = AddTeacherController()
    add_view = AddTeacherView()
    add_controller.attach(add_view)
    
    if request.method == 'POST':
        # Получаем репозиторий
        repo_type = request.args.get('repo_type', DEFAULT_REPO_TYPE)
        repository = CreateRepoFactory.create_repo(repo_type)
        
        # Добавляем преподавателя
        success = add_controller.add_teacher(repository, request.form)
        
        # Обновляем главный контроллер
        if success:
            main_controller.repository = repository
            main_controller.load_teachers(repo_type)
        
        add_controller.notify()
    
    return add_view.render()

if __name__ == '__main__':
    app.run(debug=True)
