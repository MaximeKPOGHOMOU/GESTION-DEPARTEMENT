import tkinter as tk
from tkinter import ttk, Label, Button, SUNKEN
from tkinter import messagebox
import pandas as pd
import os  # Importer le module os pour manipuler les chemins de fichiers
class FenetreEtatEtudiant(tk.Tk):
    def __init__(self, donnees):
        super().__init__()

        self.title("IMPRESSION DES DONNEES")
        self.geometry("1000x600+155+70")
        self.resizable(False, False)
        self.configure(background="white")

        self.lbltitre = Label(self, borderwidth=3, relief=SUNKEN, text="LA LISTE DES ETUDIANTS", font=("Sans Serif", 25),
                              background="#2F4F4F", fg="#FFFAFA")
        self.lbltitre.place(x=0, y=0, width=1000, height=80)

        self.table_etat_etudiant = ttk.Treeview(self, columns=(1, 2, 3, 4, 5, 6), height=5, show="headings")
        self.table_etat_etudiant.place(x=55, y=90, width=890, height=450)

        self.table_etat_etudiant.heading(1, text="MAT")
        self.table_etat_etudiant.heading(2, text="NOM")
        self.table_etat_etudiant.heading(3, text="PRENOM")
        self.table_etat_etudiant.heading(4, text="GENRE")
        self.table_etat_etudiant.heading(5, text="NIVEAU")
        self.table_etat_etudiant.heading(6, text="PROMOTION")

        self.table_etat_etudiant.column(1, width=20)
        self.table_etat_etudiant.column(2, width=100)
        self.table_etat_etudiant.column(3, width=150)
        self.table_etat_etudiant.column(4, width=50)
        self.table_etat_etudiant.column(5, width=50)
        self.table_etat_etudiant.column(6, width=50)

        self.btnAfficher = Button(self, text="EXPORTER", bd=4, font=("Arial", 12), bg="#FF4500", fg="white",
                                  command=self.exporter_vers_excel)
        self.btnAfficher.place(x=400, y=550, width=150)

        # Afficher les données reçues en argument
        self.afficher_donnees(donnees)

    def afficher_donnees(self, donnees):
        for values in donnees:
            self.table_etat_etudiant.insert("", "end", values=values)

    def exporter_vers_excel(self):
        try:
            # Demander la confirmation à l'utilisateur
            confirmation = messagebox.askyesno("Confirmation",
                                               "Voulez-vous exporter la liste des étudiants vers un fichier Excel?")

            # Si l'utilisateur a confirmé
            if confirmation:
                # Récupérer les données de la table
                data = []
                for row in self.table_etat_etudiant.get_children():
                    values = [self.table_etat_etudiant.item(row, 'values')[i] for i in range(6)]
                    data.append(values)

                # Créer un DataFrame pandas avec les données
                df = pd.DataFrame(data, columns=["MAT", "NOM", "PRENOM", "GENRE", "NIVEAU", "PROMOTION"])

                # Vérifier si le dossier existe, sinon le créer
                output_folder = r"C:\Users\MAXIME KPOGHOMOU\Desktop\G.INFOS\listeDesEtudiants"
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)

                # Chemin complet pour le fichier Excel
                default_filepath = os.path.join(output_folder, "etudiants.xlsx")

                # Exporter le DataFrame vers le fichier Excel
                df.to_excel(default_filepath, index=False)

                messagebox.showinfo("Export réussi", "Liste des étudiants exportées vers le fichier Excel avec succès!")
                # Ouvrir le fichier Excel avec l'application par défaut
                os.system(f'start excel "{default_filepath}"')
                self.destroy()
        except Exception as e:
            messagebox.showerror("Erreur d'export", f"Une erreur s'est produite lors de l'exportation : {str(e)}")

if __name__ == "__main__":
    fenetre_etat_etudiant = FenetreEtatEtudiant()
    fenetre_etat_etudiant.mainloop()