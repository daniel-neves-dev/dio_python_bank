def exibir_opcoes():
    print('''
[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair
    ''')
    escolher_opcao = int(input("Escolha uma opção acima: "))
    return escolher_opcao

def depositar(saldo, extrato):
    print(10* '=', 'Efetuar Deposito', 10*'=')

    depositar_valor = float(input('Digite o valor de deposito: R$ '))

    if depositar_valor <= 0:
        print('Valor negativo ou zero, não é possível efetuar depósito.')
        return

    saldo += depositar_valor
    extrato.append(f"Depósito: R${depositar_valor}")
    print(f"Deposito efetuado com sucesso, valor: R${depositar_valor}")
    return saldo, extrato

def efetuar_saque(saldo, limite_saque_diario, numero_saques_efetuados, extrato):
    print(10 * '=', 'Efetuar Saque', 10 * '=')

    valor_saque = float(input('Digite o valor a ser sacado: R$ '))

    if valor_saque <= 0:
        print('Valor negativo ou zero, não é possível efetuar depósito.')
        return
    elif valor_saque > saldo:
        print('Você não tem saldo suficiente.')
        return saldo, numero_saques_efetuados, extrato
    elif valor_saque > limite_saque_diario:
        print('Você não pode sacar acima de R$500.')
        return saldo, numero_saques_efetuados, extrato
    else:
        saldo -= valor_saque
        numero_saques_efetuados += 1
        extrato.append(f'Saque: R${valor_saque}')
        print('Saque efetuado com sucesso.')
        return saldo, numero_saques_efetuados, extrato

def exibir_extrato(extrato, saldo):
    if not extrato:
        print('Não foram realizadas transações.')
    else:
        for e in extrato:
            print(e)
    print(f'Saldo total: R${saldo}')

def main():
    saldo = 0.0
    limite_saque_diario = 500.0
    LIMITE_SAQUES = 3
    numero_saques_efetuados = 0
    extrato = []

    while True:
        print()
        print(10 * '=', 'NTT DATA Sistema Bancário', 10 * '=')
        escolha = exibir_opcoes()

        if escolha == 1:
            saldo, extrato = depositar(saldo, extrato)

        elif escolha == 2:
            if numero_saques_efetuados >= LIMITE_SAQUES:
                print('Você atingiu o limite de saques diários.')
                continue
            saldo, numero_saques_efetuados,extrato = (efetuar_saque
                                                      (saldo,limite_saque_diario,
                                                       numero_saques_efetuados, extrato))

        elif escolha == 3:
            exibir_extrato(extrato, saldo)

        elif escolha == 4:
            print('Obrigado por usar nosso sistema!!!')
            break

main()