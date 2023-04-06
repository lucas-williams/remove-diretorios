import os
from pathlib import Path
def lista_usuarios():
    usuarios = Path.cwd() / 'usuarios.txt'
    comando_dsquery = f'dsquery user "ou=Usuários SOLARIUM,dc=solarium,dc=corp" | dsget user -samid -disabled > {usuarios}'

    with open(usuarios, 'r') as arquivo:
        conteudo = arquivo.read()
        usuarios_ativos_ad = [valor.title().replace('.', ' ') for indice, valor in enumerate(conteudo.split()[:-3:2]) if valor not in ['samid', 'disabled'] and conteudo.split()[indice * 2 + 1] == 'no']

        return usuarios_ativos_ad

print(lista_usuarios())