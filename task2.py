from typing import List
import json
import yaml
from task1 import Teacher
import psycopg2


class TeacherRepository:
    def __init__(self, filename: str = ""):
        self._filename = filename
        self._teachers: List[Teacher] = []

    def get_by_id(self, teacher_id: int) -> Teacher | None:
        for teacher in self._teachers:
            if teacher.teacher_id == teacher_id:
                return teacher
        return None

    def get_k_n_short_list(self, k: int, n: int) -> List[str]:
        start_index = (n - 1) * k
        end_index = start_index + k

        if start_index >= len(self._teachers):
            return []

        result = []
        for teacher in self._teachers[start_index:end_index]:
            result.append(teacher.short_info())

        return result

    def sort_by_field(self, field: str = "last_name") -> List[Teacher]:
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
        for i, teacher in enumerate(self._teachers):
            if teacher.teacher_id == teacher_id:
                del self._teachers[i]
                return True
        return False

    def get_count(self) -> int:
        return len(self._teachers)

    def get_all_teachers(self) -> List[Teacher]:
        return self._teachers.copy()


class TeacherRepJson(TeacherRepository):
    def __init__(self, filename: str = "teachers.json"):
        super().__init__(filename)
        self._load_from_file()

    def _load_from_file(self):
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
    def __init__(self, filename: str = "teachers.yaml"):
        super().__init__(filename)
        self._load_from_file()

    def _load_from_file(self):
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
    def __init__(self, host: str, database: str, username: str, password: str, port: int = 5432):
        super().__init__("")
        self._db_repository = TeacherRepDB(host, database, username, password, port)

    def get_by_id(self, teacher_id: int) -> Teacher | None:
        return self._db_repository.get_by_id(teacher_id)

    def get_k_n_short_list(self, k: int, n: int) -> List[str]:
        return self._db_repository.get_k_n_short_list(k, n)

    def add_teacher(self, teacher_data: dict) -> Teacher:
        return self._db_repository.add_teacher(teacher_data)

    def update_teacher(self, teacher_id: int, teacher_data: dict) -> Teacher | None:
        return self._db_repository.update_teacher(teacher_id, teacher_data)

    def delete_teacher(self, teacher_id: int) -> bool:
        return self._db_repository.delete_teacher(teacher_id)

    def get_count(self) -> int:
        return self._db_repository.get_count()

    def get_all_teachers(self) -> List[Teacher]:
        return self._db_repository.get_all_teachers()

    def sort_by_field(self, field: str = "last_name") -> List[Teacher]:
        all_teachers = self._db_repository.get_all_teachers()

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
    _instance = None

    def __new__(cls, host: str, database: str, username: str, password: str, port: int = 5432):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection_string = f"host={host} dbname={database} user={username} password={password} port={port}"
        return cls._instance

    def get_connection(self):
        return psycopg2.connect(self._connection_string)


class TeacherRepDB:
    def __init__(self, host: str, database: str, username: str, password: str, port: int = 5432):
        self._db_connection = DatabaseConnection(host, database, username, password, port)
        self._create_table_if_not_exists()

    def _get_connection(self):
        return self._db_connection.get_connection()

    def _create_table_if_not_exists(self):
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
        sql = "SELECT teacher_id, last_name, first_name, patronymic, academic_degree, administrative_position, experience_years FROM teachers WHERE teacher_id = %s"
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

    def get_k_n_short_list(self, k: int, n: int) -> List[str]:
        sql = """
        SELECT teacher_id, last_name, first_name, patronymic, experience_years 
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
                    experience_years=row[4]
                )
                result.append(teacher.short_info())
            return result

    def add_teacher(self, teacher_data: dict) -> Teacher:
        sql = """
        INSERT INTO teachers (last_name, first_name, patronymic, academic_degree, administrative_position, experience_years)
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
        sql = """
        UPDATE teachers 
        SET last_name = %s, first_name = %s, patronymic = %s, academic_degree = %s, administrative_position = %s, experience_years = %s
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
        sql = "DELETE FROM teachers WHERE teacher_id = %s"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (teacher_id,))
            deleted = cursor.rowcount > 0
            conn.commit()
            return deleted

    def get_count(self) -> int:
        sql = "SELECT COUNT(*) as count FROM teachers"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            return cursor.fetchone()[0]

    def get_all_teachers(self) -> List[Teacher]:
        sql = "SELECT teacher_id, last_name, first_name, patronymic, academic_degree, administrative_position, experience_years FROM teachers ORDER BY teacher_id"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
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
            return result



class FilterSortDecorator:
    def __init__(self, repository):
        self._repository = repository

    def get_k_n_short_list(self, k: int, n: int, filter_func: Callable = None, sort_func: Callable = None) -> List[str]:
        teachers = self._repository.get_all_teachers()

        if filter_func:
            teachers = [t for t in teachers if filter_func(t)]

        if sort_func:
            teachers = sorted(teachers, key=sort_func)

        start_index = (n - 1) * k
        end_index = start_index + k

        if start_index >= len(teachers):
            return []

        return [teacher.short_info() for teacher in teachers[start_index:end_index]]

    def get_count(self, filter_func: Callable = None) -> int:
        teachers = self._repository.get_all_teachers()

        if filter_func:
            teachers = [t for t in teachers if filter_func(t)]

        return len(teachers)

    def __getattr__(self, name):
        return getattr(self._repository, name)
