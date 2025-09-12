import json
from xml.etree import ElementTree as ET


class Teacher:
    def __init__(self, *args, **kwargs):

        if len(args) == 1:
            data = args[0]
            if isinstance(data, str):
                if data.strip().startswith('{') and data.strip().endswith('}'):
                    self._init_from_json(data)
                elif data.strip().startswith('<') and data.strip().endswith('>'):
                    self._init_from_xml(data)
                else:
                    self._init_from_string(data)
            else:
                raise ValueError("Single argument must be a string (formatted string, JSON or XML)")
        else:
            self._init_from_params(*args, **kwargs)

    def _init_from_params(self, teacher_id, last_name, first_name, patronymic=None,
                          academic_degree=None, administrative_position=None, experience_years=0):
        self._teacher_id = self.validate_teacher_id(teacher_id)
        self._last_name = self.validate_non_empty_string(last_name, "Last name")
        self._first_name = self.validate_non_empty_string(first_name, "First name")
        self._patronymic = self.validate_optional_string(patronymic)
        self._academic_degree = self.validate_optional_string(academic_degree)
        self._administrative_position = self.validate_optional_string(administrative_position)
        self._experience_years = self.validate_experience_years(experience_years)

    def _init_from_string(self, data_string):
        parts = data_string.split(';')
        if len(parts) != 7:
            raise ValueError("String format must be: id;last_name;first_name;patronymic;degree;position;experience")

        try:
            teacher_id = int(parts[0])
            experience_years = int(parts[6])
        except ValueError:
            raise ValueError("ID and experience must be integers")

        self._init_from_params(
            teacher_id=teacher_id,
            last_name=parts[1],
            first_name=parts[2],
            patronymic=parts[3] if parts[3] != '' else None,
            academic_degree=parts[4] if parts[4] != '' else None,
            administrative_position=parts[5] if parts[5] != '' else None,
            experience_years=experience_years
        )

    def _init_from_json(self, json_string):
        try:
            data = json.loads(json_string)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")

        if not isinstance(data, dict):
            raise ValueError("JSON must be an object")

        required_fields = ['teacher_id', 'last_name', 'first_name']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field in JSON: {field}")

        self._init_from_params(
            teacher_id=data['teacher_id'],
            last_name=data['last_name'],
            first_name=data['first_name'],
            patronymic=data.get('patronymic'),
            academic_degree=data.get('academic_degree'),
            administrative_position=data.get('administrative_position'),
            experience_years=data.get('experience_years', 0)
        )

    def _init_from_xml(self, xml_string):
        try:
            root = ET.fromstring(xml_string)
        except ET.ParseError:
            raise ValueError("Invalid XML format")

        if root.tag != 'teacher':
            raise ValueError("XML root element must be 'teacher'")

        required_fields = ['teacher_id', 'last_name', 'first_name']
        data = {}
        for field in required_fields:
            element = root.find(field)
            if element is None:
                raise ValueError(f"Missing required field in XML: {field}")
            data[field] = element.text

        optional_fields = ['patronymic', 'academic_degree', 'administrative_position', 'experience_years']
        for field in optional_fields:
            element = root.find(field)
            if element is not None and element.text is not None:
                data[field] = element.text

        try:
            teacher_id = int(data['teacher_id'])
            experience_years = int(data.get('experience_years', 0))
        except ValueError:
            raise ValueError("ID and experience must be integers in XML")

        self._init_from_params(
            teacher_id=teacher_id,
            last_name=data['last_name'],
            first_name=data['first_name'],
            patronymic=data.get('patronymic'),
            academic_degree=data.get('academic_degree'),
            administrative_position=data.get('administrative_position'),
            experience_years=experience_years
        )

    @staticmethod
    def validate_teacher_id(teacher_id):
        if not isinstance(teacher_id, int) or teacher_id <= 0:
            raise ValueError("only positive integer")
        return teacher_id

    @staticmethod
    def validate_non_empty_string(value, field_name="Value"):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError(f"{field_name}: only non-empty string")
        return value.strip()

    @staticmethod
    def validate_optional_string(value):
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError("only None or a string")
        if len(value.strip()) == 0:
            return None
        return value.strip()

    @staticmethod
    def validate_experience_years(experience_years):
        if not isinstance(experience_years, int) or experience_years < 0:
            raise ValueError("Experience years. only non-negative integer")
        return experience_years

    # Геттеры
    @property
    def teacher_id(self):
        return self._teacher_id

    @property
    def last_name(self):
        return self._last_name

    @property
    def first_name(self):
        return self._first_name

    @property
    def patronymic(self):
        return self._patronymic

    @property
    def academic_degree(self):
        return self._academic_degree

    @property
    def administrative_position(self):
        return self._administrative_position

    @property
    def experience_years(self):
        return self._experience_years

    # Сеттеры
    @teacher_id.setter
    def teacher_id(self, value):
        self._teacher_id = self.validate_teacher_id(value)

    @last_name.setter
    def last_name(self, value):
        self._last_name = self.validate_non_empty_string(value, "Last name")

    @first_name.setter
    def first_name(self, value):
        self._first_name = self.validate_non_empty_string(value, "First name")

    @patronymic.setter
    def patronymic(self, value):
        self._patronymic = self.validate_optional_string(value)

    @academic_degree.setter
    def academic_degree(self, value):
        self._academic_degree = self.validate_optional_string(value)

    @administrative_position.setter
    def administrative_position(self, value):
        self._administrative_position = self.validate_optional_string(value)

    @experience_years.setter
    def experience_years(self, value):
        self._experience_years = self.validate_experience_years(value)

    def get_full_name(self):
        if self._patronymic:
            return f"{self._last_name} {self._first_name} {self._patronymic}"
        return f"{self._last_name} {self._first_name}"

    def short_info(self):
        return f"{self._teacher_id}: {self.get_full_name()} ({self._experience_years} лет)"

    def full_info(self):
        parts = [
            f"ID: {self._teacher_id}",
            f"Фамилия: {self._last_name}",
            f"Имя: {self._first_name}"
        ]

        if self._patronymic:
            parts.append(f"Отчество: {self._patronymic}")

        if self._academic_degree:
            parts.append(f"Ученая степень: {self._academic_degree}")

        if self._administrative_position:
            parts.append(f"Должность: {self._administrative_position}")

        parts.append(f"Стаж: {self._experience_years} лет")

        return ", ".join(parts)

    def __str__(self):
        return f"Teacher {self.teacher_id}: {self.get_full_name()}, Experience: {self._experience_years} years"

    def __repr__(self):
        return (f"Teacher(teacher_id={self._teacher_id}, last_name='{self._last_name}', "
                f"first_name='{self._first_name}', patronymic='{self._patronymic}', "
                f"academic_degree='{self._academic_degree}', "
                f"administrative_position='{self._administrative_position}', "
                f"experience_years={self._experience_years})")

    def __eq__(self, other):
        if not isinstance(other, Teacher):
            return False

        return (self._teacher_id == other._teacher_id and
                self._last_name == other._last_name and
                self._first_name == other._first_name and
                self._patronymic == other._patronymic and
                self._academic_degree == other._academic_degree and
                self._administrative_position == other._administrative_position and
                self._experience_years == other._experience_years)
