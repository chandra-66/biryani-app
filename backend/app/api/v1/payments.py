from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.config import get_settings
from app.models import Order, Payment, PaymentEvent, User
from app.schemas import PaymentCreate, PaymentOut

router = APIRouter(prefix='/api/v1', tags=['payments'])
settings = get_settings()


@router.post('/payments/create', response_model=PaymentOut, status_code=status.HTTP_201_CREATED)
def create_payment(payload: PaymentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == payload.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')
    if order.customer_id != current_user.id and current_user.role != 'admin':
        raise HTTPException(status_code=403, detail='Not allowed to access this payment')
    payment = Payment(order_id=order.id, provider=payload.provider, amount=order.total_amount, status='pending')
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


@router.post('/payments/verify', response_model=PaymentOut)
def verify_payment(payload: PaymentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    payment = db.query(Payment).filter(Payment.order_id == payload.order_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail='Payment not found')
    if payment.order.customer_id != current_user.id and current_user.role != 'admin':
        raise HTTPException(status_code=403, detail='Not allowed to access this payment')
    if settings.simulated_payment_mode:
        payment.status = 'paid'
        db.add(PaymentEvent(payment_id=payment.id, event_type='payment_verified', payload='simulated'))
        db.commit()
        db.refresh(payment)
        return payment
    raise HTTPException(status_code=400, detail='External payment provider not configured')


@router.post('/payments/webhook')
async def payment_webhook(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    payment = db.query(Payment).filter(Payment.provider_payment_id == data.get('payment_id')).first()
    if payment:
        payment.status = 'paid'
        db.add(PaymentEvent(payment_id=payment.id, event_type='webhook_received', payload=str(data)))
        db.commit()
        return {'message': 'Webhook processed'}
    return {'message': 'No matching payment found'}
