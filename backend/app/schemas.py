from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class TokenPayload(BaseModel):
    sub: str
    type: Optional[str] = None
    exp: Optional[datetime] = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=2)
    phone: Optional[str] = None
    role: str = 'customer'


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    email: str
    full_name: str
    phone: Optional[str]
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None


class AddressCreate(BaseModel):
    label: str
    address_line_1: str
    address_line_2: Optional[str] = None
    city: str
    state: str
    postal_code: str
    country: str = 'India'
    is_default: bool = False


class AddressOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    user_id: str
    label: str
    address_line_1: str
    address_line_2: Optional[str]
    city: str
    state: str
    postal_code: str
    country: str
    is_default: bool
    created_at: datetime
    updated_at: datetime


class RestaurantCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: str
    city: str
    state: str
    country: str = 'India'
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    is_active: Optional[bool] = None
    is_approved: Optional[bool] = None


class RestaurantOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    owner_id: str
    name: str
    slug: str
    description: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    address: str
    city: str
    state: str
    country: str
    latitude: Optional[float]
    longitude: Optional[float]
    logo_url: Optional[str]
    is_active: bool
    is_approved: bool
    average_rating: Decimal
    created_at: datetime
    updated_at: datetime


class MenuItemCreate(BaseModel):
    category: str
    name: str
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0)
    portion_size: str
    spice_level: str = 'medium'
    is_available: bool = True
    image_url: Optional[str] = None


class MenuItemUpdate(BaseModel):
    category: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = Field(default=None, gt=0)
    portion_size: Optional[str] = None
    spice_level: Optional[str] = None
    is_available: Optional[bool] = None
    image_url: Optional[str] = None


class MenuItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    restaurant_id: str
    category: str
    name: str
    description: Optional[str]
    price: Decimal
    portion_size: str
    spice_level: str
    is_available: bool
    image_url: Optional[str]
    rating: Decimal
    popularity_score: int
    created_at: datetime
    updated_at: datetime


class CartItemCreate(BaseModel):
    item_id: str
    quantity: int = Field(..., gt=0)


class CartItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0)


class CartItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    item_id: str
    quantity: int
    unit_price: Decimal
    created_at: datetime
    updated_at: datetime


class CartOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    user_id: str
    items: List[CartItemOut] = []
    total: Decimal = Decimal('0.00')


class OrderItemCreate(BaseModel):
    item_id: str
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    address_id: str
    items: List[OrderItemCreate]
    coupon_code: Optional[str] = None


class OrderItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    order_id: str
    item_id: str
    quantity: int
    unit_price: Decimal
    total_price: Decimal
    created_at: datetime


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    customer_id: str
    restaurant_id: str
    address_id: Optional[str]
    status: str
    payment_status: str
    subtotal: Decimal
    tax_amount: Decimal
    delivery_charge: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    cancellation_reason: Optional[str]
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemOut] = []


class PaymentCreate(BaseModel):
    order_id: str
    provider: str = 'simulated'


class PaymentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    order_id: str
    provider: str
    provider_payment_id: Optional[str]
    amount: Decimal
    status: str
    currency: str
    created_at: datetime
    updated_at: datetime


class ReviewCreate(BaseModel):
    restaurant_id: str
    item_id: Optional[str] = None
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class ReviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    user_id: str
    restaurant_id: str
    item_id: Optional[str]
    rating: int
    comment: Optional[str]
    sentiment: Optional[str]
    created_at: datetime
    updated_at: datetime
