from setuptools import setup, find_packages

setup(
    name='vault',
    version='1.0.0',
    author='Angelo Yana',
    description='Command-line credential manager.',
    url='https://github.com/angeloyana/vault',
    packages=find_packages(),
    install_requires=[
        'cryptography==42.0.5',
        'bcrypt==4.1.2',
        'colorama==0.4.6',
        'halo==0.0.31',
        'SQLAlchemy==2.0.27'
    ],
    entry_points={
        'console_scripts': [
            'vault = vault.__main__:main'
        ]
    }
)
