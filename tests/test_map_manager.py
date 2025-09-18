# tests/test_map_manager.py
import pytest

from vinos_ibericos.map_manager import MapManager


@pytest.fixture
def sample_manager():
    """Fixture qui prépare un MapManager avec deux vignobles."""
    vineyards = [
        {
            "nom": "Vinedo Uno",
            "coords": [40.0, -3.3],
            "description": "Premier vignoble test",
        },
        {
            "nom": "Vinedo Dos",
            "coords": [41.0, -3.7],
            "description": "Deuxième vignoble test",
        },
    ]
    return MapManager(vineyards), vineyards


def _assert_all_vineyards_in_html(manager, vineyards, filter_value=None):
    """Test commun avec HTML contenant tous les vignobles."""
    html_content = manager.generate_map_html(vinedo_filter=filter_value)
    assert isinstance(html_content, str)
    assert html_content.strip() != ""
    for v in vineyards:
        assert v["nom"] in html_content


def test_generate_map_html_global_view(sample_manager):
    """Sans filtre → le HTML doit contenir tous les vignobles."""
    manager, vineyards = sample_manager
    _assert_all_vineyards_in_html(manager, vineyards)


def test_generate_map_html_with_nonexistent_filter(sample_manager):
    """Avec un filtre inexistant → doit retomber sur la vue globale."""
    manager, vineyards = sample_manager
    _assert_all_vineyards_in_html(manager, vineyards, filter_value="Inexistant")


def test_generate_map_html_with_existing_filter(sample_manager):
    """Avec un filtre valide → le HTML doit contenir uniquement ce vignoble."""
    manager, _ = sample_manager
    html_content = manager.generate_map_html(vinedo_filter="Vinedo Uno")
    assert isinstance(html_content, str)
    assert "Vinedo Uno" in html_content
    assert "Vinedo Dos" not in html_content  # l'autre ne doit pas apparaître
    print("✅ Tests pour 'generate_map_html'")


def test_format_tooltip_and_popup_returns_correct_html(sample_manager):
    """
    Teste que les méthodes _format_tooltip et _format_popup renvoient bien une chaîne HTML
    - contenant le nom du vignoble passé en paramètre pour le tooltip,
    - contenant le nom du vignoble et la description pour le popup.
    """
    manager, vineyards = sample_manager
    html_output_tooltip = manager._format_tooltip(vineyards[0]["nom"])
    html_output_popup = manager._format_popup(vineyards[1])
    assert isinstance(html_output_tooltip, str)  # Type string attendu
    assert "Vinedo Uno" in html_output_tooltip  # Nom du vignoble présent dans le HTML
    assert isinstance(html_output_popup, str)
    assert "Vinedo Dos" in html_output_popup
    assert "Deuxième vignoble test" in html_output_popup
    print("✅ Tests pour '_format_tooltip' et '_format_popup'")
