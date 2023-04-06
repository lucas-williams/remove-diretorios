import os

def limpar_diretorios(pasta, excecoes):
    diretorio = os.listdir(pasta)
    for arquivo in diretorio:
        caminho = os.path.join(pasta, arquivo)
        if os.path.isdir(pasta):
            if arquivo in excecoes:
                raise Exception(f"A exclusão do diretório '{arquivo}' foi cancelada")
            else:
                os.rmdir(caminho)
        else:
            if arquivo in excecoes:
                raise Exception(f"A exclusão do arquivo '{arquivo}' foi cancelada")
            else:
                os.remove(caminho)
    print('Todo conteúdo da pasta %s foi excluído' % (pasta))
