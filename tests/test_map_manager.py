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
