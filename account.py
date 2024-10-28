from datetime import datetime
import abc
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

def verificar_contas_cliente(cliente, contas):
    contas_cliente = [conta for conta in contas if conta.cliente.cpf == cliente.cpf]
    if contas_cliente:
        for conta in contas_cliente:
            print(f"Agência: {conta.agencia} - Número da conta: {conta.numero_conta}")
    else:
        print(f"{cliente.nome}, não possui nenhuma conta cadastrada")

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def cadastrar_conta_corrente(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero_conta, cliente, agencia="0001", saldo=0.0):
        self._saldo = saldo
        self._numero_conta = numero_conta
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def cadastrar_conta(cls, numero_conta, cliente):
        return cls(numero_conta, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero_conta(self):
        return self._numero_conta

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

class ContaCorrente(Conta):
    def __init__(self, numero_conta, cliente, agencia="0001", saldo=0.0, limite=500.0, qtd_limite_saques=3):
        super().__init__(numero_conta, cliente, agencia, saldo)
        self.limite = limite
        self.qtd_limite_saques = qtd_limite_saques

    def depositar(self, valor):
        if valor <= 0:
            print('Valor negativo ou zero, não é possível efetuar depósito.')
            return False
        else:
            self._saldo += valor
            print(f"\nValor de R${valor:.2f}, foi creditado na sua conta.")
            return True

    def sacar(self, valor):

        if self.qtd_limite_saques <= 0:
            print('Você atingiu a quantidade de limite de saques diários.')
            return False

        if valor <= 0:
            print('Valor negativo ou zero, não é possível efetuar saque.')
            return False
        elif valor > self._saldo:
            print('Você não tem saldo suficiente.')
            return False
        elif valor > self.limite:
            print('Você não pode sacar acima de R$500.')
            return False
        else:
            self._saldo -= valor
            self.qtd_limite_saques -= 1
            print(f"Valor de R$ {valor} foi debitado da sua conta.")
            print(f"Quantidade de saques restantes hoje: {self.qtd_limite_saques}")
            return True

class Transacao(abc.ABC):
    @property
    @abc.abstractmethod
    def valor(self):
        pass

    @abc.abstractmethod
    def registrar(self, conta):
        pass

class Historico:
    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                'tipo': transacao.__class__.__name__,
                'valor': transacao.valor,
                'data': data_atual()
            }
        )

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def verificar_cpf(lista_clientes, cpf_cliente):
    clientes_cadastrado = [cliente for cliente in lista_clientes if cliente.cpf == cpf_cliente]
    return clientes_cadastrado

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

    cliente_nome = input('Digite o nome do cliente: ').title()
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe o endereço (logradouro, número - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=cliente_nome, cpf=cpf_cliente, data_nascimento=data_nascimento,endereco=endereco )
    print(f'\nCliente {cliente_nome} cadastrado com sucesso!')
    lista_clientes.append(cliente)

def exibir_lista_clientes(lista_clientes, contas):
    print()
    print(10 * '=', 'Lista de Clientes', 10 * '=')

    if not lista_clientes:
        print('Nenhum cliente cadastrado.')
        return

    clientes_ordenados = sorted(lista_clientes, key= lambda item:item.nome)

    for cliente in clientes_ordenados:
        print(50 * '-')
        print(f"Nome: {cliente.nome} - CPF:{cliente.cpf} - Data Nascimento: {cliente.data_nascimento}")
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
        print(f"Nome: {cliente.nome} - CPF:{cliente.cpf} "
              f"- Data Nascimento: {cliente.data_nascimento}\nEndereço: {cliente.endereco}")
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
        print(f"Nome: {cliente.nome} - CPF: {cliente.cpf}")
        verificar_contas_cliente(cliente, contas)

        excluir_cliente = input('Deletar cliente do sistema? [S/N]').lower()
        if excluir_cliente == 's':
            for conta in cliente.contas[:]:
                contas.remove(conta)
            lista_clientes.remove(cliente)
            print('Cliente deletado com sucesso.')

def gerar_numero_conta(contas):
    if not contas:
        return 1
    return max(conta.numero_conta for conta in contas)+1

def cadastrar_conta_corrente(lista_clientes, contas):
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
        nova_conta = input(f"Deseja cadastrar uma nova conta para {cliente.nome}? [S/N]").lower()
        if nova_conta == 's':
            numero_conta = gerar_numero_conta(contas)
            conta = ContaCorrente(numero_conta=numero_conta, cliente=cliente)
            print(f"\nConta cadastrada com sucesso para: {cliente.nome} - Número da conta: {numero_conta}")
            cliente.contas.append(conta)
            contas.append(conta)
            return contas

def exibir_lista_contas(contas):
    print()
    print(10 * '=', 'Lista Conta Corrente', 10 * '=')

    contas_ordenadas = sorted(contas, key=lambda item:item.numero_conta)
    for e, conta in enumerate(contas_ordenadas):
        print(50* '-')
        print(f"Número da conta:{conta.numero_conta} - "
              f"Agência: {conta.agencia} - "
              f"Cliente: {conta.cliente.nome} - CPF:{conta.cliente.cpf}")

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
        print(f"Nome: {cliente.nome}, CPF: {cliente.cpf}")
        verificar_contas_cliente(cliente, contas)

        excluir_numero_conta = int(input(f"Digite o número da conta: "))
        for conta in contas:
            if conta.numero_conta == excluir_numero_conta:
                excluir_conta = input('Deseja encerrar esta conta corrente? [S/N]: ').lower()
                if excluir_conta == 's':
                    contas.remove(conta)
                    print('Conta deletada com sucesso.')
                else:
                    print('Operação cancelada.')
                    return

def efetuar_deposito(lista_clientes, contas):
    print()
    print(10* '=', 'Efetuar Deposito', 10*'=')

    cpf_cliente = input('Digite o CPF (somente números): ')
    if not cpf_cliente.isdigit():
        print('Digite números inteiros.')
        return

    cliente_cadastrado = verificar_cpf(lista_clientes, cpf_cliente)
    if not cliente_cadastrado:
        print('Cliente não esta cadastrado no sistema!')
        return

    for cliente in cliente_cadastrado:
        verificar_contas_cliente(cliente, contas)
        for conta in cliente.contas:
            numero_conta = int(input('\nDigite o número da conta: '))
            conta_selecionada = next((conta for conta in cliente.contas if conta.numero_conta == numero_conta), None)
            if conta_selecionada is None:
                print('Conta não encontrada')
                continue
            valor = float(input('Digite o valor de deposito: R$ '))
            deposito = Deposito(valor)
            deposito.registrar(conta_selecionada)
            return

def efetuar_saque(*, lista_clientes, contas):
    print()
    print(10 * '=', 'Efetuar Saque', 10 * '=')

    cpf_cliente = input('Digite o CPF (somente números): ')
    if not cpf_cliente.isdigit():
        print('Digite números inteiros.')
        return

    cliente_cadastrado = verificar_cpf(lista_clientes, cpf_cliente)
    if not cliente_cadastrado:
        print('Cliente não esta cadastrado no sistema!')
        return

    for cliente in cliente_cadastrado:
        verificar_contas_cliente(cliente, contas)
        for conta in cliente.contas:
            numero_conta = int(input('\nDigite o número da conta: '))
            conta_selecionada = next((conta for conta in cliente.contas if conta.numero_conta == numero_conta), None)
            if conta_selecionada is None:
                print('Conta não encontrada')
                continue
            valor = float(input('Digite o valor para efetuar o saque: R$ '))
            saque = Saque(valor)
            saque.registrar(conta_selecionada)
            return

def exibir_extrato(lista_clientes):
    print()
    print(10 * '=', 'Extrato', 10 * '=')

    cpf_cliente = input('Digite o CPF (somente números): ')
    if not cpf_cliente.isdigit():
        print('Digite números inteiros.')
        return

    cliente_cadastrado = verificar_cpf(lista_clientes, cpf_cliente)
    if not cliente_cadastrado:
        print('Cliente não esta cadastrado no sistema!')
        return

    for cliente in cliente_cadastrado:
        if not cliente.contas:
            print(f"{cliente.nome} não possui contas para exibir extrato.")
            continue
        for conta in cliente.contas:
            print(f"Número da conta: {conta.numero_conta} - Saldo: R${conta.saldo:.2f}")

        numero_conta = int(input('\nDigite o número da conta: '))
        conta_selecionada = next((conta for conta in cliente.contas if conta.numero_conta == numero_conta), None)
        if not conta_selecionada:
            print('Conta não encontrada')
            continue
        transacao = conta_selecionada.historico._transacoes
        extrato = ''
        if not transacao:
            extrato += 'Não foi realizada nenhuma transação.'
        else:
            for t in transacao:
                extrato += f"\nData: {t['data']}\n{t['tipo']}\nValor R$: {t['valor']}\n{20 * '-'}"
        print(extrato)

def resetar_limites_diarios(LIMITE_SAQUES, LIMITE_TRANSACOES, data_ultima_transacao):
    obter_data_atual = data_atual().split(" ")[0]
    if obter_data_atual != data_ultima_transacao:
        return 3, 5, obter_data_atual
    return LIMITE_SAQUES, LIMITE_TRANSACOES, data_ultima_transacao

def main():
    data_ultima_transacao = data_atual()
    lista_clientes = []
    contas = []

    while True:
        print()
        print(10 * '=', 'NTT DATA Sistema Bancário', 10 * '=')
        print(data_atual())
        print()
        # LIMITE_SAQUES, LIMITE_TRANSACOES, data_ultima_transacao = resetar_limites_diarios(LIMITE_SAQUES,
        #                                                                                   LIMITE_TRANSACOES,
        #                                                                                   data_ultima_transacao)
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
                contas = cadastrar_conta_corrente(lista_clientes, contas)

            elif escolha == opcoes['exibir_lista_de_contas']:
                exibir_lista_contas(contas)

            elif escolha == opcoes['excluir_conta_corrente']:
                excluir_conta(contas, lista_clientes)

            elif escolha == opcoes['efetuar_deposito']:
                efetuar_deposito(lista_clientes, contas)

            elif escolha == opcoes['efetuar_saque']:
                efetuar_saque(lista_clientes=lista_clientes, contas=contas)

            elif escolha == opcoes['extrato']:
                exibir_extrato(lista_clientes)

            elif escolha == opcoes['sair']:
                print('Obrigado por usar nosso sistema!!!')
                break
            else:
                print('Digite uma opção válida.')
        except ValueError:
            print('Digite um número das opções.')

main()