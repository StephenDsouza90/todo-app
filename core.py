from models import SQLBackend, Customer
from decorator import handle_session


class Controller(SQLBackend):
    """ Controller class inherites from SQLBackend class and 
        composition from Customer class. 
        Controller class is responsible for handling the session in the DB """

    def __init__(self, DB_URL):
        super().__init__(DB_URL)
        self.customer = Customer()

    ### METHODS FOR TASK
    @handle_session
    def signup(self, session, username):
        userSignup = self.customer.signup(session, username)
        return userSignup
    
    @handle_session
    def login(self, session, username):
        userLogin = self.customer.login(session, username)
        return userLogin

    @handle_session
    def add_task(self, session, task_title, task_desc, task_date, user_id, category_id, status_id, priority_id):
        addTask = self.customer.add_task(session, task_title, task_desc, task_date, 
                    user_id, category_id, status_id, priority_id)
        return addTask

    @handle_session
    def get_tasks(self, session, user_id):
        getTasks = self.customer.get_tasks(session, user_id)
        return getTasks

    @handle_session
    def update_task(self, session, task_id, task_title, task_desc, task_date, category_id, status_id, priority_id):
        updateTask = self.customer.update_task(session, task_id, task_title, 
                        task_desc, task_date, category_id, status_id, priority_id)
        return updateTask
    
    @handle_session
    def delete_task(self, session, task_id):
        deleteTask = self.customer.delete_task(session, task_id)
        return deleteTask

    @handle_session
    def get_tasks_by_category(self, session, user_id, category_id):
        tasksByCategory = self.customer.get_tasks_by_category(session, user_id, category_id)
        return tasksByCategory

    @handle_session
    def get_tasks_by_status(self, session, user_id, status_id):
        tasksByStatus = self.customer.get_tasks_by_status(session, user_id, status_id)
        return tasksByStatus

    @handle_session
    def get_tasks_by_priority(self, session, user_id, priority_id):
        tasksByPriority = self.customer.get_tasks_by_priority(session, user_id, priority_id)
        return tasksByPriority
    
    @handle_session
    def search_by(self, session, user_id, parameter):
        searchBy = self.customer.search_by(session, user_id, parameter)
        return searchBy
    

    ### METHODS FOR LOGS
    @handle_session
    def add_activity_log(self, session, user_id, activity_id, task_id, log_date):
        addActivityLog = self.customer.add_activity_log(session, user_id, activity_id, task_id, log_date)
        return addActivityLog
    
    @handle_session
    def allactivity(self, session, user_id):
        activityLog = self.customer.allactivity(session, user_id)
        return activityLog

    @handle_session
    def delete_log(self, session, task_id):
        deleteLog = self.customer.delete_log(session, task_id)
        return deleteLog


    ### METHODS FOR FILE
    @handle_session
    def add_file(self, session, file_name, file_data, user_id):
        addFile = self.customer.add_file(session, file_name, file_data, user_id)
        return addFile
    
    @handle_session
    def get_file(self, session, user_id):
        getFile = self.customer.get_file(session, user_id)
        return getFile

    @handle_session
    def download_file(self, session, user_id, file_id):
        downloadFile = self.customer.download_file(session, user_id, file_id)
        return downloadFile

    @handle_session
    def delete_file(self, session, file_id):
        deleteFile = self.customer.delete_file(session, file_id)
        return deleteFile


    ### METHODS FOR GROUPS
    @handle_session
    def create_group(self, session, group_name, user_id):
        createGroup = self.customer.create_group(session, group_name, user_id)
        return createGroup
    
    @handle_session
    def add_user_to_group(self, session, group_id, user_id):
        addUserToGroup = self.customer.add_user_to_group(session, group_id, user_id)
        return addUserToGroup

    @handle_session
    def send_request(self, session, group_id, receiver_id, sender_id):
        sendRequest = self.customer.send_request(session, group_id, receiver_id, sender_id)
        return sendRequest

    @handle_session
    def delete_request(self, session, group_id, receiver_id):
        deleteRequest = self.customer.delete_request(session, group_id, receiver_id)
        return deleteRequest

    @handle_session
    def get_curent_user_groups(self, session, user_id):
        currentUserGroups = self.customer.get_curent_user_groups(session, user_id)
        return currentUserGroups

    @handle_session
    def get_users_in_group(self, session, group_id):
        usersInGroup = self.customer.get_users_in_group(session, group_id)
        return usersInGroup


    ### METHODS FOR ASSIGNING TASK TO OTHERS
    @handle_session
    def assign_task(self, session, task_title, task_desc, task_date, category_id, status_id, priority_id,  assigner_id, assignee_id, group_id):
        assignTask = self.customer.assign_task(session, task_title, task_desc, task_date, category_id, status_id, priority_id,  assigner_id, assignee_id, group_id)
        return assignTask

    @handle_session
    def get_assigned_tasks(self, session, user_id):
        assignedTasks = self.customer.get_assigned_tasks(session, user_id)
        return assignedTasks
    
    @handle_session
    def track_assigned_task(self, session, user_id):
        trackTask = self.customer.track_assigned_task(session, user_id)
        return trackTask

    @handle_session
    def update_assigned_task(self, session, task_id, status_id):
        updateTask = self.customer.update_assigned_task(session, task_id, status_id)
        return updateTask


    ### Helper functions
    @handle_session
    def get_task(self, session, task_id):
        getTask = self.customer.get_task(session, task_id)
        return getTask

    @handle_session
    def categories(self, session):
        categories = self.customer.categories(session)
        return categories

    @handle_session
    def status(self, session):
        status = self.customer.status(session)
        return status

    @handle_session
    def priorities(self, session):
        priorities = self.customer.priorities(session)
        return priorities
    
    @handle_session
    def get_available_activity(self, session, activity_id):
        availableActivity = self.customer.get_available_activity(session, activity_id)
        return availableActivity
    
    @handle_session
    def get_all_users(self, session, user_id):
        getUsers = self.customer.get_all_users(session, user_id)
        return getUsers

    @handle_session
    def get_groups_created_by_user(self, session, user_id):
        getGroups = self.customer.get_groups_created_by_user(session, user_id)
        return getGroups

    @handle_session
    def get_request(self, session, receiver_id):
        getRequest = self.customer.get_request(session, receiver_id)
        return getRequest

    @handle_session
    def get_group(self, session, group_id):
        getGroup = self.customer.get_group(session, group_id)
        return getGroup

    @handle_session
    def get_assignee(self, session, assignee_id):
        getAssignee = self.customer.get_assignee(session, assignee_id)
        return getAssignee
    
    @handle_session
    def get_assigned_task(self, session, task_id):
        getTask = self.customer.get_assigned_task(session, task_id)
        return getTask

