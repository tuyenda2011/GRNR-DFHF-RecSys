"""Current model names with read access to unchanged historical result folders."""
from pathlib import Path

MODEL_ALIASES = {"sgkr": "grnr", "sphr": "dfhf"}
LEGACY_NAMES = {current: previous for previous, current in MODEL_ALIASES.items()}


def canonical_model_name(name):
    return MODEL_ALIASES.get(name, name)


def model_result_roots(results, model):
    """Current results first, then the historical folder when it exists."""
    model = canonical_model_name(model)
    roots = [Path(results) / model]
    if model in LEGACY_NAMES:
        roots.append(Path(results) / LEGACY_NAMES[model])
    return roots


def resolve_model_run(results, model, density, seed):
    """Read an existing run in either layout; use the current name for a fresh run."""
    suffix = Path(f"d{round(density * 100)}") / f"seed{seed}"
    candidates = [root / suffix for root in model_result_roots(results, model)]
    for candidate in candidates:
        if (candidate / "metrics.json").is_file():
            return candidate
    return next((candidate for candidate in candidates if candidate.is_dir()), candidates[0])


def iter_model_metrics(results, model):
    """Discover both layouts once per density/seed; prefer a completed current run."""
    seen = set()
    for root in model_result_roots(results, model):
        for path in sorted(root.glob("d*/seed*/metrics.json")):
            identity = path.parent.relative_to(root)
            if identity not in seen:
                seen.add(identity)
                yield path
