import os
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import webbrowser

# Глобальные переменные
users = {"admin": "123", "doc1": "123", "doc2": "123", "doc3": "123"}
active_users = {"doc1": True, "doc2": True, "doc3": True}
patients_data = []
add_window = None  # Инициализируем переменную add_window
view_window = None

# Функции
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def login():
    username = username_entry.get()
    password = password_entry.get()

    if users.get(username) == password:
        if username == "admin":
            open_admin_window()
            root.withdraw()
        elif active_users.get(username, False):
            root.withdraw()  # Скрываем основное окно авторизации
            open_user_window()
        else:
            messagebox.showwarning("Ошибка", "Доступ запрещен")
    else:
        messagebox.showwarning("Ошибка", "Неверные учетные данные")
def open_user_window():
    user_window = tk.Toplevel(padx=200, pady=170)
    user_window.title("Пользовательский интерфейс")
    user_window.configure(bg="#99FF99")
    center_window(user_window, 700, 500)  # Центрируем окно
    tk.Button(user_window, text="Добавить животное", command=add_animal_window).pack(pady=5)
    tk.Button(user_window, text="Просмотр пациентов", command=view_patients).pack(pady=5)
    tk.Button(user_window, text="Выход", command=lambda: close_window(user_window, root)).pack(pady=5)

def add_animal_window():
    global add_window, pet_name, owner_name, animal_type, diagnosis, vaccinations, photo_path_entry, history_path_entry


    def clear_fields():
        pet_name.delete(0, tk.END)
        owner_name.delete(0, tk.END)
        animal_type.delete(0, tk.END)
        diagnosis.delete(0, tk.END)
        photo_path_entry.delete(0, tk.END)
        history_path_entry.delete(0, tk.END)
        for vaccination in vaccinations.values():
            vaccination.set(False)


    if add_window is not None:
        clear_fields()
        add_window.deiconify()
        return


    add_window = tk.Toplevel(root, padx=200, pady=40)
    add_window.title("Добавление животного")
    add_window.configure(bg="#99FF99")
    center_window(add_window, 700, 530)

    tk.Label(add_window, text="Кличка животного:", bg="#99FF99").pack()
    pet_name = tk.Entry(add_window)
    pet_name.pack()

    tk.Label(add_window, text="ФИО владельца:", bg="#99FF99").pack()
    owner_name = tk.Entry(add_window)
    owner_name.pack()

    tk.Label(add_window, text="Тип животного:", bg="#99FF99").pack()
    animal_type = tk.Entry(add_window)
    animal_type.pack()

    tk.Label(add_window, text="Диагноз:", bg="#99FF99").pack()
    diagnosis = tk.Entry(add_window)
    diagnosis.pack()

    vaccinations = {}
    for i in range(1, 4):
        var = tk.BooleanVar()
        cb = tk.Checkbutton(add_window, text=f"Прививка {i}", variable=var, bg="#99FF99")
        cb.pack()
        vaccinations[f"Прививка {i}"] = var

    tk.Label(add_window, text="Фото животного:", bg="#99FF99").pack()
    photo_path_entry = tk.Entry(add_window)
    photo_path_entry.pack(pady=5)
    tk.Button(add_window, text="Выбрать файл", command=lambda: select_file(photo_path_entry)).pack()

    tk.Label(add_window, text="История болезни:", bg="#99FF99").pack()
    history_path_entry = tk.Entry(add_window)
    history_path_entry.pack(pady=5)
    tk.Button(add_window, text="Выбрать файл", command=lambda: select_file(history_path_entry)).pack()

    def save_animal_data():
        data = {
            "Кличка": pet_name.get(),
            "Владелец": owner_name.get(),
            "Тип": animal_type.get(),
            "Диагноз": diagnosis.get(),
            "Прививки": ", ".join([key for key, value in vaccinations.items() if value.get()]),
            "Фото": photo_path_entry.get(),
            "История болезни": history_path_entry.get()
        }
        patients_data.append(data)
        messagebox.showinfo("Успешно", "Данные о животном добавлены")
        clear_fields()
        add_window.withdraw()

    tk.Button(add_window, text="Сохранить", command=save_animal_data).pack()
    tk.Button(add_window, text="Отмена", command=lambda: close_window(add_window)).pack()


def view_patients():
    global patient_table
    global view_window
    if view_window is not None and view_window.winfo_exists():
        view_window.deiconify()
    else:
        view_window = tk.Toplevel(root)
        view_window.title("Просмотр пациентов")
        view_window.configure(bg="#99FF99")
        center_window(view_window, 1000, 500)

        columns = ["Кличка", "Владелец", "Тип", "Диагноз", "Прививки"]
        patient_table = ttk.Treeview(view_window, columns=columns, show='headings')
        for col in columns:
            patient_table.heading(col, text=col)
        patient_table.pack(expand=True, fill='both')
        patient_table.bind("<Double-1>", on_double_click)

        for patient in patients_data:
            patient_table.insert('', 'end', values=list(patient.values()))


        tk.Button(view_window, text="Просмотр истории болезни", command=view_history).pack(pady=5)
        tk.Button(view_window, text="Просмотр фото", command=view_photo).pack(pady=2)

        tk.Button(view_window, text="Выход", command=lambda: close_window(view_window)).pack(pady=5)




def select_file(entry_widget):
    file_path = filedialog.askopenfilename()
    if file_path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, file_path)

def on_double_click(event):
    global patient_table
    item = event.widget.selection()[0]
    history_path = patient_table.item(item, "values")[6]
    if history_path and os.path.exists(history_path):
        webbrowser.open(history_path)
    else:
        messagebox.showinfo("Информация", "Файл истории болезни отсутствует")

def view_history():
    global patient_table
    selected_item = patient_table.selection()[0]
    history_path = patient_table.item(selected_item, "values")[6]
    if history_path and os.path.exists(history_path):
        webbrowser.open(history_path)
    else:
        messagebox.showinfo("Информация", "Файл истории болезни отсутствует")

def view_photo():
    global patient_table
    selected_item = patient_table.selection()[0]
    photo_path = patient_table.item(selected_item, "values")[5]
    if photo_path and os.path.exists(photo_path):
        webbrowser.open(photo_path)
    else:
        messagebox.showinfo("Информация", "Фото отсутствует")

def open_admin_window():
    global admin_window
    try:
        admin_window.deiconify()
    except NameError:
        admin_window = tk.Toplevel(root, padx=200, pady=70)
        admin_window.configure(bg="#99FF99")
        center_window(admin_window, 700, 500)
        admin_window.title("Администраторский интерфейс")

        def add_user():
            new_username = new_user_entry.get()
            new_password = new_pass_entry.get()
            if new_username in users:
                messagebox.showwarning("Ошибка", "Пользователь уже существует")
                return
            users[new_username] = new_password
            active_users[new_username] = True
            update_user_list()
            new_user_entry.delete(0, tk.END)
            new_pass_entry.delete(0, tk.END)

        def remove_user():
            selected_user = user_listbox.get(user_listbox.curselection())
            if selected_user in users:
                del users[selected_user]
                del active_users[selected_user]
                update_user_list()

        def update_user_list():
            user_listbox.delete(0, tk.END)
            for user in users:
                user_listbox.insert(tk.END, user)

        tk.Label(admin_window, text="Логин нового пользователя:", bg="#99FF99").pack()
        new_user_entry = tk.Entry(admin_window)
        new_user_entry.pack()

        tk.Label(admin_window, text="Пароль нового пользователя:", bg="#99FF99").pack()
        new_pass_entry = tk.Entry(admin_window, show="*")
        new_pass_entry.pack()

        tk.Button(admin_window, text="Добавить пользователя", command=add_user).pack(pady=5)
        tk.Button(admin_window, text="Удалить пользователя", command=remove_user).pack(pady=5)

        user_listbox = tk.Listbox(admin_window)
        user_listbox.pack()
        update_user_list()

        tk.Button(admin_window, text="Выйти", command=lambda: close_window(admin_window, root)).pack(pady=5)


def close_window(window, prev=None):
    window.withdraw()
    if prev:
        prev.deiconify()

root = tk.Tk()
root.title("Система авторизации")
root.configure(bg="#99FF99")
center_window(root, 700, 500)

frame = tk.Frame(root)
frame.configure(bg="#99FF99")
frame.pack(padx=200, pady=150)

tk.Label(frame, text="Имя пользователя:", bg="#99FF99").pack(pady=5)
username_entry = tk.Entry(frame)
username_entry.pack()

tk.Label(frame, text="Пароль:", bg="#99FF99").pack()
password_entry = tk.Entry(frame, show="*")
password_entry.pack()

login_button = tk.Button(frame, text="Войти", command=login)
login_button.pack(pady=10)

root.mainloop()
