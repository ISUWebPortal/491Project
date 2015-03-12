import flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask.views import MethodView
from flask_login import login_required
from flask_login import current_user

import models


class gradebookScreenView(MethodView):
    decorators = [login_required]

    def get(self):
        if(current_user.permissions == 1):
            return render_template('studentGradebook.html')

        else:
            return render_template('authorGradebook.html')


class courseGradeView(MethodView):

    def get(self, courseID):
        course = models.Course.query.filter_by(id=int(courseID) - 1000).first()
        tasks = course.tasks
        data = []
        for u in course.users:
            if u.id != current_user.id:
                for task in course.tasks:
                    response = models.TaskResponse.query.filter(models.TaskResponse.task_id == task.id, models.TaskResponse.student_id == u.id).order_by(
                        models.TaskResponse.datetime.desc()).first()
                    r = {
                        'user': u,
                        'task': task,
                        'response': response
                    }
                    data.append(r)
        if course in current_user.courses:
            return render_template("courseGrades.html", data = data)
        else:
            return render_template("home.html")


        

