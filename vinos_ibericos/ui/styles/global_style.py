#######################################################
# ui/styles/global_style.py                           #
#                                                     #
# - Fichier qui centralise le style général de l'UI   #
#   (fenêtres, boutons, textes, zones scrollables...) #
# - Fichier importé par les composants                #
#######################################################

from vinos_ibericos.ui.config_ui import ConfigUI, Colors


class GlobalStyle:
    @staticmethod
    def get_base_style() -> str:
        """Style global appliqué à toute l'application"""
        return f"""
        QWidget {{
            background-color: {Colors.BACKGROUND_DARK};
            color: {Colors.TEXT_SECONDARY};
            font-family: {ConfigUI.FONT_FAMILY};
            font-size: {ConfigUI.FONT_SIZE}pt;
        }}
        QPushButton {{
            background-color: {Colors.BACKGROUND_DARK_2};
            color: {Colors.BACKGROUND_LIGHT};
            border: none;
            padding: 6px 14px;
            border: 1px solid {Colors.PRIMARY_ACCENT};
            border-radius: 8px;
            font-size: 20px;
        }}
        QPushButton:hover {{
            background-color: {Colors.PRIMARY_MAIN};
            border: 1px solid {Colors.BORDER_COLOR};
        }}
        QScrollBar:vertical {{
            background: {Colors.TEXT_SECONDARY};
            width: 8px;
            margin: 0px;
            border-radius: 6px;
        }}
        QScrollBar::handle:vertical {{
            background: {Colors.PRIMARY_MAIN};
            border-radius: 4px;
        }}
        QScrollBar::handle:hover {{
            background: {Colors.PRIMARY_ACCENT};
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
            background-color: {Colors.BACKGROUND_DARK};
            color: {Colors.BORDER_COLOR};
        }}
        """

    @staticmethod
    def get_text_browser_style() -> str:
        """Style pour les QTextBrowser"""
        return f"""
        QTextBrowser {{
            color: {Colors.BACKGROUND_LIGHT};
            background: {Colors.BACKGROUND_DARK_2};
            border: 1px solid {Colors.BORDER_COLOR};
            border-radius: 8px;
            padding: 10px;
        }}
        """

    @staticmethod
    def get_text_browser_html_css() -> str:
        # CSS ici s'applique au contenu HTML du QTextDocument
        return f"""
        body {{
            font-family: 'Book Antiqua', 'Garamond', 'Georgia', serif;
            font-size: 18px;
            line-height: 1.1;
            color: {Colors.BACKGROUND_LIGHT};
            margin: 0;
            padding: 0;
            background: transparent; /* laisse voir le background du widget */
        }}
        a {{
            color: {Colors.PRIMARY_ACCENT};
            text-decoration: underline;            /* on active le soulignement */
            text-decoration-color: {Colors.PRIMARY_ACCENT};  /* couleur spécifique du soulignement */
        }}
        """

    @staticmethod
    def get_button_selected_style() -> str:
        """Style des boutons sélectionnés (harmonisé au thème)"""
        return f"""
        QPushButton {{
            background-color: {Colors.PRIMARY_MAIN};
            border-radius: 10px;
            color: {Colors.BACKGROUND_LIGHT};
            border: 2px solid {Colors.BORDER_COLOR};
        }}
        QPushButton:hover {{
            background-color: {Colors.BACKGROUND_LIGHT};       /* brun chaud au survol */
            color: {Colors.TEXT_PRIMARY};
        }}
        """

    @staticmethod
    def get_list_widget_style() -> str:
        """Style pour la QListWidget des vignobles."""
        return f"""
        QListWidget {{
            background-color: {Colors.BACKGROUND_DARK_2};
            color: {Colors.BACKGROUND_LIGHT};
            border: 1px solid {Colors.PRIMARY_ACCENT};  /* liséré */
            border-radius: 8px;
            font-size: 16pt;
            font-family: {ConfigUI.FONT_FAMILY};
        }}
        QListWidget::item {{
            padding: 6px 14px;
            border-radius: 6px;
        }}
        QListWidget::item:selected {{
            background-color: {Colors.PRIMARY_MAIN};
            color: {Colors.BACKGROUND_LIGHT};
            border: 1px solid {Colors.BORDER_COLOR};
        }}
        QListWidget::item:hover {{
            background-color: {Colors.PRIMARY_ACCENT};
            color: {Colors.BACKGROUND_LIGHT};
        }}
        QScrollBar:vertical {{
            background: {Colors.TEXT_SECONDARY};
            width: 8px;
            margin: 0px;
            border-radius: 6px;
        }}
        QScrollBar::handle:vertical {{
            background: {Colors.PRIMARY_MAIN};
            border-radius: 4px;
        }}
        QScrollBar::handle:hover {{
            background: {Colors.PRIMARY_ACCENT};
        }}
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {{
            height: 0px;
            background: none;
        }}
        """

    @staticmethod
    def widget_border() -> str:
        return f"""
        QFrame {{
            border: 2px solid {Colors.BORDER_COLOR}; /* bordure brun foncé */
        }}
        """
