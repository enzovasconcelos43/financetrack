
from unittest.mock import MagicMock, patch
import db
class TestDb:
    @patch('db.create_client')
    def test_get_client_retorna_cliente(self, mock_create):
        mock_create.return_value = MagicMock()
        client = db.get_client()
        assert client is not None
    @patch('db.get_client')
    def test_buscar_transacoes_retorna_lista(self, mock_client):
        mock_exec = MagicMock()
        mock_exec.execute.return_value.data = [{'id': 1, 'tipo': 'receita'}]
        mock_client.return_value.table.return_value.select.return_value.order.return_value = mock_exec
        resultado = db.buscar_transacoes()
        assert isinstance(resultado, list)
