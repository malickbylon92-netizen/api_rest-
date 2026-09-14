from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="ciel2027"
)

cursor = mydb.cursor()



@app.route('/v2/etudiants/', methods=['GET'])
def getEtudiants():

    try:
        etudiants = []

        req = "SELECT * FROM etudiant"

        cursor.execute(req)

        result = cursor.fetchall()

        for row in result:

            etudiant = {
                "idetudiant": row[0],
                "nom": row[1],
                "prenom": row[2],
                "email": row[3],
                "telephone": row[4]
            }

            etudiants.append(etudiant)

        return jsonify(etudiants), 200

    except Exception as e:
        return jsonify({'erreur': str(e)}), 500




@app.route('/v2/etudiants/<int:id>', methods=['GET'])
def getEtudiant(id):

    req = f"SELECT * FROM etudiant WHERE idetudiant = {id}"

    try:

        cursor.execute(req)

        row = cursor.fetchone()

        etudiant = {
            "idetudiant": row[0],
            "nom": row[1],
            "prenom": row[2],
            "email": row[3],
            "telephone": row[4]
        }

        return jsonify(etudiant), 200

    except TypeError:
        return jsonify({'erreur': 'id invalide'}), 404

    except Exception as e:
        return jsonify({'erreur': str(e)}), 500



@app.route('/v2/etudiants/', methods=['POST'])
def createEtudiant():

    try:

        nom = request.json['nom']
        prenom = request.json['prenom']
        email = request.json['email']
        telephone = request.json['telephone']

        req = f"""
        INSERT INTO etudiant (nom, prenom, email, telephone)
        VALUES ('{nom}', '{prenom}', '{email}', '{telephone}')

        """

        cursor.execute(req)

        mydb.commit()

        return jsonify({"message": "Ajout OK"}), 201

    except TypeError:
        return jsonify({'erreur': 'erreur il manque une information'}), 400




@app.route('/v2/etudiants/<int:id>', methods=['PUT'])
def updateEtudiant(id):

    try:

        nom = request.json['nom']
        prenom = request.json['prenom']
        email = request.json['email']
        telephone = request.json['telephone']

        req = f"""
        UPDATE etudiant
        SET nom='{nom}',
            prenom='{prenom}',
            email='{email}',
            telephone='{telephone}'
        WHERE idetudiant={id}
        """

        cursor.execute(req)

        if cursor.rowcount == 0:
            return jsonify({'erreur': 'id invalide'}), 404

        mydb.commit()

        return jsonify({"message": "Modification OK"}), 200

    except TypeError:
        return jsonify({'erreur': 'id invalide'}), 404

  




@app.route('/v2/etudiants/<int:id>', methods=['DELETE'])
def deleteEtudiant(id):

    try:

        req = f"DELETE FROM etudiant WHERE idetudiant={id}"

        cursor.execute(req)

        if cursor.rowcount == 0:
            return jsonify({'erreur': 'id invalide'}), 404

        mydb.commit()

        return jsonify({"message": "Suppression OK"}), 200

    except TypeError:
        return jsonify({'erreur': 'id invalide'}), 404

    

if __name__ == "__main__":
    app.run(debug=True)