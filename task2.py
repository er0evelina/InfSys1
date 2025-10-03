import json
import yaml
from typing import List
from task1 import Teacher


class TeacherRepJson:
    def __init__(self, filename: str = "teachers.json"):
        self._filename = filename
        self._teachers: List[Teacher] = []
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

    def sort_by_field(self, field: str = "last_name"):
        valid_fields = {
            'teacher_id': lambda t: t.teacher_id,
            'last_name': lambda t: t.last_name,
            'first_name': lambda t: t.first_name,
            'experience_years': lambda t: t.experience_years
        }

        if field not in valid_fields:
            raise ValueError(f"Недопустимое поле для сортировки: {field}")

        self._teachers.sort(key=valid_fields[field])

    def add_teacher(self, teacher_data: dict) -> Teacher:
        # Генерация нового ID
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


class TeacherRepYaml:
    def __init__(self, filename: str = "teachers.yaml"):
        self._filename = filename
        self._teachers: List[Teacher] = []
        self._load_from_file()

    def _load_from_file(self):
        """Чтение всех значений из файла"""
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
        """Запись всех значений в файл"""
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

    def get_by_id(self, teacher_id: int) -> Teacher | None:
        """Получить объект по ID"""
        for teacher in self._teachers:
            if teacher.teacher_id == teacher_id:
                return teacher
        return None

    def get_k_n_short_list(self, k: int, n: int) -> List[str]:
        """Получить список k по счету n объектов класса short"""
        start_index = (n - 1) * k
        end_index = start_index + k

        if start_index >= len(self._teachers):
            return []

        result = []
        for teacher in self._teachers[start_index:end_index]:
            result.append(teacher.short_info())

        return result

    def sort_by_field(self, field: str = "last_name"):
        """Сортировать элементы по выбранному полю"""
        valid_fields = {
            'teacher_id': lambda t: t.teacher_id,
            'last_name': lambda t: t.last_name,
            'first_name': lambda t: t.first_name,
            'experience_years': lambda t: t.experience_years
        }

        if field not in valid_fields:
            raise ValueError(f"Недопустимое поле для сортировки: {field}")

        self._teachers.sort(key=valid_fields[field])

    def add_teacher(self, teacher_data: dict) -> Teacher:
        """Добавить объект в список (при добавлении сформировать новый ID)"""
        # Генерация нового ID
        if self._teachers:
            new_id = max(teacher.teacher_id for teacher in self._teachers) + 1
        else:
            new_id = 1

        # Создание преподавателя
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
        """Заменить элемент списка по ID"""
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
        """Удалить элемент списка по ID"""
        for i, teacher in enumerate(self._teachers):
            if teacher.teacher_id == teacher_id:
                del self._teachers[i]
                return True
        return False

    def get_count(self) -> int:
        """Получить количество элементов"""
        return len(self._teachers)

    def get_all_teachers(self) -> List[Teacher]:
        """Получить всех преподавателей (для тестирования)"""
        return self._teachers.copy()
