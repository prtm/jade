def parse_str_to_int(value: str, default: int) -> int:
    """[Return the value after parsing, else default.]

    Args:
        value (str): [string that needs to be parse]
        default (int): [on error default value will be returned]

    Returns:
        int: [parsed or default value]
    """
    try:
        return int(value)
    except:
        return default
