from typing import List, Dict, Optional, Union
import json
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..config import config
from . import cipher

engine = db.create_engine(f"sqlite:///{config.get('PATH', 'Database')}")
Base = declarative_base()


class Credential(Base):
    __tablename__ = 'credentials'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    entries = db.Column(db.LargeBinary)


class Database:
    def __init__(self, pswd: str):
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)

        self.pswd = pswd
        self.session = Session()

    def exists(self, name: str) -> bool:
        credential = self.session.query(
            Credential).filter_by(name=name).first()
        return credential is not None

    def insert(self, name: str, entries: Dict[str, str]) -> None:
        encrypted_entries = cipher.encrypt(json.dumps(entries), self.pswd)
        credential = Credential(name=name, entries=encrypted_entries)
        self.session.add(credential)
        self.session.commit()

    def get(self, name: str) -> Optional[Credential]:
        credential = self.session.query(
            Credential).filter_by(name=name).first()
        if credential is not None:
            decrypted_entries = cipher.decrypt(credential.entries, self.pswd)
            credential.parsed_entries = json.loads(decrypted_entries)
            return credential

    def get_many(self) -> List[Credential]:
        credentials = self.session.query(Credential).all()
        for credential in credentials:
            decrypted_entries = cipher.decrypt(credential.entries, self.pswd)
            credential.parsed_entries = json.loads(decrypted_entries)
        return credentials

    def update(self, credential: Union[str, Credential], new_name: Optional[str], new_entries: Dict[str, str]) -> None:
        if credential is str:
            credential = self.get(credential)
        if credential is not None:
            if new_name is not None:
                credential.name = new_name
            encrypted_entries = cipher.encrypt(
                json.dumps(new_entries), self.pswd)
            credential.entries = encrypted_entries
            self.session.commit()

    def delete(self, credential: Union[str, Credential]) -> None:
        if credential is str:
            credential = self.get(credential)
        if credential is not None:
            self.session.delete(credential)
            self.session.commit()
