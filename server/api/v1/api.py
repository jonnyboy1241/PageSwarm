"""Composition root for version 1 API routers."""

from fastapi import APIRouter

from api.v1.endpoints.documents import router as documents_router

api_router = APIRouter()
api_router.include_router(documents_router, tags=["documents"])
