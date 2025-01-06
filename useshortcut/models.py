from calendar import day_abbr
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Label:
    id: int
    external_id: Optional[str]

    name: str
    archived: bool
    color: str
    created_at: datetime
    updated_at: datetime
    stats: Any

    entity_type: str = "label"
    app_url: Optional[str] = None


@dataclass
class StoryInput:
    name: str
    workflow_state_id: int

## TODO, Should these values have a default value when they are optional?
@dataclass
class Story:

    name: str
    id: Optional[int] = None  ### This does not exist when you create a story.
    global_id: Optional[str] = None
    external_id: Optional[str] = None

    deadline: Optional[datetime] = None
    description: Optional[str] = None
    story_type: str = "feature"
    estimate: Optional[str] = None
    group_id: Optional[str] = None
    story_template_id: Optional[str] = None
    workflow_state_id: Optional[int] = None
    project_id: Optional[int] = None
    requested_by_id: Optional[str] = None
    workflow_id: Optional[int] = None
    epic_id: Optional[int] = None
    iteration_id: Optional[int] = None
    labels: List[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    app_url: Optional[str] = None

    archived: Optional[bool] = None
    started: Optional[bool] = None
    completed: Optional[bool] = None
    blocker: Optional[bool] = None

    moved_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    completed_at_override: Optional[datetime] = None
    started_at: Optional[datetime] = None
    started_at_override: Optional[datetime] = None
    position: Optional[int] = None

    blocked: Optional[bool] = None

    pull_requests: Optional[List[Dict[str, Any]]] = None
    story_links: Optional[List[Dict[str, Any]]] = None
    comments: Optional[List[Dict[str, Any]]] = None
    branches: Optional[List[Dict[str, Any]]] = None
    tasks: Optional[List[Dict[str, Any]]] = None
    commits: Optional[List[Dict[str, Any]]] = None
    files: Optional[List[Dict[str, Any]]] = None
    external_links: Optional[List[Dict[str, Any]]] = None

    group_mention_ids: Optional[List[int]] = None
    follower_ids: Optional[List[int]] = None
    owner_ids: Optional[List[int]] = None

    previous_iteration_ids: Optional[List[int]] = None

    mention_ids: Optional[List[int]] = None
    member_mention_ids: Optional[List[int]] = None
    label_ids: Optional[List[int]] = None

    linked_files: Optional[List[Dict[str, Any]]] = None

    custom_fields: Optional[List[Dict[str, Any]]] = None

    stats: Optional[Dict[str, Any]] = None
    entity_type: str = "story"

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Story":
        return cls(**data)

@dataclass
class EpicInput:
    name: str

@dataclass
class Epic:
    id: int
    global_id: str
    name: str

    archived: Optional[bool] = None
    description: Optional[str] = None
    state: str = "to do" ## enum value
    group_id: str = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deadline: Optional[datetime] = None
    started: Optional[bool] = None
    started_at: Optional[datetime] = None
    requested_by_id: Optional[str] = None
    productboard_id: Optional[str] = None
    productboard_plugin_id: Optional[str] = None
    productboard_url: Optional[str] = None
    productboard_name: Optional[str] = None
    completed: Optional[bool] = None
    completed_at: Optional[datetime] = None
    completed_at_override: Optional[datetime] = None
    objective_ids: Optional[List[str]] = None
    planned_start_date: Optional[datetime] = None
    started_at_override: Optional[datetime] = None
    milestone_id: Optional[int] = None
    epic_state_id: Optional[int] = None
    app_url: Optional[str] = None
    entity_type: str = "epic"
    group_mention_ids: Optional[List[str]] = None
    follower_ids: Optional[List[str]] = None
    labels: Optional[List[Dict[str, Any]]] = None
    label_ids: Optional[List[int]] = None
    group_ids: Optional[List[str]] = None
    owner_ids: Optional[List[str]] = None
    external_id: Optional[str] = None
    position: int = None

    stories_without_projects: Optional[Any] = None

    project_ids: Optional[List[int]] = None
    mention_ids: Optional[List[str]] = None
    member_mention_ids: Optional[List[str]] = None
    associated_groups: Optional[List[Dict[str, Any]]] = None
    stats: Any = None

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Epic":
        return cls(**data)


@dataclass
class CreateIterationInput:
    name: str
    start_date: str
    end_date: str

@dataclass
class UpdateIterationInput:
    name: Optional[str]

@dataclass
class Iteration:
    id: int
    name: str
    global_id: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: str = "unstarted" ### enum

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    app_url: Optional[str] = None
    labels: Optional[List[Dict[str, Any]]] = None
    follower_ids: Optional[List[str]] = None
    group_ids: Optional[List[str]] = None
    mention_ids: Optional[List[str]] = None
    member_mention_ids: Optional[List[str]] = None
    group_mention_ids: Optional[List[str]] = None
    label_ids: Optional[List[int]] = None

    associated_groups: Optional[List[Dict[str, Any]]] = None

    entity_type: str = "iteration"
    stats: Any = None

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Iteration":
        return cls(**data)