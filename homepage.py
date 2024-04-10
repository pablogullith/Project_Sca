import os
import json 
from usuario import Usuario

class HomePage:
    def __init__(self, usuario):
        self.usuario = usuario
        self.arquivo_grupos_disponiveis = 'grupos_disponiveis.txt'
        self.grupos_disponiveis = self.carregar_grupos_disponiveis()

    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def exibir_home_page(self):
        self.limpar_tela()
        print(f"Bem-vindo à Home Page, {self.usuario.nickname}!")
        print("1. Grupos que você está")
        print("2. Criar um grupo")
        print("3. Entrar em um grupo existente")
        print("4. Ver atividades por grupo")
        print("5. Ver ranking")
        print("6. Sair")

    def carregar_grupos(self):
        return self.usuario.carregar_grupos()

    def salvar_grupos(self):
        self.usuario.salvar_grupos()

    def ver_grupos(self):
        self.usuario.ver_grupos()    

    def ver_grupos(self):
        print("\nEstes são os grupos em que você está: ")
        for i, grupo in enumerate(self.usuario.grupos, 1):
            print(f"{i}. {grupo['nome']}")

        escolha_grupo = input("\nEscolha um grupo pelo número (ou pressione Enter para voltar): ")
        if escolha_grupo.isdigit() and 1 <= int(escolha_grupo) <= len(self.usuario.grupos):
            grupo_escolhido = self.usuario.grupos[int(escolha_grupo) - 1]
            print(f"\nVocê escolheu o grupo {grupo_escolhido['nome']}.")

            while True:
                print("\n1. Registrar Atividades")
                print("2. Excluir Grupo")
                print("3. Voltar")

                escolha_opcao_grupo = input("\nEscolha uma opção (1/2/3): ")

                if escolha_opcao_grupo == '1':
                    self.registrar_atividades_no_grupo(grupo_escolhido)
                elif escolha_opcao_grupo == '2':
                    self.excluir_grupo(grupo_escolhido)
                    break
                elif escolha_opcao_grupo == '3':
                    break
                else:
                    print("\nOpção inválida. Tente novamente.")
        elif not escolha_grupo:
            pass  # Usuário escolheu voltar, não faz nada
        else:
            print("Escolha inválida.")


    def registrar_atividades_no_grupo(self, grupo):
        atividade = input("\nDigite a atividade física realizada: ")
        pontuacao = input("\nDigite a pontuação da atividade: ")

        if "atividades" not in grupo:
            grupo["atividades"] = []

        grupo["atividades"].append({"atividade": atividade, "pontuacao": pontuacao})
        self.salvar_grupos()

        print("\nAtividade registrada com sucesso!")

    def excluir_grupo(self, grupo):
        confirmacao = input("\nTem certeza que deseja excluir este grupo? (s/n): ").lower()
        if confirmacao == 's':
            self.usuario.grupos.remove(grupo)
            self.salvar_grupos()
            print(f"\nGrupo {grupo['nome']} excluído com sucesso!")
        else:
            print("\nOperação de exclusão cancelada.")
    
        

    def ver_atividades_e_total(self):
        print("\nAtividades registradas e pontuação total:\n")
        
        rankings = {}

        for grupo in self.usuario.grupos:
            nome_grupo = grupo['nome']
            print(f"\nGrupo: {nome_grupo}")

            if 'atividades' in grupo:
                total_pontos_grupo = 0
                for atividade in grupo['atividades']:
                    print(f"Atividade: {atividade['atividade']}, Pontuação: {atividade['pontuacao']}")
                    total_pontos_grupo += int(atividade['pontuacao'])
                
                if nome_grupo not in rankings:
                    rankings[nome_grupo] = {}

                usuario = self.usuario.nickname
                rankings[nome_grupo][usuario] = total_pontos_grupo
                print(f"Pontuação total: {total_pontos_grupo}")

            else:
                print("Nenhuma atividade registrada.")
                if nome_grupo not in rankings:
                    rankings[nome_grupo] = {}
                    print("Pontuação total: 0")

    
    def ver_ranking_global(self):
        grupos_usuario = [grupo['nome'] for grupo in self.usuario.grupos]

        print("\nGrupos disponíveis para ver o ranking global:")
        for i, grupo in enumerate(grupos_usuario, 1):
            print(f"{i}. {grupo}")

        escolha_grupo = input("\nEscolha um grupo pelo número: ")
        if escolha_grupo.isdigit() and 1 <= int(escolha_grupo) <= len(grupos_usuario):
            nome_grupo_escolhido = grupos_usuario[int(escolha_grupo) - 1]
            self.exibir_ranking_grupo(nome_grupo_escolhido)
        else:
            print("\nEscolha inválida.")


    def exibir_ranking_grupo(self, nome_grupo):
        rankings = {}

        for usuario in self.carregar_usuarios():
            for grupo in usuario.grupos:
                if grupo['nome'] == nome_grupo and 'atividades' in grupo:
                    total_pontos_grupo = 0
                    for atividade in grupo['atividades']:
                        pontuacao = int(atividade['pontuacao'])
                        total_pontos_grupo += pontuacao

                    usuario_nome = usuario.nickname
                    if usuario_nome not in rankings:
                        rankings[usuario_nome] = 0

                    rankings[usuario_nome] += total_pontos_grupo

        print(f"\nRanking Global de Pontuações no Grupo {nome_grupo}:")
        ranking_ordenado = sorted(rankings.items(), key=lambda x: x[1], reverse=True)

        for i, (usuario, pontuacao) in enumerate(ranking_ordenado, 1):
            print(f"{i}. {usuario}: {pontuacao} pontos")



    def carregar_usuarios(self):
        usuarios = []

        for arquivo_usuario in os.listdir('.'):
            if arquivo_usuario.endswith('_grupos.txt'):
                nickname = arquivo_usuario.replace('_grupos.txt', '')
                usuario = Usuario(nickname, '', '')  # Você pode ajustar conforme necessário
                usuarios.append(usuario)

        return usuarios
         

    def criar_grupo(self):
        nome_grupo = input("\nDigite o nome do novo grupo: ")
        novo_grupo = {"nome": nome_grupo}
        self.usuario.grupos.append(novo_grupo)
        self.salvar_grupos()

        # Adiciona o novo grupo à lista de grupos disponíveis
        self.grupos_disponiveis.append(nome_grupo)
        self.salvar_grupos_disponiveis()

        print(f"\nGrupo {nome_grupo} criado com sucesso!")

    def entrar_grupo(self):
        print("\nGrupos disponíveis para entrar:\n")
        grupos_disponiveis = self.carregar_grupos_disponiveis()

        for i, grupo in enumerate(grupos_disponiveis, 1):
            print(f"{i}. {grupo}")

        escolha_grupo = input("\nEscolha um grupo pelo número (ou pressione Enter para voltar): ")
        if escolha_grupo.isdigit() and 1 <= int(escolha_grupo) <= len(grupos_disponiveis):
            nome_grupo_escolhido = grupos_disponiveis[int(escolha_grupo) - 1]
            print(f"\nSeja bem-vindo ao grupo {nome_grupo_escolhido}!")
            novo_grupo = {"nome": nome_grupo_escolhido}
            self.usuario.grupos.append(novo_grupo)
            self.salvar_grupos()
        else:
            print("Escolha inválida.")

    def carregar_grupos_disponiveis(self):
        try:
            with open(self.arquivo_grupos_disponiveis, 'r') as arquivo:
                grupos_disponiveis = json.loads(arquivo.read())
            if not isinstance(grupos_disponiveis, list):
                raise Exception()
        except:
            grupos_disponiveis = []
        return grupos_disponiveis

    def salvar_grupos_disponiveis(self):
        with open(self.arquivo_grupos_disponiveis, 'w') as arquivo:
            arquivo.write(json.dumps(self.grupos_disponiveis, indent=4))

    def executar(self):
        while True:
            self.exibir_home_page()
            escolha = input("\nEscolha uma opção (1/2/3/4/5/6): ")

            if escolha == '1':
                self.ver_grupos()
            elif escolha == '2':
                self.criar_grupo()
            elif escolha == '3':
                self.entrar_grupo()
            elif escolha == '4':
                self.ver_atividades_e_total() 
            elif escolha == '5':
                self.ver_ranking_global()     
            elif escolha == '6':
                print("\nSaindo do programa. Até logo!")    
                self.salvar_grupos()
                break
            else:
                print("\nOpção inválida. Tente novamente.")
            
            input("\nPressione Enter para continuar...")