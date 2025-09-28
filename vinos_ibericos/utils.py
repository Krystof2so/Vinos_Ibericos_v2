# vinos_ibericos/utils.py
from contextlib import contextmanager
from PySide6.QtCore import QObject


@contextmanager
def suspend_signals(widget: QObject):
    """Contexte pour bloquer temporairement les signaux d'un widget Qt."""
    widget.blockSignals(True)
    try:
        yield
    finally:
        widget.blockSignals(False)
