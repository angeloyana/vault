from typing import Iterable, Dict, Optional
import os
import sys
import getpass
from colorama import Fore, Style


class Text:
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'

    def bold(text: str) -> str:
        return f'{Style.BRIGHT}{text}{Style.RESET_ALL}'

    def dim(text: str) -> str:
        return f'{Fore.LIGHTBLACK_EX}{text}{Style.RESET_ALL}'

    def yellow(text: str) -> str:
        return f'{Fore.YELLOW}{text}{Style.RESET_ALL}'

    def red(text: str) -> str:
        return f'{Fore.RED}{text}{Style.RESET_ALL}'

    def green(text: str) -> str:
        return f'{Fore.GREEN}{text}{Style.RESET_ALL}'

    def blue(text: str) -> str:
        return f'{Fore.BLUE}{text}{Style.RESET_ALL}'


class UI:
    # Output
    def clear() -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    def clear_line_up() -> None:
        sys.stdout.write(f'{Text.CURSOR_UP_ONE}{Text.ERASE_LINE}')

    def title(text: str, start: Optional[str] = '', end: Optional[str] = '') -> None:
        sys.stdout.write(start)
        print('-' * len(text))
        print(text)
        print('-' * len(text))
        sys.stdout.write(end)

    def instruction(instructions: Iterable[str], start: Optional[str] = '', end: Optional[str] = '') -> None:
        sys.stdout.write(start)
        for instruction in instructions:
            print(f'• {instruction}')
        sys.stdout.write(end)

    def warn(text: str) -> None:
        print(f"{Text.yellow('!!')} {text}")

    def error(text: str) -> None:
        print(f"{Text.red('✘')} {text}")

    def success(text: str) -> None:
        print(f"{Text.green('✔')} {text}")

    def print_credential(name: str, entries: Dict[str, str], start: Optional[str] = '', end: Optional[str] = '') -> None:
        print(f'{start}[{name}]')
        for key, value in entries.items():
            print(f"  {Text.dim(key)} - {value}")
        sys.stdout.write(end)

    # Input
    def getpass(prompt: Optional[str] = 'Password: ') -> str:
        pswd = getpass.getpass(prompt)
        UI.clear_line_up()
        print(f"{prompt}{'*' * len(pswd)}")
        return pswd

    def yes_or_no(prompt: str) -> bool:
        choice = input(prompt).strip().lower()
        if choice in {'', 'y', 'yes'}:
            return True
        return False
