"""
Testes Unitários e de Integração — FinanceTrack CLI
Execução: pytest test_main.py -v
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Importa todas as funções do nosso projeto
from main import (
    AWESOMEAPI_BASE_URL,
    adicionar_transacao,
    buscar_cotacao,
    calcular_saldo,
    carregar_dados,
    converter_valor,
    salvar_dados,
)


# ──────────────────────────────────────────────
# FIXTURES (dados reutilizáveis entre os testes)
# ──────────────────────────────────────────────


@pytest.fixture
def dados_vazios():
    """Retorna uma estrutura de dados financeiros vazia."""
    return {"transacoes": [], "saldo_inicial": 0.0}


@pytest.fixture
def dados_com_transacoes():
    """Retorna uma estrutura de dados com transações pré-existentes."""
    return {
        "saldo_inicial": 1000.0,
        "transacoes": [
            {"id": 1,
             "tipo": "receita", 
             "descricao": "Salário", 
             "valor": 3000.0, 
             "data": "01/06/2025"},
            
            {"id": 2, 
             "tipo": "despesa", 
             "descricao": "Aluguel", 
             "valor": 1200.0, 
             "data": "02/06/2025"},
            
            {"id": 3, 
             "tipo": "despesa", 
             "descricao": "Mercado", 
             "valor": 450.0, 
             "data": "03/06/2025"},
        ],
    }


@pytest.fixture
def arquivo_temporario(tmp_path, monkeypatch):
    """
    Redireciona DATA_FILE para um diretório temporário durante os testes,
    evitando que os testes escrevam no projeto real.
    """
    arquivo = tmp_path / "financas_teste.json"
    monkeypatch.setattr("main.DATA_FILE", arquivo)
    return arquivo


# ──────────────────────────────────────────────
# TESTES UNITÁRIOS — calcular_saldo
# ──────────────────────────────────────────────


class TestCalcularSaldo:
    def test_saldo_zerado_sem_transacoes(self, dados_vazios):
        """Com dados vazios, o saldo deve ser zero."""
        assert calcular_saldo(dados_vazios) == 0.0

    def test_saldo_apenas_com_saldo_inicial(self):
        """Sem transações, saldo deve ser igual ao saldo inicial."""
        dados = {"saldo_inicial": 500.0, "transacoes": []}
        assert calcular_saldo(dados) == 500.0

    def test_saldo_com_receita(self, dados_vazios):
        """Uma receita deve aumentar o saldo."""
        dados_vazios["transacoes"].append(
            {"tipo": "receita", "valor": 200.0}
        )
        assert calcular_saldo(dados_vazios) == 200.0

    def test_saldo_com_despesa(self, dados_vazios):
        """Uma despesa deve diminuir o saldo."""
        dados_vazios["transacoes"].append(
            {"tipo": "despesa", "valor": 100.0}
        )
        assert calcular_saldo(dados_vazios) == -100.0

    def test_saldo_misto_com_saldo_inicial(self, dados_com_transacoes):
        """Saldo deve ser: inicial + receitas - despesas."""
        # 1000 + 3000 - 1200 - 450 = 2350
        resultado = calcular_saldo(dados_com_transacoes)
        assert resultado == pytest.approx(2350.0)

    def test_saldo_negativo(self):
        """Saldo pode ficar negativo se as despesas superarem receitas."""
        dados = {
            "saldo_inicial": 100.0,
            "transacoes": [{"tipo": "despesa", "valor": 500.0}],
        }
        assert calcular_saldo(dados) == -400.0


# ──────────────────────────────────────────────
# TESTES UNITÁRIOS — adicionar_transacao
# ──────────────────────────────────────────────


class TestAdicionarTransacao:
    def test_adiciona_receita(self, dados_vazios):
        """Deve adicionar uma transação de tipo 'receita'."""
        resultado = adicionar_transacao(dados_vazios, "receita", "Freelance", 500.0)
        assert len(resultado["transacoes"]) == 1
        assert resultado["transacoes"][0]["tipo"] == "receita"
        assert resultado["transacoes"][0]["valor"] == 500.0
        assert resultado["transacoes"][0]["descricao"] == "Freelance"

    def test_adiciona_despesa(self, dados_vazios):
        """Deve adicionar uma transação de tipo 'despesa'."""
        resultado = adicionar_transacao(dados_vazios, "despesa", "Netflix", 55.90)
        assert resultado["transacoes"][0]["tipo"] == "despesa"
        assert resultado["transacoes"][0]["valor"] == pytest.approx(55.90)

    def test_valor_negativo_vira_positivo(self, dados_vazios):
        """Valores negativos informados devem ser salvos como positivos (abs)."""
        resultado = adicionar_transacao(dados_vazios, "despesa", "Conta de luz", -200.0)
        assert resultado["transacoes"][0]["valor"] == 200.0

    def test_id_auto_incrementa(self, dados_com_transacoes):
        """O ID deve ser sequencial (último ID + 1)."""
        resultado = adicionar_transacao(dados_com_transacoes, "receita", "Bônus", 100.0)
        nova = resultado["transacoes"][-1]
        assert nova["id"] == 4

    def test_transacao_tem_data(self, dados_vazios):
        """Toda transação deve ter uma data registrada."""
        resultado = adicionar_transacao(dados_vazios, "receita", "Teste", 10.0)
        assert "data" in resultado["transacoes"][0]
        assert len(resultado["transacoes"][0]["data"]) > 0


# ──────────────────────────────────────────────
# TESTES UNITÁRIOS — converter_valor
# ──────────────────────────────────────────────


class TestConverterValor:
    def test_conversao_simples(self):
        """R$ 500 com cotação de R$ 5 = 100 USD."""
        assert converter_valor(500.0, 5.0) == pytest.approx(100.0)

    def test_conversao_euro(self):
        """R$ 600 com cotação de R$ 6 = 100 EUR."""
        assert converter_valor(600.0, 6.0) == pytest.approx(100.0)

    def test_cotacao_zero_levanta_excecao(self):
        """Cotação zero deve levantar ValueError."""
        with pytest.raises(ValueError, match="maior que zero"):
            converter_valor(100.0, 0)

    def test_cotacao_negativa_levanta_excecao(self):
        """Cotação negativa deve levantar ValueError."""
        with pytest.raises(ValueError):
            converter_valor(100.0, -5.0)

    def test_valor_zero(self):
        """Valor zero convertido deve ser zero."""
        assert converter_valor(0.0, 5.0) == pytest.approx(0.0)


# ──────────────────────────────────────────────
# TESTES UNITÁRIOS — carregar_dados e salvar_dados
# ──────────────────────────────────────────────


class TestPersistencia:
    def test_carregar_dados_arquivo_inexistente(self, arquivo_temporario):
        """Se não houver arquivo, retorna estrutura padrão."""
        resultado = carregar_dados()
        assert resultado == {"transacoes": [], "saldo_inicial": 0.0}

    def test_salvar_e_carregar_dados(self, arquivo_temporario):
        """Deve salvar e recuperar os dados corretamente."""
        dados_para_salvar = {
            "saldo_inicial": 250.0,
            "transacoes": [{"id": 1, "tipo": "receita", "valor": 100.0}],
        }
        salvar_dados(dados_para_salvar)
        dados_recuperados = carregar_dados()
        assert dados_recuperados["saldo_inicial"] == 250.0
        assert len(dados_recuperados["transacoes"]) == 1

    def test_dados_salvos_sao_json_valido(self, arquivo_temporario):
        """O arquivo salvo deve ser JSON válido e legível."""
        dados = {"saldo_inicial": 50.0, "transacoes": []}
        salvar_dados(dados)
        conteudo = arquivo_temporario.read_text(encoding="utf-8")
        parsed = json.loads(conteudo)
        assert parsed["saldo_inicial"] == 50.0


# ──────────────────────────────────────────────
# TESTES DE INTEGRAÇÃO — buscar_cotacao (com mock)
# ──────────────────────────────────────────────


class TestBuscarCotacao:
    """
    Testes de integração: simulamos (mockamos) a API para não depender
    de internet real durante os testes automáticos.
    """

    def _mock_resposta(self, dados: dict):
        """Cria um objeto mock de resposta HTTP."""
        mock = MagicMock()
        mock.raise_for_status = MagicMock()
        mock.json.return_value = dados
        return mock

    @patch("main.requests.get")
    def test_retorna_dados_cotacao_validos(self, mock_get):
        """Deve retornar os dados quando a API responde com sucesso."""
        mock_get.return_value = self._mock_resposta(
            {"USDBRL": {"bid": "5.25", "ask": "5.26", "pctChange": "0.5", "name": "Dólar/Real"}}
        )
        resultado = buscar_cotacao("USD-BRL")
        assert resultado is not None
        assert resultado["bid"] == "5.25"
        assert resultado["ask"] == "5.26"

    @patch("main.requests.get")
    def test_retorna_none_quando_chave_ausente(self, mock_get):
        """Deve retornar None se a chave esperada não estiver na resposta."""
        mock_get.return_value = self._mock_resposta({})
        resultado = buscar_cotacao("USD-BRL")
        assert resultado is None

    @patch("main.requests.get")
    def test_trata_erro_de_conexao(self, mock_get):
        """Deve retornar None (sem travar) quando não há conexão."""
        import requests as req
        mock_get.side_effect = req.exceptions.ConnectionError()
        resultado = buscar_cotacao("USD-BRL")
        assert resultado is None

    @patch("main.requests.get")
    def test_trata_timeout(self, mock_get):
        """Deve retornar None ao receber timeout da API."""
        import requests as req
        mock_get.side_effect = req.exceptions.Timeout()
        resultado = buscar_cotacao("USD-BRL")
        assert resultado is None

    @patch("main.requests.get")
    def test_url_chamada_corretamente(self, mock_get):
        """A URL montada deve seguir o padrão da AwesomeAPI."""
        mock_get.return_value = self._mock_resposta({"EURBRL": {"bid": "6.10"}})
        buscar_cotacao("EUR-BRL")
        url_esperada = f"{AWESOMEAPI_BASE_URL}/last/EUR-BRL"
        mock_get.assert_called_once_with(url_esperada, timeout=10)
