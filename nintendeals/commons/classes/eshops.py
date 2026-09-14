class NAeShop:
    FORMAT = "https://www.nintendo.com/{lang}_{country}/games/detail/{slug}"

    def __init__(self, game: "Game"):
        self.game = game

    @property
    def ca_en(self) -> str:
        return NAeShop.FORMAT.format(lang="en", country="CA", slug=self.game.slug)

    @property
    def ca_fr(self) -> str:
        return NAeShop.FORMAT.format(lang="fr", country="CA", slug=self.game.slug)

    @property
    def us_en(self) -> str:
        return NAeShop.FORMAT.format(lang="en", country="US", slug=self.game.slug)


class EUeShop:
    FORMAT_LOCALE = "https://www.nintendo.com/{locale}{slug}"
    FORMAT_RUSSIA = "https://www.nintendo.ru/-{slug}"

    FORMAT_ALT = "https://ec.nintendo.com/{country}/{lang}/titles/{nsuid}"

    def __init__(self, game: "Game"):
        self.game = game

    @property
    def at_de(self) -> str:
        return EUeShop.FORMAT_LOCALE.format(locale="de-at", slug=self.game.slug)

    @property
    def be_fr(self) -> str:
        return EUeShop.FORMAT_LOCALE.format(locale="fr-be", slug=self.game.slug)

    @property
    def be_nl(self) -> str:
        return EUeShop.FORMAT_LOCALE.format(locale="nl-be", slug=self.game.slug)

    @property
    def ch_de(self) -> str:
        return EUeShop.FORMAT_LOCALE.format(locale="de-ch", slug=self.game.slug)

    @property
    def ch_fr(self) -> str:
        return EUeShop.FORMAT_LOCALE.format(locale="fr-ch", slug=self.game.slug)

    @property
    def ch_it(self) -> str:
        return EUeShop.FORMAT_LOCALE.format(locale="it-ch", slug=self.game.slug)

    @property
    def de_de(self) -> str:
        return EUeShop.FORMAT_LOCALE.format(locale="de-de", slug=self.game.slug)

    @property
    def es_es(self) -> str:
        return EUeShop.FORMAT_LOCALE.format(locale="es-es", slug=self.game.slug)

    @property
    def fr_fr(self) -> str:
        return EUeShop.FORMAT_LOCALE.format(locale="fr-fr", slug=self.game.slug)

    @property
    def it_it(self) -> str:
        return EUeShop.FORMAT_LOCALE.format(locale="it-it", slug=self.game.slug)

    @property
    def nl_nl(self) -> str:
        return EUeShop.FORMAT_LOCALE.format(locale="nl-nl", slug=self.game.slug)

    @property
    def pt_pt(self) -> str:
        return EUeShop.FORMAT_LOCALE.format(locale="pt-pt", slug=self.game.slug)

    @property
    def ru_ru(self) -> str:
        return EUeShop.FORMAT_RUSSIA.format(slug=self.game.slug)

    @property
    def uk_en(self) -> str:
        return EUeShop.FORMAT_LOCALE.format(locale="en-gb", slug=self.game.slug)

    @property
    def za_en(self) -> str:
        return EUeShop.FORMAT_LOCALE.format(locale="en-za", slug=self.game.slug)

    @property
    def au_en(self) -> str:
        return EUeShop.FORMAT_ALT.format(country="AU", lang="en", nsuid=self.game.nsuid)

    @property
    def nz_en(self) -> str:
        return EUeShop.FORMAT_ALT.format(country="NZ", lang="en", nsuid=self.game.nsuid)


class JPeShop:
    NEW_FORMAT = "https://store-jp.nintendo.com/list/software/{nsuid}.html"
    OLD_FORMAT = "https://www.nintendo.co.jp/titles/{nsuid}"

    def __init__(self, game: "Game"):
        self.game = game

    @property
    def jp_jp(self) -> str:
        return JPeShop.NEW_FORMAT.format(nsuid=self.game.nsuid)
