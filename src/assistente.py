from src.roteador import detectar_acao
from src.rag_system import buscar_produto, buscar_conhecimento
from src.prompts import gerar_prompt
from src.consulta_pedidos import consultar_status_pedido
from src.recomendador import recomendar_produto
from openai import OpenAI
import os
import re
import json

PEDIDOS_PATH = "data/pedidos.json"

class Assistente:
    def __init__(self):
        self.llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def responder(self, pergunta: str) -> str:
        acao = detectar_acao(pergunta)
        
        print(f"Acao: {acao}")
        
        if acao == "busca_produto":
            produtos = buscar_produto(pergunta)
            return "\n".join([f"- {p['nome']} (R${p['preco']})" for p in produtos]) or "Nenhum produto encontrado."
                
        elif acao == "politica_loja":
            contexto = buscar_conhecimento(pergunta)
            prompt = gerar_prompt(pergunta, contexto)
            resposta = self.llm.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            return resposta.choices[0].message.content.strip()
        
        elif acao == "consulta_pedido":
            return consultar_status_pedido(pergunta)
        
        elif acao == "recomendacao":
            return recomendar_produto(pergunta)
        
        return "Desculpe, não entendi sua solicitação. teste"
    
    def extrair_pedido_id(self, texto: str):
        match = re.search(r"#?(\d{4,})", texto)
        if match:
            return match.group(1)
        return None

    def consultar_pedido(self, pedido_id: str):
        with open(PEDIDOS_PATH, "r", encoding="utf-8") as f:
            pedidos = json.load(f)
        for pedido in pedidos:
            if pedido["pedido_id"] == pedido_id:
                return pedido
        return None
