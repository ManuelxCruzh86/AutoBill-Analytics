# src/extractor.py

import re

def parse_invoice_data(text):
    data = {}

    # Buscar RFC (Formato general de RFCs mexicanos)
    rfc_match = re.search(r'RFC[:\s\-]*([A-ZÑ&]{3,4}[0-9]{6}[A-Z0-9]{3})', text, re.IGNORECASE)
    if rfc_match:
        data['rfc'] = rfc_match.group(1)

    # Buscar fecha (varios formatos)
    date_match = re.search(r'Fecha[:\s\-]*([0-9]{2}/[0-9]{2}/[0-9]{4})', text)
    if date_match:
        data['fecha'] = date_match.group(1)

    # Buscar total (varias variantes de texto)
    total_match = re.search(r'Total[:\s\$]*([\d,]+\.\d{2})', text)
    if total_match:
        data['total'] = total_match.group(1)

    # Buscar subtotal
    subtotal_match = re.search(r'Subtotal[:\s\$]*([\d,]+\.\d{2})', text)
    if subtotal_match:
        data['subtotal'] = subtotal_match.group(1)

    # Buscar IVA
    iva_match = re.search(r'IVA[:\s\$]*([\d,]+\.\d{2})', text)
    if iva_match:
        data['iva'] = iva_match.group(1)

    # Buscar proveedor (como línea que empieza con "Proveedor" o similar)
    proveedor_match = re.search(r'Proveedor[:\s\-]*(.*)', text)
    if proveedor_match:
        data['proveedor'] = proveedor_match.group(1).strip()

    return data
