import datetime

class Carro:
    """ Classe base que define os atributos de um modelo/categoria de carro. """
    def __init__(self, categoria, transmissao, combustivel, marca, modelo):
        self.categoria = categoria
        self.transmissao = transmissao
        self.combustivel = combustivel
        self.marca = marca
        self.modelo = modelo

    def exibir_info_base(self):
        print(f"Categoria: {self.categoria}")
        print(f"Transmissão: {self.transmissao}")
        print(f"Combustível: {self.combustivel}")
        print(f"Marca: {self.marca}")
        print(f"Modelo: {self.modelo}")

class Veiculo(Carro):
    """ Classe que herda de Carro e adiciona atributos específicos da instância (Ano e Placa). """
    def __init__(self, carro_base, ano, placa):
        # Herda os atributos do objeto carro_base
        super().__init__(
            carro_base.categoria, 
            carro_base.transmissao, 
            carro_base.combustivel, 
            carro_base.marca, 
            carro_base.modelo
        )
        self.ano = ano
        self.placa = placa
        self.disponivel = True

    def exibir_detalhes(self):
        self.exibir_info_base()
        print(f"Ano: {self.ano}")
        print(f"Placa: {self.placa}")
        print(f"Status: {'Disponível' if self.disponivel else 'Alugado'}")

class Cliente:
    """ Classe que representa o cliente da locadora. """
    def __init__(self, nome, cpf, rg):
        self.nome = nome
        self.cpf = cpf
        self.rg = rg

class Locacao:
    """ Classe para gerenciar a associação entre Cliente, Veículo e Período. """
    def __init__(self, veiculo, cliente, data_inicio, data_fim):
        self.veiculo = veiculo
        self.cliente = cliente
        self.data_inicio = data_inicio
        self.data_fim = data_fim

class Locadora:
    """ Classe principal que gerencia o fluxo da aplicação. """
    def __init__(self):
        self.categorias_modelos = [] # Lista de objetos Carro (base)
        self.frota = []              # Lista de objetos Veiculo
        self.clientes = []           # Lista de objetos Cliente
        self.locacoes = []           # Lista de objetos Locacao

    def menu(self):
        while True:
            print("\n" + "="*40)
            print("Bem-vindo a Locadora Boa Viagem, escolha uma das opções abaixo:")
            print("="*40)
            print("1) Cadastrar um Novo Veículo")
            print("2) Cadastrar um Novo Cliente")
            print("3) Realizar a locação de um Veículo")
            print("4) Relatório de locação")
            print("0) Sair")
            
            opcao = input("\nEscolha uma das opções: ")

            if opcao == '1':
                self.cadastrar_veiculo()
            elif opcao == '2':
                self.cadastrar_cliente()
            elif opcao == '3':
                self.realizar_locacao()
            elif opcao == '4':
                self.exibir_relatorio()
            elif opcao == '0':
                break
            else:
                print("Opção inválida!")

    def cadastrar_veiculo(self):
        carro_base = None
        
        if self.categorias_modelos:
            print("\n++++++++ Categorias/Modelos Cadastrados ++++++++")
            for i, c in enumerate(self.categorias_modelos):
                print(f"{i+1}) {c.marca} {c.modelo} ({c.categoria})")
            
            resp = input("\nO carro está em uma das categorias acima? [S/N]: ").upper()
            if resp == 'S':
                idx = int(input("Escolha o número da Categoria: ")) - 1
                carro_base = self.categorias_modelos[idx]

        if not carro_base:
            print("\n--- Cadastro de Novo Modelo ---")
            cat = input("Entre com o nome da categoria (Ex: SUV): ")
            trans = input("Informe a Transmissão: ")
            comb = input("Informe o tipo de Combustível: ")
            marca = input("Informe a Marca: ")
            mod = input("Informe o Modelo: ")
            carro_base = Carro(cat, trans, comb, marca, mod)
            self.categorias_modelos.append(carro_base)

        print("\n--- Detalhes da Instância ---")
        ano = input("Ano: ")
        placa = input("Placa: ")
        novo_veiculo = Veiculo(carro_base, ano, placa)
        self.frota.append(novo_veiculo)
        print("\nVeículo cadastrado com sucesso!")

    def cadastrar_cliente(self):
        print("\n--- Cadastro de Cliente ---")
        nome = input("Nome: ")
        cpf = input("CPF: ")
        rg = input("RG: ")
        self.clientes.append(Cliente(nome, cpf, rg))
        print("Cliente cadastrado com sucesso!")

    def realizar_locacao(self):
        # Filtrar apenas carros disponíveis
        disponiveis = [v for v in self.frota if v.disponivel]
        
        if not disponiveis:
            print("\n[ERRO] Não há veículos disponíveis para locação no momento.")
            return

        print("\n--- Veículos Disponíveis ---")
        for i, v in enumerate(disponiveis):
            print(f"\nNúmero: {i+1}")
            v.exibir_detalhes()

        try:
            escolha_v = int(input("\nQual Carro o cliente irá alugar (Número): ")) - 1
            veiculo_escolhido = disponiveis[escolha_v]
            
            cpf_cliente = input("Qual o CPF do cliente: ")
            cliente_encontrado = next((c for c in self.clientes if c.cpf == cpf_cliente), None)
            
            if not cliente_encontrado:
                print("[ERRO] Cliente não encontrado!")
                return

            inicio = input("Qual o início da locação (DD/MM/AAAA): ")
            fim = input("Qual o fim da locação (DD/MM/AAAA): ")

            # Efetivar locação
            veiculo_escolhido.disponivel = False
            nova_locacao = Locacao(veiculo_escolhido, cliente_encontrado, inicio, fim)
            self.locacoes.append(nova_locacao)
            print("\nLocação realizada com sucesso!")

        except (ValueError, IndexError):
            print("[ERRO] Entrada inválida.")

    def exibir_relatorio(self):
        if not self.locacoes:
            print("\nNenhuma locação registrada.")
            return

        print("\n" + "="*40)
        print("       RELATÓRIO DE LOCAÇÕES")
        print("="*40)
        for loc in self.locacoes:
            print("\n--- Carro Alugado ---")
            loc.veiculo.exibir_info_base()
            print(f"Ano: {loc.veiculo.ano}")
            print(f"Placa: {loc.veiculo.placa}")
            print("\n--- Cliente ---")
            print(f"Cliente: {loc.cliente.nome}")
            print(f"CPF: {loc.cliente.cpf}")
            print(f"RG: {loc.cliente.rg}")
            print(f"Período: {loc.data_inicio} até {loc.data_fim}")
            print("-" * 20)

if __name__ == "__main__":
    app = Locadora()
    app.menu()