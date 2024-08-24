from dataclasses import dataclass
from enum import Enum


class JobApiRequestType(Enum):
    ENGINEERING = '/engineering'
    SKILL_AREAS = '/skill-areas'


@dataclass(frozen=True)
class JobDescription:
    company_name: str
    title: str
    description: str
    link: str
