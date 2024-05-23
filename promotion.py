#Les bibliothèques à importer
import tkinter
from cProfile import label
from subprocess import call
from tkinter import ttk, Tk
from tkinter import *
from tkinter import messagebox
import mysql.connector



#FONCTION RETOUR
def Retour():
    root.destroy()
    #call(["python", "menuprincipal.py"])


def refresh_table():
    # Effacer toutes les lignes de la table
    for item in table.get_children():
        table.delete(item)
    # Reconnecter à la base de données
    db = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_departement")
    connexion = db.cursor()

    # Exécuter la requête pour récupérer les données mises à jour
    connexion.execute("SELECT id_promotion, libele FROM promotion")

    # Ajouter les nouvelles données à la table
    for row in connexion:
        table.insert('', END, values=row)
    # Fermer la connexion à la base de données
    db.close()

#Fonction ajouter
def Ajouter():
    code = txtPromotion.get()
    libele = txtLibelePromotion.get()
 
    db = mysql.connector.connect(host="localhost", user= "root",password="",database="gestion_departement")
    connexion = db.cursor()
    try:
        if(code == "" ):
            messagebox.showerror("","Saisir le code de la promotion!!")
        elif(libele == ""):
            messagebox.showerror("","Saisir le libele de la promotion!!")
        else:
            sql = "INSERT INTO promotion(id_promotion,libele) VALUES (%s, %s)"
            val = (code, libele)
            connexion.execute(sql,val)
            db.commit()
            derniercodePromotion = connexion.lastrowid
            messagebox.showinfo("Information", "Promotion ajouter avec succès")
            refresh_table()
            txtPromotion.delete("0", "end")
            txtLibelePromotion.delete("0", "end")
            #root.destroy()
            #call(["python", "promotion.py"])
    except Exception as e:
        print(e)
        #retour
        db.rollback()
        db.close()


#Fonction Modifier
def Modifier():
    code = txtPromotion.get()
    libele = txtLibelePromotion.get()
    
    db = mysql.connector.connect(host="localhost", user= "root",password="",database="gestion_departement")
    connexion = db.cursor()
    try:
        sql= "UPDATE promotion SET libele=%s WHERE id_promotion=%s"
        val= (libele,code)
        connexion.execute(sql,val)
        db.commit()
        dernierMatricule = connexion.lastrowid
        messagebox.showinfo("Information","Modification éffectuée avec succès")
        refresh_table()
        txtPromotion.delete("0", "end")
        txtLibelePromotion.delete("0", "end")
        #root.destroy()
        #call(["python", "promotion.py"])
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
            sql = "DELETE FROM promotion WHERE id_promotion=%s"
            val = (matricule_a_supprimer,)
            connexion.execute(sql, val)
            db.commit()
            messagebox.showinfo("Information", "Suppression effectuée avec succès")
            txtPromotion.delete("0", "end") 
            txtLibelePromotion.delete("0", "end") 
            
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
root.title("GESTIONN DES PROMOTIONS")
root.geometry("600x400+400+200")
root.resizable(False,False)
root.configure(background="#091821")

#Titre 
lbltitre = Label(root, borderwidth=3, relief=SUNKEN, text="AJOUTER UNE PROMOTIONS",font= ("Sans Serif",25),background= "#2F4F4F",fg= "#FFFAFA")
lbltitre.place(x = 0, y = 0, width= 600, height=50)

#Code promotion
lblCodePromotion = Label(root,text="CODE ", font= ("Arial",18),background= "#091821",fg="white")
lblCodePromotion.place(x=5, y=70, width=150)
txtPromotion = Entry(root,bd=4,font=("Arial",14))
txtPromotion.place(x=130,y=70,width=150)

#libele promotion
lblLibelePromotion = Label(root,text="LIBELE ", font= ("Arial",18),background= "#091821",fg="white")
lblLibelePromotion.place(x=5, y=120, width=150)
txtLibelePromotion = Entry(root,bd=4,font=("Arial",14))
txtLibelePromotion.place(x=130,y=120,width=150)

#Bouton enregistrer
btnEnregistrer = Button(root,text="ENREGISTRER",bd=4,font=("Arial",12),bg="#FF4500",fg="white",command=Ajouter)
btnEnregistrer.place(x=300,y=70,width=150)

#Bouton Modifier
btnModifier = Button(root,text="MODIFIER",bd=4,font=("Arial",12),bg="#FF4500",fg="white",command=Modifier)
btnModifier.place(x=300,y=120,width=150)

#Bouton Supprimer
btnSupprimer = Button(root, text="SUPPRIMER", bd=4, font=("Arial", 12), bg="#FF4500", fg="white", command=Supprimer)
btnSupprimer.place(x=450,y=70,width=150)

#Bouton Retour
btnRetour = Button(root, text="RETOUR", bd=4, font=("Arial", 12), bg="#B22222", fg="white", command=Retour)
btnRetour.place(x=450, y=120, width=120)

#Creation de la Table
table = ttk.Treeview(root,columns=(1, 2),height=5,show="headings")
table.place(x=80,y=180,width=450,height=180)

#Entetes
table.heading(1, text="CODE")
table.heading(2, text="LIBELE")

#Définir les dimensions des colones
table.column(1,width=20)
table.column(2,width=150)

#Connexion au serveur et affichage des enregistrement
db = mysql.connector.connect(host="localhost",user="root",password="",database="gestion_departement")
connexion= db.cursor()
connexion.execute("select * from promotion")
for row in connexion:
    table.insert('',END, values=row)
db.close()

# Fonction appelée lorsqu'un élément est sélectionné dans le tableau
def on_select(event):
    selection = table.selection()
    if selection:
        item = table.item(selection[0])
        values = item['values']
        txtPromotion.delete(0, END)
        txtPromotion.insert(0, values[0]) 
        txtLibelePromotion.delete(0, END)
        txtLibelePromotion.insert(0, values[1])
    
# Associer la fonction à l'événement de sélection
table.bind('<ButtonRelease-1>', on_select)


#Execution
root.mainloop()