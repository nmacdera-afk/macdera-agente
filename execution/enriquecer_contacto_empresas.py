"""
Enriquece una lista de nombres de empresas (ganadores/participantes de
licitaciones) con datos de contacto (telefono, correo, direccion, sitio web)
cruzando contra el dataset abierto SECOP II - Proveedores Registrados
(datos.gov.co, qmzu-gj57).

Entrada: un JSON con una lista de objetos que tengan al menos {"nombre": "..."}
(ver .tmp/leads_comerciales/empresas_licitaciones_info.json, generado a partir
de los resultados de licitaciones.info).

Uso:
    python execution/enriquecer_contacto_empresas.py entrada.json salida.json
"""

import json
import os
import sys
import urllib.parse
import urllib.request

DATASET_URL = "https://www.datos.gov.co/resource/qmzu-gj57.json"


def normalizar(texto):
    if not texto:
        return ""
    reemplazos = {
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ñ": "n",
        "Á": "a", "É": "e", "Í": "i", "Ó": "o", "Ú": "u", "Ñ": "n",
    }
    for origen, destino in reemplazos.items():
        texto = texto.replace(origen, destino)
    texto = texto.upper()
    for token in (" S.A.S", " SAS", " S.A.", " SA", " LTDA", " LTDA.", ".", ","):
        texto = texto.replace(token, "")
    return " ".join(texto.split())


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


def buscar_empresa(nombre, app_token=None):
    params = {"$q": nombre, "$limit": 10}
    query = urllib.parse.urlencode(params)
    url = f"{DATASET_URL}?{query}"
    headers = {"X-App-Token": app_token} if app_token else {}
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=20) as respuesta:
            return json.loads(respuesta.read().decode("utf-8"))
    except Exception as exc:
        print(f"  ! error consultando '{nombre}': {exc}", file=sys.stderr)
        return []


def main():
    if len(sys.argv) < 3:
        print("Uso: python execution/enriquecer_contacto_empresas.py entrada.json salida.json")
        sys.exit(1)

    cargar_env()
    app_token = os.environ.get("SODA_APP_TOKEN")

    entrada = json.load(open(sys.argv[1], encoding="utf-8"))
    resultado = []
    encontrados = 0

    for i, empresa in enumerate(entrada):
        nombre = empresa["nombre"]
        objetivo_norm = normalizar(nombre)
        candidatos = buscar_empresa(nombre, app_token=app_token)

        match = None
        for c in candidatos:
            if normalizar(c.get("nombre", "")) == objetivo_norm:
                match = c
                break
        if not match and candidatos:
            # sin match exacto: usar el primero como candidato tentativo
            match = candidatos[0]

        enriquecido = dict(empresa)
        if match:
            enriquecido.update({
                "nit": match.get("nit"),
                "telefono": match.get("telefono"),
                "correo": match.get("correo"),
                "direccion": match.get("direccion"),
                "sitio_web": match.get("sitio_web"),
                "departamento": match.get("departamento"),
                "municipio": match.get("municipio"),
                "nombre_representante_legal": match.get("nombre_representante_legal"),
                "match_exacto": normalizar(match.get("nombre", "")) == objetivo_norm,
                "fuente_contacto": "SECOP II - Proveedores Registrados (qmzu-gj57)",
            })
            encontrados += 1
        else:
            enriquecido.update({
                "nit": None, "telefono": None, "correo": None, "direccion": None,
                "sitio_web": None, "departamento": None, "municipio": None,
                "nombre_representante_legal": None, "match_exacto": False,
                "fuente_contacto": "NO ENCONTRADO - buscar en internet",
            })

        resultado.append(enriquecido)
        print(f"[{i+1}/{len(entrada)}] {nombre} -> {'OK' if match else 'sin match'}")

    with open(sys.argv[2], "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print(f"\n{encontrados}/{len(entrada)} empresas encontradas en el registro abierto de SECOP II.")
    print(f"Guardado en: {sys.argv[2]}")


if __name__ == "__main__":
    main()
