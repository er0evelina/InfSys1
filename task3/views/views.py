from flask import render_template, request, redirect, url_for
from controllers.subject import Observer


class TeacherListView(Observer):
    def __init__(self):
        self.teachers = []
    
    def update(self, teachers):
        self.teachers = teachers
    
    def render(self):
        return render_template('index.html', teachers=self.teachers)


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
        self.error = None
        self.success = False
    
    def update(self, data):
        self.success = data.get("success", False)
        self.teacher = data.get("teacher")
        self.error = data.get("error")
    
    def render(self):
        return render_template('update_teacher_form.html', teacher=self.teacher, error=self.error)
