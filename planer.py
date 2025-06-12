import xml.etree.ElementTree as ET
import requests

def get_daily_plan_from_url(url: str, klasse: str):
    # XML aus dem Internet abrufen
    response = requests.get(url)
    response.raise_for_status()  # Fehler werfen, wenn z. B. 404

    root = ET.fromstring(response.content)

    # Datum (optional)
    datum = root.find('.//DatumPlan')
    print(f"Tagesplan für {klasse} am {datum.text.strip() if datum is not None else 'unbekanntem Datum'}:\n")

    # Klasse finden
    kl_block = next(
        (kl for kl in root.findall('.//Kl') if kl.find('Kurz').text.strip() == klasse),
        None)
    if kl_block is None:
        raise ValueError(f"Klasse {klasse} nicht gefunden")

    # Stundenplan extrahieren
    plan = []
    for std in kl_block.find('Pl').findall('Std'):
        plan.append({
            'Stunde': std.find('St').text,
            'Beginn': std.find('Beginn').text,
            'Ende'  : std.find('Ende').text,
            'Fach'  : (std.find('Fa').text or '').strip(),
            'Lehrer': (std.find('Le').text or '').strip(),
            'Raum'  : (std.find('Ra').text or '').strip(),
            'Info'  : (std.find('If').text or '').strip()
        })

    # Ausgabe
    plan.sort(key=lambda s: int(s['Stunde']))
    for st in plan:
        print(f"{st['Stunde']}. {st['Beginn']}-{st['Ende']}  "
              f"{st['Fach']}  {st['Lehrer']}  {st['Raum']}  {st['Info']}")

# Nutzung
URL = "https://www.rwg-waren.de/stundenplan/vplan/mobdaten/Klassen.xml"
get_daily_plan_from_url(URL, "11A")
