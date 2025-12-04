import json
import re
from xml.etree import ElementTree as ET


class Employee:
    def __init__(self, employee_id: int, last_name: str, first_name: str, experience_years: int = 0, snils: str = None):
        self._employee_id = self.validate_employee_id(employee_id)
        self._last_name = self.validate_name(last_name, "Last name")
        self._first_name = self.validate_name(first_name, "First name")
        self._experience_years = self.validate_experience_years(experience_years)
        self._snils = self.validate_snils(snils)

    @staticmethod
    def validate_employee_id(employee_id: int) -> int:
        if not isinstance(employee_id, int) or employee_id <= 0:
            raise ValueError("Employee ID must be a positive integer")
        return employee_id

    @staticmethod
    def validate_name(name: str, field_name: str = "Name", optional: bool = False) -> str | None:
        if optional and name is None:
            return None

        if optional and isinstance(name, str) and name.strip() == '':
            return None

        if not isinstance(name, str):
            raise ValueError(f"{field_name} must be a string")

        name = name.strip()
        if len(name) == 0:
            raise ValueError(f"{field_name} cannot be empty")

        # Регулярное выражение для проверки имени: только буквы, дефисы и пробелы
        if not re.match(r'^[A-Za-zА-Яа-яЁё\- ]+$', name):
            raise ValueError(f"{field_name} can only contain letters, hyphens and spaces")

        return name

    @staticmethod
    def validate_experience_years(experience_years: int) -> int:
        """
        Проверка снилс


        """

        if not isinstance(experience_years, int) or experience_years < 0:
            raise ValueError("Experience years must be a non-negative integer")
        return experience_years

    @staticmethod
    def validate_snils(snils: str) -> str:
        if snils is None:
            raise ValueError("SNILS cannot be None")

        if not isinstance(snils, str):
            raise ValueError("SNILS must be a string")

        snils_clean = snils.strip()

        pattern1 = r'^\d{11}$'  # Формат "12345678964"
        pattern2 = r'^\d{3}-\d{3}-\d{3} \d{2}$'  # Формат "123-456-789 64"

        if not (re.match(pattern1, snils_clean) or re.match(pattern2, snils_clean)):
            raise ValueError("SNILS must be in format '12345678964' or '123-456-789 64'")

        digits_only = re.sub(r'\D', '', snils_clean)

        if len(digits_only) != 11:
            raise ValueError("SNILS must contain exactly 11 digits")

        Employee._validate_snils_checksum(digits_only)

        return digits_only

    @staticmethod
    def _validate_snils_checksum(snils_digits: str) -> None:
        """Проверка контрольной суммы СНИЛС"""

        base_number = snils_digits[:9]
        check_number = int(snils_digits[9:])


        if int(base_number) < 1001998:
            return

        total = 0
        for i, digit in enumerate(base_number):
            weight = 9 - i
            total += int(digit) * weight

        control_sum = total % 101
        if control_sum == 100:
            control_sum = 0

        if control_sum != check_number:
            raise ValueError("Invalid SNILS checksum")

    @property
    def employee_id(self) -> int:
        return self._employee_id

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def experience_years(self) -> int:
        return self._experience_years

    @property
    def snils(self) -> str:
        return self._snils

    @employee_id.setter
    def employee_id(self, value: int):
        self._employee_id = self.validate_employee_id(value)

    @last_name.setter
    def last_name(self, value: str):
        self._last_name = self.validate_name(value, "Last name")

    @first_name.setter
    def first_name(self, value: str):
        self._first_name = self.validate_name(value, "First name")

    @experience_years.setter
    def experience_years(self, value: int):
        self._experience_years = self.validate_experience_years(value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Teacher):
            return False

        return self._snils == other._snils


class Teacher(Employee):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs:
            data = args[0]
            if isinstance(data, str):
                data = data.strip()
                if data.startswith('{') and data.endswith('}'):
                    params = Teacher._parse_json(data)
                elif data.startswith('<') and data.endswith('>'):
                    params = Teacher._parse_xml(data)
                else:
                    params = Teacher._parse_string(data)
            else:
                raise ValueError("Single argument must be a string (formatted string, JSON or XML)")
        else:
            params = {
                'teacher_id': kwargs.get('teacher_id', args[0] if len(args) > 0 else None),
                'last_name': kwargs.get('last_name', args[1] if len(args) > 1 else None),
                'first_name': kwargs.get('first_name', args[2] if len(args) > 2 else None),
                'patronymic': kwargs.get('patronymic', args[3] if len(args) > 3 else None),
                'academic_degree': kwargs.get('academic_degree', args[4] if len(args) > 4 else None),
                'administrative_position': kwargs.get('administrative_position', args[5] if len(args) > 5 else None),
                'experience_years': kwargs.get('experience_years', args[6] if len(args) > 6 else 0),
                'snils': kwargs.get('snils', args[7] if len(args) > 7 else None)
            }

        super().__init__(params['teacher_id'], params['last_name'], params['first_name'], params['experience_years'],
                         params['snils'])

        self._patronymic = Employee.validate_name(params.get('patronymic'), "patronymic", True)
        self._academic_degree = Teacher.validate_optional_string(params.get('academic_degree'), "academic_degree")
        self._administrative_position = Teacher.validate_optional_string(params.get('administrative_position'),
                                                                         "administrative_degree")

    @staticmethod
    def _parse_string(data_string):
        parts = data_string.split(';')
        if len(parts) != 8:
            raise ValueError(
                "String format must be: id;last_name;first_name;patronymic;degree;position;experience;snils")

        try:
            teacher_id = int(parts[0])
            experience_years = int(parts[6])
        except ValueError:
            raise ValueError("ID and experience must be integers")

        return {
            'teacher_id': teacher_id,
            'last_name': parts[1],
            'first_name': parts[2],
            'patronymic': parts[3] if parts[3] != '' else None,
            'academic_degree': parts[4] if parts[4] != '' else None,
            'administrative_position': parts[5] if parts[5] != '' else None,
            'experience_years': experience_years,
            'snils': parts[7] if parts[7] != '' else None
        }

    @staticmethod
    def _parse_json(json_string):
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

        return {
            'teacher_id': data['teacher_id'],
            'last_name': data['last_name'],
            'first_name': data['first_name'],
            'patronymic': data.get('patronymic'),
            'academic_degree': data.get('academic_degree'),
            'administrative_position': data.get('administrative_position'),
            'experience_years': data.get('experience_years', 0),
            'snils': data.get('snils')
        }

    @staticmethod
    def _parse_xml(xml_string):
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

        optional_fields = ['patronymic', 'academic_degree', 'administrative_position', 'experience_years', 'snils']
        for field in optional_fields:
            element = root.find(field)
            if element is not None and element.text is not None:
                data[field] = element.text

        try:
            teacher_id = int(data['teacher_id'])
            experience_years = int(data.get('experience_years', 0))
        except ValueError:
            raise ValueError("ID and experience must be integers in XML")

        return {
            'teacher_id': teacher_id,
            'last_name': data['last_name'],
            'first_name': data['first_name'],
            'patronymic': data.get('patronymic'),
            'academic_degree': data.get('academic_degree'),
            'administrative_position': data.get('administrative_position'),
            'experience_years': experience_years,
            'snils': data.get('snils')
        }

    @staticmethod
    def validate_optional_string(value: str | None, field_name: str) -> str | None:
        if value is None:
            return None

        academic_degree = value.strip()
        if len(academic_degree) == 0:
            return None

        # Ученая степень может содержать буквы, цифры, точки, запятые и другие допустимые символы
        if not re.match(r'^[A-Za-zА-Яа-яЁё0-9\s\.,\-\(\)]+$', academic_degree):
            raise ValueError(f"A{field_name} contains invalid characters")

        return academic_degree

    # Геттеры
    @property
    def teacher_id(self) -> int:
        return self._employee_id

    @property
    def patronymic(self) -> str | None:
        return self._patronymic

    @property
    def academic_degree(self) -> str | None:
        return self._academic_degree

    @property
    def administrative_position(self) -> str | None:
        return self._administrative_position

    # Сеттеры
    @teacher_id.setter
    def teacher_id(self, value: int):
        self._employee_id = self.validate_employee_id(value)

    @patronymic.setter
    def patronymic(self, value: str | None):
        self._patronymic = Employee.validate_name(value, "patronymic", True)

    @academic_degree.setter
    def academic_degree(self, value: str | None):
        self._academic_degree = Teacher.validate_optional_string(value, "academic_degree")

    @administrative_position.setter
    def administrative_position(self, value: str | None):
        self._administrative_position = Teacher.validate_optional_string(value, "administrative_position")

    def get_full_name(self) -> str:
        if self._patronymic:
            return f"{self._last_name} {self._first_name} {self._patronymic}"
        return f"{self._last_name} {self._first_name}"

    def short_info(self) -> str:
        return f"{self._employee_id}: {self.get_full_name()} ({self._experience_years} лет)"

    def full_info(self) -> str:
        parts = [
            f"ID: {self._employee_id}",
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
        parts.append(f"СНИЛС: {self._snils}")

        return ", ".join(parts)

    def __str__(self) -> str:
        return f"Teacher {self.teacher_id}: {self.get_full_name()}, SNILS: {self._snils}, Experience: {self._experience_years} years"

    def __repr__(self) -> str:
        return (f"Teacher(teacher_id={self._employee_id}, last_name='{self._last_name}', "
                f"first_name='{self._first_name}', patronymic='{self._patronymic}', "
                f"academic_degree='{self._academic_degree}', "
                f"administrative_position='{self._administrative_position}', "
                f"experience_years={self._experience_years}, snils='{self._snils}')")

