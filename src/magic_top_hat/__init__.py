import inspect
import os
import pprint
import traceback
from functools import partial
from importlib.util import module_from_spec, spec_from_file_location

from openai import OpenAI

__all__ = []


def __dir__():
    return __all__


def __getattr__(name):
    if name == "__path__":
        return None
    if name in ["__ask", "__magic"]:
        raise AttributeError("Really?? You named your function that? Come on!")
    return partial(__magic, name)


def __ask(fn_name: str, caller_code: str) -> str:
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a software engineer. You will receive a snippet of code, and must write implement a single function so that the snippet works correctly. The code is Python 3, and your answer must only contain the function body, not the entire program. You can assume the function will be called with valid arguments. The name of the function is provided in the prompt.",
            },
            {
                "role": "user",
                "content": f"You must implement the function called {fn_name} that makes the following snippet work correctly. {caller_code}",
            },
        ],
        model="gpt-3.5-turbo",
    )
    return chat_completion.choices[0].message.content


def __magic(fn_name: str, *args, **kwargs):
    stack = traceback.extract_stack()
    caller = stack[-2]
    spec = spec_from_file_location(caller.name, caller.filename)
    caller = module_from_spec(spec)
    caller_code = inspect.getsource(caller)

    raw_python = __ask(fn_name, caller_code)
    if os.environ.get("I_DONT_TRUST_ROBOTS"):
        pprint.pprint(raw_python)
    fn_definition = (
        raw_python.split("python\n")[1]
        .replace("```", "")
        .replace(fn_name, f"{fn_name}_implementation")
    )
    exec(fn_definition, globals())
    fn = globals()[f"{fn_name}_implementation"]
    return fn(*args, **kwargs)
