import os
from loopgpt import Agent
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

a = Agent()
a.name = os.environ.get('agent_name')
a.description = os.environ.get('agent_description')
# /; delmiter used to avoid splitting by `,` in case a user types a comma
a.goals = os.environ.get('agent_goals').split('/;')[:-1]
a.cli_socket(continuous=bool(os.environ.get('agent_continuous')))