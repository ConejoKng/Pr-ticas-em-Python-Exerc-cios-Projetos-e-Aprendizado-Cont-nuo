from flask import Flask, jsonify, request
from firebird.driver import connect

app = Flask(__name__)

def conexaoBanco():
    con = connect(
    database=r'192.168.0.188/3050:C:/BD/BANCO.FDB',
    user='SYSDBA',
    password='masterkey'
    )
    cursor = con.cursor()
    return con, cursor



@app.route("/ping")
def ping():
    return "pong"

@app.route("/gastos/listar", methods=["GET"])
def listarGastos():
    con, cursor = conexaoBanco()
    print("Conectado com sucesso!\n" \
    "Rota: http://127.0.0.1:5000/gastos/listar")
    pagina = int(request.args.get("pagina", 1))
    limite = 10
    inicio = ((pagina - 1) * limite) + 1
    fim = inicio + limite - 1

    cursor.execute("SELECT * FROM GASTOS ORDER BY ID ROWS ? TO ?", (inicio, fim))

    resultado = cursor.fetchall()

    gastos = []

    for linha in resultado:
        gasto = {
            "id": linha[0],
            "nome": linha[1],
            "tipo": linha[2], 
            "valor": float(linha[3]),
            "pago": linha[4]
        }

        gastos.append(gasto)

    con.close()
    return jsonify(gastos)

@app.route("/gastos/listar/filtro", methods=["GET"])
def listarGastoFiltro():
    con, cursor = conexaoBanco()
    print("Conectado com sucesso!\n" \
    "Rota: http://127.0.0.1:5000/gastos/listar/filtro")

    dados = request.get_json()

    id = dados["id"]

    cursor.execute("""
       SELECT * FROM GASTOS
       WHERE ID = ?
""", (id,))
    
    resultado = cursor.fetchone()

    if resultado is None:
        con.close()
        return jsonify({
            "Mensagem": "Gasto não encontrado!"
        })
    
    else:
        gasto = {
            "id": resultado[0],
            "nome": resultado[1],
            "tipo": resultado[2],
            "valor": resultado[3],
            "pago": resultado[4]
        }

        con.close()
        return jsonify(gasto)
    


@app.route("/gastos/adicionar", methods=["POST"])
def adicionarGasto():
    con, cursor = conexaoBanco()
    print("Conectado com sucesso!\n" \
    "Rota: http://127.0.0.1:5000/gastos/adicionar")

    dados = request.get_json()

    nome = dados["nome"]
    tipo = dados["tipo"]
    valor = dados["valor"]

    cursor.execute("""
        INSERT INTO GASTOS (NOME, TIPO, VALOR, PAGO)
        VALUES (?, ?, ?, ?)
    """, (nome, tipo, valor, False))

    con.commit()
    con.close()

    return jsonify({
        "mensagem": "Gasto Adicionado com sucesso!"
    })

@app.route("/gastos/alterar", methods=["PUT"])
def alterarGastos():
    con, cursor = conexaoBanco()
    print("Conectado com sucesso!\n" \
    "Rota: http://127.0.0.1:5000/gastos/alterar")

    dados = request.get_json()

    id = dados["id"]
    nome = dados["nome"]
    tipo = dados["tipo"]
    valor = dados["valor"]
    pago = dados["pago"]

    cursor.execute("""
        SELECT * FROM GASTOS
            WHERE ID = ?
    """, (id,))

    resultado = cursor.fetchone()

    if resultado is None:
        con.close()
        return jsonify({
            "Mensagem": "Esse gasto não existe!"
        })
    
    else: 
        cursor.execute("""
            UPDATE GASTOS
            SET
                NOME = ?,
                TIPO = ?,
                VALOR = ?,
                PAGO = ?
            WHERE ID = ?
        """, (nome, tipo, valor, pago, id))

        con.commit()
        con.close()

        return jsonify({
            "Mensagem": "Gasto alterado com sucesso!"
        })

@app.route("/gastos/excluir", methods=["DELETE"])
def excluirGasto():
    con, cursor = conexaoBanco()
    print("Conectado com sucesso!\n" \
    "Rota: http://127.0.0.1:5000/gastos/excluir")

    dados = request.get_json()

    id = dados['id']

    cursor.execute("""
        SELECT * FROM GASTOS
            WHERE ID = ?
""", (id,))
    
    resultado = cursor.fetchone()

    if resultado is None:
        con.close()
        return jsonify({
            "Mensagem": "Esse gasto não existe!"
        })
    
    else:
        cursor.execute("""
            DELETE FROM GASTOS
                WHERE ID = ?
        """, (id,))

        con.commit()
        con.close()

        return jsonify({
            "Mensagem": "Gasto deletado com sucesso!"
        })

app.run(debug=False)

