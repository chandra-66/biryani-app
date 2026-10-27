from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models import AuditLog, User, UserAddress
from app.schemas import AddressCreate, AddressOut, UserUpdate, UserOut

router = APIRouter(prefix='/api/v1/users', tags=['users'])


@router.get('/me', response_model=UserOut)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch('/me', response_model=UserOut)
def update_current_user_profile(payload: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if payload.full_name is not None:
        current_user.full_name = payload.full_name
    if payload.phone is not None:
        current_user.phone = payload.phone
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    db.add(AuditLog(user_id=current_user.id, action='profile_updated', entity_type='users', entity_id=current_user.id, details='Updated user profile'))
    db.commit()
    return current_user


@router.get('/me/addresses', response_model=list[AddressOut])
def list_user_addresses(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(UserAddress).filter(UserAddress.user_id == current_user.id).order_by(UserAddress.created_at.desc()).all()


@router.post('/me/addresses', response_model=AddressOut, status_code=status.HTTP_201_CREATED)
def create_user_address(payload: AddressCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if payload.is_default:
        db.query(UserAddress).filter(UserAddress.user_id == current_user.id).update({'is_default': False})

    address = UserAddress(user_id=current_user.id, **payload.model_dump())
    db.add(address)
    db.commit()
    db.refresh(address)
    return address
