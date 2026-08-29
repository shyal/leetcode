from rich import print

import sys


def viz_binary_search(width=100):
    def decorator(func):
        def wrapper(*args, **kwargs):
            prev_state = None
            initial_min = None
            initial_max = None
            bound1_var = None
            bound2_var = None
            mid_var = None

            def trace(frame, event, arg):
                nonlocal prev_state, initial_min, initial_max, bound1_var, bound2_var, mid_var
                if event == "line" and frame.f_code == func.__code__:
                    locals_dict = frame.f_locals
                    if bound1_var is None:
                        if (
                            "left" in locals_dict
                            and "right" in locals_dict
                            and "mid" in locals_dict
                        ):
                            bound1_var = "left"
                            bound2_var = "right"
                            mid_var = "mid"
                        elif (
                            "low" in locals_dict
                            and "high" in locals_dict
                            and "mid" in locals_dict
                        ):
                            bound1_var = "low"
                            bound2_var = "high"
                            mid_var = "mid"
                    if bound1_var is not None:
                        bound1 = locals_dict[bound1_var]
                        bound2 = locals_dict[bound2_var]
                        m = locals_dict[mid_var]
                        lower = min(bound1, bound2)
                        upper = max(bound1, bound2)
                        if abs(m - (bound1 + bound2) / 2) <= 0.5:
                            current_state = (lower, upper, m)
                            if current_state != prev_state:
                                if initial_min is None:
                                    initial_min = lower
                                    initial_max = upper
                                    delta = (
                                        initial_max - initial_min
                                        if initial_min is not None
                                        else 0
                                    )
                                    number_line = [" "] * width
                                    if delta > 0:
                                        is_int_bounds = isinstance(
                                            initial_min, int
                                        ) and isinstance(initial_max, int)
                                        if is_int_bounds and delta <= 20:
                                            for num in range(
                                                initial_min, initial_max + 1
                                            ):
                                                str_num = str(num)
                                                pos = int(
                                                    ((num - initial_min) / delta)
                                                    * (width - 1)
                                                )
                                                for i in range(len(str_num)):
                                                    if pos + i < width:
                                                        number_line[pos + i] = str_num[
                                                            i
                                                        ]
                                        else:
                                            max_ticks = min(width // 10, 11)
                                            for i in range(max_ticks):
                                                frac = (
                                                    i / (max_ticks - 1)
                                                    if max_ticks > 1
                                                    else 0
                                                )
                                                if is_int_bounds:
                                                    num = initial_min + round(
                                                        frac * delta
                                                    )
                                                    str_num = str(int(num))
                                                else:
                                                    num = initial_min + frac * delta
                                                    str_num = (
                                                        f"{num:.2f}"
                                                        if isinstance(num, float)
                                                        else str(num)
                                                    )
                                                pos = int(frac * (width - 1))
                                                for j in range(len(str_num)):
                                                    if pos + j < width:
                                                        number_line[pos + j] = str_num[
                                                            j
                                                        ]
                                    else:
                                        str_num = str(initial_min)
                                        pos = width // 2 - len(str_num) // 2
                                        for i in range(len(str_num)):
                                            number_line[pos + i] = str_num[i]
                                    print("".join(number_line))
                                delta = (
                                    initial_max - initial_min
                                    if initial_min is not None
                                    else 0
                                )
                                if delta > 0:
                                    pos_l = int(
                                        ((lower - initial_min) / delta) * (width - 1)
                                    )
                                    pos_m = int(
                                        ((m - initial_min) / delta) * (width - 1)
                                    )
                                    pos_r = int(
                                        ((upper - initial_min) / delta) * (width - 1)
                                    )
                                else:
                                    pos_l = pos_m = pos_r = width // 2
                                line = ["-"] * width
                                if pos_l == pos_r:
                                    line[pos_l] = "X"
                                else:
                                    line[pos_l] = "L"
                                    line[pos_r] = "R"
                                line_str = "".join(line)
                                line_str = (
                                    line_str.replace("L", "[green]L[/green]")
                                    .replace("R", "[red]R[/red]")
                                    .replace("X", "[magenta]X[/magenta]")
                                )
                                print(line_str)
                                pointer_line = [" "] * width
                                pointer_line[pos_m] = "M"
                                pointer_str = "".join(pointer_line)
                                pointer_str = pointer_str.replace(
                                    "M", "[yellow]M[/yellow]"
                                )
                                print(pointer_str)
                                prev_state = current_state
                return trace

            old_trace = sys.gettrace()
            sys.settrace(trace)
            try:
                return func(*args, **kwargs)
            finally:
                sys.settrace(old_trace)

        return wrapper

    return decorator
