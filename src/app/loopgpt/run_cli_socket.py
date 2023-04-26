from loopgpt import Agent
import os

a = Agent()
a.name = os.environ.get('agent_name')
a.description = os.environ.get('agent_description')
# /; delmiter used to avoid splitting by `,` in case a user types a comma
a.goals = os.environ.get('agent_goals').split('/;')[:-1]
a.cli_socket(continuous=bool(os.environ.get('agent_continuous')))
