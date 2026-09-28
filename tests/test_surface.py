from pathlib import Path

ROOT = Path(__file__).parents[1]
SOURCE = (ROOT / "contracts" / "contract.py").read_text(encoding="utf-8")

def test_contract_surface_and_runner():
    assert SOURCE.startswith('# { "Depends": "py-genlayer:')
    for method in ("open_exercise", "dispatch_move", "seal_exercise", "get_exercise", "get_moves_page", "get_exercises_page"):
        assert f"def {method}" in SOURCE
    assert "run_nondet_unsafe" in SOURCE
    assert "emit_transfer" not in SOURCE

def test_required_design_documents_exist():
    for name in ("PRODUCT_BOUNDARY.md", "frontend-design-contract.md", "readme-design-contract.md", "README.md", "VERIFICATION.md"):
        assert (ROOT / name).exists()
