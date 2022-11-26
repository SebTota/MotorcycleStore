from fastapi import APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT

from backend.exceptions import NoProductFoundError
from backend.controllers import MotorcycleController
from backend.enums import ProductStatusEnum
from backend.schemas import Motorcycle, UpdateMotorcycle, MotorcycleListResponse

router = APIRouter(tags=["Store"])


@router.get('/motorcycles', response_model=MotorcycleListResponse)
def get_motorcycles(limit: int = 1, show_sold: bool = False,
                    show_status: ProductStatusEnum = ProductStatusEnum.active.value, page: int = 1):
    start_index = (limit * page) - limit
    motorcycles_controller = MotorcycleController.collection.offset(start_index)
    motorcycles_controller = motorcycles_controller \
        .filter(sold=show_sold) \
        .filter(status=show_status)

    motorcycles_controller = motorcycles_controller.order('-date_created')
    motorcycles_controller = motorcycles_controller.fetch(limit + 1)

    motorcycles = [m.to_dict() for m in motorcycles_controller]

    has_next_page = False
    if len(motorcycles) > limit:
        motorcycles.pop()
        has_next_page = True

    return MotorcycleListResponse(num_items=len(motorcycles),
                                  items=motorcycles,
                                  page=page,
                                  has_next_page=has_next_page)


@router.get('/motorcycle/{item_id}')
def get_motorcycle(item_id: str):
    try:
        return MotorcycleController.get_motorcycle_by_id(item_id)
    except NoProductFoundError as e:
        raise HTTPException(status_code=404, detail='Invalid motorcycle id.')


@router.post('/motorcycle', status_code=201, response_description="id of the newly created item")
def new_motorcycle(motorcycle: Motorcycle, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    if not valid_motorcycle(motorcycle):
        raise HTTPException(status_code=400, detail='Invalid motorcycle details provided.')

    return {
        'id': MotorcycleController.add_motorcycle(motorcycle).id
    }


@router.post('/motorcycle/{item_id}', response_description="id of the updated item")
def update_motorcycle(item_id: str, motorcycle: UpdateMotorcycle, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return {
        'id': MotorcycleController.update_motorcycle(item_id, motorcycle, motorcycle.__fields_set__).id
    }


@router.delete('/motorcycle/{item_id}')
def delete_motorcycle(item_id: str, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    MotorcycleController.delete_motorcycle(item_id)
    return "Deleted motorcycle"


def valid_motorcycle(motorcycle: Motorcycle) -> bool:
    """
    Validate that a new motorcycle request provided information within set limits.
    """
    if motorcycle.price <= 0 or motorcycle.odometer <= 0 or motorcycle.year < 1000 or motorcycle.year > 9999:
        return False
    return True
