---
name: corporate-latex
description: Genera, personaliza y compila documentos corporativos maestros en LaTeX con las identidades de marca oficiales de BNW Corporate Group, Boletos.la, Nodo, VINI y WIT (Ordenes de Compra, Minutas Ejecutivas, Manuales SOP con Diagramas TikZ, Descriptores de Cargo, Informes de Auditoria 360, Propuestas Comerciales RFP, Actas de Recepcion SLA y Memorandums Internos).
---

# Corporate LaTeX Suite Skill

Esta skill permite generar y compilar documentos corporativos formales en PDF de alta fidelidad, con tipografia institucional, paletas cromáticas verificadas, logotipos oficiales en alta resolucion, matrices de aprobacion y sellos criptograficos para las 5 empresas del Holding BNW Corporate Group.

## 1. Marcas Oficiales Soportadas (`--brand`)

1. **`bnw` (BNW Corporate Group — Holding Matriz)**:
   - Colores: Obsidian (`#000000`), Dark Surface (`#0D0F12`), Champagne Gold (`#F2C681`), Bronze AAA (`#6B4608`), Warm Ivory (`#F5F2EB`).
   - Logo oficial: `C:/Users/ivanv/Pictures/LOGOS/bnw corporate group.png`.
   - Uso: Asambleas de accionistas, informes ejecutivos, memorandums de directorio, convenios marco del holding.

2. **`boletos` (Boletos.la — B de Grupo BNW)**:
   - Colores: Tangelo BO (`#FF6700`), Solar Amber LE (`#FFAA00`), Electric Cyan TOS (`#00C7CC`), Deep Teal LA (`#008E8A`), Anthracite (`#3F3F3F`).
   - Logo oficial: `C:/Users/ivanv/Templates Latex/logo-boletos.png`.
   - Uso: Ordenes de compra de pasajes y terminales, SLAs con operadores de transporte, minutas de operacion comercial.

3. **`nodo` (Nodo — N de Grupo BNW: Infraestructura, Terminales & Datacenters Edge)**:
   - Colores: Deep Indigo (`#1E1B4B`), Midnight Slate (`#0F172A`), Indigo AA (`#4338CA`), Edge Violet (`#6D28D9`), y barra cromatica de 5 bandas (`#4F46E5`, `#06B6D4`, `#0043A5`, `#7AC602`, `#FF4D20`).
   - Logo oficial: `C:/Users/ivanv/Pictures/LOGOS/Logo Nodo.png`.
   - Uso: Fichas tecnicas de datacenters edge, contratos de coubicacion, actas de recepcion de enlaces y racks.

4. **`vini` (VINI — W de Grupo BNW: Telemetria & Flotas)**:
   - Colores: Wordmark Black (`#000000`), Cobalt Fleet (`#2563EB`), Cobalt AA (`#1D4ED8`), Telemetry Emerald (`#059669`), Amber (`#D97706`).
   - Logo oficial: `C:/Users/ivanv/Pictures/LOGOS/LOGO VINI V4.png`.
   - Uso: Descriptores de cargo de ingenieria/flota, actas de instalacion de GPS/CAN bus, propuestas de monitoreo de flotas.

5. **`wit` (WIT Innovacion Tecnologica — Transicion a VINI)**:
   - Colores: Deep Slate (`#0B132B`), Slate Surface (`#1C2541`), Cyan Light AA (`#0077B6`), Cyan Dark (`#00B4D8`), barra de 5 unidades de negocio (`IoT #0F3C8F`, `IA #54A0EB`, `ConnP #6AB319`, `P+S #D6D411`, `TeL #E84D24`).
   - Logo oficial: `C:/Users/ivanv/Pictures/LOGOS/wit.png`.
   - Uso: Propuestas tecnicas de I+D, arquitectura IoT y proyectos heredados WIT.

---

## 2. Tipos de Documentos Soportados (`--type`)

| Tipo | Archivo Base | Descripcion y Componentes Clave |
| :--- | :--- | :--- |
| `oc` | `01_orden_compra_cotizacion.tex` | Orden de Compra y Cotizacion Formal con desglose Neto/IVA/Total en CLP/USD/PYG, Matriz de Aprobacion WIT/BNW, firmas Dual-Control y Sello SHA-256. |
| `minuta` | `02_minuta_ejecutiva_directorio.tex` | Minuta de Comite Ejecutivo/Directorio con ficha de sesion, participantes, acuerdos prioritarios y matriz de compromisos con SLAs. |
| `proceso` | `03_diagramas_flujo_y_procesos_sop.tex` | Manual de Procesos Operativos (SOP) con swimlanes por area, compuertas romboidales, maquina de estados 2PC y arquitectura de sistemas en TikZ. |
| `cargo` | `04_descriptor_cargo_rrhh.tex` | Descriptor de Cargo y Perfil de Rol con identificacion del puesto, organigrama jerarquico en TikZ, matriz de KPIs y perfil de competencias. |
| `informe` | `05_informe_ejecutivo_auditoria_360.tex` | Informe Ejecutivo / Auditoria Tecnica 360 con portada de alto impacto, cajas de directiva/alerta, graficos de disponibilidad en `pgfplots` y dictamen final. |
| `propuesta` | `06_propuesta_comercial_licitacion.tex` | Propuesta Comercial / RFP con alcance del servicio, arquitectura tecnica, cronograma de hitos, tabla de inversion multimoneda y clausula NDA. |
| `acta` | `07_acta_recepcion_conformidad_sla.tex` | Acta de Entrega y Recepcion Conforme de Hito con matriz de entregables, pruebas UAT, metricas de SLA logradas y firmas de conformidad. |
| `memo` | `08_memorandum_politica_interna.tex` | Memorandum Oficial y Circular Normativa con encabezado formal, control de versiones, directivas obligatorias y protocolo de vigencia. |

---

## 3. Uso rapido via CLI (`generate_corporate_doc.py`)

Para compilar un documento corporativo de manera instantanea y 100% automatica:

```powershell
& F:\python_lite\python.exe -B C:\Users\ivanv\.gemini\config\plugins\corporate-latex-plugin\scripts\generate_corporate_doc.py `
  --brand boletos `
  --type oc `
  --title "Orden de Compra Servidores Edge Totems" `
  --output "C:\Users\ivanv\Templates Latex\OC_Boletos_Totems.pdf"
```

### Argumentos de la CLI:
- `--brand`: `bnw` | `boletos` | `nodo` | `vini` | `wit` (defecto: `bnw`)
- `--type`: `oc` | `minuta` | `proceso` | `cargo` | `informe` | `propuesta` | `acta` | `memo`
- `--title`: Titulo principal del documento
- `--output`: Ruta de destino para el archivo `.pdf` o `.tex` generado
- `--no-compile`: Genera unicamente el codigo `.tex` sin invocar `pdflatex`
- `--ref`: Codigo de referencia o ID del documento (ej. `OC-2026-BNW-094`)
- `--author`: Nombre del autor o emisor responsable

---

## 4. Arquitectura Modular del Core (`agy-corporate-brand.sty`)

Todo documento compilado incluye el paquete maestro:
```latex
\usepackage[brand=boletos]{../core/agy-corporate-brand}
```
Esto parametriza de forma atomica:
1. Las definiciones de colores institucionales (`corpPrimary`, `corpAccent`, `corpSecondary`, etc.).
2. El comando `\drawchromaticbar` que renderiza la barra cromatica especifica de cada marca.
3. El encabezado y pie de pagina dinamico con `\setupcorporateheader{TITULO}{REFERENCIA}`.
4. Cajas estilizadas `corpdirective`, `corpalert`, `corpnote`, `corpcard`, `corpmetric`, `corpcrypto`.
5. Macros de validacion de gobernanza: `\dualcontrolsignature`, `\cryptoseal`, `\approvalmatrixbadge`.

---

## 5. Sistema Tipografico Oficial (Investigacion de Brandbooks y Carpetas de Diseno)

Conforme a las directrices normativas verificadas en los Brandbooks Oficiales (`BOLETOS_MANUAL_DE_IDENTIDAD_VISUAL_Y_MARCA.pdf`, `WIT_MANUAL_DE_IDENTIDAD_VISUAL_Y_MARCA.pdf`, `GESTSOL_MANUAL_DE_IDENTIDAD_VISUAL_Y_MARCA.pdf` y las plantillas historicas de Grupo BNW):

1. **Capa Editorial / Impreso / PDF LaTeX**:
   - **Familia Primaria**: `Helvetica Neue` / `Helvetica` escalada al 94%.
   - **Implementacion LaTeX**:
     ```latex
     \RequirePackage[scaled=0.94]{helvet}
     \renewcommand{\familydefault}{\sfdefault}
     ```
   - **Justificacion Normativa**: Establecido como estandar mandatorio para documentos formales, tarjetas ejecutivas, manuales de procedimiento y papeleria corporativa en Grupo BNW, Boletos.la, Nodo, VINI y WIT.

2. **Capa de Datos Numericos, Precios y Fiscalidad SIFEN**:
   - **Familia Monospaced**: `Courier Mono` / `JetBrains Mono` (`tabular-nums`).
   - **Implementacion LaTeX**:
     ```latex
     \RequirePackage{courier}
     ```
   - **Uso Obligatorio**: CDC SIFEN de 44 digitos, importes monetarios (Gs. 130.000 / CLP $14.500.000), hashes criptograficos SHA-256 de conciliacion 2PC y cronometros de sesion.

3. **Jerarquia Ejecutiva Editorial (Norma WIT / BNW)**:
   - **Nombres Ejecutivos**: Mayusculas sostenidas (`ALL CAPS`) con tracking expandido (`\fontsize{10}{12}\selectfont\bfseries\MakeUppercase{...}`).
   - **Cargos y Roles**: Peso regular/ligero con color institucional atenuado (`corpTextMuted` / `corpTextAccent`).
