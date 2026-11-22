"""Protocol constants for the unofficial WiZ BLE Smart Dimmer integration."""

DOMAIN = "wiz_ble_dimmer"
CONF_MAC = "mac"
MANUFACTURER_ID = 0x0617  # 1559, observed on the 2026 WiZ Smart Dimmer
EVENT_NAME = "wiz_dimmer_button"

# The following button codes and offsets were observed on one 2026 8-button
# WiZ Bluetooth Smart Dimmer. Other revisions have not yet been verified.
BUTTONS = {
    "0101": "on",
    "0201": "off",
    "0801": "brighter",
    "0901": "dimmer",
    "1001": "scene_1",
    "1101": "scene_2",
    "1201": "scene_3",
    "1301": "scene_4",
}
