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


# TODO: Should these values have a default value when they are optional?
@dataclass
class Story:

    name: str
    id: Optional[int] = None  # This does not exist when you create a story.
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
    comment_ids: Optional[List[int]] = None
    follower_ids: Optional[List[int]] = None
    owner_ids: Optional[List[int]] = None

    previous_iteration_ids: Optional[List[int]] = None

    mention_ids: Optional[List[int]] = None
    member_mention_ids: Optional[List[int]] = None
    label_ids: Optional[List[int]] = None
    task_ids: Optional[List[int]] = None
    file_ids: Optional[List[int]] = None

    linked_files: Optional[List[Dict[str, Any]]] = None
    linked_file_ids: Optional[List[int]] = None

    custom_fields: Optional[List[Dict[str, Any]]] = None
    num_tasks_completed: Optional[int] = None

    stats: Optional[Dict[str, Any]] = None
    lead_time: Optional[int] = None
    cycle_time: Optional[int] = None

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
    state: str = "to do"  # enum value
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
class EpicWorkflow:
    id: int

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "EpicWorkflow":
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})


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
    status: str = "unstarted"  # enum

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


@dataclass
class StoryLinkInput:
    object_id: int
    subject_id: int
    verb: str


@dataclass
class StoryLink:
    id: int
    object_id: int
    subject_id: int
    verb: str
    entity_type: str = "story-link"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "StoryLink":
        return cls(**data)


@dataclass
class CreateGroupInput:
    name: str
    mention_name: str


@dataclass
class UpdateGroupInput:
    name: Optional[str]


@dataclass
class Group:
    id: int
    global_id: str

    name: str
    entity_type: str = "group"

    mention_name: Optional[str] = None
    description: Optional[str] = None
    archived: Optional[bool] = None
    app_url: Optional[str] = None
    color: Optional[str] = None
    color_key: Optional[str] = None
    display_icon: Optional[Any] = None

    member_ids: Optional[List[str]] = None
    num_stories_started: Optional[int] = None
    num_stories: Optional[int] = None
    num_epics_started: Optional[int] = None
    num_stories_backlog: Optional[int] = None
    workflow_ids: Optional[List[int]] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Group":
        return cls(**data)


@dataclass
class KeyResultValue:
    boolean_value: bool
    numeric_value: str

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "KeyResultValue":
        return cls(**data)


@dataclass
class KeyResultInput:
    name: Optional[str] = None

    initial_observed_value: Optional[KeyResultValue] = None
    observed_value: Optional[KeyResultValue] = None
    target_value: Optional[KeyResultValue] = None


@dataclass
class KeyResult:
    id: int
    name: str
    current_observed_value: KeyResultValue
    current_target_value: KeyResultValue
    entity_type: str = "key"
    progress: Optional[int] = None
    objective_id: Optional[int] = None
    initial_observed_value: Optional[int] = None

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "KeyResult":
        return cls(**data)


@dataclass
class CreateLabelInput:
    name: str
    color: Optional[str]
    description: Optional[str]
    external_id: Optional[str]


@dataclass
class Label:
    id: int
    name: str
    global_id: str
    external_id: Optional[str]
    app_url: Optional[str] = None
    archived: bool = False
    color: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    description: Optional[str] = None
    entity_type: str = "label"
    stats: Any = None

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Label":
        return cls(**data)


@dataclass
class CreateLinkedFilesInput:
    name: str
    type: str  # enum
    url: str


@dataclass
class UpdatedLinkedFilesInput:
    name: Optional[str]
    type: Optional[str]
    url: Optional[str]
    uploader_id: Optional[str]


@dataclass
class LinkedFiles:
    id: int
    global_id: str
    name: Optional[str]

    content_type: Optional[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    description: Optional[str] = None
    entity_type: str = "linked-file"

    group_mention_ids: Optional[List[str]] = None
    member_mention_ids: Optional[List[str]] = None
    mention_ids: Optional[List[str]] = None

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "LinkedFiles":
        return cls(**data)


@dataclass
class CreateFileInput:
    name: str


@dataclass
class File:
    id: int
    name: str
    content_type: str
    created_at: datetime
    updated_at: datetime
    description: str
    uploader_id: str
    url: str
    size: int
    external_id: Optional[str]
    filename: str
    entity_type: str = "file"
    group_mention_ids: Optional[List[str]] = None
    member_mention_ids: Optional[List[str]] = None
    mention_ids: Optional[List[str]] = None
    story_link_id: Optional[int] = None
    story_ids: Optional[List[int]] = None
    thumbnail_url: Optional[str] = None

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "File":
        return cls(**data)


@dataclass
class Profile:
    id: str
    name: str
    mention_name: str
    gravatar_hash: str
    is_owner: bool
    email_address: str
    deactivated: bool

    display_icon: Any

    entity_type: str = "profile"
    two_factor_auth_activated: Optional[bool] = None

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Profile":
        return cls(**data)


@dataclass
class Member:
    id: str

    state: Optional[str] = None
    entity_type: str = "member"
    global_id: Optional[str] = None
    profile: Optional[Profile] = None
    role: Optional[str] = None
    disabled: Optional[bool] = None
    mention_name: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Member":

        if "profile" in data:
            data["profile"] = Profile.from_json(data["profile"])
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})


@dataclass
class CreateObjectiveInput:
    name: str


@dataclass
class UpdateObjectiveInput:
    name: Optional[str]


@dataclass
class Objective:
    id: int
    global_id: str

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Objective":
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})


@dataclass
class Repository:
    id: int

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Repository":
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})


@dataclass
class WorkflowState:
    id: int
    global_id: str
    name: str
    description: str
    verb: str
    num_stories: int
    num_story_templates: int
    position: int
    type: str  # Enum
    created_at: datetime
    updated_at: datetime
    entity_type: str = "workflow-state"
    color: Optional[str] = None

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "WorkflowState":
        return cls(**data)


@dataclass
class Workflow:
    id: int
    name: str
    description: str
    entity_type: str = "workflow"

    auto_assign_owner: Optional[bool] = None
    project_ids: Optional[List[int]] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    default_state_id: Optional[int] = None

    states: List[WorkflowState] = field(default_factory=list)

    team_id: Optional[int] = None

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Workflow":
        if "states" in data:
            data["states"] = [WorkflowState.from_json(x) for x in data["states"]]
        return cls(**data)


@dataclass
class CreateCategoryInput:
    name: str


@dataclass
class UpdateCategoryInput:
    name: Optional[str]


@dataclass
class Category:
    id: int
    global_id: str
    type: str
    archived: bool
    color: str
    created_at: datetime
    updated_at: datetime
    name: str

    external_id: Optional[str] = None
    entity_type: str = "category"

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Category":
        return cls(**data)


@dataclass
class CreateProjectInput:
    name: str


@dataclass
class UpdateProjectInput:
    name: Optional[str]


@dataclass
class Project:
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Project":
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})


@dataclass
class SearchInputs:
    query: Any
    detail: str = "slim"
    page_size: int = 25


@dataclass
class SearchStoryResult:
    data: List[Story]
    total: int
    next: Optional[str] = None

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "SearchStoryResult":
        if "data" in data:
            data["data"] = [Story.from_json(x) for x in data["data"]]
        return cls(**data)
