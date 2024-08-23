# !pip install langgraph==0.2.4
# !pip install langchain-community==0.2.12
# !pip install langchain-openai==0.1.22
# !pip install langchain-experimental==0.0.64
from langchain_core.tools import tool
from langchain_experimental.utilities import PythonREPL
from typing import Annotated
repl = PythonREPL()
@tool
def python_repl(
    code: Annotated[str, "The python code to execute to generate your chart."],
):
    """Use this to execute python code. If you want to see the output of a \
    value, you should print it out with `print(...)`. This is visible to the \
    user."""
    try:
        result = repl.run(code)
    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
    result_str = f"Successfully executed:\n```python\n{code}\n```\nStdout: \
    {result}"
    return (
        result_str + "\n\nIf you have completed all tasks, respond with FINAL \
        ANSWER."
    )