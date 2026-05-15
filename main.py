"""
FinanceTrack CLI — Gestão Financeira com Cotações de Moedas
Versão: 1.0.0
Autor: Seu Nome
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

import requests

# ──────────────────────────────────────────────
# CONFIGURAÇÕES GLOBAIS
# ──────────────────────────────────────────────

AWESOMEAPI_BASE_URL = "https://economia.awesomeapi.com.br/json"
DATA_FILE = Path("financas.json")

MOEDAS_DISPONIVEIS = {
    "1": ("USD-BRL", "Dólar Americano → Real"),
    "2": ("EUR-BRL", "Euro → Real"),
    "3": ("BTC-BRL", "Bitcoin → Real"),
    "4": ("GBP-BRL", "Libra Esterlina → Real"),
    "5": ("ARS-BRL", "Peso Argentino → Real"),
    "6": ("JPY-BRL", "Iene Japonês → Real"),
}


# ──────────────────────────────────────────────
# FUNÇÕES DE API
# ──────────────────────────────────────────────


def buscar_cotacao(par_moeda: str) -> dict | None:
    """
    Busca a cotação de um par de moedas na AwesomeAPI.

    Args:
        par_moeda: Par no formato 'USD-BRL', 'EUR-BRL', etc.

    Returns:
        Dicionário com dados da cotação ou None em caso de erro.
    """
    url = f"{AWESOMEAPI_BASE_URL}/last/{par_moeda}"
    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()
        chave = par_moeda.replace("-", "")
        return dados.get(chave)
    except requests.exceptions.ConnectionError:
        print("  ❌ Erro: Sem conexão com a internet.")
        return None
    except requests.exceptions.Timeout:
        print("  ❌ Erro: A requisição demorou demais (timeout).")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"  ❌ Erro HTTP: {e}")
        return None
    except (KeyError, json.JSONDecodeError):
        print("  ❌ Erro: Resposta inesperada da API.")
        return None


# ──────────────────────────────────────────────
# FUNÇÕES DE DADOS (persistência em JSON)
# ──────────────────────────────────────────────


def carregar_dados() -> dict:
    """Carrega as finanças salvas do arquivo JSON local."""
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"transacoes": [], "saldo_inicial": 0.0}


def salvar_dados(dados: dict) -> None:
    """Salva as finanças no arquivo JSON local."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


# ──────────────────────────────────────────────
# FUNÇÕES DE LÓGICA FINANCEIRA
# ──────────────────────────────────────────────


def calcular_saldo(dados: dict) -> float:
    """
    Calcula o saldo atual com base nas transações.

    Args:
        dados: Dicionário com 'saldo_inicial' e 'transacoes'.

    Returns:
        Saldo atual em float.
    """
    saldo = dados.get("saldo_inicial", 0.0)
    for t in dados.get("transacoes", []):
        if t["tipo"] == "receita":
            saldo += t["valor"]
        else:
            saldo -= t["valor"]
    return saldo


def adicionar_transacao(dados: dict, tipo: str, descricao: str, valor: float) -> dict:
    """
    Adiciona uma transação (receita ou despesa).

    Args:
        dados: Dicionário atual de finanças.
        tipo: 'receita' ou 'despesa'.
        descricao: Texto descritivo da transação.
        valor: Valor monetário (positivo).

    Returns:
        Dicionário atualizado com a nova transação.
    """
    transacao = {
        "id": len(dados["transacoes"]) + 1,
        "tipo": tipo,
        "descricao": descricao,
        "valor": abs(valor),
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
    }
    dados["transacoes"].append(transacao)
    return dados


def converter_valor(valor_brl: float, cotacao: float) -> float:
    """
    Converte um valor em BRL para moeda estrangeira.

    Args:
        valor_brl: Valor em reais.
        cotacao: Cotação (quantos reais vale 1 unidade da moeda).

    Returns:
        Valor convertido na moeda estrangeira.
    """
    if cotacao <= 0:
        raise ValueError("Cotação deve ser maior que zero.")
    return valor_brl / cotacao


# ──────────────────────────────────────────────
# FUNÇÕES DE INTERFACE (menus e exibição)
# ──────────────────────────────────────────────


def limpar_tela() -> None:
    """Limpa o terminal de forma multiplataforma."""
    os.system("cls" if os.name == "nt" else "clear")


def cabecalho() -> None:
    """Exibe o cabeçalho visual da aplicação."""
    print("\n" + "═" * 50)
    print("  💰  FinanceTrack CLI  v1.0.0")
    print("  Gestão Financeira + Cotações em Tempo Real")
    print("═" * 50)


def menu_cotacoes() -> None:
    """Exibe o submenu de cotações e processa a escolha."""
    print("\n📊  COTAÇÕES DE MOEDAS")
    print("─" * 30)
    for num, (par, descricao) in MOEDAS_DISPONIVEIS.items():
        print(f"  [{num}] {descricao}")
    print("  [0] Voltar ao menu principal")

    escolha = input("\n  Escolha uma moeda: ").strip()

    if escolha == "0":
        return

    if escolha not in MOEDAS_DISPONIVEIS:
        print("  ⚠️  Opção inválida.")
        return

    par, descricao = MOEDAS_DISPONIVEIS[escolha]
    print(f"\n  🔄 Buscando cotação de {descricao}...")
    dados_cotacao = buscar_cotacao(par)

    if dados_cotacao:
        bid = float(dados_cotacao.get("bid", 0))
        ask = float(dados_cotacao.get("ask", 0))
        pct = float(dados_cotacao.get("pctChange", 0))
        nome = dados_cotacao.get("name", descricao)
        data_hora = dados_cotacao.get("create_date", "N/A")

        sinal = "📈" if pct >= 0 else "📉"
        print(f"\n  ✅  {nome}")
        print(f"  Compra  : R$ {bid:.4f}")
        print(f"  Venda   : R$ {ask:.4f}")
        print(f"  Variação: {sinal} {pct:+.2f}%")
        print(f"  Hora    : {data_hora}")

        # Oferecer conversão
        print("\n  Deseja converter um valor? (s/n): ", end="")
        if input().strip().lower() == "s":
            try:
                valor_str = input("  Digite o valor em R$: ").replace(",", ".")
                valor = float(valor_str)
                moeda_sigla = par.split("-")[0]
                convertido = converter_valor(valor, bid)
                print(
                    f"\n  R$ {valor:.2f} = {convertido:.4f} {moeda_sigla} "
                    f"(cotação de compra)"
                )
            except ValueError:
                print("  ⚠️  Valor inválido. Digite apenas números.")


def menu_financas(dados: dict) -> dict:
    """Exibe o submenu de gestão financeira."""
    saldo = calcular_saldo(dados)

    print("\n💼  GESTÃO FINANCEIRA")
    print("─" * 30)
    print(f"  Saldo atual: R$ {saldo:.2f}")
    print("\n  [1] Adicionar Receita")
    print("  [2] Adicionar Despesa")
    print("  [3] Ver Extrato")
    print("  [4] Definir Saldo Inicial")
    print("  [0] Voltar")

    escolha = input("\n  Escolha: ").strip()

    if escolha == "1":
        descricao = input("  Descrição da receita: ").strip()
        try:
            valor = float(input("  Valor (R$): ").replace(",", "."))
            dados = adicionar_transacao(dados, "receita", descricao, valor)
            salvar_dados(dados)
            print(f"  ✅ Receita de R$ {valor:.2f} adicionada!")
        except ValueError:
            print("  ⚠️  Valor inválido.")

    elif escolha == "2":
        descricao = input("  Descrição da despesa: ").strip()
        try:
            valor = float(input("  Valor (R$): ").replace(",", "."))
            dados = adicionar_transacao(dados, "despesa", descricao, valor)
            salvar_dados(dados)
            print(f"  ✅ Despesa de R$ {valor:.2f} adicionada!")
        except ValueError:
            print("  ⚠️  Valor inválido.")

    elif escolha == "3":
        print("\n  📋  EXTRATO")
        print("  " + "─" * 46)
        if not dados["transacoes"]:
            print("  Nenhuma transação registrada.")
        for t in dados["transacoes"]:
            simbolo = "+" if t["tipo"] == "receita" else "-"
            cor = "💚" if t["tipo"] == "receita" else "🔴"
            print(
                f"  {cor} #{t['id']:03d} | {t['data']} | "
                f"{simbolo}R$ {t['valor']:>10.2f} | {t['descricao']}"
            )
        print("  " + "─" * 46)
        print(f"  {'SALDO ATUAL':>30}: R$ {saldo:.2f}")

    elif escolha == "4":
        try:
            saldo_novo = float(input("  Saldo inicial (R$): ").replace(",", "."))
            dados["saldo_inicial"] = saldo_novo
            salvar_dados(dados)
            print(f"  ✅ Saldo inicial definido como R$ {saldo_novo:.2f}")
        except ValueError:
            print("  ⚠️  Valor inválido.")

    return dados


# ──────────────────────────────────────────────
# PONTO DE ENTRADA PRINCIPAL
# ──────────────────────────────────────────────


def main() -> None:
    """Loop principal da aplicação CLI."""
    dados = carregar_dados()

    while True:
        cabecalho()
        print("\n  [1] 📊 Cotações de Moedas")
        print("  [2] 💼 Gestão Financeira")
        print("  [0] 🚪 Sair")

        escolha = input("\n  Digite sua opção: ").strip()

        if escolha == "1":
            menu_cotacoes()
            input("\n  Pressione ENTER para continuar...")

        elif escolha == "2":
            dados = menu_financas(dados)
            input("\n  Pressione ENTER para continuar...")

        elif escolha == "0":
            print("\n  Até logo! 👋\n")
            sys.exit(0)

        else:
            print("\n  ⚠️  Opção inválida. Tente novamente.")
            input("  Pressione ENTER para continuar...")


if __name__ == "__main__":
    main()
