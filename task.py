class Teacher:
    def __init__(self, teacher_id, last_name, first_name, patronymic=None,
                 academic_degree=None, administrative_position=None, experience_years=0):
        self._teacher_id = self.validate_teacher_id(teacher_id)
        self._last_name = self.validate_non_empty_string(last_name, "Last name")
        self._first_name = self.validate_non_empty_string(first_name, "First name")
        self._patronymic = self.validate_optional_string(patronymic)
        self._academic_degree = self.validate_optional_string(academic_degree)
        self._administrative_position = self.validate_optional_string(administrative_position)
        self._experience_years = self.validate_experience_years(experience_years)

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

    def __str__(self):
        return f"Teacher {self.teacher_id}: {self.get_full_name()}, Experience: {self._experience_years} years"

    def __repr__(self):
        return (f"Teacher(teacher_id={self._teacher_id}, last_name='{self._last_name}', "
                f"first_name='{self._first_name}', patronymic='{self._patronymic}', "
                f"academic_degree='{self._academic_degree}', "
                f"administrative_position='{self._administrative_position}', "
                f"experience_years={self._experience_years})")
