# Papierkorb-Manager

![Python Version](https://img.shields.io/badge/Python-3.x-blue.svg) ![Windows Compatible](https://img.shields.io/badge/OS-Windows-green.svg)
---

### Beschreibung

Ein benutzerfreundlicher Windows-Papierkorb-Manager, erstellt mit Python und Tkinter. Dieses Tool bietet eine grafische Oberfläche, um den Papierkorb zu verwalten, Dateien und Ordner hinzuzufügen, wiederherzustellen oder zu löschen.

### Funktionen

* **GUI-Oberfläche:** Eine einfache und intuitive Benutzeroberfläche.
* **Automatische Aktualisierung:** Zeigt den Inhalt des Papierkorbs alle 5 Sekunden an.
* **Detaillierte Übersicht:** Listet Dateiname, Größe und Löschdatum jedes Elements auf.
* **Suchfunktion:** Durchsuche den Papierkorb nach bestimmten Dateinamen.
* **Drag-and-Drop:** Verschiebe Dateien und Ordner per Drag-and-Drop in den Papierkorb.
* **Sicheres Löschen:** Leere den gesamten Papierkorb mit einer Bestätigungsabfrage.
* **Wiederherstellen:** Stelle ausgewählte Elemente mit einem Klick wieder her.

---

### Installation und Nutzung

Es gibt zwei Wege, das Programm zu bekommen:

#### 1. Für Endnutzer: Die fertige `.exe`-Datei

* Lade die neueste Version der **`Papierkorb-Manager.exe`** von der [Releases-Seite](https://github.com/andylpz20025/Papierkorb-Manager/releases) herunter.
* git clone [https://github.com/andylpz20025/Papierkorb-Manager.git](https://github.com/andylpz20025/Papierkorb-Manager.git)
cd Papierkorb-Manager
* Du musst nichts installieren. Führe die `.exe`-Datei einfach aus.

#### 2. Für Entwickler: Über den Quellcode

Du kannst das gesamte Repository mit Git klonen, um den Quellcode zu erhalten und daran zu arbeiten.

1.  **Repository klonen:**
    Öffne dein Terminal (CMD) und führe den folgenden Befehl aus, um das gesamte Projekt herunterzuladen:
    ```bash
    git clone [https://github.com/andylpz20025/Papierkorb-Manager.git](https://github.com/andylpz20025/Papierkorb-Manager.git)
    cd Papierkorb-Manager
    ```

2.  **Abhängigkeiten installieren:**
    Installiere die benötigten Bibliotheken mit der `requirements.txt`-Datei:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Programm ausführen:**
    ```bash
    python muelleimer.py
    ```

---

### Troubleshooting

Sollten Probleme auftreten (z.B. Fehler beim Abrufen oder Verschieben von Dateien), liegt dies oft an Inkompatibilitäten mit der `winshell`-Bibliothek. Ein einfaches Update behebt das Problem in den meisten Fällen:
```bash
pip install --upgrade winshell
