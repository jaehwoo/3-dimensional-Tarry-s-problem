#!/usr/bin/env python3
"""Regression tests run the guard CLI on isolated temporary source copies.

Run: python certificates/test_degree6_source.py
No manuscript or checker in the repository is modified by these tests.
"""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import check_degree6_source as guard


class SourceGuardTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.original = Path(__file__).resolve().parents[1]
        for filename in (guard.SUPPLEMENT, guard.PAPER_I, guard.CHECKER):
            target = self.root / filename
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(self.original / filename, target)

    def replace(self, filename, before, after):
        path = self.root / filename
        text = path.read_text(encoding="utf-8")
        self.assertEqual(text.count(before), 1, f"test fixture not unique: {before}")
        path.write_text(text.replace(before, after), encoding="utf-8")

    def run_guard(self, expected=None):
        result = subprocess.run(
            [sys.executable, str(self.original / "certificates/check_degree6_source.py"),
             "--root", str(self.root)],
            cwd=self.root, capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(result.returncode, 0 if expected is None else 1,
                         result.stdout + result.stderr)
        if expected is None:
            self.assertIn("PASS: degree-six source consistency", result.stdout)
        else:
            self.assertIn("FAIL:", result.stderr)
            self.assertIn(expected, result.stderr)
            self.assertNotIn("PASS: degree-six source consistency", result.stdout)
            print(f"\nDETECTED [{self._testMethodName}]: {result.stderr.strip()}", flush=True)

    def test_current_sources(self):
        self.run_guard()

    def test_polynomial_coefficient(self):
        self.replace(guard.SUPPLEMENT, "f_1(t)&=2t-1", "f_1(t)&=3t-1")
        self.run_guard("FACTOR_COEFFICIENTS: manuscript/checker mismatch")

    def test_block_sign(self):
        self.replace(guard.SUPPLEMENT, "1&2&1&7&12&-16f_3f_6", "1&2&1&7&12&16f_3f_6")
        self.run_guard("PRINTED_BLOCKS: manuscript/checker mismatch")

    def test_block_size(self):
        self.replace(guard.SUPPLEMENT, "1&2&1&7&12&-16f_3f_6", "1&2&1&7&13&-16f_3f_6")
        self.run_guard("PRINTED_BLOCKS: manuscript/checker mismatch")

    def test_block_factor(self):
        self.replace(guard.SUPPLEMENT, "1&2&1&7&12&-16f_3f_6", "1&2&1&7&12&-16f_3f_7")
        self.run_guard("PRINTED_BLOCKS: manuscript/checker mismatch")

    def test_modular_leading_coefficient(self):
        self.replace(guard.SUPPLEMENT, "37,73,73,22,82,15", "38,73,73,22,82,15")
        self.run_guard("PRINTED_LEADING_COEFFICIENTS: manuscript/checker mismatch")

    def test_checker_constant(self):
        self.replace(guard.CHECKER, "    (2, -1),", "    (3, -1),")
        self.run_guard("FACTOR_COEFFICIENTS: manuscript/checker mismatch")

    def test_matrix_formula(self):
        self.replace(guard.SUPPLEMENT, r"\frac{a!}{\alpha!\beta!\gamma!}\,t^\alpha.",
                     r"\frac{a!}{\alpha!\beta!\gamma!}\,t^{\alpha+1}.")
        self.run_guard("Supplement context: source fingerprint changed")

    def test_product_formula(self):
        self.replace(guard.SUPPLEMENT, "g(t)=56623104", "g(t)=56623105")
        self.run_guard("Supplement context: source fingerprint changed")

    def test_modulus(self):
        self.replace(guard.SUPPLEMENT, "reduce its coefficients modulo $101$",
                     "reduce its coefficients modulo $103$")
        self.run_guard("Supplement context: source fingerprint changed")

    def test_ordering(self):
        self.replace(guard.SUPPLEMENT, "For $E_6$ use lexicographic order on the whole set",
                     "For $E_6$ use reverse lexicographic order on the whole set")
        self.run_guard("Supplement context: source fingerprint changed")

    def test_paper_index_definition(self):
        self.replace(guard.PAPER_I, r"E_d=I_{d-3}\cup", r"E_d=I_{d-2}\cup")
        self.run_guard("Paper I jet indices: source fingerprint changed")

    def test_paper_row_rule(self):
        self.replace(guard.PAPER_I, r"(\phi_2)_{I_{D-3}}", r"(\phi_2)_{I_{D-2}}")
        self.run_guard("Paper I ordinary rows: source fingerprint changed")

    def test_unsupported_latex(self):
        self.replace(guard.SUPPLEMENT, "f_1(t)&=2t-1", r"f_1(t)&=\frac{4}{2}t-1")
        self.run_guard("unsupported factor layout/syntax")

    def test_unparsed_tail(self):
        self.replace(guard.SUPPLEMENT, "f_8(t)&=20t^3+90t^2+30t+1.",
                     "f_8(t)&=20t^3+90t^2+30t+1.EXTRA")
        self.run_guard("unsupported factor layout/syntax")

    def test_duplicate_factor(self):
        self.replace(guard.SUPPLEMENT, "f_2(t)&=6t+1", "f_1(t)&=6t+1")
        self.run_guard("duplicate f_1")

    def test_missing_factor(self):
        self.replace(guard.SUPPLEMENT, "f_1(t)&=2t-1,& ", "")
        self.run_guard("expected exactly f_1,...,f_11")

    def test_duplicate_weight(self):
        self.replace(guard.SUPPLEMENT, "1&2&1&7&12&-16f_3f_6", "2&2&1&7&12&-16f_3f_6")
        self.run_guard("duplicate weight 2")

    def test_duplicate_anchor(self):
        self.replace(guard.SUPPLEMENT, guard.G6, guard.G6 + guard.G6)
        self.run_guard("missing/duplicate anchor")

    def test_missing_anchor(self):
        self.replace(guard.SUPPLEMENT, guard.G6, "")
        self.run_guard("missing/duplicate anchor")

    def test_missing_file(self):
        (self.root / guard.SUPPLEMENT).unlink()
        self.run_guard("No such file")

    def test_nonliteral_checker_constant(self):
        self.replace(guard.CHECKER, "    (2, -1),", "    (int('2'), -1),")
        self.run_guard("malformed node")

    def test_equivalent_polynomial_and_factor_order(self):
        self.replace(guard.SUPPLEMENT, "f_1(t)&=2t-1", "f_1(t)&=-1 + t + t")
        self.replace(guard.SUPPLEMENT, "1&2&1&7&12&-16f_3f_6", "1&2&1&7&12&-16f_6f_3")
        self.run_guard()

    def test_context_whitespace_requires_review(self):
        self.replace(guard.SUPPLEMENT, "Use $D=6$ and write $g=g_6$.",
                     "Use $D=6$  and write $g=g_6$.")
        self.run_guard("Supplement context: source fingerprint changed")

    def test_unrelated_text_outside_scope(self):
        for filename in (guard.SUPPLEMENT, guard.PAPER_I):
            path = self.root / filename
            path.write_text("% Outside guarded regions\n" + path.read_text(encoding="utf-8"),
                            encoding="utf-8")
        self.run_guard()

    def test_crlf_line_endings(self):
        for filename in (guard.SUPPLEMENT, guard.PAPER_I):
            path = self.root / filename
            path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
        self.run_guard()


if __name__ == "__main__":
    unittest.main(verbosity=2)
