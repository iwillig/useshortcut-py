from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Generic, Optional, TypeVar

T = TypeVar("T")


@dataclass
class CreateStoryParams:
    """Request parameters for creating a story."""

    # Required fields
    name: str
    workflow_state_id: int

    # Optional fields
    description: Optional[str] = None
    story_type: Optional[str] = "feature"
    project_id: Optional[int] = None
    epic_id: Optional[int] = None
    label_ids: Optional[list[int]] = None
    archived: Optional[bool] = None
    story_links: Optional[list[dict[str, Any]]] = None
    labels: Optional[list[dict[str, Any]]] = None
    custom_fields: Optional[list[dict[str, Any]]] = None
    move_to: Optional[str] = None
    file_ids: Optional[list[int]] = None
    source_task_id: Optional[int] = None
    completed_at_override: Optional[datetime] = None
    comments: Optional[list[dict[str, Any]]] = None
    story_template_id: Optional[str] = None
    external_links: Optional[list[str]] = None
    sub_tasks: Optional[list[dict[str, Any]]] = None
    requested_by_id: Optional[str] = None
    iteration_id: Optional[int] = None
    tasks: Optional[list[dict[str, Any]]] = None
    started_at_override: Optional[datetime] = None
    group_id: Optional[str] = None
    updated_at: Optional[datetime] = None
    follower_ids: Optional[list[str]] = None
    owner_ids: Optional[list[str]] = None
    external_id: Optional[str] = None
    parent_story_id: Optional[int] = None
    estimate: Optional[int] = None
    linked_file_ids: Optional[list[int]] = None
    deadline: Optional[datetime] = None
    created_at: Optional[datetime] = None


@dataclass
class UpdateStoryInput:
    name: Optional[str] = None
    description: Optional[str] = None
    workflow_state_id: Optional[int] = None
    story_type: Optional[str] = None
    project_id: Optional[int] = None
    epic_id: Optional[int] = None
    label_ids: Optional[list[int]] = None
    owner_ids: Optional[list[str]] = None
    follower_ids: Optional[list[str]] = None
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
    parent_story_id: Optional[int] = None
    labels: list[dict[str, Any]] = field(default_factory=list)
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

    pull_requests: Optional[list[dict[str, Any]]] = field(default_factory=list)
    story_links: Optional[list[dict[str, Any]]] = field(default_factory=list)
    comments: Optional[list[dict[str, Any]]] = field(default_factory=list)
    branches: Optional[list[dict[str, Any]]] = field(default_factory=list)
    tasks: Optional[list[dict[str, Any]]] = field(default_factory=list)
    commits: Optional[list[dict[str, Any]]] = field(default_factory=list)
    files: Optional[list[dict[str, Any]]] = field(default_factory=list)
    external_links: Optional[list[dict[str, Any]]] = field(default_factory=list)

    group_mention_ids: Optional[list[int]] = field(default_factory=list)
    comment_ids: Optional[list[int]] = field(default_factory=list)
    follower_ids: Optional[list[int]] = field(default_factory=list)
    owner_ids: Optional[list[int]] = field(default_factory=list)

    previous_iteration_ids: Optional[list[int]] = field(default_factory=list)

    mention_ids: Optional[list[int]] = field(default_factory=list)
    member_mention_ids: Optional[list[int]] = field(default_factory=list)
    label_ids: Optional[list[int]] = field(default_factory=list)
    task_ids: Optional[list[int]] = field(default_factory=list)
    file_ids: Optional[list[int]] = field(default_factory=list)

    linked_files: Optional[list[dict[str, Any]]] = field(default_factory=list)
    linked_file_ids: Optional[list[int]] = field(default_factory=list)
    sub_task_story_ids: Optional[list[int]] = field(default_factory=list)

    custom_fields: Optional[list[dict[str, Any]]] = field(default_factory=list)
    num_tasks_completed: Optional[int] = None

    stats: Optional[dict[str, Any]] = None
    lead_time: Optional[int] = None
    cycle_time: Optional[int] = None
    formatted_vcs_branch_name: Optional[str] = None

    entity_type: str = "story"

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "Story":
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
        for date_field in date_fields:
            if date_field in data and isinstance(data[date_field], str):
                data[date_field] = datetime.fromisoformat(
                    data[date_field].replace("Z", "+00:00")
                )
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

    owner_ids: list[str] = field(default_factory=list)
    mention_ids: list[str] = field(default_factory=list)  # Deprecated
    member_mention_ids: list[str] = field(default_factory=list)
    group_mention_ids: list[str] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "Task":
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
    owner_ids: list[str] = field(default_factory=list)
    external_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class UpdateTaskInput:
    """Request parameters for updating a Task."""

    description: Optional[str] = None
    owner_ids: Optional[list[str]] = None
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
    owner_ids: Optional[list[str]] = None
    follower_ids: Optional[list[str]] = None
    label_ids: Optional[list[int]] = None
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
    owner_ids: Optional[list[str]] = None
    follower_ids: Optional[list[str]] = None
    label_ids: Optional[list[int]] = None
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
    objective_ids: Optional[list[str]] = field(default_factory=list)
    planned_start_date: Optional[datetime] = None
    started_at_override: Optional[datetime] = None
    milestone_id: Optional[int] = None
    epic_state_id: Optional[int] = None
    app_url: Optional[str] = None
    entity_type: str = "epic"
    group_mention_ids: Optional[list[str]] = field(default_factory=list)
    follower_ids: Optional[list[str]] = field(default_factory=list)
    labels: Optional[list[dict[str, Any]]] = field(default_factory=list)
    label_ids: Optional[list[int]] = field(default_factory=list)
    group_ids: Optional[list[str]] = field(default_factory=list)
    owner_ids: Optional[list[str]] = field(default_factory=list)
    external_id: Optional[str] = None
    position: Optional[int] = None

    stories_without_projects: Optional[Any] = None

    project_ids: Optional[list[int]] = field(default_factory=list)
    mention_ids: Optional[list[str]] = field(default_factory=list)
    member_mention_ids: Optional[list[str]] = field(default_factory=list)
    associated_groups: Optional[list[dict[str, Any]]] = field(default_factory=list)
    comments: Optional[list[dict[str, Any]]] = field(default_factory=list)
    stats: Optional[Any] = None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "Epic":
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
    epic_states: list[dict[str, Any]]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    entity_type: str = "epic-workflow"

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "EpicWorkflow":
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
    follower_ids: Optional[list[str]] = None
    group_ids: Optional[list[str]] = None
    label_ids: Optional[list[int]] = None


@dataclass
class UpdateIterationInput:
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    follower_ids: Optional[list[str]] = None
    group_ids: Optional[list[str]] = None
    label_ids: Optional[list[int]] = None


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
    labels: Optional[list[dict[str, Any]]] = field(default_factory=list)
    follower_ids: Optional[list[str]] = field(default_factory=list)
    group_ids: Optional[list[str]] = field(default_factory=list)
    mention_ids: Optional[list[str]] = field(default_factory=list)
    member_mention_ids: Optional[list[str]] = field(default_factory=list)
    group_mention_ids: Optional[list[str]] = field(default_factory=list)
    label_ids: Optional[list[int]] = field(default_factory=list)

    associated_groups: Optional[list[dict[str, Any]]] = field(default_factory=list)

    entity_type: str = "iteration"
    stats: Optional[Any] = None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "Iteration":
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
    def from_json(cls, data: dict[str, Any]) -> "StoryLink":
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

    member_ids: Optional[list[str]] = field(default_factory=list)
    num_stories_started: Optional[int] = None
    num_stories: Optional[int] = None
    num_epics_started: Optional[int] = None
    num_stories_backlog: Optional[int] = None
    workflow_ids: Optional[list[int]] = field(default_factory=list)
    default_workflow_id: Optional[int] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "Group":
        return cls(**data)


@dataclass
class KeyResultValue:
    boolean_value: bool
    numeric_value: str

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "KeyResultValue":
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
    def from_json(cls, data: dict[str, Any]) -> "KeyResult":
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
    def from_json(cls, data: dict[str, Any]) -> "Label":
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
    global_id: Optional[str] = None
    name: Optional[str] = None

    content_type: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    description: Optional[str] = None
    entity_type: str = "linked-file"

    group_mention_ids: Optional[list[str]] = field(default_factory=list)
    member_mention_ids: Optional[list[str]] = field(default_factory=list)
    mention_ids: Optional[list[str]] = field(default_factory=list)
    story_ids: Optional[list[int]] = field(default_factory=list)
    url: Optional[str] = None
    size: Optional[int] = None
    thumbnail_url: Optional[str] = None
    filename: Optional[str] = None
    type: Optional[str] = None
    uploader_id: Optional[str] = None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "LinkedFiles":
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
    group_mention_ids: Optional[list[str]] = field(default_factory=list)
    member_mention_ids: Optional[list[str]] = field(default_factory=list)
    mention_ids: Optional[list[str]] = field(default_factory=list)
    story_link_id: Optional[int] = None
    story_ids: Optional[list[int]] = field(default_factory=list)
    thumbnail_url: Optional[str] = None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "File":
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
    is_agent: Optional[bool] = None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "Profile":
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
    def from_json(cls, data: dict[str, Any]) -> "Member":

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
    def from_json(cls, data: dict[str, Any]) -> "Objective":
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
    def from_json(cls, data: dict[str, Any]) -> "Repository":
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
    def from_json(cls, data: dict[str, Any]) -> "WorkflowState":
        return cls(**data)


@dataclass
class Workflow:
    id: int
    name: str
    description: str
    entity_type: str = "workflow"

    auto_assign_owner: Optional[bool] = None
    project_ids: Optional[list[int]] = field(default_factory=list)

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    default_state_id: Optional[int] = None

    states: list[WorkflowState] = field(default_factory=list)

    team_id: Optional[int] = None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "Workflow":
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
    def from_json(cls, data: dict[str, Any]) -> "Category":
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
    follower_ids: Optional[list[str]] = None
    team_id: Optional[int] = None


@dataclass
class UpdateProjectInput:
    name: Optional[str] = None
    description: Optional[str] = None


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
    follower_ids: list[str] = field(default_factory=list)
    external_id: Optional[str] = None
    team_id: Optional[int] = None
    iteration_length: Optional[int] = None
    start_time: Optional[datetime] = None
    stats: Optional[dict[str, Any]] = None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "Project":
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
    data: list[Story]
    total: int
    next: Optional[str] = None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "SearchStoryResult":
        if "data" in data:
            data["data"] = [Story.from_json(x) for x in data["data"]]
        return cls(**data)


@dataclass
class PaginatedResponse(Generic[T]):
    """Generic paginated response wrapper for list endpoints."""

    data: list[T]
    next: Optional[str] = None
    total: Optional[int] = None

    @classmethod
    def from_json(
        cls, data: dict[str, Any], item_class: type[T]
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
    permission_ids: list[str]

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "StoryReaction":
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

    mention_ids: list[str] = field(default_factory=list)  # Deprecated
    member_mention_ids: list[str] = field(default_factory=list)
    group_mention_ids: list[str] = field(default_factory=list)
    reactions: list[StoryReaction] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "StoryComment":
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

    mention_ids: list[str] = field(default_factory=list)  # Deprecated
    member_mention_ids: list[str] = field(default_factory=list)
    group_mention_ids: list[str] = field(default_factory=list)
    comments: list["ThreadedComment"] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "ThreadedComment":
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
    def from_json(cls, data: dict[str, Any]) -> "MilestoneStats":
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

    categories: list["Category"] = field(default_factory=list)
    key_result_ids: list[str] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "Milestone":
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
    categories: list[CreateCategoryParams] = field(default_factory=list)


@dataclass
class UpdateMilestoneInput:
    """Request parameters for updating a Milestone."""

    name: Optional[str] = None
    description: Optional[str] = None
    state: Optional[str] = None  # Enum: "in progress", "to do", "done"
    archived: Optional[bool] = None
    started_at_override: Optional[datetime] = None
    completed_at_override: Optional[datetime] = None
    categories: Optional[list[CreateCategoryParams]] = None
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
    def from_json(cls, data: dict[str, Any]) -> "CustomFieldEnumValue":
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

    story_types: list[str] = field(default_factory=list)
    values: list[CustomFieldEnumValue] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "CustomField":
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
    values: Optional[list[UpdateCustomFieldEnumValue]] = None
    before_id: Optional[str] = None
    after_id: Optional[str] = None


# ============================================================================
# Documents (Docs)
# ============================================================================


@dataclass
class DocSlim:
    """A lightweight representation of a Doc."""

    id: str
    title: Optional[str]
    app_url: str

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "DocSlim":
        # Only extract fields we need
        return cls(
            id=data["id"],
            title=data.get("title"),
            app_url=data["app_url"],
        )


@dataclass
class Doc:
    """A Doc is a collaborative document in Shortcut."""

    id: str
    title: Optional[str]
    content_markdown: Optional[str]
    app_url: str
    created_at: datetime
    updated_at: datetime
    archived: bool
    content_html: Optional[str] = None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "Doc":
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
class CreateDocInput:
    """Request parameters for creating a Doc."""

    title: str
    content: str
    content_format: Optional[str] = None  # "markdown" or "html"


@dataclass
class UpdateDocInput:
    """Request parameters for updating a Doc."""

    title: Optional[str] = None
    content: Optional[str] = None
    content_format: Optional[str] = None  # "markdown" or "html"


# ============================================================================
# Entity Templates
# ============================================================================


@dataclass
class StoryContents:
    """A container entity for the attributes a template should populate."""

    entity_type: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    story_type: Optional[str] = None
    epic_id: Optional[int] = None
    iteration_id: Optional[int] = None
    group_id: Optional[str] = None
    workflow_state_id: Optional[int] = None
    project_id: Optional[int] = None
    estimate: Optional[int] = None
    deadline: Optional[datetime] = None
    follower_ids: list[str] = field(default_factory=list)
    owner_ids: list[str] = field(default_factory=list)
    label_ids: list[int] = field(default_factory=list)
    labels: list[dict[str, Any]] = field(default_factory=list)
    custom_fields: list[dict[str, Any]] = field(default_factory=list)
    external_links: list[str] = field(default_factory=list)
    tasks: list[dict[str, Any]] = field(default_factory=list)
    sub_tasks: list[dict[str, Any]] = field(default_factory=list)
    linked_files: list[dict[str, Any]] = field(default_factory=list)
    files: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "StoryContents":
        if "deadline" in data and isinstance(data["deadline"], str):
            data["deadline"] = datetime.fromisoformat(
                data["deadline"].replace("Z", "+00:00")
            )
        return cls(**data)


@dataclass
class CreateStoryContents:
    """Request parameters for story contents in a template."""

    name: Optional[str] = None
    description: Optional[str] = None
    story_type: Optional[str] = None
    epic_id: Optional[int] = None
    iteration_id: Optional[int] = None
    group_id: Optional[str] = None
    workflow_state_id: Optional[int] = None
    project_id: Optional[int] = None
    estimate: Optional[int] = None
    deadline: Optional[datetime] = None
    follower_ids: list[str] = field(default_factory=list)
    owner_ids: list[str] = field(default_factory=list)
    labels: list[dict[str, Any]] = field(default_factory=list)
    custom_fields: list[dict[str, Any]] = field(default_factory=list)
    external_links: list[str] = field(default_factory=list)
    tasks: list[dict[str, Any]] = field(default_factory=list)
    sub_tasks: list[dict[str, Any]] = field(default_factory=list)
    file_ids: list[int] = field(default_factory=list)
    linked_file_ids: list[int] = field(default_factory=list)


@dataclass
class UpdateStoryContents:
    """Updated attributes for the template to populate."""

    name: Optional[str] = None
    description: Optional[str] = None
    story_type: Optional[str] = None
    epic_id: Optional[int] = None
    iteration_id: Optional[int] = None
    group_id: Optional[str] = None
    workflow_state_id: Optional[int] = None
    project_id: Optional[int] = None
    estimate: Optional[int] = None
    deadline: Optional[datetime] = None
    follower_ids: list[str] = field(default_factory=list)
    owner_ids: list[str] = field(default_factory=list)
    labels: list[dict[str, Any]] = field(default_factory=list)
    custom_fields: list[dict[str, Any]] = field(default_factory=list)
    external_links: list[str] = field(default_factory=list)
    tasks: list[dict[str, Any]] = field(default_factory=list)
    sub_tasks: list[dict[str, Any]] = field(default_factory=list)
    file_ids: list[int] = field(default_factory=list)
    linked_file_ids: list[int] = field(default_factory=list)


@dataclass
class EntityTemplate:
    """An entity template can be used to prefill various fields when creating new stories."""

    id: str
    name: str
    author_id: str
    created_at: datetime
    updated_at: datetime
    last_used_at: datetime
    entity_type: str = "entity-template"
    story_contents: Optional[StoryContents] = None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "EntityTemplate":
        # Convert datetime strings
        for field_name in ["created_at", "updated_at", "last_used_at"]:
            if field_name in data and isinstance(data[field_name], str):
                data[field_name] = datetime.fromisoformat(
                    data[field_name].replace("Z", "+00:00")
                )
        if "story_contents" in data and data["story_contents"]:
            data["story_contents"] = StoryContents.from_json(data["story_contents"])
        return cls(**data)


@dataclass
class CreateEntityTemplateInput:
    """Request parameters for creating an entity template."""

    name: str
    story_contents: dict[str, Any]
    author_id: Optional[str] = None


@dataclass
class UpdateEntityTemplateInput:
    """Request parameters for updating an entity template."""

    name: Optional[str] = None
    story_contents: Optional[dict[str, Any]] = None


# ============================================================================
# Health
# ============================================================================


@dataclass
class Health:
    """The current health status of an Epic or Objective."""

    id: Optional[str]
    status: str  # "At Risk", "On Track", "Off Track", "No Health"
    entity_type: str = "health"
    author_id: Optional[str] = None
    epic_id: Optional[int] = None
    objective_id: Optional[int] = None
    text: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "Health":
        # Convert datetime strings
        for field_name in ["created_at", "updated_at"]:
            if field_name in data and isinstance(data[field_name], str):
                data[field_name] = datetime.fromisoformat(
                    data[field_name].replace("Z", "+00:00")
                )
        return cls(**data)


@dataclass
class CreateHealthInput:
    """Request parameters for creating a Health record."""

    status: str  # "At Risk", "On Track", "Off Track", "No Health"
    text: Optional[str] = None


@dataclass
class UpdateHealthInput:
    """Request parameters for updating a Health record."""

    status: Optional[str] = None
    text: Optional[str] = None


# ============================================================================
# Slim Models for List Responses
# ============================================================================


@dataclass
class EpicSlim:
    """A lightweight representation of an Epic."""

    id: int
    name: str
    global_id: str
    app_url: str
    archived: bool = False
    started: bool = False
    completed: bool = False
    entity_type: str = "epic"
    description: Optional[str] = None
    state: Optional[str] = None
    epic_state_id: Optional[int] = None
    milestone_id: Optional[int] = None
    objective_ids: list[int] = field(default_factory=list)
    project_ids: list[int] = field(default_factory=list)
    label_ids: list[int] = field(default_factory=list)
    follower_ids: list[str] = field(default_factory=list)
    owner_ids: list[str] = field(default_factory=list)
    group_ids: list[str] = field(default_factory=list)
    group_id: Optional[str] = None
    requested_by_id: Optional[str] = None
    deadline: Optional[datetime] = None
    planned_start_date: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    started_at_override: Optional[datetime] = None
    completed_at_override: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    position: Optional[int] = None
    stats: Optional[dict[str, Any]] = None
    labels: list[dict[str, Any]] = field(default_factory=list)
    associated_groups: list[dict[str, Any]] = field(default_factory=list)
    external_id: Optional[str] = None
    productboard_id: Optional[str] = None
    productboard_url: Optional[str] = None
    productboard_name: Optional[str] = None
    productboard_plugin_id: Optional[str] = None
    stories_without_projects: Optional[int] = None
    mention_ids: list[str] = field(default_factory=list)
    member_mention_ids: list[str] = field(default_factory=list)
    group_mention_ids: list[str] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "EpicSlim":
        # Convert datetime strings
        for field_name in [
            "deadline",
            "planned_start_date",
            "started_at",
            "completed_at",
            "started_at_override",
            "completed_at_override",
            "created_at",
            "updated_at",
        ]:
            if field_name in data and isinstance(data[field_name], str):
                data[field_name] = datetime.fromisoformat(
                    data[field_name].replace("Z", "+00:00")
                )
        return cls(**data)


@dataclass
class StorySlim:
    """A lightweight representation of a Story."""

    id: int
    name: str
    global_id: str
    app_url: str
    entity_type: str = "story"
    story_type: str = "feature"
    archived: bool = False
    started: bool = False
    completed: bool = False
    blocker: bool = False
    blocked: bool = False
    description: Optional[str] = None
    workflow_id: Optional[int] = None
    workflow_state_id: Optional[int] = None
    project_id: Optional[int] = None
    epic_id: Optional[int] = None
    iteration_id: Optional[int] = None
    parent_story_id: Optional[int] = None
    story_template_id: Optional[str] = None
    requested_by_id: Optional[str] = None
    group_id: Optional[str] = None
    estimate: Optional[int] = None
    position: Optional[int] = None
    deadline: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    started_at_override: Optional[datetime] = None
    completed_at_override: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    moved_at: Optional[datetime] = None
    external_id: Optional[str] = None
    label_ids: list[int] = field(default_factory=list)
    follower_ids: list[str] = field(default_factory=list)
    owner_ids: list[str] = field(default_factory=list)
    task_ids: list[int] = field(default_factory=list)
    file_ids: list[int] = field(default_factory=list)
    linked_file_ids: list[int] = field(default_factory=list)
    comment_ids: list[int] = field(default_factory=list)
    previous_iteration_ids: list[int] = field(default_factory=list)
    sub_task_story_ids: list[int] = field(default_factory=list)
    external_links: list[str] = field(default_factory=list)
    labels: list[dict[str, Any]] = field(default_factory=list)
    story_links: list[dict[str, Any]] = field(default_factory=list)
    custom_fields: list[dict[str, Any]] = field(default_factory=list)
    stats: Optional[dict[str, Any]] = None
    num_tasks_completed: Optional[int] = None
    lead_time: Optional[int] = None
    cycle_time: Optional[int] = None
    formatted_vcs_branch_name: Optional[str] = None
    mention_ids: list[str] = field(default_factory=list)
    member_mention_ids: list[str] = field(default_factory=list)
    group_mention_ids: list[str] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "StorySlim":
        # Convert datetime strings
        for field_name in [
            "deadline",
            "started_at",
            "completed_at",
            "started_at_override",
            "completed_at_override",
            "created_at",
            "updated_at",
            "moved_at",
        ]:
            if field_name in data and isinstance(data[field_name], str):
                data[field_name] = datetime.fromisoformat(
                    data[field_name].replace("Z", "+00:00")
                )
        return cls(**data)


@dataclass
class IterationSlim:
    """A lightweight representation of an Iteration."""

    id: int
    name: str
    global_id: str
    app_url: str
    status: str
    entity_type: str = "iteration"
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    label_ids: list[int] = field(default_factory=list)
    follower_ids: list[str] = field(default_factory=list)
    group_ids: list[str] = field(default_factory=list)
    labels: list[dict[str, Any]] = field(default_factory=list)
    associated_groups: list[dict[str, Any]] = field(default_factory=list)
    stats: Optional[dict[str, Any]] = None
    mention_ids: list[str] = field(default_factory=list)
    member_mention_ids: list[str] = field(default_factory=list)
    group_mention_ids: list[str] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "IterationSlim":
        # Convert datetime strings
        for field_name in ["start_date", "end_date", "created_at", "updated_at"]:
            if field_name in data and isinstance(data[field_name], str):
                data[field_name] = datetime.fromisoformat(
                    data[field_name].replace("Z", "+00:00")
                )
        return cls(**data)


# ============================================================================
# Search Results
# ============================================================================


@dataclass
class EpicSearchResult:
    """A single Epic search result."""

    id: int
    name: str
    entity_type: str = "epic"
    description: Optional[str] = None
    app_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    deadline: Optional[datetime] = None
    state: Optional[str] = None
    epic_state_id: Optional[int] = None
    milestone_id: Optional[int] = None
    objective_ids: list[int] = field(default_factory=list)
    project_ids: list[int] = field(default_factory=list)
    follower_ids: list[str] = field(default_factory=list)
    owner_ids: list[str] = field(default_factory=list)
    label_ids: list[int] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "EpicSearchResult":
        for field_name in [
            "created_at",
            "updated_at",
            "completed_at",
            "started_at",
            "deadline",
        ]:
            if field_name in data and isinstance(data[field_name], str):
                data[field_name] = datetime.fromisoformat(
                    data[field_name].replace("Z", "+00:00")
                )
        return cls(**data)


@dataclass
class StorySearchResult:
    """A single Story search result."""

    id: int
    name: str
    entity_type: str = "story"
    story_type: str = "feature"
    description: Optional[str] = None
    app_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    deadline: Optional[datetime] = None
    workflow_state_id: Optional[int] = None
    project_id: Optional[int] = None
    epic_id: Optional[int] = None
    iteration_id: Optional[int] = None
    estimate: Optional[int] = None
    follower_ids: list[str] = field(default_factory=list)
    owner_ids: list[str] = field(default_factory=list)
    label_ids: list[int] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "StorySearchResult":
        for field_name in [
            "created_at",
            "updated_at",
            "completed_at",
            "started_at",
            "deadline",
        ]:
            if field_name in data and isinstance(data[field_name], str):
                data[field_name] = datetime.fromisoformat(
                    data[field_name].replace("Z", "+00:00")
                )
        return cls(**data)


@dataclass
class StorySearchResults:
    """The results of a Story search query."""

    total: int
    data: list[StorySearchResult]
    next: Optional[str] = None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "StorySearchResults":
        if "data" in data:
            data["data"] = [StorySearchResult.from_json(x) for x in data["data"]]
        return cls(**data)


@dataclass
class EpicSearchResults:
    """The results of an Epic search query."""

    total: int
    data: list[EpicSearchResult]
    next: Optional[str] = None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "EpicSearchResults":
        if "data" in data:
            data["data"] = [EpicSearchResult.from_json(x) for x in data["data"]]
        return cls(**data)


@dataclass
class IterationSearchResults:
    """The results of an Iteration search query."""

    total: int
    data: list[IterationSlim]
    next: Optional[str] = None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "IterationSearchResults":
        if "data" in data:
            data["data"] = [IterationSlim.from_json(x) for x in data["data"]]
        return cls(**data)


@dataclass
class ObjectiveSearchResults:
    """The results of an Objective (Milestone) search query."""

    total: int
    data: list[Objective]
    next: Optional[str] = None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "ObjectiveSearchResults":
        if "data" in data:
            data["data"] = [Objective.from_json(x) for x in data["data"]]
        return cls(**data)


@dataclass
class DocumentSearchResults:
    """The results of a Document search query."""

    total: int
    data: list[DocSlim]
    next: Optional[str] = None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "DocumentSearchResults":
        if "data" in data:
            data["data"] = [DocSlim.from_json(x) for x in data["data"]]
        return cls(**data)


@dataclass
class SearchResults:
    """The results of a multi-entity search query."""

    epics: Optional[EpicSearchResults] = None
    stories: Optional[StorySearchResults] = None
    iterations: Optional[IterationSearchResults] = None
    milestones: Optional[ObjectiveSearchResults] = None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "SearchResults":
        if "epics" in data and data["epics"]:
            data["epics"] = EpicSearchResults.from_json(data["epics"])
        if "stories" in data and data["stories"]:
            data["stories"] = StorySearchResults.from_json(data["stories"])
        if "iterations" in data and data["iterations"]:
            data["iterations"] = IterationSearchResults.from_json(data["iterations"])
        if "milestones" in data and data["milestones"]:
            data["milestones"] = ObjectiveSearchResults.from_json(data["milestones"])
        return cls(**data)


# ============================================================================
# Story History
# ============================================================================


@dataclass
class StoryHistory:
    """Historical changes to a Story."""

    id: int
    entity_type: str = "story-history"
    story_id: Optional[int] = None
    member_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    changed_at: Optional[datetime] = None
    actions: list[dict[str, Any]] = field(default_factory=list)
    external_id: Optional[str] = None
    version: Optional[str] = None
    subject_type: Optional[str] = None
    subject_id: Optional[int] = None
    changes: Optional[dict[str, Any]] = None
    name: Optional[str] = None
    description: Optional[str] = None
    story_type: Optional[str] = None
    workflow_state_id: Optional[int] = None
    archived: Optional[bool] = None
    position: Optional[int] = None
    started: Optional[bool] = None
    completed: Optional[bool] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    estimate: Optional[int] = None
    deadline: Optional[datetime] = None
    project_id: Optional[int] = None
    epic_id: Optional[int] = None
    iteration_id: Optional[int] = None
    label_ids: Optional[list[int]] = None
    owner_ids: Optional[list[str]] = None
    follower_ids: Optional[list[str]] = None
    group_id: Optional[str] = None
    group_ids: Optional[list[str]] = None
    blocked: Optional[bool] = None
    blocker: Optional[bool] = None
    branch_ids: Optional[list[int]] = None
    commit_ids: Optional[list[int]] = None
    pull_request_ids: Optional[list[int]] = None
    file_ids: Optional[list[int]] = None
    linked_file_ids: Optional[list[int]] = None
    app_url: Optional[str] = None
    mention_ids: Optional[list[str]] = None
    member_mention_ids: Optional[list[str]] = None
    group_mention_ids: Optional[list[str]] = None
    primary_id: Optional[int] = None
    references_id: Optional[int] = None
    references: Optional[list[dict[str, Any]]] = None
    revert: Optional[bool] = None
    actor_name: Optional[str] = None
    actor_id: Optional[str] = None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "StoryHistory":
        for field_name in [
            "created_at",
            "updated_at",
            "changed_at",
            "started_at",
            "completed_at",
            "deadline",
        ]:
            if field_name in data and isinstance(data[field_name], str):
                data[field_name] = datetime.fromisoformat(
                    data[field_name].replace("Z", "+00:00")
                )
        return cls(**data)


# ============================================================================
# Bulk Operations
# ============================================================================


@dataclass
class CreateStoriesInput:
    """Request parameters for creating multiple stories."""

    stories: list[CreateStoryParams]


@dataclass
class UpdateStoriesInput:
    """Request parameters for updating multiple stories."""

    story_ids: list[int]
    workflow_state_id: Optional[int] = None
    project_id: Optional[int] = None
    epic_id: Optional[int] = None
    iteration_id: Optional[int] = None
    group_id: Optional[str] = None
    owner_ids: Optional[list[str]] = None
    follower_ids: Optional[list[str]] = None
    label_ids: Optional[list[int]] = None
    archived: Optional[bool] = None
    story_type: Optional[str] = None
    estimate: Optional[int] = None
    deadline: Optional[datetime] = None


@dataclass
class DeleteStoriesInput:
    """Request parameters for deleting multiple stories."""

    story_ids: list[int]


# ============================================================================
# Story From Template
# ============================================================================


@dataclass
class CreateStoryFromTemplateInput:
    """Request parameters for creating a story from a template."""

    story_template_id: str
    name: Optional[str] = None
    description: Optional[str] = None
    workflow_state_id: Optional[int] = None
    project_id: Optional[int] = None
    epic_id: Optional[int] = None
    iteration_id: Optional[int] = None
    group_id: Optional[str] = None
    owner_ids: Optional[list[str]] = None
    follower_ids: Optional[list[str]] = None
    label_ids: Optional[list[int]] = None
    estimate: Optional[int] = None
    deadline: Optional[datetime] = None
    external_id: Optional[str] = None
    archived: Optional[bool] = None
    story_type: Optional[str] = None


# ============================================================================
# Reactions
# ============================================================================


@dataclass
class CreateReactionInput:
    """Request parameters for creating a reaction on a comment."""

    emoji: str


@dataclass
class DeleteReactionInput:
    """Request parameters for deleting a reaction from a comment."""

    emoji: str


# ============================================================================
# Generic Integration (Webhook)
# ============================================================================


@dataclass
class GenericIntegration:
    """A generic integration (webhook)."""

    id: int
    name: str
    url: str
    entity_type: str = "integration"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "GenericIntegration":
        for field_name in ["created_at", "updated_at"]:
            if field_name in data and isinstance(data[field_name], str):
                data[field_name] = datetime.fromisoformat(
                    data[field_name].replace("Z", "+00:00")
                )
        return cls(**data)


@dataclass
class CreateGenericIntegrationInput:
    """Request parameters for creating a generic integration."""

    name: str
    url: str


# ============================================================================
# Query Stories (Advanced Search)
# ============================================================================


@dataclass
class QueryStoriesInput:
    """Request parameters for querying stories via POST."""

    query: str
    detail: str = "slim"  # "slim" or "full"
    page_size: int = 25
    next: Optional[str] = None


# ============================================================================
# UploadedFile (for file uploads)
# ============================================================================


@dataclass
class UploadedFile:
    """A file that has been uploaded to Shortcut."""

    id: int
    name: str
    content_type: str
    size: int
    filename: str
    url: str
    entity_type: str = "uploaded-file"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    uploader_id: Optional[str] = None
    description: Optional[str] = None
    external_id: Optional[str] = None
    story_ids: list[int] = field(default_factory=list)
    thumbnail_url: Optional[str] = None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "UploadedFile":
        for field_name in ["created_at", "updated_at"]:
            if field_name in data and isinstance(data[field_name], str):
                data[field_name] = datetime.fromisoformat(
                    data[field_name].replace("Z", "+00:00")
                )
        return cls(**data)


@dataclass
class UpdateFileInput:
    """Request parameters for updating a file."""

    name: Optional[str] = None
    description: Optional[str] = None
    external_id: Optional[str] = None


# ============================================================================
# LabelSlim
# ============================================================================


@dataclass
class LabelSlim:
    """A lightweight representation of a Label."""

    id: int
    name: str
    entity_type: str = "label"
    color: Optional[str] = None
    description: Optional[str] = None
    external_id: Optional[str] = None
    archived: bool = False

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "LabelSlim":
        return cls(**data)
