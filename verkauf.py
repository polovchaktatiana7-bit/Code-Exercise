# =============================================================================
# VERKAUFSPROGRAMM - ausführlich kommentierte Version für Einsteiger
#
# Was macht das Programm?
#   1. Verkäufe eingeben und in einer Datei (Sales.json) speichern
#   2. Ein Kreisdiagramm zeigen: Umsatz je Produkt
#   3. Ein Liniendiagramm zeigen: Umsatz je Wochentag und Produkt
#
# Wie liest man das Programm?
#   Python führt den Code von oben nach unten aus. Zuerst werden die Importe
#   und Konstanten gelesen, dann die Funktionen "gemerkt" (noch nicht
#   ausgeführt!) und ganz am Ende wird mit main() das Menü gestartet.
#   Eine Funktion läuft also erst, wenn sie irgendwo aufgerufen wird.
# =============================================================================

# ---------------------------------------------------------------------------
# 1. IMPORTE: Hier holen wir uns fertige Werkzeuge, die Python mitbringt
#    (json, datetime) oder die man extra installiert hat (matplotlib).
# ---------------------------------------------------------------------------
import json  # zum Lesen und Schreiben von JSON-Dateien (ein Textformat für Daten)

# Aus dem Modul datetime holen wir uns zwei Dinge:
#   datetime  -> Datum und Uhrzeit (z. B. "jetzt")
#   timedelta -> eine Zeitspanne (z. B. "3 Tage"), mit der man rechnen kann
from datetime import datetime, timedelta

# matplotlib zeichnet die Diagramme. "as plt" ist nur eine Abkürzung,
# damit wir später plt.xyz() statt matplotlib.pyplot.xyz() schreiben können.
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# 2. KONSTANTEN: Werte, die sich im Programm nie ändern.
#    Konstanten schreibt man per Konvention GROSS.
#    Vorteil: Will man einen Dateinamen ändern, tut man das nur an EINER Stelle.
# ---------------------------------------------------------------------------

# Namen der Dateien (müssen im selben Ordner wie dieses Programm liegen)
PRODUKTE_DATEI = "Products.json"
VERKAEUFE_DATEI = "Sales.json"

# Eine Liste mit den Kürzeln der Wochentage. Eine Liste beginnt bei Position 0:
#   WOCHENTAGE[0] ist "Mo", WOCHENTAGE[6] ist "So".
# Python zählt Wochentage genauso: datetime.weekday() liefert 0 für Montag
# bis 6 für Sonntag. Deshalb passen Liste und Python-Zählung zusammen.
WOCHENTAGE = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]


# =============================================================================
# 3. HILFSFUNKTIONEN
#    Kleine Funktionen, die von mehreren Stellen im Programm benutzt werden.
#    Eine Funktion definiert man mit "def". Alles, was eingerückt darunter
#    steht, gehört zur Funktion.
# =============================================================================

# -------------------- Hilfsfunktionen zum Laden und Speichern von JSON-Dateien
def lade_json(dateiname):
    """Liest eine JSON-Datei und gibt den Inhalt als Liste zurück."""
    # Der Text in dreifachen Anführungszeichen direkt unter "def" heißt
    # Docstring und beschreibt, was die Funktion tut.

    # try/except: "Versuche das hier - und wenn ein bestimmter Fehler
    # auftritt, mach stattdessen das andere." So stürzt das Programm nicht ab.
    try:
        # "with open(...)" öffnet die Datei und schließt sie am Ende
        # automatisch wieder - auch wenn etwas schiefgeht.
        #   "r"            = read (nur lesen)
        #   encoding utf-8 = damit Umlaute (ä, ö, ü) richtig gelesen werden
        #   "as datei"     = unter diesem Namen können wir die Datei benutzen
        with open(dateiname, "r", encoding="utf-8") as datei:
            # json.load wandelt den Text der Datei in Python-Objekte um
            # (hier: eine Liste von Dictionaries). "return" gibt das Ergebnis
            # an die aufrufende Stelle zurück und beendet die Funktion.
            return json.load(datei)
    except FileNotFoundError:
        # Dieser Fehler tritt auf, wenn es die Datei nicht gibt.
        # Gibt es die Datei noch nicht, starten wir mit einer leeren Liste
        return []


def speichere_json(dateiname, daten):
    """Schreibt eine Liste in eine JSON-Datei."""
    # "w" = write (schreiben). Achtung: Die Datei wird dabei komplett neu
    # geschrieben, ein alter Inhalt wird überschrieben.
    with open(dateiname, "w", encoding="utf-8") as datei:
        # json.dump schreibt die Python-Daten als Text in die Datei.
        #   indent=2            -> schöne Einrückung, damit man es gut lesen kann
        #   ensure_ascii=False  -> Umlaute bleiben Umlaute (statt \u00e4 usw.)
        json.dump(daten, datei, indent=2, ensure_ascii=False)


def farben_je_produkt(anzahl):
    """Gibt für jedes Produkt eine feste Farbe zurück (gleiche Farben in Menüpunkt 2 und 3).

    Die Farbe hängt von der Position des Produkts in Products.json ab.
    """
    # plt.get_cmap("tab10") holt eine "Farbpalette" mit 10 gut
    # unterscheidbaren Farben. Mit (range(anzahl)) nehmen wir die ersten
    # "anzahl" Farben daraus: Produkt 1 bekommt Farbe 0, Produkt 2 Farbe 1 ...
    # Weil BEIDE Diagramme diese Funktion benutzen und die Produkte immer in
    # derselben Reihenfolge durchlaufen, hat jedes Produkt überall dieselbe Farbe.
    return plt.get_cmap("tab10")(range(anzahl))


# =============================================================================
# 4. MENÜFUNKTIONEN
#    Pro Menüpunkt gibt es eine Funktion. Das Hauptmenü (ganz unten)
#    ruft sie je nach Eingabe des Benutzers auf.
# =============================================================================

# -------------------- Menüfunktionen für die verschiedenen Optionen im Hauptmenü

# Menupunkt 1: Daten eingeben
def daten_eingeben():
    """Menüpunkt 1: Verkauf eingeben und speichern."""
    # Die Produktliste aus Products.json laden. Sie sieht ungefähr so aus:
    #   [{"Produkt": "Croissant", "Preis (EUR)": 1.6}, {...}, ...]
    # Jedes Produkt ist ein "Dictionary": Man holt Werte über einen
    # Schlüssel, z. B. produkt["Produkt"] -> "Croissant".
    produkte = lade_json(PRODUKTE_DATEI)

    # Produkte mit Nummern anzeigen
    print("\n--- Daten eingeben ---")  # "\n" erzeugt vorher eine Leerzeile

    # enumerate zählt beim Durchlaufen der Liste automatisch mit.
    # start=1 sorgt dafür, dass die Zählung bei 1 beginnt (statt bei 0),
    # weil Menschen bei "1." anfangen zu zählen.
    # In jedem Durchlauf ist "nummer" die Zahl und "produkt" das Dictionary.
    for nummer, produkt in enumerate(produkte, start=1):
        # Ein f-String (f"...") setzt Variablen in geschweiften Klammern direkt
        # in den Text ein. ":.2f" bedeutet: Zahl mit genau 2 Nachkommastellen.
        print(f"{nummer}. {produkt['Produkt']} ({produkt['Preis (EUR)']:.2f} EUR)")

    # Produkt auswählen
    # input() zeigt einen Text an und wartet, bis der Benutzer etwas eintippt.
    # Das Ergebnis ist IMMER Text (String), auch wenn man eine Zahl eintippt.
    auswahl = input("Welches Produkt? (Nummer eingeben): ")

    # Eingabe prüfen. Die Bedingung besteht aus zwei Teilen:
    #   not auswahl.isdigit()  -> die Eingabe besteht NICHT nur aus Ziffern
    #   not (1 <= int(auswahl) <= len(produkte))
    #                          -> die Zahl liegt NICHT zwischen 1 und der
    #                             Anzahl der Produkte (len = Länge der Liste)
    # "or" bedeutet: Es reicht, wenn EINER der beiden Teile zutrifft.
    # Wichtig: Ist der erste Teil schon wahr, wird der zweite gar nicht mehr
    # geprüft. So gibt int("abc") keinen Fehler.
    if not auswahl.isdigit() or not (1 <= int(auswahl) <= len(produkte)):
        print("Ungültige Auswahl!")
        return  # Funktion sofort verlassen, es wird nichts gespeichert

    # int(auswahl) macht aus dem Text eine Zahl. Wir ziehen 1 ab, weil die
    # Anzeige bei 1 beginnt, die Liste aber bei 0.
    produkt = produkte[int(auswahl) - 1]

    # Verkaufsmenge eingeben
    menge = input("Verkaufsmenge: ")
    # Die Menge muss eine ganze Zahl sein und mindestens 1.
    if not menge.isdigit() or int(menge) < 1:
        print("Bitte eine ganze Zahl größer als 0 eingeben!")
        return
    menge = int(menge)  # ab jetzt ist "menge" eine Zahl und kein Text mehr

    # Umsatz berechnen: Menge mal Preis
    # round(..., 2) rundet auf 2 Nachkommastellen (Cent-Beträge).
    umsatz = round(menge * produkt["Preis (EUR)"], 2)

    # Neuen Datensatz erstellen
    jetzt = datetime.now()  # aktuelles Datum und aktuelle Uhrzeit
    # Ein Datensatz ist ein Dictionary mit Schlüssel: Wert-Paaren.
    # strftime formatiert Datum/Uhrzeit als Text:
    #   %Y-%m-%d -> z. B. 2026-11-20   (Jahr-Monat-Tag)
    #   %H:%M    -> z. B. 14:35        (Stunde:Minute)
    datensatz = {
        "Datum": jetzt.strftime("%Y-%m-%d"),
        "Uhrzeit": jetzt.strftime("%H:%M"),
        "Produkt": produkt["Produkt"],
        "Anzahl": menge,
        "Umsatz": umsatz,
    }

    # An die bestehenden Verkäufe anhängen und speichern
    # Ablauf: alles laden -> neuen Datensatz hinten anhängen -> alles speichern
    verkaeufe = lade_json(VERKAEUFE_DATEI)
    verkaeufe.append(datensatz)  # append hängt ein Element ans Listenende an
    speichere_json(VERKAEUFE_DATEI, verkaeufe)

    print(f"Gespeichert: {menge} x {produkt['Produkt']} = {umsatz:.2f} EUR")


# Menupunkt 2: Auswertung Produkte
def auswertung_produkte():
    """Menüpunkt 2: Kreisdiagramm mit dem Umsatz je Produkt."""
    produkte = lade_json(PRODUKTE_DATEI)
    verkaeufe = lade_json(VERKAEUFE_DATEI)

    # Eine leere Liste gilt in Python als "falsch". "not verkaeufe" ist also
    # wahr, wenn noch kein einziger Verkauf gespeichert wurde.
    if not verkaeufe:
        print("\nEs sind noch keine Verkaufsdaten vorhanden!")
        return

    # Umsatz je Produkt aufsummieren (alle Produkte starten bei 0)
    # Das ist eine "Dictionary Comprehension": eine Kurzschreibweise, die für
    # jedes Produkt einen Eintrag  Produktname: 0.0  anlegt.
    # Ergebnis z. B.: {"Croissant": 0.0, "Muffin": 0.0, ...}
    umsatz_je_produkt = {produkt["Produkt"]: 0.0 for produkt in produkte}

    # Jetzt gehen wir alle Verkäufe durch und addieren den Umsatz beim
    # passenden Produkt dazu.
    for verkauf in verkaeufe:
        name = verkauf["Produkt"]
        # "in" prüft, ob der Name als Schlüssel im Dictionary vorkommt.
        # So werden Verkäufe von Produkten ignoriert, die es nicht mehr gibt.
        if name in umsatz_je_produkt:
            umsatz_je_produkt[name] += verkauf["Umsatz"]  # += heißt: addiere dazu

    # Aus dem Dictionary machen wir zwei Listen, die gleich lang sind und in
    # derselben Reihenfolge stehen: die Namen und die zugehörigen Umsätze.
    namen = list(umsatz_je_produkt.keys())
    werte = list(umsatz_je_produkt.values())
    gesamt = sum(werte)  # sum zählt alle Zahlen einer Liste zusammen

    # Wenn nichts verkauft wurde, gibt es nichts zu zeichnen (und wir würden
    # unten durch 0 teilen).
    if gesamt == 0:
        print("\nDer Gesamtumsatz ist 0 - es gibt nichts darzustellen.")
        return

    # Für jedes Produkt eine eigene Farbe
    farben = farben_je_produkt(len(namen))

    # Beschriftung im Diagramm: Umsatz in Euro und Prozentanteil
    # Das ist eine Funktion IN einer Funktion. matplotlib ruft sie für jedes
    # Tortenstück auf und übergibt den Prozentwert (0 bis 100).
    # Was wir zurückgeben, wird als Text ins Tortenstück geschrieben.
    def beschriftung(prozent):
        if prozent == 0:
            return ""  # Produkte ohne Umsatz nicht beschriften
        euro = prozent / 100 * gesamt  # Prozent wieder in Euro umrechnen
        return f"{euro:.2f} EUR\n{prozent:.1f} %"

    # plt.subplots() erzeugt ein Fenster (fig) und darin eine Zeichenfläche (ax).
    # figsize=(8, 6) legt die Größe in Zoll fest (Breite, Höhe).
    fig, ax = plt.subplots(figsize=(8, 6))

    # ax.pie zeichnet das Kreisdiagramm und gibt drei Dinge zurück.
    # Wir brauchen nur die "keile" (die Tortenstücke) für die Legende.
    # Die anderen beiden nennen wir mit Unterstrich vorn - das ist die
    # Konvention für "wird nicht benutzt".
    keile, _texte, _prozente = ax.pie(
        werte,                          # Größe der Stücke
        colors=farben,                  # Farbe je Stück
        autopct=beschriftung,           # unsere Beschriftungs-Funktion von oben
        startangle=90,                  # Start oben (12-Uhr-Position)
        counterclock=False,             # im Uhrzeigersinn zeichnen
        wedgeprops={"edgecolor": "white"},  # weiße Trennlinie zwischen den Stücken
    )

    # Legende mit Produktname und Umsatz
    # zip(namen, werte) legt zwei Listen "wie ein Reißverschluss" zusammen:
    # Es entstehen Paare (Name, Wert), die wir direkt in n und w entpacken.
    # Das Ganze ist eine List Comprehension: eine Kurzschreibweise, die eine
    # neue Liste mit einem Text pro Produkt baut.
    legendentexte = [f"{n} ({w:.2f} EUR)" for n, w in zip(namen, werte)]
    # loc/bbox_to_anchor schieben die Legende rechts neben das Diagramm.
    ax.legend(keile, legendentexte, title="Produkte",
              loc="center left", bbox_to_anchor=(1, 0.5))

    ax.set_title(f"Umsatz je Produkt (Gesamt: {gesamt:.2f} EUR)")
    ax.axis("equal")  # Kreis statt Ellipse
    plt.tight_layout()  # Ränder automatisch anpassen, damit nichts abgeschnitten wird
    plt.show()  # Fenster mit dem Diagramm anzeigen (Programm wartet, bis es geschlossen wird)


# Menupunkt 3: Auswertung Wochenumsatz
def auswertung_wochenumsatz():
    """Menüpunkt 3: Liniendiagramm mit dem Umsatz je Wochentag (Mo-So) und Produkt.

    Ausgewertet wird die aktuelle Kalenderwoche (Montag bis Sonntag).
    """
    produkte = lade_json(PRODUKTE_DATEI)
    verkaeufe = lade_json(VERKAEUFE_DATEI)

    if not verkaeufe:
        print("\nEs sind noch keine Verkaufsdaten vorhanden!")
        return

    # --- Schritt 1: Die aktuelle Woche bestimmen ---
    # .date() schneidet die Uhrzeit ab, übrig bleibt nur das Datum.
    heute = datetime.now().date()
    # heute.weekday() ist 0 (Montag) bis 6 (Sonntag). Wenn heute Mittwoch (2)
    # ist, gehen wir 2 Tage zurück und landen auf dem Montag dieser Woche.
    # timedelta(days=...) ist die Zeitspanne, mit der wir rechnen.
    montag = heute - timedelta(days=heute.weekday())
    # Der Sonntag ist 6 Tage nach dem Montag.
    sonntag = montag + timedelta(days=6)

    # --- Schritt 2: Umsätze je Produkt und Wochentag aufsummieren ---
    # Für jedes Produkt legen wir eine Liste mit 7 Nullen an - eine Zahl für
    # jeden Wochentag. [0.0] * 7 bedeutet: "wiederhole die 0.0 siebenmal".
    # Aufbau: {"Croissant": [Mo, Di, Mi, Do, Fr, Sa, So], ...}
    umsatz = {produkt["Produkt"]: [0.0] * 7 for produkt in produkte}

    for verkauf in verkaeufe:
        # strptime ist das Gegenstück zu strftime: Es wandelt einen Text wie
        # "2026-11-16" in ein Datum um, mit dem man rechnen und vergleichen kann.
        tag = datetime.strptime(verkauf["Datum"], "%Y-%m-%d").date()
        name = verkauf["Produkt"]
        # "montag <= tag <= sonntag" prüft, ob der Verkauf in dieser Woche liegt.
        # Außerdem muss das Produkt bekannt sein.
        if montag <= tag <= sonntag and name in umsatz:
            # tag.weekday() ist 0 bis 6 und dient hier direkt als Position in
            # der Liste: Montag -> Position 0, Dienstag -> Position 1 usw.
            umsatz[name][(tag.weekday() + 1) % 7] += verkauf["Umsatz"]

    # --- Schritt 3: Prüfen, ob es überhaupt etwas zu zeichnen gibt ---
    # Verschachtelte Summe: Für jede Wochenliste die Summe bilden und diese
    # Summen wieder zusammenzählen = Gesamtumsatz der Woche.
    gesamt = sum(sum(werte) for werte in umsatz.values())
    if gesamt == 0:
        print("\nIn dieser Woche gibt es noch keine Verkäufe - nichts darzustellen.")
        return

    # --- Schritt 4: Farben und Beschriftungen vorbereiten ---
    # Dieselben Farben wie im Kreisdiagramm (gleiche Reihenfolge der Produkte)
    farben = farben_je_produkt(len(umsatz))

    # X-Achse: Wochentag mit Datum, z. B. "Mo\n16.11."
    # Eine List Comprehension, die für i = 0 bis 6 einen Text baut:
    #   WOCHENTAGE[i]                  -> "Mo", "Di", ...
    #   montag + timedelta(days=i)     -> das Datum des i-ten Tages der Woche
    #   strftime('%d.%m.')             -> Datum als Text, z. B. "16.11."
    # "\n" macht einen Zeilenumbruch: Wochentag oben, Datum darunter.
    beschriftungen = [
        f"{WOCHENTAGE[i]}\n{(montag + timedelta(days=i)).strftime('%d.%m.')}"
        for i in range(7)  # range(7) liefert die Zahlen 0, 1, 2, 3, 4, 5, 6
    ]

    # --- Schritt 5: Das Liniendiagramm zeichnen ---
    fig, ax = plt.subplots(figsize=(10, 6))

    # Wir laufen gleichzeitig durch Farben und Produkte (zip, wie oben).
    # umsatz.items() liefert Paare (Produktname, Wochenliste), die wir direkt
    # in "(name, werte)" entpacken. Die Klammern sind nötig, weil zip selbst
    # schon ein Paar bildet: (farbe, (name, werte)).
    for farbe, (name, werte) in zip(farben, umsatz.items()):
        # Eine Linie zeichnen:
        #   range(7)     -> x-Positionen 0 bis 6 (für Mo bis So)
        #   werte        -> y-Werte (Umsatz je Tag)
        #   marker="o"   -> ein Punkt an jedem Tag
        #   linewidth=2  -> Liniendicke
        #   label=...    -> Text für die Legende (Name + Wochenumsatz)
        ax.plot(range(7), werte, marker="o", linewidth=2, color=farbe,
                label=f"{name} ({sum(werte):.2f} EUR)")

    # Die x-Achse hat die Positionen 0 bis 6 - statt der Zahlen zeigen wir
    # unsere Beschriftungen (Wochentag + Datum) an.
    ax.set_xticks(range(7))
    ax.set_xticklabels(beschriftungen)
    ax.set_xlabel("Wochentag")
    ax.set_ylabel("Umsatz (EUR)")
    ax.set_ylim(bottom=0)  # y-Achse beginnt bei 0, nicht irgendwo darüber
    ax.grid(True, linestyle="--", alpha=0.5)  # gestricheltes, halbtransparentes Gitter
    ax.legend(title="Produkte", loc="center left", bbox_to_anchor=(1, 0.5))
    ax.set_title(
        f"Wochenumsatz je Produkt ({montag.strftime('%d.%m.')} - "
        f"{sonntag.strftime('%d.%m.%Y')}, Gesamt: {gesamt:.2f} EUR)"
    )
    plt.tight_layout()
    plt.show()


# =============================================================================
# 5. HAUPTMENÜ
#    Hier läuft das eigentliche Programm: Menü anzeigen, Eingabe lesen,
#    passende Funktion aufrufen - und das so lange, bis "Exit" eingegeben wird.
# =============================================================================

# -------------------- Hauptmenü
def main():
    """Hauptmenü: läuft in einer Schleife, bis der Benutzer 'Exit' eingibt."""
    # "while True" ist eine Endlosschleife: Sie wiederholt ihren Inhalt immer
    # wieder. Verlassen wird sie nur durch "break" (siehe unten bei "exit").
    while True:
        print("\n===== Hauptmenü =====")
        print("1. Daten eingeben")
        print("2. Auswertung Produkte (Kreisdiagramm)")
        print("3. Auswertung Wochenumsatz (Liniendiagramm)")
        print("Exit zum Beenden")

        # .strip() entfernt Leerzeichen vorn und hinten,
        # .lower() macht alles klein. So werden "Exit", "EXIT" und " exit "
        # alle als "exit" erkannt.
        wahl = input("Ihre Wahl: ").strip().lower()

        # if / elif / else: Es wird die erste passende Bedingung ausgeführt,
        # alle weiteren werden übersprungen. "==" vergleicht zwei Werte
        # (ein einzelnes "=" würde dagegen etwas zuweisen).
        if wahl == "1":
            daten_eingeben()
        elif wahl == "2":
            auswertung_produkte()
        elif wahl == "3":
            auswertung_wochenumsatz()
        elif wahl == "exit":
            print("Programm beendet. Auf Wiedersehen!")
            break  # beendet die while-Schleife -> das Programm ist zu Ende
        else:
            # Greift bei allem anderen, z. B. "7" oder "abc".
            print("Ungültige Eingabe, bitte 1, 2, 3 oder Exit eingeben.")


# Hier startet das Programm wirklich: Ohne diesen Aufruf wären oben nur
# Funktionen definiert, aber nichts würde passieren.
main()
