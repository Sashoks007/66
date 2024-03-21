import tkinter as tk
import tkinter.messagebox
import pymysql.cursors

class ListInput:
    def __init__(self, db_name, tb_name):
        self.db_name = db_name
        self.tb_name = tb_name

    def input_list_and_save(self):
        input_window = tk.Tk()
        input_window.title("Ввод списка")

        list_label = tk.Label(input_window, text="Введите список из 95 элементов через пробел:")
        list_label.pack()

        list_entry = tk.Entry(input_window, width=50)
        list_entry.pack()

        def show_even_indices():
            input_list = list(map(int, list_entry.get().split()))
            even_indices = [str(i) for i in range(len(input_list)) if input_list[i] % 2 == 0]
            even_indices_str = "\n".join(even_indices)

            result_window = tk.Tk()
            result_window.title("Индексы четных элементов")
            result_label = tk.Label(result_window, text=even_indices_str)
            result_label.pack()

            connection = pymysql.connect(host="localhost",
                                        user="root",
                                        password="root",
                                        database=self.db_name,
                                        cursorclass=pymysql.cursors.Cursor)
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO {self.tb_name} (list, indexes) VALUES ('{list_entry.get()}', '{even_indices_str}')")
            connection.commit()

        show_button = tk.Button(input_window, text="Показать индексы четных элементов", command=show_even_indices)
        show_button.pack()

app = App()
app.mainloop()