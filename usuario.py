import json

class Usuario:
    def __init__(self, nickname, email, senha):
        self.nickname = nickname
        self.email = email
        self.senha = senha
        self.arquivo_grupos = f'{nickname}_grupos.txt'
        self.grupos = self.carregar_grupos()

    def to_dict(self):
        return {"nickname": self.nickname, "email": self.email, "senha": self.senha}

    def carregar_grupos(self):
        try:
            with open(self.arquivo_grupos, 'r') as arquivo:
                grupos = json.loads(arquivo.read())
            if not isinstance(grupos, list):
                raise Exception()
        except:
            grupos = []
        return grupos

    def salvar_grupos(self):
        with open(self.arquivo_grupos, 'w') as arquivo:
            arquivo.write(json.dumps(self.grupos, indent=4))