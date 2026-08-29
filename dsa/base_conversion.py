def convert_base(num_as_string: str, b1: int, b2: int) -> str:
    def to_base(num_as_int, base):
        return (
            ""
            if num_as_int == 0
            else to_base(num_as_int // base, base)
            + hexdigits[num_as_int % base].upper()
        )

    is_negative = num_as_string[0] == "-"
    num_as_int = reduce(
        lambda x, c: x * b1 + hexdigits.index(c.lower()),
        num_as_string[is_negative:],
        0,
    )
    return ("-" if is_negative else "") + (
        "0" if num_as_int == 0 else to_base(num_as_int, b2)
    )


print(convert_base("10", 10, 2))
print(convert_base("10", 2, 10))
