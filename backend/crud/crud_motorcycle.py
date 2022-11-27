from typing import Any, Dict, Union, List
import string
import random

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.crud.base import CRUDBase
from backend.enums import ProductStatusEnum
from backend.models.motorcycle import Motorcycle
from backend.schemas.motorcycle import MotorcycleCreate, MotorcycleUpdate


def _get_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


class CRUDMotorcycle(CRUDBase[Motorcycle, MotorcycleCreate, MotorcycleUpdate]):

    def create(self, db: Session, *, obj_in: MotorcycleCreate) -> Motorcycle:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, id=_get_random_string(12))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: Motorcycle, obj_in: Union[MotorcycleUpdate, Dict[str, Any]]
    ) -> Motorcycle:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_multi_with_filters(
        self, db: Session, *, offset: int = 0, limit: int = 100,
            show_sold: bool = False, show_status: ProductStatusEnum = ProductStatusEnum.active.value
    ) -> List[Motorcycle]:
        return db.query(self.model)\
            .where(Motorcycle.sold == show_sold)\
            .where(Motorcycle.status == show_status) \
            .order_by(desc(Motorcycle.date_created)) \
            .offset(offset)\
            .limit(limit)\
            .all()


motorcycle = CRUDMotorcycle(Motorcycle)
