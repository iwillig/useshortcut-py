# Implementation Plan for Missing Shortcut API Endpoints

## Overview
This plan outlines the systematic approach to add missing endpoints to the useshortcut Python client, prioritized by importance and grouped by feature area.

## Phase 1: Priority 1 - Core Features (Week 1)

### 1.1 Comments System
**Endpoints to implement:**
- `GET /stories/{story-id}/comments` - list_story_comments()
- `POST /stories/{story-id}/comments` - create_story_comment()
- `GET /stories/{story-id}/comments/{comment-id}` - get_story_comment()
- `PUT /stories/{story-id}/comments/{comment-id}` - update_story_comment()
- `DELETE /stories/{story-id}/comments/{comment-id}` - delete_story_comment()
- `GET /epics/{epic-id}/comments` - list_epic_comments()
- `POST /epics/{epic-id}/comments` - create_epic_comment()
- `GET /epics/{epic-id}/comments/{comment-id}` - get_epic_comment()
- `PUT /epics/{epic-id}/comments/{comment-id}` - update_epic_comment()
- `DELETE /epics/{epic-id}/comments/{comment-id}` - delete_epic_comment()

**Required models:**
- Comment
- CreateCommentInput
- UpdateCommentInput

### 1.2 Tasks System
**Endpoints to implement:**
- `GET /stories/{story-id}/tasks` - list_story_tasks()
- `POST /stories/{story-id}/tasks` - create_story_task()
- `GET /stories/{story-id}/tasks/{task-id}` - get_story_task()
- `PUT /stories/{story-id}/tasks/{task-id}` - update_story_task()
- `DELETE /stories/{story-id}/tasks/{task-id}` - delete_story_task()

**Required models:**
- Task
- CreateTaskInput
- UpdateTaskInput

### 1.3 Milestones
**Endpoints to implement:**
- `GET /milestones` - list_milestones()
- `POST /milestones` - create_milestone()
- `GET /milestones/{milestone-id}` - get_milestone()
- `PUT /milestones/{milestone-id}` - update_milestone()
- `DELETE /milestones/{milestone-id}` - delete_milestone()
- `GET /milestones/{milestone-id}/epics` - list_milestone_epics()
- `GET /categories/{category-id}/milestones` - list_category_milestones()

**Required models:**
- Milestone
- CreateMilestoneInput
- UpdateMilestoneInput

### 1.4 Custom Fields
**Endpoints to implement:**
- `GET /custom-fields` - list_custom_fields()
- `GET /custom-fields/{custom-field-id}` - get_custom_field()
- `PUT /custom-fields/{custom-field-id}` - update_custom_field()
- `DELETE /custom-fields/{custom-field-id}` - delete_custom_field()

**Required models:**
- CustomField
- UpdateCustomFieldInput

## Phase 2: Priority 2 - Enhanced Functionality (Week 2)

### 2.1 Bulk Operations
**Endpoints to implement:**
- `POST /stories/bulk` - create_stories_bulk()
- `PUT /stories/bulk` - update_stories_bulk()
- `DELETE /stories/bulk` - delete_stories_bulk()

**Required models:**
- BulkCreateStoriesInput
- BulkUpdateStoriesInput

### 2.2 Entity Templates
**Endpoints to implement:**
- `GET /entity-templates` - list_entity_templates()
- `POST /entity-templates` - create_entity_template()
- `GET /entity-templates/{template-id}` - get_entity_template()
- `PUT /entity-templates/{template-id}` - update_entity_template()
- `DELETE /entity-templates/{template-id}` - delete_entity_template()
- `PUT /entity-templates/disable` - disable_entity_templates()
- `PUT /entity-templates/enable` - enable_entity_templates()
- `POST /stories/from-template` - create_story_from_template()

**Required models:**
- EntityTemplate
- CreateEntityTemplateInput
- UpdateEntityTemplateInput

### 2.3 Missing Update Methods
**Endpoints to implement:**
- `PUT /labels/{label-id}` - update_label()

**Required models:**
- UpdateLabelInput

### 2.4 Pagination Support
**Endpoints to implement:**
- `GET /epics/paginated` - list_epics_paginated()

## Phase 3: Priority 3 - Integration Features (Week 3)

### 3.1 Story History
**Endpoints to implement:**
- `GET /stories/{story-id}/history` - get_story_history()

### 3.2 Health Tracking
**Endpoints to implement:**
- `GET /epics/{epic-id}/health` - get_epic_health()
- `GET /epics/{epic-id}/health-history` - get_epic_health_history()
- `GET /health/{health-id}` - get_health()

### 3.3 External Links
**Endpoints to implement:**
- `GET /external-link/stories` - list_external_link_stories()

### 3.4 Integrations
**Endpoints to implement:**
- `GET /integrations/webhook` - list_webhooks()
- `GET /integrations/webhook/{webhook-id}` - get_webhook()
- `DELETE /epics/{epic-id}/unlink-productboard` - unlink_epic_from_productboard()

## Phase 4: Priority 4 - Convenience Features (Week 4)

### 4.1 Related Entity Endpoints
**Endpoints to implement:**
- `GET /projects/{project-id}/stories` - list_project_stories()
- `GET /groups/{group-id}/stories` - list_group_stories()
- `GET /labels/{label-id}/stories` - list_label_stories()
- `GET /labels/{label-id}/epics` - list_label_epics()
- `GET /iterations/{iteration-id}/stories` - list_iteration_stories()
- `GET /epics/{epic-id}/stories` - list_epic_stories()
- `GET /objectives/{objective-id}/epics` - list_objective_epics()
- `GET /categories/{category-id}/objectives` - list_category_objectives()

### 4.2 Search Enhancements
**Endpoints to implement:**
- `GET /search` - Enhanced search (already exists but needs documentation)
- `GET /search/iterations` - search_iterations()
- `GET /search/milestones` - search_milestones()
- `GET /search/objectives` - search_objectives()

### 4.3 Workflow State Management
**Endpoints to implement:**
- `PUT /iterations/disable` - disable_iterations()
- `PUT /iterations/enable` - enable_iterations()

### 4.4 Comment Reactions
**Endpoints to implement:**
- `POST /stories/{story-id}/comments/{comment-id}/reactions` - create_comment_reaction()
- `DELETE /stories/{story-id}/comments/{comment-id}/reactions` - delete_comment_reaction()
- `DELETE /stories/{story-id}/comments/{comment-id}/unlink-from-slack` - unlink_comment_from_slack()

## Implementation Guidelines

1. **Model Creation/Updates**:
   - Check if models already exist in models.py
   - Create new dataclasses for missing models
   - Ensure all models have proper from_json() methods
   - Add appropriate type hints

2. **Method Naming Convention**:
   - Use consistent naming: `{action}_{entity}_{sub_entity}`
   - Examples: `list_story_comments`, `create_epic_comment`

3. **Error Handling**:
   - Maintain existing error handling patterns
   - Let requests.raise_for_status() handle HTTP errors

4. **Testing**:
   - Add unit tests for each new endpoint
   - Include integration tests where appropriate
   - Test error cases and edge conditions

5. **Documentation**:
   - Add docstrings to all new methods
   - Update README with new functionality examples
   - Keep API_COVERAGE_REPORT.md updated

## Success Metrics
- All Priority 1 endpoints implemented and tested
- API coverage increased from 45% to 75%+
- All new endpoints have corresponding tests
- Documentation updated for new features