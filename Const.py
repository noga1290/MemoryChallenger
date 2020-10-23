import re
from enum import Enum

HEBREW_ALPHABET_DICT = \
    {"א": "Aleph",
     "ב": "Bet",
     "ג": "Gimel",
     "ד": "Dalet",
     "ה": "Hey",
     "ו": "Vav",
     "ז": "Zayin",
     "ח": "heth",
     "ט": "Tet",
     "י": "Yood",
     "כ": "Kaf",
     "ל": "Lamed",
     "מ": "Mam",
     "נ": "Noon",
     "ס": "Sameh",
     "ע": "Ayin",
     "פ": "Peh",
     "צ": "Tzadik",
     "ק": "Koof",
     "ר": "Reysh",
     "ש": "Shin",
     "ת": "Tav"}

HEBREW_ALPHABET = list(HEBREW_ALPHABET_DICT.keys())
ENGLISH_ALPHABET = [chr(ord("A") + i) for i in range(26)]

DIGITS = [i for i in range(10)]
HEBREW_DIGITS_DICT = {
    0: "Eh fehs",
    1: "Ehad",
    2: "Shtaah'yim",
    3: "Shalosh",
    4: "Arba",
    5: "Ha mesh",
    6: "Sheh'esh",
    7: "Sheh vah",
    8: "Shmo neh",
    9: "Teh sha",
}
HEBREW_DIGITS = list(HEBREW_DIGITS_DICT.keys())


class LANGUAGE(Enum):
    HEBREW = "HEBREW"
    ENGLISH = "ENGLISH"


LANGUAGES_LIST = [LANGUAGE.HEBREW.value, LANGUAGE.ENGLISH.value]


class COMMAND(Enum):
    BEGIN = 'begin'
    NEXT = 'next'
    EMPTY_COMMAND = ''

    QUIT = 'quit'
    EXIT = 'exit'
    BYE = 'bye'

    CHANGE_LENGTH = re.compile('change length \d+')
    CHANGE_LANGUAGE = 'change language'
    CHANGE_SORTED = 'change sorted'


QUIT_COMMANDS_LIST = [COMMAND.QUIT, COMMAND.EXIT, COMMAND.BYE]
NEXT_COMMANDS_LIST = [COMMAND.BEGIN, COMMAND.NEXT, COMMAND.EMPTY_COMMAND]
LIST_COMMANDS = NEXT_COMMANDS_LIST + QUIT_COMMANDS_LIST + [COMMAND.CHANGE_LANGUAGE, COMMAND.CHANGE_SORTED,
                                                           COMMAND.CHANGE_LENGTH.value.pattern]


class STATUS(Enum):
    UNDEFINED_ACTION = -1
    QUIT = 0
    NEXT = 1
    DONE_ACTION = 2
