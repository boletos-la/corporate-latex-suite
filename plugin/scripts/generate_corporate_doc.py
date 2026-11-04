#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_corporate_doc.py - Official Antigravity Corporate Document Generator
Generates and compiles production-grade corporate LaTeX documents for:
  - Brands: bnw, boletos, nodo, vini, wit
  - Types: oc, minuta, proceso, cargo, informe, propuesta, acta, memo
"""

import os
import sys
import argparse
import subprocess
import shutil
import re
from pathlib import Path

# Enforce UTF-8 in stdio
if sys.platform == "win32":
    try:
        sys.stdin.reconfigure(encoding="utf-8")
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

TYPE_TO_TEMPLATE = {
    "oc": "01_orden_compra_cotizacion.tex",
    "minuta": "02_minuta_ejecutiva_directorio.tex",
    "proceso": "03_diagramas_flujo_y_procesos_sop.tex",
    "cargo": "04_descriptor_cargo_rrhh.tex",
    "informe": "05_informe_ejecutivo_auditoria_360.tex",
    "propuesta": "06_propuesta_comercial_licitacion.tex",
    "acta": "07_acta_recepcion_conformidad_sla.tex",
    "memo": "08_memorandum_politica_interna.tex"
}

VALID_BRANDS = ["bnw", "boletos", "nodo", "vini", "wit"]


def find_suite_dir(candidate_path=None) -> Path:
    if candidate_path:
        p = Path(candidate_path).resolve()
        if p.exists() and (p / "core" / "agy-corporate-brand.sty").exists():
            return p
        raise FileNotFoundError(f"Custom suite path invalid or missing core/agy-corporate-brand.sty: {candidate_path}")

    # Standard default paths
    candidates = [
        Path("C:/Users/ivanv/Templates Latex/CORPORATE_SUITE"),
        Path(__file__).resolve().parent.parent.parent.parent / "Templates Latex" / "CORPORATE_SUITE"
    ]
    for c in candidates:
        if c.exists() and (c / "core" / "agy-corporate-brand.sty").exists():
            return c.resolve()

    raise FileNotFoundError("Could not locate CORPORATE_SUITE directory with core/agy-corporate-brand.sty")


def generate_document(brand: str, doc_type: str, title: str, output_path: str,
                      ref: str = None, author: str = None, date_str: str = None,
                      compile_pdf: bool = True, suite_dir: Path = None):
    brand = brand.lower().strip()
    if brand not in VALID_BRANDS:
        raise ValueError(f"Invalid brand '{brand}'. Must be one of: {', '.join(VALID_BRANDS)}")

    doc_type = doc_type.lower().strip()
    if doc_type not in TYPE_TO_TEMPLATE:
        raise ValueError(f"Invalid type '{doc_type}'. Must be one of: {', '.join(TYPE_TO_TEMPLATE.keys())}")

    if suite_dir is None:
        suite_dir = find_suite_dir()

    template_file = suite_dir / "templates" / TYPE_TO_TEMPLATE[doc_type]
    if not template_file.exists():
        raise FileNotFoundError(f"Template file not found: {template_file}")

    with open(template_file, "r", encoding="utf-8") as f:
        tex_content = f.read()

    # Re-route package to agy-corporate-brand directly (local copy or relative)
    tex_content = re.sub(
        r"\\usepackage\[.*?\]\{.*?agy-corporate-brand\}",
        f"\\\\usepackage[brand={brand}]{{agy-corporate-brand}}",
        tex_content
    )

    # Optional replacements for title, ref, author, date if supplied
    if title:
        tex_content = re.sub(
            r"(\\title\{)[^}]*(\})",
            lambda m: f"{m.group(1)}{title}{m.group(2)}",
            tex_content
        )
        # Also replace in \setupcorporateheader{...} first argument
        tex_content = re.sub(
            r"(\\setupcorporateheader\{)[^}]*(\}\{)",
            lambda m: f"{m.group(1)}{title}{m.group(2)}",
            tex_content
        )

    if ref:
        tex_content = re.sub(
            r"(\\setupcorporateheader\{[^}]*\}\{)[^}]*(\})",
            lambda m: f"{m.group(1)}{ref}{m.group(2)}",
            tex_content
        )

    out_p = Path(output_path).resolve()
    out_p.parent.mkdir(parents=True, exist_ok=True)

    if not compile_pdf:
        # Save as .tex directly
        tex_target = out_p.with_suffix(".tex") if out_p.suffix == ".pdf" else out_p
        with open(tex_target, "w", encoding="utf-8") as f:
            f.write(tex_content)
        return {
            "success": True,
            "brand": brand,
            "type": doc_type,
            "output_file": str(tex_target),
            "compiled": False
        }

    # Compile mode
    final_pdf = out_p.with_suffix(".pdf")
    work_dir = out_p.parent
    base_name = final_pdf.stem
    tmp_tex = work_dir / f"{base_name}.tex"

    # Copy agy-corporate-brand.sty into work_dir if not present to avoid path spacing issues in LaTeX
    brand_sty_src = suite_dir / "core" / "agy-corporate-brand.sty"
    brand_sty_dest = work_dir / "agy-corporate-brand.sty"
    if brand_sty_src.exists() and not brand_sty_dest.exists():
        try:
            shutil.copy(brand_sty_src, brand_sty_dest)
        except Exception:
            pass

    with open(tmp_tex, "w", encoding="utf-8") as f:
        f.write(tex_content)

    # Set TEXINPUTS environment
    env = os.environ.copy()
    core_dir_str = str((suite_dir / "core").resolve())
    env["TEXINPUTS"] = f".;{core_dir_str};{env.get('TEXINPUTS', '')}"

    # Run pdflatex (2 passes)
    for pass_num in (1, 2):
        cmd = [
            "pdflatex",
            "-interaction=nonstopmode",
            f"-output-directory={work_dir}",
            str(tmp_tex.name)
        ]
        res = subprocess.run(
            cmd,
            cwd=str(work_dir),
            capture_output=True,
            text=True,
            env=env,
            timeout=120
        )
        if res.returncode != 0 and pass_num == 2:
            return {
                "success": False,
                "brand": brand,
                "type": doc_type,
                "error": f"pdflatex compilation failed (code {res.returncode}):\n{res.stdout[-1500:]}"
            }

    if not final_pdf.exists():
        return {
            "success": False,
            "brand": brand,
            "type": doc_type,
            "error": "Final PDF was not created."
        }

    pdf_size = final_pdf.stat().st_size
    if pdf_size < 25 * 1024:
        return {
            "success": False,
            "brand": brand,
            "type": doc_type,
            "error": f"Generated PDF is smaller than 25 KB ({pdf_size} bytes)."
        }

    # Clean intermediate files
    for ext in [".aux", ".log", ".out", ".toc"]:
        aux = work_dir / f"{base_name}{ext}"
        if aux.exists():
            try:
                aux.unlink()
            except Exception:
                pass

    return {
        "success": True,
        "brand": brand,
        "type": doc_type,
        "output_file": str(final_pdf),
        "size_bytes": pdf_size,
        "compiled": True
    }


def main():
    parser = argparse.ArgumentParser(description="Antigravity Corporate Document Generator CLI")
    parser.add_argument("--brand", choices=VALID_BRANDS, default="bnw", help="Brand identifier")
    parser.add_argument("--type", choices=list(TYPE_TO_TEMPLATE.keys()), required=True, help="Document archetype type")
    parser.add_argument("--title", default="", help="Document Title")
    parser.add_argument("--output", required=True, help="Output destination path (.pdf or .tex)")
    parser.add_argument("--ref", default="", help="Document reference or ID")
    parser.add_argument("--author", default="", help="Author or emitter name")
    parser.add_argument("--date", default="", help="Document date string")
    parser.add_argument("--no-compile", action="store_true", help="Only generate TeX without compiling to PDF")
    parser.add_argument("--suite-dir", default=None, help="Custom path to CORPORATE_SUITE root")

    args = parser.parse_args()

    try:
        suite = find_suite_dir(args.suite_dir)
        res = generate_document(
            brand=args.brand,
            doc_type=args.type,
            title=args.title,
            output_path=args.output,
            ref=args.ref,
            author=args.author,
            date_str=args.date,
            compile_pdf=not args.no_compile,
            suite_dir=suite
        )
        if res["success"]:
            print(f"[SUCCESS] Document generated: {res['output_file']}")
            if res.get("size_bytes"):
                print(f"[SIZE] {res['size_bytes'] / 1024.0:.1f} KB")
            sys.exit(0)
        else:
            print(f"[ERROR] {res.get('error')}", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"[EXCEPTION] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
