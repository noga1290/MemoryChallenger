import argparse
import pyttsx3
import Const
import Validators
from Memory_Challenger import MemoryChallengerProperties, MemoryChallenger, admin_message


def init(seq_len: int, language, is_sorted: bool) -> MemoryChallenger:
    Validators.validate_seq_len(seq_len)
    const_language = Validators.validate_format_language(language)

    read_engine = pyttsx3.init()
    read_rate = read_engine.getProperty('rate')
    read_engine.setProperty('rate', read_rate - 50)
    mem_challenger = MemoryChallenger(seq_len, const_language, read_engine, is_sorted)
    return mem_challenger


def parse_command(user_command: str, mem_challenger: MemoryChallenger) -> Const.STATUS:
    new_length = Validators.validate_format_regex_length(Const.COMMAND.CHANGE_LENGTH.value, user_command)
    if new_length is not None:
        mem_challenger.set_seq_length(new_length)
    else:
        try:
            user_command_enum = Const.COMMAND(user_command)
        except ValueError:
            print(admin_message(f"The command {user_command} is unknown. Please try to use one of the following"
                                f" commands: {Const.LIST_COMMANDS}"))
            return Const.STATUS.UNDEFINED_ACTION

        if user_command_enum in Const.QUIT_COMMANDS_LIST:
            return Const.STATUS.QUIT
        elif user_command_enum in Const.NEXT_COMMANDS_LIST:
            return Const.STATUS.NEXT
        elif user_command_enum == Const.COMMAND.CHANGE_LANGUAGE:
            mem_challenger.change_language()
        elif user_command_enum == Const.COMMAND.CHANGE_SORTED:
            mem_challenger.change_sorted()

    print(admin_message(f"The command '{user_command}' was executed."))
    return Const.STATUS.DONE_ACTION


def parse_cmd_args():
    parser = argparse.ArgumentParser(description=admin_message('Please enter parameters for the Memory Challenger.'))
    parser.add_argument('--language', metavar='language', choices=Const.LANGUAGES_LIST,
                        help=admin_message(f'Select language from the following list: {Const.LANGUAGES_LIST}'))
    parser.add_argument('--length', metavar='sequence_length', type=int,
                        help=admin_message(f'Select sequence length for the exercise; must be >0!'))
    parser.add_argument('--sorted', required=False, dest='is_sorted', action='store_true',
                        help=admin_message(f'Select if you want sorting as a part of the exercise.'))
    parser.set_defaults(is_sorted=False)

    args = parser.parse_args()
    mem_challenger_properties = MemoryChallengerProperties(args.length, args.language, args.is_sorted)
    return mem_challenger_properties


def main():
    mem_challenger_properties = parse_cmd_args()
    mem_challenger = init(mem_challenger_properties.seq_len, mem_challenger_properties.language,
                          mem_challenger_properties.is_sorted)

    while True:
        user_command = input()
        action_status = parse_command(user_command, mem_challenger)
        if action_status is Const.STATUS.QUIT:
            break

        elif action_status is Const.STATUS.NEXT:  # should begin exercise only in such case
            mem_challenger.randomize_sequence()
            mem_challenger.read_sequence()
            user_answer = input()
            mem_challenger.check_answer(user_answer)
            mem_challenger.reset_sequence()


if __name__ == "__main__":
    main()
