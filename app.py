from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Configurações do banco de dados
db_config = {
    "host": "consulta_coaf.mysql.dbaas.com.br",
    "user": "consulta_coaf",
    "password": "Toriba@2023",
    "database": "consulta_coaf"
}

@app.route("/", methods=["GET", "POST"])
def index():
    resultados = []
    if request.method == "POST":
        busca_nome = request.form.get("nome")
        busca_cpf = request.form.get("cpf")

        # Conectar ao banco de dados MySQL
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor()

        # Executar uma consulta usando os valores inseridos
        query = "SELECT * FROM pessoas WHERE 1=1"
        query_params = []

        if busca_nome:
            query += " AND nome LIKE %s"
            query_params.append('%' + busca_nome + '%')
        if busca_cpf:
            query += " AND cpf LIKE %s"
            query_params.append('%' + busca_cpf + '%')

        cursor.execute(query, query_params)

        # Obter os resultados da consulta
        resultados = cursor.fetchall()

        # Fechar a conexão com o banco de dados
        cursor.close()
        db_connection.close()
        if not resultados:
            resultados = [("Não consta",)]

    return render_template("index.html", resultados=resultados)

if __name__ == "__main__":
    app.run(debug=True)