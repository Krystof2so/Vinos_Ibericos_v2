# tests/test_vinedo_button.py
import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPixmap

from vinos_ibericos.vinedo_button import VinedoButton

BTN_MAX_CHARS: int = 11
COURT_NAME: str = "Nom court"
FAKE_IMG: str = "fake_path.png"
LONG_NAME: str = "X" * (BTN_MAX_CHARS + 5)


# QApplication doit exister pour tester les widgets
@pytest.fixture(scope="session", autouse=True)
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_split_text_short_text():
    """_split_text ne modifie pas un texte plus court que BTN_MAX_CHARS"""
    assert VinedoButton(COURT_NAME, FAKE_IMG)._split_text(COURT_NAME) == COURT_NAME


def test_split_text_long_text():
    """_split_text coupe correctement un texte trop long"""
    result = VinedoButton(LONG_NAME, FAKE_IMG)._split_text(LONG_NAME)
    assert "\n" in result  # le texte est bien coupé en deux lignes
    assert len(result.replace("\n", "")) == BTN_MAX_CHARS + 5


def test_get_pixmap_with_valid_image(tmp_path):
    """get_pixmap retourne un QPixmap valide si l’image existe"""
    # Crée une petite image temporaire :
    img_path = tmp_path / FAKE_IMG
    QPixmap(10, 10).save(str(img_path))
    result = VinedoButton(COURT_NAME, str(img_path)).get_pixmap()
    assert isinstance(result, QPixmap)
    assert not result.isNull()


def test_get_pixmap_with_invalid_image():
    """get_pixmap retourne un pixmap non nul même si le chemin est invalide (fallback image par défaut)"""
    result = VinedoButton(COURT_NAME, FAKE_IMG).get_pixmap()
    assert isinstance(result, QPixmap)
    assert not result.isNull()  # fallback a fonctionné
