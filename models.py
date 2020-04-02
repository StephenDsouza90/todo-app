import time

from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, DateTime, Date, or_, LargeBinary, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class SQLBackend(object):
    """ SQLBackend manages creating the engine and session """

    def __init__(self, DB_URL):
        self.engine = None
        self.Session = sessionmaker(autocommit=False, expire_on_commit=False)
        self.setup_engine(DB_URL)
    
    def setup_engine(self, DB_URL):
        """ Return engine if it exist else create it """

        if self.engine:
            return
        self.engine = create_engine(DB_URL, echo=False, pool_recycle=3600, 
                        connect_args={'check_same_thread': False})
        self.Session.configure(bind=self.engine)

    def bootstrap(self):
        """ Establish a connection to the engine """

        connection = None
        for i in range(2):
            try:
                connection = self.engine.connect()
            except:
                time.sleep(i*2)
                continue
        if not connection:
            raise Exception("Couldn't connect to DB Server even after retries!")
        Base.metadata.create_all(self.engine)
        connection.close()


class User(Base):
    """ Represents users """

    __tablename__ = "users"
    user_id = Column(Integer(), primary_key=True, nullable=False, unique=True, 
                autoincrement=True)
    username = Column(String(256), nullable=False, unique=True)


class Task(Base):
    """ Represents user's task """

    __tablename__ = "task"
    task_id = Column(Integer(), primary_key=True, nullable=False, unique=True, 
                autoincrement=True)
    task_title = Column(String(256), nullable=False)
    task_desc = Column(String(256), nullable=False)
    task_date = Column(Date, nullable=False)
    user_id = Column(Integer(), ForeignKey("users.user_id"), nullable=False)
    category_id = Column(Integer(), ForeignKey("categories.category_id"), nullable=False)
    status_id = Column(Integer(), ForeignKey("status.status_id"), nullable=False)
    priority_id = Column(Integer(), ForeignKey("priority.priority_id"), nullable=False)


class Category(Base):
    """ Represents task category """

    __tablename__ = "categories"
    category_id = Column(Integer(), primary_key=True, nullable=False, 
                    unique=True, autoincrement=True)
    category_name = Column(String(256), nullable=False)


class Status(Base):
    """ Represents task status """

    __tablename__ = "status"
    status_id = Column(Integer(), primary_key=True, nullable=False, 
                    unique=True, autoincrement=True)
    status_name = Column(String(256), nullable=False)


class Priority(Base):
    """ Represents task priority """

    __tablename__ = "priority"
    priority_id = Column(Integer(), primary_key=True, nullable=False, unique=True, 
                    autoincrement=True)
    priority_name = Column(String(256), nullable=False)


class ActivityLog(Base):
    """ Represents user activity log """

    __tablename__ = "activities"
    log_id = Column(Integer(), primary_key=True, nullable=False, unique=True, 
                    autoincrement=True)
    user_id = Column(Integer(), ForeignKey("users.user_id"), nullable=False)
    activity_id = Column(Integer(), ForeignKey("available_activities.activity_id"), nullable=False)
    task_id = Column(Integer(), ForeignKey("task.task_id"), nullable=False)
    log_date = Column(DateTime(), nullable=False)


class AvailableActivities(Base):
    """ Represents activities available for a user """

    __tablename__ = "available_activities"
    activity_id = Column(Integer(), primary_key=True, nullable=False, unique=True, 
                    autoincrement=True)
    activity_name = Column(String(256), nullable=False)


class FilesContent(Base):
    """ Represents user's files """

    __tablename__ = "files"
    file_id = Column(Integer(), primary_key=True, unique=True, autoincrement=True)
    file_name = Column(String(256))
    file_data = Column(LargeBinary)
    user_id = Column(Integer(), ForeignKey("users.user_id"), nullable=False)


class Group(Base):
    """ Groups created by users """

    __tablename__ = "groups"
    group_id = Column(Integer(), primary_key=True, nullable=False, unique=True, 
                    autoincrement=True)
    group_name = Column(String(256), nullable=False)
    user_id = Column(Integer(), ForeignKey("users.user_id"), nullable=False)


class UserGroup(Base):
    """ Groups which users are in after accepted request """

    __tablename__ = "user_groups"
    id = Column(Integer(), primary_key=True)
    group_id = Column(Integer(), ForeignKey("groups.group_id"), nullable=False)
    user_id = Column(Integer(), ForeignKey("users.user_id"), nullable=False)


class Request(Base):
    """ Request sent to users to join a group """

    __tablename__ = "request"
    id = Column(Integer(), primary_key=True)
    group_id = Column(Integer(), ForeignKey("groups.group_id"), nullable=False)
    sender_id = Column(Integer(), ForeignKey("users.user_id"), nullable=False)
    receiver_id = Column(Integer(), ForeignKey("users.user_id"), nullable=False)


class TaskAssignment(Base):
    """ Task assigned by user """

    __tablename__ = "task_assignment"
    task_id = Column(Integer(), primary_key=True, nullable=False, unique=True, 
                autoincrement=True)
    task_title = Column(String(256), nullable=False)
    task_desc = Column(String(256), nullable=False)
    task_date = Column(Date, nullable=False)
    category_id = Column(Integer(), ForeignKey("categories.category_id"), nullable=False)
    status_id = Column(Integer(), ForeignKey("status.status_id"), nullable=False)
    priority_id = Column(Integer(), ForeignKey("priority.priority_id"), nullable=False)
    group_id = Column(Integer(), ForeignKey("groups.group_id"), nullable=False)
    assignee_id = Column(Integer(), ForeignKey("users.user_id"), nullable=False)
    assigner_id = Column(Integer(), ForeignKey("users.user_id"), nullable=False)


class Customer:
    """ Customer's operation """

    ### METHODS FOR TASK
    def signup(self, session, username):
        userSignup = User(username=username)
        session.add(userSignup)
        session.commit()
        return userSignup
    
    def login(self, session, username):
        userLogin = session.query(User).filter_by(username=username).first()
        return userLogin

    def add_task(self, session, task_title, task_desc, task_date, user_id, category_id, status_id, priority_id):
        addTask = Task(task_title=task_title, task_desc=task_desc, task_date=task_date,
            user_id=user_id, category_id=category_id, status_id=status_id, priority_id=priority_id)
        session.add(addTask)
        session.commit()
        return addTask

    def get_tasks(self, session, user_id):
        getTasks = session.query(Task, Category, Status, Priority).\
                    filter(Task.category_id == Category.category_id).\
                    filter(Task.status_id == Status.status_id).\
                    filter(Task.priority_id == Priority.priority_id).\
                    filter(Task.user_id == user_id)
        return getTasks

    def update_task(self, session, task_id, task_title, task_desc, task_date, category_id, status_id, priority_id):
        updateTask = session.query(Task).filter(Task.task_id == task_id).\
                        update({Task.task_title: task_title,
                                Task.task_desc: task_desc,
                                Task.task_date: task_date,
                                Task.category_id: category_id,
                                Task.status_id: status_id,
                                Task.priority_id: priority_id},
                                synchronize_session=False)
        session.commit()
        return updateTask

    def delete_task(self, session, task_id):
        deleteTask = session.query(Task).filter_by(task_id=task_id).delete()
        session.commit()
        return deleteTask

    def get_tasks_by_category(self, session, user_id, category_id):
        tasksByCategory = session.query(Task, Category).\
                            filter(Task.category_id == Category.category_id).\
                            filter(Task.category_id == category_id).\
                            filter(Task.user_id == user_id)
        return tasksByCategory

    def get_tasks_by_status(self, session, user_id, status_id):
        tasksByStatus = session.query(Task, Status).\
                            filter(Task.status_id == Status.status_id).\
                            filter(Task.status_id == status_id).\
                            filter(Task.user_id == user_id)
        return tasksByStatus

    def get_tasks_by_priority(self, session, user_id, priority_id):
        tasksByPriority = session.query(Task, Priority).\
                            filter(Task.priority_id == Priority.priority_id).\
                            filter(Task.priority_id == priority_id).\
                            filter(Task.user_id == user_id)
        return tasksByPriority

    def search_by(self, session, user_id, parameter):
        searchBy = session.query(Task).\
                        filter(Task.user_id == user_id).\
                        filter(or_(Task.task_title.like(parameter), 
                            Task.task_desc.like(parameter)))
        return searchBy


    ### METHODS FOR LOGS
    def add_activity_log(self, session, user_id, activity_id, task_id, log_date):
        addActivityLog = ActivityLog(user_id=user_id, activity_id=activity_id, task_id=task_id, log_date=log_date)
        session.add(addActivityLog)
        session.commit()
        return addActivityLog
    
    def allactivity(self, session, user_id):
        activityLog = session.query(ActivityLog, User, AvailableActivities, Task).\
                        filter(ActivityLog.activity_id == AvailableActivities.activity_id).\
                        filter(ActivityLog.user_id == User.user_id).\
                        filter(ActivityLog.task_id == Task.task_id).\
                        filter(ActivityLog.user_id == user_id)
        return activityLog

    def delete_log(self, session, task_id):
        deleleLog = session.query(ActivityLog).filter_by(task_id=task_id).delete()
        session.commit()
        return deleleLog


    ### METHODS FOR FILE
    def add_file(self, session, file_name, file_data, user_id):
        addFile = FilesContent(file_name=file_name, file_data=file_data, user_id=user_id)
        session.add(addFile)
        session.commit()
        return addFile
    
    def get_file(self, session, user_id):
        getFile = session.query(FilesContent).\
                    filter(FilesContent.user_id == user_id)
        return getFile

    def download_file(self, session, user_id, file_id):
        downloadFile = session.query(FilesContent).\
                    filter_by(user_id=user_id, file_id=file_id).first()
        return downloadFile

    def delete_file(self, session, file_id):
        deleteFile = session.query(FilesContent).filter_by(file_id=file_id).delete()
        session.commit()
        return deleteFile


    ### METHODS FOR GROUPS
    def create_group(self, session, group_name, user_id):
        createGroup = Group(group_name=group_name, user_id=user_id)
        session.add(createGroup)
        session.commit()
        return createGroup

    def add_user_to_group(self, session, group_id, user_id):
        addUserToGroup = UserGroup(group_id=group_id, user_id=user_id)
        session.add(addUserToGroup)
        session.commit()
        return addUserToGroup

    def send_request(self, session, group_id, receiver_id, sender_id):
        sendRequest = Request(group_id=group_id, receiver_id=receiver_id, sender_id=sender_id)
        session.add(sendRequest)
        session.commit()
        return sendRequest

    def delete_request(self, session, group_id, receiver_id):
        deleteRequest = session.query(Request).filter(and_(Request.group_id == group_id, Request.receiver_id == receiver_id)).delete()
        session.commit()
        return deleteRequest

    def get_curent_user_groups(self, session, user_id):
        currentUserGroups = session.query(UserGroup, Group).\
                            filter(UserGroup.group_id == Group.group_id).\
                            filter(Group.user_id == User.user_id).\
                            filter(UserGroup.user_id == user_id)
        return currentUserGroups

    def get_users_in_group(self, session, group_id):
        usersInGroup = session.query(UserGroup, User).\
                        filter(UserGroup.user_id == User.user_id).\
                        filter(UserGroup.group_id == group_id)
        return usersInGroup


    ### METHODS FOR ASSIGNING TASK TO OTHERS
    def assign_task(self, session, task_title, task_desc, task_date, category_id, status_id, priority_id,  assigner_id, assignee_id, group_id):
        assignTask = TaskAssignment(task_title=task_title, task_desc=task_desc, task_date=task_date, category_id=category_id, status_id=status_id,
                        priority_id=priority_id, assigner_id=assigner_id, assignee_id=assignee_id, group_id=group_id) 
        session.add(assignTask)
        session.commit()
        return assignTask

    def get_assigned_tasks(self, session, user_id):
        assignedTasks = session.query(TaskAssignment, Category, Priority, Status, User, Group).\
                        filter(TaskAssignment.category_id == Category.category_id).\
                        filter(TaskAssignment.priority_id == Priority.priority_id).\
                        filter(TaskAssignment.status_id == Status.status_id).\
                        filter(TaskAssignment.assigner_id == User.user_id).\
                        filter(TaskAssignment.group_id == Group.group_id).\
                        order_by(TaskAssignment.task_date).\
                        filter(TaskAssignment.assignee_id == user_id)
        return assignedTasks
    
    def track_assigned_task(self, session, user_id):
        trackTask = session.query(TaskAssignment, Category, Priority, Status, User, Group).\
                        filter(TaskAssignment.category_id == Category.category_id).\
                        filter(TaskAssignment.priority_id == Priority.priority_id).\
                        filter(TaskAssignment.status_id == Status.status_id).\
                        filter(TaskAssignment.assignee_id == User.user_id).\
                        filter(TaskAssignment.group_id == Group.group_id).\
                        filter(TaskAssignment.group_id == Group.group_id).\
                        order_by(TaskAssignment.task_date).\
                        filter(TaskAssignment.assigner_id == user_id)
        return trackTask

    def update_assigned_task(self, session, task_id, status_id):
        updateTask = session.query(TaskAssignment).filter(TaskAssignment.task_id == task_id).\
                        update({TaskAssignment.status_id: status_id},
                        synchronize_session=False)
        session.commit()
        return updateTask

    # filter(TaskAssignment.group_id == Group.group_id).\

    ### Helper functions
    def get_task(self, session, task_id):
        getTask = session.query(Task, Category, Status, Priority).\
                filter(Task.category_id == Category.category_id).\
                filter(Task.status_id == Status.status_id).\
                filter(Task.priority_id == Priority.priority_id).\
                filter(Task.task_id == task_id)
        return getTask

    def categories(self, session):
        categories = session.query(Category).all()
        return categories

    def status(self, session):
        status = session.query(Status).all()
        return status

    def priorities(self, session):
        priorities = session.query(Priority).all()
        return priorities
    
    def get_available_activity(self, session, activity_id):
        availableActivity = session.query(AvailableActivities).\
                                filter_by(activity_id=activity_id).first()
        return availableActivity
    
    def get_all_users(self, session, user_id):
        getUsers = session.query(User).filter(User.user_id != user_id)
        return getUsers

    def get_groups_created_by_user(self, session, user_id):
        getGroups = session.query(Group).filter(Group.user_id == user_id)
        return getGroups

    def get_request(self, session, receiver_id):
        getRequest = session.query(Request, Group, User).\
                        filter(Request.group_id == Group.group_id).\
                        filter(Request.sender_id == User.user_id).\
                        filter(Request.receiver_id == receiver_id)    
        return getRequest

    def get_group(self, session, group_id):
        getGroup = session.query(Group).filter(Group.group_id == group_id)
        return getGroup

    def get_assignee(self, session, assignee_id):
        getAssignee = session.query(User).filter(User.user_id == assignee_id)
        return getAssignee
    
    def get_assigned_task(self, session, task_id):
        getAssignedTask = session.query(TaskAssignment, Category, Status, Priority).\
                            filter(TaskAssignment.category_id == Category.category_id).\
                            filter(TaskAssignment.status_id == Status.status_id).\
                            filter(TaskAssignment.priority_id == Priority.priority_id).\
                            filter(TaskAssignment.task_id == task_id)
        return getAssignedTask

