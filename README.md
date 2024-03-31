# vault

A command-line tool made with python for managing secrets such as passwords 🔐 and API keys 🔑 securely.

## Features

* Add, Get, List, Update, Delete credentials.
* Encrypt and decrypt credentials using a master password.

## Installation

For quick installation, run:

```sh
git clone https://github.com/angeloyana/vault.git
cd vault
pip install .
```

## Usage

To get start, you can run `vault`.
At first you will be prompted to create your master password, then you must enter that password on the next sessions to continue.

```
$ vault
-----------------------------
New here? Setup your password
-----------------------------
Create password: ********
Confirm password: ********
✔ Password was created!
->
```

Inside the session, you can type `help` or `?` to see the list of commands.

```
-> help
------------
Command list
------------
...
```

By default, if you didn't supply any argument when you called the `vault`,
it will run as interactive mode, which means is will continuously prompt you for a command,
until you type `exit` or run `Ctrl-C`. But if you run `vault <command>`, it will execute that command right away but it won't run in interactive mode.

---

You can find the configuration file of `vault` in `~/.vault.ini`.

## Reminders

This is for educational purpose only and might not be suitable for daily life usage.

## License

[MIT](/LICENSE)
