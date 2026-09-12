"""Named keys for MobileDriver.key_press.

Deliberately tiny (AXI-1145): the earlier consumer-page HID constants
(HOME, volume, media keys, ...) were speculative and are gone for now.
Grow this list entry by entry, in lockstep with the named-key table on
the device side, as real needs appear. The contract enumerates the deployed
names (`KeyboardKeyPressParams.key`, generated as `_wire.Key`);
`tests/test_keys.py` fails when this class and that enum disagree, so a key
the phone learns cannot stay a raw string here.
"""


class Key:
    """Keys `driver.key_press` can press."""

    # Submits forms / fires the on-screen keyboard's Go / Search action.
    ENTER = "enter"
    # Toggles the on-screen keyboard's caps lock.
    CAPSLOCK = "capslock"
