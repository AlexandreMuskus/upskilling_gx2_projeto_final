# src/recomendador.py
import json

def recomendar_produto(pergunta: str) -> str:
    print(f"Pergunta recebida para recomendação: {pergunta}")
    try:
        with open("data/produtos.json", "r") as f:
            produtos = json.load(f)
    except FileNotFoundError:
        return "Catálogo de produtos não encontrado."

    palavras_chave = {
        "cozinhar": ["panela", "liquidificador", "air fryer", "forno"],
        "tecnologia": ["notebook", "smartphone", "tablet", "fones", "gadget"],
        "gamer": ["console", "monitor", "teclado", "mouse", "cadeira gamer"],
        "viagem": ["mochila", "fones", "carregador", "powerbank"]
    }

    recomendadas = []
    for tema, palavras in palavras_chave.items():
        if tema in pergunta.lower():
            for produto in produtos:
                if any(palavra in produto["nome"].lower() for palavra in palavras):
                    recomendadas.append(produto)

    if not recomendadas:
        return "Não encontrei recomendações específicas, mas posso ajudar com sugestões se você quiser me contar mais."

    resposta = "Recomendações para você:\n"
    for p in recomendadas[:5]:  # Limita a 5 sugestões
        resposta += f"- {p['nome']} (R${p['preco']:.2f})\n"

    return resposta.strip()
