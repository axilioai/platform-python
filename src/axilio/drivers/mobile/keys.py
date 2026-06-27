"""HID consumer-page key codes (USB HID Usage Tables 1.4, Consumer Page 0x0C)."""


class Key:
    """Common HID consumer-page codes."""

    HOME = 0x0223
    BACK = 0x0224
    MENU = 0x0040
    RECENTS = 0x0301

    POWER = 0x0030

    VOLUME_UP = 0x00E9
    VOLUME_DOWN = 0x00EA
    MUTE = 0x00E2

    PLAY_PAUSE = 0x00CD
    NEXT_TRACK = 0x00B5
    PREV_TRACK = 0x00B6
    STOP = 0x00B7

    SEARCH = 0x0221
    ASSIST = 0x01CB
