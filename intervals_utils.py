def draw_interval(interval):
    if interval[1] > 0 and interval[1] < 1e4:
        return
    for i in range(interval[1] + 1):
        if i < interval[0]:
            print("  ", end="")
        elif i == interval[0]:
            print("[" + str(interval[0]), end="")
        elif i == interval[1]:
            print(str(interval[1]) + "]", end="")
        else:
            print("--", end="")
    print("")


def draw_intervals(ints):
    for interval in ints:
        draw_interval(interval)
    print("============================")
