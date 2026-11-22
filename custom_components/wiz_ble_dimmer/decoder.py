"""Decode observed WiZ Bluetooth Smart Dimmer manufacturer payloads.

This is an independent, experimentally reverse-engineered decoder and is not
associated with Signify/WiZ. No Bluetooth connection or pairing is needed.
"""

from .const import BUTTONS


def decode_button(data: bytes, address: str) -> tuple[str, str] | None:
    """Return (action, hex code) for a recognized advertisement.

    Observed packet layout (manufacturer ID is not part of ``data``):
    byte 0      0x40
    bytes 1..6  six MAC address octets, normal left-to-right display order
    bytes 7..15 device-specific payload
    bytes 16..17 button code

    The prefix is derived from *the user's configured remote MAC*, never
    hardcoded to the original tester's private device address.
    """
    if len(data) < 18:
        return None
    try:
        prefix = b"\x40" + bytes.fromhex(address.replace(":", ""))
    except ValueError:
        return None
    if len(prefix) != 7 or not data.startswith(prefix):
        return None
    code = data[16:18].hex().upper()
    action = BUTTONS.get(code)
    return (action, code) if action is not None else None
