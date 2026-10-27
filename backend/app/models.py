from __future__ import annotations

import uuid
from datetime import datetime, timezone
from decimal import Decimal as PyDecimal
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    role: Mapped[str] = mapped_column(String(32), default='customer', nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    addresses = relationship('UserAddress', back_populates='user', cascade='all, delete-orphan')
    restaurants = relationship('Restaurant', back_populates='owner', cascade='all, delete-orphan')
    cart = relationship('Cart', back_populates='user', uselist=False, cascade='all, delete-orphan')
    orders = relationship('Order', back_populates='customer', cascade='all, delete-orphan')
    reviews = relationship('Review', back_populates='user', cascade='all, delete-orphan')
    favorites = relationship('Favorite', back_populates='user', cascade='all, delete-orphan')
    notifications = relationship('Notification', back_populates='user', cascade='all, delete-orphan')
    preferences = relationship('UserPreference', back_populates='user', cascade='all, delete-orphan')
    audit_logs = relationship('AuditLog', back_populates='user', cascade='all, delete-orphan')


class UserAddress(Base):
    __tablename__ = 'user_addresses'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    label: Mapped[str] = mapped_column(String(100), nullable=False)
    address_line_1: Mapped[str] = mapped_column(String(255), nullable=False)
    address_line_2: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(20), nullable=False)
    country: Mapped[str] = mapped_column(String(100), default='India', nullable=False)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)
    user = relationship('User', back_populates='addresses')


class Restaurant(Base):
    __tablename__ = 'restaurants'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), default='India', nullable=False)
    latitude: Mapped[Optional[float]] = mapped_column(Numeric(10, 7), nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Numeric(10, 7), nullable=True)
    logo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    average_rating: Mapped[float] = mapped_column(Numeric(3, 2), default=0.0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    owner = relationship('User', back_populates='restaurants')
    categories = relationship('RestaurantCategory', back_populates='restaurant', cascade='all, delete-orphan')
    hours = relationship('RestaurantHour', back_populates='restaurant', cascade='all, delete-orphan')
    menu_items = relationship('BiryaniItem', back_populates='restaurant', cascade='all, delete-orphan')
    reviews = relationship('Review', back_populates='restaurant', cascade='all, delete-orphan')
    favorites = relationship('Favorite', back_populates='restaurant', cascade='all, delete-orphan')


class RestaurantHour(Base):
    __tablename__ = 'restaurant_hours'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    restaurant_id: Mapped[str] = mapped_column(ForeignKey('restaurants.id', ondelete='CASCADE'), nullable=False)
    day_of_week: Mapped[int] = mapped_column(Integer, nullable=False)
    open_time: Mapped[str] = mapped_column(String(10), nullable=False)
    close_time: Mapped[str] = mapped_column(String(10), nullable=False)
    is_closed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)
    restaurant = relationship('Restaurant', back_populates='hours')


class RestaurantCategory(Base):
    __tablename__ = 'restaurant_categories'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    restaurant_id: Mapped[str] = mapped_column(ForeignKey('restaurants.id', ondelete='CASCADE'), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    restaurant = relationship('Restaurant', back_populates='categories')


class MenuCategory(Base):
    __tablename__ = 'menu_categories'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    restaurant_id: Mapped[str] = mapped_column(ForeignKey('restaurants.id', ondelete='CASCADE'), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)


class BiryaniItem(Base):
    __tablename__ = 'biryani_items'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    restaurant_id: Mapped[str] = mapped_column(ForeignKey('restaurants.id', ondelete='CASCADE'), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price: Mapped[PyDecimal] = mapped_column(Numeric(10, 2), nullable=False)
    portion_size: Mapped[str] = mapped_column(String(50), nullable=False)
    spice_level: Mapped[str] = mapped_column(String(20), default='medium', nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    rating: Mapped[float] = mapped_column(Numeric(3, 2), default=0.0, nullable=False)
    popularity_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    restaurant = relationship('Restaurant', back_populates='menu_items')
    customizations = relationship('ItemCustomization', back_populates='item', cascade='all, delete-orphan')
    cart_items = relationship('CartItem', back_populates='biryani_item', cascade='all, delete-orphan')
    order_items = relationship('OrderItem', back_populates='biryani_item', cascade='all, delete-orphan')
    reviews = relationship('Review', back_populates='biryani_item', cascade='all, delete-orphan')


class ItemCustomization(Base):
    __tablename__ = 'item_customizations'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    item_id: Mapped[str] = mapped_column(ForeignKey('biryani_items.id', ondelete='CASCADE'), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price_delta: Mapped[PyDecimal] = mapped_column(Numeric(10, 2), default=0.00, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    item = relationship('BiryaniItem', back_populates='customizations')


class Cart(Base):
    __tablename__ = 'carts'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)
    user = relationship('User', back_populates='cart')
    items = relationship('CartItem', back_populates='cart', cascade='all, delete-orphan')


class CartItem(Base):
    __tablename__ = 'cart_items'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    cart_id: Mapped[str] = mapped_column(ForeignKey('carts.id', ondelete='CASCADE'), nullable=False)
    item_id: Mapped[str] = mapped_column(ForeignKey('biryani_items.id', ondelete='CASCADE'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    unit_price: Mapped[PyDecimal] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)
    cart = relationship('Cart', back_populates='items')
    biryani_item = relationship('BiryaniItem', back_populates='cart_items')


class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    restaurant_id: Mapped[str] = mapped_column(ForeignKey('restaurants.id', ondelete='CASCADE'), nullable=False)
    address_id: Mapped[Optional[str]] = mapped_column(ForeignKey('user_addresses.id', ondelete='SET NULL'), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default='pending', nullable=False)
    payment_status: Mapped[str] = mapped_column(String(32), default='pending', nullable=False)
    subtotal: Mapped[PyDecimal] = mapped_column(Numeric(10, 2), default=0.00, nullable=False)
    tax_amount: Mapped[PyDecimal] = mapped_column(Numeric(10, 2), default=0.00, nullable=False)
    delivery_charge: Mapped[PyDecimal] = mapped_column(Numeric(10, 2), default=0.00, nullable=False)
    discount_amount: Mapped[PyDecimal] = mapped_column(Numeric(10, 2), default=0.00, nullable=False)
    total_amount: Mapped[PyDecimal] = mapped_column(Numeric(10, 2), default=0.00, nullable=False)
    cancellation_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)
    customer = relationship('User', back_populates='orders')
    restaurant = relationship('Restaurant')
    address = relationship('UserAddress')
    items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')
    payments = relationship('Payment', back_populates='order', cascade='all, delete-orphan')


class OrderItem(Base):
    __tablename__ = 'order_items'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id: Mapped[str] = mapped_column(ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    item_id: Mapped[str] = mapped_column(ForeignKey('biryani_items.id', ondelete='CASCADE'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[PyDecimal] = mapped_column(Numeric(10, 2), nullable=False)
    total_price: Mapped[PyDecimal] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    order = relationship('Order', back_populates='items')
    biryani_item = relationship('BiryaniItem', back_populates='order_items')


class Payment(Base):
    __tablename__ = 'payments'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id: Mapped[str] = mapped_column(ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    provider: Mapped[str] = mapped_column(String(50), default='simulated', nullable=False)
    provider_payment_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    amount: Mapped[PyDecimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default='pending', nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default='INR', nullable=False)
    raw_payload: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)
    order = relationship('Order', back_populates='payments')
    events = relationship('PaymentEvent', back_populates='payment', cascade='all, delete-orphan')


class PaymentEvent(Base):
    __tablename__ = 'payment_events'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    payment_id: Mapped[str] = mapped_column(ForeignKey('payments.id', ondelete='CASCADE'), nullable=False)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    payload: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    payment = relationship('Payment', back_populates='events')


class Review(Base):
    __tablename__ = 'reviews'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    restaurant_id: Mapped[str] = mapped_column(ForeignKey('restaurants.id', ondelete='CASCADE'), nullable=False)
    item_id: Mapped[Optional[str]] = mapped_column(ForeignKey('biryani_items.id', ondelete='SET NULL'), nullable=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sentiment: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)
    user = relationship('User', back_populates='reviews')
    restaurant = relationship('Restaurant', back_populates='reviews')
    biryani_item = relationship('BiryaniItem', back_populates='reviews')


class Favorite(Base):
    __tablename__ = 'favorites'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    restaurant_id: Mapped[Optional[str]] = mapped_column(ForeignKey('restaurants.id', ondelete='CASCADE'), nullable=True)
    item_id: Mapped[Optional[str]] = mapped_column(ForeignKey('biryani_items.id', ondelete='CASCADE'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    user = relationship('User', back_populates='favorites')
    restaurant = relationship('Restaurant', back_populates='favorites')


class Coupon(Base):
    __tablename__ = 'coupons'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    discount_percent: Mapped[PyDecimal] = mapped_column(Numeric(5, 2), default=0.00, nullable=False)
    max_discount_amount: Mapped[PyDecimal] = mapped_column(Numeric(10, 2), default=0.00, nullable=False)
    min_order_amount: Mapped[PyDecimal] = mapped_column(Numeric(10, 2), default=0.00, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    valid_to: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)


class CouponRedemption(Base):
    __tablename__ = 'coupon_redemptions'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    coupon_id: Mapped[str] = mapped_column(ForeignKey('coupons.id', ondelete='CASCADE'), nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    order_id: Mapped[Optional[str]] = mapped_column(ForeignKey('orders.id', ondelete='SET NULL'), nullable=True)
    redeemed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)


class UserPreference(Base):
    __tablename__ = 'user_preferences'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    key: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)
    user = relationship('User', back_populates='preferences')


class Notification(Base):
    __tablename__ = 'notifications'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    user = relationship('User', back_populates='notifications')


class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[Optional[str]] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    user = relationship('User', back_populates='audit_logs')
