from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_roles
from app.models import Restaurant, User
from app.schemas import RestaurantCreate, RestaurantOut, RestaurantUpdate

router = APIRouter(prefix='/api/v1', tags=['restaurants'])


@router.get('/restaurants', response_model=list[RestaurantOut])
def list_restaurants(
    city: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Restaurant)
    if city:
        query = query.filter(Restaurant.city == city)
    return query.filter(Restaurant.is_active.is_(True)).all()


@router.get('/restaurants/{restaurant_id}', response_model=RestaurantOut)
def get_restaurant(restaurant_id: str, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail='Restaurant not found')
    return restaurant


@router.post('/restaurants', response_model=RestaurantOut, status_code=201)
def create_restaurant(
    payload: RestaurantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles('owner', 'admin')),
):
    restaurant = Restaurant(owner_id=current_user.id, **payload.model_dump())
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant


@router.patch('/restaurants/{restaurant_id}', response_model=RestaurantOut)
def update_restaurant(
    restaurant_id: str,
    payload: RestaurantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail='Restaurant not found')
    if current_user.role != 'admin' and restaurant.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail='Not allowed to update this restaurant')
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(restaurant, key, value)
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant
