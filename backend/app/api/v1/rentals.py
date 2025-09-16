from fastapi import APIRouter, Depends, HTTPException, Query, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db.session import AsyncSessionLocal
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

router = APIRouter(prefix="/rents", tags=["rentals"])