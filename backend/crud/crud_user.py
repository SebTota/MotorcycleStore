from typing import Any, Dict, Optional, Union

from sqlalchemy import or_
from sqlalchemy.orm import Session

from backend.core.security import get_password_hash, verify_password
from backend.crud.base import CRUDBase
from backend.models.user import User
from backend.schemas.user import UserCreate, UserUpdate
from backend.utils.deps import get_random_string


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email_or_username(self, db: Session, *, email: str, username: str) -> Optional[User]:
        return db.query(User).filter(or_(User.email == email, User.username == username)).first()

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            id=get_random_string(12),
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            username=obj_in.username,
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            is_active=True,
            is_superuser=False
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, username: str, password: str) -> Optional[User]:
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
