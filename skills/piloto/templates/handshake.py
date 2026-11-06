#!/usr/bin/env python3
"""Handshake de um serviço: confirma que a credencial do .env funciona.

Contrato: lê .env, confere as variáveis exigidas, faz UMA chamada só de leitura,
imprime "OK <servico>" ou "FALHA <servico>: <motivo>" (sem segredos) e sai com 0/1.
Copie para tools/handshake_<servico>.py e ajuste SERVICE, REQUIRED e URL.
Pode trocar urllib pelo SDK oficial do serviço.
"""
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

SERVICE = "servico"
REQUIRED = ["SERVICO_TOKEN"]
URL = "https://api.exemplo.com/v1/me"  # endpoint só de leitura ("quem sou eu")


def load_env(path=Path(__file__).resolve().parent.parent / ".env"):
    # shortcut: parser simples (sem export, sem multilinha); troque por python-dotenv se o .env crescer.
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


def main():
    load_env()
    missing = [k for k in REQUIRED if not os.environ.get(k)]
    if missing:
        print(f"FALHA {SERVICE}: faltam no .env: {', '.join(missing)}")
        return 1
    req = urllib.request.Request(URL, headers={"Authorization": f"Bearer {os.environ[REQUIRED[0]]}"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            resp.read()
    except urllib.error.HTTPError as e:
        print(f"FALHA {SERVICE}: HTTP {e.code}")
        return 1
    except OSError as e:
        print(f"FALHA {SERVICE}: {e}")
        return 1
    print(f"OK {SERVICE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
