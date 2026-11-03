# Corporate LaTeX Suite & Antigravity Plugin

Suite corporativa maestra de documentos LaTeX y extensión oficial para **Antigravity**, diseñada para la generación y compilación automatizada de documentación ejecutiva, técnica, fiscal y de gobernanza con las identidades de marca oficiales del Holding **Grupo BNW**, **Boletos.la**, **Nodo**, **VINI** y **WIT**.

---

## 1. Instalación Rápida

### Opción A: Directamente desde Antigravity (Recomendado)
Pega el siguiente prompt en el chat de tu Antigravity:
```text
Descarga e instala el plugin oficial de documentos corporativos LaTeX desde https://github.com/ivalenzuela/corporate-latex-suite en mi directorio ~/.gemini/config/plugins/corporate-latex-plugin y verifica que la skill corporate-latex esté lista para usar.
```

### Opción B: Clonar manualmente con Git
```bash
git clone https://github.com/ivalenzuela/corporate-latex-suite.git
cd corporate-latex-suite
python install.py
```
*(o en PowerShell: `.\install.ps1`)*

---

## 2. Marcas Oficiales Soportadas (`--brand`)

| Marca ID | Empresa / Unidad | Paleta Principal | Logo Oficial |
| :--- | :--- | :--- | :--- |
| **`bnw`** | **BNW Corporate Group** (Holding Matriz) | Obsidian `#000000`, Champagne Gold `#F2C681`, Bronze AAA `#6B4608`, Warm Ivory `#F5F2EB`, Slate `#5A5E66` | `bnw corporate group.png` |
| **`boletos`** | **Boletos.la** (Transporte Interurbano) | Tangelo BO `#FF6700`, Solar Amber `#FFAA00`, Electric Cyan `#00C7CC`, Deep Teal `#008E8A`, Anthracite `#3F3F3F` | `logo-boletos.png` |
| **`nodo`** | **Nodo** (Infraestructura Edge & Datacenters) | Deep Indigo `#1E1B4B`, Midnight Slate `#0F172A`, Indigo AA `#4338CA`, Edge Violet `#6D28D9` + 5 bandas | `Logo Nodo.png` |
| **`vini`** | **VINI** (Telemetría IoT & Flotas) | Wordmark Black `#000000`, Cobalt Fleet `#2563EB`, Telemetry Emerald `#059669`, Amber `#D97706` | `LOGO VINI V4.png` |
| **`wit`** | **WIT** (Ingeniería & Proyectos I+D) | Deep Slate `#0B132B`, Slate Surface `#1C2541`, Cyan Light AA `#0077B6`, Cyan Dark `#00B4D8` + 5 UBN | `wit.png` |

---

## 3. Tipos de Documentos Soportados (`--type`)

1. **`oc`** — **Orden de Compra y Cotización Formal**: Tabla de ítems multimoneda (CLP/USD/PYG), desglose Neto/IVA/Total, Matriz de Aprobación WIT-V4, firmas dual-control y sello SHA-256.
2. **`minuta`** — **Minuta de Reunión y Directorio**: Ficha de control, quórum, acuerdos prioritarios y tabla de compromisos con SLAs y responsables.
3. **`proceso`** — **Manual SOP y Diagramas TikZ**: Carriles (swimlanes) interdepartamentales, compuertas romboidales, máquina de estados 2PC y arquitectura de sistemas distribuida.
4. **`cargo`** — **Descriptor de Cargo RRHH**: Identificación del rol, organigrama jerárquico TikZ, matriz de KPIs y competencias.
5. **`informe`** — **Informe Ejecutivo y Auditoría 360°**: Portada corporativa, resumen ejecutivo, cajas estilizadas de alerta/directiva, gráficos `pgfplots` y dictamen de gobernanza.
6. **`propuesta`** — **Propuesta Comercial / RFP**: Alcance del servicio, arquitectura técnica, cronograma de hitos, tabla de inversión y confidencialidad NDA.
7. **`acta`** — **Acta de Recepción Conforme y SLA**: Verificación de entregables, pruebas UAT y certificación formal de SLA.
8. **`memo`** — **Memorándum y Circular Normativa**: Control de versiones, directivas obligatorias y protocolo de vigencia.

---

## 4. Tipografía Oficial (Brandbooks Normativos)

- **Capa Editorial & PDF/LaTeX**: `Helvetica Neue` / `Helvetica` escalada al 94% (`helvet` + `\familydefault{\sfdefault}`).
- **Capa Numérica & Fiscal SIFEN**: `Courier Mono` (`courier` / `JetBrains Mono` tabular) para CDC de 44 dígitos, montos y hashes criptográficos.
- **Jerarquía Ejecutiva**: Mayúsculas sostenidas (`ALL CAPS`) con tracking para nombres y color atenuado para cargos.

---

## 5. Uso Rápido via CLI

```powershell
python scripts/generate_corporate_doc.py \
  --brand boletos \
  --type oc \
  --title "Orden de Compra Servidores Edge Totems" \
  --output "C:/Users/ivanv/Templates Latex/OC_Boletos_Totems.pdf"
```

Argumentos principales:
- `--brand`: `bnw` | `boletos` | `nodo` | `vini` | `wit`
- `--type`: `oc` | `minuta` | `proceso` | `cargo` | `informe` | `propuesta` | `acta` | `memo`
- `--title`: Título formal del documento
- `--output`: Ruta de destino (`.pdf` o `.tex`)
- `--no-compile`: Exporta únicamente el código `.tex` sin compilar a PDF

---

## Licencia y Gobernanza

© 2026 BNW Corporate Group & Boletos.la. Todos los derechos reservados.
