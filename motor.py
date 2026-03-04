import json
from dotenv import load_dotenv
import os
from google import genai
import yaml
import hashlib

class MotorIA: #Classe principal
    def __init__(self, versao):
        load_dotenv() #Carregamento da chave API
        GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
        self.cliente = genai.Client(api_key=GEMINI_API_KEY)
        self.versao = versao

        with open('alunos.json', 'r', encoding='utf-8') as f:
            self.alunos = json.load(f) #Carregando os dados dos alunos

        with open('prompts.yaml', 'r', encoding='utf-8') as p:
            self.prompts = yaml.safe_load(p) #Carregando os prompts

        self.pasta_cache = 'cache'
        if not os.path.exists(self.pasta_cache): os.mkdir(f'./{self.pasta_cache}') #Criando a pasta cache

    def construir_prompt(self, aluno, topico, tipo_conteudo, modo):
        persona = self.prompts[self.versao]['persona_base']
        instrucao = self.prompts[self.versao]['tarefas'][tipo_conteudo]['instrucao']
        molde = self.prompts[self.versao]['tarefas'][tipo_conteudo]['molde']

        prompt_final = f'{persona}\n\nTarefa: {instrucao}\n\nMolde: {molde}'
        replacements = { #Dados a serem inseridos no prompt (extraído de prompts.yaml)
            "{{nome}}": aluno['nome'],
            "{{idade}}": str(aluno['idade']),
            "{{nivel}}": aluno['nivel'],
            "{{estilo}}": aluno['estilo'],
            "{{topico}}": topico,
            "{{modo_temperatura}}": modo
        }

        for um, outro in replacements.items(): #Replace entre os dados e as variáveis no prompt
            prompt_final = prompt_final.replace(um, outro)

        return prompt_final

    def gerar_conteudo(self, indice_aluno, topico, tipo_conteudo, modo):
        chave = self.gerar_chave_cache(self.alunos[indice_aluno], topico, tipo_conteudo, modo)
        valor = self.buscar_no_cache(chave) #Caso o pedido ja tenha sido feito, está salvo no cache
        if valor: 
            print('CACHE USADO')
            return valor

        modo = modo.capitalize()
        if modo == 'Preciso': valor=0.1 #Classficando a temperature baseado no modo escolhido
        elif modo == 'Equilibrado': valor=0.7
        else: valor= 1.4

        response = self.cliente.models.generate_content( #Instâncias dos modelos
            model='gemini-3-flash-preview',
            contents=self.construir_prompt(self.alunos[indice_aluno], topico, tipo_conteudo, modo),
            config= {
                'temperature': valor
            }
        )

        resposta = response.text.replace('```json', '').replace('```', '') #Garantindo limpeza da resposta
        resposta = json.loads(resposta) #Formatando resposta em json
        self.salvar_no_cache(chave, resposta)

        return resposta

    def gerar_chave_cache(self, aluno, topico, tipo_conteudo, modo):
        dados = f'{topico} - {aluno["nivel"]} - {aluno["estilo"]} - {tipo_conteudo} - {modo} - {self.versao}'
        return hashlib.md5(dados.encode()).hexdigest() #Chave de cache para identificação
    
    def buscar_no_cache(self, chave):
        cache_arquivo = os.path.join(self.pasta_cache, chave + '.json')
        if os.path.exists(cache_arquivo):
            with open(cache_arquivo, 'r', encoding='utf-8') as f:
                return json.load(f) #Caso o arquivo ja esteja em cache, permitir reutilização
        return None
    
    def salvar_no_cache(self, chave, conteudo):
        cache_arquivo = os.path.join(self.pasta_cache, chave + '.json')
        with open(cache_arquivo, 'w', encoding='utf-8') as f:
            json.dump(conteudo, f, indent=3, ensure_ascii=False) #Dump do arquivo no cache 