# NOTE: simple layers go on top!

from collections.abc import Callable
from typing import Any

import punq


def _global_namespace() -> dict[str, Any]:
    # ruff: ignore[import-outside-top-level, unused-import]
    from django.conf import LazySettings

    # ruff: ignore[import-outside-top-level, unused-import]
    from django.core.cache import BaseCache

    return locals()


def _create_injector[Thing](
    container: punq.Container,
    localns: dict[str, Any],
) -> Callable[[Thing], Thing]:
    # We need to provide the same string names as we do in the definition.
    localns.pop('container')
    localns.update(_global_namespace())
    # pyrefly: ignore [missing-attribute]
    container.registrations._localns.update(localns)  # ruff: ignore[private-member-access]
    return lambda service: service


def _inject_django(container: punq.Container) -> None:
    # ruff: ignore[import-outside-top-level]
    from django.conf import LazySettings, settings

    # Django:
    container.register(
        LazySettings,
        instance=settings,
        scope=punq.Scope.singleton,
    )


def _inject_main(container: punq.Container) -> None:

    # Hacks to resolve annotations:
    inject = _create_injector(container, locals())

    # Things to register:


def populate_dependencies(container: punq.Container) -> punq.Container:
    """Populates dependencies for the container."""
    # Deps:
    _inject_django(container)
    # Apps:
    _inject_main(container)
    return container
