# bs_utils.py

from rich import print


def viz_binary_search(func):
    def wrapper(*args, **kwargs):
        LINE_WIDTH = 150

        def print_number_line(low, mid, high, condition_result, is_minimization):
            # Scale the range to fit within LINE_WIDTH
            range_width = high - low + 1
            if range_width <= LINE_WIDTH:
                scale = 1
                display_low, display_high = low, high
            else:
                scale = range_width / LINE_WIDTH
                display_low = 0
                display_high = LINE_WIDTH - 1

            # Map low, mid, high to positions on the line
            def map_value(val):
                if range_width <= LINE_WIDTH:
                    return val - low
                else:
                    return int((val - low) / scale)

            low_pos = map_value(low)
            mid_pos = map_value(mid)
            high_pos = map_value(high)

            # Get value at a given display position
            def get_value_at_pos(pos):
                if range_width <= LINE_WIDTH:
                    return low + pos
                else:
                    return low + int(pos * scale)

            # Create markers row for L, M, H (handling overlaps by spreading)
            markers = [" "] * LINE_WIDTH
            pos_groups = {}
            for lab, p in [("L", low_pos), ("M", mid_pos), ("H", high_pos)]:
                pos_groups.setdefault(p, []).append(lab)
            for p, labs in pos_groups.items():
                for i, lab in enumerate(labs):
                    pp = p + i
                    if pp < LINE_WIDTH:
                        markers[pp] = lab

            # Create the number line with ticks
            line = ["-"] * LINE_WIDTH

            # Add regular ticks every ~15 positions
            step = max(1, LINE_WIDTH // 10)
            for i in range(0, LINE_WIDTH, step):
                line[i] = "|"

            # Ensure ticks at key positions
            for p in {low_pos, mid_pos, high_pos}:
                line[p] = "|"

            # Create numbers row
            numbers = [" "] * LINE_WIDTH

            def place_number(pos, val):
                strv = str(val)
                lenv = len(strv)
                start = max(0, pos - lenv // 2)
                end = start + lenv
                if end > LINE_WIDTH:
                    start = LINE_WIDTH - lenv
                    end = LINE_WIDTH
                # Check for overlap
                if any(numbers[j] != " " for j in range(start, end)):
                    return False
                numbers[start:end] = list(strv)
                return True

            # Place key numbers first (low, mid, high)
            place_number(low_pos, low)
            place_number(mid_pos, mid)
            place_number(high_pos, high)

            # Place numbers at regular ticks if no overlap
            for i in range(0, LINE_WIDTH, step):
                place_number(i, get_value_at_pos(i))

            # Determine action message
            if condition_result and is_minimization:
                action = f"Update high to {mid - 1}"
            elif condition_result:
                action = f"Update low to {mid + 1}"
            elif is_minimization:
                action = f"Update low to {mid + 1}"
            else:
                action = f"Update high to {mid - 1}"

            # Print the visualization
            print(f"\nIteration: low={low}, mid={mid}, high={high}")
            print(
                f"Condition: {'✅' if condition_result else '❌'} "
                f"{'Feasible' if condition_result else 'Not feasible'}"
            )
            print(f"Action: {action}")
            print("Number line:")
            print("".join(markers))
            print("".join(line))
            print("".join(numbers))
            if range_width > LINE_WIDTH:
                print(f"(Scaled: 1 unit ≈ {scale:.2f} actual units)")
            print("-" * LINE_WIDTH)

        # Wrap the binary search function
        def binary_search_wrapper(self, weights, days):
            low = max(weights)
            high = sum(weights)
            result = -1
            is_minimization = True

            while low <= high:
                mid = low + (high - low) // 2
                condition_result = self.daysToShipPackages(weights, mid) <= days
                print_number_line(low, mid, high, condition_result, is_minimization)

                if condition_result:
                    result = mid
                    if is_minimization:
                        high = mid - 1
                    else:
                        low = mid + 1
                else:
                    if is_minimization:
                        low = mid + 1
                    else:
                        high = mid - 1

            return result

        # Call the wrapped binary search
        return binary_search_wrapper(*args, **kwargs)

    return wrapper
