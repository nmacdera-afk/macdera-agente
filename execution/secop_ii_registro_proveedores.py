"""
Construye una base de datos de leads comerciales (constructoras, contratistas,
proveedores de acabados/construccion) a partir del registro abierto de
proveedores de SECOP II en Colombia Compra Eficiente (dataset Socrata
qmzu-gj57, "SECOP II - Proveedores Registrados", ~141.000 empresas).

Este dataset YA trae telefono, correo, direccion, sitio web y datos del
representante legal para cada empresa registrada como proveedor del Estado
-- por eso es la fuente prioritaria de enriquecimiento de contacto antes de
recurrir a busqueda en internet (mas rapido, gratis y sin ambiguedad de
"cual empresa es" entre varias con nombre parecido).

Limitacion importante (ver directives/prospeccion_licitaciones.md): este
dataset es un DIRECTORIO de empresas registradas, no una lista de quienes
ofertaron en un proceso especifico. La lista de "aspirantes" (oferentes) por
proceso puntual solo se ve en la pagina publica de cada proceso en
community.secop.gov.co, que esta protegida con ReCaptcha -- no se puede
scrapear de forma automatica (regla: nunca sortear CAPTCHAs). Por eso este
script filtra por categoria de negocio + ubicacion (prospeccion en frio,
Objetivo 1 de la directiva) en vez de por proceso especifico.

Uso:
    python execution/secop_ii_registro_proveedores.py [--departamentos ...] [--categorias ...] [--salida ruta]
"""

import argparse
import csv
import json
import os
import sys
import urllib.parse
import urllib.request

DATASET_URL = "https://www.datos.gov.co/resource/qmzu-gj57.json"

DEPARTAMENTOS_DEFAULT = ["bogota", "distrito capital", "antioquia"]

# Categorias UNSPSC (campo "descripcion_categoria_principal") relevantes para
# MACDERA: constructoras/contratistas que compran acabados de piso como
# insumo, y proveedores de materiales de acabado (competidores/instaladores
# que tambien pueden ser canal). Ajustar con el equipo comercial segun
# resultados reales.
CATEGORIAS_DEFAULT = [
    "Estructuras y edificios permanentes",
    "Estructuras y edificios prefabricados",
    "Estructuras y edificios móviles",
    "Materiales estructurales",
    "Productos de construcción estructurales",
    "Componentes estructurales y formas básicas",
    "Componentes de construcción de estructura portátil",
    "Equipo de apoyo para Construcción y Mantenimiento",
    "Maquinaria y equipo pesado de construcción",
    "Materiales de acabado de interiores",
    "Materiales para acabado de exteriores",
    "Hormigón, cemento y yeso",
    "Instalaciones de plomería",
]


def normalizar(texto):
    if not texto:
        return ""
    reemplazos = {
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ñ": "n",
        "Á": "a", "É": "e", "Í": "i", "Ó": "o", "Ú": "u", "Ñ": "n",
    }
    for origen, destino in reemplazos.items():
        texto = texto.replace(origen, destino)
    return texto.lower().strip()


def cargar_env(ruta_env=".env"):
    if not os.path.exists(ruta_env):
        return
    with open(ruta_env, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith("#") or "=" not in linea:
                continue
            clave, _, valor = linea.partition("=")
            os.environ.setdefault(clave.strip(), valor.strip())


def consultar_pagina(offset, limite, categorias, app_token=None):
    categorias_sql = ", ".join("'{}'".format(c.replace("'", "''")) for c in categorias)
    where = f"esta_activa = 'Si' AND descripcion_categoria_principal in ({categorias_sql})"
    params = {
        "$where": where,
        "$limit": limite,
        "$offset": offset,
        "$order": "nombre",
    }
    query = urllib.parse.urlencode(params)
    url = f"{DATASET_URL}?{query}"
    headers = {"X-App-Token": app_token} if app_token else {}
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as respuesta:
        return json.loads(respuesta.read().decode("utf-8"))


def traer_todos(categorias, app_token=None, tam_pagina=1000, tope_paginas=50):
    resultados = []
    offset = 0
    for _ in range(tope_paginas):
        pagina = consultar_pagina(offset, tam_pagina, categorias, app_token=app_token)
        resultados.extend(pagina)
        if len(pagina) < tam_pagina:
            break
        offset += tam_pagina
    return resultados


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--departamentos", nargs="+", default=DEPARTAMENTOS_DEFAULT,
                         help="Fragmentos (normalizados, sin tildes) que deben aparecer en 'departamento'. Default: Bogota/Antioquia.")
    parser.add_argument("--categorias", nargs="+", default=CATEGORIAS_DEFAULT,
                         help="Lista de valores exactos de 'descripcion_categoria_principal' a incluir.")
    parser.add_argument("--salida", default=None, help="Ruta base de salida (sin extension).")
    args = parser.parse_args()

    cargar_env()
    app_token = os.environ.get("SODA_APP_TOKEN")

    print(f"Consultando registro de proveedores SECOP II ({len(args.categorias)} categoria(s))...")
    crudos = traer_todos(args.categorias, app_token=app_token)
    print(f"  Total registros activos en esas categorias (todo el pais): {len(crudos)}")

    deptos_norm = [normalizar(d) for d in args.departamentos]
    filas = []
    for r in crudos:
        depto_norm = normalizar(r.get("departamento"))
        if not any(d in depto_norm for d in deptos_norm):
            continue
        filas.append({
            "nit": r.get("nit"),
            "nombre": r.get("nombre"),
            "categoria_principal": r.get("descripcion_categoria_principal"),
            "telefono": r.get("telefono"),
            "correo": r.get("correo"),
            "direccion": r.get("direccion"),
            "sitio_web": r.get("sitio_web"),
            "departamento": r.get("departamento"),
            "municipio": r.get("municipio"),
            "tipo_empresa": r.get("tipo_empresa"),
            "es_pyme": r.get("espyme"),
            "nombre_representante_legal": r.get("nombre_representante_legal"),
            "telefono_representante_legal": r.get("telefono_representante_legal"),
            "correo_representante_legal": r.get("correo_representante_legal"),
            "fecha_creacion": r.get("fecha_creacion"),
            "fuente": "SECOP II - Proveedores Registrados (datos.gov.co qmzu-gj57)",
        })

    # de-duplicar por NIT (una empresa puede repetirse si tiene mas de una fila de categoria)
    por_nit = {}
    for fila in filas:
        nit = fila["nit"] or fila["nombre"]
        if nit not in por_nit:
            por_nit[nit] = fila
    filas_unicas = list(por_nit.values())
    filas_unicas.sort(key=lambda f: (f["municipio"] or "", f["nombre"] or ""))

    con_telefono = sum(1 for f in filas_unicas if f["telefono"])
    con_correo = sum(1 for f in filas_unicas if f["correo"])

    if args.salida:
        base_salida = args.salida
    else:
        os.makedirs(os.path.join(".tmp", "leads_comerciales"), exist_ok=True)
        base_salida = os.path.join(".tmp", "leads_comerciales", "registro_proveedores")

    with open(base_salida + ".json", "w", encoding="utf-8") as f:
        json.dump(filas_unicas, f, ensure_ascii=False, indent=2)
    if filas_unicas:
        with open(base_salida + ".csv", "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(filas_unicas[0].keys()))
            writer.writeheader()
            writer.writerows(filas_unicas)

    print(f"\nEmpresas unicas en Bogota/Antioquia para esas categorias: {len(filas_unicas)}")
    print(f"  Con telefono: {con_telefono} | Con correo: {con_correo}")
    print(f"Guardado en: {base_salida}.json" + (f" y {base_salida}.csv" if filas_unicas else ""))


if __name__ == "__main__":
    main()
