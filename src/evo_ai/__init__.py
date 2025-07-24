from labs.adk.agent_loader import AgentLoader

from . import fake_data, function_tools

__all__ = ["fake_data", "function_tools"]

root_agent = AgentLoader(__name__)
