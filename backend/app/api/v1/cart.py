from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models import BiryaniItem, Cart, CartItem, User
from app.schemas import CartItemCreate, CartItemOut, CartItemUpdate, CartOut

router = APIRouter(prefix='/api/v1', tags=['cart'])


@router.get('/cart', response_model=CartOut)
def get_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
    total = sum((item.unit_price * item.quantity) for item in items)
    return CartOut(id=cart.id, user_id=current_user.id, items=[CartItemOut.model_validate(item) for item in items], total=Decimal(str(total)))


@router.post('/cart/items', response_model=CartItemOut, status_code=201)
def add_item_to_cart(payload: CartItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = db.query(BiryaniItem).filter(BiryaniItem.id == payload.item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail='Item not found')
    if not item.is_available:
        raise HTTPException(status_code=400, detail='Item is not available')
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    existing = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.item_id == payload.item_id).first()
    if existing:
        existing.quantity += payload.quantity
        existing.unit_price = item.price
        db.add(existing)
        db.commit()
        db.refresh(existing)
        return existing
    cart_item = CartItem(cart_id=cart.id, item_id=item.id, quantity=payload.quantity, unit_price=item.price)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item


@router.patch('/cart/items/{item_id}', response_model=CartItemOut)
def update_cart_item(item_id: str, payload: CartItemUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail='Cart not found')
    cart_item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.id == item_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail='Cart item not found')
    cart_item.quantity = payload.quantity
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item


@router.delete('/cart/items/{item_id}')
def remove_cart_item(item_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail='Cart not found')
    cart_item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.id == item_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail='Cart item not found')
    db.delete(cart_item)
    db.commit()
    return {'message': 'Cart item removed'}
