from typing import Optional
import os
import sys
import bcrypt
from halo import Halo

from vault.config import config
from vault.ui import UI


def create_pswd() -> Optional[str]:
    UI.title('New here? Setup your password')
    pswd = UI.getpass('Create password: ')
    confirm_pswd = UI.getpass('Confirm password: ')
    if pswd != confirm_pswd:
        UI.error('Password did not match!')
        sys.exit(1)

    with open(config.get('PATH', 'Password'), 'wb') as pswd_file, Halo('Saving password...') as spinner:
        hashed_pswd = bcrypt.hashpw(pswd.encode(), bcrypt.gensalt())
        pswd_file.write(hashed_pswd)
        spinner.succeed('Password was created!')
        return pswd


def verify_pswd() -> Optional[str]:
    UI.title('Welcome back! Enter your password')
    pswd = UI.getpass()
    with open(config.get('PATH', 'Password'), 'rb') as pswd_file, Halo('Verifying password...') as spinner:
        hashed_pswd = pswd_file.read()
        if not bcrypt.checkpw(pswd.encode(), hashed_pswd):
            spinner.fail('Incorrect password!')
            sys.exit(1)
        spinner.succeed('Password was verified!')
        return pswd


def authenticate_user() -> Optional[str]:
    if not os.path.isfile(config.get('PATH', 'Password')) or os.path.getsize(config.get('PATH', 'Password')) == 0:
        return create_pswd()
    return verify_pswd()
