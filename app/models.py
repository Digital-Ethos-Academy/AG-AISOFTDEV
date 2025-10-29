# models.py
# SQLAlchemy ORM Models for the Employee Onboarding Tool
# Description: This file contains the SQLAlchemy ORM models that map to the
#              Employee Onboarding Tool's database schema.

from __future__ import annotations

import datetime
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    PrimaryKeyConstraint,
    String,
    Table,
    Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""
    pass


# Association table for the many-to-many relationship between OnboardingPlan and Template
plan_templates_table = Table(
    "plan_templates",
    Base.metadata,
    Column("plan_id", Integer, ForeignKey("onboarding_plans.plan_id", ondelete="CASCADE"), primary_key=True),
    Column("template_id", Integer, ForeignKey("templates.template_id", ondelete="CASCADE"), primary_key=True),
)

# Association table for the many-to-many relationship between ScheduleEvent and User (attendees)
event_attendees_table = Table(
    "event_attendees",
    Base.metadata,
    Column("event_id", Integer, ForeignKey("schedule_events.event_id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True),
)


class User(Base):
    """Represents a user in the system (e.g., new hire, manager, HR admin)."""
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    sso_identifier: Mapped[Optional[str]] = mapped_column(Text, unique=True)
    role: Mapped[str] = mapped_column(Text, nullable=False)
    manager_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"))
    hire_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    # Self-referential relationship for manager/reports
    manager: Mapped[Optional["User"]] = relationship(remote_side=[user_id], back_populates="reports")
    reports: Mapped[List["User"]] = relationship(back_populates="manager")

    # Relationships to other tables
    onboarding_plan_as_new_hire: Mapped[Optional["OnboardingPlan"]] = relationship(
        foreign_keys="OnboardingPlan.new_hire_user_id", back_populates="new_hire"
    )
    onboarding_plan_as_buddy: Mapped[List["OnboardingPlan"]] = relationship(
        foreign_keys="OnboardingPlan.buddy_user_id", back_populates="buddy"
    )
    assigned_tasks: Mapped[List["AssignedTask"]] = relationship(
        foreign_keys="AssignedTask.assignee_user_id", back_populates="assignee"
    )
    created_templates: Mapped[List["Template"]] = relationship(
        foreign_keys="Template.created_by_user_id", back_populates="creator"
    )
    created_resources: Mapped[List["Resource"]] = relationship(
        foreign_keys="Resource.created_by_user_id", back_populates="creator"
    )
    created_events: Mapped[List["ScheduleEvent"]] = relationship(
        foreign_keys="ScheduleEvent.created_by_user_id", back_populates="creator"
    )
    attending_events: Mapped[List["ScheduleEvent"]] = relationship(
        secondary=event_attendees_table, back_populates="attendees"
    )


class Template(Base):
    """Represents a reusable template for onboarding, playbooks, etc."""
    __tablename__ = "templates"

    template_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    template_type: Mapped[str] = mapped_column(Text, nullable=False)
    created_by_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    creator: Mapped["User"] = relationship(foreign_keys=[created_by_user_id], back_populates="created_templates")
    tasks: Mapped[List["TemplateTask"]] = relationship(back_populates="template", cascade="all, delete-orphan")
    onboarding_plans: Mapped[List["OnboardingPlan"]] = relationship(
        secondary=plan_templates_table, back_populates="templates"
    )


class TemplateTask(Base):
    """Represents a single task item within a template."""
    __tablename__ = "template_tasks"

    template_task_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    template_id: Mapped[int] = mapped_column(Integer, ForeignKey("templates.template_id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    default_due_days_offset: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    default_assignee_role: Mapped[str] = mapped_column(Text, nullable=False)
    is_compliance_task: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    template: Mapped["Template"] = relationship(back_populates="tasks")
    assigned_tasks: Mapped[List["AssignedTask"]] = relationship(back_populates="template_task")


class OnboardingPlan(Base):
    """Represents a specific onboarding plan for a new hire."""
    __tablename__ = "onboarding_plans"

    plan_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    new_hire_user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, unique=True
    )
    buddy_user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"))
    start_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    new_hire: Mapped["User"] = relationship(
        foreign_keys=[new_hire_user_id], back_populates="onboarding_plan_as_new_hire"
    )
    buddy: Mapped[Optional["User"]] = relationship(foreign_keys=[buddy_user_id], back_populates="onboarding_plan_as_buddy")
    templates: Mapped[List["Template"]] = relationship(secondary=plan_templates_table, back_populates="onboarding_plans")
    assigned_tasks: Mapped[List["AssignedTask"]] = relationship(back_populates="plan", cascade="all, delete-orphan")
    schedule_events: Mapped[List["ScheduleEvent"]] = relationship(back_populates="plan", cascade="all, delete-orphan")
    survey_responses: Mapped[List["SurveyResponse"]] = relationship(back_populates="plan", cascade="all, delete-orphan")


class AssignedTask(Base):
    """Represents a task assigned to a specific user as part of an onboarding plan."""
    __tablename__ = "assigned_tasks"

    assigned_task_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plan_id: Mapped[int] = mapped_column(Integer, ForeignKey("onboarding_plans.plan_id", ondelete="CASCADE"), nullable=False)
    assignee_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    template_task_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("template_tasks.template_task_id", ondelete="SET NULL")
    )
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text, nullable=False)
    due_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    completed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    plan: Mapped["OnboardingPlan"] = relationship(back_populates="assigned_tasks")
    assignee: Mapped["User"] = relationship(foreign_keys=[assignee_user_id], back_populates="assigned_tasks")
    template_task: Mapped[Optional["TemplateTask"]] = relationship(back_populates="assigned_tasks")


class Resource(Base):
    """Represents a learning or informational resource (e.g., link, document)."""
    __tablename__ = "resources"

    resource_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    resource_type: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_by_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"), nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    creator: Mapped["User"] = relationship(foreign_keys=[created_by_user_id], back_populates="created_resources")


class ScheduleEvent(Base):
    """Represents a scheduled event, like a meeting or a check-in."""
    __tablename__ = "schedule_events"

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plan_id: Mapped[int] = mapped_column(Integer, ForeignKey("onboarding_plans.plan_id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    start_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    location_or_link: Mapped[Optional[str]] = mapped_column(Text)
    created_by_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    plan: Mapped["OnboardingPlan"] = relationship(back_populates="schedule_events")
    creator: Mapped["User"] = relationship(foreign_keys=[created_by_user_id], back_populates="created_events")
    attendees: Mapped[List["User"]] = relationship(secondary=event_attendees_table, back_populates="attending_events")


class SurveyResponse(Base):
    """Represents a feedback survey response from a new hire."""
    __tablename__ = "survey_responses"

    response_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plan_id: Mapped[int] = mapped_column(Integer, ForeignKey("onboarding_plans.plan_id", ondelete="CASCADE"), nullable=False)
    nps_score: Mapped[Optional[int]] = mapped_column(Integer)
    feedback_text: Mapped[Optional[str]] = mapped_column(Text)
    submitted_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    plan: Mapped["OnboardingPlan"] = relationship(back_populates="survey_responses")
