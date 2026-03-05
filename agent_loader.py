# agent_loader.py
import importlib.util
import os

AGENT_DIR = "./agents"

def load_agents():
    agents = []
    for file in os.listdir(AGENT_DIR):
        if file.endswith(".py"):
            spec = importlib.util.spec_from_file_location(file[:-3], os.path.join(AGENT_DIR, file))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            agents.append(module.Agent())  # Each agent defines an Agent class
    return agents
