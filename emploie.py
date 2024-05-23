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
    connexion.execute("SELECT id_emploi,jour,heure,id_enseignant,salle,id_matiere")

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
    matiere = comboMatiere.get()
    enseignant = comboEnseigant.get()
    jour = comboJour.get()
    heure = txtHeure.get()
    salle = comboSalle.get()
    db = mysql.connector.connect(host="localhost", user= "root",password="",database="gestion_departement")
    connexion = db.cursor()
    try:
        if(code == "" ):
            messagebox.showerror("","Saisir le matricule!!")
        elif(matiere == ""):
            messagebox.showerror("","Choisir la matiere!!")
        elif(enseignant == ""):
            messagebox.showerror("","Choisir l'enseignant!!")
        elif(jour ==""):
            messagebox.showerror("","Choisir le jour!!")
        elif(heure == ""):
            messagebox.showerror("","Saisir l'adresse!!")
        elif (salle == ""):
            messagebox.showerror("", "Saisir la salle!!")
        else:
            sql= "INSERT INTO emploi_temps (id_emploi,jour,heure,id_enseignant,salle,id_matiere) VALUES (%s, %s, %s,%s, %s,%s)"
            val= (code,jour, heure,enseignant,salle,matiere)
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
    matiere = comboMatiere.get()
    enseignant = comboEnseigant.get()
    jour = comboJour.get()
    heure = txtHeure.get()
    db = mysql.connector.connect(host="localhost", user= "root",password="",database="gestion_departement")
    connexion = db.cursor()
    try:
        if(code == "" ):
            messagebox.showerror("","Saisir le matricule!!")
        elif(matiere == ""):
            messagebox.showerror("","Saisir le nom!!")
        elif(enseignant == ""):
            messagebox.showerror("","Saisir le prenom!!")
        elif(jour ==""):
            messagebox.showerror("","Saisir le numéro de téléphone!!")
        elif(heure == ""):
            messagebox.showerror("","Saisir l'adresse!!")
        else:
            sql= "UPDATE emploi_temps SET id_enseignant=%s, id_matiere=%s, jour=%s, heure=%s WHERE id_emploi=%s"
            val= (enseignant, matiere, jour,heure, code)
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
            sql = "DELETE FROM emploi_temps WHERE id_emploi=%s"
            val = (matricule_a_supprimer,)
            connexion.execute(sql, val)
            db.commit()
            messagebox.showinfo("Information", "Suppression effectuée avec succès")
            txtCode.delete("0", "end") 
            comboJour.delete("0", "end") 
            txtHeure.delete("0", "end") 
            comboEnseigant.delete("0", "end")
            comboMatiere.delete("0", "end") 
            # Mise à jour du tableau après la suppression
            table.delete(selection)
        except Exception as e:
            print(e)
            # Retour en cas d'erreur
            db.rollback()
        finally:
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


def charger_promotions():
    # Connexion à la base de données
    db = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_departement")
    cursor = db.cursor()

    try:
        # Exécuter la requête pour récupérer les promotions depuis la table
        cursor.execute("SELECT CONCAT(nom, ' ', prenom) AS nom_complet FROM enseignant")
        resultats = cursor.fetchall()

        # Liste pour stocker les promotions
        enseignant = [row[0] for row in resultats]

        # Peupler le menu déroulant avec les promotions
        comboEnseigant['values'] = enseignant
    except Exception as e:
        print(e)

    finally:
        # Fermer la connexion à la base de données
        cursor.close()
        db.close() 


#Creation de la fenetre de connexion
root = Tk()
root.title("GESTION DES EMPLOIS DU TEMPS")
root.geometry("1350x700+0+0")
root.resizable(False, False)
root.configure(background="#091821")


#Titre 
lbltitre = Label(root, borderwidth=3, relief=SUNKEN, text="GESTION DES EMPLOIS DU TEMPS", font=("Sans Serif", 25), background="#2F4F4F", fg="#FFFAFA")
lbltitre.place(x=0, y=0, width=1350, height=80)

#Matricule
lblCode = Label(root,text="IDENTIFIANT", font=("Arial", 18), background="#091821", fg="white")
lblCode.place(x=70, y=150, width=155)
txtCode = Entry(root, bd=4, font=("Arial", 14))
txtCode.place(x=250, y=150, width=200)

# Étiquette pour la promotion
lblSenseignant = Label(root, text="ENSEIGNANT", font=("Arial", 18), background="#091821", fg="white")
lblSenseignant.place(x=50, y=190, width=200)
# Combobox pour les enseignant
comboEnseigant = ttk.Combobox(root, font=("Arial", 14))
comboEnseigant.place(x=250, y=190, width=200)
#Appel de la fonction
charger_promotions()

# Étiquette pour la promotion
lblMatiere = Label(root, text="MATIERES", font=("Arial", 18), background="#091821", fg="white")
lblMatiere.place(x=50, y=230, width=200)
# Combobox pour les enseignant
comboMatiere = ttk.Combobox(root, font=("Arial", 14))
comboMatiere.place(x=250, y=230, width=200)
charger_matiere()

#Niveau
lblSalle = Label(root,text="SALLE", font=("Arial", 18), background="#091821", fg="white")
lblSalle.place(x=70, y=270, width=150)
comboSalle= ttk.Combobox(root,font=("Arial",14))
comboSalle['values'] = ['SALLE INFOS1', 'SALLE INFOS2', 'SALLE INFOS3', 'EMPHIE']
comboSalle.place(x=250,y=270,width=200)

#Niveau
lblJour = Label(root, text="JOUR", font=("Arial", 18), background="#091821", fg="white")
lblJour.place(x=70, y=310, width=150)
comboJour= ttk.Combobox(root, font=("Arial", 14))
comboJour['values'] = ['LUNDI', 'MARDI', 'MERCREDI', 'JEUDI', 'VENDREDI', 'SAMEDI']
comboJour.place(x=250, y=310, width=200)

#Niveau
lblHeure= Label(root, text="HEURE", font=("Arial", 18), background="#091821", fg="white")
lblHeure.place(x=70, y=350, width=150)
txtHeure = Entry(root, bd=4, font=("Arial", 14))
txtHeure.place(x=250, y=350, width=200)



#Bouton enregistrer
btnEnregistrer = Button(root, text="ENREGISTRER", bd=4, font=("Arial", 12), bg="#FF4500", fg="white", command=Ajouter)
btnEnregistrer.place(x=250, y=400, width=150)

#Bouton Modifier
btnModifier = Button(root, text="MODIFIER", bd=4, font=("Arial", 12), bg="#FF4500", fg="white", command=Modifier)
btnModifier.place(x=250, y=440, width=150)

#Bouton Supprimer
btnSupprimer = Button(root, text="SUPPRIMER", bd=4, font=("Arial", 12), bg="#FF4500", fg="white", command=Supprimer)
btnSupprimer.place(x=250, y=480, width=150)

#Bouton Retour
btnRetour = Button(root, text="RETOUR", bd=4, font=("Arial", 12), bg="#B22222", fg="white", command=Retour)
btnRetour.place(x=1200, y=100, width=120)

#IMPRIMER
btnAfficher = Button(root, text="IMPRESSION", bd=4, font=("Arial", 12), bg="#FF4500", fg="white", command="recuperer_et_afficher")
btnAfficher.place(x=900, y=100, width=150)

#Rechercher
lblRechercher = Label(root,text="RECHERCHER", font= ("Arial",18),background= "#091821",fg="white")
lblRechercher.place(x=460, y=100, width=250)
txtRechercher = Entry(root,bd=4,font=("Arial",14))
txtRechercher.place(x=680,y=100,width=200)

#Creation de la Table
table = ttk.Treeview(root, columns=(1, 2, 3, 4, 5, 6), height=5, show="headings")
table.place(x=500, y=150, width=820, height=450)


#Entetes
table.heading(1, text="IDENTIFIANT")
table.heading(2, text="JOUR")
table.heading(3, text="HEURE")
table.heading(4, text="ENSEIGNANT")
table.heading(5, text="SALLE")
table.heading(6, text="MATIERE")

#Définir les dimensions des colones
table.column(1, width=20)
table.column(2, width=50)
table.column(3, width=100)
table.column(4, width=200)
table.column(5, width=100)
table.column(6, width=100)


#Connexion au serveur 
db = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_departement")
connexion= db.cursor()
connexion.execute("select * from emploi_temps")
for row in connexion:
    table.insert('', END, values=row)
db.close()

def on_select(event):
    selection = table.selection()
    if selection:
        item = table.item(selection[0])
        values = item['values']
        txtCode.delete(0, END)
        txtCode.insert(0, values[0]) 
        comboEnseigant.delete(0, END)
        comboEnseigant.insert(0, values[3])
        comboMatiere.delete(0, END)
        comboMatiere.insert(0, values[5])
        comboSalle.delete(0, END)
        comboSalle.insert(0, values[4])
        comboJour.delete(0, END)
        comboJour.insert(0, values[1])
        txtHeure.delete(0, END)
        txtHeure.insert(0, values[2])


# Associer la fonction à l'événement de sélection
table.bind('<ButtonRelease-1>', on_select)
       

       
table.bind('<ButtonRelease-1>', on_select)


#Execution
root.mainloop()