#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORPORATE_SUITE - Showcase Multi-Brand Compiler
Compiles LaTeX corporate templates across all 5 official brands:
  1. bnw      (BNW Corporate Group)
  2. boletos  (Boletos.la)
  3. nodo     (Nodo Edge Infrastructure)
  4. vini     (VINI Fleet Telemetry)
  5. wit      (WIT Innovacion Tecnologica)

Executes 2-pass pdflatex compilation to ensure complete cross-referencing,
verifies output size > 25 KB, and reports execution telemetry.
"""

import os
import sys
import re
import subprocess
import shutil
from pathlib import Path

BRANDS = ["bnw", "boletos", "nodo", "vini", "wit"]

SHOWCASE_MATRIX = [
    {
        "brand": "bnw",
        "template": "05_informe_ejecutivo_auditoria_360.tex",
        "output_slug": "bnw_informe_ejecutivo_auditoria_360"
    },
    {
        "brand": "boletos",
        "template": "01_orden_compra_cotizacion.tex",
        "output_slug": "boletos_orden_compra_cotizacion"
    },
    {
        "brand": "nodo",
        "template": "03_diagramas_flujo_y_procesos_sop.tex",
        "output_slug": "nodo_diagramas_flujo_procesos_sop"
    },
    {
        "brand": "vini",
        "template": "04_descriptor_cargo_rrhh.tex",
        "output_slug": "vini_descriptor_cargo_rrhh"
    },
    {
        "brand": "wit",
        "template": "06_propuesta_comercial_licitacion.tex",
        "output_slug": "wit_propuesta_comercial_licitacion"
    },
    {
        "brand": "boletos",
        "template": "02_minuta_ejecutiva_directorio.tex",
        "output_slug": "boletos_minuta_ejecutiva_directorio"
    },
    {
        "brand": "nodo",
        "template": "07_acta_recepcion_conformidad_sla.tex",
        "output_slug": "nodo_acta_recepcion_conformidad_sla"
    },
    {
        "brand": "bnw",
        "template": "08_memorandum_politica_interna.tex",
        "output_slug": "bnw_memorandum_politica_interna"
    }
]


def compile_showcase_item(item, base_dir: Path):
    templates_dir = base_dir / "templates"
    core_dir = base_dir / "core"
    showcase_dir = base_dir / "compiled_showcase"
    showcase_dir.mkdir(parents=True, exist_ok=True)

    brand = item["brand"]
    template_name = item["template"]
    output_slug = item["output_slug"]

    src_tex = templates_dir / template_name
    if not src_tex.exists():
        return {
            "slug": output_slug,
            "brand": brand,
            "success": False,
            "error": f"Template not found: {src_tex}"
        }

    with open(src_tex, "r", encoding="utf-8") as f:
        content = f.read()

    # Normalize relative path to package for compilation inside compiled_showcase/
    # Replace any \usepackage[...]{...agy-corporate-brand} with explicit brand pointing to ../core/agy-corporate-brand
    rel_core = "../core/agy-corporate-brand"
    content = re.sub(
        r"\\usepackage\[.*?\]\{.*?agy-corporate-brand\}",
        f"\\\\usepackage[brand={brand}]{{{rel_core}}}",
        content
    )

    target_tex = showcase_dir / f"{output_slug}.tex"
    with open(target_tex, "w", encoding="utf-8") as f:
        f.write(content)

    # 2-pass pdflatex compilation
    target_pdf = showcase_dir / f"{output_slug}.pdf"
    for pass_num in (1, 2):
        cmd = [
            "pdflatex",
            "-interaction=nonstopmode",
            f"-output-directory={showcase_dir}",
            str(target_tex.name)
        ]
        result = subprocess.run(
            cmd,
            cwd=str(showcase_dir),
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode != 0 and pass_num == 2:
            return {
                "slug": output_slug,
                "brand": brand,
                "success": False,
                "error": f"pdflatex failed with exit code {result.returncode}:\n{result.stdout[-1500:]}"
            }

    if not target_pdf.exists():
        return {
            "slug": output_slug,
            "brand": brand,
            "success": False,
            "error": "PDF was not generated."
        }

    pdf_size = target_pdf.stat().st_size
    if pdf_size < 25 * 1024:
        return {
            "slug": output_slug,
            "brand": brand,
            "success": False,
            "error": f"PDF generated is too small ({pdf_size} bytes < 25 KB threshold)."
        }

    # Clean intermediate artifacts
    for ext in [".aux", ".log", ".out", ".toc"]:
        aux_file = showcase_dir / f"{output_slug}{ext}"
        if aux_file.exists():
            try:
                aux_file.unlink()
            except Exception:
                pass

    return {
        "slug": output_slug,
        "brand": brand,
        "success": True,
        "size_bytes": pdf_size,
        "path": str(target_pdf)
    }


def main():
    script_dir = Path(__file__).resolve().parent
    suite_dir = script_dir.parent
    print(f"=== CORPORATE_SUITE Showcase Multi-Brand Compiler ===")
    print(f"Suite Directory: {suite_dir}")
    print(f"Total showcase builds: {len(SHOWCASE_MATRIX)}")

    results = []
    failures = 0

    for i, item in enumerate(SHOWCASE_MATRIX, 1):
        print(f"[{i}/{len(SHOWCASE_MATRIX)}] Compiling {item['output_slug']} (brand: {item['brand']})...", end=" ", flush=True)
        res = compile_showcase_item(item, suite_dir)
        results.append(res)
        if res["success"]:
            kb = res["size_bytes"] / 1024.0
            print(f"OK ({kb:.1f} KB)")
        else:
            print("FAILED")
            print(f"   Reason: {res.get('error')}")
            failures += 1

    print("\n--- Summary ---")
    print(f"Total: {len(results)}, Succeeded: {len(results) - failures}, Failed: {failures}")
    if failures > 0:
        sys.exit(1)
    print("All corporate showcase PDFs generated and verified successfully!")


if __name__ == "__main__":
    main()
