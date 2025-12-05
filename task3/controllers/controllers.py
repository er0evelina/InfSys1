from models.repositories import TeacherRepository
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
    
    def load_teachers(self):
        teachers_count = self._repository.get_count()
        try:
            teachers = self._repository.get_k_n_short_list(teachers_count, 1)
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
    
    def get_teacher(self, teacher_id):
        try:
            teacher = self._repository.get_by_id(teacher_id)
            self.update({"teacher": teacher})
        except Exception as e:
            self.update({"error": str(e)})
    
    def update_teacher(self, teacher_id, teacher_data):
        try:
            teacher = self._repository.update_teacher(teacher_id, teacher_data)
            if teacher:
                self._repository.save_to_file()
                self.update({"success": True, "teacher": teacher})
            else:
                self.update({"success": False, "error": "Преподаватель не найден"})
        except Exception as e:
            self.update({"success": False, "error": str(e)})
