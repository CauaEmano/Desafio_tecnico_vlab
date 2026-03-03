import json
from dotenv import load_dotenv
import os
from google import genai
import yaml
import hashlib

class MotorIA:
    def __init__(self):
        load_dotenv()
        GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
        self.cliente = genai.Client(api_key=GEMINI_API_KEY)

        with open('alunos.json', 'r', encoding='utf-8') as f:
            self.alunos = json.load(f)

        with open('prompts.yaml', 'r', encoding='utf-8') as p:
            self.prompts = yaml.safe_load(p)

        self.pasta_cache = 'cache'
        if not os.path.exists(self.pasta_cache):
            os.mkdir(f'./{self.pasta_cache}')

    def construir_prompt(self, aluno, topico, tipo_conteudo):
        persona = self.prompts['persona_base']
        instrucao = self.prompts['tarefas'][tipo_conteudo]['instrucao']
        molde = self.prompts['tarefas'][tipo_conteudo]['molde']

        prompt_final = f'{persona}\n\nTarefa: {instrucao}\n\nMolde: {molde}'
        replacements = {
            "{{nome}}": aluno['nome'],
            "{{idade}}": str(aluno['idade']),
            "{{nivel}}": aluno['nivel'],
            "{{estilo}}": aluno['estilo'],
            "{{topico}}": topico
        }

        for um, outro in replacements.items():
            prompt_final = prompt_final.replace(um, outro)

        return prompt_final

    def gerar_conteudo(self, indice_aluno, topico, tipo_conteudo):
        chave = self.gerar_chave_cache(self.alunos[indice_aluno], topico, tipo_conteudo)
        valor = self.buscar_no_cache(chave)
        if valor:
            print('CACHE USADO')
            return valor
    
        response = self.cliente.models.generate_content(
            model='gemini-3-flash-preview',
            contents=self.construir_prompt(self.alunos[indice_aluno], topico, tipo_conteudo)
        )

        resposta = response.text.replace('```json', '').replace('```', '')
        resposta = json.loads(resposta)
        self.salvar_no_cache(chave, resposta)

        return resposta

    def gerar_chave_cache(self, aluno, topico, tipo_conteudo):
        dados = f'{topico} - {aluno["nivel"]} - {aluno["estilo"]} - {tipo_conteudo}'
        return hashlib.md5(dados.encode()).hexdigest()
    
    def buscar_no_cache(self, chave):
        cache_arquivo = os.path.join(self.pasta_cache, chave + '.json')
        if os.path.exists(cache_arquivo):
            with open(cache_arquivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def salvar_no_cache(self, chave, conteudo):
        cache_arquivo = os.path.join(self.pasta_cache, chave + '.json')
        with open(cache_arquivo, 'w', encoding='utf-8') as f:
            json.dump(conteudo, f, indent=3, ensure_ascii=False)