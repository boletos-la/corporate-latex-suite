#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for generate_corporate_doc.py
"""

import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys

scripts_dir = Path(__file__).resolve().parent.parent / "scripts"
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

from generate_corporate_doc import (
    VALID_BRANDS,
    TYPE_TO_TEMPLATE,
    find_suite_dir,
    generate_document,
    main
)


class TestGenerateCorporateDoc(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        try:
            suite = find_suite_dir()
            showcase = suite / "compiled_showcase"
            for f in showcase.glob("_test*"):
                try:
                    f.unlink()
                except Exception:
                    pass
        except Exception:
            pass

    def test_valid_brands_and_types(self):
        self.assertEqual(len(VALID_BRANDS), 5)
        for b in ["bnw", "boletos", "nodo", "vini", "wit"]:
            self.assertIn(b, VALID_BRANDS)
        for t in ["oc", "minuta", "proceso", "cargo", "informe", "propuesta", "acta", "memo"]:
            self.assertIn(t, TYPE_TO_TEMPLATE)

    def test_find_suite_dir(self):
        suite = find_suite_dir()
        self.assertTrue(suite.exists())
        self.assertTrue((suite / "core" / "agy-corporate-brand.sty").exists())

    def test_invalid_brand_raises(self):
        with self.assertRaises(ValueError):
            generate_document("fake_brand", "oc", "Title", "out.pdf", compile_pdf=False)

    def test_invalid_type_raises(self):
        with self.assertRaises(ValueError):
            generate_document("bnw", "fake_type", "Title", "out.pdf", compile_pdf=False)

    def test_generate_tex_all_types(self):
        suite = find_suite_dir()
        out_dir = suite / "compiled_showcase"
        for t in TYPE_TO_TEMPLATE.keys():
            out_file = out_dir / f"_test_{t}.tex"
            res = generate_document(
                brand="bnw",
                doc_type=t,
                title=f"Test {t.upper()}",
                output_path=str(out_file),
                ref=f"REF-{t.upper()}-01",
                compile_pdf=False,
                suite_dir=suite
            )
            self.assertTrue(res["success"])
            self.assertFalse(res["compiled"])
            self.assertTrue(out_file.exists())
            content = out_file.read_text(encoding="utf-8")
            self.assertIn("agy-corporate-brand", content)
            out_file.unlink()

    def test_custom_suite_dir_not_found(self):
        with self.assertRaises(FileNotFoundError):
            find_suite_dir("C:/NonExistentPath/12345")

    def test_compile_pdf_integration(self):
        suite = find_suite_dir()
        out_pdf = suite / "compiled_showcase" / "_test_oc_compile.pdf"
        res = generate_document(
            brand="boletos",
            doc_type="oc",
            title="Prueba Unitaria de Compilacion",
            output_path=str(out_pdf),
            ref="OC-UNIT-001",
            compile_pdf=True,
            suite_dir=suite
        )
        self.assertTrue(res["success"])
        self.assertTrue(res["compiled"])
        self.assertTrue(out_pdf.exists())
        self.assertGreater(out_pdf.stat().st_size, 25 * 1024)
        out_pdf.unlink()

    def test_find_suite_dir_candidate_path(self):
        suite = find_suite_dir()
        found = find_suite_dir(str(suite))
        self.assertEqual(suite, found)

    def test_generate_document_default_suite_dir(self):
        out_file = Path("C:/Users/ivanv/Templates Latex/CORPORATE_SUITE/compiled_showcase/_test_default_suite.tex")
        res = generate_document(
            brand="vini",
            doc_type="memo",
            title="Test Memo",
            output_path=str(out_file),
            compile_pdf=False
        )
        self.assertTrue(res["success"])
        if out_file.exists():
            out_file.unlink()

    def test_missing_template_raises(self):
        suite = Path("C:/Users/ivanv/Templates Latex/CORPORATE_SUITE/compiled_showcase")
        with self.assertRaises(FileNotFoundError):
            generate_document("bnw", "oc", "Title", "out.tex", compile_pdf=False, suite_dir=suite)

    def test_cli_main_success_and_failure_branches(self):
        # Test main with --help catching SystemExit
        with self.assertRaises(SystemExit) as cm:
            sys.argv = ["generate_corporate_doc.py", "--help"]
            main()
        self.assertEqual(cm.exception.code, 0)

        # Test main with --no-compile
        suite = find_suite_dir()
        test_out = suite / "compiled_showcase" / "_test_cli_main.tex"
        sys.argv = [
            "generate_corporate_doc.py",
            "--brand", "wit",
            "--type", "propuesta",
            "--title", "Propuesta CLI Test",
            "--output", str(test_out),
            "--no-compile"
        ]
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
        if test_out.exists():
            test_out.unlink()

        # Test main reporting size on compile success
        fake_success = {
            "success": True,
            "output_file": "dummy.pdf",
            "size_bytes": 102400
        }
        with patch("generate_corporate_doc.generate_document", return_value=fake_success):
            sys.argv = ["generate_corporate_doc.py", "--type", "oc", "--output", "dummy.pdf"]
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 0)

        # Test main reporting error on compile failure
        fake_fail = {
            "success": False,
            "error": "Simulated compilation error"
        }
        with patch("generate_corporate_doc.generate_document", return_value=fake_fail):
            sys.argv = ["generate_corporate_doc.py", "--type", "oc", "--output", "dummy.pdf"]
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 1)

        # Test main failure with invalid brand
        sys.argv = [
            "generate_corporate_doc.py",
            "--brand", "invalid_brand",
            "--type", "propuesta",
            "--output", "dummy.pdf"
        ]
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertNotEqual(cm.exception.code, 0)

    def test_pdflatex_compilation_failure_handling(self):
        suite = find_suite_dir()
        out_pdf = suite / "compiled_showcase" / "_test_fail.pdf"
        fake_process = MagicMock()
        fake_process.returncode = 1
        fake_process.stdout = "Fatal LaTeX error: Missing \\begin{document}"
        with patch("subprocess.run", return_value=fake_process):
            res = generate_document(
                brand="bnw",
                doc_type="oc",
                title="Fail Test",
                output_path=str(out_pdf),
                compile_pdf=True,
                suite_dir=suite
            )
            self.assertFalse(res["success"])
            self.assertIn("pdflatex compilation failed", res["error"])

    def test_pdf_missing_or_undersized(self):
        suite = find_suite_dir()
        out_pdf = suite / "compiled_showcase" / "_test_size.pdf"
        fake_process = MagicMock()
        fake_process.returncode = 0

        # Subtest 1: PDF not created (mocked subprocess creates nothing)
        if out_pdf.exists():
            out_pdf.unlink()
        with patch("subprocess.run", return_value=fake_process):
            res = generate_document(
                brand="bnw", doc_type="oc", title="T", output_path=str(out_pdf), compile_pdf=True, suite_dir=suite
            )
            self.assertFalse(res["success"])
            self.assertIn("Final PDF was not created", res["error"])

        # Subtest 2: PDF undersized (< 25 KB)
        def create_small_pdf(*args, **kwargs):
            out_pdf.write_bytes(b"%PDF-1.4 small test file\n%%EOF")
            return fake_process

        with patch("subprocess.run", side_effect=create_small_pdf):
            res = generate_document(
                brand="bnw", doc_type="oc", title="T", output_path=str(out_pdf), compile_pdf=True, suite_dir=suite
            )
            self.assertFalse(res["success"])
            self.assertIn("smaller than 25 KB", res["error"])
        if out_pdf.exists():
            out_pdf.unlink()

    def test_cli_main_exception_branch(self):
        with patch("generate_corporate_doc.find_suite_dir", side_effect=RuntimeError("Forced suite discovery error")):
            sys.argv = ["generate_corporate_doc.py", "--type", "oc", "--output", "dummy.pdf"]
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
