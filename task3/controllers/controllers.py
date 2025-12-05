from models.repositories import TeacherRepository, FilterDecorator
from controllers.subject import Subject, Observer


class Controller:
    def __init__(self, repository: TeacherRepository):
        self._repository = repository

    def get_repo(self):
        return self._repository

    def set_repo(self, repository: TeacherRepository):
        self._repository = repository


class TeacherController(Subject, Controller):
    def __init__(self, repository: TeacherRepository):
        Subject.__init__(self)
        Controller.__init__(self, repository)

    def _get_filter_func(self, filter_data):
        """Создает функцию фильтрации на основе переданных параметров"""
        if not filter_data:
            return None

        def filter_func(teacher):
            # Фильтрация по фамилии
            if 'last_name' in filter_data and filter_data['last_name']:
                if filter_data['last_name'].lower() not in teacher.last_name.lower():
                    return False

            # Фильтрация по имени
            if 'first_name' in filter_data and filter_data['first_name']:
                if filter_data['first_name'].lower() not in teacher.first_name.lower():
                    return False

            # Фильтрация по отчеству
            if 'patronymic' in filter_data and filter_data['patronymic']:
                if not teacher.patronymic or filter_data['patronymic'].lower() not in teacher.patronymic.lower():
                    return False

            # Фильтрация по ученой степени
            if 'academic_degree' in filter_data and filter_data['academic_degree']:
                if not teacher.academic_degree or filter_data[
                    'academic_degree'].lower() not in teacher.academic_degree.lower():
                    return False

            # Фильтрация по должности
            if 'position' in filter_data and filter_data['position']:
                if not teacher.administrative_position or filter_data[
                    'position'].lower() not in teacher.administrative_position.lower():
                    return False

            # Фильтрация по минимальному стажу
            if 'min_experience' in filter_data and filter_data['min_experience']:
                try:
                    min_exp = int(filter_data['min_experience'])
                    if teacher.experience_years < min_exp:
                        return False
                except ValueError:
                    pass

            # Фильтрация по максимальному стажу
            if 'max_experience' in filter_data and filter_data['max_experience']:
                try:
                    max_exp = int(filter_data['max_experience'])
                    if teacher.experience_years > max_exp:
                        return False
                except ValueError:
                    pass

            return True

        return filter_func

    def load_teachers(self, filter_params=None):
        """Загружает преподавателей с возможной фильтрацией"""
        teachers_count = self._repository.get_count()

        try:
            # Создаем функцию фильтрации, если есть параметры
            filter_func = None
            if filter_params:
                filter_func = self._get_filter_func(filter_params)

            # Применяем фильтрацию, если есть функция
            if filter_func:
                repository = FilterDecorator(self._repository, filter_func)
            else:
                repository = self._repository

            teachers = repository.get_k_n_short_list(teachers_count, 1)
        except IndexError:
            teachers = []

        self.update(teachers)


class AddTeacherController(Subject, Controller):
    def __init__(self, repository: TeacherRepository):
        Subject.__init__(self)
        Controller.__init__(self, repository)

    def add_teacher(self, teacher_data):
        try:
            teacher = self._repository.add_teacher(teacher_data)
            self._repository.save_to_file()
            self.update({"success": True, "teacher": teacher})
        except Exception as e:
            self.update({"success": False, "error": str(e)})


class UpdateTeacherController(Subject, Controller):
    def __init__(self, repository: TeacherRepository):
        Subject.__init__(self)
        Controller.__init__(self, repository)
        self.current_teacher_id = None

    def get_teacher(self, teacher_id):
        try:
            self.current_teacher_id = teacher_id
            teacher = self._repository.get_by_id(teacher_id)
            self.update({"teacher": teacher})
        except Exception as e:
            self.update({"error": str(e)})

    def update_teacher(self, teacher_id, teacher_data):
        try:
            self.current_teacher_id = teacher_id
            teacher = self._repository.update_teacher(teacher_id, teacher_data)
            if teacher:
                self._repository.save_to_file()
                self.update({"success": True, "teacher": teacher})
            else:
                self.update({"success": False, "error": "Преподаватель не найден", "teacher_id": teacher_id})
        except Exception as e:
            self.update({"success": False, "error": str(e), "teacher_id": teacher_id})


class DeleteTeacherController(Subject, Controller):
    def __init__(self, repository: TeacherRepository):
        Subject.__init__(self)
        Controller.__init__(self, repository)

    def delete_teacher(self, teacher_id):
        try:
            success = self._repository.delete_teacher(teacher_id)
            if success:
                self._repository.save_to_file()
                self.update({"success": True, "teacher_id": teacher_id})
            else:
                self.update({"success": False, "error": "Преподаватель не найден"})
        except Exception as e:
            self.update({"success": False, "error": str(e)})
