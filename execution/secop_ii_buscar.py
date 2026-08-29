"""
Busca procesos de contratación en SECOP II (datos abiertos, dataset p6dx-8zbt de
Colombia Compra Eficiente / Socrata) que matcheen las palabras clave y el valor
minimo definidos en directives/prospeccion_licitaciones.md.

Uso:
    python execution/secop_ii_buscar.py [--dias N] [--valor-minimo N] [--salida ruta.json]

No requiere librerias externas (solo stdlib). Si existe la variable de entorno
SODA_APP_TOKEN en .env, se usa para evitar throttling de la API de Socrata
(no es obligatoria para volumenes bajos de consultas).
"""

import argparse
import csv
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

DATASET_URL = "https://www.datos.gov.co/resource/p6dx-8zbt.json"

PALABRAS_CLAVE = [
    "piso vinilico",
    "piso spc",
    "vinilo spc",
    "piso laminado",
    "piso en rollo",
    "acabados de piso",
    "revestimiento de piso",
    "piso flotante",
    "hydrocore",
]

# Palabras que indican match "alto" (marca de producto / termino muy especifico
# del catalogo MACDERA) vs. "medio" (termino generico de acabados de piso).
PALABRAS_MATCH_ALTO = {
    "piso vinilico", "piso spc", "vinilo spc", "piso laminado", "hydrocore",
}


def cargar_env(ruta_env=".env"):
    """Carga variables simples KEY=VALUE de un archivo .env sin dependencias externas."""
    if not os.path.exists(ruta_env):
        return
    with open(ruta_env, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith("#") or "=" not in linea:
                continue
            clave, _, valor = linea.partition("=")
            os.environ.setdefault(clave.strip(), valor.strip())


def normalizar(texto):
    if not texto:
        return ""
    reemplazos = {
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ñ": "n",
        "Á": "a", "É": "e", "Í": "i", "Ó": "o", "Ú": "u", "Ñ": "n",
    }
    for origen, destino in reemplazos.items():
        texto = texto.replace(origen, destino)
    return texto.lower()


def consultar_socrata(params, app_token=None):
    query = urllib.parse.urlencode(params)
    url = f"{DATASET_URL}?{query}"
    headers = {}
    if app_token:
        headers["X-App-Token"] = app_token
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as respuesta:
        return json.loads(respuesta.read().decode("utf-8"))


def buscar_por_palabra_clave(palabra, desde_iso, valor_minimo, app_token=None):
    """Trae candidatos amplios via $q (Socrata hace full-text por token, tipo OR,
    no por frase exacta) y luego filtra en cliente exigiendo que la frase completa
    aparezca en el nombre o la descripcion del procedimiento. Sin este filtro,
    busquedas de dos palabras como 'piso spc' devuelven falsos positivos como
    'Obra piso 7' (matchea el token 'piso' solo)."""
    where = (
        f"precio_base >= {valor_minimo} "
        f"AND estado_de_apertura_del_proceso = 'Abierto' "
        f"AND fecha_de_publicacion_del >= '{desde_iso}'"
    )
    params = {
        "$q": palabra,
        "$where": where,
        "$order": "fecha_de_publicacion_del DESC",
        "$limit": 1000,
    }
    try:
        candidatos = consultar_socrata(params, app_token=app_token)
    except Exception as exc:
        print(f"  ! error consultando '{palabra}': {exc}", file=sys.stderr)
        return []

    frase = normalizar(palabra)
    resultados = []
    for proceso in candidatos:
        texto = normalizar(proceso.get("nombre_del_procedimiento", "")) + " " + \
            normalizar(proceso.get("descripci_n_del_procedimiento", ""))
        if frase in texto:
            resultados.append(proceso)
    return resultados


def clasificar_match(proceso, palabras_encontradas):
    if any(p in PALABRAS_MATCH_ALTO for p in palabras_encontradas):
        return "alto"
    return "medio"


def dias_hasta(fecha_iso):
    if not fecha_iso:
        return None
    try:
        fecha = datetime.fromisoformat(fecha_iso.replace("Z", "+00:00"))
    except ValueError:
        return None
    if fecha.tzinfo is None:
        fecha = fecha.replace(tzinfo=timezone.utc)
    ahora = datetime.now(timezone.utc)
    return (fecha - ahora).total_seconds() / 3600.0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dias", type=int, default=3,
                         help="Buscar procesos publicados en los ultimos N dias (default: 3)")
    parser.add_argument("--valor-minimo", type=int, default=6_000_000,
                         help="Valor minimo del proceso en COP (default: 6.000.000)")
    parser.add_argument("--salida", default=None,
                         help="Ruta base de salida (sin extension). Default: .tmp/secop_ii/AAAAMMDD_HHMM")
    args = parser.parse_args()

    cargar_env()
    app_token = os.environ.get("SODA_APP_TOKEN")

    desde = datetime.now(timezone.utc) - timedelta(days=args.dias)
    desde_iso = desde.strftime("%Y-%m-%dT00:00:00.000")

    procesos_por_id = {}
    print(f"Buscando en SECOP II procesos desde {desde_iso} con valor >= {args.valor_minimo:,} COP")
    for palabra in PALABRAS_CLAVE:
        resultados = buscar_por_palabra_clave(palabra, desde_iso, args.valor_minimo, app_token=app_token)
        print(f"  - '{palabra}': {len(resultados)} resultado(s)")
        for proceso in resultados:
            id_proceso = proceso.get("id_del_proceso")
            if not id_proceso:
                continue
            entrada = procesos_por_id.setdefault(id_proceso, {"proceso": proceso, "palabras": set()})
            entrada["palabras"].add(palabra)

    filas = []
    for id_proceso, datos in procesos_por_id.items():
        proceso = datos["proceso"]
        palabras = sorted(datos["palabras"])
        fecha_limite = proceso.get("fecha_de_recepcion_de")
        horas_restantes = dias_hasta(fecha_limite)
        urgente = horas_restantes is not None and 0 <= horas_restantes <= 48

        fila = {
            "id_del_proceso": id_proceso,
            "referencia_del_proceso": proceso.get("referencia_del_proceso"),
            "entidad": proceso.get("entidad"),
            "ciudad_entidad": proceso.get("ciudad_entidad"),
            "departamento_entidad": proceso.get("departamento_entidad"),
            "nombre_del_procedimiento": proceso.get("nombre_del_procedimiento"),
            "modalidad_de_contratacion": proceso.get("modalidad_de_contratacion"),
            "precio_base": proceso.get("precio_base"),
            "fase": proceso.get("fase"),
            "estado_del_procedimiento": proceso.get("estado_del_procedimiento"),
            "fecha_de_publicacion_del": proceso.get("fecha_de_publicacion_del"),
            "fecha_de_recepcion_de": fecha_limite,
            "horas_restantes": round(horas_restantes, 1) if horas_restantes is not None else None,
            "urgente_48h": urgente,
            "nivel_de_match": clasificar_match(proceso, palabras),
            "palabras_clave_encontradas": ", ".join(palabras),
            "url_proceso": (proceso.get("urlproceso") or {}).get("url"),
            "plataforma": "SECOP II",
        }
        filas.append(fila)

    filas.sort(key=lambda f: (f["horas_restantes"] is None, f["horas_restantes"] or 0))

    if args.salida:
        base_salida = args.salida
    else:
        os.makedirs(os.path.join(".tmp", "secop_ii"), exist_ok=True)
        marca = datetime.now().strftime("%Y%m%d_%H%M")
        base_salida = os.path.join(".tmp", "secop_ii", marca)

    ruta_json = base_salida + ".json"
    ruta_csv = base_salida + ".csv"

    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(filas, f, ensure_ascii=False, indent=2)

    if filas:
        with open(ruta_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
            writer.writeheader()
            writer.writerows(filas)

    urgentes = [f for f in filas if f["urgente_48h"]]
    print(f"\nTotal procesos unicos encontrados: {len(filas)}")
    print(f"Urgentes (cierre <48h): {len(urgentes)}")
    print(f"Guardado en: {ruta_json}" + (f" y {ruta_csv}" if filas else ""))


if __name__ == "__main__":
    main()
