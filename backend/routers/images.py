import io
from PIL import Image
from fastapi import APIRouter, Depends, UploadFile
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT

from backend.utils.image_handler import upload_image_to_cloud_storage, create_thumbnail_for_image
from backend.models.api.UploadImageResponse import UploadImageResponse
from backend.exceptions.FileUploadError import FileUploadError

router = APIRouter(tags=["Images"])


@router.post('/productImage', response_model=UploadImageResponse, status_code=201)
async def upload_product_image(image: UploadFile, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    image_content = await image.read()
    img = Image.open(io.BytesIO(image_content))

    try:
        thumbnail_url = create_thumbnail_for_image(img, image.filename)
        image_url = upload_image_to_cloud_storage(img, image.filename)
        return UploadImageResponse(thumbnail=thumbnail_url, image=image_url)
    except FileUploadError as e:
        raise HTTPException(status_code=500, detail='Failed to process image.')