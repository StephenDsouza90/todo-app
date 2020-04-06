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
        user = self.customer.signup(session, username)
        return user
    
    @handle_session
    def get_user(self, session, username):
        user = self.customer.get_user(session, username)
        return user

    @handle_session
    def add_task(self, session, task_title, task_desc, task_date, user_id, category_id, status_id, priority_id):
        task = self.customer.add_task(session, task_title, task_desc, task_date, 
                    user_id, category_id, status_id, priority_id)
        return task

    @handle_session
    def get_categories(self, session):
        categories = self.customer.get_categories(session)
        return categories

    @handle_session
    def get_status(self, session):
        status = self.customer.get_status(session)
        return status

    @handle_session
    def get_priorities(self, session):
        priorities = self.customer.get_priorities(session)
        return priorities


    @handle_session
    def get_tasks(self, session, user_id):
        tasks = self.customer.get_tasks(session, user_id)
        return tasks

    @handle_session
    def get_task(self, session, task_id):
        task = self.customer.get_task(session, task_id)
        return task

    @handle_session
    def update_task(self, session, task_id, task_title, task_desc, task_date, category_id, status_id, priority_id):
        task = self.customer.update_task(session, task_id, task_title, 
                        task_desc, task_date, category_id, status_id, priority_id)
        return task
    
    @handle_session
    def delete_task(self, session, task_id):
        task = self.customer.delete_task(session, task_id)
        return task

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
        searchByParameter = self.customer.search_by(session, user_id, parameter)
        return searchByParameter
    
    ### METHODS FOR LOGS
    @handle_session
    def add_activity_log(self, session, user_id, activity_id, task_id, log_date):
        activity = self.customer.add_activity_log(session, user_id, activity_id, task_id, log_date)
        return activity
    
    @handle_session
    def get_all_activities(self, session, user_id):
        activities = self.customer.get_all_activities(session, user_id)
        return activities

    @handle_session
    def get_available_activities(self, session, activity_id):
        availableActivities = self.customer.get_available_activities(session, activity_id)
        return availableActivities

    @handle_session
    def delete_activity_log(self, session, task_id):
        activity = self.customer.delete_activity_log(session, task_id)
        return activity

    ### METHODS FOR FILE
    @handle_session
    def add_file(self, session, file_name, file_data, user_id):
        _file = self.customer.add_file(session, file_name, file_data, user_id)
        return _file
    
    @handle_session
    def get_files(self, session, user_id):
        _files = self.customer.get_files(session, user_id)
        return _files

    @handle_session
    def download_file(self, session, user_id, file_id):
        _file = self.customer.download_file(session, user_id, file_id)
        return _file

    @handle_session
    def delete_file(self, session, file_id):
        _file = self.customer.delete_file(session, file_id)
        return _file

    ### METHODS FOR GROUPS
    @handle_session
    def create_group(self, session, group_name, user_id):
        group = self.customer.create_group(session, group_name, user_id)
        return group
    
    @handle_session
    def get_all_users(self, session, user_id):
        users = self.customer.get_all_users(session, user_id)
        return users

    @handle_session
    def get_groups_created_by_user(self, session, user_id):
        groups = self.customer.get_groups_created_by_user(session, user_id)
        return groups

    @handle_session
    def send_request(self, session, group_id, receiver_id, sender_id):
        request = self.customer.send_request(session, group_id, receiver_id, sender_id)
        return request

    @handle_session
    def get_request(self, session, receiver_id):
        request = self.customer.get_request(session, receiver_id)
        return request

    @handle_session
    def delete_request(self, session, group_id, receiver_id):
        request = self.customer.delete_request(session, group_id, receiver_id)
        return request

    @handle_session
    def add_user_in_group(self, session, group_id, user_id):
        userInGroup = self.customer.add_user_in_group(session, group_id, user_id)
        return userInGroup

    @handle_session
    def get_groups_of_user(self, session, user_id):
        groupsOfUser = self.customer.get_groups_of_user(session, user_id)
        return groupsOfUser

    @handle_session
    def get_users_in_group(self, session, group_id):
        usersInGroup = self.customer.get_users_in_group(session, group_id)
        return usersInGroup

    @handle_session
    def get_group(self, session, group_id):
        group = self.customer.get_group(session, group_id)
        return group

    ### METHODS FOR ASSIGNING TASK TO OTHERS
    @handle_session
    def assign_task(self, session, task_title, task_desc, task_date, category_id, status_id, priority_id,  assigner_id, assignee_id, group_id):
        assignedTask = self.customer.assign_task(session, task_title, task_desc, 
                        task_date, category_id, status_id, priority_id,  
                        assigner_id, assignee_id, group_id)
        return assignedTask

    @handle_session
    def get_assignee(self, session, assignee_id):
        assignee = self.customer.get_assignee(session, assignee_id)
        return assignee

    @handle_session
    def get_assigned_tasks(self, session, user_id):
        assignedTasks = self.customer.get_assigned_tasks(session, user_id)
        return assignedTasks
    
    @handle_session
    def track_assigned_task(self, session, user_id):
        assignedTasks = self.customer.track_assigned_task(session, user_id)
        return assignedTasks

    @handle_session
    def update_assigned_task(self, session, task_id, status_id):
        assignedTasks = self.customer.update_assigned_task(session, task_id, status_id)
        return assignedTasks
   
    @handle_session
    def get_assigned_task(self, session, task_id):
        assignedTask = self.customer.get_assigned_task(session, task_id)
        return assignedTask