from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models import Restaurant, Review, User
from app.schemas import ReviewCreate, ReviewOut

router = APIRouter(prefix='/api/v1', tags=['reviews'])


@router.post('/reviews', response_model=ReviewOut, status_code=201)
def create_review(payload: ReviewCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == payload.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail='Restaurant not found')
    review = Review(
        user_id=current_user.id,
        restaurant_id=payload.restaurant_id,
        item_id=payload.item_id,
        rating=payload.rating,
        comment=payload.comment,
        sentiment='positive' if payload.rating >= 4 else 'neutral' if payload.rating == 3 else 'negative',
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.get('/restaurants/{restaurant_id}/reviews', response_model=list[ReviewOut])
def list_restaurant_reviews(restaurant_id: str, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail='Restaurant not found')
    return db.query(Review).filter(Review.restaurant_id == restaurant_id).all()
