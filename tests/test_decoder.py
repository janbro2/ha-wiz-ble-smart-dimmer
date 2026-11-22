"""Pure Python protocol tests without installing Home Assistant."""

import importlib.util
from pathlib import Path
import sys
import types
import unittest

INTEGRATION_DIR = Path(__file__).resolve().parents[1] / "custom_components" / "wiz_ble_dimmer"
PACKAGE = "wiz_ble_dimmer_test_package"
pkg = types.ModuleType(PACKAGE)
pkg.__path__ = [str(INTEGRATION_DIR)]
sys.modules[PACKAGE] = pkg


def load_module(name: str):
    spec = importlib.util.spec_from_file_location(f"{PACKAGE}.{name}", INTEGRATION_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


const = load_module("const")
decoder = load_module("decoder")
REMOTE = "AA:BB:CC:DD:EE:FF"  # synthetic example, not a real device


def packet(code: str, address: str = REMOTE) -> bytes:
    return (
        b"\x40"
        + bytes.fromhex(address.replace(":", ""))
        + bytes.fromhex("01 01 00 81 6A 00 00 00 20")
        + bytes.fromhex(code)
        + b"\x00\x00"
    )


class TestDecoder(unittest.TestCase):
    def test_all_eight_buttons(self):
        for code, action in const.BUTTONS.items():
            with self.subTest(code=code):
                self.assertEqual(decoder.decode_button(packet(code), REMOTE), (action, code))

    def test_mismatched_remote_rejected(self):
        self.assertIsNone(decoder.decode_button(packet("0101"), "11:22:33:44:55:66"))

    def test_short_packet_rejected(self):
        self.assertIsNone(decoder.decode_button(packet("0101")[:17], REMOTE))

    def test_unknown_button_rejected(self):
        self.assertIsNone(decoder.decode_button(packet("FF01"), REMOTE))

    def test_invalid_address_rejected(self):
        self.assertIsNone(decoder.decode_button(packet("0101"), "not-a-mac"))


if __name__ == "__main__":
    unittest.main()
