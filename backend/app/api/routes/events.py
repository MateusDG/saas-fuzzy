from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...database import get_db
from ...schemas import EventIn, EventResponse
from ...services.event_service import create_event


router = APIRouter()


@router.post("/events", response_model=EventResponse)
def create_event_route(event: EventIn, db: Session = Depends(get_db)) -> EventResponse:
    return create_event(event, db)
