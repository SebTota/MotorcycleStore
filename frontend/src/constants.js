export const HOST = 'http://localhost:9000';
export const ROUTES = {
    GET_MOTORCYCLES: '/store/motorcycles?show_sold={show_sold}',
    GET_MOTORCYCLE: '/store/motorcycle/{id}',
    UPDATE_MOTORCYCLE: '/store/motorcycle/{id}',
    CREATE_MOTORCYCLE: '/store/motorcycle',
    DELETE_MOTORCYCLE: '/store/motorcycle/{id}',
    USER_LOGIN: '/login',
    UPLOAD_IMAGE: '/store/productImage'
}
