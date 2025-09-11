class Teacher:
    def __init__(self, teacher_id, last_name, first_name, patronymic=None,
                 academic_degree=None, administrative_position=None, experience_years=0):
        self._teacher_id = teacher_id
        self._last_name = last_name
        self._first_name = first_name
        self._patronymic = patronymic
        self._academic_degree = academic_degree
        self._administrative_position = administrative_position
        self._experience_years = experience_years

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

    @teacher_id.setter
    def teacher_id(self, value):
        self._teacher_id = value

    @last_name.setter
    def last_name(self, value):
        self._last_name = value

    @first_name.setter
    def first_name(self, value):
        self._first_name = value

    @patronymic.setter
    def patronymic(self, value):
        self._patronymic = value

    @academic_degree.setter
    def academic_degree(self, value):
        self._academic_degree = value

    @administrative_position.setter
    def administrative_position(self, value):
        self._administrative_position = value

    @experience_years.setter
    def experience_years(self, value):
        self._experience_years = value