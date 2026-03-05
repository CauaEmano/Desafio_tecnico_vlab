# Notas de Engenharia de Prompt 

Este documento detalha as estratégias, técnicas avançadas e decisões arquiteturais tomadas na construção dos prompts do Motor IA, visando atender perfis diversificados de aprendizado.

## 1. Abordagem Geral e Context Setting
Para garantir a personalização do ensino, foi utilizado um sistema dinâmico de injeção de variáveis (`Context Setting`). O prompt base não é estático; ele recebe o nome, idade, nível de conhecimento e estilo de aprendizado do aluno antes de ser enviado à API. Isso garante que o LLM adapte seu vocabulário e complexidade cognitiva especificamente para cada requisição.

Além disso, implementou-se o **Output Formatting**, forçando a IA a retornar os dados estritamente em um molde JSON predefinido, garantindo a integração perfeita com o front-end.

## 2. Versionamento e Evolução dos Prompts
Para permitir a comparação de qualidade, o sistema conta com duas versões distintas de `persona prompting` e estratégias pedagógicas:

### Versão 1: O Professor Estruturado (Chain-of-Thought)
* **Objetivo:** Oferecer uma explicação metódica e linear.
* **Técnica Principal:** `Chain-of-Thought` (CoT) explícito. 
* **Como funciona:** O prompt obriga a IA a pensar em 4 etapas lógicas (Diagnóstico, Estrutura Lógica, Consolidação e Aplicação). Em vez de apenas pedir "explique o assunto", o modelo é forçado a dividir o problema, o que reduz alucinações e melhora a precisão conceitual.

### Versão 2: O Tutor Socrático (Técnica de Feynman)
* **Objetivo:** Focar na compreensão profunda e na correção de rotas através de perguntas.
* **Técnica Principal:** Persona Socrática e Analogias Extremas (Feynman).
* **Como funciona:** O prompt obriga a IA a desenvolver o assunto a partir da construção de percepções do aluno. Em vez de apenas entregar tudo de bandeija, o modelo estimula o pensamento crítico e o raciocínio frente ao conteúdo

## 3. Controle Implícito e Explícito de Temperatura
Uma das inovações deste motor é o controle bidimensional da criatividade da IA:
1. **No Código (Explícito):** A temperatura matemática (parâmetro `temperature` da API) é ajustada dinamicamente:
   * Modo Preciso = 0.1 (Foco técnico, determinístico)
   * Modo Equilibrado = 0.7 (Uso cotidiano)
   * Modo Criativo = 1.4 (Analogias e narrativas)
2. **No Prompt (Implícito):** O texto do prompt também recebe a variável `{{modo_temperatura}}`, instruindo o modelo sobre *como* ele deve se comportar textualmente dentro daquela temperatura matemática.

## 4. Análise Comparativa de Resultados
A versão 1 mostrou-se ser mais técnica, mas ainda assim funcional, adaptando sua linguagem conforme o estudante.
Já a versão 2 mostrou-se mais criativa, apesar de ambas estarem na mesma `temperature`, a v2 trouxe consigo analogias que fizeram sentido para o aluno.