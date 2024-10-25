from datetime import datetime
from logging import exception
from time import process_time_ns

import pytz

opcoes = {
    'cadastrar_cliente':1,
    'exibir_lista_clientes': 2,
    'procurar_cliente': 3,
    'deletar_cliente': 4,
    'cadastrar_conta_corrente': 5,
    'exibir_lista_de_contas': 6,
    'excluir_conta_corrente':7,
    'efetuar_deposito': 8,
    'efetuar_saque': 9,
    'extrato': 10,
    'sair': 11
}

def exibir_opcoes():
    for opcao, numero in opcoes.items():
        print(f"{numero} - {opcao.replace('_', ' ').title()}")

    escolher_opcao = int(input("\nEscolha uma opção acima: "))
    return escolher_opcao

def data_atual():
    return datetime.now(pytz.timezone("America/Sao_Paulo")).strftime("%d/%m/%Y - %H:%M:%S")

def verificar_cpf(lista_clientes, cpf_cliente):
    clientes_cadastrado = [cliente for cliente in lista_clientes if cliente['cpf'] == cpf_cliente]
    return clientes_cadastrado

def verificar_contas_cliente(cliente, contas):
    contas_cliente = [conta for conta in contas if conta['cliente']['cpf'] == cliente['cpf']]
    if contas_cliente:
        for conta in contas_cliente:
            print(f"Agência: {conta['AGENCIA']} - Número da conta: {conta['numero_conta']}")
    else:
        print(f"{cliente['nome']}, não possui nenhuma conta cadastrada")

def cadastrar_cliente(lista_clientes):
    print()
    print(10 * '=', 'Cadastro de Clientes', 10 * '=')

    cpf_cliente = input('Digite o CPF (somente números): ')
    if not cpf_cliente.isdigit():
        print('Digite números inteiros.')
        return

    cliente_cadastrado = verificar_cpf(lista_clientes, cpf_cliente)
    if cliente_cadastrado:
        print('Cliente já cadastro!')
        return

    cliente_nome = input('Digite o nome do cliente: ')
    print(f'Cliente {cliente_nome} cadastrado com sucesso!')
    lista_clientes.append({'nome': cliente_nome.title(), 'cpf':cpf_cliente})

def exibir_lista_clientes(lista_clientes, contas):
    print()
    print(10 * '=', 'Lista de Clientes', 10 * '=')

    if not lista_clientes:
        print('Nenhum cliente cadastrado.')
        return

    clientes_ordenados = sorted(lista_clientes, key= lambda item:item['nome'])

    for cliente in clientes_ordenados:
        print(50 * '-')
        print(f"Nome: {cliente['nome']} - CPF:{cliente['cpf']}")
        verificar_contas_cliente(cliente, contas)

def procurar_cliente(lista_clientes, contas):
    print()
    print(10 * '=', 'Procurar Cliente', 10 * '=')

    cpf_cliente = input('Digite o CPF (somente números): ')
    if not cpf_cliente.isdigit():
        print('Digite números inteiros.')
        return

    cliente_cadastrado = verificar_cpf(lista_clientes, cpf_cliente)
    if not cliente_cadastrado:
        print('Cliente não encontrado!')
        return

    for cliente in cliente_cadastrado:
        print(f"Nome: {cliente['nome']}")
        verificar_contas_cliente(cliente, contas)

def deletar_cliente(lista_clientes, contas):
    print()
    print(10 * '=', 'Deletar Cliente', 10 * '=')

    cpf_cliente = input('Digite o CPF (somente números): ')
    if not cpf_cliente.isdigit():
        print('Digite números inteiros.')
        return

    cliente_cadastrado = verificar_cpf(lista_clientes, cpf_cliente)
    if not cliente_cadastrado:
        print('Cliente não encontrado!')
        return

    for cliente in cliente_cadastrado:
        print(f"Nome: {cliente['nome']}")
        verificar_contas_cliente(cliente, contas)

        excluir_cliente = input('Deletar cliente do sistema? [S/N]').lower()
        if excluir_cliente == 's':
            for conta in contas:
                contas.remove(conta)
            lista_clientes.remove(cliente)
            print('Cliente deletado com sucesso.')

def gerar_numero_conta(contas):
    if not contas:
        return 1
    return max(conta['numero_conta'] for conta in contas)+1

def cadastrar_conta_corrente(lista_clientes, AGENCIA, contas):
    print()
    print(10 * '=', 'Cadastrar Conta Corrente', 10 * '=')

    cpf_cliente = input('Digite o CPF (somente números): ')
    if not cpf_cliente.isdigit():
        print('Digite números inteiros.')
        return

    cliente_cadastrado = verificar_cpf(lista_clientes, cpf_cliente)
    if not cliente_cadastrado:
        print('Cliente não esta cadastrado no sistema!')
        return contas

    for cliente in cliente_cadastrado:
        nova_conta = input(f"Deseja cadastrar uma nova conta para {cliente['nome']}? [S/N]").lower()
        if nova_conta == 's':
            numero_conta = gerar_numero_conta(contas)
            nova_conta = ({'cliente': cliente, 'numero_conta':numero_conta, 'AGENCIA': AGENCIA})
            print(f"\nConta cadastrada com sucesso: {cliente['nome']} - Número da conta: {numero_conta}")
            contas.append(nova_conta)
            return contas

def exibir_lista_contas(contas):
    print()
    print(10 * '=', 'Lista Conta Corrente', 10 * '=')

    contas_ordenadas = sorted(contas, key=lambda item:item['numero_conta'])
    for e, conta in enumerate(contas_ordenadas):
        print(50* '-')
        print(f"Número da conta:{conta['numero_conta']} - "
              f"Agência: {conta['AGENCIA']} - "
              f"Cliente: {conta['cliente']['nome']} - CPF:{conta['cliente']['cpf']}")

def excluir_conta(contas, lista_clientes):
    print()
    print(10 * '=', 'Excluir Conta Corrente', 10 * '=')

    cpf_cliente = input('Digite o CPF (somente números): ')
    if not cpf_cliente.isdigit():
        print('Digite números inteiros.')
        return

    cliente_cadastrado = verificar_cpf(lista_clientes, cpf_cliente)
    if not cliente_cadastrado:
        print('Cliente não encontrado!')
        return

    for cliente in cliente_cadastrado:
        print(f"Nome: {cliente['nome']}, CPF: {cliente['cpf']}")
        verificar_contas_cliente(cliente, contas)

        excluir_numero_conta = int(input(f"Digite o número da conta: "))
        for conta in contas:
            if conta['numero_conta'] == excluir_numero_conta:
                excluir_conta = input('Deseja encerrar esta conta corrente? [S/N]: ').lower()
                if excluir_conta == 's':
                    contas.remove(conta)
                    print('Conta deletada com sucesso.')
                else:
                    print('Operação cancelada.')
                    return

def depositar(saldo, extrato, LIMITE_TRANSACOES):
    print()
    print(10* '=', 'Efetuar Deposito', 10*'=')

    while True:
        try:
            depositar_valor = float(input('Digite o valor de deposito: R$ '))

            if depositar_valor <= 0:
                print('Valor negativo ou zero, não é possível efetuar depósito.')
                continue
            saldo += depositar_valor
            LIMITE_TRANSACOES -= 1
            extrato.append(f"{data_atual()} - Crédito: R${depositar_valor}")
            print(f"\nValor de R${depositar_valor:.2f}, foi creditado na sua conta.\n")
            return saldo, extrato, LIMITE_TRANSACOES
        except ValueError:
            print('Digite somete números')

def efetuar_saque(*, valor, saldo, limite_saque_diario, numero_saques_efetuados, extrato):

    if valor <= 0:
        print('Valor negativo ou zero, não é possível efetuar depósito.')
        return
    elif valor > saldo:
        print('Você não tem saldo suficiente.')
        return saldo, numero_saques_efetuados, extrato
    elif valor > limite_saque_diario:
        print('Você não pode sacar acima de R$500.')
        return saldo, numero_saques_efetuados, extrato
    else:
        saldo -= valor
        numero_saques_efetuados += 1
        extrato.append(f'{data_atual()} - Débito: R${valor}')
        print(f"\nValor de R${valor:.2f}, foi debitado da sua conta.\n")
        return saldo, numero_saques_efetuados, extrato

def exibir_extrato(saldo, LIMITE_TRANSACOES, *, extrato):
    print()
    print(10 * '=', 'Extrato', 10 * '=')
    if not extrato:
        print('Não foram realizadas transações.')
    else:
        for e in extrato:
            print(f"\n{e}")
    print(f'\nSaldo total: R${saldo}')
    print(f"Quantidade de transações restantes: {LIMITE_TRANSACOES}")

def resetar_limites_diarios(LIMITE_SAQUES, LIMITE_TRANSACOES, data_ultima_transacao):
    obter_data_atual = data_atual().split(" ")[0]
    if obter_data_atual != data_ultima_transacao:
        return 3, 5, obter_data_atual
    return LIMITE_SAQUES, LIMITE_TRANSACOES, data_ultima_transacao

def main():
    LIMITE_SAQUES = 3
    AGENCIA = '0001'
    LIMITE_TRANSACOES = 5
    saldo = 0.0
    limite_saque_diario = 500.0
    numero_saques_efetuados = 0
    extrato = []
    lista_clientes = []
    contas = []
    data_ultima_transacao = data_atual()

    while True:
        print()
        print(10 * '=', 'NTT DATA Sistema Bancário', 10 * '=')
        print(data_atual())
        print()
        LIMITE_SAQUES, LIMITE_TRANSACOES, data_ultima_transacao = resetar_limites_diarios(LIMITE_SAQUES,
                                                                                          LIMITE_TRANSACOES,
                                                                                          data_ultima_transacao)
        try:
            escolha = exibir_opcoes()

            if escolha == opcoes['cadastrar_cliente']:
                cadastrar_cliente(lista_clientes)

            elif escolha == opcoes['exibir_lista_clientes']:
                exibir_lista_clientes(lista_clientes, contas)

            elif escolha == opcoes['procurar_cliente']:
                procurar_cliente(lista_clientes, contas)

            elif escolha == opcoes['deletar_cliente']:
                deletar_cliente(lista_clientes, contas)

            elif escolha == opcoes['cadastrar_conta_corrente']:
                contas = cadastrar_conta_corrente(lista_clientes, AGENCIA, contas)

            elif escolha == opcoes['exibir_lista_de_contas']:
                exibir_lista_contas(contas)

            elif escolha == opcoes['excluir_conta_corrente']:
                excluir_conta(contas, lista_clientes)

            elif escolha == opcoes['efetuar_deposito']:
                if LIMITE_TRANSACOES <= 0:
                    print('Limite de transações da conta atingidos.')
                    continue
                else:
                    saldo, extrato, LIMITE_TRANSACOES = depositar(saldo, extrato, LIMITE_TRANSACOES)

            elif escolha == opcoes['efetuar_saque']:
                if numero_saques_efetuados >= LIMITE_SAQUES:
                    print('Você atingiu o limite de saques diários.')
                    continue
                else:
                    print(10 * '=', 'Efetuar Saque', 10 * '=')
                    valor = float(input('Digite o valor a ser retirado da conta: R$ '))
                    saldo, numero_saques_efetuados, extrato = efetuar_saque(valor=valor, saldo=saldo,
                                                                            limite_saque_diario=limite_saque_diario,
                                                                            numero_saques_efetuados=numero_saques_efetuados,
                                                                            extrato=extrato)
                    if valor <= saldo and valor <= limite_saque_diario:
                        LIMITE_TRANSACOES -= 1

            elif escolha == opcoes['extrato']:
                exibir_extrato(saldo, LIMITE_TRANSACOES, extrato=extrato)

            elif escolha == opcoes['sair']:
                print('Obrigado por usar nosso sistema!!!')
                break
            else:
                print('Digite uma opção válida.')
        except ValueError:
            print('Digite um número das opções.')

main()