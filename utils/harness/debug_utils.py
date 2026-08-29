import sys


def debug_vars(*var_names):
    def decorator(func):
        def wrapper(*args, **kwargs):
            def trace(frame, event, arg):
                # Only trace within the decorated function's code
                if event == "line" and frame.f_code == func.__code__:
                    locals_dict = frame.f_locals
                    for var in var_names:
                        if var in locals_dict:
                            print(f"In {func.__name__}: {var} = {locals_dict[var]}")
                return trace

            # Save and set the trace function
            old_trace = sys.gettrace()
            sys.settrace(trace)
            try:
                return func(*args, **kwargs)
            finally:
                # Restore original trace
                sys.settrace(old_trace)

        return wrapper

    return decorator


def debug_var(var_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            def trace(frame, event, arg):
                if event == "line" and frame.f_code == func.__code__:
                    if var_name in frame.f_locals:
                        print(
                            f"In {func.__name__}: {var_name} = {frame.f_locals[var_name]}"
                        )
                return trace

            old_trace = sys.gettrace()
            sys.settrace(trace)
            try:
                return func(*args, **kwargs)
            finally:
                # Restore original trace
                sys.settrace(old_trace)

        return wrapper

    return decorator
