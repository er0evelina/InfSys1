"""Модуль для работы с репозиториями преподавателей."""
from typing import List, Callable
import json
import yaml
import psycopg2
from task1 import Teacher



class TeacherRepository:
    """Базовый класс репозитория преподавателей."""

    def __init__(self):
        """Инициализирует репозиторий."""
        self._teachers: List[Teacher] = []

    def _load_from_file(self):
        """Загружает данные из файла."""

    def save_to_file(self):
        """Сохраняет данные в файл."""

    def get_by_id(self, teacher_id: int) -> Teacher | None:
        """Возвращает преподавателя по ID."""
        for teacher in self._teachers:
            if teacher.teacher_id == teacher_id:
                return teacher
        return None

    def get_k_n_short_list(self, k: int, n: int) -> List[Teacher]:
        """Возвращает список преподавателей с пагинацией."""
        start_index = (n - 1) * k
        end_index = start_index + k

        if start_index >= len(self._teachers):
            raise IndexError("start index out of range")

        result = []
        for teacher in self._teachers[start_index:end_index]:
            result.append(teacher)

        return result

    def sort_by_field(self, field: str = "last_name") -> List[Teacher]:
        """Сортирует преподавателей по указанному полю."""
        valid_fields = {
            'teacher_id': lambda t: t.teacher_id,
            'last_name': lambda t: t.last_name,
            'first_name': lambda t: t.first_name,
            'experience_years': lambda t: t.experience_years
        }

        if field not in valid_fields:
            raise ValueError(f"Недопустимое поле для сортировки: {field}")

        self._teachers.sort(key=valid_fields[field])
        return self._teachers.copy()

    def add_teacher(self, teacher_data: dict) -> Teacher:
        """Добавляет нового преподавателя."""
        if self._teachers:
            new_id = max(teacher.teacher_id for teacher in self._teachers) + 1
        else:
            new_id = 1

        teacher = Teacher(
            teacher_id=new_id,
            last_name=teacher_data['last_name'],
            first_name=teacher_data['first_name'],
            patronymic=teacher_data.get('patronymic'),
            academic_degree=teacher_data.get('academic_degree'),
            administrative_position=teacher_data.get('administrative_position'),
            experience_years=teacher_data.get('experience_years', 0)
        )

        self._teachers.append(teacher)
        return teacher

    def update_teacher(self, teacher_id: int, teacher_data: dict) -> Teacher | None:
        """Обновляет данные преподавателя."""
        for i, teacher in enumerate(self._teachers):
            if teacher.teacher_id == teacher_id:
                updated_teacher = Teacher(
                    teacher_id=teacher_id,
                    last_name=teacher_data['last_name'],
                    first_name=teacher_data['first_name'],
                    patronymic=teacher_data.get('patronymic'),
                    academic_degree=teacher_data.get('academic_degree'),
                    administrative_position=teacher_data.get('administrative_position'),
                    experience_years=teacher_data.get('experience_years', 0)
                )
                self._teachers[i] = updated_teacher
                return updated_teacher
        return None

    def delete_teacher(self, teacher_id: int) -> bool:
        """Удаляет преподавателя по ID."""
        for i, teacher in enumerate(self._teachers):
            if teacher.teacher_id == teacher_id:
                del self._teachers[i]
                return True
        return False

    def get_count(self) -> int:
        """Возвращает количество преподавателей."""
        return len(self._teachers)


class TeacherRepJson(TeacherRepository):
    """Реализация репозитория для JSON формата."""

    def __init__(self, filename: str):
        """Инициализирует JSON репозиторий."""
        super().__init__()
        self._filename = filename
        self._load_from_file()

    def _load_from_file(self):
        """Загружает данные из JSON файла."""
        try:
            with open(self._filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self._teachers = []
                for item in data:
                    try:
                        teacher = Teacher(
                            teacher_id=item['teacher_id'],
                            last_name=item['last_name'],
                            first_name=item['first_name'],
                            patronymic=item.get('patronymic'),
                            academic_degree=item.get('academic_degree'),
                            administrative_position=item.get('administrative_position'),
                            experience_years=item.get('experience_years', 0)
                        )
                        self._teachers.append(teacher)
                    except (ValueError, KeyError) as e:
                        print(f"Ошибка при создании преподавателя: {e}")
        except FileNotFoundError:
            self._teachers = []
        except json.JSONDecodeError:
            print(f"Ошибка чтения файла {self._filename}")
            self._teachers = []

    def save_to_file(self):
        """Сохраняет данные в JSON файл."""
        data = []
        for teacher in self._teachers:
            teacher_data = {
                'teacher_id': teacher.teacher_id,
                'last_name': teacher.last_name,
                'first_name': teacher.first_name,
                'patronymic': teacher.patronymic,
                'academic_degree': teacher.academic_degree,
                'administrative_position': teacher.administrative_position,
                'experience_years': teacher.experience_years
            }
            data.append(teacher_data)

        with open(self._filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)


class TeacherRepYaml(TeacherRepository):
    """Реализация репозитория для YAML формата."""

    def __init__(self, filename: str):
        """Инициализирует YAML репозиторий."""
        super().__init__()
        self._filename = filename
        self._load_from_file()

    def _load_from_file(self):
        """Загружает данные из YAML файла."""
        try:
            with open(self._filename, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                if data is None:
                    self._teachers = []
                    return

                self._teachers = []
                for item in data:
                    try:
                        teacher = Teacher(
                            teacher_id=item['teacher_id'],
                            last_name=item['last_name'],
                            first_name=item['first_name'],
                            patronymic=item.get('patronymic'),
                            academic_degree=item.get('academic_degree'),
                            administrative_position=item.get('administrative_position'),
                            experience_years=item.get('experience_years', 0)
                        )
                        self._teachers.append(teacher)
                    except (ValueError, KeyError) as e:
                        print(f"Ошибка при создании преподавателя: {e}")
        except FileNotFoundError:
            self._teachers = []
        except yaml.YAMLError as e:
            print(f"Ошибка чтения YAML файла {self._filename}: {e}")
            self._teachers = []

    def save_to_file(self):
        """Сохраняет данные в YAML файл."""
        data = []
        for teacher in self._teachers:
            teacher_data = {
                'teacher_id': teacher.teacher_id,
                'last_name': teacher.last_name,
                'first_name': teacher.first_name,
                'patronymic': teacher.patronymic,
                'academic_degree': teacher.academic_degree,
                'administrative_position': teacher.administrative_position,
                'experience_years': teacher.experience_years
            }
            data.append(teacher_data)

        with open(self._filename, 'w', encoding='utf-8') as file:
            yaml.dump(data, file, allow_unicode=True, default_flow_style=False, indent=2)


class TeacherRepDBAdapter(TeacherRepository):
    """Адаптер для работы с базой данных."""

    def __init__(self, host: str, database: str, username: str, password: str, port: int = 5432):
        """Инициализирует адаптер БД."""
        super().__init__()
        self._db_repository = TeacherRepDB(host, database, username, password, port)

    def get_by_id(self, teacher_id: int) -> Teacher | None:
        """Возвращает преподавателя по ID из БД."""
        return self._db_repository.get_by_id(teacher_id)

    def get_k_n_short_list(self, k: int, n: int) -> List[Teacher]:
        """Возвращает список преподавателей с пагинацией из БД."""
        return self._db_repository.get_k_n_short_list(k, n)

    def add_teacher(self, teacher_data: dict) -> Teacher:
        """Добавляет нового преподавателя в БД."""
        return self._db_repository.add_teacher(teacher_data)

    def update_teacher(self, teacher_id: int, teacher_data: dict) -> Teacher | None:
        """Обновляет данные преподавателя в БД."""
        return self._db_repository.update_teacher(teacher_id, teacher_data)

    def delete_teacher(self, teacher_id: int) -> bool:
        """Удаляет преподавателя по ID из БД."""
        return self._db_repository.delete_teacher(teacher_id)

    def get_count(self) -> int:
        """Возвращает количество преподавателей из БД."""
        return self._db_repository.get_count()

    def sort_by_field(self, field: str = "last_name") -> List[Teacher]:
        """Сортирует преподавателей по указанному полю из БД."""
        all_teachers = self._db_repository.get_k_n_short_list(
            self._db_repository.get_count(), 1
        )

        sort_functions = {
            'teacher_id': lambda t: t.teacher_id,
            'last_name': lambda t: t.last_name,
            'first_name': lambda t: t.first_name,
            'experience_years': lambda t: t.experience_years
        }

        if field not in sort_functions:
            raise ValueError(f"Недопустимое поле для сортировки: {field}")

        return sorted(all_teachers, key=sort_functions[field])


class DatabaseConnection:
    """Класс для управления подключением к базе данных (Singleton)."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        """Создает единственный экземпляр класса."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host: str, database: str, username: str, password: str, port: int = 5432):
        """Инициализирует подключение к базе данных."""
        if not hasattr(self, '_connection_string'):
            self._connection_string = (
                f"host={host} dbname={database} user={username} "
                f"password={password} port={port}"
            )

    def get_connection(self):
        """Возвращает соединение с базой данных."""
        return psycopg2.connect(self._connection_string)


class TeacherRepDB:
    """Реализация репозитория для работы с базой данных."""

    def __init__(self, host: str, database: str, username: str, password: str, port: int = 5432):
        """Инициализирует репозиторий БД."""
        self._db_connection = DatabaseConnection(host, database, username, password, port)
        self._create_table_if_not_exists()

    def _get_connection(self):
        """Возвращает соединение с БД."""
        return self._db_connection.get_connection()

    def _create_table_if_not_exists(self):
        """Создает таблицу, если она не существует."""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS teachers (
            teacher_id SERIAL PRIMARY KEY,
            last_name VARCHAR(100) NOT NULL,
            first_name VARCHAR(100) NOT NULL,
            patronymic VARCHAR(100),
            academic_degree VARCHAR(200),
            administrative_position VARCHAR(200),
            experience_years INTEGER NOT NULL DEFAULT 0
        )
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(create_table_sql)
            conn.commit()

    def get_by_id(self, teacher_id: int) -> Teacher | None:
        """Возвращает преподавателя по ID из БД."""
        sql = """SELECT teacher_id, last_name, first_name, patronymic, academic_degree,
        administrative_position, experience_years FROM teachers WHERE teacher_id = %s"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (teacher_id,))
            row = cursor.fetchone()
            if row:
                return Teacher(
                    teacher_id=row[0],
                    last_name=row[1],
                    first_name=row[2],
                    patronymic=row[3],
                    academic_degree=row[4],
                    administrative_position=row[5],
                    experience_years=row[6]
                )
        return None

    def get_k_n_short_list(self, k: int, n: int) -> List[Teacher]:
        """Возвращает список преподавателей с пагинацией из БД."""
        sql = """
        SELECT teacher_id, last_name, first_name, patronymic, academic_degree, 
        administrative_position, experience_years 
        FROM teachers 
        ORDER BY teacher_id 
        LIMIT %s OFFSET %s
        """
        offset = (n - 1) * k
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (k, offset))
            rows = cursor.fetchall()
            result = []
            for row in rows:
                teacher = Teacher(
                    teacher_id=row[0],
                    last_name=row[1],
                    first_name=row[2],
                    patronymic=row[3],
                    academic_degree=row[4],
                    administrative_position=row[5],
                    experience_years=row[6]
                )
                result.append(teacher)
            if len(result) == 0:
                raise IndexError("start index out of range")
            return result

    def add_teacher(self, teacher_data: dict) -> Teacher:
        """Добавляет нового преподавателя в БД."""
        sql = """
        INSERT INTO teachers (last_name, first_name, patronymic, 
        academic_degree, administrative_position, experience_years)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING teacher_id
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (
                teacher_data['last_name'],
                teacher_data['first_name'],
                teacher_data.get('patronymic'),
                teacher_data.get('academic_degree'),
                teacher_data.get('administrative_position'),
                teacher_data.get('experience_years', 0)
            ))
            new_id = cursor.fetchone()[0]
            conn.commit()

            return Teacher(
                teacher_id=new_id,
                last_name=teacher_data['last_name'],
                first_name=teacher_data['first_name'],
                patronymic=teacher_data.get('patronymic'),
                academic_degree=teacher_data.get('academic_degree'),
                administrative_position=teacher_data.get('administrative_position'),
                experience_years=teacher_data.get('experience_years', 0)
            )

    def update_teacher(self, teacher_id: int, teacher_data: dict) -> Teacher | None:
        """Обновляет данные преподавателя в БД."""
        sql = """
        UPDATE teachers 
        SET last_name = %s, first_name = %s, patronymic = %s, 
        academic_degree = %s, administrative_position = %s, experience_years = %s
        WHERE teacher_id = %s
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (
                teacher_data['last_name'],
                teacher_data['first_name'],
                teacher_data.get('patronymic'),
                teacher_data.get('academic_degree'),
                teacher_data.get('administrative_position'),
                teacher_data.get('experience_years', 0),
                teacher_id
            ))
            if cursor.rowcount > 0:
                conn.commit()
                return Teacher(
                    teacher_id=teacher_id,
                    last_name=teacher_data['last_name'],
                    first_name=teacher_data['first_name'],
                    patronymic=teacher_data.get('patronymic'),
                    academic_degree=teacher_data.get('academic_degree'),
                    administrative_position=teacher_data.get('administrative_position'),
                    experience_years=teacher_data.get('experience_years', 0)
                )
        return None

    def delete_teacher(self, teacher_id: int) -> bool:
        """Удаляет преподавателя по ID из БД."""
        sql = "DELETE FROM teachers WHERE teacher_id = %s"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (teacher_id,))
            deleted = cursor.rowcount > 0
            conn.commit()
            return deleted

    def get_count(self) -> int:
        """Возвращает количество преподавателей в БД."""
        sql = "SELECT COUNT(*) as count FROM teachers"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            return cursor.fetchone()[0]


class FilterDecorator:
    """Декоратор для фильтрации преподавателей."""

    def __init__(self, repository: TeacherRepository, filter_func: Callable | None):
        """Инициализирует декоратор фильтра."""
        self._repository = repository
        self._filter_func: Callable = filter_func

    def get_k_n_short_list(self, k: int, n: int) -> List[Teacher]:
        """Возвращает отфильтрованный список с пагинацией."""
        teachers = self._repository.get_k_n_short_list(self._repository.get_count(), 1)

        if self._filter_func:
            teachers = [t for t in teachers if self._filter_func(t)]

        start_index = (n - 1) * k
        end_index = start_index + k

        if start_index >= len(teachers):
            raise IndexError("start index out of range")

        return list(teachers[start_index:end_index])

    def get_count(self) -> int:
        """Возвращает количество отфильтрованных преподавателей."""
        teachers = self._repository.get_k_n_short_list(self._repository.get_count(), 1)

        if self._filter_func:
            teachers = [t for t in teachers if self._filter_func(t)]

        return len(teachers)

    @property
    def filter_func(self) -> Callable:
        """Возвращает функцию фильтрации."""
        return self._filter_func

    @filter_func.setter
    def filter_func(self, func):
        """Устанавливает функцию фильтрации."""
        self._filter_func = func


class SortDecorator:
    """Декоратор для сортировки преподавателей."""

    def __init__(
            self, repository: TeacherRepository,
            sort_func: Callable | None, reverse: bool = False
    ):
        """Инициализирует декоратор сортировки."""
        self._repository = repository
        self._sort_func: Callable = sort_func
        self._reverse: bool = reverse

    def get_k_n_short_list(self, k: int, n: int) -> List[Teacher]:
        """Возвращает отсортированный список с пагинацией."""
        teachers = self._repository.get_k_n_short_list(self._repository.get_count(), 1)

        if self._sort_func:
            teachers = sorted(teachers, key=self._sort_func, reverse=self._reverse)
        elif self._reverse:
            teachers.reverse()

        start_index = (n - 1) * k
        end_index = start_index + k

        if start_index >= len(teachers):
            raise IndexError("start index out of range")

        return list(teachers[start_index:end_index])

    def get_count(self):
        """Возвращает количество преподавателей."""
        return self._repository.get_count()

    @property
    def sort_func(self) -> Callable:
        """Возвращает функцию сортировки."""
        return self._sort_func

    @sort_func.setter
    def sort_func(self, func):
        """Устанавливает функцию сортировки."""
        self._sort_func = func
