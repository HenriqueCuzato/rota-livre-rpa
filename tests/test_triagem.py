import json
import tempfile
import unittest
from pathlib import Path
from src.triagem import ROOT, executar


class TestTriagem(unittest.TestCase):
    def test_ciclo_e_recuperacao(self):
        with tempfile.TemporaryDirectory() as pasta:
            saida = Path(pasta) / "alertas.json"
            log = Path(pasta) / "auditoria.jsonl"
            for _ in range(2):
                self.assertEqual(executar(ROOT/"dados/ocorrencias_teste.json", saida, log), 0)
                self.assertEqual([i["id"] for i in json.loads(saida.read_text(encoding="utf-8"))["alertas"]], ["teste-1"])
            anterior = saida.read_bytes()
            self.assertEqual(executar(Path(pasta)/"ausente.json", saida, log), 1)
            self.assertEqual(saida.read_bytes(), anterior)
            self.assertEqual(executar(ROOT/"dados/apos_resolucao.json", saida, log), 0)
            self.assertEqual(json.loads(saida.read_text(encoding="utf-8"))["alertas"], [])
            motivos = {json.loads(l)["resultado"] for l in log.read_text(encoding="utf-8").splitlines()}
            self.assertTrue({"ativo","resolvida","duplicado","coordenada_invalida","falha_lote"} <= motivos)
