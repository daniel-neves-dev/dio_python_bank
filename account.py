import textwrap
from datetime import datetime
import pytz

MENU_OPCOES = {
"ADICIONAR_CLIENTE": 1,
"CRIAR_CONTA_CORRENTE": 2,
"EXCLUIR_CONTA_CORRENTE": 3,
"MOSTRAR_CLIENTES": 4,
"EXCLUIR_CLIENTES": 5,
"LISTA_CONTAS": 6,
"BUSCAR_CLIENTE": 7,
"DEPOSITAR": 8,
"SACAR": 9,
"EXTRATO": 10,
"SAIR": 11
}

def mostras_opcoes():
    print("\n===== NTT Sistema Bancário =====")
    print(data_atual())
    print()
    
    for opcao, numero in MENU_OPCOES.items():
        print(f"[{numero}] {opcao.replace('_', ' ').title()}")
    
    return int(input('\nEscolha uma opção acima: '))

def data_atual():
    return datetime.now(pytz.timezone("America/Sao_Paulo")).strftime("%d/%m/%Y - %H:%M:%S")

def obter_clinte_cpf(clientes, cpf):
    cliente_cadastrado = [cliente for cliente in clientes if cliente['cpf'] == cpf]
    return cliente_cadastrado 
    
def adicionar_cliente(clientes):
    print("\n======= Cadastrar Cliente =======")
    cpf = input("\nDigite o CPF, somente números: ")

    if obter_clinte_cpf(clientes, cpf):
        print("\nClinte já cadastrado")
        return

    nome = input("\nDigite o nome completo: ")
    data_nascimento = input("\nInforme a data de nascimento (dd/mm/aaaa): ")
    endereco = input("\nInforme o endereço : Logradouro - Número - Bairro - Cidade/sigla:  Estado/sigla: ")

    clientes.append({"nome": nome, "cpf": cpf, "data_nascimento": data_nascimento, "endereco": endereco})
    print ("\nCliente cadastrado com sucesso")

def adicionar_conta_corrente(AGENCIA, clientes, numero_conta):

    print("\n======= Adicionar Conta Corrente =======")

    cpf = input("\nDigite o CPF, somente números: ")

    cliente_cadastrado = obter_clinte_cpf(clientes, cpf)

    if not cliente_cadastrado:
        print("\nClinte não cadastrado")
    
    for cliente in cliente_cadastrado:
        adicionar_conta = input(f"\nCriar conta para {cliente['nome']}? [S/N]")
        if adicionar_conta.lower() == 's':
            print(f"\nConta cadastrada com sucesso\nNúmero conta: {numero_conta}")
            return ({"AGENCIA": AGENCIA, "numero_conta": numero_conta, "cliente":cliente })
        elif adicionar_conta.lower() == 'n':
            print('\nOperação cancelada')
            return
        else:
            print('\nDigite uma opção valída')

def encerrar_conta_corrente(contas, clientes):
    print("\n======= Encerrar Conta Corrente =======")

    cpf = input("\nDigite o número do CPF: ")

    cliente_cadastrado = obter_clinte_cpf(clientes, cpf)

    if not cliente_cadastrado:
        print('\nCliente não cadastrado')
        return

    if cliente_cadastrado:
        for cliente in cliente_cadastrado:
            print(f"\nNome: {cliente['nome']}\nCPF: {cliente['cpf']}")
            contas_cliente = [conta for conta in contas if conta['cliente']['cpf'] == cliente['cpf']]
            if contas_cliente:
                for conta in contas_cliente:
                    print(f"\nAgência: {conta['AGENCIA']} - Número da Conta: {conta['numero_conta']}")
        
        numero_conta = input("\nDigite o número da conta conrrente a ser encerrada: ")

        for conta in contas:
            if conta['numero_conta'] == int(numero_conta):
                excluir_conta = input('Deseja encerrar esta conta corrente? [S/N]')
                if excluir_conta.lower() == 's':
                    contas.remove(conta)
                print('\nConta encerrada com sucesso')
                return
            
        print('\nConta não encontrada')  

def mostrar_clientes(clientes, contas):
    print("\n======= Lista de Clientes =======")
    if not clientes:
        print("\nNenhum cliente foi cadastrado")
        return
        
    clientes_ordenados = sorted(clientes, key=lambda x:x['nome'])

    for cliente in clientes_ordenados:
        print(f"\nNome: {cliente['nome']}\nCPF: {cliente['cpf']}\nData Nascimento: {cliente['data_nascimento']}")
        
        contas_cliente = [conta for conta in contas if conta['cliente']['cpf'] == cliente['cpf']]
        if contas_cliente:
            for conta in contas_cliente:
                print(f"Agência: {conta['AGENCIA']} - Número da Conta: {conta['numero_conta']}")
        else:
            print("\nNenhuma conta cadastrada para este cliente.")

def excuir_clientes(clientes, contas):
    print("\n========== Excluir Cliente ==========")
    if not clientes:
        print("\nNenhum cliente foi cadastrado")
        return

    cpf = input("\nDigite o número do CPF: ")

    cliente_cadastrado = obter_clinte_cpf(clientes, cpf)

    if not cliente_cadastrado:
        print('\nCliente não cadastrado')
        return
    
    if cliente_cadastrado:
        for cliente in cliente_cadastrado:
            print(f"\nNome: {cliente['nome']}\nCPF: {cliente['cpf']}")
            excuir_cliente = input('Deseja deletear este cliente do sistema? [S/N]')
            if excuir_cliente.lower() == 's':
                contas_cliente = [conta for conta in contas if conta['cliente']['cpf'] == cliente['cpf']]
                for conta in contas_cliente:
                    contas.remove(conta)
                clientes.remove(cliente)
                print('\nCliente, e contas corrente, removido com sucesso')
                return      

def mostrar_lista_contas(contas):
    print("\n======= Lista de Contas =======")

    for conta in contas:
        lista = f""" 
            Agência: {conta['AGENCIA']}
            Conta Corrente: {conta['numero_conta']}
            Cliente: {conta['cliente']['nome']} - CPF: {conta['cliente']['cpf']}
        """
        print(textwrap.dedent(lista))
    print("\n------------------------------")

def buscar_cliente(clientes, contas):
    print("\n========== Cliente ==========")
    if not clientes:
        print("Cliente não cadastrado")
        return

    cpf = input("\nDigite o número do CPF: ")

    cliente_cadastrado = obter_clinte_cpf(clientes, cpf)

    if cliente_cadastrado:
        for cliente in cliente_cadastrado:
            print(f"\nNome: {cliente['nome']}\nCPF: {cliente['cpf']}\nData Nascimento: {cliente['data_nascimento']}")
            print(f"\nEndereço: {cliente['endereco']}")
            contas_cliente = [conta for conta in contas if conta['cliente']['cpf'] == cliente['cpf']]
            if contas_cliente:
                for conta in contas_cliente:
                    print(f"\nAgência: {conta['AGENCIA']} - Número da Conta: {conta['numero_conta']}")
            else:
                print("\nNenhuma conta cadastrada para este cliente.")
    else:
        print('\nCliente não cadastrado')
    
def depositar(valor, saldo, extrato, limite):
    print("\n======= Efetuar Depósito =======")
    
    if valor <= 0:
        print('\nO valor do depósito deve ser maior que zero.')
        return saldo, extrato, limite
    
    if limite < 500:
        repor_limite = min(500 - limite, valor)
        limite += repor_limite
        saldo += (valor - repor_limite)
        extrato += f"\n{data_atual()} - Crédito: R${valor:.2f}"
        print(f"\nValor de R${valor:.2f}, foi creditado na sua conta.\n")
    else:
        saldo += valor
        extrato += f"\n{data_atual()} - Crédito: R${valor:.2f}"
        print(f"\nValor de R${valor:.2f}, foi creditado na sua conta.\n")

    return saldo, extrato, limite

def efetuar_saque(*, valor, saldo, limite, extrato, LIMITE_SAQUES):
    print("\n======= Efetuar Saque =======")
    
    if LIMITE_SAQUES == 0:
        print('\n*Limite de saques diário atingido.*')
        return saldo, extrato, limite, LIMITE_SAQUES
    
    if valor <= 0:
        print('\n*O valor do saque deve ser maior que zero.*')
        return saldo, extrato, limite, LIMITE_SAQUES

    if valor <= saldo:
        saldo -= valor
        LIMITE_SAQUES -= 1
        extrato += f"\n{data_atual()} - Débito: R${valor:.2f}"
        print(f"\nSaque realizado com sucesso!")
    elif (valor <= (limite + saldo)) and (limite > 0):
        limite_usado = valor - saldo
        limite -= limite_usado
        saldo = 0
        LIMITE_SAQUES -= 1
        extrato += f"\n{data_atual()} - Débito: R${valor:.2f}"
        print(f"\nSaque realizado com sucesso.\nFoi debitado R${limite_usado:.2f} do seu limite.")
    else:
        print("\n*Saldo e limite insuficientes.*")

    return saldo, extrato, limite, LIMITE_SAQUES

def mostrar_extrato(saldo, limite, LIMITE_SAQUES, LIMITE_TRANSACOES, *, extrato):
    print("\n============ Extrato ============")

    print(f"\nLimite disponível:\tR${limite:.2f}")

    if LIMITE_SAQUES >= 2:
        print(f"\nVocê pode realizar {LIMITE_SAQUES} saques.")
    elif LIMITE_SAQUES == 1:
        print(f"\nVocê pode realizar somente mais uma saque.")
    elif LIMITE_SAQUES == 0:
        print(f"\n*Você excedeu o limite de saques para a data de hoje.*")        
    
    if LIMITE_TRANSACOES >= 2:
        print(f"\nVocê pode realizar {LIMITE_TRANSACOES} transações.")
    elif LIMITE_TRANSACOES == 1:
        print(f"\nVocê pode realizar somente mais uma transação.")
    elif LIMITE_TRANSACOES == 0:
        print(f"\n*Você excedeu o limite de transações para a data de hoje.*")
    
    print("\nNenhuma transação realizada." if not extrato else extrato)
    print(f"\nSaldo:\tR${saldo:.2f}")
    print("\n=================================")

def sair():
    print('\nObrigado por utilizar o nosso sistema!\n')

def resetar_limites_diarios(LIMITE_SAQUES, LIMITE_TRANSACOES, data_ultima_transacao):
    obter_data_atual = data_atual().split(" ")[0]
    if obter_data_atual != data_ultima_transacao:
        return 3, 5, obter_data_atual
    return LIMITE_SAQUES, LIMITE_TRANSACOES, data_ultima_transacao

def main():
    AGENCIA = '0001'
    LIMITE_SAQUES = 3
    LIMITE_TRANSACOES = 5
    saldo = 0.0
    limite = 500.0
    extrato = ""
    clientes = []
    contas = []
    data_ultima_transacao = data_atual()

    while True:

        LIMITE_SAQUES, LIMITE_TRANSACOES, data_ultima_transacao = resetar_limites_diarios(LIMITE_SAQUES, LIMITE_TRANSACOES, data_ultima_transacao)

        escolha = mostras_opcoes()

        if escolha == MENU_OPCOES["ADICIONAR_CLIENTE"]:
            adicionar_cliente(clientes)
        
        elif escolha == MENU_OPCOES["CRIAR_CONTA_CORRENTE"]:
            numero_conta = len(contas) + 1
            conta = adicionar_conta_corrente(AGENCIA, clientes, numero_conta)

            if conta:
                contas.append(conta)

        elif escolha == MENU_OPCOES["EXCLUIR_CONTA_CORRENTE"]:        
            encerrar_conta_corrente(contas, clientes)

        elif escolha == MENU_OPCOES["LISTA_CONTAS"]:
            mostrar_lista_contas(contas)

        elif escolha == MENU_OPCOES["MOSTRAR_CLIENTES"]:
            mostrar_clientes(clientes, contas)
        
        elif escolha == MENU_OPCOES["BUSCAR_CLIENTE"]:
            buscar_cliente(clientes, contas)

        elif escolha == MENU_OPCOES["EXCLUIR_CLIENTES"]:
            excuir_clientes(clientes, contas)

        elif escolha == MENU_OPCOES["DEPOSITAR"]:
            if LIMITE_TRANSACOES == 0:
                print(f"\n*Você excedeu o limite de transações para a data de hoje.*")
            else:
                valor = float(input("\nDigite o valor a ser depositado: R$"))
                saldo, extrato, limite, = depositar(valor, saldo, extrato, limite)
                if valor > 0:
                    LIMITE_TRANSACOES -= 1
        
        elif escolha == MENU_OPCOES["SACAR"]:
            if LIMITE_TRANSACOES == 0:
                print(f"\n*Você excedeu o limite de transações para a data de hoje.*")
            else:
                valor = float(input("\nDigite o valor para efetuar o saque: R$"))
                saldo, extrato, limite, LIMITE_SAQUES = efetuar_saque(valor=valor, saldo=saldo, limite=limite, extrato=extrato, LIMITE_SAQUES=LIMITE_SAQUES)
                if valor > 0:
                    LIMITE_TRANSACOES -= 1

        elif escolha == MENU_OPCOES["EXTRATO"]:
            mostrar_extrato(saldo, limite, LIMITE_SAQUES, LIMITE_TRANSACOES, extrato=extrato)

        elif escolha == MENU_OPCOES["SAIR"]:
            sair()
            break

        else:
            print('\nEscolha uma opção válida.')

main()