import re
from datetime import datetime

def parse_invoice_data(text):
    data = {}

    # Buscar RFC del emisor
    rfc_emisor = re.search(r'RFC.?emisor[:\s\-]*([A-ZÑ&]{3,4}[0-9]{6}[A-Z0-9]{3})', text, re.IGNORECASE)
    if rfc_emisor:
        data['rfc_emisor'] = rfc_emisor.group(1)

    # Buscar RFC del receptor
    rfc_receptor = re.search(r'RFC.?receptor[:\s\-]*([A-ZÑ&]{3,4}[0-9]{6}[A-Z0-9]{3})', text, re.IGNORECASE)
    if rfc_receptor:
        data['rfc_receptor'] = rfc_receptor.group(1)

    # Alternativa si solo hay dos RFCs en el texto
    if not rfc_emisor or not rfc_receptor:
        rfc_matches = re.findall(r'([A-ZÑ&]{3,4}[0-9]{6}[A-Z0-9]{3})', text)
        if len(rfc_matches) >= 2:
            data['rfc_emisor'] = rfc_matches[0]
            data['rfc_receptor'] = rfc_matches[1]

    # Buscar fecha en varios formatos
    fecha_match = re.search(r'([0-9]{4}-[0-9]{2}-[0-9]{2})', text)  # Formato: 2025-07-20
    if not fecha_match:
        fecha_match = re.search(r'([0-9]{2}/[0-9]{2}/[0-9]{4})', text)  # Formato: 28/06/2025
    if not fecha_match:
        fecha_match = re.search(r'([0-9]{2}/[0-9]{2}/[0-9]{2})', text)  # Formato: 28/06/25

    if fecha_match:
        fecha_str = fecha_match.group(1)
        data['fecha'] = fecha_str

        # Detectar y convertir el formato adecuado
        try:
            if "-" in fecha_str:
                fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d")
            elif len(fecha_str.split("/")[-1]) == 4:
                fecha_obj = datetime.strptime(fecha_str, "%d/%m/%Y")
            else:
                fecha_obj = datetime.strptime(fecha_str, "%d/%m/%y")

            data['dia'] = str(fecha_obj.day)
            data['mes'] = str(fecha_obj.month)
            data['anio'] = str(fecha_obj.year)
        except ValueError:
            print(f"⚠️ No se pudo convertir la fecha: {fecha_str}")

    # Totales
    for key in ['subtotal', 'iva', 'total']:
        match = re.search(fr'{key}[:\s\$]*([\d,]+\.\d{{2}})', text, re.IGNORECASE)
        if match:
            data[key] = match.group(1)

    # Proveedor
    proveedor_match = re.search(r'Proveedor[:\s\-]*(.*)', text)
    if proveedor_match:
        data['proveedor'] = proveedor_match.group(1).strip()

    return data
