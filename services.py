import mysql.connector
from datetime import datetime


connexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="gestion_departement"
)
def enregistrer_action_utilisateur(nameUser, action):
    cursor = connexion.cursor()
    date_action = datetime.now().strftime("%Y-%m-%d")
    heure_action = datetime.now().strftime("%H:%M:%S")

    insert_query = "INSERT INTO historique_connexion (idUser, date, heure, action) VALUES (%s, %s, %s, %s)"
    data = (nameUser, date_action, heure_action, action)

    cursor.execute(insert_query, data)
    connexion.commit()
    cursor.close()







