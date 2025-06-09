#!/usr/bin/python3
# -*- coding: utf-8 -*-
import click
from useshortcut.client import APIClient
import useshortcut.models as models


@click.group()
@click.option(
    "--token", envvar="SHORTCUT_API_TOKEN", required=True, help="Shortcut API token"
)
@click.pass_context
def cli(ctx, token):
    """CLI tool for interacting with the Shortcut API"""
    ctx.obj = APIClient(api_token=token)


@cli.group()
def stories():
    """Manage Shortcut stories"""
    pass


@stories.command()
@click.option("--query", required=True, help="Search query for stories")
@click.pass_obj
def search(client, query):
    """Search for stories"""
    search_params = models.SearchInputs(query=query)
    results = client.search_stories(search_params)
    for story in results.data:
        click.echo(f"[{story.id}] {story.name}")


@stories.command()
@click.option("--name", required=True, help="Name of the story")
@click.option("--workflow-id", required=True, type=int, help="Workflow state ID")
@click.pass_obj
def create(client, name, workflow_id):
    """Create a new story"""
    story = client.create_story(
        models.StoryInput(name=name, workflow_state_id=workflow_id)
    )
    click.echo(f"Created story [{story.id}] {story.name}")


@cli.command()
@click.pass_obj
def workflows(client):
    """List all workflows"""
    workflows = client.list_workflows()
    for workflow in workflows:
        click.echo(f"[{workflow.id}] {workflow.name}")
        for state in workflow.states:
            click.echo(f"  - [{state.id}] {state.name}")


@cli.command()
@click.pass_obj
def me(client):
    """Get current member info"""
    member = client.get_current_member()
    click.echo(f"Name: {member.profile.name}")
    click.echo(f"Mention: {member.mention_name}")


# Epics group
@cli.group()
def epics():
    """Manage Shortcut epics"""
    pass


@epics.command()
@click.pass_obj
def list(client):
    """List all epics"""
    epics = client.list_epics()
    for epic in epics:
        click.echo(f"[{epic.id}] {epic.name}")


@epics.command()
@click.option("--name", required=True, help="Name of the epic")
@click.pass_obj
def create(client, name):
    """Create a new epic"""
    epic = client.create_epic(models.EpicInput(name=name))
    click.echo(f"Created epic [{epic.id}] {epic.name}")


# Iterations group
@cli.group()
def iterations():
    """Manage Shortcut iterations"""
    pass


@iterations.command()
@click.pass_obj
def list(client):
    """List all iterations"""
    iterations = client.list_iterations()
    for iteration in iterations:
        click.echo(f"[{iteration.id}] {iteration.name}")


@iterations.command()
@click.option("--name", required=True, help="Name of the iteration")
@click.option("--start-date", required=True, help="Start date (YYYY-MM-DD)")
@click.option("--end-date", required=True, help="End date (YYYY-MM-DD)")
@click.pass_obj
def create(client, name, start_date, end_date):
    """Create a new iteration"""
    iteration = client.create_iteration(
        models.CreateIterationInput(name=name, start_date=start_date, end_date=end_date)
    )
    click.echo(f"Created iteration [{iteration.id}] {iteration.name}")


# Labels group
@cli.group()
def labels():
    """Manage Shortcut labels"""
    pass


@labels.command()
@click.pass_obj
def list(client):
    """List all labels"""
    labels = client.list_labels()
    for label in labels:
        click.echo(f"[{label.id}] {label.name}")


@labels.command()
@click.option("--name", required=True, help="Name of the label")
@click.option("--color", help="Color code for the label")
@click.option("--description", help="Description of the label")
@click.pass_obj
def create(client, name, color, description):
    """Create a new label"""
    label = client.create_label(
        models.CreateLabelInput(name=name, color=color, description=description)
    )
    click.echo(f"Created label [{label.id}] {label.name}")


# Groups group
@cli.group()
def groups():
    """Manage Shortcut groups"""
    pass


@groups.command()
@click.pass_obj
def list(client):
    """List all groups"""
    groups = client.list_groups()
    for group in groups:
        click.echo(f"[{group.id}] {group.name}")


@groups.command()
@click.option("--name", required=True, help="Name of the group")
@click.option("--mention-name", required=True, help="Mention name for the group")
@click.pass_obj
def create(client, name, mention_name):
    """Create a new group"""
    group = client.create_group(
        models.CreateGroupInput(name=name, mention_name=mention_name)
    )
    click.echo(f"Created group [{group.id}] {group.name}")


# Members group
@cli.group()
def members():
    """Manage Shortcut members"""
    pass


@members.command()
@click.pass_obj
def list(client):
    """List all members"""
    members = client.list_members()
    for member in members:
        click.echo(f"[{member.id}] {member.profile.name}")


# Projects group
@cli.group()
def projects():
    """Manage Shortcut projects"""
    pass


@projects.command()
@click.pass_obj
def list(client):
    """List all projects"""
    projects = client.list_projects()
    for project in projects:
        click.echo(f"[{project.id}] {project.name}")


# Categories group
@cli.group()
def categories():
    """Manage Shortcut categories"""
    pass


@categories.command()
@click.pass_obj
def list(client):
    """List all categories"""
    categories = client.list_categories()
    for category in categories:
        click.echo(f"[{category.id}] {category.name}")


@categories.command()
@click.option("--name", required=True, help="Name of the category")
@click.pass_obj
def create(client, name):
    """Create a new category"""
    category = client.create_category(models.CreateCategoryInput(name=name))
    click.echo(f"Created category [{category.id}] {category.name}")


if __name__ == "__main__":
    cli()
