from typing import Optional, List, Dict, Any, TypeVar, Generic
from dataclasses import dataclass, field
from datetime import datetime

T = TypeVar("T")


@dataclass
class StoryInput:
    name: str
    workflow_state_id: int
    description: Optional[str] = None
    story_type: Optional[str] = "feature"
    project_id: Optional[int] = None
    epic_id: Optional[int] = None
    label_ids: Optional[List[int]] = None


@dataclass
class UpdateStoryInput:
    name: Optional[str] = None
    description: Optional[str] = None
    workflow_state_id: Optional[int] = None
    story_type: Optional[str] = None
    project_id: Optional[int] = None
    epic_id: Optional[int] = None
    label_ids: Optional[List[int]] = None
    owner_ids: Optional[List[str]] = None
    follower_ids: Optional[List[str]] = None
    archived: Optional[bool] = None
    deadline: Optional[datetime] = None
    estimate: Optional[int] = None
    requested_by_id: Optional[str] = None
    iteration_id: Optional[int] = None
    completed_at_override: Optional[datetime] = None
    started_at_override: Optional[datetime] = None
    group_id: Optional[str] = None
    before_id: Optional[int] = None
    after_id: Optional[int] = None


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
    labels: List[Dict[str, Any]] = field(default_factory=list)
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

    pull_requests: Optional[List[Dict[str, Any]]] = field(default_factory=list)
    story_links: Optional[List[Dict[str, Any]]] = field(default_factory=list)
    comments: Optional[List[Dict[str, Any]]] = field(default_factory=list)
    branches: Optional[List[Dict[str, Any]]] = field(default_factory=list)
    tasks: Optional[List[Dict[str, Any]]] = field(default_factory=list)
    commits: Optional[List[Dict[str, Any]]] = field(default_factory=list)
    files: Optional[List[Dict[str, Any]]] = field(default_factory=list)
    external_links: Optional[List[Dict[str, Any]]] = field(default_factory=list)

    group_mention_ids: Optional[List[int]] = field(default_factory=list)
    comment_ids: Optional[List[int]] = field(default_factory=list)
    follower_ids: Optional[List[int]] = field(default_factory=list)
    owner_ids: Optional[List[int]] = field(default_factory=list)

    previous_iteration_ids: Optional[List[int]] = field(default_factory=list)

    mention_ids: Optional[List[int]] = field(default_factory=list)
    member_mention_ids: Optional[List[int]] = field(default_factory=list)
    label_ids: Optional[List[int]] = field(default_factory=list)
    task_ids: Optional[List[int]] = field(default_factory=list)
    file_ids: Optional[List[int]] = field(default_factory=list)

    linked_files: Optional[List[Dict[str, Any]]] = field(default_factory=list)
    linked_file_ids: Optional[List[int]] = field(default_factory=list)

    custom_fields: Optional[List[Dict[str, Any]]] = field(default_factory=list)
    num_tasks_completed: Optional[int] = None

    stats: Optional[Dict[str, Any]] = None
    lead_time: Optional[int] = None
    cycle_time: Optional[int] = None
    formatted_vcs_branch_name: Optional[str] = None

    entity_type: str = "story"

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Story":
        # Convert datetime strings
        date_fields = [
            "created_at",
            "updated_at",
            "deadline",
            "moved_at",
            "completed_at",
            "completed_at_override",
            "started_at",
            "started_at_override",
        ]
        for field in date_fields:
            if field in data and isinstance(data[field], str):
                data[field] = datetime.fromisoformat(data[field].replace("Z", "+00:00"))
        return cls(**data)


@dataclass
class Task:
    """A Task on a Story."""

    id: int
    description: str
    complete: bool
    story_id: int
    entity_type: str
    position: int
    created_at: datetime

    completed_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    external_id: Optional[str] = None
    global_id: Optional[str] = None

    owner_ids: List[str] = field(default_factory=list)
    mention_ids: List[str] = field(default_factory=list)  # Deprecated
    member_mention_ids: List[str] = field(default_factory=list)
    group_mention_ids: List[str] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Task":
        # Convert datetime strings
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(
                data["created_at"].replace("Z", "+00:00")
            )
        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(
                data["updated_at"].replace("Z", "+00:00")
            )
        if "completed_at" in data and isinstance(data["completed_at"], str):
            data["completed_at"] = datetime.fromisoformat(
                data["completed_at"].replace("Z", "+00:00")
            )

        return cls(**data)


@dataclass
class CreateTaskInput:
    """Request parameters for creating a Task on a Story."""

    description: str
    complete: bool = False
    owner_ids: List[str] = field(default_factory=list)
    external_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class UpdateTaskInput:
    """Request parameters for updating a Task."""

    description: Optional[str] = None
    owner_ids: Optional[List[str]] = None
    complete: Optional[bool] = None
    before_id: Optional[int] = None
    after_id: Optional[int] = None


@dataclass
class CreateEpicInput:
    name: str
    description: Optional[str] = None
    state: Optional[str] = "to do"
    milestone_id: Optional[int] = None
    requested_by_id: Optional[str] = None
    group_id: Optional[str] = None
    owner_ids: Optional[List[str]] = None
    follower_ids: Optional[List[str]] = None
    label_ids: Optional[List[int]] = None
    planned_start_date: Optional[datetime] = None
    deadline: Optional[datetime] = None


@dataclass
class UpdateEpicInput:
    name: Optional[str] = None
    description: Optional[str] = None
    state: Optional[str] = None
    milestone_id: Optional[int] = None
    requested_by_id: Optional[str] = None
    group_id: Optional[str] = None
    owner_ids: Optional[List[str]] = None
    follower_ids: Optional[List[str]] = None
    label_ids: Optional[List[int]] = None
    planned_start_date: Optional[datetime] = None
    deadline: Optional[datetime] = None
    archived: Optional[bool] = None
    before_id: Optional[int] = None
    after_id: Optional[int] = None


# Alias for backward compatibility
EpicInput = CreateEpicInput


@dataclass
class Epic:
    id: int
    global_id: str
    name: str

    archived: Optional[bool] = None
    description: Optional[str] = None
    state: str = "to do"  # enum value
    group_id: Optional[str] = None
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
    objective_ids: Optional[List[str]] = field(default_factory=list)
    planned_start_date: Optional[datetime] = None
    started_at_override: Optional[datetime] = None
    milestone_id: Optional[int] = None
    epic_state_id: Optional[int] = None
    app_url: Optional[str] = None
    entity_type: str = "epic"
    group_mention_ids: Optional[List[str]] = field(default_factory=list)
    follower_ids: Optional[List[str]] = field(default_factory=list)
    labels: Optional[List[Dict[str, Any]]] = field(default_factory=list)
    label_ids: Optional[List[int]] = field(default_factory=list)
    group_ids: Optional[List[str]] = field(default_factory=list)
    owner_ids: Optional[List[str]] = field(default_factory=list)
    external_id: Optional[str] = None
    position: Optional[int] = None

    stories_without_projects: Optional[Any] = None

    project_ids: Optional[List[int]] = field(default_factory=list)
    mention_ids: Optional[List[str]] = field(default_factory=list)
    member_mention_ids: Optional[List[str]] = field(default_factory=list)
    associated_groups: Optional[List[Dict[str, Any]]] = field(default_factory=list)
    comments: Optional[List[Dict[str, Any]]] = field(default_factory=list)
    stats: Optional[Any] = None

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Epic":
        # Convert datetime strings
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(
                data["created_at"].replace("Z", "+00:00")
            )
        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(
                data["updated_at"].replace("Z", "+00:00")
            )
        if "deadline" in data and isinstance(data["deadline"], str):
            data["deadline"] = datetime.fromisoformat(
                data["deadline"].replace("Z", "+00:00")
            )
        if "started_at" in data and isinstance(data["started_at"], str):
            data["started_at"] = datetime.fromisoformat(
                data["started_at"].replace("Z", "+00:00")
            )
        if "completed_at" in data and isinstance(data["completed_at"], str):
            data["completed_at"] = datetime.fromisoformat(
                data["completed_at"].replace("Z", "+00:00")
            )
        if "completed_at_override" in data and isinstance(
            data["completed_at_override"], str
        ):
            data["completed_at_override"] = datetime.fromisoformat(
                data["completed_at_override"].replace("Z", "+00:00")
            )
        if "started_at_override" in data and isinstance(
            data["started_at_override"], str
        ):
            data["started_at_override"] = datetime.fromisoformat(
                data["started_at_override"].replace("Z", "+00:00")
            )
        if "planned_start_date" in data and isinstance(data["planned_start_date"], str):
            data["planned_start_date"] = datetime.fromisoformat(
                data["planned_start_date"].replace("Z", "+00:00")
            )
        return cls(**data)


@dataclass
class EpicWorkflow:
    id: int
    default_epic_state_id: int
    epic_states: List[Dict[str, Any]]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    entity_type: str = "epic-workflow"

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "EpicWorkflow":
        # Convert datetime strings
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(
                data["created_at"].replace("Z", "+00:00")
            )
        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(
                data["updated_at"].replace("Z", "+00:00")
            )
        return cls(**data)


@dataclass
class CreateIterationInput:
    name: str
    start_date: str
    end_date: str
    description: Optional[str] = None
    follower_ids: Optional[List[str]] = None
    group_ids: Optional[List[str]] = None
    label_ids: Optional[List[int]] = None


@dataclass
class UpdateIterationInput:
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    follower_ids: Optional[List[str]] = None
    group_ids: Optional[List[str]] = None
    label_ids: Optional[List[int]] = None


@dataclass
class Iteration:
    id: int
    name: str
    global_id: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: str = "unstarted"  # enum
    description: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    app_url: Optional[str] = None
    labels: Optional[List[Dict[str, Any]]] = field(default_factory=list)
    follower_ids: Optional[List[str]] = field(default_factory=list)
    group_ids: Optional[List[str]] = field(default_factory=list)
    mention_ids: Optional[List[str]] = field(default_factory=list)
    member_mention_ids: Optional[List[str]] = field(default_factory=list)
    group_mention_ids: Optional[List[str]] = field(default_factory=list)
    label_ids: Optional[List[int]] = field(default_factory=list)

    associated_groups: Optional[List[Dict[str, Any]]] = field(default_factory=list)

    entity_type: str = "iteration"
    stats: Optional[Any] = None

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Iteration":
        # Convert datetime strings
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(
                data["created_at"].replace("Z", "+00:00")
            )
        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(
                data["updated_at"].replace("Z", "+00:00")
            )
        if "start_date" in data and isinstance(data["start_date"], str):
            data["start_date"] = datetime.fromisoformat(
                data["start_date"].replace("Z", "+00:00")
            )
        if "end_date" in data and isinstance(data["end_date"], str):
            data["end_date"] = datetime.fromisoformat(
                data["end_date"].replace("Z", "+00:00")
            )
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
    name: Optional[str] = None


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

    member_ids: Optional[List[str]] = field(default_factory=list)
    num_stories_started: Optional[int] = None
    num_stories: Optional[int] = None
    num_epics_started: Optional[int] = None
    num_stories_backlog: Optional[int] = None
    workflow_ids: Optional[List[int]] = field(default_factory=list)
    default_workflow_id: Optional[int] = None

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
    color: Optional[str] = None
    description: Optional[str] = None
    external_id: Optional[str] = None


@dataclass
class UpdateLabelInput:
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    archived: Optional[bool] = None


@dataclass
class Label:
    id: int
    name: str
    global_id: str
    external_id: Optional[str] = None
    app_url: Optional[str] = None
    archived: bool = False
    color: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    description: Optional[str] = None
    entity_type: str = "label"
    stats: Optional[Any] = None

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Label":
        # Convert datetime strings
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(
                data["created_at"].replace("Z", "+00:00")
            )
        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(
                data["updated_at"].replace("Z", "+00:00")
            )
        return cls(**data)


@dataclass
class CreateLinkedFilesInput:
    name: str
    type: str  # enum
    url: str


@dataclass
class UpdatedLinkedFilesInput:
    name: Optional[str] = None
    type: Optional[str] = None
    url: Optional[str] = None
    uploader_id: Optional[str] = None


@dataclass
class LinkedFiles:
    id: int
    global_id: str
    name: Optional[str] = None

    content_type: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    description: Optional[str] = None
    entity_type: str = "linked-file"

    group_mention_ids: Optional[List[str]] = field(default_factory=list)
    member_mention_ids: Optional[List[str]] = field(default_factory=list)
    mention_ids: Optional[List[str]] = field(default_factory=list)

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
    filename: str
    entity_type: str = "file"
    external_id: Optional[str] = None
    group_mention_ids: Optional[List[str]] = field(default_factory=list)
    member_mention_ids: Optional[List[str]] = field(default_factory=list)
    mention_ids: Optional[List[str]] = field(default_factory=list)
    story_link_id: Optional[int] = None
    story_ids: Optional[List[int]] = field(default_factory=list)
    thumbnail_url: Optional[str] = None

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "File":
        return cls(**data)


@dataclass
class Profile:
    id: str
    name: str
    mention_name: str
    is_owner: bool
    email_address: str
    deactivated: bool

    gravatar_hash: Optional[str] = None
    display_icon: Optional[Any] = None
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
    name: Optional[str] = None


@dataclass
class Objective:
    id: int
    global_id: str
    name: Optional[str] = None
    description: Optional[str] = None
    archived: Optional[bool] = None
    started: Optional[bool] = None
    completed: Optional[bool] = None
    entity_type: str = "objective"
    app_url: Optional[str] = None
    position: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    started_at_override: Optional[datetime] = None
    completed_at_override: Optional[datetime] = None
    state: Optional[str] = None
    stats: Optional[Any] = None

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Objective":
        return cls(**data)


@dataclass
class Repository:
    type: str
    id: Optional[int] = None
    name: Optional[str] = None
    entity_type: str = "repository"
    url: Optional[str] = None
    full_name: Optional[str] = None
    external_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Repository":
        return cls(**data)


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
    project_ids: Optional[List[int]] = field(default_factory=list)

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
    type: str = "milestone"
    color: Optional[str] = None
    external_id: Optional[str] = None


@dataclass
class UpdateCategoryInput:
    name: Optional[str] = None


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
        # Convert datetime strings
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(
                data["created_at"].replace("Z", "+00:00")
            )
        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(
                data["updated_at"].replace("Z", "+00:00")
            )
        return cls(**data)


@dataclass
class CreateProjectInput:
    name: str
    abbreviation: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None
    external_id: Optional[str] = None
    follower_ids: Optional[List[str]] = None
    team_id: Optional[int] = None


@dataclass
class UpdateProjectInput:
    name: Optional[str] = None


@dataclass
class Project:
    id: int
    name: str
    app_url: Optional[str] = None
    archived: bool = False
    entity_type: str = "project"
    color: Optional[str] = None
    abbreviation: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    follower_ids: List[str] = field(default_factory=list)
    external_id: Optional[str] = None
    team_id: Optional[int] = None
    iteration_length: Optional[int] = None
    start_time: Optional[datetime] = None
    stats: Optional[Dict[str, Any]] = None

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Project":
        # Convert datetime strings
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(
                data["created_at"].replace("Z", "+00:00")
            )
        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(
                data["updated_at"].replace("Z", "+00:00")
            )
        if "start_time" in data and isinstance(data["start_time"], str):
            data["start_time"] = datetime.fromisoformat(
                data["start_time"].replace("Z", "+00:00")
            )
        return cls(**data)


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


@dataclass
class PaginatedResponse(Generic[T]):
    """Generic paginated response wrapper for list endpoints."""

    data: List[T]
    next: Optional[str] = None
    total: Optional[int] = None

    @classmethod
    def from_json(
        cls, data: Dict[str, Any], item_class: type[T]
    ) -> "PaginatedResponse[T]":
        """Create a PaginatedResponse from JSON data.

        Args:
            data: The raw JSON response
            item_class: The class to use for deserializing items
        """
        if isinstance(data, list):
            # Non-paginated response - wrap it
            return cls(data=[item_class.from_json(item) for item in data])
        else:
            # Paginated response
            result = {
                "data": [item_class.from_json(item) for item in data.get("data", [])],
                "next": data.get("next"),
                "total": data.get("total"),
            }
            return cls(**result)


@dataclass
class StoryReaction:
    """Emoji reaction on a comment."""

    emoji: str
    permission_ids: List[str]

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "StoryReaction":
        return cls(**data)


@dataclass
class StoryComment:
    """A Comment is any note added within the Comment field of a Story."""

    id: int
    text: Optional[str]
    author_id: Optional[str]
    created_at: datetime
    entity_type: str
    story_id: int
    position: int

    app_url: Optional[str] = None
    deleted: bool = False
    updated_at: Optional[datetime] = None
    external_id: Optional[str] = None
    parent_id: Optional[int] = None
    blocker: bool = False
    unblocks_parent: bool = False
    linked_to_slack: bool = False

    mention_ids: List[str] = field(default_factory=list)  # Deprecated
    member_mention_ids: List[str] = field(default_factory=list)
    group_mention_ids: List[str] = field(default_factory=list)
    reactions: List[StoryReaction] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "StoryComment":
        # Convert datetime strings
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(
                data["created_at"].replace("Z", "+00:00")
            )
        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(
                data["updated_at"].replace("Z", "+00:00")
            )

        # Convert reactions
        if "reactions" in data:
            data["reactions"] = [StoryReaction.from_json(r) for r in data["reactions"]]

        return cls(**data)


@dataclass
class CreateStoryCommentInput:
    """Request parameters for creating a Comment on a Shortcut Story."""

    text: str
    author_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    external_id: Optional[str] = None
    parent_id: Optional[int] = None


@dataclass
class UpdateStoryCommentInput:
    """Request parameters for updating a Comment."""

    text: str


# Aliases for consistency with other endpoints
CreateCommentInput = CreateStoryCommentInput
UpdateCommentInput = UpdateStoryCommentInput


@dataclass
class ThreadedComment:
    """Comments associated with Epic Discussions."""

    id: int
    text: str
    author_id: str
    created_at: datetime
    entity_type: str

    app_url: Optional[str] = None
    deleted: bool = False
    updated_at: Optional[datetime] = None
    external_id: Optional[str] = None

    mention_ids: List[str] = field(default_factory=list)  # Deprecated
    member_mention_ids: List[str] = field(default_factory=list)
    group_mention_ids: List[str] = field(default_factory=list)
    comments: List["ThreadedComment"] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "ThreadedComment":
        # Convert datetime strings
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(
                data["created_at"].replace("Z", "+00:00")
            )
        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(
                data["updated_at"].replace("Z", "+00:00")
            )

        # Convert nested comments
        if "comments" in data:
            data["comments"] = [ThreadedComment.from_json(c) for c in data["comments"]]

        return cls(**data)


@dataclass
class MilestoneStats:
    """A group of calculated values for this Milestone."""

    num_related_documents: int
    average_cycle_time: Optional[int] = None
    average_lead_time: Optional[int] = None

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "MilestoneStats":
        return cls(**data)


@dataclass
class Milestone:
    """(Deprecated) A Milestone is a collection of Epics that represent a release or some other large initiative."""

    id: int
    name: str
    description: str
    state: str
    position: int
    created_at: datetime
    updated_at: datetime
    entity_type: str
    app_url: str
    global_id: str
    stats: MilestoneStats

    archived: bool = False
    started: bool = False
    completed: bool = False
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    started_at_override: Optional[datetime] = None
    completed_at_override: Optional[datetime] = None

    categories: List["Category"] = field(default_factory=list)
    key_result_ids: List[str] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Milestone":
        # Convert datetime strings
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(
                data["created_at"].replace("Z", "+00:00")
            )
        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(
                data["updated_at"].replace("Z", "+00:00")
            )
        if "started_at" in data and isinstance(data["started_at"], str):
            data["started_at"] = datetime.fromisoformat(
                data["started_at"].replace("Z", "+00:00")
            )
        if "completed_at" in data and isinstance(data["completed_at"], str):
            data["completed_at"] = datetime.fromisoformat(
                data["completed_at"].replace("Z", "+00:00")
            )
        if "started_at_override" in data and isinstance(
            data["started_at_override"], str
        ):
            data["started_at_override"] = datetime.fromisoformat(
                data["started_at_override"].replace("Z", "+00:00")
            )
        if "completed_at_override" in data and isinstance(
            data["completed_at_override"], str
        ):
            data["completed_at_override"] = datetime.fromisoformat(
                data["completed_at_override"].replace("Z", "+00:00")
            )

        # Convert stats
        if "stats" in data:
            data["stats"] = MilestoneStats.from_json(data["stats"])

        # Convert categories - Category class is defined later in this file
        if "categories" in data:
            data["categories"] = [Category.from_json(c) for c in data["categories"]]

        return cls(**data)


@dataclass
class CreateCategoryParams:
    """Parameters for creating or referencing a category."""

    name: Optional[str] = None  # Optional when using id
    color: Optional[str] = None
    external_id: Optional[str] = None
    id: Optional[int] = None  # For referencing existing categories


@dataclass
class CreateMilestoneInput:
    """Request parameters for creating a Milestone."""

    name: str
    description: Optional[str] = None
    state: Optional[str] = "to do"  # Enum: "in progress", "to do", "done"
    started_at_override: Optional[datetime] = None
    completed_at_override: Optional[datetime] = None
    categories: List[CreateCategoryParams] = field(default_factory=list)


@dataclass
class UpdateMilestoneInput:
    """Request parameters for updating a Milestone."""

    name: Optional[str] = None
    description: Optional[str] = None
    state: Optional[str] = None  # Enum: "in progress", "to do", "done"
    archived: Optional[bool] = None
    started_at_override: Optional[datetime] = None
    completed_at_override: Optional[datetime] = None
    categories: Optional[List[CreateCategoryParams]] = None
    before_id: Optional[int] = None
    after_id: Optional[int] = None


@dataclass
class CustomFieldEnumValue:
    """A value within the domain of a Custom Field."""

    id: str
    value: str
    position: int
    entity_type: str = "custom-field-enum-value"
    color_key: Optional[str] = None
    enabled: bool = True

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "CustomFieldEnumValue":
        return cls(**data)


@dataclass
class CustomField:
    """A custom field that can be applied to stories."""

    id: str
    name: str
    field_type: str  # Currently only "enum"
    position: int
    enabled: bool
    created_at: datetime
    updated_at: datetime
    entity_type: str = "custom-field"

    description: Optional[str] = None
    icon_set_identifier: Optional[str] = None
    canonical_name: Optional[str] = None
    fixed_position: bool = False

    story_types: List[str] = field(default_factory=list)
    values: List[CustomFieldEnumValue] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "CustomField":
        # Convert datetime strings
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(
                data["created_at"].replace("Z", "+00:00")
            )
        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(
                data["updated_at"].replace("Z", "+00:00")
            )

        # Convert values
        if "values" in data:
            data["values"] = [CustomFieldEnumValue.from_json(v) for v in data["values"]]

        return cls(**data)


@dataclass
class UpdateCustomFieldEnumValue:
    """Parameters for updating a custom field enum value."""

    id: Optional[str] = None
    value: Optional[str] = None
    color_key: Optional[str] = None
    enabled: Optional[bool] = None


@dataclass
class UpdateCustomFieldInput:
    """Request parameters for updating a Custom Field."""

    name: Optional[str] = None
    description: Optional[str] = None
    enabled: Optional[bool] = None
    icon_set_identifier: Optional[str] = None
    values: Optional[List[UpdateCustomFieldEnumValue]] = None
    before_id: Optional[str] = None
    after_id: Optional[str] = None
