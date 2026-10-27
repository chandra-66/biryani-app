from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.security import create_access_token, create_refresh_token, hash_password, verify_password
from app.models import AuditLog, User
from app.schemas import TokenResponse, UserCreate, UserLogin, UserOut

router = APIRouter(prefix='/api/v1/auth', tags=['auth'])


@router.post('/register', response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == payload.email.lower()).first()
    if existing_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    user = User(
        email=payload.email.lower(),
        password_hash=hash_password(payload.password),
        full_name=payload.full_name,
        phone=payload.phone,
        role=payload.role.lower(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    db.add(AuditLog(user_id=user.id, action='user_registered', entity_type='users', entity_id=user.id, details='New user registered'))
    db.commit()
    return user


@router.post('/login', response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    if not user.is_active:
        raise HTTPException(status_code=403, detail='Account disabled')
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post('/logout')
def logout(current_user: User = Depends(get_current_user)):
    return {'message': f'User {current_user.email} logged out successfully'}


@router.post('/refresh', response_model=TokenResponse)
def refresh_token(token: str, db: Session = Depends(get_db)):
    from app.core.security import decode_token

    payload = decode_token(token)
    if payload.get('type') != 'refresh':
        raise HTTPException(status_code=401, detail='Invalid refresh token')
    user = db.query(User).filter(User.id == payload.get('sub')).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return TokenResponse(access_token=create_access_token(user.id), refresh_token=create_refresh_token(user.id))
