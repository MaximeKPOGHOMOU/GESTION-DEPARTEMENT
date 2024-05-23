
from tkinter import *
from tkinter import messagebox
import mysql.connector
from passlib.hash import sha256_crypt
import subprocess
from services import enregistrer_action_utilisateur

# Fonction pour hacher le mot de passe
def hash_password(password):
    hashed_password = sha256_crypt.using(rounds=1000).hash(password)
    return hashed_password

#VERIFICATION DU MOT DE PASSE
def verify_password(entered_password, stored_password_hash):
    return sha256_crypt.verify(entered_password, stored_password_hash)

# DECLARATION DES VARIABLES GLOBALES
global_user_name = ""
global_user_photo = ""

# Fonction pour se connecter

def Seconnecter():
    global global_user_name
    global global_user_photo

    userName = txtNomUtilisateur.get()
    password = txtmdp.get()

    db = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_departement")
    connexion = db.cursor()
    if userName == "":
        messagebox.showerror("", "Entrer le nom d'utilisateur")
        txtNomUtilisateur.delete("0", "end")
    elif password == "":
        messagebox.showerror("", "Entrer le mot de passe")
        txtmdp.delete("0", "end")
    else:
        try:
            # Récupérer le mot de passe haché et les informations de l'utilisateur
            connexion.execute("SELECT pwd, userName, photo FROM utilisateur WHERE userName=%s", (userName,))
            result = connexion.fetchone()
            if result:
                stored_password_hash, user_name, user_photo = result
                # Vérifier les deux hachages
                if verify_password(password, stored_password_hash):
                    txtmdp.delete("0", "end")
                    txtNomUtilisateur.delete("0", "end")
                    # STOCKER LES INFORMATIONS DE CONNEXION DANS LES VARIABLE GLOBALES
                    global_user_name = user_name
                    global_user_photo = user_photo
                    enregistrer_action_utilisateur(global_user_name, "Connexion")
                    root.destroy()
                    subprocess.run(["python", "menuprincipal.py", str(user_name), str(user_photo)])
                else:
                    messagebox.showerror("Authentification échouée", "Nom utilisateur ou mot de passe incorrect!!")
                    txtmdp.delete("0", "end")
            else:
                messagebox.showerror("Authentification échouée", "Nom utilisateur ou mot de passe incorrect!!")
                txtmdp.delete("0", "end")
        except Exception as e:
            print(e)
        finally:
            connexion.close()
            db.close()

# FONCTIOON POUR SE DECONNECTER
def Quitter():
    confirmation = messagebox.askyesno("Confirmation", "Voulez-vous quitter l'application?")
    if confirmation:
        root.destroy()

# CREATION DE LA FENETRE  PRINCIPALE
root = Tk()
root.title("AUTHENTIFICATION")
root.geometry("400x300+450+200")
root.resizable(False, False)
root.configure(background="#091821")

# TITRE
lbltitre = Label(root, borderwidth=3, relief=SUNKEN, text="Formulaire de connexion", font=("Sans Serif", 25), background="#2F4F4F", fg="white")
lbltitre.place(x=0, y=0, width=400)

# NOM UTILISATEUR
lblNomUtilisateur = Label(root, text="User name", font=("Arial", 16), background="#091821", fg="white")
lblNomUtilisateur.place(x=20, y=100, width=150)
txtNomUtilisateur = Entry(root, bd=4, font=("Arial", 13))
txtNomUtilisateur.place(x=170, y=100, width=200, height=30)

# MOT DE PASSE
lblmdp = Label(root, text="Password", font=("Arial", 16), background="#091821", fg="white")
lblmdp.place(x=20, y=150, width=150)
txtmdp = Entry(root, show="*", bd=4, font=("Arial", 13))
txtmdp.place(x=170, y=150, width=200, height=30)

# Bouton se connecter
btnConnexion = Button(root, text="CONNEXION", bd=4, font=("Arial", 16), bg="#FF4500", fg="white", command=Seconnecter)
btnConnexion.place(x=40, y=200, width=150)

# Bouton se DECONNECTER
btnConnexion = Button(root, text="QUITTER", bd=4, font=("Arial", 16), bg="#B22222", fg="white", command=Quitter)
btnConnexion.place(x=220, y=200, width=150)

# Execution
root.mainloop()