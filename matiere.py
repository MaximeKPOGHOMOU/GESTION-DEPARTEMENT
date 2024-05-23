
from subprocess import call
from tkinter import ttk, Tk
from tkinter import *
from tkinter import messagebox
import mysql.connector
from etatMatiere import FenetreEtatMatiere

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
    connexion.execute("SELECT code_mat, libele_mat, semestre, mat_enseignant FROM matiere")

    # Ajouter les nouvelles données à la table
    for row in connexion:
        table.insert('', END, values=row)
    # Fermer la connexion à la base de données
    db.close()


def recuperer_et_afficher():
    # Récupérer les données de la table de la fenêtre etudiant
    data_matiere = []
    for row in table.get_children():
        values = [table.item(row, 'values')[i] for i in range(4)]
        data_matiere.append(values)

    # Afficher les données dans la fenêtre etatEtudiant
    fenetre_etat_matiere = FenetreEtatMatiere(data_matiere)

#Fonction ajouter
def Ajouter():
    code = txtCode.get()
    libele = txtLibele.get()
    semestre = comboSemestre.get()
    enseignant = comboEnseigant.get()
    
    db = mysql.connector.connect(host="localhost", user= "root",password="",database="gestion_departement")
    connexion = db.cursor()
    try:
        if(code == "" ):
            messagebox.showerror("","Saisir le matricule!!")
        elif(libele == ""):
            messagebox.showerror("","Saisir le nom!!")
        elif(semestre == ""):
            messagebox.showerror("","Saisir le prenom!!")
        elif(enseignant ==""):
            messagebox.showerror("","Saisir le numéro de téléphone!!")
        else:
            sql= "INSERT INTO matiere (code_mat,libele_mat,semestre,mat_enseignant) VALUES (%s, %s, %s, %s)"
            val= (code, libele, semestre, enseignant)
            connexion.execute(sql,val)
            db.commit()
            dernierMatricule = connexion.lastrowid
            messagebox.showinfo("Information","Enregistrement éffectué avec succès")
            refresh_table()
            txtCode.delete("0", "end")
            txtLibele.delete("0", "end")
            comboEnseigant.set("")
            comboSemestre.set("")
            #root.destroy()
            #call(["python", "matiere.py"])
    except Exception as e:
        print(e)
        #retour
        db.rollback()
        db.close()


#Fonction Modifier
def Modifier():
    code = txtCode.get()
    libele = txtLibele.get()
    semestre = comboSemestre.get()
    enseignant = comboEnseigant.get()
    db = mysql.connector.connect(host="localhost", user= "root",password="",database="gestion_departement")
    connexion = db.cursor()
    try:
        if(code == "" ):
                messagebox.showerror("","Saisir le matricule!!")
        elif(libele == ""):
            messagebox.showerror("","Saisir le nom!!")
        elif(semestre == ""):
            messagebox.showerror("","Saisir le prenom!!")
        elif(enseignant ==  ""):
            messagebox.showerror("","Saisir le numéro de téléphone!!")
        else:  
            sql= "UPDATE matiere SET libele_mat=%s, semestre=%s, mat_enseignant=%s WHERE code_mat=%s"
            val= (libele, semestre, enseignant, code)
            connexion.execute(sql,val)
            db.commit()
            dernierMatricule = connexion.lastrowid
            messagebox.showinfo("Information","Modification éffectuée avec succès")
            refresh_table()
            txtCode.delete("0", "end")
            txtLibele.delete("0", "end")
            comboEnseigant.set("")
            comboSemestre.set("")
            #root.destroy()
            #call(["python", "matiere.py"])
    except Exception as e:
        print(e)
        #retour
        db.rollback()
        db.close()
        



def Supprimer():
    selection = table.selection()
    if selection:
        matricule_a_supprimer = table.item(selection[0])['values'][0]
        try:
            db = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_departement")
            connexion = db.cursor()           
            sql = "DELETE FROM matiere WHERE code_mat=%s"
            val = (matricule_a_supprimer,)
            connexion.execute(sql, val)
            db.commit()
            messagebox.showinfo("Information", "Suppression effectuée avec succès")
            txtCode.delete("0", "end") 
            txtLibele.delete("0", "end")      
            comboEnseigant.set("") 
            comboSemestre.set("")
            # Mise à jour du tableau après la suppression
            table.delete(selection)
        except Exception as e:
            print(e)
            # Retour en cas d'erreur
            db.rollback()
        finally:
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

        # Fonction pour récupérer et afficher les étudiants par promotion depuis MySQL

def afficher_par_semestre():
    niveau_selec = comboAffSemestre.get()

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gestion_departement"
    )
    cursor = connection.cursor()

    try:
        # Exécutez la requête pour récupérer les matières par semestre
        cursor.execute("SELECT * FROM matiere WHERE semestre = %s", (niveau_selec,))
        semestres = cursor.fetchall()

        # Nettoyer la table avant d'afficher de nouvelles données
        for row in table.get_children():
            table.delete(row)

        # Affichez les matières dans la table
        for semestre in semestres:
            table.insert("", "end", values=semestre)

    except Exception as e:
        print(e)

    finally:
        # Fermez la connexion à la base de données, même si une exception est levée
        cursor.close()
        connection.close()

def afficher():
    afficher_par_semestre()


#Creation de la fenetre de connexion
root = Tk()
root.title("GESTION  DES MATIERES")
root.geometry("1350x700+0+0")
root.resizable(False,False)
root.configure(background="#091821")



#Titre 
lbltitre = Label(root, borderwidth = 3, relief = SUNKEN ,text="ENREGISTREMENT DES MATIERES",font= ("Sans Serif",25),background= "#2F4F4F",fg= "#FFFAFA")
lbltitre.place(x = 0, y = 0, width= 1350, height=80)

#Matricule
lblCode = Label(root,text="CODE :", font= ("Arial",18),background= "#091821",fg="white")
lblCode.place(x=70, y=120, width=150)
txtCode = Entry(root,bd=4,font=("Arial",14))
txtCode.place(x=250,y=120,width=150)

#Rechercher
lblRechercher = Label(root,text="RECHERCHER:", font= ("Arial",18),background= "#091821",fg="white")
lblRechercher.place(x=520, y=120, width=250)
txtRechercher = Entry(root,bd=4,font=("Arial",14))
txtRechercher.place(x=750,y=120,width=200)

#Nom
lblLibele= Label(root,text="LIBELE :", font= ("Arial",18),background= "#091821",fg="white")
lblLibele.place(x=40, y=160, width=200)
txtLibele = Entry(root,bd=4,font=("Arial",14))
txtLibele.place(x=250,y=160,width=300)

#Niveau
lblSemestre = Label(root,text="SEMESTRE :", font= ("Arial",18),background= "#091821",fg="white")
lblSemestre.place(x=50, y=200, width=200)
comboSemestre = ttk.Combobox(root,font=("Arial",14))
comboSemestre['values'] = ['S1', 'S2', 'S3', 'S4','S5', 'S6', 'S7', 'S8']
comboSemestre.place(x=250,y=200,width=300)

# Étiquette pour la promotion
lblSenseignant = Label(root, text="ENSEIGNANT :", font=("Arial", 18), background="#091821", fg="white")
lblSenseignant.place(x=50, y=240, width=200)
# Combobox pour les enseignant
comboEnseigant = ttk.Combobox(root, font=("Arial", 14))
comboEnseigant.place(x=250,y=240,width=300)
#Appel de la fonction 
charger_promotions()


#Bouton enregistrer
btnEnregistrer = Button(root,text="ENREGISTRER",bd=4,font=("Arial",12),bg="#FF4500",fg="white",command=Ajouter)
btnEnregistrer.place(x=250,y=300,width=150)

#Bouton Modifier
btnModifier = Button(root,text="MODIFIER",bd=4,font=("Arial",12),bg="#FF4500",fg="white",command=Modifier)
btnModifier.place(x=250,y=340,width=150)

#Bouton Supprimer
btnSupprimer = Button(root, text="SUPPRIMER", bd=4, font=("Arial", 12), bg="#FF4500", fg="white", command=Supprimer)
btnSupprimer.place(x=250, y=380, width=150)

#Bouton Affichage
btnAfficher = Button(root, text="AFFICHER", bd=4, font=("Arial", 12), bg="#FF4500", fg="white", command=afficher)
btnAfficher.place(x=250, y=490, width=150)

# La liste des etudiants par SEMESTRE
lblSearch = Label(root,text="AFFICHER PAR :", font= ("Arial",18),background= "#091821",fg="white")
lblSearch.place(x=20, y=450, width=250)

#Affichage par niveau
comboAffSemestre = ttk.Combobox(root,font=("Arial",14))
comboAffSemestre['values'] = ['S1', 'S2', 'S3', 'S4','S5', 'S6', 'S7', 'S8']
comboAffSemestre.place(x=250,y=450,width=150)

#Bouton Retour
btnRetour = Button(root, text="RETOUR", bd=4, font=("Arial", 12), bg="#B22222", fg="white", command=Retour)
btnRetour.place(x=1220, y=120, width=120)

#IMPRIMER
btnAfficher = Button(root, text="IMPRESSION", bd=4, font=("Arial", 12), bg="#FF4500", fg="white", command=recuperer_et_afficher)
btnAfficher.place(x=980, y=120, width=150)


#Creation de la Table
table = ttk.Treeview(root, columns=(1, 2, 3, 4, 5), height=5, show="headings")
table.place(x=560, y=160, width=780, height=450)

#Entetes
table.heading(1, text="ID")
table.heading(2, text="LIBELE")
table.heading(3, text="SEMESTRE")
table.heading(4, text="ENSEIGNANT")
table.column(1,width=100)
table.column(2,width=250)
table.column(3,width=250)
table.column(4,width=200)

#Connexion au serveur 
db = mysql.connector.connect(host="localhost",user="root",password="",database="gestion_departement")
connexion= db.cursor()
connexion.execute("select * from matiere")
for row in connexion:
    table.insert('',END, values=row)
db.close()



# Fonction appelée lorsqu'un élément est sélectionné dans la table
def on_select(event):
    selection = table.selection()
    if selection:
        item = table.item(selection[0])
        values = item['values']

        # Mettre à jour les champs avec les valeurs de l'enregistrement sélectionné
        txtCode.delete(0, END)
        txtCode.insert(0, values[0])

        txtLibele.delete(0, END)
        txtLibele.insert(0, values[1])

        # Assurez-vous que le semestre est sélectionné dans la liste des valeurs possibles
        if values[2] in ('S1', 'S2', 'S3', 'S4','S5', 'S6', 'S7', 'S8'):
            comboSemestre.set(values[2])
        else:
            comboSemestre.set('')

        # Récupérer la liste des enseignants depuis la table dans la base de données
        enseignants = obtenir_liste_enseignants()

        # Assurez-vous que l'enseignant est sélectionné dans la liste des valeurs possibles
        if values[3] in enseignants:
            comboEnseigant.set(values[3])
        else:
            comboEnseigant.set('')

# Fonction pour récupérer la liste des enseignants depuis la table dans la base de données
def obtenir_liste_enseignants():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gestion_departement"
    )
    cursor = connection.cursor()

    try:
        # Exécuter la requête pour récupérer les enseignants depuis la table
        cursor.execute("SELECT CONCAT(nom, ' ', prenom) AS nom_complet FROM enseignant")
        resultats = cursor.fetchall()

        # Liste pour stocker les enseignants
        enseignants = [row[0] for row in resultats]
        return enseignants
    except Exception as e:
        print(e)
    finally:
        # Fermer la connexion à la base de données
        cursor.close()
        connection.close()

# Associer la fonction à l'événement de sélection
table.bind('<ButtonRelease-1>', on_select)


def RechercherInstantaneeMatiere():
    # Effacer le tableau avant d'afficher les résultats de la recherche
    for item in table.get_children():
        table.delete(item)

    recherche_termes = txtRechercher.get()
    try:
        db = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_departement")
        connexion = db.cursor()
        sql = "SELECT * FROM matiere WHERE libele_mat LIKE %s OR code_mat LIKE %s"
        val = ('%' + recherche_termes + '%', '%' + recherche_termes + '%')
        connexion.execute(sql, val)
        resultats = connexion.fetchall()

        for row in resultats:
            table.insert('', END, values=row)
    except Exception as e:
        print(e)
    finally:
        db.close()


# Fonction pour déclencher la recherche instantanée après un délai
def recherche_instantanee_callback_matiere(event):
    root.after(500, RechercherInstantaneeMatiere)


# Associer la fonction à l'événement de frappe de l'utilisateur
txtRechercher.bind('<KeyRelease>', recherche_instantanee_callback_matiere)

#Execution
root.mainloop()