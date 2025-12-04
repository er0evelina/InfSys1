from observer import Subject
from models.teachers import Teacher

class AddTeacherController(Subject):
    """Контроллер для добавления преподавателя"""
    
    def __init__(self):
        super().__init__()
        self._message = ""
    
    def add_teacher(self, repository, form_data):
        """Добавляет преподавателя в репозиторий"""
        try:
            # Подготавливаем данные
            teacher_data = {
                'last_name': form_data.get('last_name'),
                'first_name': form_data.get('first_name'),
                'patronymic': form_data.get('patronymic'),
                'academic_degree': form_data.get('academic_degree'),
                'administrative_position': form_data.get('administrative_position'),
                'experience_years': int(form_data.get('experience_years', 0)),
                'snils': form_data.get('snils')
            }
            
            # Добавляем преподавателя
            teacher = repository.add_teacher(teacher_data)
            
            # Сохраняем в файл
            repository.save_to_file()
            
            self._message = f"Преподаватель {teacher.last_name} добавлен успешно!"
            return True
            
        except Exception as e:
            self._message = f"Ошибка: {str(e)}"
            return False
    
    @property
    def message(self):
        return self._message
