from flask import render_template
from observer import Observer

class AddTeacherView(Observer):
    """Представление для добавления преподавателя"""
    
    def __init__(self):
        self._message = ""
    
    def update(self, subject):
        """Получает обновление от контроллера"""
        self._message = subject.message
    
    def render(self):
        """Рендерит форму добавления"""
        return render_template('add_teacher.html', message=self._message)
