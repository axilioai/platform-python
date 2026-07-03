"""Named keys for MobileDriver.key_press.

Deliberately tiny (AXI-1145): the earlier consumer-page HID constants
(HOME, volume, media keys, ...) were speculative and are gone for now.
Grow this list entry by entry, in lockstep with the named-key table on
the device side, as real needs appear.
"""


class Key:
    """Keys `driver.key_press` can press."""

    # Submits forms / fires the on-screen keyboard's Go / Search action.
    ENTER = "enter"
