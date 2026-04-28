import os

def limparTela():
    os.system('cls') 


def programa():
    while True:
        limparTela()
        while True:
            try:
                opcao = int(input("Escolha o sistema:\n" \
                "1 - Gerenciador de gastos\n" \
                "2 - Gerenciador de Tarefas\n" \
                "3 - Sair\n" \
                "Respostas: "))
                if opcao < 1 or opcao > 3:
                    print("Opção invalida")
                else:
                    break
            except ValueError:
                print("Opção invalida")

        if opcao == 1:
            gerenciadorGastos()
        
        elif opcao == 2:
            gerenciadorTarefas()
        
        else:
            print("Encerrando Aplicação")
            exit()


def gerenciadorGastos():
    gastos = []
    categorias = [
        "Moradia",
        "Alimentação",
        "Transporte",
        "Saúde",
        "Educação",
        "Lazer",
        "Serviços",
        "Compras",
        "Investimentos",
        "Dívidas"
        ]

    def msg():
        print("Use numeros inteiros!")

    def adicionarGasto():
        limparTela()
        while True:
            try:
                quantidade = int(input("Quantos Gastos deseja Adicionar?: "))
                break
            except ValueError:
                msg()
        for i in range(quantidade):
            print("====================")
            nome = input(f"{i + 1} - Nome do gasto: ")
            print("Qual o tipo do gasto?: ")
            for i in range(len(categorias)):
                print(f"{i + 1} - {categorias[i]}")
            while True:
                try:
                    escolha = int(input(f"Digite o numero do gasto: "))
                    if escolha < 1 or escolha > len(categorias):
                        print("Opção Invalida!")
                    else:
                        break
                except ValueError:
                    print("Use numeros inteiros!")
            tipo = categorias[escolha - 1]
            while True:
                try:
                    valor = float(input(f"{i + 1} - Quanto custou?: "))
                    break
                except ValueError:
                    print("Não pode conter letras nem caracteres especiais")
            gasto = {
                "nome": nome,
                "tipo": tipo,
                "valor": valor,
                "pago": False
            }
            gastos.append(gasto)
        print("Gastos adicionados com sucesso!")
        input("Pressione ENTER para continuar...")

    def listarGastos():
        limparTela()
        if len(gastos) == 0:
            print("Não existe gastos!")
        else:
            for i, gasto in enumerate(gastos):
                print("====================")
                print(f"ID: {1 + i}")
                print(f"Nome: {gasto['nome']}")
                print(f"Tipo: {gasto['tipo']}")
                print(f"Valor: {gasto['valor']}")
                print(f"Pago: {'Sim' if gasto['pago'] else 'Não'}")
                print("====================")
        input("Pressione ENTER para continuar...")

    def marcarPago():
        limparTela()
        listarGastos()
        if len(gastos) == 0:
            return
        else:
            while True:
                try:
                    id = int(input("Qual é o ID do gasto que deseja pagar?: "))
                    if id - 1 < 0 or id - 1 >= len(gastos):
                        print("Esse ID não existe")
                    else:
                        break
                except ValueError:
                    print("ID invalido")
            gastos[id - 1]['pago'] = True
            print("Gasto pago com sucesso!")
            input("Pressione ENTER para continuar...")

    def excluirgasto():
        limparTela()
        listarGastos()
        if len(gastos) == 0:
            return
        else:
            while True:
                try:
                    id = int(input("Qual é o ID do gasto que deseja excluir?: "))
                    if id - 1 < 0 or id - 1 >= len(gastos):
                        print("Esse ID não existe")
                    else:
                        break
                except ValueError:
                    print("ID invalido")
            gastos.pop(id - 1)
            print("Gasto excluido com sucesso!")
            input("Pressione ENTER para continuar...")
    
    def calcularGasto():
        limparTela()
        while True:
            while True: 
                try:
                    opcao = int(input("Escolha uma opção: \n" \
                    "1 - Calcular Soma\n" \
                    "2 - Filtrar por categorias\n" \
                    "3 - Calcular Media\n" \
                    "4 - Voltar\n" \
                    "Resposta: "))
                    if opcao < 1 or opcao > 4:
                        print("Opção invalida!")
                    else:
                        break
                except ValueError:
                    print("Use somente numeros inteiros!")
            
            if opcao == 1:
                print("=====Calcular Soma=====")
                totalSoma = 0
                for gasto in gastos:
                    totalSoma += gasto['valor']
                print(f"O seu total de gastos foi: {totalSoma}")
                totalSoma = 0
                input("Pressione ENTER para continuar...")
                limparTela()

            elif opcao == 2:
                totalCategorias = {}

                for gasto in gastos:
                    categoria = gasto['tipo']
                    valor = gasto['valor']

                    if categoria not in totalCategorias:
                        totalCategorias[categoria] = valor
                    else:
                        totalCategorias[categoria] += valor

                for categoria, total in totalCategorias.items():
                    print(f"{categoria}: {total}")

                input("Pressione ENTER para continuar...")
                limparTela()


            elif opcao == 3:
                print("=====Calcular Media=====")
                media = 0
                for gasto in gastos:
                    media += gasto['valor'] / len(gastos)
                print(f"A sua media de gastos foi: {media}")
                media = 0
                input("Pressione ENTER para continuar...")
                limparTela()
            
            else:
                break

    def principal():
        while True:
            limparTela()
            print("=====Gerenciador de Gastos=====")
            while True:
                try:
                    opcao = int(input("Selecione uma opção: \n" \
                    "1 - Adicionar gasto\n" \
                    "2 - Listar Gastos\n" \
                    "3 - Marcar como pago\n" \
                    "4 - Remover gasto\n" \
                    "5 - Calcular Gastos\n" \
                    "6 - Sair\n" \
                    "Resposta: "))
                    break
                except ValueError:
                    msg()

            if opcao == 1:
                adicionarGasto()

            elif opcao == 2:
                listarGastos()

            elif opcao == 3:
                marcarPago()

            elif opcao == 4:
                excluirgasto()

            elif opcao == 5:
                calcularGasto()

            elif opcao == 6:
                print("Encerrando o sistema...")
                break

            else:
                print("Opção invalida!")

    principal()


def gerenciadorTarefas():
    tarefas = []
    importancias = [
        "Alta",
        "Media",
        "Baixa"
    ]

    def incluirTarefa():
        limparTela()
        while True:
            try:
                quantidade = int(input("Quantas tarefas você quer adicionar: "))
                break
            except ValueError:
                print("Escreva numeros inteiros!")
        for i in range(quantidade):
            print("====================")
            descricao = input("Descrição: ")
            print("Qual a importancia?: ")
            for i in range(len(importancias)):
                print(f"{i + 1} - {importancias[i]}")
            while True:
                try:
                    importancia = int(input("Importanca: "))
                    if importancia < 1 or importancia > len(importancias):
                        print("Opção invalida!")
                    else:
                        break
                except ValueError:
                    print("Use numeros inteiros")
            status = False
            tarefa = {
                'descricao': descricao,
                'importancia': importancias[importancia - 1],
                'status': status
            }
            tarefas.append(tarefa)
        print("Terefas adicionadas com sucesso!")
        input("Pressione ENTER para continuar...")

    def listarTarefas():
        limparTela()
        if len(tarefas) == 0:
            print("Não existe tarefas.")
        else:
            for i, tarefa in enumerate(tarefas):
                print("====================")
                print(f"ID tarefa: {i + 1}")
                print(f"Descrição: {tarefa['descricao']}")
                print(f"Importancia: {tarefa['importancia']}")
                print(f"Status: {'Concluida' if tarefa['status'] else 'Pendente'}")
                print("====================")
        input("Pressione ENTER para continuar...")

    def marcarConcluida():
        limparTela()
        listarTarefas()
        if len(tarefas) == 0:
            return
        else:
            while True:
                try:
                    id = int(input("Digite o ID da tarefa que deseja Concluir: "))
                    if id - 1 < 0 or id - 1 >= len(tarefas):
                        print("ID Invalido!")
                    else:
                        break
                except ValueError:
                    print("Use numeros inteiros")
            
            tarefas[id - 1]['status'] = True
            print("Tarefa concluida com sucesso!")
            input("Pressione ENTER para continuar...")

    def excluirTarefa():
        limparTela()
        listarTarefas()
        if len(tarefas) == 0:
            return
        else:
            while True:
                try:
                    id = int(input("Digite o ID da tarefa que deseja excluir: "))
                    if id - 1 < 0 or id - 1 >= len(tarefas):
                        print("ID Invalido!")
                    else:
                        break
                except ValueError:
                    print("Use numeros inteiros")

            tarefas.pop(id - 1)
            print("Tarefa excluida com sucesso!")
            input("Pressione ENTER para continuar...")

    def principal():
        while True:
            limparTela()
            print("=====Gerenciador de Tarefas=====")
            while True:
                try:
                    opcao = int(input("Escolha uma opção:\n" \
                    "1 - Incluir tarefa\n" \
                    "2 - Listar Tarefas\n" \
                    "3 - Marcar como concluida\n" \
                    "4 - Excluir tarefa\n" \
                    "5 - Sair\n" \
                    "Resultado: "))
                    if opcao < 0 or opcao > 5:
                        print("Opção Invalida!")
                    else:
                        break
                except ValueError:
                    print("Use numeros inteiros!")

            if opcao == 1:
                incluirTarefa()

            elif opcao == 2:
                listarTarefas()

            elif opcao == 3:
                marcarConcluida()
            
            elif opcao == 4:
                excluirTarefa()
            
            elif opcao == 5:
                break
        
    principal()


programa()