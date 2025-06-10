def gerar_prompt(pergunta: str, contexto: str) -> str:
    return f"""
Você é um assistente virtual de e-commerce.
Contexto: {contexto}
Pergunta do usuário: {pergunta}
Responda de forma clara e objetiva.
"""
