import textwrap
from datetime import datetime
import pytz

ADICIONAR_CLIENTE = 1
CRIAR_CONTA_CORRENTE = 2
EXCLUIR_CONTA_CORRENTE = 3
MOSTRAR_CLIENTES = 4
LISTA_CONTAS = 5
BUSCAR_CLIENTE = 6
DEPOSITAR = 7
SACAR = 8
EXTRATO = 9
SAIR = 10

def opcoes():
    print("\n===== NTT Sistema Bancário =====")
    print(data_atual())
    print()
    print(f"[{ADICIONAR_CLIENTE}] Cadastrar novo cliente")
    print(f"[{CRIAR_CONTA_CORRENTE}] Cadastrar Conta corrente")
    print(f"[{EXCLUIR_CONTA_CORRENTE}] Encerrar conta corrente")
    print(f"[{MOSTRAR_CLIENTES}] Visualizar lista de clientes")
    print(f"[{LISTA_CONTAS}] Visualizar lista de contas")
    print(f"[{BUSCAR_CLIENTE}] Procurar Cliente")
    print(f"[{DEPOSITAR}] Depositar")
    print(f"[{SACAR}] Sacar")
    print(f"[{EXTRATO}] Extrato")
    print(f"[{SAIR}] Sair")
    
    return int(input(textwrap.dedent('\nEscolha uma opção acima: ')))


def data_atual():
    data = datetime.now(pytz.timezone("America/Sao_Paulo"))
    mascara_ptbr = "%d/%m/%Y - %H:%M"
    dataBR = data.strftime(mascara_ptbr)
    return dataBR

def banco_dados_vazio(clientes):
    print("\nNenhum cliente foi cadastrado")
    
def adicionar_cliente(clientes):
    cpf = input("Digite o CPF, somente números: ")

    for cliente in clientes:
        if cliente['cpf'] == cpf:
            print('Cliente já cadastrado')
            return

    nome = input("Digite o nome: ")

    clientes.append({"nome": nome, "cpf": cpf})
    print ("\nCliente cadastrado com sucesso")

def conta_corrente(AGENCIA, clientes, numero_conta):
    cpf = input("Digite o CPF, somente números: ")
    cliente_cadastrado = [cliente for cliente in clientes if cliente['cpf'] == cpf]

    if cliente_cadastrado:
        for cliente in cliente_cadastrado:
            adicionar_conta = input(f"Criar conta para {cliente['nome']}? [S/N]")
            if adicionar_conta.lower() == 's':
                print(f"Conta cadastrada com sucesso\nNúmero conta: {numero_conta}")
                return ({"AGENCIA": AGENCIA, "numero_conta": numero_conta, "cliente":cliente })
            else: return
    else:
        print('Cliente não cadastrado')

def encerrar_conta_corrente(contas):
    numero_conta = input("\nDigite o número da conta conrrente a ser encerrada: ")

    for conta in contas:
        if conta['numero_conta'] == int(numero_conta):
            print(f"\nConta Corrente: {conta['numero_conta']}\nCliente: {conta['cliente']['nome']} - CPF: {conta['cliente']['cpf']}")
            excluir_conta = input('Deseja encerrar esta conta corrente? [S/N]')
            if excluir_conta.lower() == 's':
                contas.remove(conta)
            print('\nConta encerrada com sucesso')
        else:
            print('\nConta não encontrada')
            return

def mostrar_clientes(clientes, contas):
    print("\n======= Lista de Clientes =======")
    if not clientes:
        banco_dados_vazio(clientes)
        return
        
    clientes_ordenados = sorted(clientes, key=lambda x:x['nome'])

    for cliente in clientes_ordenados:
        print(f"\nNome: {cliente['nome']}\nCPF: {cliente['cpf']}")
        
        contas_cliente = [conta for conta in contas if conta['cliente']['cpf'] == cliente['cpf']]
        if contas_cliente:
            for conta in contas_cliente:
                print(f"Agência: {conta['AGENCIA']} - Número da Conta: {conta['numero_conta']}")
        else:
            print("\nNenhuma conta cadastrada para este cliente.")

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
        banco_dados_vazio(clientes)
        return

    cpf = input("\nDigite o número do CPF: ")

    cliente_cadastrado = [cliente for cliente in clientes if cliente['cpf'] == cpf]

    if cliente_cadastrado:
        for cliente in cliente_cadastrado:
                print(f"\nNome: {cliente['nome']}\nCPF: {cliente['cpf']}")
                contas_cliente = [conta for conta in contas if conta['cliente']['cpf'] == cliente['cpf']]
                if contas_cliente:
                    for conta in contas_cliente:
                        print(f"\nAgência: {conta['AGENCIA']} - Número da Conta: {conta['numero_conta']}")
                else:
                    print("\nNenhuma conta cadastrada para este cliente.")
    else:
        print('\nCliente não cadastrado')
    
def depositar(valor, saldo, extrato, limite):
    
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
    obter_data_atual = data_atual()
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

        escolha = opcoes()

        if escolha == ADICIONAR_CLIENTE:
            adicionar_cliente(clientes)
        
        elif escolha == CRIAR_CONTA_CORRENTE:
            numero_conta = len(contas) + 1
            conta = conta_corrente(AGENCIA, clientes, numero_conta)

            if conta:
                contas.append(conta)

        elif escolha == EXCLUIR_CONTA_CORRENTE:        
            encerrar_conta_corrente(contas)

        elif escolha == LISTA_CONTAS:
            mostrar_lista_contas(contas)

        elif escolha == MOSTRAR_CLIENTES:
            mostrar_clientes(clientes, contas)
        
        elif escolha == BUSCAR_CLIENTE:
            buscar_cliente(clientes, contas)

        elif escolha == DEPOSITAR:
            if LIMITE_TRANSACOES == 0:
                print(f"\n*Você excedeu o limite de transações para a data de hoje.*")
            else:
                valor = float(input("\nDigite o valor a ser depositado: R$"))
                saldo, extrato, limite, = depositar(valor, saldo, extrato, limite)
                if valor > 0:
                    LIMITE_TRANSACOES -= 1
        
        elif escolha == SACAR:
            if LIMITE_TRANSACOES == 0:
                print(f"\n*Você excedeu o limite de transações para a data de hoje.*")
            else:
                valor = float(input("\nDigite o valor para efetuar o saque: R$"))
                saldo, extrato, limite, LIMITE_SAQUES = efetuar_saque(valor=valor, saldo=saldo, limite=limite, extrato=extrato, LIMITE_SAQUES=LIMITE_SAQUES)
                if valor > 0:
                    LIMITE_TRANSACOES -= 1

        elif escolha == EXTRATO:
            mostrar_extrato(saldo, limite, LIMITE_SAQUES, LIMITE_TRANSACOES, extrato=extrato)

        elif escolha == SAIR:
            sair()
            break

        else:
            print('\nEscolha uma opção válida.')

main()