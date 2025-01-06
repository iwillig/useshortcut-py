from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Story:
    id: int
    name: str
    description: Optional[str] = None
    story_type: str = "feature"
    workflow_state_id: Optional[int] = None
    epic_id: Optional[int] = None
    iteration_id: Optional[int] = None
    labels: List[Dict[str, Any]] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Story":
        return cls(**data)


@dataclass
class Epic:
    id: int
    name: str
    description: Optional[str] = None
    state: str = "to do" ## enum value
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Epic":
        return cls(**data)


@dataclass
class Iteration:
    id: int
    name: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: str = "unstarted" ### enum
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Iteration":
        return cls(**data)