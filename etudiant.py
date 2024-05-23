#Les bibliothèques à importer
from subprocess import call
from tkinter import ttk, Tk
from tkinter import *
from tkinter import messagebox
import mysql.connector
#installation du module mysql.connector "python -m pip install mysql-connector-python"
from etatEtudiant import FenetreEtatEtudiant


# Ajouter cette fonction pour rafraîchir la table après la modification
def refresh_table():
    # Effacer toutes les lignes de la table
    for item in table.get_children():
        table.delete(item)
    # Reconnecter à la base de données
    db = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_departement")
    connexion = db.cursor()
    # Exécuter la requête pour récupérer les données mises à jour
    connexion.execute("SELECT matricule, nom, prenom, genre, niveau, id_promotion, annee_univer FROM etudiants")

    # Ajouter les nouvelles données à la table
    for row in connexion:
        table.insert('', END, values=row)
    # Fermer la connexion à la base de données
    db.close()

#FONCTION RETOUR
def Retour():
    root.destroy()
    #call(["python", "menuprincipal.py"])

def recuperer_et_afficher():
    # Récupérer les données de la table de la fenêtre etudiant
    data_etudiant = []
    for row in table.get_children():
        values = [table.item(row, 'values')[i] for i in range(6)]
        data_etudiant.append(values)

    # Afficher les données dans la fenêtre etatEtudiant
    fenetre_etat_etudiant = FenetreEtatEtudiant(data_etudiant)

# Fonction pour vérifier si le matricule de l'étudiant existe déjà dans la base de données
def matricule_exists(matricule):
    db = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_departement")
    connexion = db.cursor()
    
    try:
        sql = "SELECT COUNT(*) FROM etudiants WHERE matricule = %s"
        val = (matricule,)
        connexion.execute(sql, val)
        result = connexion.fetchone()
        # Si le résultat est différent de zéro, cela signifie que le matricule existe déjà
        return result[0] != 0
    except Exception as e:
        print(e)
    finally:
        connexion.close()
        db.close()

# Fonction pour ajouter un nouvel étudiant
def Ajouter():
    matricule = txtMatricule.get()
    nom = txtNom.get()
    prenom = txtPrenom.get()
    genre = valeurSexe.get()
    niveau = comboNiveau.get()
    promotion = combopromotion.get()
    annee = comboAnnee.get()
    
    # Vérifier si le matricule existe déjà dans la base de données
    if matricule_exists(matricule):
        messagebox.showerror("", "Ce matricule existe déjà. Veuillez utiliser un autre matricule.")
        return

    db = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_departement")
    connexion = db.cursor()

    try:
        if matricule == "" or nom == "" or prenom == "" or genre == "" or niveau == "" or promotion == "" or annee == "":
            messagebox.showerror("", "Veuillez remplir tous les champs!")
        else:
            sql = "INSERT INTO etudiants (matricule, nom, prenom, genre, niveau, id_promotion,annee_univer) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (matricule, nom, prenom, genre, niveau, promotion,annee)
            connexion.execute(sql, val)
            db.commit()
            dernierMatricule = connexion.lastrowid
            messagebox.showinfo("Information", "Enregistrement effectué avec succès")
            refresh_table()
            txtMatricule.delete("0", "end")
            txtNom.delete("0", "end")
            txtPrenom.delete("0", "end")
            valeurSexe.set("")
            comboNiveau.set("")
            combopromotion.set("")
            comboAnnee.set("")
            #root.destroy()
            #call(["python", "etudiant.py"])
    except Exception as e:
        print(e)
        # Retour en cas d'erreur
        db.rollback()
    finally:
        connexion.close()
        db.close()

#Fonction Modifier
def Modifier():
    matricule = txtMatricule.get()
    nom = txtNom.get()
    prenom = txtPrenom.get()
    genre = valeurSexe.get()
    niveau = comboNiveau.get()
    promotion = combopromotion.get()
    annee = comboAnnee.get()
    db = mysql.connector.connect(host="localhost", user="root",password="",database="gestion_departement")
    connexion = db.cursor()
    try:
        if(matricule == "" ):
                messagebox.showerror("","Saisir le matricule!!")
        elif(nom == ""):
            messagebox.showerror("","Saisir le nom!!")
        elif(prenom == ""):
            messagebox.showerror("","Saisir le prenom!!")
        elif(genre == ""):
            messagebox.showerror("","Choisir le genre!!")
        elif(niveau == ""):
            messagebox.showerror("","Choisir le niveau!!")
        elif(promotion == ""):
            messagebox.showerror("","Choisir le promotion!!")
        elif (annee == ""):
            messagebox.showerror("", "Choisir le l'année universtaire!!")
        else:   
            sql = "UPDATE etudiants SET nom=%s, prenom=%s, genre=%s, niveau=%s, id_promotion=%s, annee_univer =%s WHERE matricule=%s"
            val = (nom, prenom, genre, niveau, promotion, annee, matricule)
            connexion.execute(sql,val)
            db.commit()
            dernierMatricule = connexion.lastrowid
            messagebox.showinfo("Information","Modification éffectuée avec succès")
            refresh_table()
            txtMatricule.delete("0", "end")
            txtNom.delete("0", "end")
            txtPrenom.delete("0", "end")
            valeurSexe.set("")
            comboNiveau.set("")
            combopromotion.set("")
            comboAnnee.set("")
            #root.destroy()
            #call(["python", "etudiant.py"])
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
            sql = "DELETE FROM etudiants WHERE matricule=%s"
            val = (matricule_a_supprimer,)
            connexion.execute(sql, val)
            db.commit()
            messagebox.showinfo("Information", "Suppression effectuée avec succès")
            txtMatricule.delete("0", "end") 
            txtNom.delete("0", "end") 
            txtPrenom.delete("0", "end")
            valeurSexe.set("") 
            comboNiveau.set("") 
            combopromotion.set("")
            comboAnnee.set("")
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
        cursor.execute("SELECT libele FROM promotion")
        resultats = cursor.fetchall()

        # Liste pour stocker les promotions
        promotions = [row[0] for row in resultats]

        # Peupler le menu déroulant avec les promotions
        combopromotion['values'] = promotions
        comboPromotion['values'] = promotions
    except Exception as e:
        print(e)

    finally:
        # Fermer la connexion à la base de données
        cursor.close()
        db.close()  
        

# Fonction pour récupérer et afficher les étudiants par promotion depuis MySQL
def afficher_par_promotion():
    promotion_selec = comboPromotion.get()

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gestion_departement"
    )
    cursor = connection.cursor()

    # Exécutez la requête pour récupérer les étudiants par promotion
    cursor.execute("SELECT * FROM etudiants WHERE id_promotion = %s", (promotion_selec,))
    etudiants = cursor.fetchall()

    # Nettoyer la table avant d'afficher de nouvelles données
    for row in table.get_children():
        table.delete(row)

    # Affichez les étudiants dans la table
    for etudiant in etudiants:
        table.insert("", "end", values=etudiant)

    # Fermez la connexion à la base de données
    cursor.close()
    connection.close()
    
# Fonction pour récupérer et afficher les étudiants par promotion depuis MySQL
def afficher_par_niveau():
    niveau_selec = comboNiveauAff.get()

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gestion_departement"
    )
    cursor = connection.cursor()

    # Exécutez la requête pour récupérer les étudiants par promotion
    cursor.execute("SELECT * FROM etudiants WHERE niveau = %s", (niveau_selec,))
    etudiants = cursor.fetchall()

    # Nettoyer la table avant d'afficher de nouvelles données
    for row in table.get_children():
        table.delete(row)

    # Affichez les étudiants dans la table
    for etudiant in etudiants:
        table.insert("", "end", values=etudiant)

    # Fermez la connexion à la base de données
    cursor.close()
    connection.close()

# Fonction pour déterminer quelle fonction appeler en fonction de la sélection
def afficher():
    if comboNiveauAff.get():
        afficher_par_niveau()
    elif comboPromotion.get():
        afficher_par_promotion()
    else:
        messagebox.showwarning("Sélection nécessaire", "Veuillez sélectionner un niveau ou une promotion.")

def obtenir_promotions():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gestion_departement"
    )
    cursor = connection.cursor()

    # Exécutez la requête pour récupérer les promotions distinctes
    cursor.execute("SELECT DISTINCT id_promotion FROM etudiants")
    promotions = [row[0] for row in cursor.fetchall()]

    # Fermez la connexion à la base de données
    cursor.close()
    connection.close()

    return promotions


#Creation de la fenetre de connexion
root = Tk()
root.title("GESTION DES ETUDIANTS")
root.geometry("1350x700+0+0")
root.resizable(False,False)
root.configure(background="#091821")

#Titre 
lbltitre = Label(root, borderwidth = 3, relief = SUNKEN ,text="GESTION DES ETUDIANTS",font= ("Sans Serif",25),background= "#2F4F4F",fg= "#FFFAFA")
lbltitre.place(x = 0, y = 0, width= 1350, height=80)

#Matricule
lblMatricule = Label(root,text="MATRICULE", font= ("Arial",18),background= "#091821",fg="white")
lblMatricule.place(x=20, y=90, width=150)
txtMatricule = Entry(root,bd=4,font=("Arial",14))
txtMatricule.place(x=180,y=90,width=130)

#Rechercher
lblRechercher = Label(root, text="RECHERCHER", font=("Arial", 18), background="#091821", fg="white")
lblRechercher.place(x=0, y=250, width=180)
txtRechercher = Entry(root, bd=4, font=("Arial", 14))
txtRechercher.place(x=180, y=250, width=250)

#Nom
lblNom = Label(root, text="NOM", font=("Arial", 18), background="#091821", fg="white")
lblNom.place(x=30, y=130, width=150)
txtNom = Entry(root,bd=4,font=("Arial",14))
txtNom.place(x=180, y=130, width=250)

#Prenom
lblPrenom = Label(root, text="PRENOM", font=("Arial", 18), background="#091821", fg="white")
lblPrenom.place(x=30, y=170, width=150)
txtPrenom = Entry(root, bd=4, font=("Arial", 14))
txtPrenom.place(x=180, y=170, width=250)

# La liste des etudiants par niveau
lblSearch = Label(root, text="AFFICHER PAR", font=("Arial", 18), background="#091821", fg="white")
lblSearch.place(x=450, y=250, width=180)

#Sexe
lblGenre = Label(root, text="GENRE", font=("Arial", 18), background="#091821", fg="white")
lblGenre.place(x=470, y=170, width=130)
valeurSexe = StringVar()
lblSexeMasculin = Radiobutton(root,text="MASCULIN",value="M",variable=valeurSexe,indicatoron=0,font=("Arial",14), bg="#091821",fg="#696969")
lblSexeMasculin.place(x=650,y=170,width=115)
txtSexeFeminin = Radiobutton(root,text="FEMININ",value="F",variable=valeurSexe,indicatoron=0,font=("Arial",14), bg="#091821",fg="#696969")
txtSexeFeminin.place(x=780,y=170,width=115)

#ANNEE UNIVERSITAIRE
lblAnnee = Label(root, text="ANNEE-UNIV", font=("Arial", 18), background="#091821", fg="white")
lblAnnee.place(x=480, y=210, width=150)
comboAnnee = ttk.Combobox(root, font=("Arial", 14))
comboAnnee['values'] = ['2020-2021', '2021-2022', '2022-2023', '2023-2024', '2024-2025', '2025-2026', '2026-2027']
comboAnnee.place(x=650, y=210, width=245)

#NIVEAU
lblNiveau = Label(root,text="NIVEAU", font= ("Arial",18),background= "#091821",fg="white")
lblNiveau.place(x=480, y=90, width=150)
comboNiveau = ttk.Combobox(root, font=("Arial", 14))
comboNiveau['values'] = ['L1', 'L2', 'L3', 'L4']
comboNiveau.place(x=650, y=90, width=245)

#Affichage par niveau
comboNiveauAff = ttk.Combobox(root,font=("Arial", 14))
comboNiveauAff['values'] = ['L1', 'L2', 'L3', 'L4']
comboNiveauAff.place(x=780,y=250,width=115)

#Affichage par PROMOTION
comboPromotion = ttk.Combobox(root, font=("Arial", 14))
comboPromotion.place(x=650, y=250, width=115)
obtenir_promotions()

# Étiquette pour la promotion
lblPromotion = Label(root, text="PROMOTION", font=("Arial", 18), background="#091821", fg="white")
lblPromotion.place(x=470, y=130, width=150)
# Combobox pour les promotions
combopromotion = ttk.Combobox(root, font=("Arial", 14))
combopromotion.place(x=650, y=130, width=245)
#Appel de la fonction 
charger_promotions()

#Bouton enregistrer
btnEnregistrer = Button(root, text="ENREGISTRER", bd=4, font=("Arial", 12), bg="#FF4500", fg="white", command=Ajouter)
btnEnregistrer.place(x=980, y=90, width=150)

#Bouton Modifier
btnModifier = Button(root, text="MODIFIER", bd=4, font=("Arial", 12), bg="#FF4500", fg="white", command=Modifier)
btnModifier.place(x=980, y=130, width=150)

#Bouton Supprimer
btnSupprimer = Button(root, text="SUPPRIMER", bd=4, font=("Arial", 12), bg="#FF4500", fg="white", command=Supprimer)
btnSupprimer.place(x=980, y=170, width=150)

#Bouton Affichage
btnAfficher = Button(root, text="AFFICHER", bd=4, font=("Arial", 12), bg="#FF4500", fg="white", command=afficher)
btnAfficher.place(x=980, y=250, width=150)

#Bouton Retour
btnRetour = Button(root, text="RETOUR", bd=4, font=("Arial", 12), bg="#B22222", fg="white", command=Retour)
btnRetour.place(x=1180, y=250, width=120)

#IMPRIMER
btnAfficher = Button(root, text="IMPRESSION", bd=4, font=("Arial", 12), bg="#FF4500", fg="white", command=recuperer_et_afficher)
btnAfficher.place(x=980, y=210, width=150)

#Creation de la Table
table = ttk.Treeview(root, columns=(1, 2, 3, 4, 5, 6, 7), height=5, show="headings")
table.place(x=50, y=300, width=1250, height=380)

#Entetes
table.heading(1, text="MATRICULE")
table.heading(2, text="NOM")
table.heading(3, text="PRENOM")
table.heading(4, text="GENRE")
table.heading(5, text="NIVEAU")
table.heading(6, text="PROMOTION")
table.heading(7, text="ANNEE-UNIVERSTAIRE")

#Définir les dimensions des colones
table.column(1, width=100)
table.column(2, width=200)
table.column(3, width=150)
table.column(4, width=100)
table.column(5, width=100)
table.column(6, width=100)
table.column(7, width=150)

#Connexion au serveur 
db = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_departement")
connexion = db.cursor()
connexion.execute("select * from etudiants")
for row in connexion:
    table.insert('',END, values=row)
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
        # Assurez-vous que le genre est sélectionné dans la liste des valeurs possibles
        if values[3] in ('M', 'F'):
            valeurSexe.set(values[3])
        else:
            valeurSexe.set('')  # Réinitialisez la variable de sexe si la valeur n'est pas valide
        # Assurez-vous que le niveau est sélectionné dans la liste des valeurs possibles
        if values[4] in ('L1', 'L2', 'L3', 'L4'):
            comboNiveau.set(values[4])
        else:
            comboNiveau.set('')
        # Chargement de la promotion dans le Combobox correspondant
        promotion_selectionnee = values[5]  # Assurez-vous d'ajuster l'index en fonction de votre structure de table
        combopromotion.set(promotion_selectionnee)
        if values[6] in ('2020-2021', '2021-2022', '2022-2023', '2023-2024', '2024-2025', '2025-2026', '2026-2027'):
            comboAnnee.set(values[6])
        else:
            comboAnnee.set('')
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
        sql = "SELECT * FROM etudiants WHERE matricule LIKE %s OR nom LIKE %s OR prenom LIKE %s"
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