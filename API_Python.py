from flask import Flask, jsonify, request
from functools import wraps
from firebird.driver import connect
from datetime import datetime

app = Flask(__name__)
USUARIO = "admin"
SENHA = "1234"

def autenticacao(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth = request.authorization

        if not auth:
            return jsonify({
                "Mensagem": "Autenticação necessária"
            }), 401

        if auth.username != USUARIO or auth.password != SENHA:
            return jsonify({
                "Mensagem": "Usuário ou senha inválidos"
            }), 401

        return f(*args, **kwargs)

    return decorated

def conexaoBanco():
    con = connect(
    database=r'192.168.0.188/3050:C:/BD/BANCO.FDB',
    user='SYSDBA',
    password='masterkey'
    )
    cursor = con.cursor()
    return con, cursor

def transformarGasto(linha):
        return {
            "id": linha[0],
            "nome": linha[1],
            "tipo": linha[2], 
            "valor": float(linha[3]),
            "pago": linha[4],
            "data_pagamento": linha[5],
            "data_vencimento": linha[6]
        }


@app.route("/ping")
def ping():
    return "pong"

@app.route("/gastos/listar", methods=["GET"])
@autenticacao
def listarGastos():
    con, cursor = conexaoBanco()
    print("Conectado com sucesso!\n" \
    "Rota: http://127.0.0.1:5000/gastos/listar")
    try:
        pagina = request.args.get("pagina", "1")
        id = request.args.get("id", "0")

        pagina = int(pagina) if pagina.strip() != "" else 1
        id = int(id) if id.strip() != "" else 0

    except ValueError:
        con.close()
        return jsonify({
            "Erro": "Os parâmetros pagina e id devem ser números inteiros"
        }), 400
    limite = 10
    inicio = ((pagina - 1) * limite) + 1
    fim = inicio + limite - 1
    
    if pagina == 0:
        return jsonify({
            "Error": "impossivel a pagina ser 0"
        }), 400

    if id == 0:
        cursor.execute("SELECT * FROM GASTOS ORDER BY ID ROWS ? TO ?", (inicio, fim))

        resultado = cursor.fetchall()

        if len(resultado) == 0:
            con.close()
            return jsonify({
                "OK": "Não há registros para listar..."
            }), 200
        
        else:

            gastos = []

            for linha in resultado:
                gastos.append(transformarGasto(linha))

            con.close()
            return jsonify(gastos)
    
    else:
        cursor.execute("SELECT * FROM GASTOS WHERE ID = ?", (id,))

        resultado = cursor.fetchone()
        if resultado is None:
            con.close()
            return jsonify({
                "OK": "Esse gasto não existe"
            }), 200
        else:
            gasto = transformarGasto(resultado)
            con.close

            return jsonify(gasto)

@app.route("/gastos/adicionar", methods=["POST"])
@autenticacao
def adicionarGasto():
    con, cursor = conexaoBanco()

    dados = request.get_json()

    nome = dados["nome"]
    tipo = dados["tipo"]
    valor = dados["valor"]
    data_pagamento = dados.get("data_pagamento")
    data_vencimento = dados.get("data_vencimento")

    if data_pagamento is not None:
        data_pagamento = datetime.strptime(
            data_pagamento,
            "%d/%m/%Y"
        ).date()

    if data_vencimento is not None:
        data_vencimento = datetime.strptime(
            data_vencimento,
            "%d/%m/%Y"
        ).date()

    cursor.execute("""
        INSERT INTO GASTOS (
            NOME,
            TIPO,
            VALOR,
            PAGO,
            DATA_PAGAMENTO,
            DATA_VENCIMENTO
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        nome,
        tipo,
        valor,
        False,
        data_pagamento,
        data_vencimento
    ))

    con.commit()
    con.close()

    return jsonify({
        "OK": "Gasto adicionado com sucesso!"
    }), 201

@app.route("/gastos/pagar", methods=["PUT"])
@autenticacao
def pagarGastos():
    con, cursor = conexaoBanco()
    print("Conectado com sucesso!\n" \
    "Rota: http://127.0.0.1:5000/gastos/pagar")
    
    dados = request.get_json()

    id = dados["id"]
    data_pagamento = dados.get("data_pagamento")

    if data_pagamento is not None:
        data_pagamento = datetime.strptime(
            data_pagamento,
            "%d/%m/%Y"
        ).date()

    cursor.execute("SELECT * FROM GASTOS WHERE ID = ?", (id,))
    resultado = cursor.fetchone()

    if resultado is None:
        con.close()
        return jsonify({
            "Mensagem": "Esse gasto não existe..."
        })
    else:
        cursor.execute("UPDATE GASTOS SET PAGO = ?, DATA_PAGAMENTO = ? WHERE ID = ?", (True, data_pagamento, id))
        con.commit()
        con.close()

        return jsonify({
            "OK": "Gasto pago com sucesso!"
        }), 201

@app.route("/gastos/alterar", methods=["PUT"])
@autenticacao
def alterarGastos():
    con, cursor = conexaoBanco()
    print("Conectado com sucesso!\n" \
    "Rota: http://127.0.0.1:5000/gastos/alterar")

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
            "OK": "Esse gasto não existe!"
        }), 200
    
    else: 
        nome = dados.get("nome", resultado[1])
        tipo = dados.get("tipo", resultado[2])
        valor = dados.get("valor", resultado[3])
        pago = dados.get("pago", resultado[4])
        data_pagamento = dados.get("data_pagamento", resultado[5])
        data_vencimento = dados.get("data_vencimento", resultado[6])

        if data_pagamento is not None:
            data_pagamento = datetime.strptime(
                data_pagamento,
                "%d/%m/%Y"
            ).date()

        if data_vencimento is not None:
            data_vencimento = datetime.strptime(
                data_vencimento,
                "%d/%m/%Y"
            ).date()

        cursor.execute("""
            UPDATE GASTOS
            SET
                NOME = ?,
                TIPO = ?,
                VALOR = ?,
                PAGO = ?,
                DATA_PAGAMENTO = ?,
                DATA_VENCIMENTO = ?
            WHERE ID = ?
        """, (nome, tipo, valor, pago, data_pagamento, data_vencimento, id))

        con.commit()
        con.close()

        return jsonify({
            "OK": "Gasto alterado com sucesso!"
        }), 201

@app.route("/gastos/excluir", methods=["DELETE"])
@autenticacao
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
            "OK": "Esse gasto não existe!"
        }), 200
    
    else:
        cursor.execute("""
            DELETE FROM GASTOS
                WHERE ID = ?
        """, (id,))

        con.commit()
        con.close()

        return jsonify({
            "OK": "Gasto deletado com sucesso!"
        }), 201
    

def transformarTarefa(linha):
    return {
        "id": linha[0],
        "descricao": linha[1],
        "importancia": linha[2],
        "status": linha[3],
        "data": linha[4],
    }

@app.route("/tarefas/listar", methods=["GET"])
@autenticacao
def listarTarfeas():
    con, cursor = conexaoBanco()
    print("Conectado com sucesso!\n" \
    "Rota: http://127.0.0.1:5000/tarefas/listar")
    try:
        pagina = request.args.get("pagina", "1")
        id = request.args.get("id", "0")

        pagina = int(pagina) if pagina.strip() != "" else 1
        id = int(id) if id.strip() != "" else 0

    except ValueError:
        con.close()
        return jsonify({
            "Erro": "Os parâmetros pagina e id devem ser números inteiros"
        }), 400
    
    limite = 10
    inicio = ((pagina - 1) * limite) + 1
    fim = inicio + limite - 1

    if pagina == 0:
        return jsonify({
            "Error": "impossivel a pagina ser 0"
        }), 400

    if id == 0:
        cursor.execute(
            """
            SELECT * FROM TAREFAS ORDER BY ID ASC ROWS ? TO ?
        """, (inicio, fim))

        resultado = cursor.fetchall()

        if len(resultado) == 0:
            con.close()
            return jsonify({
                "Mensagem": "Nenhuma tarefa encontrada"
            })
        else: 
            tarefas = []

            for linha in resultado:
                tarefa = transformarTarefa(linha)

                tarefas.append(tarefa)

            con.close()
            return jsonify(tarefas)
    else:
        cursor.execute("SELECT * FROM TAREFAS WHERE ID = ?", (id,))
        resultado = cursor.fetchone()

        if resultado is None:
            con.close()
            return jsonify ({
                "OK": "Essa tarefa não existe"
            }), 200
        else:
            tarefa = transformarTarefa(resultado)
            con.close

            return jsonify(tarefa)
    
@app.route("/tarefas/adicionar", methods=["POST"])
@autenticacao
def adicionarTarefa():
    con, cursor = conexaoBanco()
    print("Conectado com sucesso!\n" \
    "Rota: http://127.0.0.1:5000/tarefas/adicionar")

    dados = request.get_json()

    descricao = dados["descricao"]
    importancia = dados["importancia"]
    data = dados.get("data")

    if data is not None:
        data = datetime.strptime(
            data,
            "%d/%m/%Y"
        ).date()

    cursor.execute("""
       INSERT INTO TAREFAS (descricao, importancia, status, data) VALUES (?, ?, ?, ?)
""", (descricao, importancia, False, data))
    
    con.commit()
    
    con.close()
    return jsonify({
        "OK": "Tarefa Adicionada com sucesso!"
    }), 201

@app.route("/tarefas/alterar", methods=["PUT"])
@autenticacao
def alterarTarefa():
    con, cursor = conexaoBanco()
    print("Conectado com sucesso!\n" \
    "Rota: http://127.0.0.1:5000/tarefas/alterar")
    
    dados = request.get_json()

    id = dados["id"]

    cursor.execute("""
        SELECT * FROM TAREFAS
            WHERE ID = ?
""", (id,))
    
    resultado = cursor.fetchone()
    if resultado is None:
        con.close()
        return jsonify({
            "200": "Essa tarefa não existe"
        })
    else:
        descricao = dados.get("descricao", resultado[1])
        importancia = dados.get("importancia", resultado[2])
        status = dados.get("status", resultado[3])
        data = dados.get("data", resultado[4])
        if data is not None:
            data = datetime.strptime(
            data,
            "%d/%m/%Y"
        ).date()
        cursor.execute("""
            UPDATE TAREFAS
            SET
                DESCRICAO = ?,
                IMPORTANCIA = ?,
                STATUS = ?,
                DATA = ?
            WHERE ID = ?
        """, (descricao, importancia, status, data, id))

        con.commit()
        con.close()
        return jsonify({
            "OK": "Tarefa alterada com sucesso!"
        }), 201
    
@app.route("/tarefas/concluir", methods=["PUT"])
@autenticacao
def concluirTarefa():
    con, cursor = conexaoBanco()
    print("Conectado com sucesso!\n" \
    "Rota: http://127.0.0.1:5000/tarefas/concluir")

    dados = request.get_json()
    while True:
        try:
            id = int(dados.get("id"))
            break
        except (TypeError, ValueError):
            return jsonify({
                "Error": "id Invalido"
            }), 400
    
    cursor.execute("SELECT * FROM TAREFAS WHERE ID = ?", (id,))
    resultado = cursor.fetchone()

    if resultado is None:
        con.close()
        return jsonify({
            "OK": "Essa tarefa não existe"
        }), 200
    
    elif resultado[3] == True:
        con.close()
        return jsonify({
            "OK": "Essa tarefa já foi concluida!"
        }), 200

    else: 
        data = dados.get("data")
        if data == "":
            data = None
            
        if data is not None:
            data = datetime.strptime(
            data,
            "%d/%m/%Y"
        ).date()
        cursor.execute("""UPDATE TAREFAS
            SET
                STATUS = ?,
                DATA = ?
            WHERE ID = ?
        """, (True, data, id))

        con.commit()
        con.close()
        return jsonify({
            "OK": "Tarefa concluida com sucesso!"
        }), 201


@app.route("/tarefas/excluir", methods=["DELETE"])
@autenticacao
def excluirTarefa():
    con, cursor = conexaoBanco()
    print("Conectado com sucesso!\n" \
    "Rota: http://127.0.0.1:5000/tarefas/excluir")

    dados = request.get_json()

    id = dados["id"]

    cursor.execute("SELECT * FROM TAREFAS WHERE ID = ?", (id,))
    resultado = cursor.fetchone()
    if resultado is None:
        con.close()
        return jsonify({
            "OK": "Essa tarefa não existe"
        }), 200
    else: 
        cursor.execute("DELETE FROM TAREFAS WHERE ID = ?", (id,))

        con.commit()
        con.close()
        return jsonify({
            "OK": "Tarefa excluida com sucesso!"
        }), 201

app.run(host="0.0.0.0", port=5000, debug=False)