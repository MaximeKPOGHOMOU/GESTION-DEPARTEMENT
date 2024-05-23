#Les bibliothèques à importer
import tkinter
from cProfile import label
from subprocess import call
from tkinter import ttk, Tk
from tkinter import *
from tkinter import messagebox
import mysql.connector


# Ajouter cette fonction pour rafraîchir la table après la modification
def refresh_table():
    # Effacer toutes les lignes de la table
    for item in table.get_children():
        table.delete(item)
    # Reconnecter à la base de données
    db = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_departement")
    connexion = db.cursor()
    # Exécuter la requête pour récupérer les données mises à jour
    connexion.execute("SELECT code_eva,matricule,code_mat,moyenne FROM evaluer")

    # Ajouter les nouvelles données à la table
    for row in connexion:
        table.insert('', END, values=row)
    # Fermer la connexion à la base de données
    db.close()

#FONCTION RETOUR
def Retour():
    root.destroy()
    #call(["python", "menuprincipal.py"])

#Fonction ajouter
def Ajouter():
    code = txtCode.get()
    etudiant = comboEtudiant.get()
    matiere = comboMatiere.get()
    moyenne = txtMoyenne.get()
    db = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_departement")
    connexion = db.cursor()
    try:
        if(code == "" ):
            messagebox.showerror("","Saisir le matricule!!")
        elif(etudiant == ""):
            messagebox.showerror("","Saisir le nom!!")
        elif(matiere == ""):
            messagebox.showerror("","Saisir le prenom!!")
        else:
            sql= "INSERT INTO evaluer(code_eva,matricule,code_mat,moyenne) VALUES (%s, %s, %s, %s)"
            val= (code, etudiant, matiere, moyenne)
            connexion.execute(sql,val)
            db.commit()
            dernierMatricule = connexion.lastrowid
            messagebox.showinfo("Information","Enregistrement éffectué avec succès")
            refresh_table()
    except Exception as e:
        print(e)
        #retour
        db.rollback()
        db.close()
        
        
#Fonction Modifier
def Modifier():
    code = txtCode.get()
    etudiant = comboEtudiant.get()
    matiere = comboMatiere.get()
    moyenne = txtMoyenne.get()
    db = mysql.connector.connect(host="localhost", user= "root",password="",database="gestion_departement")
    connexion = db.cursor()
    try:
        if(code == "" ):
            messagebox.showerror("","Saisir le matricule!!")
        if(etudiant == ""):
            messagebox.showerror("","Saisir le nom!!")
        elif(matiere == ""):
            messagebox.showerror("","Saisir le prenom!!")
        elif(moyenne == ""):
            messagebox.showerror("","Saisir le prenom!!")
        else:
            sql= "UPDATE evaluer SET matricule=%s, code_mat=%s, moyenne=%s WHERE code_eva=%s"
            val= (etudiant, matiere, moyenne,code)
            connexion.execute(sql,val)
            db.commit()
            dernierMatricule = connexion.lastrowid
            messagebox.showinfo("Information","Modification éffectuée avec succès")
            refresh_table()
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
            txtCode.delete("0", "end") 
            txtMoyenne.delete("0", "end") 
            comboEtudiant.delete("0", "end")
            comboMatiere.delete("0", "end") 
            # Mise à jour du tableau après la suppression
            table.delete(selection)
        except Exception as e:
            print(e)
            # Retour en cas d'erreur
            db.rollback()
        finally:
            db.close()  


def charger_etudiant():
    # Connexion à la base de données
    db = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_departement")
    cursor = db.cursor()

    try:
        # Exécuter la requête pour récupérer les promotions depuis la table
        cursor.execute("SELECT CONCAT(nom, ' ', prenom) AS nom_complet FROM etudiants")
        resultats = cursor.fetchall()

        # Liste pour stocker les promotions
        etudiant = [row[0] for row in resultats]

        # Peupler le menu déroulant avec les promotions
        comboEtudiant['values'] = etudiant
    except Exception as e:
        print(e)

    finally:
        # Fermer la connexion à la base de données
        cursor.close()
        db.close() 



def charger_matiere():
    # Connexion à la base de données
    db = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_departement")
    cursor = db.cursor()

    try:
        # Exécuter la requête pour récupérer les promotions depuis la table
        cursor.execute("SELECT libele_mat FROM matiere")
        resultats = cursor.fetchall()

        # Liste pour stocker les promotions
        matiere = [row[0] for row in resultats]

        # Peupler le menu déroulant avec les promotions
        comboMatiere['values'] = matiere
    except Exception as e:
        print(e)

    finally:
        # Fermer la connexion à la base de données
        cursor.close()
        db.close() 



#Creation de la fenetre de connexion
root = Tk()
root.title("GESTION DES NOTES")
root.geometry("1350x700+0+0")
root.resizable(False,False)
root.configure(background="#091821")


#Titre 
lbltitre = Label(root, borderwidth=3, relief=SUNKEN, text="GESTION DES NOTES", font=("Sans Serif", 25),background="#2F4F4F", fg="#FFFAFA")
lbltitre.place(x=0, y=0, width=1350, height=80)


#Matricule
lblCode= Label(root, text="CODE ", font=("Arial", 18), background="#091821", fg="white")
lblCode.place(x=70, y=100, width=150)
txtCode = Entry(root, bd=4, font=("Arial", 14))
txtCode.place(x=250, y=100, width=200)

#Rechercher
lblRechercher = Label(root, text="RECHERCHER", font=("Arial", 18), background="#091821", fg="white")
lblRechercher.place(x=650, y=220, width=250)
txtRechercher = Entry(root, bd=4, font=("Arial", 14))
txtRechercher.place(x=900, y=220, width=200)

# Étiquette pour la promotion
lblEtudiant = Label(root, text="ETUDIANT ", font=("Arial", 18), background="#091821", fg="white")
lblEtudiant.place(x=50, y=140, width=200)
# Combobox pour les enseignant
comboEtudiant = ttk.Combobox(root, font=("Arial", 14))
comboEtudiant.place(x=250, y=140, width=200)
#Appel de la fonction 
charger_etudiant()

# Étiquette pour la promotion
lblMatiere = Label(root, text="MATIERES ", font=("Arial", 18), background="#091821", fg="white")
lblMatiere.place(x=50, y=180, width=200)
# Combobox pour les enseignant
comboMatiere = ttk.Combobox(root, font=("Arial", 14))
comboMatiere.place(x=250, y=180, width=200)
charger_matiere()

#MOYENNE
lblMoyenne = Label(root,text="MOYENNE ", font= ("Arial",18),background= "#091821",fg="white")
lblMoyenne.place(x=70, y=220, width=150)
txtMoyenne = Entry(root,bd=4,font=("Arial",14))
txtMoyenne.place(x=250,y=220,width=200)


#Bouton enregistrer
btnEnregistrer = Button(root,text="ENREGISTRER",bd=4,font=("Arial",12),bg="#FF4500",fg="white",command=Ajouter)
btnEnregistrer.place(x=500,y=100,width=150)

#Bouton Modifier
btnModifier = Button(root,text="MODIFIER",bd=4,font=("Arial",12),bg="#FF4500",fg="white",command=Modifier)
btnModifier.place(x=500, y=140, width=150)

#Bouton Supprimer
btnSupprimer = Button(root, text="SUPPRIMER", bd=4, font=("Arial", 12), bg="#FF4500", fg="white", command=Supprimer)
btnSupprimer.place(x=500, y=180, width=150)

#IMPRIMER
btnAfficher = Button(root, text="IMPRESSION", bd=4, font=("Arial", 12), bg="#FF4500", fg="white", command="recuperer_et_afficher")
btnAfficher.place(x=500, y=220, width=150)

#Bouton Retour
btnRetour = Button(root, text="RETOUR", bd=4, font=("Arial", 12), bg="#B22222", fg="white", command=Retour)
btnRetour.place(x=1150, y=220, width=120)


#Creation de la Table
table = ttk.Treeview(root,columns=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10), height=5, show="headings")
table.place(x=70, y=280, width=1200, height=400)

#Entetes
table.heading(1, text="CODE")
table.heading(2, text="NOM ET PRENOM")
table.heading(3, text="MATIERE")
table.heading(4, text="MOYENNE")


#Définir les dimensions des colones
table.column(1, width=200)
table.column(2, width=500)
table.column(3, width=300)
table.column(4, width=200)


#Connexion au serveur 
db = mysql.connector.connect(host="localhost",user="root",password="",database="gestion_departement")
connexion = db.cursor()
connexion.execute("select * from evaluer")
for row in connexion:
    table.insert('',END, values=row)
db.close()


def on_select(event):
    selection = table.selection()
    if selection:
        item = table.item(selection[0])
        values = item['values']
        txtCode.delete(0, END)
        txtCode.insert(0, values[0]) 
        comboEtudiant.delete(0, END)
        comboEtudiant.insert(0, values[1])
        comboMatiere.delete(0, END)
        comboMatiere.insert(0, values[2])
        txtMoyenne.delete(0,END)
        txtMoyenne.insert(0,values[3])

# Associer la fonction à l'événement de sélection
table.bind('<ButtonRelease-1>', on_select)



#Execution
root.mainloop()