from abc import ABC, abstractclassmethod, abstractproperty
import textwrap
AGENCIA = "0001"
def menu():
    menu = ''' #### Banco DIO ####

    Selecione a opção desejada: 

    [1] Criar Usuário
    [2] Criar Conta
    [3] Listar Contas
    [4] Depositar
    [5] Sacar
    [6] Extrato
    [7] Sair

    => '''
    return int(input(textwrap.dedent(menu)))

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class DadosCliente (Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        super().__init__(endereco)

class Conta:
    def __init__(self, numero, usuario):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._usuario = usuario
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, usuario, numero):
        return cls(numero, usuario)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._usuario
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self._saldo
    
        if valor > saldo:
            self._saldo
            print("Saldo insuficiente!\n")
    
        elif valor >0:
            self._saldo -= valor
            print("***Saque efetuado com sucesso!***")
            return True

        else:
            print("Comando invalido!")
    
        return False

        
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Deposito efetuado com sucesso!")
        else:
            print("Valor inválido!")
            return False
        
        return True

class ContaCorrente(Conta):
    def __init__(self,numero, usuario, limite = 500, limite_saques=3):
        super().__init__(numero, usuario)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("*** Valor para saque excedeu o limite! ***\n")
        
        elif excedeu_saques:
            print("*** Limite diario de saque excedido! ***\n")

        else:
            return super().sacar(valor)
    
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self._agencia}
            C/C:\t\t{self._numero}
            Titular:\t{self._usuario.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

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

def depositar(usuarios):
    cpf = input("Informe o CPF do usuario: ")
    usuario = filtro_usuarios(cpf, usuarios)

    if not usuario:
        print("\nCliente não encontrado!")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(usuario)
    if not conta:
        return

    usuario.realizar_transacao(conta, transacao)

def sacar(usuarios):
    cpf = input("Informe o CPF do cliente: ")
    usuario = filtro_usuarios(cpf, usuarios)

    if not usuario:
        print("\nCliente não encontrado!")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(usuario)
    if not conta:
        return

    usuario.realizar_transacao(conta, transacao)

def recuperar_conta_cliente(usuario):
    if not usuario.contas:
        print("\nCliente não possui conta!")
        return

    return usuario.contas[0]

def exibir_extrato(usuarios):
    cpf = input("Informe o CPF do cliente: ")
    usuario = filtro_usuarios(cpf, usuarios)

    if not usuario:
        print("\n Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(usuario)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

def filtro_usuarios(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario.cpf == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_usuarios(usuarios):
    cpf = input("Informe seu cpf (apenas numeros): ")
    usuario = filtro_usuarios(cpf, usuarios)

    if usuario:
        print("CPF já possui cadastro em sistema!")

    nome = input("Informe seu nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe seu endereço (logradouro, numero - bairro - cidade/sigla do estado): ")
    
    usuario = DadosCliente(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    
    usuarios.append(usuario)

    print("Usuario cadastrado com sucesso!")

def criar_contas(numero_conta, usuarios, contas):
    cpf = input("Digite o cpf do usuario (Apenas numeros): ")
    usuario = filtro_usuarios(cpf, usuarios)

    if not usuario:
        print("Usuario nao encontrado.")
        return
    
    conta = ContaCorrente.nova_conta(usuario=usuario, numero=numero_conta)
    contas.append(conta)
    usuario.contas.append(conta)
    print("Conta criada com sucesso!")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def main():
    usuarios = []
    contas = []
    while True:
        opcao = menu()
        
        if opcao == 1:
            print("###Criar Usuario###")
            criar_usuarios(usuarios)

        elif opcao == 2:
            print("###Criar Conta###")
            nova_conta = len(contas) + 1
            criar_contas(nova_conta, usuarios, contas)


        elif opcao == 3:
            listar_contas(contas)

        elif opcao == 4:
            print("###Deposito###")
            depositar(usuarios)  

        elif opcao == 5:
            print("###Saque###\n")
            sacar(usuarios)

        elif opcao == 6:
            print("###Extrato###\n")
            exibir_extrato(usuarios)

        elif opcao == 7:
            print("Obrigado por usar o Banco DIO!")
            break

        else:
            print("Comando inválido. Por favor selecione a operação desejada.\n")

main()