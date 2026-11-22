# WiZ BLE Smart Dimmer in Home Assistant – ohne WiZ-Lampe

**Inoffizielle, experimentelle Lösung für den 2026 erschienenen WiZ Smart Dimmer mit 8 Tasten und Bluetooth.** Du brauchst weder eine WiZ-Lampe noch einen WiZ-Hub: Dein Home Assistant empfängt die Bluetooth-Signale und schaltet dadurch beliebige bereits in Home Assistant eingebundene Lampen (etwa Govee, Matter oder Zigbee).

**Getestet:** Ein Gerät mit Home Assistant Core 2026.11.2 und einem lokalen Broadcom-Bluetooth-Adapter. Andere Hardware- oder Firmwareversionen sind noch nicht bestätigt. Funktioniert nicht mit der älteren WiZmote-Fernbedienung.

## Einrichtung

1. Ab Home Assistant 2026.11: **Einstellungen → Marketplace → Aus Link hinzufügen**, dann `https://github.com/janbro2/ha-wiz-ble-smart-dimmer` eingeben und die Integration installieren. Alternativ das Repository als ZIP herunterladen und den Ordner `custom_components/wiz_ble_dimmer/` nach `/config/custom_components/wiz_ble_dimmer/` kopieren.
2. Falls angefordert, Home Assistant neu starten.
3. Unter **Einstellungen → Geräte & Dienste → Integration hinzufügen** nach **WiZ BLE Smart Dimmer (Unofficial)** suchen.
4. Eigene Bluetooth-Adresse des Dimmers eintragen. Diese ist **für jedes Gerät anders**; keine MAC-Adresse aus einem Beispiel übernehmen.

### Bluetooth-Adresse finden

- **Einstellungen → Geräte & Dienste → Bluetooth → Werbepaketmonitor** öffnen.
- Mehrfach den Dimmer drücken, ggf. direkt neben dem Home-Assistant-Bluetooth-Stick.
- Ein *nicht verbindbares* Bluetooth-Gerät suchen, das Manufacturer-ID `1559` (`0x0617`) sendet. Die Daten sollten sich beim Tastendruck ändern.
- Die Adresse in der Integration eingeben.

### Funktion prüfen

Unter **Entwicklerwerkzeuge → Ereignisse** auf `wiz_dimmer_button` lauschen. Ein Tastendruck erzeugt beispielsweise `action: "on"` und `code: "0101"`. Wenn keine Ereignisse erscheinen, zuerst den Bluetooth-Empfang und die eingegebene Adresse prüfen.

## Tasten

| Taste | Bluetooth-Code | Home-Assistant-Ereignis |
|---|---|---|
| Ein | `0101` | `on` |
| Aus | `0201` | `off` |
| Heller | `0801` | `brighter` |
| Dunkler | `0901` | `dimmer` |
| Szene 1 | `1001` | `scene_1` |
| Szene 2 | `1101` | `scene_2` |
| Szene 3 | `1201` | `scene_3` |
| Szene 4 | `1301` | `scene_4` |

## Alle acht Tasten zuweisen – mit dem Blueprint

Im Repository liegt eine wiederverwendbare Automationsvorlage: `blueprints/automation/wiz_ble_dimmer/remote_8_buttons.yaml`.

1. Erstelle vier **Szenen** in Home Assistant. Jede Szene speichert die gewünschten Farben und die Helligkeit deiner Lampen.
2. Importiere den Blueprint über [seine öffentliche GitHub-Datei](https://github.com/janbro2/ha-wiz-ble-smart-dimmer/blob/main/blueprints/automation/wiz_ble_dimmer/remote_8_buttons.yaml) oder kopiere seine YAML-Datei nach `/config/blueprints/automation/wiz_ble_dimmer/`.
3. Erzeuge eine Automation aus dem Blueprint.
4. Wähle die zu steuernden Lampen, die Bluetooth-Adresse, die vier Szenen und deine Standardhelligkeit aus.

Danach funktionieren **Ein / Aus**, **Heller / Dunkler** (standardmäßig ±10 Prozentpunkte) und die **vier Szenentasten**. Jede Szenentaste ruft die Szene mit ihrer gespeicherten Helligkeit ab, sodass eine zuvor gedimmte Lampe wieder auf die Helligkeit der Szene springt.

Szenenideen fürs Bad: **1 Standardlicht**, **2 Guten Morgen** (helles neutrales Weiß), **3 Spa** (sanftes Türkis/Blau), **4 Nachtlicht** (sehr dunkles Warmweiß). Die Helligkeiten bestimmt jede Person selbst.

## Einschränkungen

- Experimentelles, durch Beobachtung ermitteltes Bluetooth-Protokoll; **nicht offiziell von WiZ unterstützt**.
- Ein gleichartiger Tastendruck innerhalb von 350 ms kann bewusst unterdrückt werden, um doppelte Bluetooth-Pakete zu filtern.
- **Gedrückthalten** für kontinuierliches Dimmen wird derzeit nicht unterstützt; jeder Tastendruck ist ein Schritt.
- Home Assistant muss die BLE-Werbepakete empfangen können.
- Die Integration allein schaltet keine Lampen; dafür ist die Automation bzw. der Blueprint zuständig.
- Vor der Installation eigener Integrationen ein Home-Assistant-Backup anlegen.

**Wichtig für Beiträge im Internet:** Keine echten Bluetooth-MAC-Adressen, lokalen IP-Adressen oder persönlichen Gerätedaten veröffentlichen. Logs und Screenshots vor dem Teilen anonymisieren.

Lizenz: MIT. Unabhängiges Community-Projekt, keine Verbindung zu WiZ, Philips oder Signify.
