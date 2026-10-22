import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from classes import Task, TaskManager


class TaskManagerApp:
    def __init__(self, root):
        self.manager = TaskManager()
        self.root = root
        self.root.title("Менеджер задач")
        self.setup_ui()

    def setup_ui(self):
        # Поля ввода
        tk.Label(self.root, text="Название").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(self.root, width=33)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Описание").grid(row=1, column=0, padx=5, pady=5)
        self.desc_text = tk.Text(self.root, height=3, width=25)
        self.desc_text.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Срок (ГГГГ-ММ-ДД)").grid(row=2, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(self.root, width=33)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопки
        tk.Button(self.root, text="Добавить задачу", command=self.add_task).grid(row=3, column=0, pady=5)
        tk.Button(self.root, text="Удалить задачу", command=self.delete_task).grid(row=3, column=1, pady=5)

        # Список задач
        self.tasks_listbox = tk.Listbox(self.root, width=50)
        self.tasks_listbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        self.update_listbox()

    def add_task(self):
        title = self.title_entry.get().strip()
        description = self.desc_text.get("1.0", tk.END).strip()
        due_date = self.date_entry.get().strip()

        if not (title and description and due_date):
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return

        # проверяем, что дата введена правильно
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД, например 2026-11-30")
            return

        task = Task(title, description, due_date)
        self.manager.add_task(task)
        self.update_listbox()
        self.clear_inputs()

    def delete_task(self):
        selected = self.tasks_listbox.curselection()
        if selected:
            self.manager.delete_task(selected[0])
            self.update_listbox()
        else:
            messagebox.showinfo("Подсказка", "Сначала выберите задачу в списке")

    def update_listbox(self):
        self.tasks_listbox.delete(0, tk.END)
        for task in self.manager.tasks:
            self.tasks_listbox.insert(tk.END, f"{task.title} (до {task.due_date})")

    def clear_inputs(self):
        self.title_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        self.date_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
