from src.main import main


def test_project_initialization() -> None:
    assert main() == "Essay Generation project initialized"
