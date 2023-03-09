import uuid
from datetime import date

from pydantic import NonNegativeInt, root_validator

from apps.schedule.domain.constants import AvailabilityType, PeriodicityType
from apps.schedule.domain.schedule import BaseEvent, BasePeriodicity
from apps.shared.domain import PublicModel

__all__ = [
    "PublicPeriodicity",
    "PublicEvent",
    "ActivityEventCount",
    "FlowEventCount",
    "PublicEventCount",
    "PublicEventByUser",
    "HourMinute",
    "TimerDto",
    "EventAvailabilityDto",
    "ScheduleEventDto",
]


class PublicPeriodicity(PublicModel, BasePeriodicity):
    pass


class PublicEvent(PublicModel, BaseEvent):
    id: uuid.UUID
    periodicity: PublicPeriodicity
    user_id: uuid.UUID | None
    activity_id: uuid.UUID | None
    flow_id: uuid.UUID | None


class ActivityEventCount(PublicModel):
    count: int
    activity_id: uuid.UUID
    activity_name: str


class FlowEventCount(PublicModel):
    count: int
    flow_id: uuid.UUID
    flow_name: str


class PublicEventCount(PublicModel):
    activity_events: list[ActivityEventCount] | None
    flow_events: list[FlowEventCount] | None


class HourMinute(PublicModel):
    hours: NonNegativeInt
    minutes: NonNegativeInt

    @root_validator
    def validate_hour_minute(cls, values):
        if values.get("hours") > 23:
            raise ValueError("Hours must be between 0 and 23")
        if values.get("minutes") > 59:
            raise ValueError("Minutes must be between 0 and 59")
        return values


class TimerDto(PublicModel):
    timer: HourMinute | None
    idleTimer: HourMinute | None


class EventAvailabilityDto(PublicModel):
    oneTimeCompletion: bool
    periodicityType: PeriodicityType
    timeFrom: HourMinute | None
    timeTo: HourMinute | None
    allowAccessBeforeFromTime: bool
    startDate: date | None
    endDate: date | None


class ScheduleEventDto(PublicModel):
    id: uuid.UUID
    entityId: uuid.UUID
    availability: EventAvailabilityDto
    timers: TimerDto
    availabilityType: AvailabilityType


class PublicEventByUser(PublicModel):
    applet_id: uuid.UUID
    events: list[ScheduleEventDto] | None
