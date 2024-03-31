from typing import Optional
import os
import sys
import bcrypt
from halo import Halo

from vault.config import config
from vault.ui import UI


def create_pswd(
        title: Optional[str] = None,
        pswd_prompt: str = 'Create password: ',
        confirm_pswd_prompt: str = 'Confirm password: ',
        confirm_save_prompt: Optional[str] = 'Save it? (Y|n) ',
        confirm_save: Optional[bool] = False,
        on_save_message: Optional[str] = 'Password was created!',
        exit: Optional[bool] = True) -> Optional[str]:
    if title is not None:
        UI.title(title)
    pswd = UI.getpass(pswd_prompt)
    confirm_pswd = UI.getpass(confirm_pswd_prompt)
    if pswd != confirm_pswd:
        UI.error('Password did not match!')
        if exit:
            sys.exit(1)
        else:
            return

    if confirm_save:
        choice = UI.yes_or_no(confirm_save_prompt)
    else:
        choice = True

    if choice:
        with open(config.get('PATH', 'Password'), 'wb') as pswd_file, Halo('Saving password...') as spinner:
            hashed_pswd = bcrypt.hashpw(pswd.encode(), bcrypt.gensalt())
            pswd_file.write(hashed_pswd)
            spinner.succeed(on_save_message)
            return pswd
    else:
        UI.warn('Cancelled')
        if exit:
            sys.exit(0)


def verify_pswd(
        title: Optional[str] = None,
        pswd_prompt: str = 'Password: ',
        exit: Optional[bool] = True) -> Optional[str]:
    if title is not None:
        UI.title(title)
    pswd = UI.getpass(pswd_prompt)
    with open(config.get('PATH', 'Password'), 'rb') as pswd_file, Halo('Verifying password...') as spinner:
        hashed_pswd = pswd_file.read()
        if not bcrypt.checkpw(pswd.encode(), hashed_pswd):
            spinner.fail('Incorrect password!')
            if exit:
                sys.exit(1)
            else:
                return
        spinner.succeed('Password was verified!')
        return pswd


def authenticate_user() -> Optional[str]:
    if not os.path.isfile(config.get('PATH', 'Password')) or os.path.getsize(config.get('PATH', 'Password')) == 0:
        return create_pswd('New here? Setup your password')
    return verify_pswd('Welcome back! Enter your password')
