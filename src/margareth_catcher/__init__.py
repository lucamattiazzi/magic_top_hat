import inspect
import os
import traceback
from functools import partial
from importlib.util import module_from_spec, spec_from_file_location
from random import choice

__all__ = []


def __dir__():
    return __all__


def __getattr__(name):
    if name == "__path__":
        return None
    if name.startswith("__"):
        raise AttributeError("Please don't import dunder methods!")
    return partial(__magic, name)


def __get_messages(fn_name: str, caller_code: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": """
                You are a software engineer.
                You will receive a snippet of code, and must write implement a single function so that the snippet works correctly.
                Use the context provided in the snippet to guide your implementation.
                The code is Python 3, and your answer must only contain the function body, not the entire program.
                You can assume the function will be called with valid arguments.
                If the function you implement is too complex, you can import helper functions from the library `magic_top_hat`, but you must use expressive function names and arguments.
                The name of the function is provided in the prompt.
            """,
        },
        {
            "role": "user",
            "content": f"You must implement the function called {fn_name} that makes the following snippet work correctly. {caller_code}",
        },
    ]


def __ask_ollama(fn_name: str, caller_code: str) -> str:
    import ollama

    response = ollama.chat(
        model="codegemma", messages=__get_messages(fn_name, caller_code)
    )
    breakpoint()
    return response["message"]["content"]


def __ask_openai(fn_name: str, caller_code: str) -> str:
    from openai import OpenAI

    client = OpenAI()
    chat_completion = client.chat.completions.create(
        messages=__get_messages(fn_name, caller_code),
        model="gpt-4o-mini",
    )
    return chat_completion.choices[0].message.content


def __ask_claude(fn_name: str, caller_code: str) -> str:
    from anthropic import Anthropic

    client = Anthropic()
    chat_completion = client.messages.create(
        messages=__get_messages(fn_name, caller_code),
        model="claude-3-5-sonnet-20240620",
    )
    return chat_completion.choices[0].message.content


def __ask(fn_name: str, caller_code: str) -> str:
    openai_available = os.getenv("OPENAI_API_KEY") is not None
    anthropic_available = os.getenv("ANTHROPIC_API_KEY") is not None

    if True:
        return __ask_ollama(fn_name, caller_code)
    if openai_available and not anthropic_available:
        return __ask_openai(fn_name, caller_code)
    if anthropic_available and not openai_available:
        return __ask_claude(fn_name, caller_code)

    return choice([__ask_claude, __ask_openai, __ask_ollama])(fn_name, caller_code)


def __magic(fn_name: str, *args, **kwargs):
    stack = traceback.extract_stack()
    caller = stack[-2]
    spec = spec_from_file_location(caller.name, caller.filename)
    caller = module_from_spec(spec)
    caller_code = inspect.getsource(caller)

    raw_python = __ask(fn_name, caller_code)
    fn_definition = (
        raw_python.replace("```python", "")
        .replace("```", "")
        .replace(fn_name, f"{fn_name}_implementation")
    )
    if os.environ.get("I_DONT_TRUST_ROBOTS"):
        print(fn_definition)
    breakpoint()
    exec(fn_definition, globals())
    fn = globals()[f"{fn_name}_implementation"]
    return fn(*args, **kwargs)
