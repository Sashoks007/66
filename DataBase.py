
import tkinter as tk
import tkinter.messagebox
import pymysql.cursors

class DatabaseCreation:
    def init(self, db_name):
        self.db_name = db_name

    def create_database(self):
        try:
            conn = pymysql.connect(host="localhost",
                                   user="root",
                                   password="root",
                                   database=self.db_name,
                                   cursorclass=pymysql.cursors.Cursor)
            print("Вы подключились")
            tkinter.messagebox.showinfo("Вы подключились", self.db_name)
        except pymysql.err.MySQLError:
            conn = pymysql.connect(host="localhost",
                                   user="root",
                                   password="root",
                                   cursorclass=pymysql.cursors.Cursor)

            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
            print("Вы создали БД")
            tkinter.messagebox.showinfo("Вы создали БД", self.db_name)
        return conn

    def list_databases(self):
        connection = self.create_database()
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES;")
        databases = cursor.fetchall()

        db_list = [db[0] for db in databases]
        db_list_str = "\\n".join(db_list)

        tkinter.messagebox.showinfo("Список баз данных", db_list_str)

class TableCreation:
    def init(self, db_name, tb_name):
        self.db_name = db_name
        self.tb_name = tb_name

    def create_table(self):
        connection = pymysql.connect(host="localhost",
                                    user="root",
                                    password="root",
                                    database=self.db_name,
                                    cursorclass=pymysql.cursors.Cursor)
        cursor = connection.cursor()
        try:
            cursor.execute(f"SELECT * FROM {self.tb_name}")
            print("Таблица подключена")
            tkinter.messagebox.showinfo("Таблица подключена", self.tb_name)
        except pymysql.err.MySQLError:
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {self.tb_name} (id bigint NOT NULL AUTO_INCREMENT,"
                f" list varchar(1000) NOT NULL,"
                f" indexes varchar(1000) NOT NULL,"
                f" PRIMARY KEY (id)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;")
            connection.commit()
            print("Таблица создана и подключена")
            tkinter.messagebox.showinfo("Таблица создана и подключена", self.tb_name)

    def list_tables(self):
        connection = pymysql.connect(host="localhost",
                                    user="root",
                                    password="root",
                                    database=self.db_name,
                                    cursorclass=pymysql.cursors.Cursor)
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()

        table_list = [table[0] for table in tables]
        table_list_str = "\\n".join(table_list)

        tkinter.messagebox.showinfo("Список таблиц", table_list_str)

class App(tk.Tk):
    def init(self):
        super().init()
        self.title("Создание базы данных и таблицы")

        self.create_db_label = tk.Label(self, text="Имя базы данных:")
        self.create_db_label.pack()
        self.create_db_entry = tk.Entry(self, textvariable=tk.StringVar())
        self.create_db_entry.pack()

        self.create_db_button = tk.Button(self, text="Создать базу данных", command=self.create_database)
        self.create_db_button.pack()

        self.create_table_label = tk.Label(self, text="Имя таблицы:")
        self.create_table_label.pack()
        self.create_table_entry = tk.Entry(self, textvariable=tk.StringVar())
        self.create_table_entry.pack()
        self.create_table_button = tk.Button(self, text="Создать таблицу", command=self.create_table)
        self.create_table_button.pack()

    def create_database(self):
        db_creator = DatabaseCreation(self.create_db_entry.get())
        db_creator.create_database()

    def create_table(self):
        table_creator = TableCreation(self.create_db_entry.get(), self.create_table_entry.get())
        table_creator.create_table()

app = App()
app.mainloop()


