import  tkinter as tk
from tkinter import messagebox
from subprocess import call
import mysql.connector
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime
import locale
from time import strftime
import sys
from PIL import Image, ImageTk, ImageDraw
from services import enregistrer_action_utilisateur


#CONFIGURATION DU FUSEAU HORAIRE
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')


# FONCTIOON POUR SE DECONNECTER
def Quitter():
    confirmation = messagebox.askyesno("Confirmation", "Voulez-vous quitter l'application?")
    if confirmation:
        # Utilisation de la fonction pour la déconnexion
        enregistrer_action_utilisateur(received_user_name, "Déconnexion")

        # Affichez un message de déconnexion
        messagebox.showinfo("Déconnexion", "Vous êtes déconnecté.")

        # Fermez la fenêtre principale de l'application
        root.destroy()

# Fonction pour afficher le graphique
def afficher_graphique():
    # Connexion à la base de données
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='gestion_departement'
    )

    # Création d'un curseur pour exécuter des requêtes SQL
    cursor = connection.cursor(dictionary=True)

    # Exécution de la requête SQL pour obtenir le nombre d'élèves par promotion
    query = """
        SELECT id_promotion, COUNT(*) AS nombre_eleves
        FROM etudiants
        GROUP BY id_promotion
    """

    cursor.execute(query)

    # Récupération des résultats
    result = cursor.fetchall()

    # Fermeture du curseur et de la connexion à la base de données
    cursor.close()
    connection.close()

    # Extraction des données pour le graphique
    promotions = [row['id_promotion'] for row in result]
    nombre_eleves = [row['nombre_eleves'] for row in result]

    # Création de la figure Matplotlib
    fig, ax = plt.subplots()
    ax.bar(promotions, nombre_eleves, color='blue')
    ax.set_title('Nombre d\'étudiant par promotion')
    ax.set_xlabel('Promotions')
    ax.set_ylabel('Nombre d\'étudiant')

    # Incorporation de la figure dans Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=500, y=200)  # Ajustez les coordonnées selon vos besoins

def actualiser_fenetre():
    afficher_graphique()

    # Mettez à jour le nombre d'étudiants dans le bloc étudiant
    nombre_enregistrements_etudiants = NombreEnregistrementEtudiant()
    lblNombreEnreg_etudiant.config(text=f"{nombre_enregistrements_etudiants}")

    # Mettez à jour le nombre d'enseignants dans le bloc enseignant
    nombre_enregistrements_enseignants = NombreEnregistrementEnseignant()
    lblNombreEnreg_enseignant.config(text=f"{nombre_enregistrements_enseignants}")

    # Mettez à jour le nombre de promotions dans le bloc promotion
    nombre_enregistrements_promotions = NombreEnregistrementPromotion()
    lblNombreEnreg_promotion.config(text=f"{nombre_enregistrements_promotions}")

def update_time():
    current_time = strftime('%H:%M:%S')
    texte_heure.set(current_time)
    root.after(1000, update_time)  # Répéter après 1000 millisecondes (1 seconde)

def update_date():
    current_date = datetime.now().strftime('%A %d %B %Y')  # Format 'lundi 14 janvier 2024'
    texte_date.set(current_date)
    root.after(60000, update_date) # Répéter après 60000 millisecondes (60 secondes)

# Fonctions pour appeler différentes fenêtres
def Etudiant():
    call(["python", "etudiant.py"])

def Enseignant():
    call(["python", "enseignant.py"])

def Matiere():
    call(["python", "matiere.py"])

def Note():
    call(["python", "note.py"])

def emploi():
    call(["python", "emploie.py"])

def promotion():
    call(["python", "promotion.py"])

def parametre():
    call(["python", "parametre.py"])

def backup():
    call(["python", "backup.py"])

# Fonctions pour obtenir le nombre d'enregistrements
def NombreEnregistrementEtudiant():
    db = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_departement")
    connexion = db.cursor()
    connexion.execute("SELECT COUNT(*) FROM etudiants")
    nombre_enreg = connexion.fetchone()[0]
    connexion.close()
    db.close()
    return nombre_enreg

def NombreEnregistrementEnseignant():
    db = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_departement")
    connexion = db.cursor()
    connexion.execute("SELECT COUNT(*) FROM enseignant")
    nombre_enreg = connexion.fetchone()[0]
    connexion.close()
    db.close()
    return nombre_enreg

def NombreEnregistrementPromotion():
    db = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_departement")
    connexion = db.cursor()
    connexion.execute("SELECT COUNT(*) FROM promotion")
    nombre_enreg = connexion.fetchone()[0]
    connexion.close()
    db.close()
    return nombre_enreg

# Créer la fenêtre principale
root = tk.Tk()
root.title("MENU PRINCIPAL")
root.geometry("1350x700+0+0")
root.resizable(False, False)
root.configure(background="#091821")

lblNombreEnreg_enseignant = None
lblNombreEnreg_etudiant = None
lblNombreEnreg_promotion = None


#BLOC A GAUCHE
lblBlog = tk.Label(root, borderwidth=3, relief=tk.SUNKEN, font=("Arial", 18), background="black", fg="black")
lblBlog.place(x=5, y=14, width=300, height=900)

# NAV BAR
lblNav = tk.Label(root, borderwidth=3, relief=tk.SUNKEN, text="G-INFOS-V.1.0", font=("Arial", 18), background="white", fg="black")
lblNav.place(x=323, y=15, width=1000, height=40)

# Variable pour stocker le texte de l'heure
texte_heure = tk.StringVar()

# Étiquette pour afficher l'heure
etiquette_heure = tk.Label(lblNav, textvariable=texte_heure, font=("Helvetica", 15), fg="black", background="white")
etiquette_heure.place(x=5, y=0, width=180, height=40)

# Variable pour stocker le texte de la date
texte_date = tk.StringVar()

# ETIQUETTE POUR AFFICHER LA DATE
etiquette_date = tk.Label(lblNav, textvariable=texte_date, font=("Helvetica", 15), fg="black", background="white")
etiquette_date.place(x=740, y=0, width=250, height=40)

# Bloc étudiant
lblMatricule = tk.Label(root, borderwidth=3, relief=tk.SUNKEN, font=("Arial", 18), background="white", fg="black")
lblMatricule.place(x=360, y=70, width=250, height=110)
lblMat = tk.Label(root, text="ETUDIANTS", font=("Arial", 18), background="white", fg="black")
lblMat.place(x=410, y=80, width=150, height=40)
canvas_tiret = tk.Canvas(lblMatricule, width=200, height=2, bg="white", highlightthickness=0)
canvas_tiret.place(x=145, y=55, relwidth=1, anchor="center")
canvas_tiret.create_line(0, 1, 200, 1, fill="black", width=2)
lblNombreEnreg_etudiant = tk.Label(root, text="Nombre", font=("Arial", 30), background="white", fg="black")
lblNombreEnreg_etudiant.place(x=410, y=145, width=150, height=30)
nombreEnreg = NombreEnregistrementEtudiant()
lblNombreEnreg_etudiant.config(text=f"{nombreEnreg}")

# Bloc Enseignant
lblenseignant = tk.Label(root, borderwidth=3, relief=tk.SUNKEN, font=("Arial", 18), background="white", fg="black")
lblenseignant.place(x=630, y=70, width=250, height=110)
lblEnsei = tk.Label(root, text="ENSEIGNANTS", font=("Arial", 18), background="white", fg="black")
lblEnsei.place(x=670, y=80, width=180, height=40)
canvas_tiret = tk.Canvas(lblenseignant, width=200, height=2, bg="white", highlightthickness=0)
canvas_tiret.place(x=145, y=55, relwidth=1, anchor="center")
canvas_tiret.create_line(0, 1, 200, 1, fill="black", width=2)
lblNombreEnreg_enseignant = tk.Label(root, text="Nombre", font=("Arial", 30), background="white", fg="black")
lblNombreEnreg_enseignant.place(x=670, y=145, width=150, height=30)
nombreEnreg_enseignant = NombreEnregistrementEnseignant()
lblNombreEnreg_enseignant.config(text=f"{nombreEnreg_enseignant}")

# Bloc PROMOTION
lblMatiere = tk.Label(root, borderwidth=3, relief=tk.SUNKEN, font=("Arial", 18), background="white", fg="black")
lblMatiere.place(x=900, y=70, width=250, height=110)
lblMati = tk.Label(root, text="PROMOTION", font=("Arial", 18), background="white", fg="black")
lblMati.place(x=950, y=80, width=150, height=40)
canvas_tiret = tk.Canvas(lblMatiere, width=200, height=2, bg="white", highlightthickness=0)
canvas_tiret.place(x=145, y=55, relwidth=1, anchor="center")
canvas_tiret.create_line(0, 1, 200, 1, fill="black", width=2)
lblNombreEnreg_promotion = tk.Label(root, text="Nombre", font=("Arial", 30), background="white", fg="black")
lblNombreEnreg_promotion.place(x=950, y=145, width=150, height=30)
nombreEnreg_promotion = NombreEnregistrementPromotion()
lblNombreEnreg_promotion.config(text=f"{nombreEnreg_promotion}")

# Boutons pour appeler différentes fenêtres
btnAfficheEtudiant = tk.Button(root, text="ETUDIANTS", bd=4, font=("Arial", 16), bg="white", fg="black", command=Etudiant)
btnAfficheEtudiant.place(x=55, y=190, width=200)

btnAfficheEnseignant = tk.Button(root, text="ENSEIGNANTS", bd=4, font=("Arial", 16), bg="white", fg="black", command=Enseignant)
btnAfficheEnseignant.place(x=55, y=250, width=200)

btnAfficheMatiere = tk.Button(root, text="MATIERES", bd=4, font=("Arial", 16), bg="white", fg="black", command=Matiere)
btnAfficheMatiere.place(x=55, y=310, width=200)

btnAfficheEmploi = tk.Button(root, text="NOTES", bd=4, font=("Arial", 16), bg="white", fg="black", command=Note)
btnAfficheEmploi.place(x=55, y=370, width=200)

btnAffichePara = tk.Button(root, text="EMPLOIE", bd=4, font=("Arial", 16), bg="white", fg="black", command=emploi)
btnAffichePara.place(x=55, y=430, width=200)

btnAffichePara = tk.Button(root, text="PROMOTION", bd=4, font=("Arial", 16), bg="white", fg="black", command=promotion)
btnAffichePara.place(x=55, y=490, width=200)


btnEnregistrer = tk.Button(root, text="ACTUALISER", bd=4, font=("Arial", 12), bg="#FF4500", fg="white", command=actualiser_fenetre)
btnEnregistrer.place(x=1205, y=70, width=120,height=40)

# Bouton se DECONNECTER
btnDeconnexion = tk.Button(root, text="QUITTER", bd=4, font=("Arial", 12), bg="#B22222", fg="white", command=Quitter)
btnDeconnexion.place(x=1205, y=120, width=120,height=40)

btnAfficheEmploi = tk.Button(root, text="PARAMETRES", bd=4, font=("Arial", 16), bg="white", fg="black", command=parametre)
btnAfficheEmploi.place(x=55, y=550, width=200)

#btnAfficheEmploi = tk.Button(root, text="SAUVEGARDER", bd=4, font=("Arial", 16), bg="white", fg="black", command=backup)
#btnAfficheEmploi.place(x=55, y=600, width=200)

#Nom
#lblIst = tk.Label(root,text="G.INFORMATIQUE", font= ("Arial",15),background= "#091821",fg="white")
#lblIst.place(x=70, y=600, width=200)

# Appeler la fonction pour la première fois pour initialiser l'affichage

#update_time()  # Appel initial
#update_date()  # Appel initial
afficher_graphique()

if len(sys.argv) >= 3:
    received_user_name = sys.argv[1]
    received_user_photo = sys.argv[2]
else:
    print("Usage: python menuprincipal.py <user_name> <user_photo>")
    sys.exit(1)


photo_label = tk.Label(root, background="black",)
photo_label.place(x=60, y=30,width=120,height=120)

# Charger et rendre en cercle la photo de l'utilisateur avec Pillow
try:
    user_image = Image.open(received_user_photo)

    # Ajuster la taille de l'image pour correspondre à la taille du cercle
    circle_size = (120, 120)  # Dimensions du cercle (à ajuster selon vos besoins)
    user_image = user_image.resize(circle_size, Image.LANCZOS)

    circle_image = Image.new("RGBA", circle_size, (0, 0, 0, 255))  # Noir avec une opacité complète

    # Créer un masque circulaire
    mask = Image.new("L", circle_size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, circle_size[0], circle_size[1]), fill=255)

    # Superposer l'image redimensionnée sur le fond transparent en utilisant le masque
    circle_image.paste(user_image, mask=mask)

    user_photo = ImageTk.PhotoImage(circle_image)

    # Créer un label en forme de cercle
    photo_label = tk.Label(root, image=user_photo, background="white", borderwidth=0)
    photo_label.image = user_photo  # Gardez une référence à l'image pour éviter la suppression par le garbage collector
    photo_label.place(x=100, y=30, width=circle_size[0], height=circle_size[1])
except Exception as e:
    print("Erreur lors du chargement de l'image :", e)

# USER NAME
lblUserName = tk.Label(root, borderwidth=3, text=f"{received_user_name}", font=("Arial", 18), background="black", fg="white")
lblUserName.place(x=20, y=150, width=280)

# Lancer la boucle principale de l'application
root.mainloop()
