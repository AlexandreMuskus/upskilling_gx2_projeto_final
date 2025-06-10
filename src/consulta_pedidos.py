# src/consulta_pedidos.py
import json
import re

def consultar_status_pedido(pergunta: str) -> str:
    # Expressão regular para capturar números de pedido (ex: 12345)
    match = re.search(r"#?(\d{4,})", pergunta)
    if not match:
        return "Por favor, informe o número do pedido (ex: #12345)."

    pedido_id = match.group(1)

    try:
        with open("data/pedidos.json", "r") as f:
            pedidos = json.load(f)

        for pedido in pedidos:
            if pedido["pedido_id"] == pedido_id:
                return (
                    f"Status do pedido #{pedido_id}: {pedido['status']}.\n"
                    f"Data da compra: {pedido['data_compra']}\n"
                    f"Previsão de entrega: {pedido['previsao_entrega']}"
                )

        return f"Não encontrei informações para o pedido #{pedido_id}."
    
    except FileNotFoundError:
        return "Base de pedidos não encontrada."
