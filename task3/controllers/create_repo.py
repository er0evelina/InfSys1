from models.repositories import TeacherRepJson, TeacherRepYaml, TeacherRepDBAdapter
from config import *


class CreateRepoFactory:
    """Фабрика для создания репозиториев"""

    @staticmethod
    def create_repo(repo_type: str = DEFAULT_REPO_TYPE):
        """
        Создает экземпляр репозитория по типу

        Args:
            repo_type: тип репозитория ('json', 'yaml', 'db')

        Returns:
            Объект репозитория
        """
        if repo_type == 'json':
            return TeacherRepJson(JSON_FILE_PATH)
        elif repo_type == 'yaml':
            return TeacherRepYaml(YAML_FILE_PATH)
        elif repo_type == 'db':
            return TeacherRepDBAdapter(
                host=DB_HOST,
                database=DB_NAME,
                username=DB_USER,
                password=DB_PASSWORD,
                port=DB_PORT
            )
        else:
            raise ValueError(f"Неизвестный тип репозитория: {repo_type}")
