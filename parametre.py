
from subprocess import call
from tkinter import *


def user():
    root.destroy()
    call(["python", "user.py"])

def historique():
    root.destroy()
    call(["python", "historique.py"])

#Creation de la fenetre de connexion
root = Tk()
root.title("GESTIONN DES PARAMETRES")
root.geometry("600x300+400+200")
root.resizable(False,False)
root.configure(background="#091821")

#Titre
lbltitre = Label(root, borderwidth=3, relief=SUNKEN, text="PARAMETRES", font=("Sans Serif", 25), background="#2F4F4F",fg= "#FFFAFA")
lbltitre.place(x=0, y=0, width=600, height=50)

#Bouton enregistrer
btnEnregistrer = Button(root, text="UTILISATEURS", bd=4, font=("Arial", 12), bg="#FF4500", fg="white", command=user)
btnEnregistrer.place(x=150, y=140, width=150)

#Bouton Modifier
btnModifier = Button(root, text="HISTORIQUES", bd=4, font=("Arial", 12), bg="#FF4500", fg="white", command=historique)
btnModifier.place(x=320, y=140, width=150)


#Execution
root.mainloop()