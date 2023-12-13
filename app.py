from tkinter import *
import ttkbootstrap as ttk
import sqlite3
import datetime
from sqlalchemy import create_engine, text
from ttkbootstrap.dialogs import Messagebox
from tkinter import messagebox
import config

class MainPage(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.db = db

        self.init_main_page()
        self.view_all_projects()
        self.view_not_approved()

    def init_main_page(self):
        def select_not_approved_project(a):
            item = self.tree_not_approved.focus()
            global id_not_approved_project
            id_not_approved_project = self.tree_not_approved.item(item)['values'][0]
            ApprovedProject()

        def select_edit_project(a):
            item = self.tree_main_page.focus()
            global id_edit_project
            id_edit_project = self.tree_main_page.item(item)['values'][0]
            EditProject()

        btn_added = ttk.Button(self, text='Добавить новый проект', bootstyle="success", width=20,
                               command=self.added_project_page)
        btn_added.pack(pady=50)

        self.tabControl = ttk.Notebook(self)

        tab_main = ttk.Frame(self.tabControl)
        tab_not_approved_projects = ttk.Frame(self.tabControl)
        tab_add_project = ttk.Frame(self.tabControl)

        self.tabControl.add(tab_main, text='Главная')
        self.tabControl.add(tab_not_approved_projects, text='Утверждение')


        self.tabControl.pack(expand=1, fill="both")

        self.label_main_page = ttk.Label(tab_main, text='Все проекты:',
                                             font=("Helvetica", 24, 'bold'))
        self.label_main_page.pack(pady=(50, 0))

        self.tree_main_page = ttk.Treeview(tab_main,
                                           columns=('project.title', 'project.description', 'project.skills',
                                                    'project.status', 'project.owner'),
                                           height=35,
                                           show='headings')
        self.tree_main_page.column('project.title', width=200, anchor=ttk.CENTER)
        self.tree_main_page.column('project.description', width=200, anchor=ttk.CENTER)
        self.tree_main_page.column('project.skills', width=200, anchor=ttk.CENTER)
        self.tree_main_page.column('project.status', width=200, anchor=ttk.CENTER)
        self.tree_main_page.column('project.owner', width=200, anchor=ttk.CENTER)

        self.tree_main_page.heading('project.title', text='Название проекта', anchor=ttk.CENTER)
        self.tree_main_page.heading('project.description', text='Описание', anchor=ttk.CENTER)
        self.tree_main_page.heading('project.skills', text='Скилы', anchor=ttk.CENTER)
        self.tree_main_page.heading('project.status', text='Статус', anchor=ttk.CENTER)
        self.tree_main_page.heading('project.owner', text='Владелец', anchor=ttk.CENTER)

        self.tree_main_page.bind('<ButtonRelease-1>', select_edit_project)

        self.tree_main_page.pack(pady=(80, 150))



        self.label_not_approved = ttk.Label(tab_not_approved_projects, text='Проекты на утверждение:',
                                            font=("Helvetica", 24, 'bold'))
        self.label_not_approved.pack(pady=(50, 0))

        self.tree_not_approved = ttk.Treeview(tab_not_approved_projects,
                                               columns=('project.id', 'project.title', 'project.description', 'project.skills',
                                                        'project.status', 'project.owner'),
                                               height=35,
                                               show='headings')
        self.tree_not_approved.column('project.id', width=200, anchor=ttk.CENTER)
        self.tree_not_approved.column('project.title', width=200, anchor=ttk.CENTER)
        self.tree_not_approved.column('project.description', width=200, anchor=ttk.CENTER)
        self.tree_not_approved.column('project.skills', width=200, anchor=ttk.CENTER)
        self.tree_not_approved.column('project.status', width=200, anchor=ttk.CENTER)
        self.tree_not_approved.column('project.owner', width=200, anchor=ttk.CENTER)

        self.tree_not_approved.heading('project.id', text='Номер проекта', anchor=ttk.CENTER)
        self.tree_not_approved.heading('project.title', text='Название проекта', anchor=ttk.CENTER)
        self.tree_not_approved.heading('project.description', text='Описание', anchor=ttk.CENTER)
        self.tree_not_approved.heading('project.skills', text='Скилы', anchor=ttk.CENTER)
        self.tree_not_approved.heading('project.status', text='Статус', anchor=ttk.CENTER)
        self.tree_not_approved.heading('project.owner', text='Владелец', anchor=ttk.CENTER)

        self.tree_not_approved.bind('<ButtonRelease-1>', select_not_approved_project)


        self.tree_not_approved.pack(pady=(80, 150))

    def added_project_page(self):
        AddedNewProject()

    def view_not_approved(self):
        self.db.cur.execute(
            f"SELECT db.projects.projects_project_id, db.projects.projects_project_title, db.projects.projects_project_description, db.projects.projects_project_skills, db.projects.projects_project_status, db.projects.projects_project_owner_users_user_id FROM db.projects WHERE projects_project_status = 'На утверждении'"
        )
        [self.tree_not_approved.delete(i) for i in self.tree_not_approved.get_children()]
        [self.tree_not_approved.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

    def view_all_projects(self):
        self.db.cur.execute(
            f"SELECT db.projects.projects_project_id, db.projects.projects_project_title, db.projects.projects_project_description, db.projects.projects_project_skills, db.projects.projects_project_status, db.projects.projects_project_owner_users_user_id FROM db.projects"
        )
        [self.tree_main_page.delete(i) for i in self.tree_main_page.get_children()]
        [self.tree_main_page.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

class ApprovedProject(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.db = db
        self.init_approved()
        self.get_data_project()

    def init_approved(self):
        self.title('Утвердить проект')
        self.geometry('1200x800')
        self.resizable(False, False)

        btn_approved = ttk.Button(self, text='Утвердить проект', bootstyle="success", width=20,
                                  command=self.approved_project)
        btn_approved.pack(pady=50)

        self.label_approved = ttk.Label(self, text='Информация о проекте:',
                                            font=("Helvetica", 24, 'bold'))
        self.label_approved.pack(pady=(50, 0))

        self.tree_approved = ttk.Treeview(self,
                                              columns=(
                                              'project.id', 'project.title', 'project.description', 'project.skills',
                                              'project.status', 'project.owner'),
                                              height=35,
                                              show='headings')
        self.tree_approved.column('project.id', width=200, anchor=ttk.CENTER)
        self.tree_approved.column('project.title', width=200, anchor=ttk.CENTER)
        self.tree_approved.column('project.description', width=200, anchor=ttk.CENTER)
        self.tree_approved.column('project.skills', width=200, anchor=ttk.CENTER)
        self.tree_approved.column('project.status', width=200, anchor=ttk.CENTER)
        self.tree_approved.column('project.owner', width=200, anchor=ttk.CENTER)

        self.tree_approved.heading('project.id', text='Номер проекта', anchor=ttk.CENTER)
        self.tree_approved.heading('project.title', text='Название проекта', anchor=ttk.CENTER)
        self.tree_approved.heading('project.description', text='Описание', anchor=ttk.CENTER)
        self.tree_approved.heading('project.skills', text='Скилы', anchor=ttk.CENTER)
        self.tree_approved.heading('project.status', text='Статус', anchor=ttk.CENTER)
        self.tree_approved.heading('project.owner', text='Владелец', anchor=ttk.CENTER)

        self.tree_approved.pack(pady=(80, 150))


    def approved_project(self):
        self.db.cur.execute(
            f"UPDATE db.projects SET projects_project_status = 'Активен' WHERE projects_project_id ={id_not_approved_project}"
        )
        self.db.connection.commit()
        self.destroy()
        Success()


    def get_data_project(self):
        self.db.cur.execute(
            f"SELECT db.projects.projects_project_id, db.projects.projects_project_title, db.projects.projects_project_description, db.projects.projects_project_skills, db.projects.projects_project_status, db.projects.projects_project_owner_users_user_id FROM db.projects WHERE projects_project_id = {id_not_approved_project}"
        )
        [self.tree_approved.delete(i) for i in self.tree_approved.get_children()]
        [self.tree_approved.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

class AddedNewProject(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.db = db
        self.init_added()

    def init_added(self):
        self.title('Добавить новый проект')
        self.geometry('1200x800')
        self.resizable(False, False)

        btn_added = ttk.Button(self, text='Добавить проект', bootstyle="success", width=20,
                                  command=self.added_project)
        btn_added.pack(pady=50)

        self.label_title = ttk.Label(self, text='Название проекта:',
                                            font=("Helvetica", 24, 'bold'))
        self.label_title.pack(pady=(50, 0))

        self.entry_title = ttk.Entry(self, bootstyle='secondary', font=("Helvetica", 8, 'bold'))
        self.entry_title.pack(side=ttk.TOP, padx=10, pady=(5, 20))

        self.label_description = ttk.Label(self, text='Описание проекта:',
                                     font=("Helvetica", 24, 'bold'))
        self.label_description.pack(pady=(50, 0))

        self.entry_description = ttk.Entry(self, bootstyle='secondary', font=("Helvetica", 8, 'bold'))
        self.entry_description.pack(side=ttk.TOP, padx=10, pady=(5, 20))

        self.label_skills = ttk.Label(self, text='Навыки:',
                                     font=("Helvetica", 24, 'bold'))
        self.label_skills.pack(pady=(50, 0))

        self.entry_skills = ttk.Entry(self, bootstyle='secondary', font=("Helvetica", 8, 'bold'))
        self.entry_skills.pack(side=ttk.TOP, padx=10, pady=(5, 20))

    def added_project(self):
        title = self.entry_title.get()
        description = self.entry_description.get()
        skills = self.entry_skills.get()


        self.db.cur.execute(
            f"INSERT INTO db.projects(projects_project_title, projects_project_description, projects_project_owner_users_user_id, projects_project_skills, projects_project_status) VALUES('{title}', '{description}', 2, '{skills}', 'На утверждении')"
        )
        self.db.connection.commit()
        self.destroy()
        Success()

class EditProject(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.db = db
        self.init_edit()

    def init_edit(self):
        self.title('Редактировать проект')
        self.geometry('1200x800')
        self.resizable(False, False)

        btn_edit = ttk.Button(self, text='Подвердить изменения', bootstyle="success", width=20,
                                  command=self.edit_project)
        btn_edit.pack(pady=50)

        btn_edit_team = ttk.Button(self, text='Команда проекта', bootstyle="success", width=20,
                              command=self.edit_team_project_page)
        btn_edit_team.pack(pady=50)

        btn_delete = ttk.Button(self, text='Удалить проект', bootstyle="success", width=20,
                                   command=self.delete_project)
        btn_delete.pack(pady=50)

        self.label_description_edit = ttk.Label(self, text='Описание проекта:',
                                           font=("Helvetica", 24, 'bold'))
        self.label_description_edit.pack(pady=(50, 0))

        self.entry_description_edit = ttk.Entry(self, bootstyle='secondary', font=("Helvetica", 8, 'bold'))
        self.entry_description_edit.pack(side=ttk.TOP, padx=10, pady=(5, 20))


        combobox_values = ['На утверждении', 'Активен', 'Закончен']
        self.combobox_status_edit = ttk.Combobox(self, values=combobox_values, bootstyle="secondary")
        self.combobox_status_edit.pack(side=ttk.LEFT, padx=35, pady=5)

    def edit_project(self):
        description = self.entry_description_edit.get()
        status = self.combobox_status_edit.get()


        self.db.cur.execute(
            f"UPDATE db.projects SET projects_project_description = '{description}', projects_project_status = '{status}' WHERE projects_project_id ={id_edit_project}"
        )
        self.db.connection.commit()
        self.destroy()
        Success()

    def delete_project(self):
        self.db.cur.execute(
            f"DELETE FROM db.projects WHERE projects_project_id ={id_edit_project}"
        )
        self.db.connection.commit()
        self.destroy()
        Success()

    def edit_team_project_page(self):
        EditProjectTeam()

class EditProjectTeam(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.db = db
        self.init_edit_team_project()
        self.edit_team_project()

    def init_edit_team_project(self):
        self.title('Редактирование команды проекта')
        self.geometry('1200x800')
        self.resizable(False, False)

        def select_delete_member(a):
            item = self.tree_project_team.focus()
            global id_team_member
            id_team_member = self.tree_project_team.item(item)['values'][0]
            DeleteTeamMember()

        self.label_project_team = ttk.Label(self, text='Команда проекта:',
                                            font=("Helvetica", 24, 'bold'))
        self.label_project_team.pack(pady=(50, 0))

        self.tree_project_team = ttk.Treeview(self,
                                              columns=(
                                              'users.id', 'users.login'),
                                              height=35,
                                              show='headings')
        self.tree_project_team.column('users.id', width=200, anchor=ttk.CENTER)
        self.tree_project_team.column('users.login', width=200, anchor=ttk.CENTER)


        self.tree_project_team.heading('users.id', text='Номер участника', anchor=ttk.CENTER)
        self.tree_project_team.heading('users.login', text='Логин участника', anchor=ttk.CENTER)


        self.tree_project_team.pack(pady=(80, 150))

    def edit_team_project(self):
        self.db.cur.execute(
            f"SELECT users_user_id, users_user_login FROM db.project_team_members INNER JOIN db.users ON db.users.users_user_id = db.project_team_members.project_team_members_users_user_id INNER JOIN db.project_team ON db.project_team.project_team_id = db.project_team_members.project_team_members_project_team_project_team_id INNER JOIN db.projects ON db.projects.projects_project_id = db.project_team.project_team_projects_project_id WHERE projects.projects_project_id ={id_edit_project}"
        )
        [self.tree_project_team.delete(i) for i in self.tree_project_team.get_children()]
        [self.tree_project_team.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

class DeleteTeamMember(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.db = db
        self.init_delete_team_member()

    def init_delete_team_member(self):
        self.title('Удалить участника')
        self.geometry('1200x800')
        self.resizable(False, False)

        btn_delete_member = ttk.Button(self, text='Подвердить удаление', bootstyle="success", width=20,
                                  command=self.delete_member)
        btn_delete_member.pack(pady=50)

#ЗАКОНЧИТЬ
    def delete_member(self):
        self.db.cur.execute(
            f"DELETE FROM db.projects WHERE projects_project_id ={id_edit_project}"
        )
        self.db.connection.commit()
        self.destroy()
        Success()

class Success(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)

        self.db = db

        self.init_registration()

    def init_registration(self):
        self.title('Успешно')
        self.geometry('200x400')
        self.resizable(False, False)

        self.label_success = ttk.Label(self, text='Успешно!',
                                            font=("Helvetica", 24, 'bold'))
        self.label_success.pack(pady=(50, 0))


class DB:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}/{database}")
        self.connection = self.engine.raw_connection()
        self.cur = self.connection.cursor()

if __name__ == "__main__":

    root = ttk.Window(themename='darkly')
    db = DB(config.host, config.user, config.password, config.db_name)

    app = MainPage(root)
    app.pack()

    root.title('Главная')
    root.iconbitmap('')
    root.geometry('1200x800')
    root.resizable(False, False)
    root.mainloop()