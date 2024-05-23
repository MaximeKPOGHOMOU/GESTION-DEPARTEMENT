from tkinter import ttk, Tk
from tkinter import *
from tkinter import messagebox
import mysql.connector
from subprocess import call

#FONCTION RETOUR
def Retour():
    root.destroy()
    call(["python", "parametre.py"])

# Fonction pour récupérer les données de la table historique_connexion
def charger_historique_connexion():
    # Connexion à la base de données
    connexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gestion_departement"
    )

    # Création d'un curseur
    cursor = connexion.cursor()

    # Exécution de la requête SQL pour récupérer les données
    query = "SELECT idUser, date, heure, action FROM historique_connexion"
    cursor.execute(query)

    # Récupération des résultats
    resultats = cursor.fetchall()

    # Fermeture du curseur et de la connexion
    cursor.close()
    connexion.close()

    return resultats

# Création de la fenêtre Tkinter
root = Tk()
root.title("GESTION DES ENSEIGNANTS")
root.geometry("1350x700+0+0")
root.resizable(False, False)
root.configure(background="#091821")

#Rechercher
lblRechercher = Label(root, text="RECHERCHER", font=("Arial", 18), background="#091821", fg="white")
lblRechercher.place(x=320, y=130, width=180)
txtRechercher = Entry(root, bd=4, font=("Arial", 14))
txtRechercher.place(x=530, y=130, width=250)


#Bouton Retour
btnRetour = Button(root, text="RETOUR", bd=4, font=("Arial", 12), bg="#B22222", fg="white", command=Retour)
btnRetour.place(x=1150, y=180, width=100)
# Titre
lbltitre = Label(root, borderwidth=3, relief=SUNKEN, text="HISTORIQUE DE LA CONNEXION DES UTILISATEURS", font=("Sans Serif", 25), background="#2F4F4F", fg="#FFFAFA")
lbltitre.place(x=0, y=0, width=1350, height=80)

# Création de la Table
table = ttk.Treeview(root, columns=(1, 2, 3, 4), height=5, show="headings")
table.place(x=320, y=180, width=780, height=500)

# Entêtes
table.heading(1, text="NOM UTILISATEUR")
table.heading(2, text="DATE DE CONNEXION")
table.heading(3, text="HEURE DE CONNEXION")
table.heading(4, text="ACTION EFFECTUEE")

# Définir les dimensions des colonnes
table.column(1, width=200)
table.column(2, width=150)
table.column(3, width=100)
table.column(4, width=100)

# Charger les données depuis la base de données
donnees_historique = charger_historique_connexion()

# Remplir la table avec les données
for donnee in donnees_historique:
    table.insert('', 'end', values=donnee)

# Démarrer la boucle principale Tkinter
root.mainloop()