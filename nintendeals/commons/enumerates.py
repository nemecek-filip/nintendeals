from enum import Enum


class Features(str, Enum):
    AMIIBO = "Amiibo Supported"
    DEMO = "Demo Available"
    DLC = "DLC Available"
    GAME_VOUCHER = "Game Voucher Eligible"
    ONLINE_PLAY = "Online Play"
    SAVE_DATA_CLOUD = "Save Data Cloud Supported"
    VOICE_CHAT = "Voice Chat Supported"

    def __str__(self):
        return str(self.value)


class Platforms(str, Enum):
    NINTENDO_SWITCH = "Nintendo Switch"
    NINTENDO_SWITCH_2 = "Nintendo Switch 2"

    def __str__(self):
        return str(self.value)


class Ratings(str, Enum):
    CERO = "CERO"  # JP
    ESRB = "ESRB"  # NA
    PEGI = "PEGI"  # EU

    def __str__(self):
        return str(self.value)


class Regions(str, Enum):
    NA = "NA"
    EU = "EU"
    JP = "JP"

    def __str__(self):
        return str(self.value)
