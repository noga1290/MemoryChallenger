import re
import Const


class MemoryChallengerIllegalValue(Exception):
    def __init__(self, value):
        self.message = f"Error: Illegal value received {str(value)}"


def validate_seq_len(seq_len: int):
    if seq_len <= 0:
        raise MemoryChallengerIllegalValue(seq_len)


def validate_format_language(language) -> Const.LANGUAGE:
    try:
        return Const.LANGUAGE(language)
    except Exception:
        raise MemoryChallengerIllegalValue(language)


def validate_format_regex_length(regex_command: re, str_to_check: str) -> int:
    change_length = regex_command.match(str_to_check)
    if change_length is not None:
        num_match = re.search('\d+', change_length.string)
        return int(str(num_match.group()))

    return None

