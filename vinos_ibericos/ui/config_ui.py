from dataclasses import dataclass


@dataclass(frozen=True)
class ConfigUI:
    # Titres & tailles
    DEFAULT_TITLE: str = "Détails vignoble"
    DETAIL_WIN_SIZE: tuple[int, int] = (650, 680)
    DETAIL_IMG_SIZE: tuple[int, int] = (600, 320)

    # Palette de couleurs
    COLOR_PRIMARY: str = "#590212"  # Bordeaux vin
    COLOR_SECONDARY: str = "#8C6B58"  # Brun chaud
    COLOR_NEUTRAL: str = "#BFA18F"  # Beige doux
    COLOR_ACCENT: str = "#8A9BA6"  # Gris bleuté
    COLOR_DARK: str = "#261D15"  # Brun foncé

    # Couleurs additionnelles
    PARCHMENT: str = "#E8D9CC"  # Beige clair type parchemin

    # Police par défaut
    FONT_FAMILY: str = "Segoe UI, sans-serif"
    FONT_SIZE: int = 12
