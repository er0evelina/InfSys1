from models.repositories import TeacherRepository
from typing import List
from models.teacher import Teacher
from observer import Subject


class TeacherController(Subject):
    """Контроллер для работы с преподавателями"""

    def __init__(self, repository: TeacherRepository):
        super().__init__()
        self.repository = repository
        self._teachers: List[Teacher] = []
        self._current_repo_type: str = ""
        self._repo_info: str = ""

    def load_teachers(self, repo_type: str):
        """Загружает преподавателей из репозитория и уведомляет наблюдателей"""
        self._current_repo_type = repo_type

        try:
            self._teachers = self.repository.get_k_n_short_list(self.repository.get_count(), 1)
        except IndexError:
            self._teachers = []

        repo_class = type(self.repository).__name__
        count = self.repository.get_count()
        self._repo_info = f"{repo_class} ({count} записей)"

        # Уведомляем наблюдателей об изменениях
        self.notify()

    @property
    def teachers(self) -> List[Teacher]:
        return self._teachers

    @property
    def current_repo_type(self) -> str:
        return self._current_repo_type

    @property
    def repo_info(self) -> str:
        return self._repo_info
