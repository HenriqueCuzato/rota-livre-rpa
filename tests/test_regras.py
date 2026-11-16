import json
import tempfile
import unittest
from pathlib import Path
from src.triagem import classificar, executar

BASE = dict(id='a', category='Buraco', status='Registrada', lat=-23.5745, lng=-46.6228)

class TestRegras(unittest.TestCase):
    def test_duplicados(self):
        ativos, decisoes = classificar([BASE, dict(BASE)])
        self.assertEqual(len(ativos), 1)
        self.assertEqual(decisoes[2], 'duplicado')

    def test_conflito_id(self):
        ativos, decisoes = classificar([BASE, dict(BASE, status='Resolvida')])
        self.assertEqual(ativos, [])
        self.assertEqual(set(decisoes.values()), {'conflito_de_id'})

    def test_coordenadas_invalidas(self):
        for value in [None, True, '23', 91, -91, float('nan'), float('inf')]:
            with self.subTest(value=value):
                ativos, decisoes = classificar([dict(BASE, lat=value)])
                self.assertEqual(ativos, [])
                self.assertEqual(decisoes[1], 'coordenada_invalida')

    def test_id_categoria_status(self):
        for item, motivo in [(dict(BASE,id=''), 'id_invalido'), (None,'id_invalido'), (dict(BASE,category=' '),'categoria_ausente'), (dict(BASE,status='Outro'),'status_invalido')]:
            with self.subTest(motivo=motivo):
                self.assertEqual(classificar([item]), ([],{1:motivo}))

    def test_resolvida(self):
        self.assertEqual(classificar([dict(BASE,status='Resolvida')]), ([],{1:'resolvida'}))

    def test_lote_vazio(self):
        self.assertEqual(classificar([]), ([],{}))

    def test_json_invalido_preserva_saida(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp); entrada=folder/'entrada.json'; saida=folder/'saida.json'; log=folder/'log.jsonl'
            for conteudo in ['{quebrado', '{}']:
                entrada.write_text(conteudo,encoding='utf-8'); saida.write_text('anterior',encoding='utf-8')
                self.assertEqual(executar(entrada,saida,log),1)
                self.assertEqual(saida.read_text(), 'anterior')
                self.assertEqual(json.loads(log.read_text().splitlines()[-1])['resultado'],'falha_lote')

    def test_exportacao_mvp(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp); entrada=folder/'entrada.json'; saida=folder/'saida.json'; log=folder/'log.jsonl'
            entrada.write_text(json.dumps([dict(BASE,title='DEMO',photo='privado',description='não exportar')]),encoding='utf-8')
            self.assertEqual(executar(entrada,saida,log),0)
            result=json.loads(saida.read_text())
            self.assertEqual(result['alertas'],[BASE])
            self.assertIn('execucao',result); self.assertIn('atualizado',result)
