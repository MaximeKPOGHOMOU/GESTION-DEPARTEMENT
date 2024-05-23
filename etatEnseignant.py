import tkinter as tk
from tkinter import ttk, Label, Button, SUNKEN, messagebox
import pandas as pd
import os

class FenetreEtatEnseignant(tk.Tk):
    def __init__(self, donnees):
        super().__init__()

        self.title("IMPRESSION DES DONNEES")
        self.geometry("1000x600+155+70")
        self.resizable(False, False)
        self.configure(background="white")

        self.lbltitre = Label(self, borderwidth=3, relief=SUNKEN, text="LA LISTE DES ENSEIGNANTS", font=("Sans Serif", 25),
                              background="#2F4F4F", fg="#FFFAFA")
        self.lbltitre.place(x=0, y=0, width=1000, height=80)

        self.table_etat_enseignant = ttk.Treeview(self, columns=(1, 2, 3, 4, 5), height=5, show="headings")
        self.table_etat_enseignant.place(x=55, y=90, width=890, height=450)

        self.table_etat_enseignant.heading(1, text="MAT")
        self.table_etat_enseignant.heading(2, text="NOM")
        self.table_etat_enseignant.heading(3, text="PRENOM")
        self.table_etat_enseignant.heading(4, text="TELEPHONE")
        self.table_etat_enseignant.heading(5, text="ADRESSE")

        self.table_etat_enseignant.column(1, width=70)
        self.table_etat_enseignant.column(2, width=150)
        self.table_etat_enseignant.column(3, width=300)
        self.table_etat_enseignant.column(4, width=150)
        self.table_etat_enseignant.column(5, width=150)

        self.btnAfficher = Button(self, text="EXPORTER", bd=4, font=("Arial", 16), bg="#FF4500", fg="white",
                                  command=self.exporter_vers_excel)
        self.btnAfficher.place(x=400, y=550, width=200)

        # Afficher les données reçues en argument
        self.afficher_donnees(donnees)

    def afficher_donnees(self, donnees):
        for values in donnees:
            self.table_etat_enseignant.insert("", "end", values=values)

    def exporter_vers_excel(self):
        try:
            # Demander la confirmation à l'utilisateur
            confirmation = messagebox.askyesno("Confirmation",
                                               "Voulez-vous exporter la liste des enseignants vers un fichier Excel?")

            # Si l'utilisateur a confirmé
            if confirmation:
                # Récupérer les données de la table
                data = []
                for row in self.table_etat_enseignant.get_children():
                    values = [self.table_etat_enseignant.item(row, 'values')[i] for i in range(5)]
                    data.append(values)

                # Créer un DataFrame pandas avec les données
                df = pd.DataFrame(data, columns=["MAT", "NOM", "PRENOM", "TELEPHONE", "ADRSSE"])

                # Vérifier si le dossier existe, sinon le créer
                output_folder = r"C:\Users\MAXIME KPOGHOMOU\Desktop\G.INFOS\listeDesEnseignants"
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)

                # Chemin complet pour le fichier Excel
                default_filepath = os.path.join(output_folder, "enseignants.xlsx")

                # Exporter le DataFrame vers le fichier Excel
                df.to_excel(default_filepath, index=False)

                messagebox.showinfo("Export réussi", "Liste des enseignants exportées vers le fichier Excel avec succès!")
                # Ouvrir le fichier Excel avec l'application par défaut
                os.system(f'start excel "{default_filepath}"')
                self.destroy()
        except Exception as e:
            messagebox.showerror("Erreur d'export", f"Une erreur s'est produite lors de l'exportation : {str(e)}")
        self.destroy()

if __name__ == "__main__":

    fenetre_etat_enseignant = FenetreEtatEnseignant()
    fenetre_etat_enseignant.mainloop()