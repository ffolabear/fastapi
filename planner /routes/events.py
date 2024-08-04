from fastapi import APIRouter

event_router = APIRouter(
    tags=["Events"]
)

events = []
