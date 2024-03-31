from typing import List, Dict, Union, Optional
import sys
import cmd
from halo import Halo

from vault.ui import UI, Text
from vault.database import Database, Credential
from vault.auth import verify_pswd, create_pswd

CommandList = List[Dict[str, Union[str, None]]]


class CredentialManager(cmd.Cmd):
    prompt = '-> '
    nohelp = Text.dim("No description for '%s'")
    unknowncmd = Text.dim("Unknown command '%s'")

    def __init__(self, pswd: str):
        super().__init__()
        self.db = Database(pswd)

    @staticmethod
    def get_commands() -> CommandList:
        commands = [getattr(CredentialManager, attr) for attr in dir(
            CredentialManager) if attr.startswith('do_')]
        commands = [{'name': command.__name__[3:],
                     'description': command.__doc__} for command in commands]
        return commands

    def default(self, args: str) -> None:
        for command in self.get_commands():
            if args in command['name']:
                UI.warn(f"Did you mean '{command['name']}'")
                return
        print(self.unknowncmd % args)

    def pick_credential(self, title: str) -> Optional[Credential]:
        credentials = self.db.get_many()
        if not credentials:
            UI.warn('Database is empty')
            return

        UI.title(title)
        for i, credential in enumerate(credentials, 1):
            print(f'{i}. {credential.name}')
        try:
            choice = int(input(f'Choose from [1-{len(credentials)}]: '))
            if choice < 0 or choice > len(credentials):
                UI.error('Choice is out of range!')
                return
        except ValueError:
            UI.error('Invalid choice!')
            return

        picked_credential = credentials[choice - 1]
        return picked_credential

    # Commands
    def do_help(self, args: str) -> None:
        """Display this"""
        if args:
            command = [cmd['description']
                       for cmd in self.get_commands() is cmd['name'] == args]
            if command:
                print(command[0])
            else:
                print(self.nohelp % args)
        else:
            UI.title('Command list')
            for command in self.get_commands():
                name, description = command.values()
                print(f' {name} - {description}')

    def do_clear(self, args: str) -> None:
        """Clear the terminal screen"""
        UI.clear()

    def do_exit(self, args: str) -> None:
        """Exit the session"""
        sys.exit(0)

    def do_change_password(self, args: str) -> None:
        """Change your master password"""
        verify_pswd(title='Change Password', pswd_prompt='Current password: ')
        pswd = create_pswd(title=None, pswd_prompt='New password: ', confirm_pswd_prompt='Confirm new password: ',
                           confirm_save=True, exit=False, on_save_message='New password was saved!')

        if pswd is not None:
            with Halo("Updating database with the new password, PLEASE DON'T EXIT...") as spinner:
                credentials = self.db.get_many()
                self.db.pswd = pswd
                for credential in credentials:
                    self.db.update(credential, None, credential.parsed_entries)
                spinner.succeed('Database was safely updated!')

    # CRUD Commands
    def do_add(self, args: str) -> None:
        """Add new credential"""
        UI.title('Add Credential')
        while True:
            name = input('Name: ').strip()
            if not name:
                UI.warn('Please enter the name')
                continue
            if self.db.exists(name):
                UI.warn(f"'{name}' was already used")
                continue
            break

        UI.instruction(['Leave the key prompt empty to proceed.'], start='\n')
        entries = {}
        while True:
            key = input('Key: ')
            if not key and len(entries.keys()) > 0:
                break
            if key in entries:
                UI.warn(f"'{key}' was already used")
                continue
            if not key and len(entries.keys()) == 0:
                UI.warn('Must add atleast 1 key-value pair')
                continue

            value = input('Value: ')
            entries[key] = value

        UI.title('Confirmation')
        UI.print_credential(name, entries, end='\n')
        choice = UI.yes_or_no('Save it? (Y|n) ')
        if choice:
            self.db.insert(name, entries)
            UI.success(f"'{name}' was added!")
        else:
            UI.warn('Cancelled')

    def do_get(self, args: str) -> None:
        """Get a credential"""
        picked_credential = self.pick_credential('Get Credential')
        if picked_credential is None:
            return

        UI.print_credential(
            picked_credential.name, picked_credential.parsed_entries, start='\n', end='\n')

    def do_list(self, args: str) -> None:
        """List all credential"""
        credentials = self.db.get_many()
        if not credentials:
            UI.warn('Database is empty')
            return

        UI.title('Credential list')
        for credential in credentials:
            UI.print_credential(
                credential.name, credential.parsed_entries, end='\n')

    def do_update(self, args: str) -> None:
        """Update a credential"""
        picked_credential = self.pick_credential('Update Credential')
        if picked_credential is None:
            return

        UI.title('Update current values', start='\n')
        UI.instruction([
            'Leave the prompt empty to keep the previous value.',
            f"Type {Text.bold('del')} on key prompt to delete that entry."
        ])
        name = picked_credential.name
        new_name = input(f'Name: ({name}) ').strip() or None
        new_entries = {}

        for key, value in picked_credential.parsed_entries.items():
            new_key = input(f'Key: ({key}) ').strip()
            if new_key == 'del':
                continue
            new_value = input(f'Value: ({value}) ').strip()
            new_entries[new_key or key] = new_value or value

        UI.title('Add new entries', start='\n')
        UI.instruction(['Leave the key prompt empty to proceed.'])
        while True:
            key = input('Key: ')
            if not key and len(new_entries.keys()) > 0:
                break
            if key in new_entries:
                UI.warn(f"'{key}' was already used")
                continue
            if not key and len(new_entries.keys()) == 0:
                UI.warn('Must add atleast 1 key-value pair')
                continue

            value = input('Value: ')
            new_entries[key] = value

        UI.title('Confirmation')
        UI.print_credential(
            name, picked_credential.parsed_entries, start='Previous:\n', end='\n')
        UI.print_credential(new_name or name, new_entries,
                            start='Updated:\n', end='\n')
        choice = UI.yes_or_no('Update it? (Y|n) ')
        if choice:
            self.db.update(picked_credential, new_name, new_entries)
            UI.success(f"'{name}' was updated!")
        else:
            UI.warn('Cancelled')

    def do_delete(self, args: str) -> None:
        """Delete a credential"""
        picked_credential = self.pick_credential('Delete Credential')
        if picked_credential is None:
            return

        UI.title('Confirmation')
        UI.print_credential(picked_credential.name,
                            picked_credential.parsed_entries, end='\n')
        choice = UI.yes_or_no('Delete it? (Y|n) ')
        if choice:
            self.db.delete(picked_credential)
            UI.success(f"'{picked_credential.name}' was deleted.")
        else:
            UI.warn('Cancelled')
