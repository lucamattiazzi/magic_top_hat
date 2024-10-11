import inspect
import sys


def get_call_args(tb):
    frame = tb.tb_frame
    code = frame.f_code
    local_vars = frame.f_locals
    arg_names = code.co_varnames[: code.co_argcount]
    args = {name: local_vars.get(name, "<not found>") for name in arg_names}
    return args


def is_call_attempt(tb):
    try:
        frame = tb.tb_frame
        code = frame.f_code
        return code.co_name != "<module>" and (
            (code.co_name == "<lambda>" and code.co_filename == "<string>")
            or any(opname.startswith("CALL_") for opname in code.co_names)
        )
    except Exception:
        return False


def global_non_existent_call_handler(exctype, value, tb):
    if exctype in (AttributeError, NameError) and is_call_attempt(tb):
        args = get_call_args(tb)
        function_name = tb.tb_frame.f_code.co_name
        print(f"Attempted to call non-existent function or method: {function_name}")
        print(f"Arguments passed: {args}")
        print(f"Error message: {value}")
        # You can add more custom handling here if needed
    else:
        # For all other exceptions, use the default exception handling
        sys.__excepthook__(exctype, value, tb)


# Set the global exception handler
sys.excepthook = global_non_existent_call_handler

# Example usage


def existing_function(a, b, c=3):
    non_existent_function(a, b, c)


# This will be caught by our handler
existing_function(1, 2, c=4)


# This will also be caught, demonstrating method call
class TestClass:
    def __init__(self, x):
        self.x = x

    def test_method(self, y):
        self.non_existent_method(self.x, y)


test = TestClass(5)
test.test_method(10)

# This will NOT be caught by our handler (not a call)
print(non_existent_variable)
