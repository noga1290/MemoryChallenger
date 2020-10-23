import Const
import random
from termcolor import colored
import Validators
import pyttsx3


class MemoryChallengerProperties:
    def __init__(self, seq_len: int, language, is_sorted: bool):
        self.seq_len = seq_len
        self.language = language
        self.is_sorted = is_sorted


class MemoryChallenger:
    def __init__(self, seq_len: int, language, read_engine: pyttsx3, is_sorted: bool):
        Validators.validate_seq_len(seq_len)
        if type(language) is not Const.LANGUAGE:
            Validators.validate_format_language(language)

        self.language: Const.LANGUAGE = language
        self.seq_len: int = seq_len
        self.is_sorted: bool = is_sorted
        self.sequence: str = ""
        self.read_engine: pyttsx3.Engine = read_engine

    def change_language(self) -> None:
        if self.language is Const.LANGUAGE.HEBREW:
            self.language = Const.LANGUAGE.ENGLISH
        else:
            self.language = Const.LANGUAGE.HEBREW

    @property
    def __alphabet(self) -> None:
        if self.language is Const.LANGUAGE.HEBREW:
            return Const.HEBREW_ALPHABET
        elif self.language is Const.LANGUAGE.ENGLISH:
            return Const.ENGLISH_ALPHABET

    def change_sorted(self) -> None:
        self.is_sorted = not self.is_sorted

    def set_seq_length(self, new_seq_len: int) -> None:
        Validators.validate_seq_len(new_seq_len)
        self.seq_len = new_seq_len

    def reset_sequence(self) -> None:
        self.sequence = ""

    def randomize_sequence(self) -> None:
        for _ in range(self.seq_len):
            if random.choice([True, False]):
                new_char = random.choice(self.__alphabet)
            else:
                new_char = random.choice(Const.DIGITS)
            self.sequence += str(new_char)

    @property
    def __sequence_for_engine(self) -> str:
        sequence_for_read = ""
        for c in self.sequence:
            if self.language is Const.LANGUAGE.HEBREW:
                if c in Const.HEBREW_ALPHABET:
                    c = Const.HEBREW_ALPHABET_DICT[c]
                else:  # c is a digit
                    c = Const.HEBREW_DIGITS_DICT[int(c)]

            sequence_for_read += c + ", "

        return sequence_for_read

    def read_sequence(self) -> None:
        seq_to_read = self.__sequence_for_engine
        self.read_engine.say(seq_to_read)
        self.read_engine.runAndWait()

    def check_answer(self, answer_str: str) -> None:
        stripped_answer_str = answer_str.upper().strip()
        sequence = self.sequence
        if self.is_sorted:
            sequence = self.__sorted_sequence

        if stripped_answer_str == sequence:
            self.print_success()
        else:
            self.print_failure(answer_str)

    @property
    def __sorted_sequence(self) -> str:
        sorted_sequence = ''.join(sorted(self.sequence))
        return sorted_sequence

    def __message_addition_if_sorted(self, message_str: str) -> str:
        message_str += admin_message(f' and the sorted sequence was {self.__sorted_sequence}')
        return message_str

    def print_success(self) -> None:
        str_to_print = admin_message(f'Well done! The sequence was {self.sequence}')
        if self.is_sorted:
            str_to_print = self.__message_addition_if_sorted(str_to_print)
        print(str_to_print)

    def print_failure(self, answer_by_user: str) -> None:
        str_to_print = admin_message(f'The sequence was {self.sequence}, but you typed ') + colored(answer_by_user, 'red')
        if self.is_sorted:
            str_to_print = self.__message_addition_if_sorted(str_to_print)
        print(str_to_print)

    def print_mem_challenge(self) -> None:
        print(admin_message('*** NEW MEMORY CHALLENGE ***'))
        print(self)

    def __str__(self):
        return self.sequence


def admin_message(message: str):
    return colored(message, 'yellow')
