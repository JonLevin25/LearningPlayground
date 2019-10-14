import helper

b64_to_int = helper.dict_builder(('A', 'Z'), ('a', 'z'), ('0', '9'), '+' '/')
int_to_b64 = {v: k for k, v in b64_to_int.items()}


def serialize_bin_str(ints, group_len: int = 8):
    return "".join((helper.byte_str(i, group_len) for i in ints))


def encode(input_str: str, debug: bool = False) -> str:
    # get raw binary string (without '0b' prefix) of entire input string
    utf_codes = (ord(c) for c in input_str)
    if debug:
        # if using iterator for debug, should still be usable afterwards
        # otherwise, it will be a one time use (lazy) generator, which should be more memory efficient
        utf_codes = list(utf_codes)
        print(F"utf codes: {', '.join(map(str, zip(input_str, utf_codes)))}")

    binary = serialize_bin_str(utf_codes)
    if debug:
        print(f"binary: {binary} ({list(helper.group_str(8, binary, filler='0'))})")

    # split binary to groups of 6 bits (each of which corresponds to 1 base64 digit)
    grouped_binary = list(helper.group_str(6, binary, filler='0')) # TODO: convert to generator and get 'remaining' by final str len?
    symbols = len(grouped_binary)
    if debug:
        grouped_binary = list(grouped_binary)
        print(f"grouped: {grouped_binary}")

    char_codes = map(lambda i: int(i, 2), grouped_binary)
    result = "".join((int_to_b64[i] for i in char_codes))

    remaining_symbols = (4 - (symbols % 4)) % 4 # invert modulo gets the "symbols left". modulo again takes care of edge case where symbols % 4 == 0
    result += "=" * remaining_symbols
    return result


def decode(base64_str: str, debug: bool = False) -> str:
    try:
        ints = (b64_to_int[i] for i in base64_str if i != '=')
        if debug:
            ints = list(ints)
            print(f"input: {''.join(map(str, zip(base64_str, ints)))}")
        binary = serialize_bin_str(ints, group_len=6)
        if debug:
            print(f"binary: {list(helper.group_str(8, binary))}")

        # group binary into octets, parse to ints
        utf_codes = (int(bin_str, 2) for bin_str in helper.group_str(8, binary, "0"))

        if debug:
            utf_codes = list(utf_codes)
            print(f"decoded utf: {', '.join(utf_codes)}")
        return "".join((chr(i) for i in utf_codes))

    except KeyError:
        raise ValueError("Invalid input string!")


DEBUG = 1
# result = decode("SGVsbG8=", DEBUG)
result = encode("Hello", DEBUG)
print(result)
