#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador interativo de NÚMEROS DE CELULAR do Brasil (CLI)
-------------------------------------------------------
• Execute e responda às perguntas no próprio CMD/Terminal.
• Escolha QUANTOS números gerar e o MODO:
    (1) Por DDD específico  → gera apenas para um DDD escolhido
    (2) Aleatório (todos)   → distribui entre TODOS os DDDs válidos do Brasil
• Sempre usa o nono dígito (9) para celular e evita padrões triviais (99999999 etc.).
• Salva em CSV e TXT: E.164 (+55DDDNXXXXXXXX) e formato nacional.

Como usar:
    python gerador_celular_br.py

Saídas:
    - <nome_base>.csv  (colunas: e164,nacional,ddd,numero)
    - <nome_base>.txt  (um número por linha, padrão E.164)

Extras:
    python gerador_celular_br.py --selftest   # roda testes rápidos
"""
from __future__ import annotations
import csv
import random
import sys
import tempfile
from pathlib import Path
from typing import Iterable, List, Set, Tuple, Optional
from datetime import datetime

# ========================= DDDs válidos (ANATEL) =============================
VALID_DDDS: Set[str] = set([
    "11","12","13","14","15","16","17","18","19",
    "21","22","24","27","28",
    "31","32","33","34","35","37","38",
    "41","42","43","44","45","46","47","48","49",
    "51","53","54","55",
    "61","62","63","64","65","66","67","68","69",
    "71","73","74","75","77","79",
    "81","82","83","84","85","86","87","88","89",
    "91","92","93","94","95","96","97","98","99",
])

# fonte de aleatoriedade segura
sysrand = random.SystemRandom()

# ========================= Utilitários =======================================

def print_banner() -> None:
    print("=" * 70)
    print(" GERADOR DE CELULARES BR (INTERATIVO)")
    print("=" * 70)
    print("• Nonos dígitos (celular) sempre iniciando com 9.")
    print("• DDDs válidos reconhecidos:", len(VALID_DDDS))
    print()


def is_trivially_invalid(seq: str) -> bool:
    """Evita padrões muito improváveis: todos iguais, sequência crescente/decrescente longa."""
    if len(set(seq)) == 1:
        return True  # ex: 99999999 ou 00000000
    inc = all(int(b) - int(a) == 1 for a, b in zip(seq, seq[1:]))
    dec = all(int(a) - int(b) == 1 for a, b in zip(seq, seq[1:]))
    if len(seq) >= 6 and (inc or dec):
        return True
    return False


def gen_local_9digits() -> str:
    """Gera os 9 dígitos de um celular brasileiro (começa com 9 + 8 dígitos)."""
    tail = ''.join(str(sysrand.randint(0, 9)) for _ in range(8))
    seq = '9' + tail
    while is_trivially_invalid(seq):
        tail = ''.join(str(sysrand.randint(0, 9)) for _ in range(8))
        seq = '9' + tail
    return seq


def gen_number_for_ddd(ddd: str) -> Tuple[str, str, str, str]:
    """Retorna tupla (e164, nacional, ddd, numero_9digitos)."""
    numero = gen_local_9digits()
    e164 = f"+55{ddd}{numero}"
    nacional = f"({ddd}) {numero[0]} {numero[1:5]}-{numero[5:]}"
    return e164, nacional, ddd, numero


def generate(ddds: Iterable[str], qtd: int, dedup: bool = True) -> List[Tuple[str,str,str,str]]:
    results: List[Tuple[str,str,str,str]] = []
    seen: Set[str] = set()
    ddds = list(ddds)
    i = 0
    attempts = 0
    max_attempts = max(qtd * 20, 200)
    while len(results) < qtd and attempts < max_attempts:
        ddd = ddds[i % len(ddds)]
        e164, nacional, ddd_out, numero = gen_number_for_ddd(ddd)
        attempts += 1
        if dedup:
            if e164 in seen:
                continue
            seen.add(e164)
        results.append((e164, nacional, ddd_out, numero))
        i += 1
    if len(results) < qtd:
        print(f"[AVISO] Gerei apenas {len(results)} de {qtd} solicitados após {attempts} tentativas.")
    return results


def write_outputs(rows: List[Tuple[str,str,str,str]], out_base: Path) -> None:
    csv_path = out_base.with_suffix('.csv')
    txt_path = out_base.with_suffix('.txt')

    # CSV
    with csv_path.open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(["e164", "nacional", "ddd", "numero"])
        for r in rows:
            w.writerow(r)

    # TXT (E.164 por linha)
    with txt_path.open('w', encoding='utf-8') as f:
        for e164, *_ in rows:
            f.write(e164 + '\n')

    print("\n✓ Arquivos salvos:")
    print(" -", csv_path)
    print(" -", txt_path)


# ========================= Interação (CLI) ===================================

def ask_int(prompt: str, min_value: int = 1, max_value: Optional[int] = None) -> int:
    while True:
        raw = input(prompt).strip()
        if not raw.isdigit():
            print("Por favor, digite um número inteiro válido.")
            continue
        val = int(raw)
        if val < min_value:
            print(f"O valor mínimo é {min_value}.")
            continue
        if max_value is not None and val > max_value:
            print(f"O valor máximo é {max_value}.")
            continue
        return val


def ask_mode() -> str:
    print("Escolha o modo:")
    print("  [1] Por DDD específico")
    print("  [2] Aleatório em TODOS os DDDs do Brasil")
    while True:
        m = input("Opção (1/2): ").strip()
        if m in {"1", "2"}:
            return m
        print("Opção inválida. Digite 1 ou 2.")


def ask_ddd() -> str:
    while True:
        d = input("Informe o DDD (ex: 11): ").strip()
        if d in VALID_DDDS:
            return d
        print("DDD inválido. Tente novamente.")


def main() -> None:
    try:
        print_banner()
        qtd = ask_int("Quantos números deseja gerar? ")
        modo = ask_mode()

        if modo == "1":
            ddd = ask_ddd()
            print("\nFormato base quando é por DDD:")
            print(f"  DDD: {ddd} | adicional (nono dígito): 9 | número: 00000000")
            ddds_escolhidos = [ddd]
        else:
            print("\nModo aleatório em TODOS os DDDs do Brasil selecionado.")
            ddds_escolhidos = sorted(VALID_DDDS)

        base = input("\nNome base do arquivo (ENTER = numeros_br): ").strip() or "numeros_br"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if modo == "1":
            out_base = Path(f"{base}_ddd_{ddds_escolhidos[0]}_{timestamp}")
        else:
            out_base = Path(f"{base}_todos_{timestamp}")

        rows = generate(ddds_escolhidos, qtd, dedup=True)
        write_outputs(rows, out_base)

        print("\nExemplos gerados (até 5):")
        for e164, nacional, ddd, numero in rows[:5]:
            print(f"  {e164}  |  {nacional}")

        print("\nConcluído. Obrigado!\n")

    except KeyboardInterrupt:
        print("\nCancelado pelo usuário.")
    except Exception as e:
        # Em produção, manter saída com código 1 é útil para pipelines/monitoração.
        print("[ERRO]", e)
        sys.exit(1)


# ========================= Testes rápidos (opcional) =========================

def _selftest() -> None:
    """Testes básicos de sanidade para o gerador."""
    # 1) O local deve ter 9 dígitos, começar com 9 e ser numérico
    n = gen_local_9digits()
    assert len(n) == 9 and n[0] == '9' and n.isdigit(), "nono dígito inválido"

    # 2) Gerar 10 números para DDD 11
    rows = generate(["11"], 10, dedup=True)
    assert len(rows) == 10, "quantidade incorreta"
    assert all(r[0].startswith("+5511") for r in rows), "DDD errado nos E.164"

    # 3) Gerar 50 números em todos os DDDs, sem duplicatas
    rows2 = generate(sorted(VALID_DDDS), 50, dedup=True)
    assert len(rows2) == 50, "quantidade incorreta (todos DDDs)"
    assert len({r[0] for r in rows2}) == 50, "duplicação indevida"

    # 4) Persistência: escrever e reler .txt e .csv
    with tempfile.TemporaryDirectory() as tmpdir:
        out = Path(tmpdir) / "teste_out"
        write_outputs(rows[:5], out)
        assert out.with_suffix('.csv').exists(), "CSV não foi criado"
        assert out.with_suffix('.txt').exists(), "TXT não foi criado"
        txt_lines = out.with_suffix('.txt').read_text(encoding='utf-8').splitlines()
        assert len(txt_lines) == 5 and all(l.startswith('+55') for l in txt_lines), "TXT inválido"

    print("[SELFTEST] OK")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--selftest':
        _selftest()
    else:
        main()
