#!/usr/bin/env python3
"""Compare the degree-six printed data with the standalone checker's constants.

Run: python certificates/check_degree6_source.py [--root REPOSITORY]
Uses only the standard library; reads the checker as AST, without executing it.

Supported LaTeX is deliberately narrow: integer polynomials in t, signed
products of f_i, and an integer list. Unsupported syntax fails closed. This is
not a general LaTeX interpreter (macros/includes elsewhere are not inspected).
The two aligned factor bodies, block-table body, and gathered coefficient body
are compared structurally. All other text in Supplement lines 1440-1506 and
Paper I lines 2120-2130, 2173-2176 is fingerprinted against commit
c6501c2db457bffded229d3d0aa8674a37eae904. Anchors, not line numbers, select text.
Fingerprints preserve whitespace/comments; only CRLF/CR become LF on reading.

A fingerprint failure requires source review, even for harmless formatting.
Never refresh hashes merely to make CI pass: review the changed definitions,
ordering, matrix formula, product formula and modular convention against the
checker, then rerun both this guard and the independent finite calculation.
Matching fingerprints attest only to unchanged text, not mathematical truth.
Neither this guard nor the finite calculation verifies the moving-graph
argument or the Tarry convergence theorem.
"""

import argparse
import ast
import hashlib
from pathlib import Path
import re
import sys


SUPPLEMENT = "Complete_Affine_Jets_Supplement.tex"
PAPER_I = "Complete_Affine_Jets_I.tex"
CHECKER = "certificates/verify_degree6_normal.py"
NORMAL = r"\section{Normal determinant factors in degrees six through nine}\label{supp:normal-factors}"
G6 = r"\subsection{The degree-six slope factorization}\label{supp:g6-factors}"
G7 = r"\subsection{The degree-seven slope factorization}\label{supp:g7-factors}"
INDICES = r"\begin{definition}[Jet index sets]\label{def:jet-indices}"
ROWS = r"\begin{equation}\label{surf:ordinary-list}"
F_INDEX = r"f_(?:\{([0-9]+)\}|([0-9]))"
CONSTANT_NAMES = (
    "FACTOR_COEFFICIENTS", "PRINTED_BLOCKS", "PRINTED_LEADING_COEFFICIENTS",
)
# SHA-256 of the exact selected text; Supplement data bodies are masked below.
FINGERPRINTS = {
    "Supplement context": "d40b21b2073014852561679f8b9d86ee695d020dc54b1eb05ee5dd7599629636",
    "Paper I jet indices": "14ef309b7b71934894f649ef505d76acfe67c980a90a707ea5b830be1c28ce30",
    "Paper I ordinary rows": "eb75dd6c719a56bf3118eff4f684a300a396e3958f2588b7615633e4d47912dc",
}


class SourceMismatch(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise SourceMismatch(message)


def unique_position(text, anchor):
    require(text.count(anchor) == 1, f"missing/duplicate anchor: {anchor}")
    return text.index(anchor)


def region(text, start, end, include_end=False):
    left = unique_position(text, start)
    right = unique_position(text, end)
    require(left < right, f"reversed anchors: {start}")
    return text[left:right + (len(end) if include_end else 0)]


def environment(text, start, end):
    # The opening anchor must be unique. Stop at its first closing marker;
    # any changed/truncated selected body must still match its fingerprint.
    left = unique_position(text, start)
    right = text.find(end, left + len(start))
    require(right >= 0, f"missing closing marker: {end}")
    return text[left:right + len(end)]


def compact(text):
    return re.sub(r"\s+", "", text)


def polynomial(text):
    """Parse every character as a signed integer monomial; no eval/sympify."""
    term = r"([+-]?)(?:(\d*)t(?:\^(?:\{(\d+)\}|(\d)))?|(\d+))"
    coefficients = {}
    position = 0
    while position < len(text):
        match = re.match(term, text[position:])
        require(match is not None, f"unsupported polynomial: {text}")
        sign, coefficient, braced_power, power, constant = match.groups()
        require(position == 0 or sign, f"missing polynomial sign: {text}")
        exponent = 0 if constant is not None else int(braced_power or power or 1)
        require(exponent <= 6, f"unsupported degree: {text}")
        value = int(constant if constant is not None else coefficient or 1)
        coefficients[exponent] = coefficients.get(exponent, 0) + (-value if sign == "-" else value)
        position += match.end()
    require(coefficients, "empty polynomial")
    degree = max((p for p, c in coefficients.items() if c), default=0)
    return tuple(coefficients.get(p, 0) for p in range(degree, -1, -1))


def factors(bodies):
    result = {}
    pattern = F_INDEX + r"\(t\)&=([+\-0-9t^{}]+)(?:,&|,\\\\|\.)"
    for body in bodies:
        text = compact(body)
        position = 0
        while position < len(text):
            match = re.match(pattern, text[position:])
            require(match is not None, "unsupported factor layout/syntax")
            index = int(match[1] or match[2])
            require(index not in result, f"duplicate f_{index}")
            result[index] = polynomial(match[3])
            position += match.end()
    require(set(result) == set(range(1, 12)), "expected exactly f_1,...,f_11")
    return tuple(result[i] for i in range(1, 12))


def determinant(text):
    match = re.fullmatch(r"([+-]?)([0-9]*)((?:f_(?:\{[0-9]+\}|[0-9]))*)", text)
    require(match is not None and (match[2] or match[3]), f"unsupported determinant: {text}")
    scalar = int(match[2] or 1) * (-1 if match[1] == "-" else 1)
    indices = tuple(sorted(int(m[1] or m[2]) for m in re.finditer(F_INDEX, match[3])))
    require(all(1 <= i <= 11 for i in indices), f"unknown factor: {text}")
    return scalar, indices


def blocks(body):
    rows = compact(body).split(r"\\")
    require(rows[-1] == "", "missing final block-table row terminator")
    result = {}
    for row in rows[:-1]:
        cells = row.split("&")
        require(len(cells) == 6, "expected two blocks per table row")
        for offset in (0, 3):
            w, size, expression = cells[offset:offset + 3]
            require(re.fullmatch(r"[0-9]+", w) and re.fullmatch(r"[0-9]+", size),
                    "noninteger block weight/size")
            weight = int(w)
            require(weight not in result, f"duplicate weight {weight}")
            result[weight] = (weight, int(size), *determinant(expression))
    require(set(result) == set(range(1, 13)), "expected exactly weights 1,...,12")
    return tuple(result[w] for w in range(1, 13))


def leading_coefficients(body):
    text = compact(body).replace(r"\\", "")
    require(re.fullmatch(r"[0-9]+(?:,[0-9]+)*\.", text), "unsupported leading-coefficient list")
    result = tuple(map(int, text[:-1].split(",")))
    require(len(result) == 33, "expected 33 leading coefficients")
    return result


def source_data(supplement, paper):
    context = region(supplement, NORMAL, G7)
    degree_six = region(context, G6, r"\end{gathered}", include_end=True)
    aligned = list(re.finditer(r"\\begin\{aligned\}(.*?)\\end\{aligned\}", degree_six, re.S))
    require(len(aligned) == 2, "expected two aligned factor environments")
    table = region(degree_six, r"\midrule", r"\bottomrule")[len(r"\midrule"):]
    gathered = region(degree_six, r"\begin{gathered}", r"\end{gathered}")[len(r"\begin{gathered}"):]
    bodies = [m[1] for m in aligned]
    values = (factors(bodies), blocks(table), leading_coefficients(gathered))
    # Mask only fully parsed bodies; unexpected extra text remains fingerprinted.
    for name, body in zip(("factors-1-8", "factors-9-11", "blocks", "leading-coefficients"),
                          bodies + [table, gathered]):
        require(context.count(body) == 1, f"ambiguous data body: {name}")
        context = context.replace(body, f"<parsed:{name}>")
    contexts = {
        "Supplement context": context,
        "Paper I jet indices": environment(paper, INDICES, r"\end{definition}"),
        "Paper I ordinary rows": environment(paper, ROWS, r"\end{equation}"),
    }
    return dict(zip(CONSTANT_NAMES, values)), contexts


def checker_constants(text):
    tree = ast.parse(text)
    result = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store) and node.id in CONSTANT_NAMES:
            require(node.id not in result, f"duplicate checker constant: {node.id}")
            assignments = [item for item in tree.body if isinstance(item, ast.Assign)
                           and len(item.targets) == 1 and item.targets[0] is node]
            require(len(assignments) == 1, f"expected literal top-level assignment: {node.id}")
            result[node.id] = ast.literal_eval(assignments[0].value)
    require(set(result) == set(CONSTANT_NAMES), "missing checker constant")
    return result


def check(root):
    printed, contexts = source_data((root / SUPPLEMENT).read_text(encoding="utf-8"),
                                    (root / PAPER_I).read_text(encoding="utf-8"))
    expected = checker_constants((root / CHECKER).read_text(encoding="utf-8"))
    for name in CONSTANT_NAMES:
        require(printed[name] == expected[name], f"{name}: manuscript/checker mismatch")
        print(f"PASS: {name} ({len(printed[name])} entries)")
    for name, value in contexts.items():
        digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
        require(digest == FINGERPRINTS[name],
                f"{name}: source fingerprint changed; review required (SHA-256 {digest})")
        print(f"PASS: {name} fingerprint")
    print("PASS: degree-six source consistency (not a proof verification)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        check(args.root)
    except (OSError, ValueError, SyntaxError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
