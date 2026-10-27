from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_roles
from app.models import BiryaniItem, Restaurant, User
from app.schemas import MenuItemCreate, MenuItemOut, MenuItemUpdate

router = APIRouter(prefix='/api/v1', tags=['menu'])


@router.get('/biryani', response_model=list[MenuItemOut])
def list_biryani_items(db: Session = Depends(get_db), category: str | None = None):
    query = db.query(BiryaniItem)
    if category:
        query = query.filter(BiryaniItem.category == category)
    return query.filter(BiryaniItem.is_available.is_(True)).all()


@router.get('/biryani/{item_id}', response_model=MenuItemOut)
def get_biryani_item(item_id: str, db: Session = Depends(get_db)):
    item = db.query(BiryaniItem).filter(BiryaniItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail='Menu item not found')
    return item


@router.post('/restaurants/{restaurant_id}/menu', response_model=MenuItemOut, status_code=status.HTTP_201_CREATED)
def create_menu_item(
    restaurant_id: str,
    payload: MenuItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles('owner', 'admin')),
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail='Restaurant not found')
    if current_user.role != 'admin' and restaurant.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail='Not allowed to manage this menu')
    item = BiryaniItem(restaurant_id=restaurant.id, **payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.patch('/menu/{item_id}', response_model=MenuItemOut)
def update_menu_item(
    item_id: str,
    payload: MenuItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = db.query(BiryaniItem).filter(BiryaniItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail='Menu item not found')
    restaurant = db.query(Restaurant).filter(Restaurant.id == item.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail='Restaurant not found')
    if current_user.role != 'admin' and restaurant.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail='Not allowed to modify this menu item')
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete('/menu/{item_id}')
def delete_menu_item(item_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = db.query(BiryaniItem).filter(BiryaniItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail='Menu item not found')
    restaurant = db.query(Restaurant).filter(Restaurant.id == item.restaurant_id).first()
    if current_user.role != 'admin' and restaurant and restaurant.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail='Not allowed to delete this menu item')
    db.delete(item)
    db.commit()
    return {'message': 'Menu item deleted'}
