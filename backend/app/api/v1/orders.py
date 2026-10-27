from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models import BiryaniItem, Cart, CartItem, Order, OrderItem, User
from app.schemas import OrderCreate, OrderOut

router = APIRouter(prefix='/api/v1', tags=['orders'])


@router.post('/orders', response_model=OrderOut, status_code=201)
def create_order(payload: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=400, detail='Cart is empty')
    cart_items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail='Cart is empty')

    subtotal = Decimal('0.00')
    order_items = []
    for cart_item in cart_items:
        item = db.query(BiryaniItem).filter(BiryaniItem.id == cart_item.item_id).first()
        if not item or not item.is_available:
            raise HTTPException(status_code=400, detail=f'Item {cart_item.item_id} is unavailable')
        line_total = item.price * cart_item.quantity
        subtotal += line_total
        order_items.append(OrderItem(item_id=item.id, quantity=cart_item.quantity, unit_price=item.price, total_price=line_total))

    order = Order(
        customer_id=current_user.id,
        restaurant_id=cart_items[0].biryani_item.restaurant_id,
        address_id=payload.address_id,
        subtotal=subtotal,
        tax_amount=Decimal('0.00'),
        delivery_charge=Decimal('0.00'),
        discount_amount=Decimal('0.00'),
        total_amount=subtotal,
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    for order_item in order_items:
        order_item.order_id = order.id
        db.add(order_item)
    db.commit()
    db.refresh(order)

    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()
    return order


@router.get('/orders', response_model=list[OrderOut])
def list_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role == 'admin':
        return db.query(Order).all()
    return db.query(Order).filter(Order.customer_id == current_user.id).all()


@router.get('/orders/{order_id}', response_model=OrderOut)
def get_order(order_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')
    if current_user.role != 'admin' and order.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail='Not allowed to access this order')
    return order


@router.post('/orders/{order_id}/cancel')
def cancel_order(order_id: str, reason: str | None = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')
    if current_user.role != 'admin' and order.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail='Not allowed to cancel this order')
    order.status = 'cancelled'
    order.cancellation_reason = reason or 'Customer requested cancellation'
    db.add(order)
    db.commit()
    return {'message': 'Order cancelled', 'order_id': order.id}
