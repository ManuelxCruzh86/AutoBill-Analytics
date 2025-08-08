import re
from datetime import datetime
from predictor_campos import predecir_campo

def parse_invoice_data(text):
    data = {}

    # Normaliza el texto para facilitar las búsquedas
    text = text.replace("\n", " ")

    # ----------- RFC EMISOR Y RECEPTOR FLEXIBLE -----------
    # Busca por label primero
    rfc_emisor = re.search(r'Emisor.*?R[\.]?F[\.]?C[\.]?[:\s\-]*([A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3})', text, re.IGNORECASE)
    rfc_receptor = re.search(r'Receptor.*?R[\.]?F[\.]?C[\.]?[:\s\-]*([A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3})', text, re.IGNORECASE)

    # Si no encuentra por label, busca todos los RFCs válidos
    rfcs = re.findall(r'[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}', text, re.IGNORECASE)

    if rfc_emisor:
        data['rfc_emisor'] = rfc_emisor.group(1)
    elif rfcs:
        data['rfc_emisor'] = rfcs[0]
    else:
        print("⚠️ RFC emisor no encontrado por regex, intentando predicción...")
        data['rfc_emisor'] = predecir_campo(text, "rfc_emisor")

    if rfc_receptor:
        data['rfc_receptor'] = rfc_receptor.group(1)
    elif len(rfcs) > 1:
        data['rfc_receptor'] = rfcs[1]
    else:
        print("⚠️ RFC receptor no encontrado por regex, intentando predicción...")
        data['rfc_receptor'] = predecir_campo(text, "rfc_receptor")



    # ----------- FECHA -----------
    fecha_match = re.search(r'([0-9]{4}-[0-9]{2}-[0-9]{2})', text)
    if not fecha_match:
        fecha_match = re.search(r'([0-9]{2}/[0-9]{2}/[0-9]{4})', text)
    if not fecha_match:
        fecha_match = re.search(r'([0-9]{2}/[0-9]{2}/[0-9]{2})', text)

    if fecha_match:
        fecha_str = fecha_match.group(1)
        data['fecha'] = fecha_str
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
    else:
        fecha_predicha = predecir_campo(text, "fecha")
        data["fecha"] = fecha_predicha
        try:
            fecha_obj = datetime.strptime(fecha_predicha, "%Y-%m-%d")
            data['dia'] = str(fecha_obj.day)
            data['mes'] = str(fecha_obj.month)
            data['anio'] = str(fecha_obj.year)
        except ValueError:
            pass

    # ----------- SUBTOTAL -----------
    subtotal_match = re.search(r'Subtotal[:\s\$]*([\d,]+\.\d{2})', text, re.IGNORECASE)
    if subtotal_match:
        data['subtotal'] = subtotal_match.group(1)
    else:
        data['subtotal'] = predecir_campo(text, "subtotal")

    # ----------- IVA -----------
    iva_match = re.search(r'IVA[:\s\$]*([\d,]+\.\d{2})', text, re.IGNORECASE)
    if iva_match:
        data['iva'] = iva_match.group(1)
    else:
        data['iva'] = predecir_campo(text, "iva")

     # ----------- TOTAL -----------
    total_matches = re.findall(r'Total(?:\s*(?:General|a Pagar))?[:\s\$]*([\d,]+\.\d{2})', text, re.IGNORECASE)
    if total_matches:
        data['total'] = total_matches[-1]  # Toma el último "Total"
    else:
        data['total'] = predecir_campo(text, "total")



    # ----------- FOLIO -----------
    folio_match = re.search(r'Folio[:\s\-]*([A-Z0-9\-]+)', text, re.IGNORECASE)
    if folio_match:
        data["folio"] = folio_match.group(1)
    else:
        data["folio"] = predecir_campo(text, "folio")

    # ----------- TEXTO OCR (para auditoría) -----------
    data["ocr_texto"] = text

    return data
