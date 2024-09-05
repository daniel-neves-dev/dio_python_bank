DEPOSITAR = 1
SACAR = 2
EXTRATO = 3
SAIR = 4

def opcoes():
    print()
    print("=====NTT Sistema Bancario=====\n")
    print(f"{[DEPOSITAR]} Depositar")
    print(f"{[SACAR]} Sacar")
    print(f"{[EXTRATO]} Extrato")
    print(f"{[SAIR]} Sair")
    return int(input('\nEscolha uma opção acima: '))
print()

def depositar(valor, saldo, extrato, limite, /):
   
    if valor >= 0:
        if limite < 500:
            repor_limite = min(500 - limite, valor)
            limite += repor_limite
            saldo += (valor - repor_limite) 
            extrato += f"\nDepositado: ${valor:.2f}"
            print(f"\nValor de ${valor:.2f}, depositado com sucesso.")
        else:
            saldo += valor
            extrato += f"\nDepositado: ${valor:.2f}"
            print(f"\nValor de ${valor:.2f}, depositado com sucesso.")
    else:
        print('\nValor de depospito deve ser acima de zero')
    
    return saldo, extrato, limite

def sacar():
    global saldo
    global limite
    global extrato
    global WITHDRAW_limiteS 

    valor = float(input("\nType the valor withdraw: $"))

    if WITHDRAW_limiteS == 0:
        print('\nTransitions limite made')
        return

    if valor <= saldo:
        saldo -= valor
        WITHDRAW_limiteS -= 1
        extrato += f"\nWithdrawn: ${valor:.2f}"
        print(f"\nvalor: ${valor:.2f} withdraw.")

    elif (valor <=  limite + saldo) and (limite > 0):
        limite_used = (valor - saldo)
        limite -= limite_used
        saldo = 0
        WITHDRAW_limiteS -= 1
        extrato += f"\nWithdrawn: ${valor:.2f}"
        print(f"\nvalor: ${(valor):.2f} withdrawn using limite.")

    else:
        print("\nNot enough limite.")
    
        
def mostar_extrato(saldo, limite, /, *, extrato):

    print("\n=====Extrato=====")
    
    print(f"\nValor do limite disponível: R${limite:.2f}")

    print("\nNão foi realizado nenhuma transação hoje." if extrato == " " else extrato)
    print()
    print(f"\nSaldo: ${saldo:.2f}\n")
    print("===========================\n")

def sair():
    return print('\nObrigado por utilizar o nosso sistema!!!\n')


def main():
    saldo = 0.0
    limite = 500.0
    extrato = ""
    NUMERO_SAQUES = 3

    escolha = opcoes()

    while True:

        if escolha == DEPOSITAR:
            valor = float(input("\nDigite o valor a ser depositatdo: R$"))
            saldo, extrato, limite = depositar(valor, saldo, extrato, limite)

        elif escolha == SACAR:
            sacar()

        elif escolha == EXTRATO:
            mostar_extrato(saldo, limite, extrato=extrato)

        elif SAIR:
            sair()
            break

        else:
            print('\nEscolha uma opção valída')

        escolha = opcoes()
    
main()