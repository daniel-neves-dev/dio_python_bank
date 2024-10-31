from datetime import datetime
import abc, os, pytz

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
    def __init__(self, numero_conta, cliente, agencia="0001", saldo=0.0, limite=500.0, qtd_limite_saques=3, qtd_transacoes=5, data_ultima_transacao=None):
        super().__init__(numero_conta, cliente, agencia, saldo)
        self.limite = limite
        self.qtd_limite_saques = qtd_limite_saques
        self.qtd_transacoes = qtd_transacoes

        if data_ultima_transacao is None:
            self.data_ultima_transacao = data_atual().split(' ')[0]
        else:
            self.data_ultima_transacao = data_ultima_transacao

        self.qtd_limite_saques, self.qtd_transacoes, self.data_ultima_transacao = resetar_limites_diarios(
            self.data_ultima_transacao,
            self.qtd_limite_saques,
            self.qtd_transacoes
        )

    def depositar(self, valor):
        if self.qtd_transacoes <= 0:
            print('\n   Você atingiu a quantidade limite de transações diárias.')
            return False

        if valor <= 0:
            print('\n   Valor negativo ou zero, não é possível efetuar depósito.')
            return False
        else:
            self._saldo += valor
            self.qtd_transacoes -= 1
            print(f"\n   Valor de R${valor:.2f}, foi creditado na sua conta.")
            print(f"\n   Quantidade de transações restantes hoje: {self.qtd_transacoes}")
            return True

    def sacar(self, valor):

            if self.qtd_limite_saques <= 0:
                print('\n   Você atingiu a quantidade limite de saques diários.')
                return False

            if self.qtd_transacoes <= 0:
                print('\n   Você atingiu a quantidade limite de transações diárias.')
                return False

            if valor <= 0:
                print('\n   Valor negativo ou zero, não é possível efetuar saque.')
                return False
            elif valor > self._saldo:
                print('\n   Você não tem saldo suficiente.')
                return False
            elif valor > self.limite:
                print('\n   Você não pode sacar acima de R$500.')
                return False
            else:
                self._saldo -= valor
                self.qtd_limite_saques -= 1
                self.qtd_transacoes -= 1
                print(f"\n   Valor de R$ {valor} foi debitado da sua conta.")
                print(f"   Quantidade de saques restantes : {self.qtd_limite_saques}")
                print(f"   Quantidade de transações restantes : {self.qtd_transacoes}")
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

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def exibir_opcoes():
    for opcao, numero in opcoes.items():
        print(f"   {numero} - {opcao.replace('_', ' ').title()}")

    escolher_opcao = int(input(f"\n   Escolha uma opção acima: "))
    return escolher_opcao

def data_atual():
    return datetime.now(pytz.timezone("America/Sao_Paulo")).strftime("%d/%m/%Y - %H:%M:%S")

def verificar_contas_cliente(cliente, contas):
    contas_cliente = [conta for conta in contas if conta.cliente.cpf == cliente.cpf]
    if contas_cliente:
        for conta in contas_cliente:
            print(f"   Agência: {conta.agencia} - Número da conta: {conta.numero_conta} - Saldo: R$ {conta.saldo}")

def validar_cpf(cpf_cliente):
    return cpf_cliente.isdigit() and len(cpf_cliente) == 11

def verificar_cpf(lista_clientes, cpf_cliente):
    clientes_cadastrado = [cliente for cliente in lista_clientes if cliente.cpf == cpf_cliente]
    return clientes_cadastrado

def cadastrar_cliente(lista_clientes):
    print()
    print(f" ", 10 * '=', 'Cadastro de Clientes', 10 * '=')

    while True:

        cpf_cliente = input('\n   Digite o CPF (somente números): ').strip()
        validar_cpf(cpf_cliente)
        if not validar_cpf(cpf_cliente):
            print('\n   Digite 11 números inteiros para cpf.')
            continue

        cliente_cadastrado = verificar_cpf(lista_clientes, cpf_cliente)
        if cliente_cadastrado:
            print('\n   Cliente já cadastrado!')
            return

        cliente_nome = input('\n   Digite o nome do cliente: ').title()
        while True:
            try:
                data_nascimento_str = input("\n   Informe a data de nascimento (dd/mm/aaaa): ")
                data_nascimento = datetime.strptime(data_nascimento_str, '%d/%m/%Y')
                break
            except ValueError:
                print('   Digite a data no formato (dd/mm/aaaa)')
                continue

        endereco = input("\n   Informe o endereço (logradouro, número - bairro - cidade/sigla estado): ")

        cliente = PessoaFisica(nome=cliente_nome, cpf=cpf_cliente, data_nascimento=data_nascimento,endereco=endereco )
        print(f'\n   Cliente {cliente_nome} cadastrado com sucesso!')
        lista_clientes.append(cliente)
        return lista_clientes

def exibir_lista_clientes(lista_clientes, contas):
    print()
    print(f" ", 10 * '=', 'Lista de Clientes', 10 * '=')

    if not lista_clientes:
        print('\n   Nenhum cliente cadastrado.')
        return

    clientes_ordenados = sorted(lista_clientes, key= lambda item:item.nome)

    for cliente in clientes_ordenados:
        print(f" ",50 * '-')
        print(f"\n   Nome: {cliente.nome} - CPF:{cliente.cpf} - Data Nascimento: {cliente.data_nascimento}")
        verificar_contas_cliente(cliente, contas)
        if not cliente.contas:
            print(f"   {cliente.nome} não possui conta cadastrada.")
    return

def procurar_cliente(lista_clientes, contas):
    print()
    print(f" ",10 * '=', 'Procurar Cliente', 10 * '=')

    while True:
        cpf_cliente = input('\n   Digite o CPF (somente números): ').strip()
        validar_cpf(cpf_cliente)
        if not validar_cpf(cpf_cliente):
            print('\n   Digite 11 números inteiros para cpf.')
            continue

        cliente_cadastrado = verificar_cpf(lista_clientes, cpf_cliente)
        if not cliente_cadastrado:
            print('\n   Cliente não cadastrado!')
            return

        for cliente in cliente_cadastrado:
            print(f"   Nome: {cliente.nome} - CPF:{cliente.cpf} "
                  f"   - Data Nascimento: {cliente.data_nascimento}\n   Endereço: {cliente.endereco}")
            verificar_contas_cliente(cliente, contas)
            return

def deletar_cliente(lista_clientes, contas):
    print()
    print(f" ", 10 * '=', 'Deletar Cliente', 10 * '=')

    while True:
        cpf_cliente = input('\n   Digite o CPF (somente números): ').strip()
        validar_cpf(cpf_cliente)
        if not validar_cpf(cpf_cliente):
            print('\n   Digite 11 números inteiros para cpf.')
            continue

        cliente_cadastrado = verificar_cpf(lista_clientes, cpf_cliente)
        if not cliente_cadastrado:
            print('\n   Cliente não cadastrado!')
            return

        for cliente in cliente_cadastrado:
            print(f"   Nome: {cliente.nome} - CPF: {cliente.cpf}")
            verificar_contas_cliente(cliente, contas)

            excluir_cliente = input('   Deletar cliente do sistema? [S/N]').lower()
            if excluir_cliente == 's':
                for conta in cliente.contas[:]:
                    contas.remove(conta)
                lista_clientes.remove(cliente)
                print('   Cliente deletado com sucesso.')
                return contas

def gerar_numero_conta(contas):
    if not contas:
        return 1
    return max(conta.numero_conta for conta in contas)+1

def cadastrar_conta_corrente(lista_clientes, contas):
    print()
    print(f" ", 10 * '=', 'Cadastrar Conta Corrente', 10 * '=')

    while True:
        cpf_cliente = input('\n   Digite o CPF (somente números): ').strip()
        validar_cpf(cpf_cliente)
        if not validar_cpf(cpf_cliente):
            print('\n   Digite 11 números inteiros para cpf.')
            continue

        cliente_cadastrado = verificar_cpf(lista_clientes, cpf_cliente)
        if not cliente_cadastrado:
            print('\n   Cliente não cadastrado!')
            return contas

        for cliente in cliente_cadastrado:
            nova_conta = input(f"\n   Deseja cadastrar uma nova conta para {cliente.nome}? [S/N]").lower()
            if nova_conta == 's':
                numero_conta = gerar_numero_conta(contas)
                conta = ContaCorrente(numero_conta=numero_conta, cliente=cliente)
                print(f"\n   Conta cadastrada com sucesso para: {cliente.nome} - Número da conta: {numero_conta}")
                cliente.contas.append(conta)
                contas.append(conta)
                return contas
        return contas

def exibir_lista_contas(contas):
    print()
    print(f" ",10 * '=', 'Lista Conta Corrente', 10 * '=')

    contas_ordenadas = sorted(contas, key=lambda item:item.numero_conta)
    for e, conta in enumerate(contas_ordenadas):
        print(f" ",50* '-')
        print(f"   Número da conta:{conta.numero_conta} - "
              f"   Agência: {conta.agencia} - "
              f"   Cliente: {conta.cliente.nome} - CPF:{conta.cliente.cpf}")

def excluir_conta(contas, lista_clientes):
    print()
    print(f" ",10 * '=', 'Excluir Conta Corrente', 10 * '=')

    while True:
        cpf_cliente = input('\n   Digite o CPF (somente números): ').strip()

        if not validar_cpf(cpf_cliente):
            print('\n   Digite 11 números inteiros para cpf.')
            continue

        cliente_cadastrado = verificar_cpf(lista_clientes, cpf_cliente)
        if not cliente_cadastrado:
            print('   Cliente não cadastrado!')
            return

        for cliente in cliente_cadastrado:
            verificar_contas_cliente(cliente, contas)
            if not cliente.contas:
                print(f"   {cliente.nome} não possui conta cadastrada.")
                return

            while True:
                try:
                    numero_conta = int(input('\n   Digite o número da conta: '))
                except ValueError:
                    print('   Digite somente números para conta.')
                    continue

                conta_selecionada = next((conta for conta in cliente.contas if conta.numero_conta == numero_conta),None)

                if conta_selecionada is None:
                    print('   Conta não encontrada')
                    buscar_nova_conta = input('\n   Deseja procurar outa conta? [S/N] ').lower()
                    if buscar_nova_conta == 's':
                        continue
                    else:
                        print('   Operação cancelada')
                        return
                else:
                    break

        if conta_selecionada.saldo > 0:
            print(f'\n   Sua conta possui R$ {conta_selecionada.saldo}')
            sacar = input('\n   Deseja realizar o saque agora? [S/N]: ').lower()
            while True:
                if sacar == 's':
                    valor = float(input('\n   Digite o valor para efetuar o saque: R$ '))
                    saque = Saque(valor)
                    saque.registrar(conta_selecionada)

                    if conta_selecionada.saldo != 0:
                        print('\n   O valor total da conta deve ser sacado, procure o gerente se necessário.')
                        continue
                    else:
                        break
                else:
                    print('\n   Não é possível excluir conta com saldo positivo')
                    return

        while True:
            confirmar = input(
                f'\n   Deseja realmente excluir a conta número {conta_selecionada.numero_conta}? [S/N]: ').lower().strip()
            if confirmar == 's':
                try:
                    contas.remove(conta_selecionada)
                    cliente.contas.remove(conta_selecionada)
                    print(f'\n   Conta excluída com sucesso.')
                except ValueError:
                    print('   Conta não encontrada.')
                return
            elif confirmar == 'n':
                print('   Operação cancelada.')
                return
            else:
                print('   Resposta inválida. Por favor, responda com "S" ou "N".')
                continue

def efetuar_deposito(lista_clientes, contas):
    print()
    print(f" ",10* '=', 'Efetuar Deposito', 10*'=')

    while True:
        cpf_cliente = input('\n   Digite o CPF (somente números): ').strip()
        validar_cpf(cpf_cliente)
        if not validar_cpf(cpf_cliente):
            print('\n   Digite 11 números inteiros para cpf.')
            continue

        cliente_cadastrado = verificar_cpf(lista_clientes, cpf_cliente)
        if not cliente_cadastrado:
            print('   Cliente não cadastrado!')
            return

        for cliente in cliente_cadastrado:
            print(f"\n   Nome: {cliente.nome} - CPF: {cliente.cpf}")
            verificar_contas_cliente(cliente, contas)
            if not cliente.contas:
                print(f"   {cliente.nome} não possui conta cadastrada.")
                return

            for conta in cliente.contas:
                while True:
                    try:
                        numero_conta = int(input('\n   Digite o número da conta: '))
                    except ValueError:
                        print('   Digite somente números para conta.')
                        continue

                    conta_selecionada = next((conta for conta in cliente.contas if conta.numero_conta == numero_conta), None)

                    if conta_selecionada is None:
                        print('   Conta não encontrada')
                        buscar_nova_conta = input('\n   Deseja procurar outa conta? [S/N] ').lower()
                        if buscar_nova_conta == 's':
                            continue
                        else:
                            print('   Operação cancelada')
                            return
                    else:
                        break

                while True:
                    valor = float(input('\n   Digite o valor de deposito: R$ '))
                    deposito = Deposito(valor)
                    deposito.registrar(conta_selecionada)
                    return

def efetuar_saque(*, lista_clientes, contas):
    print()
    print(f" ", 10 * '=', 'Efetuar Saque', 10 * '=')

    while True:
        cpf_cliente = input('\n   Digite o CPF (somente números): ').strip()
        validar_cpf(cpf_cliente)
        if not validar_cpf(cpf_cliente):
            print('\n   Digite 11 números inteiros para cpf.')
            continue

        cliente_cadastrado = verificar_cpf(lista_clientes, cpf_cliente)
        if not cliente_cadastrado:
            print('   Cliente não cadastrado!')
            return

        for cliente in cliente_cadastrado:
            print(f"\n   Nome: {cliente.nome} - CPF: {cliente.cpf}")
            verificar_contas_cliente(cliente, contas)
            if not cliente.contas:
                print(f"   {cliente.nome} não possui conta cadastrada.")
                return

            for conta in cliente.contas:
                while True:
                    try:
                        numero_conta = int(input('\n   Digite o número da conta: '))
                    except ValueError:
                        print('   Digite somente números para conta.')
                        continue

                    conta_selecionada = next((conta for conta in cliente.contas if conta.numero_conta == numero_conta),
                                             None)

                    if conta_selecionada is None:
                        print('   Conta não encontrada')
                        buscar_nova_conta = input('\n   Deseja procurar outa conta? [S/N] ').lower()
                        if buscar_nova_conta == 's':
                            continue
                        else:
                            print('   Operação cancelada')
                            return
                    else:
                        break

                while True:
                    valor = float(input('\n   Digite o valor para efetuar o saque: R$ '))
                    saque = Saque(valor)
                    saque.registrar(conta_selecionada)
                    return

def exibir_extrato(lista_clientes):
    print()
    print(f" ",10 * '=', 'Extrato', 10 * '=')

    while True:
        cpf_cliente = input('\n   Digite o CPF (somente números): ').strip()
        validar_cpf(cpf_cliente)
        if not validar_cpf(cpf_cliente):
            print('\n   Digite 11 números inteiros para cpf.')
            continue

        cliente_cadastrado = verificar_cpf(lista_clientes, cpf_cliente)
        if not cliente_cadastrado:
            print('\n   Cliente não cadastrado!')
            return

        for cliente in cliente_cadastrado:
            print(f"\n   Nome: {cliente.nome} - CPF: {cliente.cpf}")
            if not cliente.contas:
                print(f"\n   {cliente.nome} não possui contas para exibir extrato.")
                return
            for conta in cliente.contas:
                print(f"\n   Número da conta: {conta.numero_conta} - Saldo: R${conta.saldo:.2f}")

            numero_conta = int(input('\n   Digite o número da conta: '))
            conta_selecionada = next((conta for conta in cliente.contas if conta.numero_conta == numero_conta), None)
            if not conta_selecionada:
                print('\n   Conta não encontrada')
                continue
            transacao = conta_selecionada.historico._transacoes
            extrato = ''
            if not transacao:
                extrato += '\n   Não foi realizada nenhuma transação.'
            else:
                for t in transacao:
                    extrato += f"\n   Data: {t['data']}\n   {t['tipo']}\n   Valor R$: {t['valor']}\n   {20 * '-'}"
            print(extrato)
            return

def resetar_limites_diarios(data_ultima_transacao, qtd_limite_saques, qtd_transacoes):
    obter_data_atual = data_atual().split(' ')[0]
    if obter_data_atual != data_ultima_transacao:
        return 3, 5, obter_data_atual
    return qtd_limite_saques, qtd_transacoes, data_ultima_transacao

def main():
    data_ultima_transacao = data_atual().split(' ')[0]
    lista_clientes = []
    contas = []

    while True:
        print()
        print(f" ",10 * '=', 'NTT DATA Sistema Bancário', 10 * '=')
        print(f"   {data_atual()}")
        print()

        nova_data = data_atual().split(' ')[0]
        if nova_data != data_ultima_transacao:
            for conta in contas:
                if isinstance(conta, ContaCorrente):
                    conta.qtd_limite_saques, conta.qtd_transacoes, conta.data_ultima_transacao = resetar_limites_diarios(
                        conta.data_ultima_transacao,
                        conta.qtd_limite_saques,
                        conta.qtd_transacoes
                    )
            data_ultima_transacao = nova_data

        try:
            escolha = exibir_opcoes()

            if escolha == opcoes['cadastrar_cliente']:
                clear_screen()
                cadastrar_cliente(lista_clientes)

            elif escolha == opcoes['exibir_lista_clientes']:
                clear_screen()
                exibir_lista_clientes(lista_clientes, contas)

            elif escolha == opcoes['procurar_cliente']:
                clear_screen()
                procurar_cliente(lista_clientes, contas)

            elif escolha == opcoes['deletar_cliente']:
                clear_screen()
                deletar_cliente(lista_clientes, contas)

            elif escolha == opcoes['cadastrar_conta_corrente']:
                clear_screen()
                contas = cadastrar_conta_corrente(lista_clientes, contas)

            elif escolha == opcoes['exibir_lista_de_contas']:
                clear_screen()
                exibir_lista_contas(contas)

            elif escolha == opcoes['excluir_conta_corrente']:
                clear_screen()
                excluir_conta(contas, lista_clientes)

            elif escolha == opcoes['efetuar_deposito']:
                clear_screen()
                efetuar_deposito(lista_clientes, contas)

            elif escolha == opcoes['efetuar_saque']:
                clear_screen()
                efetuar_saque(lista_clientes=lista_clientes, contas=contas)

            elif escolha == opcoes['extrato']:
                clear_screen()
                exibir_extrato(lista_clientes)

            elif escolha == opcoes['sair']:
                print('\n   Obrigado por usar nosso sistema!!!')
                break
            else:
                print('\n   Digite uma opção válida.')
        except ValueError:
            print('\n   Digite um número das opções.')

main()