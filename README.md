# MyKlaus2
MyKlaus

## Nutzungsvorbereitung

### Module Installieren
Zur Nutzung dieses Projektes müssen als erstes die benötigen Python Module installiert werden. Um dies zu tun kann entweder die Eingabeaufforderung (cmd) genutzt werden oder es wird direkt in Visual Studio gemacht.

#### Die Installation mit Hilfe der Eingabeaufforderung:
1. Cmd Starten
2. In das Projektverzeichnis navigieren
3. Folgenden Befehl eingaben
```cmd
pip install -r requirements.txt
```

#### Installation mit Hilfe von Visual Studio
1. Projektmappe in Visual Studio öffnen
2. Rechtsklick auf die aktive Python-Umgebung
![Siehe Bild](https://i.ibb.co/4sQBhCn/1.png)
3. Im Dropdown "Aus 'requirements.txt' installieren" anklicken
![Siehe Bild](https://i.ibb.co/qxdrRRd/2.png)

### Datenbankvorbereitung
Des Weiteren nutzt MyKlaus2 eine MySQL-Datenbank.
Nachdem der MySql Server installiert ist muss eine Datenbank erstellt werden
```MySql
CREATE DATABASE myklaus2 CHARACTER SET UTF8;
```

Nun muss in der settings.ini im Sektor "Database" die URI und ggf. der Port angepasst werden.

Zum Schluss müssen die Tabellen noch erstellt werden. Dafür öffnen wir die Eingabeaufforderung und navigieren ind das Projektverzeichnis und geben den Befehl ein:
```cmd
python initdb.py
```

Wenn die Initialisierung erfolgreich war sollte in der Konsole "Initialized the database." stehen.

## WSGI Konfiguration
Gute beschreibung zur Konfiguration ist hier zu Finden: [Klick mich](https://gist.github.com/bluekvirus/c88cd0f67adf71197d9bedf1d62f6333#user-content-configure-uwsgi-and-nginx)