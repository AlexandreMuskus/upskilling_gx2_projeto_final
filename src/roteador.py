# src/roteador.py
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def detectar_acao(pergunta: str) -> str:
    prompt = f"""
Classifique a intenção da pergunta do usuário abaixo em uma das seguintes opções:

- "busca_produto"
- "politica_loja"
- "consulta_pedido"
- "recomendacao"

Pergunta: "{pergunta}"

Responda apenas com a categoria exata.
"""
    resposta = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return resposta.choices[0].message.content.strip().lower().replace('"', "")
