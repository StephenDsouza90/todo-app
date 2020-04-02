from io import BytesIO
from datetime import timedelta, date, datetime

import waitress
from flask import Flask, render_template, request, redirect, session, send_file, flash

import constants
from core import Controller
from decorator import handle_login


def create_app(fos):
    """ Creates the server app """

    app = Flask('Todo App')
    app.config["SECRET_KEY"] = "SECRET_KEY"

    @app.route("/")
    @handle_login
    def index():
        """ View all tasks of a user """

        tasks = fos.get_tasks(int(session.get("user_id")))
        overdue = []
        today = []
        tomorrow = []
        upcoming = []
        completed = []

        for task, category, status, priority in tasks:
            if task.task_date < date.today() and task.status_id == constants.ONGOING:
                ## Over task
                overdue.append((task, category, status, priority))
            elif task.task_date == date.today() and task.status_id == constants.ONGOING:
                ## Today task
                today.append((task, category, status, priority))
            elif task.task_date == date.today() + timedelta(days=1) and task.status_id == constants.ONGOING:
                ## Tomorrow task
                tomorrow.append((task, category, status, priority))
            elif task.task_date > date.today() and task.status_id == constants.ONGOING:
                ## Upcoming task
                upcoming.append((task, category, status, priority))
            elif task.status_id == constants.COMPLETED:
                ## Completed task
                completed.append((task, category, status, priority))
        
        context = {
            "overdue": overdue,
            "today": today,
            "tomorrow": tomorrow,
            "upcoming": upcoming,
            "completed": completed,

            "requests": fos.get_request(receiver_id=session.get("user_id"))
        }
        return render_template("index.html", context=context)

    @app.route("/get-started", methods=["GET", "POST"])
    def get_started():
        """ If user already exist then log user in, 
            otherwise add user and then log user in.
            Store username and user_id in session. """

        session.clear()
        if request.method == "POST":
            username = request.form.get("username")
            existing_user = fos.login(username)
            if not username:
                return render_template("error.html", message="Please provide a username!")
            elif existing_user is None:
                user = fos.signup(username)
                user_id = user.user_id
            elif existing_user.username == username:
                user_id = existing_user.user_id
            session["username"] = username
            session["user_id"] = str(user_id)
            session.permanent = True
            return redirect("/")
        else:
            return render_template("login.html")

    @app.route("/logout", methods=["GET"])
    def logout():
        """ User logout """

        session.clear()
        return redirect("/")


    ### FUNCTIONS FOR TASK
    @app.route("/add-task", methods=["GET", "POST"])
    @handle_login
    def add_task():
        """ Add a task """

        if request.method == "POST":
            task_title = request.form.get("task_title")
            task_desc = request.form.get("task_desc")
            x =  request.form.get("task_date")
            task_date = date(year=int(x[:4]), month=int(x[5:7]), day=int(x[8:10]))
            user_id = session.get("user_id")
            category_id = request.form.get("category_id")
            status_id = request.form.get("status_id")
            priority_id = request.form.get("priority_id")
            if not task_title or not task_desc:
                return render_template("error.html", message="Please fill in all details!")

            ## Add task in task table
            task = fos.add_task(task_title, task_desc, task_date,
                user_id, int(category_id), int(status_id), int(priority_id))

            ## Add activity log
            added_activity = fos.get_available_activity(constants.ADDED)
            fos.add_activity_log(user_id, added_activity.activity_id, task.task_id, datetime.now())

            flash("Task added!", "info")
            return redirect("/")
        else:
            context = {
                "categories": fos.categories(),
                "status": fos.status(),
                "priorities": fos.priorities(),
            }
            return render_template("add_task.html", context=context)

    # HTML does not support PUT request, POST request is used instead
    @app.route("/update-task/<int:task_id>", methods=["GET", "POST"])
    @handle_login
    def update_task(task_id):
        """ Update a task """

        if request.method == "POST":
            task_title = request.form.get("task_title")
            task_desc = request.form.get("task_desc")
            x =  request.form.get("task_date")
            task_date = date(year=int(x[:4]), month=int(x[5:7]), day=int(x[8:10]))
            category_id = request.form.get("category_id")
            status_id = request.form.get("status_id")
            priority_id = request.form.get("priority_id")
            if not task_title or not task_desc:
                return render_template("error.html", message="Please fill in all details!")

            ## Update task
            fos.update_task(task_id, task_title, task_desc, task_date, category_id, 
                status_id, priority_id)

            ## Add activity log
            added_activity = fos.get_available_activity(constants.UPDATED)
            fos.add_activity_log(int(session.get("user_id")), added_activity.activity_id, task_id, datetime.now())

            flash("Task updated!", "info")
            return redirect("/")
        else:
            context = {
                "task": fos.get_task(task_id),
                "categories": fos.categories(),
                "status": fos.status(),
                "priorities": fos.priorities()
            }
            return render_template("update_task.html", context=context)

    # HTML does not support DELETE request, GET request is used instead
    @app.route("/delete-task/<int:task_id>", methods=["GET"])
    @handle_login
    def delete_task(task_id):
        """ Delete a task """

        if request.method == "GET":
            fos.delete_task(task_id)
            fos.delete_log(task_id)
            flash("Task deleted!", "info")
            return redirect("/")

    @app.route("/search/c/<int:category_id>", methods=["GET"])
    @handle_login
    def get_task_by_category(category_id):
        """ Search for tasks by category """

        if request.method == "GET":
            resultTaskCategory = fos.get_tasks_by_category(session.get("user_id"), category_id)
            context = {
                "resultTaskCategory": resultTaskCategory
                }
            return render_template("results.html", context=context)

    @app.route("/search/s/<int:status_id>", methods=["GET"])
    @handle_login
    def get_task_by_status(status_id):
        """ Search for tasks by status """

        if request.method == "GET":
            resultTaskStatus = fos.get_tasks_by_status(session.get("user_id"), status_id)
            context = {
                "resultTaskStatus": resultTaskStatus
                }
            return render_template("results.html", context=context)

    @app.route("/search/p/<int:priority_id>", methods=["GET"])
    @handle_login
    def get_task_by_priority(priority_id):
        """ Search for tasks by priority """

        if request.method == "GET":
            resultTaskPriority = fos.get_tasks_by_priority(session.get("user_id"), priority_id)
            context = {
                "resultTaskPriority": resultTaskPriority
                }
            return render_template("results.html", context=context)

    @app.route("/search", methods=["GET"])
    @handle_login
    def search_by():
        """ Search task by title or desc """

        if request.method == "GET":
            parameter = "%" + request.args.get("parameter") + "%"
            resultSearchBy = fos.search_by(session.get("user_id"), parameter)
            context = {
                "resultSearchBy": resultSearchBy
                }
            return render_template("results.html", context=context)


    ### FUNCTIONS FOR LOGS (FOR TASKS ONLY)
    @app.route("/allactivity", methods=["GET"])
    @handle_login
    def allactivity():
        """ All activities of a user """

        if request.method == "GET":
            resultActivityLog = fos.allactivity(session.get("user_id"))
            context = {
                "resultActivityLog": resultActivityLog
            }
            return render_template("results.html", context=context)


    ### FUNCTIONS FOR FILE
    @app.route("/add-file", methods=["GET", "POST"])
    @handle_login
    def add_file():
        """ Add a task """

        if request.method == "POST":
            file_name = request.form.get("file_name")
            file_data = request.files["inputFile"]
            user_id = session.get("user_id")
            _file = fos.add_file(file_name, file_data.read(), user_id)
            flash("File added!", "info")
            return redirect("/files")
        else:
            return render_template("add_file.html")

    @app.route("/files", methods=["GET"])
    @handle_login
    def get_file():
        """ Get file """

        if request.method == "GET":
            resultFiles = fos.get_file(session.get("user_id"))            
            context = {
                "resultFiles": resultFiles
            }
            return render_template("results.html", context=context)

    @app.route("/download-file/<int:file_id>", methods=["GET"])
    @handle_login
    def download_file(file_id):
        """ Download file """

        if request.method == "GET":
            result = fos.download_file(session.get("user_id"), file_id)            
            return send_file(BytesIO(result.file_data), attachment_filename=f"{result.file_name}.pdf", as_attachment=False)

    @app.route("/delete-file/<int:file_id>", methods=["GET"])
    @handle_login
    def delete_file(file_id):
        """ Delete file """

        if request.method == "GET":
            fos.delete_file(file_id)
            flash("File deleted!", "info")
            return redirect("/files")


    ### FUNCTIONS FOR GROUPS
    @app.route("/create-group", methods=["GET", "POST"])
    @handle_login
    def create_group():
        """ Create a group """

        if request.method == "POST":
            group_name = request.form.get("group_name")
            user_id = session.get("user_id")
            group = fos.create_group(group_name, user_id)
            fos.add_user_to_group(group.group_id, user_id)
            return redirect("/groups")
        else:
            return render_template("create_group.html")

    @app.route("/groups", methods=["GET", "POST"])
    @handle_login
    def get_user_groups():
        """ users: Show all users except the one in session.
            groups_created_by_user: Groups created by a user. 
            groupsDict: Groups with its users. """

        if request.method == "POST":
            """ Nothing to POST yet """
            return redirect("/groups")
        else:
            groupsDict = {}
            currentGroupsOfUser = fos.get_curent_user_groups(session.get("user_id"))
            for UserGroup, Group in currentGroupsOfUser:
                groupsDict[Group.group_name] = [(_User.username, _UserGroup.group_id, _User.user_id) for _UserGroup, _User in fos.get_users_in_group(UserGroup.group_id)]
            context = {
                "users": fos.get_all_users(session.get("user_id")),
                "groups_created_by_user": fos.get_groups_created_by_user(session.get("user_id")),
                "groupsDict": groupsDict,
                "assigned_task": fos.get_assigned_tasks(session.get("user_id"))
            }
            return render_template("groups.html", context=context)

    @app.route("/send-request", methods=["POST"])
    @handle_login
    def send_request():
        """ Send a request to a another user to join a group """

        if request.method == "POST":
            group_id = request.form.get("group_id")
            # Person receiving the request
            receiver_id = request.form.get("receiver_id")
            # Person sending the request
            sender_id = session.get("user_id")
            fos.send_request(group_id, receiver_id, sender_id)
            flash("Request sent")
            return redirect("/")

    @app.route("/accept-request/<int:group_id>/<int:receiver_id>", methods=["POST"])
    @handle_login
    def accept_request(group_id, receiver_id):
        """ User accepts a request.
            Removing request from request table so it wont show again. """

        if request.method == "POST":
            fos.add_user_to_group(group_id, user_id=receiver_id)
            fos.delete_request(group_id, receiver_id)
            return redirect("/groups")

    @app.route("/decline-request/<int:group_id>/<int:receiver_id>", methods=["GET"])
    @handle_login
    def decline_request(group_id, receiver_id):
        """ User declines a request. """

        if request.method == "GET":
            fos.delete_request(group_id, receiver_id)
            flash("Request declined")
            return redirect("/")


    ### FUNCTIONS FOR ASSIGNING TASK TO OTHERS
    @app.route("/assign-task/<group_id>/<assignee_id>", methods=["GET", "POST"])
    @handle_login
    def assign_task(group_id, assignee_id):
        """ Assign a task to a user.
            Assigner: Person assigning the task.
            Assignee: Person to whom the task is being assigned """
        
        if request.method == "POST":
            task_title = request.form.get("task_title")
            task_desc = request.form.get("task_desc")
            x =  request.form.get("task_date")
            task_date = date(year=int(x[:4]), month=int(x[5:7]), day=int(x[8:10]))
            category_id = request.form.get("category_id")
            status_id = request.form.get("status_id")
            priority_id = request.form.get("priority_id")
            assigner_id = session.get("user_id")
            fos.assign_task(task_title, task_desc, task_date, category_id, status_id, priority_id,  assigner_id, assignee_id, group_id)
            flash("Task assigned!")
            return redirect("/groups")
        else:
            context = {
                "group_name": fos.get_group(group_id),
                "assignee_name": fos.get_assignee(assignee_id),
                "categories": fos.categories(),
                "status": fos.status(),
                "priorities": fos.priorities()
            }
            return render_template("assign_task.html", context=context)

    @app.route("/track-assigned-task", methods=["GET"])
    def track_assigned_task():
        """ User can track task they assigned to a user """
        
        context = {
            "tasks": fos.track_assigned_task(session.get("user_id"))
        }
        return render_template("track_task.html", context=context)

    @app.route("/update-assigned-task/<int:task_id>", methods=["GET", "POST"])
    def update_assigned_task(task_id):
        """ User can update the status of the task """

        if request.method == "POST":
            status_id = request.form.get("status_id")
            fos.update_assigned_task(task_id, status_id)
            flash("Assigned task updated!", "info")
            return redirect("/groups")
        else:
            context = {
                "assigned_task": fos.get_assigned_task(task_id),
                "status": fos.status(),
            }
            return render_template("update_assigned_task.html", context=context)

    return app


def main():
    """ Run the server """

    DB_URL = "sqlite:///todo.db"
    controller = Controller(DB_URL)
    controller.bootstrap()
    app = create_app(controller)
    waitress.serve(app, host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()