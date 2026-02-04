import argparse
import csv
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Dict, Optional, Tuple, List


PRIMITIVOS = {
    "V": "void",
    "Z": "boolean",
    "B": "byte",
    "C": "char",
    "S": "short",
    "I": "int",
    "J": "long",
    "F": "float",
    "D": "double",
}


def _ler_tipo(desc: str, i: int) -> Tuple[str, int]:
    if i >= len(desc):
        return ("", i)

    if desc[i] == "[":
        base, j = _ler_tipo(desc, i + 1)
        return (f"{base}[]", j)

    if desc[i] in PRIMITIVOS:
        return (PRIMITIVOS[desc[i]], i + 1)

    if desc[i] == "L":
        j = desc.find(";", i)
        if j == -1:
            return ("object", i + 1)
        nome = desc[i + 1 : j].replace("/", ".")
        return (nome, j + 1)

    return ("object", i + 1)


def assinatura_legivel(nome_metodo: str, desc: str) -> str:
    if not desc or "(" not in desc or ")" not in desc:
        return f"{nome_metodo}{desc}"

    ini = desc.find("(")
    fim = desc.find(")")
    args_desc = desc[ini + 1 : fim]
    ret_desc = desc[fim + 1 :]

    args: List[str] = []
    i = 0
    while i < len(args_desc):
        t, i = _ler_tipo(args_desc, i)
        if t:
            args.append(t)

    ret, _ = _ler_tipo(ret_desc, 0)
    return f"{nome_metodo}({', '.join(args)}) -> {ret}"


@dataclass(frozen=True)
class ChaveMetodo:
    classe: str
    metodo: str
    descritor: str


@dataclass
class InfoMetodo:
    pacote: str
    classe: str
    metodo: str
    descritor: str
    assinatura: str
    linha: int
    instr_cobertas: int
    instr_perdidas: int
    linhas_cobertas: int
    linhas_perdidas: int
    ramos_cobertos: int
    ramos_perdidos: int

    def coberto(self) -> bool:
        return (self.instr_cobertas > 0) or (self.linhas_cobertas > 0)

    def pct_instr(self) -> float:
        total = self.instr_cobertas + self.instr_perdidas
        return 0.0 if total == 0 else (100.0 * self.instr_cobertas / total)

    def pct_linhas(self) -> float:
        total = self.linhas_cobertas + self.linhas_perdidas
        return 0.0 if total == 0 else (100.0 * self.linhas_cobertas / total)

    def pct_ramos(self) -> float:
        total = self.ramos_cobertos + self.ramos_perdidos
        return 0.0 if total == 0 else (100.0 * self.ramos_cobertos / total)


def _ler_contadores(elemento) -> Tuple[int, int, int, int, int, int]:
    instr_c = instr_m = linhas_c = linhas_m = ramos_c = ramos_m = 0

    for c in elemento.findall("counter"):
        tipo = c.get("type", "")
        missed = int(c.get("missed", "0"))
        covered = int(c.get("covered", "0"))

        if tipo == "INSTRUCTION":
            instr_m, instr_c = missed, covered
        elif tipo == "LINE":
            linhas_m, linhas_c = missed, covered
        elif tipo == "BRANCH":
            ramos_m, ramos_c = missed, covered

    return instr_c, instr_m, linhas_c, linhas_m, ramos_c, ramos_m


def ler_jacoco_xml(caminho: str) -> Dict[ChaveMetodo, InfoMetodo]:
    arvore = ET.parse(caminho)
    raiz = arvore.getroot()

    metodos: Dict[ChaveMetodo, InfoMetodo] = {}

    for p in raiz.findall("package"):
        nome_pacote = p.get("name", "").replace("/", ".")
        for cl in p.findall("class"):
            nome_classe = cl.get("name", "").replace("/", ".")
            for m in cl.findall("method"):
                nome_metodo = m.get("name", "")
                descritor = m.get("desc", "")
                linha = int(m.get("line", "-1"))

                instr_c, instr_m, linhas_c, linhas_m, ramos_c, ramos_m = _ler_contadores(m)
                ass = assinatura_legivel(nome_metodo, descritor)

                chave = ChaveMetodo(nome_classe, nome_metodo, descritor)
                metodos[chave] = InfoMetodo(
                    pacote=nome_pacote,
                    classe=nome_classe,
                    metodo=nome_metodo,
                    descritor=descritor,
                    assinatura=ass,
                    linha=linha,
                    instr_cobertas=instr_c,
                    instr_perdidas=instr_m,
                    linhas_cobertas=linhas_c,
                    linhas_perdidas=linhas_m,
                    ramos_cobertos=ramos_c,
                    ramos_perdidos=ramos_m,
                )

    return metodos


def classificar_origem(cob_unit: bool, cob_it: bool) -> str:
    if cob_unit and cob_it:
        return "ambos"
    if cob_unit and not cob_it:
        return "unitario"
    if (not cob_unit) and cob_it:
        return "integracao"
    return "nenhum"


def escrever_csv(
    saida: str,
    todos: Dict[ChaveMetodo, InfoMetodo],
    unit: Optional[Dict[ChaveMetodo, InfoMetodo]],
    it: Optional[Dict[ChaveMetodo, InfoMetodo]],
    somente_testados: bool,
):
    campos = [
        "pacote",
        "classe",
        "metodo",
        "descritor",
        "assinatura",
        "linha",
        "instr_cobertas",
        "instr_perdidas",
        "pct_instr",
        "linhas_cobertas",
        "linhas_perdidas",
        "pct_linhas",
        "ramos_cobertos",
        "ramos_perdidos",
        "pct_ramos",
        "coberto",
        "origem",
    ]

    chaves_ordenadas = sorted(todos.keys(), key=lambda k: (k.classe, k.metodo, k.descritor))

    with open(saida, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()

        for chave in chaves_ordenadas:
            info = todos[chave]

            cob_info = info.coberto()
            if somente_testados and (not cob_info):
                continue

            info_unit = unit.get(chave) if unit else None
            info_it = it.get(chave) if it else None

            cob_unit = info_unit.coberto() if info_unit else False
            cob_it = info_it.coberto() if info_it else False
            origem = classificar_origem(cob_unit, cob_it) if (unit or it) else "desconhecido"

            w.writerow(
                {
                    "pacote": info.pacote,
                    "classe": info.classe,
                    "metodo": info.metodo,
                    "descritor": info.descritor,
                    "assinatura": info.assinatura,
                    "linha": info.linha,
                    "instr_cobertas": info.instr_cobertas,
                    "instr_perdidas": info.instr_perdidas,
                    "pct_instr": f"{info.pct_instr():.2f}",
                    "linhas_cobertas": info.linhas_cobertas,
                    "linhas_perdidas": info.linhas_perdidas,
                    "pct_linhas": f"{info.pct_linhas():.2f}",
                    "ramos_cobertos": info.ramos_cobertos,
                    "ramos_perdidos": info.ramos_perdidos,
                    "pct_ramos": f"{info.pct_ramos():.2f}",
                    "coberto": "sim" if cob_info else "nao",
                    "origem": origem,
                }
            )


def unir_bases(*bases: Dict[ChaveMetodo, InfoMetodo]) -> Dict[ChaveMetodo, InfoMetodo]:
    saida: Dict[ChaveMetodo, InfoMetodo] = {}
    for b in bases:
        for k, v in b.items():
            saida[k] = v
    return saida


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jacoco", help="caminho do jacoco.xml (geral)", default=None)
    ap.add_argument("--unit", help="caminho do jacoco.xml de unit tests", default=None)
    ap.add_argument("--it", help="caminho do jacoco.xml de integration tests", default=None)
    ap.add_argument("--saida", help="csv final", default="metodos_jacoco.csv")
    ap.add_argument("--saida_testados", help="csv somente cobertos", default="metodos_testados.csv")
    args = ap.parse_args()

    base_geral = ler_jacoco_xml(args.jacoco) if args.jacoco else {}
    base_unit = ler_jacoco_xml(args.unit) if args.unit else None
    base_it = ler_jacoco_xml(args.it) if args.it else None

    if not base_geral and (base_unit or base_it):
        base_geral = unir_bases(base_unit or {}, base_it or {})

    todos = unir_bases(base_geral, base_unit or {}, base_it or {})

    escrever_csv(args.saida, todos, base_unit, base_it, somente_testados=False)
    escrever_csv(args.saida_testados, todos, base_unit, base_it, somente_testados=True)

    total = len(todos)
    testados = sum(1 for v in todos.values() if v.coberto())
    print(f"metodos_total={total}")
    print(f"metodos_testados={testados}")
    print(f"metodos_nao_testados={total - testados}")
    print(f"csv={args.saida}")
    print(f"csv_testados={args.saida_testados}")


if __name__ == "__main__":
    main()
