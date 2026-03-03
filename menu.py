from motor import MotorIA 
from datetime import datetime
import os
import json

def salvar_resultado(aluno, topico, lista_conteudos):
    resultado = {
        'metadata': {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'topico': topico
        },
        'perfil_aluno': aluno,
        'materiais': lista_conteudos
    }

    if not os.path.exists('samples'): os.makedirs('./samples')
    caminho = os.path.join('samples', f'{resultado['metadata']['timestamp']} - ' + aluno['nome'] + ' - ' + topico)

    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False)

def menu():
    app = MotorIA()
    
    print('\nAlunos Disponíveis:')
    for i, aluno in enumerate(app.alunos):
        print(f'[{i}] {aluno}')

    indice_aluno = int(input('\nDigite o número respectivo ao aluno a ser escolhido: '))
    topico = input('Digite o tópico a ser estudado: ')

    print("\n--- O que deseja gerar? ---")
    print("1. Explicação Conceitual (Chain-of-Thought)")
    print("2. Exemplos Práticos (Contextualizados)")
    print("3. Perguntas de Reflexão")
    print("4. Resumo Visual (ASCII/Mapa Mental)")
    print("5. Gerar todos os anteriores")
    
    opcao = input("\nEscolha (1-5): ")

    mapa_tarefas = {
        "1": [("explicacao", "Explicação Conceitual", "Chain-of-Thought")],
        "2": [("exemplos", "Exemplos Práticos", "Contextualização")],
        "3": [("reflexao", "Perguntas de Reflexão", "Pensamento Crítico")],
        "4": [("resumo", "Resumo Visual", "ASCII/Diagrama")],
        "5": [
            ("explicacao", "Explicação Conceitual", "Chain-of-Thought"),
            ("exemplos", "Exemplos Práticos", "Contextualização"),
            ("reflexao", "Perguntas de Reflexão", "Pensamento Crítico"),
            ("resumo", "Resumo Visual", "ASCII/Diagrama")
        ]
    }

    selecionados =  mapa_tarefas.get(opcao, [])
    if not selecionados:
        print('Opção Inválida')
        return None
    
    resultados_finais = []

    for i, l, g in selecionados:
        resposta = app.gerar_conteudo(indice_aluno, topico, i)
        resultados_finais.append({
            'Técnica': g,
            'label': l
        })

        print(resposta) 

    salvar_resultado(app.alunos[indice_aluno], topico, resultados_finais)

if __name__ == '__main__':
    menu()