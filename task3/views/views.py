from flask import render_template, request, redirect, url_for
from controllers.subject import Observer


class TeacherListView(Observer):
    def __init__(self):
        self.teachers = []

    def update(self, teachers):
        self.teachers = teachers

    def render(self):
        return render_template('index.html',
                               teachers=self.teachers,
                               request_args=request.args)


class AddTeacherView(Observer):
    def __init__(self):
        self.error = None
        self.success = False

    def update(self, data):
        self.success = data.get("success", False)
        self.error = data.get("error")

    def render(self):
        return render_template('add_teacher_form.html', error=self.error)


class UpdateTeacherView(Observer):
    def __init__(self):
        self.teacher = None
        self.teacher_id = None
        self.error = None
        self.success = False

    def update(self, data):
        self.success = data.get("success", False)
        self.teacher = data.get("teacher")
        self.teacher_id = data.get("teacher_id")
        self.error = data.get("error")

    def render(self):
        # Если нет teacher, но есть form_data, используем его
        form_data = self.teacher if isinstance(self.teacher, dict) else None
        return render_template('update_teacher_form.html',
                               teacher=self.teacher,
                               form_data=form_data,
                               teacher_id=self.teacher_id,
                               error=self.error)


class DeleteTeacherView(Observer):
    def __init__(self):
        self.success = False
        self.error = None
        self.teacher_id = None

    def update(self, data):
        self.success = data.get("success", False)
        self.error = data.get("error")
        self.teacher_id = data.get("teacher_id")

    def render(self):
        pass
