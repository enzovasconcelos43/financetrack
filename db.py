"""
Módulo de conexão com o banco de dados Supabase.
Substitui a persistência local que usava o financas.json.
"""

import os

from dotenv import load_dotenv
from supabase import Client, create_client

# Lê as variáveis secretas do arquivo .env
load_dotenv()


def get_client() -> Client:
    """Cria e retorna a conexão com o Supabase."""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("SUPABASE_URL e SUPABASE_KEY não encontrados no .env")
    return create_client(url, key)


def buscar_transacoes() -> list:
    """Busca todas as transações salvas no banco, em ordem cronológica."""
    client = get_client()
    response = client.table("transacoes").select("*").order("created_at").execute()
    return response.data


def inserir_transacao(tipo: str, descricao: str, valor: float) -> dict:
    """Grava uma nova transação (receita ou despesa) no banco."""
    client = get_client()
    response = (
        client.table("transacoes")
        .insert({"tipo": tipo, "descricao": descricao, "valor": abs(valor)})
        .execute()
    )
    return response.data[0] if response.data else {}
    
def buscar_transacoes_por_tipo(tipo: str) -> list:
    """Busca transações filtrando por tipo (receita ou despesa)."""
    client = get_client()
    response = (
        client.table("transacoes")
        .select("*")
        .eq("tipo", tipo)
        .order("created_at")
        .execute()
    )
    return response.data
