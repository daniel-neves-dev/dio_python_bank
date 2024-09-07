import textwrap

ADICIONAR_CLIENTE = 1
CRIAR_CONTA_CORRENTE = 2
MOSTRAR_CLIENTES = 3
BUSCAR_CLIENTE = 4
DEPOSITAR = 5
SACAR = 6
EXTRATO = 7
SAIR = 8

def opcoes():
    print("\n===== NTT Sistema Bancário =====")
    print(f"[{ADICIONAR_CLIENTE}]Cadastrar novo cliente")
    print(f"[{CRIAR_CONTA_CORRENTE}]Cadastrar Conta corrente")
    print(f"[{MOSTRAR_CLIENTES}]Visualizar lista de clientes")
    print(f"[{BUSCAR_CLIENTE}]Procurar Cliente")
    print(f"[{DEPOSITAR}]Depositar")
    print(f"[{SACAR}]Sacar")
    print(f"[{EXTRATO}]Extrato")
    print(f"[{SAIR}]Sair")
    
    return int(input(textwrap.dedent('\nEscolha uma opção acima: ')))


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
            

def mostrar_clientes(clientes, contas):
    print("\n====== Lista de Clientes ======")
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
            print("Nenhuma conta cadastrada para este cliente.")

def buscar_cliente(clientes):
    if not clientes:
        banco_dados_vazio(clientes)
        return

    cpf = input("Digite o número do CPF: ")

    cliente_cadastrado = [cliente for cliente in clientes if cliente['cpf'] == cpf]

    if cliente_cadastrado:
        for cliente in cliente_cadastrado:
                print(f"\nNome: {cliente['nome']}\nCPF: {cliente['cpf']}")
    else:
        print('Cliente não cadastrado')
        

def depositar(valor, saldo, extrato, limite):
    if valor > 0:
        if limite < 500:
            repor_limite = min(500 - limite, valor)
            limite += repor_limite
            saldo += (valor - repor_limite)
            extrato += f"\nDepósito: R${valor:.2f}"
            print(f"\nValor de R${valor:.2f}, depositado com sucesso.\n")
        else:
            saldo += valor
            extrato += f"\nDepósito: R${valor:.2f}"
            print(f"\nValor de R${valor:.2f}, depositado com sucesso.\n")
    else:
        print('\nO valor do depósito deve ser maior que zero.')

    return saldo, extrato, limite

def efetuar_saque(*, valor, saldo, limite,LIMITE_SAQUES, extrato):
    if LIMITE_SAQUES == 0:
        print('\nLimite de saques diário atingido.')
        return saldo, extrato, limite,LIMITE_SAQUES

    if valor <= saldo:
        saldo -= valor
        LIMITE_SAQUES -= 1
        extrato += f"\nSaque:\tR${valor:.2f}"
        print(f"\nSaque realizado com sucesso!")
    elif (valor <= (limite + saldo)) and (limite > 0):
        limite_usado = valor - saldo
        limite -= limite_usado
        saldo = 0
        LIMITE_SAQUES -= 1
        extrato += f"\nSaque:\tR${valor:.2f}"
        print(f"\nSaque realizado com sucesso.\nFoi retirado R${limite_usado:.2f} do seu limite.")
    else:
        print("\nSaldo e limite insuficientes.")

    return saldo, extrato, limite, LIMITE_SAQUES

def mostrar_extrato(saldo, limite, LIMITE_SAQUES, *, extrato):
    print("\n===== Extrato =====")
    print(f"\nLimite disponível:\tR${limite:.2f}")
    
    if LIMITE_SAQUES > 2:
        print(f"\nVocê pode realizar {LIMITE_SAQUES} saques.")
    elif LIMITE_SAQUES == 1:
        print(f"\nVocê pode realizar somente mais 1 saque.")
    elif LIMITE_SAQUES == 0:
        print(f"\nVocê não pode realizar nenhum saque.")
    
    print("\nNenhuma transação realizada." if not extrato else extrato)
    print(f"\nSaldo:\tR${saldo:.2f}")
    print("===========================\n")

def sair():
    print('\nObrigado por utilizar o nosso sistema!\n')

def main():
    AGENCIA = '0001'
    saldo = 0.0
    limite = 500.0
    extrato = ""
    LIMITE_SAQUES = 3
    clientes = []
    contas = []

    while True:
        escolha = opcoes()

        if escolha == ADICIONAR_CLIENTE:
            adicionar_cliente(clientes)
        
        elif escolha == CRIAR_CONTA_CORRENTE:
            numero_conta = len(contas) + 1
            conta = conta_corrente(AGENCIA, clientes, numero_conta)

            if conta:
                contas.append(conta)
        
        elif escolha == MOSTRAR_CLIENTES:
            mostrar_clientes(clientes, contas)
        
        elif escolha == BUSCAR_CLIENTE:
            buscar_cliente(clientes)

        elif escolha == DEPOSITAR:
            valor = float(input("\nDigite o valor a ser depositado: R$"))
            saldo, extrato, limite = depositar(valor, saldo, extrato, limite)

        elif escolha == EXTRATO:
            mostrar_extrato(saldo, limite, LIMITE_SAQUES,extrato=extrato)

        elif escolha == SACAR:
            valor = float(input("\nDigite o valor para efetuar o saque: R$"))
            saldo, extrato, limite, LIMITE_SAQUES = efetuar_saque(
                valor=valor,
                saldo=saldo,
                limite=limite,
                extrato=extrato,
                LIMITE_SAQUES=LIMITE_SAQUES
            )

        elif escolha == SAIR:
            sair()
            break

        else:
            print('\nEscolha uma opção válida.')

main()