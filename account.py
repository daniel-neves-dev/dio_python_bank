import textwrap

ADICIONAR_CLIENTE = 1
MOSTRAR_CLIENTES = 2
BUSCAR_CLIENTE = 3
DEPOSITAR = 4
SACAR = 5
EXTRATO = 6
SAIR = 7

def opcoes():
    print("\n===== NTT Sistema Bancário =====")
    print(f"[{ADICIONAR_CLIENTE}]Cadastrar novo cliente")
    print(f"[{MOSTRAR_CLIENTES}]Visualizar lista de clientes")
    print(f"[{BUSCAR_CLIENTE}]Procurar Cliente")
    print(f"[{DEPOSITAR}]Depositar")
    print(f"[{SACAR}]Sacar")
    print(f"[{EXTRATO}]Extrato")
    print(f"[{SAIR}]Sair")
    
    return int(input(textwrap.dedent('\nEscolha uma opção acima: ')))

def banco_dados_vazio(clientes):
    if not clientes:
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

def mostrar_clientes(clientes):
    print("\n====== Lista de Clientes ======")
    if not clientes:
        banco_dados_vazio(clientes)
        return
        
    clientes_ordenados = sorted(clientes, key=lambda x:x['nome'])

    for cliente in clientes_ordenados:
        print(f"\nNome: {cliente['nome']}\nCPF: {cliente['cpf']}")

def buscar_cliente(clientes):
    if not clientes:
        banco_dados_vazio(clientes)
        return

    cpf = input("Digite o número do CPF: ")

    for cliente in clientes:
        if cliente['cpf'] == cpf:
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

def efetuar_saque(*, valor, saldo, limite, limite_saques, extrato):
    if limite_saques == 0:
        print('\nLimite de saques diário atingido.')
        return saldo, extrato, limite, limite_saques

    if valor <= saldo:
        saldo -= valor
        limite_saques -= 1
        extrato += f"\nSaque:\tR${valor:.2f}"
        print(f"\nSaque realizado com sucesso!")
    elif (valor <= (limite + saldo)) and (limite > 0):
        limite_usado = valor - saldo
        limite -= limite_usado
        saldo = 0
        limite_saques -= 1
        extrato += f"\nSaque:\tR${valor:.2f}"
        print(f"\nSaque realizado com sucesso.\nFoi retirado R${limite_usado:.2f} do seu limite.")
    else:
        print("\nSaldo e limite insuficientes.")

    return saldo, extrato, limite, limite_saques

def mostrar_extrato(saldo, limite, limite_saques, *, extrato):
    print("\n===== Extrato =====")
    print(f"\nLimite disponível:\tR${limite:.2f}")
    
    if limite_saques == 2:
        print(f"\nVocê pode realizar {limite_saques} saques.")
    elif limite_saques == 1:
        print(f"\nVocê pode realizar somente mais 1 saque.")
    elif limite_saques == 0:
        print(f"\nVocê não pode realizar nenhum saque.")
    
    print("\nNenhuma transação realizada." if not extrato else extrato)
    print(f"\nSaldo:\tR${saldo:.2f}")
    print("===========================\n")

def sair():
    print('\nObrigado por utilizar o nosso sistema!\n')

def main():
    saldo = 0.0
    limite = 500.0
    extrato = ""
    limite_saques = 3
    clientes = []

    while True:
        escolha = opcoes()

        if escolha == ADICIONAR_CLIENTE:
            adicionar_cliente(clientes)
        
        elif escolha == MOSTRAR_CLIENTES:
            mostrar_clientes(clientes)
        
        elif escolha == BUSCAR_CLIENTE:
            buscar_cliente(clientes)

        elif escolha == DEPOSITAR:
            valor = float(input("\nDigite o valor a ser depositado: R$"))
            saldo, extrato, limite = depositar(valor, saldo, extrato, limite)

        elif escolha == EXTRATO:
            mostrar_extrato(saldo, limite, limite_saques,extrato=extrato)

        elif escolha == SACAR:
            valor = float(input("\nDigite o valor para efetuar o saque: R$"))
            saldo, extrato, limite, limite_saques = efetuar_saque(
                valor=valor,
                saldo=saldo,
                limite=limite,
                extrato=extrato,
                limite_saques=limite_saques
            )

        elif escolha == SAIR:
            sair()
            break

        else:
            print('\nEscolha uma opção válida.')

main()