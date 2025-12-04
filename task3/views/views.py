from flask import render_template
from typing import List
from models.teacher import Teacher
from observer import Observer
from controllers.controllers import TeacherController
from config import REPO_TYPES


class TeacherView(Observer):
    """Представление для преподавателей"""

    def __init__(self):
        self._teachers: List[Teacher] = []
        self._current_repo_type: str = ""
        self._repo_info: str = ""

    def update(self, subject: TeacherController):
        """Получает обновление от контроллера"""
        self._teachers = subject.teachers
        self._current_repo_type = subject.current_repo_type
        self._repo_info = subject.repo_info

    def render(self):
        """Рендерит HTML шаблон"""
        return render_template(
            'teachers.html',
            teachers=self._teachers,
            repo_types=REPO_TYPES,
            current_repo_type=self._current_repo_type,
            repo_info=self._repo_info
        )
