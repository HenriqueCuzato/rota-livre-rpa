"""Processa a exportação JSON do Rota Livre. Execute com Python 3.9+."""
import argparse
import json
import math
import os
import sys
import tempfile
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def agora():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def coordenada(valor, limite):
    return (type(valor) in (float, int) and -limite <= valor <= limite
            and math.isfinite(valor))


def classificar(lote):
    grupos = defaultdict(list)
    decisoes = {}
    ativos = []
    for numero, item in enumerate(lote, 1):
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"].strip():
            decisoes[numero] = "id_invalido"
        else:
            grupos[item["id"]].append((numero, item))
    for grupo in grupos.values():
        numero, item = grupo[0]
        if any(outro != item for _, outro in grupo[1:]):
            for indice, _ in grupo:
                decisoes[indice] = "conflito_de_id"
            continue
        for indice, _ in grupo[1:]:
            decisoes[indice] = "duplicado"
        if item.get("status") == "Resolvida":
            decisoes[numero] = "resolvida"
        elif item.get("status") not in ("Registrada", "Em análise"):
            decisoes[numero] = "status_invalido"
        elif not coordenada(item.get("lat"), 90) or not coordenada(item.get("lng"), 180):
            decisoes[numero] = "coordenada_invalida"
        elif not isinstance(item.get("category"), str) or not item["category"].strip():
            decisoes[numero] = "categoria_ausente"
        else:
            ativos.append({k: item[k] for k in ("id", "category", "status", "lat", "lng")})
            decisoes[numero] = "ativo"
    return ativos, decisoes


def executar(entrada, saida, log):
    log.parent.mkdir(parents=True, exist_ok=True)
    run = uuid.uuid4().hex
    with log.open("a", encoding="utf-8") as audit:
        def evento(**campos):
            audit.write(json.dumps(dict(hora=agora(), execucao=run, **campos), ensure_ascii=False) + "\n")
            audit.flush()
        try:
            lote = json.loads(entrada.read_text(encoding="utf-8-sig"))
            if not isinstance(lote, list):
                raise ValueError("formato")
            ativos, decisoes = classificar(lote)
            for indice, motivo in sorted(decisoes.items()):
                evento(item=indice, resultado=motivo)
            saida.parent.mkdir(parents=True, exist_ok=True)
            tmp = None
            try:
                with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=saida.parent, delete=False) as arq:
                    tmp = Path(arq.name)
                    json.dump(dict(execucao=run, atualizado=agora(), alertas=ativos), arq, ensure_ascii=False, indent=2)
                os.replace(tmp, saida)
            finally:
                if tmp:
                    tmp.unlink(missing_ok=True)
            evento(resultado="concluido", processados=len(lote), ativos=len(ativos))
            print(f"{len(lote)} registros processados. {len(ativos)} alerta(s) ativo(s).")
            return 0
        except (OSError, ValueError) as erro:
            evento(resultado="falha_lote", motivo=type(erro).__name__)
            print(f"Falha no lote ({type(erro).__name__}). Confira a entrada e repita.", file=sys.stderr)
            return 1


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("entrada", nargs="?", type=Path, default=ROOT/"dados/ocorrencias_teste.json")
    cli.add_argument("--saida", type=Path, default=ROOT/"painel/alertas_ativos.json")
    cli.add_argument("--log", type=Path, default=ROOT/"logs/auditoria.jsonl")
    args = cli.parse_args()
    try:
        sys.exit(executar(args.entrada, args.saida, args.log))
    except OSError as erro:
        sys.exit("Falha ao gravar auditoria: " + type(erro).__name__)
