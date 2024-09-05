import textwrap

ADICIONAR_CLIENTE = 1
DEPOSITAR = 2
SACAR = 3
EXTRATO = 4
SAIR = 5

def opcoes():
    print("===== NTT Sistema Bancário =====")
    print(f"[{ADICIONAR_CLIENTE}]Cadastrar novo cliente")
    print(f"[{DEPOSITAR}]Depositar")
    print(f"[{SACAR}]Sacar")
    print(f"[{EXTRATO}]Extrato")
    print(f"[{SAIR}]Sair")
    
    return int(input(textwrap.dedent('\nEscolha uma opção acima: ')))

def adicionar_cliente(clientes):
    nome = input("Digite o nome: ")
    cpf = input("Digite o CPF, somente números: ")
    
    clientes.append({"nome": nome, "cpf": cpf})
    print ("Cliente cadastrado com sucesso")


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
    print('\nObrigado por utilizar o nosso sistema!')

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

        if escolha == DEPOSITAR:
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