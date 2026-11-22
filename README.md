# WiZ BLE Smart Dimmer → Home Assistant (unofficial) 🔘

**Use the newer 8-button WiZ Bluetooth Smart Dimmer directly in Home Assistant, without a WiZ bulb or bridge.** This experimental local integration decodes Bluetooth advertising packets and fires `wiz_dimmer_button` events. A companion automation blueprint can control **any** Home Assistant lights and four user-selected scenes (Govee, Hue, Matter, Zigbee, etc.).

> **Community proof of concept.** Verified with one 2026-model 8-button dimmer and Home Assistant Core 2026.11.2 using a Broadcom Bluetooth adapter. The packet layout may vary with model, firmware or region. **This is not the older WiZmote** and is not an official integration, nor affiliated with WiZ or Signify. Please report other successful/unsuccessful models with anonymized packet details.

## What works

| Button | Bluetooth code | Event `action` | Blueprint behavior |
|---|---|---|---|
| On | `0101` | `on` | Turn on light(s) at configured brightness |
| Off | `0201` | `off` | Turn off light(s) |
| Brighter | `0801` | `brighter` | Brightness +N percentage points |
| Dimmer | `0901` | `dimmer` | Brightness −N percentage points |
| Scene 1 | `1001` | `scene_1` | Activate Home Assistant scene 1 |
| Scene 2 | `1101` | `scene_2` | Activate Home Assistant scene 2 |
| Scene 3 | `1201` | `scene_3` | Activate Home Assistant scene 3 |
| Scene 4 | `1301` | `scene_4` | Activate Home Assistant scene 4 |

All eight buttons have been observed and tested on one device. No BLE pairing or cloud connection required. The Home Assistant host (or suitable Bluetooth proxy) must receive the remote's BLE advertisements. Button-held repeating/long-press behavior has **not** been validated.

## Requirements

- Home Assistant Core **2026.11+** (version used for testing), with **Bluetooth integration** and an adapter that hears your remote.
- The **new 8-button WiZ Bluetooth dimmer**, whose advertisement carries manufacturer ID `0x0617` (decimal `1559`).
- For the optional blueprint, at least one `light.*` entity and four Home Assistant `scene.*` entities (they can be created under Settings → Automations & Scenes → Scenes).

## Install the integration

### Using the Home Assistant Marketplace (2026.11+)

1. In Home Assistant, open **Settings → Marketplace → Add from link**.
2. Enter **https://github.com/janbro2/ha-wiz-ble-smart-dimmer** and select **Add**.
3. Open **WiZ BLE Smart Dimmer (Unofficial)** in the Marketplace and install it.
4. If Home Assistant asks for a restart, restart it; then add the integration under **Settings → Devices & services**.

The Marketplace is built into Home Assistant 2026.11+. Earlier installations using the standalone HACS custom-integration manager can add the same repository there.

Alternatively, download the repository and manually copy:

```
custom_components/wiz_ble_dimmer/
```

into:

```
/config/custom_components/wiz_ble_dimmer/
```

Then restart Home Assistant.

**Important:** The companion blueprint is a separate file; installing the integration alone does not install the blueprint.

## Find and add your dimmer

1. Open **Settings → Devices & services → Bluetooth → Advertisement monitor** in Home Assistant. Do **not** click “Add Bluetooth adapter”; that wizard is for installing another radio adapter.
2. Press a button on the dimmer several times while close to the Home Assistant Bluetooth receiver.
3. Find a device with manufacturer ID **1559 / 0x0617**. Confirm that its manufacturer data changes when you press different buttons.
4. Note *your own* Bluetooth address from that entry (e.g. `AA:BB:CC:DD:EE:FF`). Don't copy an address from someone else's guide.
5. **Settings → Devices & services → Add integration → WiZ BLE Smart Dimmer (Unofficial)**. Paste your Bluetooth address; the field has **no hardcoded default MAC**.
6. To verify events, open **Developer tools → Events**, listen for `wiz_dimmer_button`, and press different buttons.

An event resembles:

```yaml
 event_type: wiz_dimmer_button
 data:
   address: "AA:BB:CC:DD:EE:FF"
   action: scene_3
   code: "1201"
   rssi: -63
```

If you see no events, check the advertisement monitor first, try closer proximity, and check the Bluetooth address. The integration does not create a light entity by itself: it only fires events.

## Install the reusable 8-button automation blueprint

Download the [reusable 8-button blueprint](https://github.com/janbro2/ha-wiz-ble-smart-dimmer/blob/main/blueprints/automation/wiz_ble_dimmer/remote_8_buttons.yaml) or copy the file:

```
blueprints/automation/wiz_ble_dimmer/remote_8_buttons.yaml
```

to the same path under your Home Assistant config folder:

```
/config/blueprints/automation/wiz_ble_dimmer/remote_8_buttons.yaml
```

In **Settings → Automations & Scenes → Blueprints**, select **WiZ BLE Smart Dimmer – 8 buttons (unofficial)** and create an automation. Fill in:

- Your dimmer's **Bluetooth address** (UPPERCASE, with colons)
- Light(s) to operate
- Brightness when pressing **On** (default 100%)
- Brightness step per **+ / −** press (default 10 percentage points)
- Four existing `scene.*` entities of your choice

**Scenes restore their saved brightness and colors** when pressed again, even after you've dimmed the lights. The **On** button only sets the configured brightness; it otherwise retains the lamps' current color/color temperature. For a full default look, assign that as Scene 1.

You can use multiple remotes by adding multiple integration entries and blueprint automations with distinct MAC addresses.

## Example bathroom assignment

One installation uses two Govee bathroom ceiling bulbs, but any lights work.

- **Scene 1:** Standard / everyday lighting
- **Scene 2:** Good morning (bright neutral white)
- **Scene 3:** Spa / relaxing bath lighting (dim blue and turquoise)
- **Scene 4:** Night light (very dim warm white)

Save these as four Home Assistant scenes with brightness values; the blueprint recalls them.

## Packet decoder details

Packets from the tested remote use Bluetooth LE *advertising* (not GATT). Manufacturer ID `0x0617` is stripped by Home Assistant before its payload reaches the decoder.

Observed manufacturer payload byte offsets:

```
00:    40
01–06: AA BB CC DD EE FF    ← the remote's own six MAC octets (example)
07–15: device-specific data  ← not interpreted
16–17: 12 01                ← example: Scene 3
18+:   remaining bytes      ← ignored
```

The integration deliberately verifies the **configured** Bluetooth address against both the advertising sender and the payload prefix. It **does not** contain the original tester's hardware address, coordinates, home setup, or secrets. The 350 ms suppression interval filters repeated identical advertisements; rapid repeat presses might need tuning for some devices. Different firmware might encode buttons differently or rotate addresses; please open an issue instead of assuming compatibility.

## Troubleshooting and limitations

- **Bluetooth adapter appears online but no remote shown:** Move the remote closer, press a button while watching the advertisement monitor, and verify the adapter is scanning.
- **Button events arrive but lights don't react:** The integration only fires events. Install/configure the blueprint and check that the target entities are available.
- **Other devices unexpectedly react:** Review other automations listening for `wiz_dimmer_button` and constrain them to your own Bluetooth address.
- **Scene leaves lights at the wrong brightness:** Edit the Home Assistant scene and save the desired brightness; the blueprint activates the scene each time.
- **Repeated rapid presses missed:** The decoder currently suppresses repeated identical codes within 350 ms.
- **Bluetooth privacy:** Bluetooth MAC addresses are device identifiers. **Never include your own address or complete advertising payloads in public issues without anonymizing them.**

## Source, tests and contributions

Run the pure Python protocol tests with:

```bash
python -m unittest discover -s tests -v
```

Source layout:

```
custom_components/wiz_ble_dimmer/       # local Bluetooth event integration
blueprints/automation/wiz_ble_dimmer/    # optional reusable 8-button mapping
tests/                                  # packet decoder unit tests
```

Please contribute hardware revision, firmware, model number (if available) and sanitized manufacturer data to extend support. Test new releases locally before replacing a working installation; community-provided integrations are not reviewed or supported by the Home Assistant project.

License: MIT. See [LICENSE](LICENSE).

---

## Deutsch: Schnellstart 🇩🇪

Mit der **neuen WiZ-Bluetooth-Fernbedienung mit acht Tasten** lassen sich Lampen direkt über Home Assistant bedienen – ohne zusätzliche WiZ-Lampe. Nicht mit der alten WiZmote verwechseln.

1. Über **Einstellungen → Marketplace → Aus Link hinzufügen** das Repository `janbro2/ha-wiz-ble-smart-dimmer` installieren oder `custom_components/wiz_ble_dimmer` nach `/config/custom_components/` kopieren und Home Assistant neu starten.
2. Unter **Bluetooth → Werbepaketmonitor** durch Tastendruck den Dimmer mit Hersteller-ID `1559` finden und **eigene** Bluetooth-Adresse notieren.
3. Unter **Integration hinzufügen → WiZ BLE Smart Dimmer** diese Adresse eintragen.
4. Unter **Entwicklerwerkzeuge → Ereignisse** auf `wiz_dimmer_button` lauschen und Tastencodes überprüfen.
5. Optional die Blueprint-Datei nach `/config/blueprints/automation/wiz_ble_dimmer/` kopieren und eine Automation daraus erstellen. Lampen und vier Szenen frei wählen.

**Hinweis:** Nur mit einem Gerät praktisch erprobt (HA Core 2026.11.2). Das ist ein experimentelles Community-Projekt, keine offizielle WiZ-Unterstützung.
