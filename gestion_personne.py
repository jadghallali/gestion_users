import tkinter as tk
from tkinter import ttk, messagebox

class Personne:
    def __init__(self, nom, prenom, age):
        self.nom = nom
        self.prenom = prenom
        self.age = age

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.age} ans)"

class GestionnairePersonnes:
    def __init__(self, master):
        self.master = master
        master.title("Gestion des Personnes")

        self.style = ttk.Style(master)
        self.configure_styles()

        self.personnes = []

        # --- Widgets ---
        self.label_nom = ttk.Label(master, text="Nom:")
        self.label_prenom = ttk.Label(master, text="Prénom:")
        self.label_age = ttk.Label(master, text="Âge:")

        self.entry_nom = ttk.Entry(master)
        self.entry_prenom = ttk.Entry(master)
        self.entry_age = ttk.Entry(master)

        self.bouton_ajouter = ttk.Button(master, text="Ajouter", command=self.ajouter_personne, style="Accent.TButton")
        self.bouton_supprimer = ttk.Button(master, text="Supprimer", command=self.supprimer_personne, style="Danger.TButton")

        self.liste_personnes_var = tk.StringVar(value=[str(p) for p in self.personnes])
        self.liste_personnes = tk.Listbox(master, listvariable=self.liste_personnes_var, height=10, selectbackground="#a8dadc", selectforeground="black")

        # --- Layout ---
        self.label_nom.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_nom.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.label_prenom.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_prenom.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.label_age.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_age.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.bouton_ajouter.grid(row=3, column=0, columnspan=2, padx=10, pady=15, sticky="ew")
        self.bouton_supprimer.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.liste_personnes.grid(row=0, column=2, rowspan=5, padx=15, pady=10, sticky="nsew")

        # --- Configuration des colonnes pour le redimensionnement ---
        master.grid_columnconfigure(1, weight=1)
        master.grid_columnconfigure(2, weight=1)
        master.grid_rowconfigure(5, weight=1)

    def configure_styles(self):
        # Style général de l'application
        self.style.theme_use('clam') # Un thème neutre pour commencer

        # Style pour les labels
        self.style.configure("TLabel", foreground="#1d3557", font=("Segoe UI", 10))

        # Style pour les entrées
        self.style.configure("TEntry", foreground="#457b9d", font=("Segoe UI", 10))

        # Style pour le bouton Ajouter
        self.style.configure("Accent.TButton", foreground="white", background="#2a9d8f", font=("Segoe UI", 10, "bold"), padding=8)
        self.style.map("Accent.TButton",
                       background=[("active", "#52b788"), ("disabled", "#808080")],
                       foreground=[("disabled", "#c0c0c0")])

        # Style pour le bouton Supprimer
        self.style.configure("Danger.TButton", foreground="white", background="#e63946", font=("Segoe UI", 10, "bold"), padding=8)
        self.style.map("Danger.TButton",
                       background=[("active", "#ef476f"), ("disabled", "#808080")],
                       foreground=[("disabled", "#c0c0c0")])

        # Style pour la Listbox
        self.style.configure("TListbox", font=("Segoe UI", 10), background="#f1faee")

    def ajouter_personne(self):
        nom = self.entry_nom.get()
        prenom = self.entry_prenom.get()
        age_str = self.entry_age.get()

        if not nom or not prenom or not age_str:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return

        try:
            age = int(age_str)
            if age < 0:
                messagebox.showerror("Erreur", "L'âge doit être un nombre positif.")
                return
        except ValueError:
            messagebox.showerror("Erreur", "L'âge doit être un nombre entier.")
            return

        personne = Personne(nom, prenom, age)
        self.personnes.append(personne)
        self.mettre_a_jour_liste()
        self.vider_champs()

    def supprimer_personne(self):
        selection = self.liste_personnes.curselection()
        if selection:
            index = selection[0]
            del self.personnes[index]
            self.mettre_a_jour_liste()
        else:
            messagebox.showinfo("Information", "Veuillez sélectionner une personne à supprimer.")

    def mettre_a_jour_liste(self):
        self.liste_personnes_var.set([str(p) for p in self.personnes])

    def vider_champs(self):
        self.entry_nom.delete(0, tk.END)
        self.entry_prenom.delete(0, tk.END)
        self.entry_age.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = GestionnairePersonnes(root)
    root.mainloop()