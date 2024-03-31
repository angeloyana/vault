import argparse
from vault.auth import authenticate_user
from vault.manager import CredentialManager


def main():
    parser = argparse.ArgumentParser(
        prog='vault', description='Command-line credential manager.')
    commands = [command['name']
                for command in CredentialManager.get_commands()]
    parser.add_argument('command', nargs='?', choices=commands)

    args = parser.parse_args()
    pswd = authenticate_user()
    manager = CredentialManager(pswd)

    if args.command is None:
        manager.cmdloop()
    else:
        command = getattr(manager, f'do_{args.command}')
        command('')


if __name__ == '__main__':
    main()
