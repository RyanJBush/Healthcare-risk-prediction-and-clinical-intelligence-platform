from app.services.model_registry import ModelRegistry, RegisteredModel, build_default_registry


def test_registry_register_and_resolve_round_trip() -> None:
    registry = ModelRegistry()
    model = RegisteredModel(
        name="Custom Risk Model",
        version="v2",
        target_type="readmission",
        family="gradient_boosting",
        description="custom model",
    )

    registry.register(model)

    resolved = registry.resolve("readmission", "v2")
    assert resolved == model


def test_registry_resolve_returns_none_for_unknown_key() -> None:
    registry = ModelRegistry()
    assert registry.resolve("readmission", "missing") is None


def test_registry_register_overwrites_same_target_version() -> None:
    registry = ModelRegistry()
    first = RegisteredModel(
        name="Old",
        version="tiered-v1",
        target_type="readmission",
        family="family_a",
        description="old",
    )
    second = RegisteredModel(
        name="New",
        version="tiered-v1",
        target_type="readmission",
        family="family_b",
        description="new",
    )

    registry.register(first)
    registry.register(second)

    assert registry.resolve("readmission", "tiered-v1") == second
    assert len(registry.list_all()) == 1


def test_registry_list_all_is_sorted_by_target_then_version() -> None:
    registry = ModelRegistry()
    registry.register(
        RegisteredModel(
            name="B", version="v2", target_type="readmission", family="f", description=""
        )
    )
    registry.register(
        RegisteredModel(
            name="A", version="v1", target_type="adverse_event", family="f", description=""
        )
    )
    registry.register(
        RegisteredModel(
            name="C", version="v1", target_type="readmission", family="f", description=""
        )
    )

    ordered = registry.list_all()
    assert [(m.target_type, m.version) for m in ordered] == [
        ("adverse_event", "v1"),
        ("readmission", "v1"),
        ("readmission", "v2"),
    ]


def test_build_default_registry_registers_all_default_targets() -> None:
    registry = build_default_registry()

    for target in ("readmission", "deterioration", "adverse_event"):
        resolved = registry.resolve(target, "tiered-v1")
        assert resolved is not None
        assert resolved.name == "Tiered Clinical Risk Engine"
        assert resolved.family == "rule_calibrated_logit"
        assert target in resolved.description

    assert len(registry.list_all()) == 3
