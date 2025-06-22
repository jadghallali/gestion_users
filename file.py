import tkinter as tk
from tkinter import ttk, messagebox

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Application de Connexion")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.style.configure('TFrame', background='#e0e0e0')
        self.style.configure('TLabel', background='#e0e0e0', font=('Arial', 10))
        self.style.configure('TEntry', fieldbackground='white', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10, 'bold'),
                             background='#007bff', foreground='white',
                             relief='flat', borderwidth=0)
        self.style.map('TButton', background=[('active', '#0056b3')])

        self.create_login_widgets()

    def create_login_widgets(self):
        main_frame = ttk.Frame(self.root, padding="30 30 30 30")
        main_frame.pack(expand=True, fill='both')

        username_label = ttk.Label(main_frame, text="Nom d'utilisateur:")
        username_label.pack(pady=(10, 5), anchor='w')

        self.username_entry = ttk.Entry(main_frame, width=30)
        self.username_entry.pack(pady=(0, 10), fill='x')

        password_label = ttk.Label(main_frame, text="Mot de passe:")
        password_label.pack(pady=(10, 5), anchor='w')

        self.password_entry = ttk.Entry(main_frame, show="*", width=30)
        self.password_entry.pack(pady=(0, 20), fill='x')

        login_button = ttk.Button(main_frame, text="Se Connecter", command=self.login)
        login_button.pack(fill='x', pady=(0, 10))

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "password":
            messagebox.showinfo("Connexion Réussie", "Bienvenue, Admin !")
            self.root.destroy()
            self.open_dashboard()
        else:
            messagebox.showerror("Échec de la Connexion", "Nom d'utilisateur ou mot de passe invalide.")

    def open_dashboard(self):
        dashboard_root = tk.Tk()
        DashboardApp(dashboard_root)
        dashboard_root.mainloop()

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tableau de Bord des Tâches")
        self.root.geometry("600x400")
        self.root.resizable(True, True)

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.style.configure('TFrame', background='#f5f5f5')
        self.style.configure('TLabel', background='#f5f5f5', font=('Arial', 12))
        self.style.configure('TButton', font=('Arial', 10, 'bold'),
                             background='#28a745', foreground='white',
                             relief='flat', borderwidth=0)
        self.style.map('TButton', background=[('active', '#218838')])
        self.style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
        self.style.configure('Treeview', font=('Arial', 10), rowheight=25)

        self.create_dashboard_widgets()

    def create_dashboard_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20 20 20 20")
        main_frame.pack(expand=True, fill='both')

        title_label = ttk.Label(main_frame, text="Liste des Tâches à Effectuer", font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20), anchor='center')

        self.task_tree = ttk.Treeview(main_frame, columns=("Task", "Status"), show="headings", selectmode="browse")
        self.task_tree.heading("Task", text="Tâche")
        self.task_tree.heading("Status", text="Statut")

        self.task_tree.column("Task", width=300, anchor='w')
        self.task_tree.column("Status", width=150, anchor='center')

        self.task_tree.pack(fill='both', expand=True, pady=(0, 10))

        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.task_tree.pack(side="left", fill="both", expand=True)

        self.add_task("Imprimer le rapport mensuel", "En attente")
        self.add_task("Calculer les ventes trimestrielles", "En cours")
        self.add_task("Vérifier l'inventaire", "Terminé")
        self.add_task("Mettre à jour la base de données clients", "En attente")
        self.add_task("Préparer la présentation pour la réunion", "En attente")

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(10, 0))

        mark_done_button = ttk.Button(button_frame, text="Marquer comme Terminé", command=self.mark_task_done)
        mark_done_button.pack(side='left', padx=(0, 10))

        add_task_button = ttk.Button(button_frame, text="Ajouter une Tâche", command=self.add_new_task)
        add_task_button.pack(side='left', padx=(0, 10))

        exit_button = ttk.Button(button_frame, text="Quitter", command=self.root.destroy, style='TButton')
        exit_button.pack(side='right')

    def add_task(self, task_name, status):
        self.task_tree.insert("", "end", values=(task_name, status))

    def mark_task_done(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner une tâche à marquer comme terminée.")
            return

        for item in selected_item:
            current_values = self.task_tree.item(item, 'values')
            if current_values[1] != "Terminé":
                self.task_tree.item(item, values=(current_values[0], "Terminé"))
            else:
                messagebox.showinfo("Statut", "Cette tâche est déjà marquée comme 'Terminé'.")

    def add_new_task(self):
        new_task_window = tk.Toplevel(self.root)
        new_task_window.title("Ajouter une Nouvelle Tâche")
        new_task_window.geometry("300x150")
        new_task_window.transient(self.root)

        ttk.Label(new_task_window, text="Nom de la tâche:").pack(pady=10)
        task_entry = ttk.Entry(new_task_window, width=40)
        task_entry.pack(pady=5)

        def save_task():
            task_name = task_entry.get()
            if task_name:
                self.add_task(task_name, "En attente")
                new_task_window.destroy()
            else:
                messagebox.showwarning("Entrée requise", "Veuillez entrer un nom pour la tâche.")

        ttk.Button(new_task_window, text="Ajouter", command=save_task).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app=LoginApp(root)
    root.mainloop()
