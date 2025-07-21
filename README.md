## Guia de Uso - Atividade com Assistente

### 1. Pré‑requisitos

* Python ≥ 3.10. Baixe [aqui](https://www.python.org/downloads/) se ainda não tiver.
* Conta na OpenAI e **OPENAI\_API\_KEY** válida.

### 2. Clone e crie um ambiente virtual

### 2.1 Crie um ambiente virtual
- Verifique sua versão do Python, algumas vezes pode ser necessário tentar com python3 ao invés de python.
```bash
cd chatbot_app
python -m venv .venv_aula_prompt
```

### 2.2 Ative ele para garantir que os pacotes sejam instalados apenas nele.
```bash
# Linux/macOS
source .venv_aula_prompt/bin/activate
# Windows (PowerShell)
.venv_aula_prompt\Scripts\Activate.ps1
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as chaves

Crie um arquivo **.env** na raiz com o seguinte conteúdo (ajuste se usar outro modelo):

```
OPENAI_API_KEY=sk-SUA_CHAVE_AQUI
OPENAI_MODEL=gpt-4.1-nano
PERSONA_MODEL=gpt-3.5-turbo-0125
```

> **Nunca** faça commit do arquivo `.env`. Adicione no .gitignore sempre

### 5. Rode a aplicação

```bash
export FLASK_APP=chatbot.wsgi        # Linux/macOS
$env:FLASK_APP="chatbot.wsgi"        # Windows PowerShell
flask run
```

A aplicação estará disponível em [http://localhost:5000](http://localhost:5000).

### 6. Criando seu próprio agente

1. **Edite** o arquivo‑modelo `agents/meu_agente.yaml`.

2. **Edite** os campos do YAML:
   | Campo | O que alterar  |
   | ----- | ------------   |
   | `name`| Nome do agente |
   | `description` | Breve descrição de referência, por hora não será aplicada a nada (mas poderia ir na interface) |
   | `instructions` | -Prompt-Sistema que orienta o modelo |
   | `pdf` (opcional) | - **sem RAG** → deixe vazio, sem nenhum valor para a chave PDF <br><br>- **com RAG** → coloque o PDF na pasta `chatbot/documents` e escreva aqui o nome completo do arquivo, incluindo `.pdf`. |

