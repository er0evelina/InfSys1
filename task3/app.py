from flask import Flask, request, session, redirect, url_for
import config
from controllers.create_repo import CreateRepoFactory
from controllers.controllers import TeacherController, AddTeacherController, UpdateTeacherController, DeleteTeacherController
from views import views

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Создаем контроллеры и представления
repo = CreateRepoFactory.create_repo(config.DEFAULT_REPO_TYPE)

teacher_controller = TeacherController(repo)
teacher_view = views.TeacherListView()
teacher_controller.attach(teacher_view)

add_teacher_controller = AddTeacherController(repo)
add_teacher_view = views.AddTeacherView()
add_teacher_controller.attach(add_teacher_view)

update_teacher_controller = UpdateTeacherController(repo)
update_teacher_view = views.UpdateTeacherView()
update_teacher_controller.attach(update_teacher_view)

delete_teacher_controller = DeleteTeacherController(repo)
delete_teacher_view = views.DeleteTeacherView()
delete_teacher_controller.attach(delete_teacher_view)


def get_current_repo():
    repo_type = session.get('repo_type', config.DEFAULT_REPO_TYPE)
    return CreateRepoFactory.create_repo(repo_type)


@app.route('/')
def index():
    # Получаем параметры фильтрации из GET-запроса
    filter_params = {}
    
    # Простые текстовые фильтры
    if request.args.get('last_name'):
        filter_params['last_name'] = request.args.get('last_name')
    if request.args.get('first_name'):
        filter_params['first_name'] = request.args.get('first_name')
    if request.args.get('patronymic'):
        filter_params['patronymic'] = request.args.get('patronymic')
    if request.args.get('academic_degree'):
        filter_params['academic_degree'] = request.args.get('academic_degree')
    if request.args.get('position'):
        filter_params['position'] = request.args.get('position')
    
    # Фильтры по стажу
    if request.args.get('min_experience'):
        filter_params['min_experience'] = request.args.get('min_experience')
    if request.args.get('max_experience'):
        filter_params['max_experience'] = request.args.get('max_experience')
    
    # Загружаем преподавателей с фильтрацией
    teacher_controller.load_teachers(filter_params)
    
    # Передаем параметры фильтрации в шаблон
    return teacher_view.render()


@app.route('/change_repo', methods=['POST'])
def change_repo():
    repo_type = request.form.get('repo_type')
    if repo_type in config.REPO_TYPES:
        session['repo_type'] = repo_type
        new_repo = CreateRepoFactory.create_repo(repo_type)
        teacher_controller.set_repo(new_repo)
        add_teacher_controller.set_repo(new_repo)
        update_teacher_controller.set_repo(new_repo)
        delete_teacher_controller.set_repo(new_repo)
    return redirect(url_for('index'))


@app.route('/add/', methods=['GET'])
def add_teacher_form():
    return add_teacher_view.render()


@app.route('/add/', methods=['POST'])
def add_teacher():
    teacher_data = {
        'last_name': request.form.get('last_name'),
        'first_name': request.form.get('first_name'),
        'patronymic': request.form.get('patronymic') or None,
        'snils': request.form.get('snils') or None,
        'academic_degree': request.form.get('academic_degree') or None,
        'administrative_position': request.form.get('administrative_position') or None,
        'experience_years': int(request.form.get('experience_years', 0))
    }
    
    add_teacher_controller.add_teacher(teacher_data)
    
    if add_teacher_view.success:
        teacher_controller.load_teachers()
        return redirect(url_for('index'))
    else:
        return add_teacher_view.render()


@app.route('/<int:teacher_id>/', methods=['GET'])
def update_teacher_form(teacher_id):
    update_teacher_controller.get_teacher(teacher_id)
    return update_teacher_view.render()


@app.route('/<int:teacher_id>/', methods=['POST'])
def update_teacher(teacher_id):
    teacher_data = {
        'last_name': request.form.get('last_name'),
        'first_name': request.form.get('first_name'),
        'patronymic': request.form.get('patronymic') or None,
        'snils': request.form.get('snils') or None,
        'academic_degree': request.form.get('academic_degree') or None,
        'administrative_position': request.form.get('administrative_position') or None,
        'experience_years': int(request.form.get('experience_years', 0))
    }
    
    update_teacher_controller.update_teacher(teacher_id, teacher_data)
    
    if update_teacher_view.success:
        teacher_controller.load_teachers()
        return redirect(url_for('index'))
    else:
        form_teacher_data = {
            'teacher_id': teacher_id,
            'last_name': teacher_data['last_name'],
            'first_name': teacher_data['first_name'],
            'patronymic': teacher_data['patronymic'],
            'snils': teacher_data['snils'],
            'academic_degree': teacher_data['academic_degree'],
            'administrative_position': teacher_data['administrative_position'],
            'experience_years': teacher_data['experience_years']
        }
        update_teacher_view.update({"success": False, 
                                   "error": update_teacher_view.error,
                                   "teacher_id": teacher_id,
                                   "teacher": form_teacher_data})
        return update_teacher_view.render()


@app.route('/<int:teacher_id>/delete', methods=['POST'])
def delete_teacher(teacher_id):
    delete_teacher_controller.delete_teacher(teacher_id)
    
    if delete_teacher_view.success:
        teacher_controller.load_teachers()
        return redirect(url_for('index'))
    else:
        update_teacher_controller.get_teacher(teacher_id)
        update_teacher_view.update({"success": False, 
                                   "error": delete_teacher_view.error,
                                   "teacher_id": teacher_id})
        return update_teacher_view.render()


if __name__ == '__main__':
    app.run(debug=True)
