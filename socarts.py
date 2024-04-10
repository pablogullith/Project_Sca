import os
import json
from usuario import Usuario 
from homepage import HomePage

class Socarts:
    def __init__(self):
        print("🅂🄾🄲🄰🅁🅃🅂\n")
        self.menu()

    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def menu(self):
        print("1. Entrar")
        print("2. Cadastrar")
        print("3. Sair")

    def entrar(self):
        print("\nVocê escolheu entrar. ")
        email = input("\nEntre com seu email: ")
        senha = input("\nEntre com sua senha: ")

        try:
            with open('dados_usuarios.txt', 'r') as arquivo:
                users = json.loads(arquivo.read())
            if not isinstance(users, list):
                raise Exception()
        except:
            users = []

        usuario_encontrado = False
        for user in users:
            if user["email"] == email and user["senha"] == senha:
                usuario_encontrado = True
                print(f"\nSeja bem-vindo, {user['nickname']}!")
                usuario = Usuario(user['nickname'], user['email'], user['senha'])
                home_page = HomePage(usuario)
                home_page.executar()
                break

        if not usuario_encontrado:
            print("\nLogin ou senha não existe.")

    def cadastrar(self):
        print("\nVocê escolheu cadastrar. ")
        nickname = input("\nEntre com o seu nickname: ")
        cadastrar_email = input("\nCadastre seu email: ")
        cadastrar_senha = input("\nCadastre sua senha: ")
        user = {
            "nickname": nickname,
            "email": cadastrar_email,
            "senha": cadastrar_senha
        }
        try:
            with open('dados_usuarios.txt', 'r') as arquivo:
                users = json.loads(arquivo.read())
            if not isinstance(users, list):
                raise Exception()
        except:
            users = []
        users.append(user)

        with open('dados_usuarios.txt', 'w') as arquivo:
            arquivo.write(json.dumps(users, indent=4))

    def executar(self):
        while True:
            self.limpar_tela()
            self.menu()
            escolha = input("\nEscolha uma opção (1/2/3): ")

            if escolha == '1':
                self.entrar()
            elif escolha == '2':
                self.cadastrar()
            elif escolha == '3':
                print("\nSaindo do programa. Até logo!")
                self.limpar_tela()
                break
            else:
                print("\nOpção inválida. Tente novamente.")

            input("\nPressione Enter para continuar...")
