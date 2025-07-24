"""Package initialization for :mod:`evo_ai`."""

import logging

try:
    from labs.adk.agent_loader import AgentLoader
except Exception:  # pragma: no cover - optional dependency
    AgentLoader = None
    logging.getLogger(__name__).warning(
        "labs-adk not available; AgentLoader functionality disabled"
    )

from . import fake_data, function_tools

__all__ = ["fake_data", "function_tools"]

root_agent = AgentLoader(__name__) if AgentLoader else None
