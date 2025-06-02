import os  # Biblioteca para interagir com o sistema operacional
from time import sleep  # Função para pausar a execução (usada ao sair)

# Nome do arquivo onde os dados das contas são armazenados
ARQUIVO_CONTAS = "contas.txt"

# Função para limpar o terminal (compatível com Windows e Unix)
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# Função que carrega as contas do arquivo de texto para uma lista de dicionários
def carregar_contas():
    contas = []
    try:
        with open(ARQUIVO_CONTAS, "r") as arquivo:
            for linha in arquivo:
                nome, cpf, saldo = linha.strip().split(",")  # Divide a linha nos dados
                contas.append({"nome": nome, "cpf": cpf, "saldo": float(saldo)})  # Converte saldo para float
    except FileNotFoundError:
        # Se o arquivo não existir, simplesmente retorna uma lista vazia
        pass
    return contas

# Função que salva a lista de contas no arquivo de texto
def salvar_contas(contas):
    with open(ARQUIVO_CONTAS, "w") as arquivo:
        for conta in contas:
            # Escreve os dados separados por vírgula, um por linha
            arquivo.write(f"{conta['nome']},{conta['cpf']},{conta['saldo']}\n")

# Função para criar uma nova conta, verificando se o CPF já existe
def criar_conta(nome, cpf, saldo_inicial):
    contas = carregar_contas()
    for conta in contas:
        if conta["cpf"] == cpf:
            print("\n❌ Já existe uma conta com esse CPF.")
            return  # Encerra se o CPF já estiver cadastrado
    contas.append({"nome": nome, "cpf": cpf, "saldo": saldo_inicial})
    salvar_contas(contas)
    print(f"\n✅ Conta criada com sucesso para {nome} (CPF: {cpf})!")

# Função para exibir todas as contas cadastradas
def listar_contas():
    contas = carregar_contas()
    if not contas:
        print("\n⚠️ Nenhuma conta encontrada.")
    else:
        print("\n📋 --- Contas Cadastradas ---")
        for conta in contas:
            print(f"👤 Titular: {conta['nome']} | CPF: {conta['cpf']} | Saldo: R${conta['saldo']:.2f}")

# Função para realizar depósito em uma conta pelo CPF
def depositar(cpf, valor):
    contas = carregar_contas()
    for conta in contas:
        if conta["cpf"] == cpf:
            conta["saldo"] += valor  # Adiciona o valor ao saldo
            salvar_contas(contas)
            print(f"\n💵 Depósito de R${valor:.2f} realizado com sucesso para {conta['nome']} (CPF: {cpf}).")
            return
    print("\n❌ Conta não encontrada.")  # CPF não localizado

# Função para realizar saque de uma conta, se houver saldo suficiente
def sacar(cpf, valor):
    contas = carregar_contas()
    for conta in contas:
        if conta["cpf"] == cpf:
            if conta["saldo"] >= valor:
                conta["saldo"] -= valor  # Subtrai o valor do saldo
                salvar_contas(contas)
                print(f"\n💸 Saque de R${valor:.2f} realizado com sucesso para {conta['nome']} (CPF: {cpf}).")
            else:
                print("\n❌ Saldo insuficiente.")  # Verifica saldo antes de sacar
            return
    print("\n❌ Conta não encontrada.")  # CPF não localizado

# Função principal com o menu de operações do sistema bancário
def menu():
    while True:
        limpar_tela()
        print("═" * 30)
        print("🏦  SISTEMA BANCÁRIO PYTHON  ")
        print("═" * 30)
        print("1️⃣  Criar conta")
        print("2️⃣  Listar contas")
        print("3️⃣  Depositar")
        print("4️⃣  Sacar")
        print("5️⃣  Sair")
        print("═" * 30)
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            try:
                nome = input("\nDigite o nome do titular: ")
                cpf = input("Digite o CPF (apenas números): ")
                saldo = float(input("Digite o saldo inicial: "))
                criar_conta(nome, cpf, saldo)
            except ValueError:
                print("\n❌ Valor inválido. Tente novamente.")  # Captura erro ao converter saldo

        elif opcao == "2":
            listar_contas()

        elif opcao == "3":
            cpf = input("\nDigite o CPF da conta para depósito: ")
            contas = carregar_contas()
            conta = next((c for c in contas if c["cpf"] == cpf), None)  # Busca conta pelo CPF
            if not conta:
                print("\n❌ Conta não encontrada.")
            else:
                try:
                    valor = float(input("Valor do depósito: "))
                    depositar(cpf, valor)
                except ValueError:
                    print("\n❌ Valor inválido. Tente novamente.")  # Captura erro na conversão do valor

        elif opcao == "4":
            cpf = input("\nDigite o CPF da conta para saque: ")
            contas = carregar_contas()
            conta = next((c for c in contas if c["cpf"] == cpf), None)
            if not conta:
                print("\n❌ Conta não encontrada.")
            else:
                try:
                    valor = float(input("Valor do saque: "))
                    sacar(cpf, valor)
                except ValueError:
                    print("\n❌ Valor inválido. Tente novamente.")

        elif opcao == "5":
            print("\n👋 Encerrando o sistema... Até logo!")
            sleep(1.5)  # Pausa de 1.5 segundos antes de encerrar
            break  # Encerra o loop

        else:
            print("\n❌ Opção inválida. Tente novamente.")  # Opção fora das permitidas

        input("\nPressione Enter para continuar...")  # Pausa para leitura do usuário

# Início do programa
menu()
