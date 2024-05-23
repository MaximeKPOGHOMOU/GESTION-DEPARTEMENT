#Les bibliothèques à importer

from subprocess import call
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import mysql.connector

from etatEnseignant import FenetreEtatEnseignant


#FONCTION RETOUR
def Retour():
    root.destroy()
    #call(["python", "menuprincipal.py"])


# Ajouter cette fonction pour rafraîchir la table après la modification
def refresh_table():
    # Effacer toutes les lignes de la table
    for item in table.get_children():
        table.delete(item)
    # Reconnecter à la base de données
    db = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_departement")
    connexion = db.cursor()

    # Exécuter la requête pour récupérer les données mises à jour
    connexion.execute("SELECT matricule, nom, prenom, telephone, adresse FROM enseignant")

    # Ajouter les nouvelles données à la table
    for row in connexion:
        table.insert('', END, values=row)
    # Fermer la connexion à la base de données
    db.close()


def recuperer_et_afficher():
    # Récupérer les données de la table de la fenêtre etudiant
    data_enseignant = []
    for row in table.get_children():
        values = [table.item(row, 'values')[i] for i in range(5)]
        data_enseignant.append(values)

    # Afficher les données dans la fenêtre etatEnseignant
    fenetre_etat_etudiant = FenetreEtatEnseignant(data_enseignant)

#Fonction ajouter
def Ajouter():
    matricule = txtMatricule.get()
    nom = txtNom.get()
    prenom = txtPrenom.get()
    telephone = txtTelephone.get()
    adresse = txtAdresse.get()
    db = mysql.connector.connect(host="localhost", user= "root",password="",database="gestion_departement")
    connexion = db.cursor()
    try:
        if(matricule == "" ):
            messagebox.showerror("","Saisir le matricule!!")
        elif(nom == ""):
            messagebox.showerror("","Saisir le nom!!")
        elif(prenom == ""):
            messagebox.showerror("","Saisir le prenom!!")
        elif(telephone == ""):
            messagebox.showerror("","Saisir le numéro de téléphone!!")
        elif(adresse == ""):
            messagebox.showerror("","Saisir l'adresse!!")
        else:
            sql= "INSERT INTO enseignant (matricule,nom,prenom,telephone,adresse) VALUES (%s, %s, %s, %s,%s)"
            val= (matricule, nom, prenom, telephone, adresse)
            connexion.execute(sql,val)
            db.commit()
            dernierMatricule = connexion.lastrowid
            messagebox.showinfo("Information","Enregistrement éffectué avec succès")
            refresh_table()
            txtAdresse.delete("0", "end")
            txtMatricule.delete("0", "end")
            txtTelephone.delete("0", "end")
            txtPrenom.delete("0", "end")
            txtNom.delete("0", "end")
            #root.destroy()
            #call(["python", "enseignant.py"])
    except Exception as e:
        print(e)
        #retour
        db.rollback()
        db.close()

#Fonction Modifier
def Modifier():
    matricule = txtMatricule.get()
    nom = txtNom.get()
    prenom = txtPrenom.get()
    telephone = txtTelephone.get()
    adresse = txtAdresse.get()
    db = mysql.connector.connect(host="localhost", user= "root",password="",database="gestion_departement")
    connexion = db.cursor()
    try:
        if(matricule == "" ):
            messagebox.showerror("","Saisir le matricule!!")
        elif(nom == ""):
            messagebox.showerror("","Saisir le nom!!")
        elif(prenom == ""):
            messagebox.showerror("","Saisir le prenom!!")
        elif(telephone ==""):
            messagebox.showerror("","Saisir le numéro de téléphone!!")
        elif(adresse == ""):
            messagebox.showerror("","Saisir l'adresse!!")
        else:
            sql= "UPDATE enseignant SET nom=%s, prenom=%s, telephone=%s, adresse=%s WHERE matricule=%s"
            val= (nom, prenom, telephone,adresse, matricule)
            connexion.execute(sql,val)
            db.commit()
            dernierMatricule = connexion.lastrowid
            messagebox.showinfo("Information","Modification éffectuée avec succès")
            refresh_table()
            txtAdresse.delete("0", "end")
            txtMatricule.delete("0", "end")
            txtTelephone.delete("0", "end")
            txtPrenom.delete("0", "end")
            txtNom.delete("0", "end")
            #root.destroy()
            #call(["python", "enseignant.py"])
    except Exception as e:
        print(e)
        #retour
        db.rollback()
        db.close()

#Fonction Supprimer
def Supprimer():
    selection = table.selection()
    if selection:
        matricule_a_supprimer = table.item(selection[0])['values'][0]
        try:
            db = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_departement")
            connexion = db.cursor()           
            sql = "DELETE FROM enseignant WHERE matricule=%s"
            val = (matricule_a_supprimer,)
            connexion.execute(sql, val)
            db.commit()
            messagebox.showinfo("Information", "Suppression effectuée avec succès")
            txtAdresse.delete("0", "end") 
            txtMatricule.delete("0", "end") 
            txtTelephone.delete("0", "end")
            txtPrenom.delete("0", "end") 
            txtNom.delete("0", "end")  
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
root.title("GESTION DES ENSEIGNANTS")
root.geometry("1350x700+0+0")
root.resizable(False,False)
root.configure(background="#091821")

lbltitre = Label(root, borderwidth = 3, relief=SUNKEN, text="GESTION DES ENSEIGNANTS",font= ("Sans Serif",25),background="#2F4F4F", fg="#FFFAFA")
lbltitre.place(x=0, y=0, width=1350, height=80)

#Matricule
lblMatricule = Label(root,text="MATRICULE :", font= ("Arial",18),background= "#091821",fg="white")
lblMatricule.place(x=70, y=150, width=150)
txtMatricule = Entry(root, bd=4, font=("Arial", 14))
txtMatricule.place(x=250, y=150, width=150)

#Rechercher
lblRechercher = Label(root,text="RECHERCHER:", font= ("Arial",18),background= "#091821",fg="white")
lblRechercher.place(x=520, y=150, width=250)
txtRechercher = Entry(root, bd=4,font=("Arial",14))
txtRechercher.place(x=750, y=150, width=230)

#Nom
lblNom = Label(root, text="NOM :", font=("Arial", 18), background="#091821", fg="white")
lblNom.place(x=70, y=200, width=150)
txtNom = Entry(root, bd=4, font=("Arial",14))
txtNom.place(x=250, y=200, width=300)

#Prenom
lblPrenom = Label(root,text="PRENOM :", font= ("Arial",18),background= "#091821",fg="white")
lblPrenom.place(x=70, y=250, width=150)
txtPrenom = Entry(root,bd=4,font=("Arial",14))
txtPrenom.place(x=250,y=250,width=300)

#Telephone
lblTelehone = Label(root, text="TELEPONE :", font=("Arial", 18), background="#091821", fg="white")
lblTelehone.place(x=70, y=300, width=150)
txtTelephone = Entry(root, bd=4, font=("Arial", 14))
txtTelephone.place(x=250, y=300, width=300)
#Adresse
lblAdresse = Label(root, text="ADRESSE :", font=("Arial", 18), background="#091821", fg="white")
lblAdresse.place(x=70, y=350, width=150)
txtAdresse = Entry(root, bd=4, font=("Arial", 14))
txtAdresse.place(x=250, y=350, width=300)

#Bouton enregistrer
btnEnregistrer = Button(root, text="ENREGISTRER", bd=4, font=("Arial", 12), bg="#FF4500", fg="white", command=Ajouter)
btnEnregistrer.place(x=250, y=400, width=150)

#Bouton Modifier
btnModifier = Button(root, text="MODIFIER", bd=4, font=("Arial", 12),bg="#FF4500", fg="white", command=Modifier)
btnModifier.place(x=250, y=440, width=150)

#Bouton Supprimer
btnSupprimer = Button(root, text="SUPPRIMER", bd=4, font=("Arial", 12), bg="#FF4500", fg="white", command=Supprimer)
btnSupprimer.place(x=250, y=480, width=150)

#btnEnregistrer = tk.Button(root, text="ACTUALISER", bd=4, font=("Arial", 12), bg="#FF4500", fg="white", command="actualiser_fenetre")
#btnEnregistrer.place(x=1000, y=150, width=120)

#IMPRIMER
btnAfficher = Button(root, text="IMPRESSION", bd=4, font=("Arial", 12), bg="#FF4500", fg="white", command=recuperer_et_afficher)
btnAfficher.place(x=1000, y=150, width=150)

#Bouton Retour
btnRetour = Button(root, text="RETOUR", bd=4, font=("Arial", 12), bg="#B22222", fg="white", command=Retour)
btnRetour.place(x=1220, y=150, width=120)


#Creation de la Table
table = ttk.Treeview(root, columns=(1, 2, 3, 4, 5), height=5, show="headings")
table.place(x=560, y=200, width=780, height=450)


#Entetes
table.heading(1, text="MAT")
table.heading(2, text="NOM")
table.heading(3, text="PRENOM")
table.heading(4, text="TELEPHONE")
table.heading(5, text="ADRESSE")

#Définir les dimensions des colones
table.column(1, width=20)
table.column(2, width=100)
table.column(3, width=150)
table.column(4, width=50)
table.column(5, width=100)

#Connexion au serveur 
db = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_departement")
connexion = db.cursor()
connexion.execute("select * from enseignant")
for row in connexion:
    table.insert('', END, values=row)
db.close()

# Fonction appelée lorsqu'un élément est sélectionné dans le tableau
def on_select(event):
    selection = table.selection()
    if selection:
        item = table.item(selection[0])
        values = item['values']
        txtMatricule.delete(0, END)
        txtMatricule.insert(0, values[0]) 
        txtNom.delete(0, END)
        txtNom.insert(0, values[1])
        txtPrenom.delete(0, END)
        txtPrenom.insert(0, values[2])
        txtTelephone.delete(0,END)
        txtTelephone.insert(0,values[3])
        txtAdresse.delete(0,END)
        txtAdresse.insert(0,values[4])

# Associer la fonction à l'événement de sélection
table.bind('<ButtonRelease-1>', on_select)

#La fonction rechercher
def RechercherInstantanee():
    # Effacer le tableau avant d'afficher les résultats de la recherche
    for item in table.get_children():
        table.delete(item)
    recherche_termes = txtRechercher.get()
    try:
        db = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_departement")
        connexion = db.cursor()
        sql = "SELECT * FROM enseignant WHERE matricule LIKE %s OR nom LIKE %s OR prenom LIKE %s "
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
    root.after(500, RechercherInstantanee)
# Associer la fonction à l'événement de frappe de l'utilisateur
txtRechercher.bind('<KeyRelease>', recherche_instantanee_callback)
 
 
 
    
    
 
#Execution
root.mainloop()