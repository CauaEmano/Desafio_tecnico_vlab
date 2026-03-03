import json

def carregar_arquivo(arquivo):

    try:
        with open(arquivo, 'r', encoding='utf-8') as al:
            perfis = json.load(al)
    except FileNotFoundError:
        return {}
    
    return perfis

