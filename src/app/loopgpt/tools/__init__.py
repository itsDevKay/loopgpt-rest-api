from app.loopgpt.tools.agent_manager import (
    CreateAgent,
    MessageAgent,
    DeleteAgent,
    ListAgents,
)
from app.loopgpt.tools.base_tool import BaseTool
from app.loopgpt.tools.browser import Browser
from app.loopgpt.tools.code import ExecutePythonFile, EvaluateCode, ImproveCode, WriteTests
from app.loopgpt.tools.google_search import GoogleSearch
from app.loopgpt.tools.filesystem import (
    ReadFromFile,
    WriteToFile,
    AppendToFile,
    DeleteFile,
    CheckIfFileExists,
    ListFiles,
    FileSystemTools,
)
from app.loopgpt.tools.shell import Shell
from app.loopgpt.tools.memory_manager import AddToMemory


user_tools = {}


def register_tool_type(tool):
    if isinstance(tool, BaseTool):
        tool = tool.__class__
    if not isinstance(tool, type):
        raise TypeError(f"{tool} is not a class")
    if not issubclass(tool, BaseTool):
        raise TypeError(f"{tool} does not inherit from BaseTool")
    user_tools[tool.__name__] = tool


def from_config(config) -> BaseTool:
    class_name = config["class"]
    clss = user_tools.get(class_name) or globals()[class_name]
    return clss.from_config(config)


def builtin_tools():
    return [
        GoogleSearch,
        Browser,
        CreateAgent,
        MessageAgent,
        ListAgents,
        DeleteAgent,
        *FileSystemTools,
        EvaluateCode,
        ImproveCode,
        WriteTests,
        ExecutePythonFile,
    ]
