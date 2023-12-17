import tkinter as tk
from tkinter import ttk
from sqlalchemy import create_engine, text
import config


class Autorization(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Вход в систему')
        self.iconbitmap('')
        self.geometry('850x400')
        self['background'] = 'gray'
        self.resizable(False, False)

        self.db = db
        self.init_autorization_page()

    def init_autorization_page(self):
        self.label_welcome = ttk.Label(self, text='Добро пожаловать в систему управления!',
                                        font=("Helvetica", 24, 'bold'), foreground='white', background='gray')
        self.label_welcome.pack(pady=(50, 0))

        self.label_welcome_subtitle = ttk.Label(self, text='Введите логин и пароль от аккаунта',
                                        font=("Helvetica", 16, 'bold'), foreground='white', background='gray')
        self.label_welcome_subtitle.pack(pady=(25, 0))

        s = ttk.Style()
        s.configure('TFrame', background='gray')

        btn_frame_login = ttk.Frame(self, style='TFrame')
        btn_frame_login.pack()

        self.label_login_autorazation = ttk.Label(btn_frame_login, text='Логин:',
                                                font=("Helvetica", 16, 'bold'), foreground='white', background='gray')
        self.label_login_autorazation.pack(side=tk.LEFT, pady=(25, 0))

        self.entry_login_autorization = ttk.Entry(btn_frame_login, font=("Helvetica", 14, 'bold'), width=30)
        self.entry_login_autorization.pack(side=tk.LEFT, pady=(25, 0), padx=(20, 0))

        btn_frame_password = ttk.Frame(self)
        btn_frame_password.pack()

        self.label_password_autorazation = ttk.Label(btn_frame_password, text='Пароль:',
                                                    font=("Helvetica", 16, 'bold'), foreground='white', background='gray')
        self.label_password_autorazation.pack(side=tk.LEFT, pady=(25, 0))

        self.entry_password_autorization = ttk.Entry(btn_frame_password, font=("Helvetica", 14, 'bold'), width=30, show='*')
        self.entry_password_autorization.pack(side=tk.LEFT, pady=(25, 0), padx=(5, 0))

        btn_frame_btn_autorization = ttk.Frame(self)
        btn_frame_btn_autorization.pack()

        self.show_password = ttk.Button(btn_frame_btn_autorization, text='Показать пароль', command=self.show_password_func)
        self.show_password.pack(side=tk.LEFT, pady=20, padx=(0, 20))

        self.btn_autorization = ttk.Button(btn_frame_btn_autorization, text='Вход в систему', width=40, command=self.check_valid_account)
        self.btn_autorization.pack(side=tk.LEFT, pady=20)

    def check_valid_account(self):
        login = self.entry_login_autorization.get()
        password = self.entry_password_autorization.get()

        lavid_login = self.db.cur.execute(
            f"SELECT * FROM db.users WHERE db.users.users_user_login='{login}' AND db.users.users_user_status='admin'"
        )

        results_login = self.db.cur.fetchall()
        if results_login:
            lavid_password = self.db.cur.execute(
                f"SELECT db.users.users_user_password FROM db.users WHERE db.users.users_user_login='{login}' AND db.users.users_user_password='{password}'"
            )
            results_password = self.db.cur.fetchall()
            if results_password:

                global id_autorization_user
                id_autorization_user = self.db.cur.execute(
                    f"SELECT db.users.users_user_id FROM db.users WHERE db.users.users_user_login='{login}' AND db.users.users_user_password='{password}'"
                )
                id_autorization_user = self.db.cur.fetchall()
                id_autorization_user = id_autorization_user[0][0]

                self.destroy()
                MainPage()
            else:
                PasswordError()
        else:
            LoginNotExits()

    def show_password_func(self):
        if self.show_password['text'] == 'Показать пароль':
            self.entry_password_autorization['show'] = ''
            self.show_password['text'] = 'Скрыть пароль'
        else:
            self.entry_password_autorization['show'] = '*'
            self.show_password['text'] = 'Показать пароль'





class LoginNotExits(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Ошибка!')
        self.iconbitmap('')
        self.geometry('700x350')
        self['background'] = 'gray'
        self.resizable(False, False)

        self.init_login_not_exits()

    def init_login_not_exits(self):
        self.label_error_login = ttk.Label(self, text='Аккаунт с таким логином не найден!',
                                            font=("Helvetica", 24, 'bold'), foreground='white', background='gray')
        self.label_error_login.pack(pady=(100, 0))

        self.btn_error_login = ttk.Button(self, text='Попробовать ещё раз', width=40, command=self.btn_error_login_okay)
        self.btn_error_login.pack(pady=50)

    def btn_error_login_okay(self):
        self.destroy()

class PasswordError(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Ошибка!')
        self.iconbitmap('')
        self.geometry('700x350')
        self['background'] = 'gray'
        self.resizable(False, False)

        self.init_password_error()

    def init_password_error(self):
        self.label_error_password = ttk.Label(self, text='Неверный пароль!',
                                            font=("Helvetica", 24, 'bold'), foreground='white', background='gray')
        self.label_error_password.pack(pady=(100, 0))

        self.btn_error_password = ttk.Button(self, text='Попробовать ещё раз', width=40, command=self.btn_error_password_okay)
        self.btn_error_password.pack(pady=50)

    def btn_error_password_okay(self):
        self.destroy()


########################################################################################################################
class MainPage(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Главная')
        self.iconbitmap('')
        self.geometry('1200x800')
        self['background'] = 'gray'
        self.resizable(False, False)

        self.db = db
        self.init_main_page()
        self.view_all_projects()
        self.view_not_approved_projects()


    def init_main_page(self):
        self.mainMenu = ttk.Notebook(self)

        tab_main = ttk.Frame(self.mainMenu)
        tab_not_approved_projects = ttk.Frame(self.mainMenu)
        tab_analytis = ttk.Frame(self.mainMenu)

        self.mainMenu.add(tab_main, text='Все проекты')
        self.mainMenu.add(tab_not_approved_projects, text='Утверждение')
        self.mainMenu.add(tab_analytis, text='Аналитика')

        self.mainMenu.pack(expand=1, fill="both")

        #tab_main

        def select_project_main_page(a):
            selected_item = self.tree_main_page.focus()
            global id_selected_project
            id_selected_project = self.tree_main_page.item(selected_item)['values'][0]

        self.label_main_page = ttk.Label(tab_main, text='Все проекты:',
                                         font=("Helvetica", 24, 'bold'), foreground='gray')
        self.label_main_page.pack(pady=(50, 0), padx=(50, 0))

        self.tree_main_page = ttk.Treeview(tab_main,
                                           columns=('project.id', 'project.title', 'project.description',
                                                    'project.status'),
                                           height=25,
                                           show='headings')
        self.tree_main_page.column('project.id', width=200, anchor=tk.CENTER)
        self.tree_main_page.column('project.title', width=200, anchor=tk.CENTER)
        self.tree_main_page.column('project.description', width=200, anchor=tk.CENTER)
        self.tree_main_page.column('project.status', width=200, anchor=tk.CENTER)

        self.tree_main_page.heading('project.id', text='Номер', anchor=tk.CENTER)
        self.tree_main_page.heading('project.title', text='Название', anchor=tk.CENTER)
        self.tree_main_page.heading('project.description', text='Описание', anchor=tk.CENTER)
        self.tree_main_page.heading('project.status', text='Статус', anchor=tk.CENTER)

        self.tree_main_page.bind("<<TreeviewSelect>>", select_project_main_page)

        self.tree_main_page.pack(pady=20)

        btn_frame_main_page = ttk.Frame(tab_main)
        btn_frame_main_page.pack()

        self.btn_add_project = ttk.Button(btn_frame_main_page, text='Добавить', width=30, command=self.open_added_project_page)
        self.btn_add_project.pack(side=tk.LEFT, pady=10, padx=15)

        self.btn_info_project = ttk.Button(btn_frame_main_page, text='Информация', width=30, command=self.open_info_project_page)
        self.btn_info_project.pack(side=tk.LEFT, pady=10, padx=15)

        self.btn_edit_project = ttk.Button(btn_frame_main_page, text='Редактировать', width=30, command=self.open_edit_project_page)
        self.btn_edit_project.pack(side=tk.LEFT, pady=10, padx=15)

        self.btn_delete_project = ttk.Button(btn_frame_main_page, text='Удалить', width=30, command=self.open_del_project_page)
        self.btn_delete_project.pack(side=tk.LEFT, pady=10, padx=15)

        self.btn_update_project = ttk.Button(btn_frame_main_page, text='Обновить', width=30, command=self.view_all_projects)
        self.btn_update_project.pack(side=tk.LEFT, pady=10, padx=15)

        process = self.db.cur.execute(
            f"SELECT COUNT(*) FROM db.projects WHERE db.projects.projects_project_status = 'Активен'"
        )
        process = self.db.cur.fetchone()
        self.proccess = process[0]

        realise = self.db.cur.execute(
            f"SELECT COUNT(*) FROM db.projects WHERE db.projects.projects_project_status = 'Закончен' AND db.projects.projects_project_status = 'На утверждении'"
        )
        realise = self.db.cur.fetchone()
        self.realise = realise[0]

        all_projects = self.db.cur.execute(
            f"SELECT COUNT(*) FROM db.projects"
        )
        all_projects = self.db.cur.fetchone()
        self.all_projects = all_projects[0]

        self.label_analytics_title = ttk.Label(tab_analytis, text='Аналитика',
                                             font=("Helvetica", 26, 'bold'), foreground='gray')
        self.label_analytics_title.pack(pady=(100, 0))

        self.label_analytics_all= ttk.Label(tab_analytis, text=f'Всего проектов: {self.all_projects}',
                                           font=("Helvetica", 22, 'bold'), foreground='gray')
        self.label_analytics_all.pack(pady=(100, 0))

        self.label_analytics_proccess = ttk.Label(tab_analytis, text=f'В процессе: {self.proccess}',
                                             font=("Helvetica", 22, 'bold'), foreground='gray')
        self.label_analytics_proccess.pack(pady=(100, 0))

        self.label_analytics_realise = ttk.Label(tab_analytis, text=f'Реализовано: {self.realise}',
                                                  font=("Helvetica", 22, 'bold'), foreground='gray')
        self.label_analytics_realise.pack(pady=(100, 0))



        def select_project_not_approved_page(a):
            selected_item_not_approved = self.tree_not_approved_page.focus()
            global id_selected_project_not_approved
            id_selected_project_not_approved = self.tree_not_approved_page.item(selected_item_not_approved)['values'][0]

        self.label_not_approved_page = ttk.Label(tab_not_approved_projects, text='Не утверждены:',
                                         font=("Helvetica", 24, 'bold'), foreground='gray')
        self.label_not_approved_page.pack(pady=(50, 0), padx=(50, 0))

        self.tree_not_approved_page = ttk.Treeview(tab_not_approved_projects,
                                           columns=('project.id', 'project.title', 'project.description',
                                                    'project.status'),
                                           height=25,
                                           show='headings')
        self.tree_not_approved_page.column('project.id', width=200, anchor=tk.CENTER)
        self.tree_not_approved_page.column('project.title', width=200, anchor=tk.CENTER)
        self.tree_not_approved_page.column('project.description', width=200, anchor=tk.CENTER)
        self.tree_not_approved_page.column('project.status', width=200, anchor=tk.CENTER)

        self.tree_not_approved_page.heading('project.id', text='Номер', anchor=tk.CENTER)
        self.tree_not_approved_page.heading('project.title', text='Название', anchor=tk.CENTER)
        self.tree_not_approved_page.heading('project.description', text='Описание', anchor=tk.CENTER)
        self.tree_not_approved_page.heading('project.status', text='Статус', anchor=tk.CENTER)

        self.tree_not_approved_page.bind("<<TreeviewSelect>>", select_project_not_approved_page)

        self.tree_not_approved_page.pack(pady=20)

        btn_frame_not_approved_page = ttk.Frame(tab_not_approved_projects)
        btn_frame_not_approved_page.pack()

        self.btn_approved_project = ttk.Button(btn_frame_not_approved_page, text='Утвердить', width=30, command=self.open_approved_project)
        self.btn_approved_project.pack(side=tk.LEFT, pady=10, padx=15)

        self.btn_update_not_approved = ttk.Button(btn_frame_not_approved_page, text='Обновить', width=30,
                                             command=self.view_not_approved_projects)
        self.btn_update_not_approved.pack(side=tk.LEFT, pady=10, padx=15)

    def view_all_projects(self):
        self.db.cur.execute(
            f"SELECT db.projects.projects_project_id, db.projects.projects_project_title, db.projects.projects_project_description, db.projects.projects_project_status FROM db.projects"
        )
        [self.tree_main_page.delete(i) for i in self.tree_main_page.get_children()]
        [self.tree_main_page.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

    def view_not_approved_projects(self):
        self.db.cur.execute(
            f"SELECT db.projects.projects_project_id, db.projects.projects_project_title, db.projects.projects_project_description, db.projects.projects_project_status FROM db.projects WHERE db.projects.projects_project_status = 'На утверждении'"
        )
        [self.tree_not_approved_page.delete(i) for i in self.tree_not_approved_page.get_children()]
        [self.tree_not_approved_page.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

    def open_approved_project(self):
        selected_item_not_approved_exits = self.tree_not_approved_page.selection()
        if selected_item_not_approved_exits:
            OpenApprovedProject()
        else:
            DontSelectedItem()

    def open_added_project_page(self):
        AddedNewProject()

    def open_info_project_page(self):
        selected_item_not_approved_exits = self.tree_main_page.selection()
        if selected_item_not_approved_exits:
            OpenInfoProject()
        else:
            DontSelectedItem()

    def open_edit_project_page(self):
        selected_item_not_approved_exits = self.tree_main_page.selection()
        if selected_item_not_approved_exits:
            OpenEditProject()
        else:
            DontSelectedItem()

    def open_del_project_page(self):
        selected_item_not_approved_exits = self.tree_main_page.selection()
        if selected_item_not_approved_exits:
            OpenDeleteProject()
        else:
            DontSelectedItem()

class DontSelectedItem(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Ошибка!')
        self.iconbitmap('')
        self.geometry('700x350')
        self['background'] = 'gray'
        self.resizable(False, False)

        self.init_dontselected_error()

    def init_dontselected_error(self):
        self.label_error_selected = ttk.Label(self, text='Не выбрана запись!',
                                            font=("Helvetica", 24, 'bold'), foreground='white', background='gray')
        self.label_error_selected.pack(pady=(100, 0))

        self.btn_error_selected = ttk.Button(self, text='Попробовать ещё раз', width=40, command=self.btn_error_selected_okay)
        self.btn_error_selected.pack(pady=50)

    def btn_error_selected_okay(self):
        self.destroy()

class AddedNewProject(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Добавить новый проект')
        self.iconbitmap('')
        self.geometry('1200x500')
        self['background'] = 'gray'
        self.resizable(False, False)

        self.db = db
        self.init_added_new_project_page()


    def init_added_new_project_page(self):
        st = ttk.Style()
        st.configure('st.TFrame', background='gray')

        self.label_added_new_project = ttk.Label(self, text='Добавить новый проект',
                                     font=("Helvetica", 24, 'bold'), foreground='white', background='gray')
        self.label_added_new_project.pack(pady=(100, 0))

        frame_title_project = ttk.Frame(self, style='st.TFrame')
        frame_title_project.pack()

        self.label_title = ttk.Label(frame_title_project, text='Название проекта:',
                                     font=("Helvetica", 22, 'bold'), foreground='white', background='gray')
        self.label_title.pack(side=tk.LEFT, padx=10, pady=(40, 0))

        self.entry_title = ttk.Entry(frame_title_project, font=("Helvetica", 16, 'bold'))
        self.entry_title.pack(side=tk.LEFT, padx=10, pady=(40, 0))

        frame_description_project = ttk.Frame(self, style='st.TFrame')
        frame_description_project.pack()

        self.label_description = ttk.Label(frame_description_project, text='Описание проекта:',
                                           font=("Helvetica", 22, 'bold'), foreground='white', background='gray')
        self.label_description.pack(side=tk.LEFT, padx=10, pady=(40, 0))

        self.entry_description = ttk.Entry(frame_description_project, font=("Helvetica", 16, 'bold'))
        self.entry_description.pack(side=tk.LEFT, padx=10, pady=(40, 0))

        frame_skills_project = ttk.Frame(self, style='st.TFrame')
        frame_skills_project.pack()

        self.label_skills = ttk.Label(frame_skills_project, text='Навыки:',
                                      font=("Helvetica", 22, 'bold'), foreground='white', background='gray')
        self.label_skills.pack(side=tk.LEFT, padx=10, pady=(40, 0))

        combobox_skills_values = ['Дата каратист', 'Игродел', '.NET']
        self.combobox_skills = ttk.Combobox(frame_skills_project, values=combobox_skills_values, width=35)
        self.combobox_skills.pack(side=tk.LEFT, padx=10, pady=(40, 0))

        self.btn_added_new_project = ttk.Button(self, text='Добавить проект', width=40, command=self.added_new_project)
        self.btn_added_new_project.pack(side=tk.TOP, pady=50)

    def added_new_project(self):
        title = self.entry_title.get()
        description = self.entry_description.get()
        skills = self.combobox_skills.get()

        if title == '':
            DontFieldsFilled()
        elif description == '':
            DontFieldsFilled()
        elif skills == '':
            DontFieldsFilled()
        else:
            self.db.cur.execute(
                f"INSERT INTO db.projects(projects_project_title, projects_project_description, projects_project_owner_users_user_id, projects_project_skills, projects_project_status) VALUES('{title}', '{description}', {id_autorization_user}, '{skills}', 'На утверждении') RETURNING projects_project_id"
            )
            self.db.connection.commit()
            last_id_project = self.db.cur.fetchone()
            last_id_project = last_id_project[0]

            self.db.cur.execute(
                f"INSERT INTO db.project_team(project_team_projects_project_id) VALUES({last_id_project}) RETURNING project_team_id"
            )
            self.db.connection.commit()
            last_id_team = self.db.cur.fetchone()
            last_id_team = last_id_team[0]

            self.db.cur.execute(
                f"INSERT INTO db.project_team_members(project_team_members_project_team_project_team_id, project_team_members_users_user_id, project_team_members_role) VALUES({last_id_team}, {id_autorization_user}, 'Владелец')"
            )
            self.db.connection.commit()
            self.destroy()
            Success()

class DontFieldsFilled(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Ошибка!')
        self.iconbitmap('')
        self.geometry('700x350')
        self['background'] = 'gray'
        self.resizable(False, False)

        self.init_filled_error()

    def init_filled_error(self):
        self.label_filled_selected = ttk.Label(self, text='Не все поля заполнены!',
                                            font=("Helvetica", 24, 'bold'), foreground='white', background='gray')
        self.label_filled_selected.pack(pady=(100, 0))

        self.btn_filled_selected = ttk.Button(self, text='Попробовать ещё раз', width=40, command=self.btn_error_filled_okay)
        self.btn_filled_selected.pack(pady=50)

    def btn_error_filled_okay(self):
        self.destroy()

class OpenInfoProject(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Информация о проекте')
        self.iconbitmap('')
        self.geometry('1200x800')
        self['background'] = 'gray'
        self.resizable(False, False)

        self.db = db
        self.init_info_project_page()

    def init_info_project_page(self):
        result = self.db.cur.execute(
            f"SELECT db.projects.projects_project_id, db.projects.projects_project_title, db.projects.projects_project_description, db.projects.projects_project_skills, db.projects.projects_project_status FROM db.projects WHERE db.projects.projects_project_id ={id_selected_project}"
        )
        result = self.db.cur.fetchone()
        self.number = result[0]
        self.title = result[1]
        self.description = result[2]
        self.skills = result[3]
        self.status = result[4]

        result_owner = self.db.cur.execute(
            f"SELECT db.users.users_user_login FROM db.users INNER JOIN db.project_team_members ON db.project_team_members.project_team_members_users_user_id = db.users.users_user_id INNER JOIN db.project_team ON db.project_team.project_team_id = db.project_team_members.project_team_members_project_team_project_team_id INNER JOIN db.projects ON db.projects.projects_project_id = db.project_team.project_team_projects_project_id WHERE db.projects.projects_project_id ={id_selected_project}"
        )
        result_owner = self.db.cur.fetchone()


        self.owner = result_owner[0]


        self.label_info_project = ttk.Label(self, text='Информация о проекте:',
                                     font=("Helvetica", 24, 'bold'), foreground='white', background='gray')
        self.label_info_project.pack(pady=(100, 0))

        self.label_info_number = ttk.Label(self, text=f'Номер: {self.number}',
                                            font=("Helvetica", 22, 'bold'), foreground='white', background='gray')
        self.label_info_number.pack(pady=(50, 0))

        self.label_info_title = ttk.Label(self, text=f'Название: {self.title}',
                                           font=("Helvetica", 22, 'bold'), foreground='white', background='gray')
        self.label_info_title.pack(pady=(50, 0))

        self.label_info_description = ttk.Label(self, text=f'Описание: {self.description}',
                                           font=("Helvetica", 22, 'bold'), foreground='white', background='gray')
        self.label_info_description.pack(pady=(50, 0))

        self.label_info_owner = ttk.Label(self, text=f'Владелец: {self.owner}',
                                           font=("Helvetica", 22, 'bold'), foreground='white', background='gray')
        self.label_info_owner.pack(pady=(50, 0))

        self.label_info_skills = ttk.Label(self, text=f'Скиллы: {self.skills}',
                                           font=("Helvetica", 22, 'bold'), foreground='white', background='gray')
        self.label_info_skills.pack(pady=(50, 0))

        self.label_info_status = ttk.Label(self, text=f'Статус: {self.status}',
                                           font=("Helvetica", 22, 'bold'), foreground='white', background='gray')
        self.label_info_status.pack(pady=(50, 0))

class OpenEditProject(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Редактировать')
        self.iconbitmap('')
        self.geometry('800x300')
        self['background'] = 'gray'
        self.resizable(False, False)

        self.db = db
        self.init_edit_project_page()

    def init_edit_project_page(self):
        self.btn_edit_project_info_page = ttk.Button(self, text='Редактировать информацию', width=40,
                                                command=self.edit_project_info)
        self.btn_edit_project_info_page.pack(side=tk.TOP, pady=(50, 0))

        self.btn_edit_project_team_page = ttk.Button(self, text='Команда', width=40,
                                                command=self.edit_project_team)
        self.btn_edit_project_team_page.pack(side=tk.TOP, pady=(50, 0))

        self.btn_edit_project_result_page = ttk.Button(self, text='Результаты', width=40,
                                                command=self.edit_project_info)
        self.btn_edit_project_result_page.pack(side=tk.TOP, pady=(50, 0))

    def edit_project_info(self):
        OpenEditProjectInfo()

    def edit_project_team(self):
        OpenEditProjectTeam()

class OpenEditProjectInfo(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Изменение информации о проекте')
        self.iconbitmap('')
        self.geometry('1200x600')
        self['background'] = 'gray'
        self.resizable(False, False)

        self.db = db
        self.init_edit_project_info_page()

    def init_edit_project_info_page(self):
        self.label_edit_project = ttk.Label(self, text='Изменить информацию о проекте',
                                            font=("Helvetica", 24, 'bold'), foreground='white', background='gray')
        self.label_edit_project.pack(pady=(100, 0))

        self.label_description_edit = ttk.Label(self, text='Описание проекта:',
                                                font=("Helvetica", 22, 'bold'), foreground='white', background='gray')
        self.label_description_edit.pack(pady=(20, 0))

        self.entry_description_edit = ttk.Entry(self, font=("Helvetica", 16, 'bold'), width=40)
        self.entry_description_edit.pack(pady=(20, 0))

        self.label_status = ttk.Label(self, text='Статус проекта:',
                                      font=("Helvetica", 22, 'bold'), foreground='white', background='gray')
        self.label_status.pack(pady=(20, 0))

        combobox_status_values = ['На утверждении', 'Активен', 'Закончен']
        self.combobox_status_edit = ttk.Combobox(self, values=combobox_status_values, width=40)
        self.combobox_status_edit.pack(pady=(20, 0))

        self.btn_edit_project_info = ttk.Button(self, text='Подвердить измениня', width=40, command=self.edit_project_info)
        self.btn_edit_project_info.pack(side=tk.TOP, pady=50)

    def edit_project_info(self):
        description = self.entry_description_edit.get()
        status = self.combobox_status_edit.get()
        if status == '':
            DontFieldsFilled()
        else:
            self.db.cur.execute(
                f"UPDATE db.projects SET projects_project_description = '{description}', projects_project_status = '{status}' WHERE projects_project_id ={id_selected_project}"
            )
            self.db.connection.commit()
            self.destroy()
            Success()

class OpenEditProjectTeam(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Изменение информации о команде')
        self.iconbitmap('')
        self.geometry('1200x800')
        self['background'] = 'gray'
        self.resizable(False, False)

        self.db = db
        self.init_edit_project_team_page()
        self.view_team_members()

    def init_edit_project_team_page(self):
        def select_team_member(a):
            selected_item = self.tree_team_page.focus()
            global id_selected_member
            id_selected_member = self.tree_team_page.item(selected_item)['values'][0]

        self.label_edit_project_team = ttk.Label(self, text='Команда проекта:',
                                            font=("Helvetica", 24, 'bold'), foreground='white', background='gray')
        self.label_edit_project_team.pack(pady=(100, 0))

        self.tree_team_page = ttk.Treeview(self,
                                           columns=('member.id', 'member.login'),
                                           height=25,
                                           show='headings')
        self.tree_team_page.column('member.id', width=200, anchor=tk.CENTER)
        self.tree_team_page.column('member.login', width=200, anchor=tk.CENTER)


        self.tree_team_page.heading('member.id', text='Номер', anchor=tk.CENTER)
        self.tree_team_page.heading('member.login', text='Логин', anchor=tk.CENTER)


        self.tree_team_page.bind("<<TreeviewSelect>>", select_team_member)

        self.tree_team_page.pack(pady=10)

        self.btn_delete_member = ttk.Button(self, text='Исключить из команды', width=40,
                                                command=self.delete_team_member)
        self.btn_delete_member.pack(pady=10)

    def view_team_members(self):
        self.db.cur.execute(
            f"SELECT db.users.users_user_id, db.users.users_user_login FROM db.projects INNER JOIN db.project_team ON db.project_team.project_team_projects_project_id = db.projects.projects_project_id INNER JOIN db.project_team_members ON db.project_team_members.project_team_members_project_team_project_team_id = db.project_team.project_team_id INNER JOIN db.users ON db.users.users_user_id = db.project_team_members.project_team_members_users_user_id WHERE db.projects.projects_project_id={id_selected_project}"
        )
        [self.tree_team_page.delete(i) for i in self.tree_team_page.get_children()]
        [self.tree_team_page.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

    def delete_team_member(self):
        self.db.cur.execute(
            f"DELETE FROM db.project_team_members WHERE project_team_members_users_user_id =1 AND db.project_team_members.project_team_members_project_team_project_team_id = (SELECT db.project_team.project_team_id FROM db.project_team WHERE db.project_team.project_team_projects_project_id = {id_selected_project})"
        )
        self.db.connection.commit()
        self.destroy()
        Success()

class OpenDeleteProject(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Удалить проект')
        self.iconbitmap('')
        self.geometry('800x500')
        self['background'] = 'gray'
        self.resizable(False, False)

        self.db = db
        self.init_delete_project_page()

    def init_delete_project_page(self):
        self.label_delete_project= ttk.Label(self, text='Вы хотите удалить проект?',
                                                 font=("Helvetica", 24, 'bold'), foreground='white', background='gray')
        self.label_delete_project.pack(pady=(100, 0))

        self.btn_yes_delete = ttk.Button(self, text='Да', width=40,
                                                command=self.delete_project)
        self.btn_yes_delete.pack(side=tk.TOP, pady=50)

        self.btn_no_delete = ttk.Button(self, text='Нет', width=40,
                                                command=self.destroy)
        self.btn_no_delete.pack(side=tk.TOP, pady=50)

    def delete_project(self):
        id_team = self.db.cur.execute(
            f"SELECT db.project_team.project_team_id FROM db.project_team WHERE db.project_team.project_team_projects_project_id ={id_selected_project}"
        )
        id_team = self.db.cur.fetchone()
        id_team = id_team[0]

        self.db.cur.execute(
            f"DELETE FROM db.project_team_members WHERE db.project_team_members.project_team_members_project_team_project_team_id ={id_team}"
        )
        self.db.connection.commit()

        self.db.cur.execute(
            f"DELETE FROM db.project_team WHERE db.project_team.project_team_projects_project_id ={id_selected_project}"
        )
        self.db.connection.commit()

        self.db.cur.execute(
            f"DELETE FROM db.projects WHERE projects_project_id ={id_selected_project}"
        )
        self.db.connection.commit()
        self.destroy()
        Success()

class OpenApprovedProject(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Утвердить проект')
        self.iconbitmap('')
        self.geometry('800x500')
        self['background'] = 'gray'
        self.resizable(False, False)

        self.db = db
        self.init_approved_project_page()

    def init_approved_project_page(self):
        self.label_approved_project= ttk.Label(self, text='Вы хотите утвердить проект?',
                                                 font=("Helvetica", 24, 'bold'), foreground='white', background='gray')
        self.label_approved_project.pack(pady=(100, 0))

        self.btn_yes_approved = ttk.Button(self, text='Да', width=40,
                                                command=self.approved_project)
        self.btn_yes_approved.pack(side=tk.TOP, pady=50)

        self.btn_no_approved = ttk.Button(self, text='Нет', width=40,
                                                command=self.destroy)
        self.btn_no_approved.pack(side=tk.TOP, pady=50)

    def approved_project(self):
        self.db.cur.execute(
            f"UPDATE db.projects SET projects_project_status = 'Активен' WHERE projects_project_id ={id_selected_project_not_approved}"
        )
        self.db.connection.commit()
        self.destroy()
        Success()

#######################################################################################

class Success(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Успешно')
        self.iconbitmap('')
        self.geometry('300x250')
        self['background'] = 'gray'
        self.resizable(False, False)

        self.db = db

        self.init_success()

    def init_success(self):
        self.label_success= ttk.Label(self, text='Успешно!',
                                      font=("Helvetica", 24, 'bold'), foreground='white', background='gray')
        self.label_success.pack(pady=(50, 0))

        self.btn_error_password = ttk.Button(self, text='Продолжить', width=25,
                                             command=self.btn_success)
        self.btn_error_password.pack(pady=(50, 0))

    def btn_success(self):
        self.destroy()


class DB:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}/{database}")
        self.connection = self.engine.raw_connection()
        self.cur = self.connection.cursor()


db = DB(config.host, config.user, config.password, config.db_name)
app = Autorization()

app.mainloop()