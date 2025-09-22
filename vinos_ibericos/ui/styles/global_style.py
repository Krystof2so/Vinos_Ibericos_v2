#######################################################
# ui/styles/global_style.py                           #
#                                                     #
# - Fichier qui centralise le style général de l'UI   #
#   (fenêtres, boutons, textes, zones scrollables...) #
# - Fichier importé par les composants                #
#######################################################

from vinos_ibericos.ui.config_ui import ConfigUI


class GlobalStyle:
    @staticmethod
    def get_base_style() -> str:
        """Style global appliqué à toute l'application"""
        return f"""
        QWidget {{
            background-color: {ConfigUI.COLOR_NEUTRAL};
            color: {ConfigUI.COLOR_DARK};
            font-family: {ConfigUI.FONT_FAMILY};
            font-size: {ConfigUI.FONT_SIZE}pt;
        }}
        QPushButton {{
            background-color: {ConfigUI.COLOR_PRIMARY};
            color: #F5E1D0;
            border: none;
            padding: 6px 14px;
            border: 2px solid {ConfigUI.PARCHMENT};
            border-radius: 8px;
            font-size: 20px;
        }}
        QPushButton:hover {{
            background-color: {ConfigUI.COLOR_SECONDARY};
        }}
        QScrollBar:vertical {{
            background: {ConfigUI.COLOR_NEUTRAL};
            width: 8px;
            margin: 0px;
            border-radius: 6px;
        }}
        QScrollBar::handle:vertical {{
            background: {ConfigUI.COLOR_ACCENT};
            border-radius: 4px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {ConfigUI.COLOR_PRIMARY};
        }}
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {{
            height: 0px;
            background: none;
        }}
        """

    @staticmethod
    def get_dialog_style() -> str:
        """Style spécifique aux QDialog"""
        return f"""
        QDialog {{
            background-color: {ConfigUI.COLOR_NEUTRAL};
            color: {ConfigUI.COLOR_DARK};
        }}
        """

    @staticmethod
    def get_text_browser_style() -> str:
        """Style pour les QTextBrowser"""
        return f"""
        QTextBrowser {{
            color: {ConfigUI.COLOR_DARK};
            background: {ConfigUI.PARCHMENT};
            border: 1px solid {ConfigUI.COLOR_SECONDARY};
            border-radius: 8px;
            padding: 10px;
            font-family: 'Book Antiqua','Garamond', 'Georgia', serif;
            font-size: 18px;
            line-height: 1.4em;   /* espacement entre lignes */
        }}
        """

    @staticmethod
    def get_button_selected_style() -> str:
        """Style des boutons sélectionnés (harmonisé au thème)"""
        return f"""
        QPushButton {{
            background-color: {ConfigUI.COLOR_ACCENT};          /* gris bleuté doux */
            border: 3px solid {ConfigUI.COLOR_PRIMARY};         /* rappel bordeaux vin */
            border-radius: 10px;
            color: {ConfigUI.COLOR_DARK};
        }}
        QPushButton:hover {{
            background-color: {ConfigUI.COLOR_SECONDARY};       /* brun chaud au survol */
            color: white;
        }}
        """

    @staticmethod
    def widget_border() -> str:
        return f"""
        QFrame {{
            border: 2px solid {ConfigUI.COLOR_DARK}; /* bordure brun foncé */
        }}
        """
