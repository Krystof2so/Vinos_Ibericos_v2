from dataclasses import dataclass


@dataclass(frozen=True)
class ConfigUI:
    # Titres, tailles, Polices
    DEFAULT_TITLE: str = "Détails vignoble"
    DETAIL_WIN_SIZE: tuple[int, int] = (650, 680)
    DETAIL_IMG_SIZE: tuple[int, int] = (600, 320)
    FONT_FAMILY: str = "Segoe UI, sans-serif"
    FONT_SIZE: int = 12


@dataclass(frozen=True)
class Colors:
    """Palette de couleurs."""

    PRIMARY_MAIN = (
        "#a90a2e"  # Boutons principaux, titres, éléments clés (Rouge bordeaux)
    )
    PRIMARY_ACCENT = "#e07d00"  # Accent / hover / notification (Orange)
    BACKGROUND_LIGHT = "#e6d4c3"  # Fond principal (Beige clair type parchemin)
    BACKGROUND_DARK = (
        "#4b4a5b"  # Fond alternatif (Bleu violet : mode sombre ou encadrés)
    )
    BACKGROUND_DARK_2 = "#5c5b70"
    TEXT_PRIMARY = "#5a0000"  # Texte principal (Noir raisin)
    TEXT_SECONDARY = "#BFA18F"  # Texte secondaire / descriptif (Beige doux)
    BORDER_COLOR = "#dadada"  # Bordures et séparateurs (Gris clair)
    HIGHLIGHT = "#c83768"  # Liens / accents visuels (Rose raisin)
    WARNING = "#e0cc02"  # Avertissements, surbrillance ponctuelle (Vert/Jaune)
