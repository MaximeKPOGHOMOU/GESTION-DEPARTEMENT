
from subprocess import call
from tkinter import ttk, Tk
from tkinter import *
from tkinter import messagebox
import mysql.connector
from passlib.hash import sha256_crypt
from tkinter import filedialog
import shutil


#FONCTION RETOUR
def Retour():
    root.destroy()
    call(["python", "parametre.py"])

def enregistrer_photo():
    photoEntrer.config(text="Aucune image sélectionner")


# fonction pour rafraîchir la table après la modification
def refresh_table():
    # Effacer toutes les lignes de la table
    for item in table.get_children():
        table.delete(item)
    # Reconnecter à la base de données
    db = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_departement")
    connexion = db.cursor()

    # Exécuter la requête pour récupérer les données mises à jour
    connexion.execute("SELECT idUser, userName, telephone, email FROM utilisateur")

    # Ajouter les nouvelles données à la table
    for row in connexion:
        table.insert('', END, values=row)
    # Fermer la connexion à la base de données
    db.close()


# Fonction pour hacher le mot de passe
def hash_password(password):
    return sha256_crypt.using(rounds=1000).hash(password)


# Fonction pour vérifier si l'e-mail existe déjà dans la base de données
def email_exists(email):
    db = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_departement")
    connexion = db.cursor()

    try:
        sql = "SELECT COUNT(*) FROM utilisateur WHERE email = %s"
        val = (email,)
        connexion.execute(sql, val)
        result = connexion.fetchone()

        # Si le résultat est différent de zéro, cela signifie que l'e-mail existe déjà
        return result[0] != 0
    except Exception as e:
        print(e)
    finally:
        connexion.close()
        db.close()

# Déclarer imageName comme une variable globale
imageName = None


# Fonction pour parcourir et stocker l'image dans le dossier du projet
def Parcourir():
    global imageName
    imG = filedialog.askopenfilename(initialdir="/", title="Sélectionner une image",
                                     filetypes=(("fichiers PNG", "*.png"), ("fichiers JPG", "*.jpg")))
    if imG:
        imageName = imG
        # Copier l'image sélectionnée dans le dossier du projet
        destination = "./images/"  # Remplacez par le chemin réel de votre dossier de projet
        shutil.copy(imageName, destination)
        # Mettre à jour le chemin affiché dans votre interface utilisateur
        photoEntrer.configure(text=".../images/" + imageName.split("/")[-1])


# Fonction pour ajouter un nouvel utilisateur
def Ajouter():
    matricule = txtMatricule.get()
    name = txtName.get()
    email = txtEmail.get()
    telephone = txttelephone.get()
    password = txtPassword.get()

    # Hacher le mot de passe avant de l'ajouter à la base de données
    hashed_password = hash_password(password)

    # Vérifier si l'e-mail existe déjà dans la base de données
    if email_exists(email):
        messagebox.showerror("", "Cet e-mail est déjà utilisé. Veuillez utiliser une autre adresse e-mail.")
        return
    # Continuer avec l'ajout de l'utilisateur si l'e-mail n'existe pas encore
    db = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_departement")
    connexion = db.cursor()
    try:
        if matricule == "" or name == "" or email == "" or password == "" or telephone == "":
            messagebox.showerror("", "Veuillez remplir tous les champs!")
        else:
            # Mettre à jour la requête SQL pour stocker le chemin de l'image
            sql = "INSERT INTO utilisateur (idUser, userName, telephone, pwd, email, photo) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (matricule, name, telephone, hashed_password, email, "images/" + imageName.split("/")[-1])
            connexion.execute(sql, val)
            db.commit()
            dernierMatricule = connexion.lastrowid
            messagebox.showinfo("Information", "Enregistrement effectué avec succès")
            refresh_table()
            txtEmail.delete("0", "end")
            txtMatricule.delete("0", "end")
            txtName.delete("0", "end")
            txtPassword.delete("0", "end")
            txttelephone.delete("0", "end")
            enregistrer_photo()
            #root.destroy()
            #call(["python", "user.py"])
    except Exception as e:
        print(e)
        # Retour en cas d'erreur
        db.rollback()
    finally:
        connexion.close()
        db.close()

#Fonction Modifier
def Modifier():
    global imageName  # Declare imageName as a global variable
    matricule = txtMatricule.get()
    name = txtName.get()
    email = txtEmail.get()
    telephone = txttelephone.get()
    passwrod = txtPassword.get()

    # Hacher le mot de passe avant de l'enregistrer dans la base de données
    hashed_password = hash_password(passwrod)

    # Assurez-vous que vous avez une photo mise en place
    photo = imageName if imageName else photoEntrer.cget("text")

    # Connexion à la base de données
    db = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_departement")
    connexion = db.cursor()

    try:
        if matricule == "" or name == "" or email == "" or telephone == "":
            messagebox.showerror("", "Veuillez remplir tous les champs!")
        else:
            # Requête de mise à jour
            sql = "UPDATE utilisateur SET userName=%s, telephone=%s, email=%s, photo=%s WHERE idUser=%s"
            val = (name, telephone, email, photo, matricule)
            # Exécution de la requête
            connexion.execute(sql, val)
            # Commit des changements dans la base de données
            db.commit()
            messagebox.showinfo("Information", "Modification effectuée avec succès")
            txtEmail.delete("0", "end")
            txtMatricule.delete("0", "end")
            txtName.delete("0", "end")
            txtPassword.delete("0", "end")
            txttelephone.delete("0", "end")
            refresh_table()
            enregistrer_photo()
            #root.destroy()
            #call(["python", "user.py"])
            # Fermeture de la connexion à la base de données
            db.close()

            # Rafraîchir la table avec les nouvelles données
            #refresh_table()
    except Exception as e:
        print(e)
        messagebox.showerror("Erreur", "Une erreur s'est produite lors de la modification!")

#Fonction Supprimer
def Supprimer():
    selection = table.selection()
    if selection:
        matricule_a_supprimer = table.item(selection[0])['values'][0]
        try:
            db = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_departement")
            connexion = db.cursor()
            sql = "DELETE FROM utilisateur WHERE idUser=%s"
            val = (matricule_a_supprimer,)
            connexion.execute(sql, val)
            db.commit()
            messagebox.showinfo("Information", "Suppression effectuée avec succès")
            txtEmail.delete("0", "end")
            txtMatricule.delete("0", "end")
            txtName.delete("0", "end")
            txtPassword.delete("0", "end")
            txttelephone.delete("0", "end")
            enregistrer_photo()
            # Mise à jour du tableau après la suppression
            table.delete(selection)
        except Exception as e:
            print(e)
            # Retour en cas d'erreur
            db.rollback()
        finally:
            db.close()


#Creation de la fenetre de connexion
root = Tk()
root.title("GESTION DES UTILISATEURS")
root.geometry("1350x700+0+0")
root.resizable(False,False)
root.configure(background="#091821")

#Titre
lbltitre = Label(root, borderwidth = 3, relief = SUNKEN ,text="GESTION DES UTILISATEURS",font= ("Sans Serif",25),background= "#2F4F4F",fg= "#FFFAFA")
lbltitre.place(x = 0, y = 0, width= 1350, height=100)

#Matricule
lblMatricule = Label(root,text="MATRICULE:", font= ("Arial",18),background= "#091821",fg="white")
lblMatricule.place(x=20, y=150, width=230)
txtMatricule = Entry(root,bd=4,font=("Arial",14))
txtMatricule.place(x=270,y=150,width=200)

#Matricule
lblName = Label(root,text="NOM UTILISATEUR:", font= ("Arial",18),background= "#091821",fg="white")
lblName.place(x=20, y=200, width=230)
txtName = Entry(root,bd=4,font=("Arial",14))
txtName.place(x=270,y=200,width=200)

#Matricule
lblpassWord = Label(root,text="MOT DE PASSE:", font= ("Arial",18),background= "#091821",fg="white")
lblpassWord.place(x=40, y=250, width=230)
txtPassword = Entry(root,show="*",bd=4,font=("Arial",14))
txtPassword.place(x=270,y=250,width=200)

#Matricule
lbltelephone = Label(root,text="TELEPHONE:", font= ("Arial",18),background= "#091821",fg="white")
lbltelephone.place(x=40, y=300, width=230)
txttelephone = Entry(root,bd=4,font=("Arial",14))
txttelephone.place(x=270,y=300,width=200)

#Nom
lblemail= Label(root,text="EMAIL :", font= ("Arial",18),background= "#091821",fg="white")
lblemail.place(x=40, y=350, width=200)
txtEmail = Entry(root,bd=4,font=("Arial",14))
txtEmail.place(x=270,y=350,width=300)

#Matricule
lblPhoto= Label(root,text="PHOTO:", font= ("Arial",18),background= "#091821",fg="white")
lblPhoto.place(x=40, y=400, width=230)
photoEntrer = Label(root,text="Aucune image sélectionner",font= ("Arial",13))
photoEntrer.place(x=270,y=400,width=210)

#Bouton parcourir
btnParcourir = Button(root,text="Parcourir",bd=4,font=("Arial",8),bg="#FF4500",fg="white",command=Parcourir)
btnParcourir.place(x=490,y=400,width=80)

#Bouton enregistrer
btnEnregistrer = Button(root,text="ENREGISTRER",bd=4,font=("Arial",12),bg="#FF4500",fg="white",command=Ajouter)
btnEnregistrer.place(x=270,y=450,width=150)

#Bouton Modifier
btnModifier = Button(root,text="MODIFIER",bd=4,font=("Arial",12),bg="#FF4500",fg="white",command=Modifier)
btnModifier.place(x=270,y=490,width=150)

#Bouton Supprimer
btnSupprimer = Button(root, text="SUPPRIMER", bd=4, font=("Arial", 12), bg="#FF4500", fg="white", command=Supprimer)
btnSupprimer.place(x=270, y=530, width=150)

#Bouton Retour
btnRetour = Button(root, text="RETOUR", bd=4, font=("Arial", 12), bg="#B22222", fg="white", command=Retour)
btnRetour.place(x=1200, y=150, width=120)


#Rechercher
lblRechercher = Label(root,text="RECHERCHER:", font= ("Arial",18),background= "#091821",fg="white")
lblRechercher.place(x=580, y=150, width=250)
txtRechercher = Entry(root,bd=4,font=("Arial",14))
txtRechercher.place(x=800,y=150,width=200)


#Creation de la Table
table = ttk.Treeview(root,columns=(1, 2, 3, 4, 5),height=5,show="headings")
table.place(x=620,y=200,width=700,height=450)

#Entetes
table.heading(1, text="MATRICULE")
table.heading(2, text="NOM UTILISATEUR")
table.heading(3, text="TELEPHONE")
table.heading(4, text="EMAIL")


#Définir les dimensions des colones
table.column(1,width=100)
table.column(2,width=200)
table.column(3,width=150)
table.column(4,width=300)

#Connexion au serveur
db = mysql.connector.connect(host="localhost",user="root",password="",database="gestion_departement")
connexion= db.cursor()
connexion.execute("select idUser, userName, telephone, email from utilisateur")
for row in connexion:
    table.insert('',END, values=row)
db.close()

# Fonction appelée lorsqu'un élément est sélectionné dans le tableau
def on_select(event):
    selection = table.selection()
    if selection:
        item = table.item(selection[0])
        user_id = item['values'][0]  # Suppose que la première colonne est l'ID de l'utilisateur
        retrieve_user_data(user_id)

# Fonction pour récupérer les données de l'utilisateur à partir de la base de données
def retrieve_user_data(user_id):
    # Connexion à la base de données
    db = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_departement")
    cursor = db.cursor()

    # Exécuter la requête pour récupérer les données de l'utilisateur
    query = "SELECT * FROM utilisateur WHERE idUser = %s"
    cursor.execute(query, (user_id,))
    user_data = cursor.fetchone()

    # Fermer la connexion à la base de données
    db.close()

    # Mettre à jour les champs d'entrée avec les données récupérées
    if user_data:
        txtMatricule.delete(0, END)
        txtMatricule.insert(0, user_data[0])
        txtName.delete(0, END)
        txtName.insert(0, user_data[1])
        txttelephone.delete(0, END)
        txttelephone.insert(0, user_data[2])
        #txtPassword.delete(0, END)
        #txtPassword.insert(0, user_data[3])
        txtEmail.delete(0, END)
        txtEmail.insert(0, user_data[4])
        photoEntrer.configure(text=user_data[5])
        # La colonne 'photo' contient l'emplacement de la photo dans votre cas
        # Vous pouvez mettre à jour votre logique pour traiter la photo en conséquence
        # photoEntrer.configure(text=user_data[5]) ou autre traitement pour les photos
# Associer la fonction à l'événement de sélection
table.bind('<ButtonRelease-1>', on_select)

# La fonction rechercher
def RechercherInstantanee():
    # Effacer le tableau avant d'afficher les résultats de la recherche
    for item in table.get_children():
        table.delete(item)

    recherche_termes = txtRechercher.get()

    try:
        db = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_departement")
        connexion = db.cursor()
        sql = "SELECT idUser, userName, telephone, email FROM utilisateur WHERE userName LIKE %s OR telephone LIKE %s OR email LIKE %s"
        val = ('%' + recherche_termes + '%', '%' + recherche_termes + '%', '%' + recherche_termes + '%')
        connexion.execute(sql, val)
        resultats = connexion.fetchall()

        for row in resultats:
            table.insert('', END, values=row)
    except Exception as e:
        print(e)
    finally:
        db.close()

# Fonction pour déclencher la recherche instantanée après un délai
def recherche_instantanee_callback(event):
    root.after(200, RechercherInstantanee)

# Associer la fonction à l'événement de frappe de l'utilisateur
txtRechercher.bind('<KeyRelease>', recherche_instantanee_callback)



#Execution
root.mainloop()