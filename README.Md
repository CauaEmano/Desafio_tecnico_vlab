# Motor IA - Gerador de Conteúdo Educativo

Este projeto é uma plataforma educativa desenvolvida para o Desafio Técnico de Estágio dev.IA/Prompt. A aplicação recebe tópicos e características de alunos (nível, idade, estilo de aprendizado) e gera materiais educativos personalizados usando técnicas avançadas de Engenharia de Prompt.

## Funcionalidades

* **Geração Dinâmica:** Cria explicações (Chain-of-Thought e Feynman), exemplos práticos, perguntas de reflexão e resumos visuais.
* **Interface Web:** Interface simples e intuitiva construída com HTML, CSS e Axios, comunicando-se com um back-end Flask.
* **Controle de Temperatura:** Ajuste explícito e implícito do nível de criatividade da IA (Preciso, Equilibrado, Criativo).
* **Sistema de Cache Local:** Evita chamadas redundantes à API, economizando tokens e tempo de resposta através de chaves Hash MD5.
* **Versionamento de Prompts:** Arquitetura que permite comparar a qualidade gerada entre diferentes abordagens pedagógicas.
* **Persistência de Dados:** Salvamento automático de todos os materiais gerados em arquivos `.json` estruturados na pasta `/samples`.

## Tecnologias Utilizadas

* **Back-end:** Python 3.12, Flask
* **Front-end:** HTML5, JavaScript (Axios)
* **IA/LLM:** Google Gemini API (gemini-3-flash-preview)
* **Outros:** `python-dotenv` (gerenciamento de variáveis), `pyyaml` (estruturação de prompts).

## Configuração e Instalação (Setup)

Siga os passos abaixo para rodar o projeto localmente:

1. **Clone o repositório:**
    ```bash
    git clone https://github.com/CauaEmano/Desafio_tecnico_vlab
    cd Desafio_tecnico_vlab
    ```

2. **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate #No Linux/Mac
    venv\Scripts\activate #No Windows
    ```

3. **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configuração da API:**
    * Renomeie o arquivo .env.example para .env
    * Insira a sua chave da API do Google Gemini:
        `GEMINI_API_KEY=sua_chave_aqui`

## Como Executar

Com o ambiente ativado e as dependências instaladas, inicie o servidor Flask:
```bash
python app.py
```
Acesse a interface da aplicação no seu navegador através do endereço:
`http://127.0.0.1:5000`

## Estrutura do Projeto

* `app.py`: Servidor Flask e rotas da aplicação web.
* `motor.py`: Classe principal (MotorIA) que gerencia a comunicação com a API, cache e construção de prompts.
* `menu.py`: Funções auxiliares (como salvar_resultado).
* `prompts.yaml`: Arquivo com as versões dos prompts (Engenharia de Prompt) .
* `alunos.json`: Base de dados dos perfis de alunos .
* `templates/index.html`: Interface web do usuário.
* `/cache`: Diretório gerado automaticamente para armazenar requisições em cache.
* `/samples`: Diretório com exemplos de outputs finais em JSON.
* `PROMPT_ENGINEERING_NOTES.md`: Documentação detalhada sobre as escolhas de design dos prompts.