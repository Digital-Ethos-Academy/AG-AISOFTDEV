CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    sso_identifier TEXT UNIQUE,
    role TEXT NOT NULL CHECK(role IN ('new_hire', 'manager', 'hr_admin')),
    manager_id INTEGER,
    hire_date DATE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (manager_id) REFERENCES users(user_id) ON DELETE SET NULL
);

CREATE TABLE templates (
    template_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    template_type TEXT NOT NULL CHECK(template_type IN ('ONBOARDING_JOURNEY', 'ROLE_PLAYBOOK', '30_60_90_PLAN')),
    created_by_user_id INTEGER NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by_user_id) REFERENCES users(user_id)
);

CREATE TABLE template_tasks (
    template_task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    template_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    default_due_days_offset INTEGER NOT NULL DEFAULT 0,
    default_assignee_role TEXT NOT NULL CHECK(default_assignee_role IN ('new_hire', 'manager', 'buddy', 'hr_admin', 'it')),
    is_compliance_task INTEGER NOT NULL DEFAULT 0,
    display_order INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (template_id) REFERENCES templates(template_id) ON DELETE CASCADE
);

CREATE TABLE onboarding_plans (
    plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    new_hire_user_id INTEGER NOT NULL UNIQUE,
    buddy_user_id INTEGER,
    start_date DATE NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('preboarding', 'active', 'completed')),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (new_hire_user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (buddy_user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

CREATE TABLE plan_templates (
    plan_id INTEGER NOT NULL,
    template_id INTEGER NOT NULL,
    PRIMARY KEY (plan_id, template_id),
    FOREIGN KEY (plan_id) REFERENCES onboarding_plans(plan_id) ON DELETE CASCADE,
    FOREIGN KEY (template_id) REFERENCES templates(template_id) ON DELETE CASCADE
);

CREATE TABLE assigned_tasks (
    assigned_task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_id INTEGER NOT NULL,
    assignee_user_id INTEGER NOT NULL,
    template_task_id INTEGER,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL CHECK(status IN ('pending', 'completed')),
    due_date DATE,
    completed_at DATETIME,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (plan_id) REFERENCES onboarding_plans(plan_id) ON DELETE CASCADE,
    FOREIGN KEY (assignee_user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (template_task_id) REFERENCES template_tasks(template_task_id) ON DELETE SET NULL
);

CREATE TABLE resources (
    resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    resource_type TEXT NOT NULL CHECK(resource_type IN ('LINK', 'DOCUMENT', 'PAGE')),
    content TEXT NOT NULL,
    created_by_user_id INTEGER NOT NULL,
    is_published INTEGER NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by_user_id) REFERENCES users(user_id)
);

CREATE TABLE schedule_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    location_or_link TEXT,
    created_by_user_id INTEGER NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (plan_id) REFERENCES onboarding_plans(plan_id) ON DELETE CASCADE,
    FOREIGN KEY (created_by_user_id) REFERENCES users(user_id)
);

CREATE TABLE event_attendees (
    event_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (event_id, user_id),
    FOREIGN KEY (event_id) REFERENCES schedule_events(event_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE survey_responses (
    response_id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_id INTEGER NOT NULL,
    nps_score INTEGER CHECK(nps_score >= 0 AND nps_score <= 10),
    feedback_text TEXT,
    submitted_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (plan_id) REFERENCES onboarding_plans(plan_id) ON DELETE CASCADE
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_manager_id ON users(manager_id);
CREATE INDEX idx_template_tasks_template_id ON template_tasks(template_id);
CREATE INDEX idx_onboarding_plans_new_hire_id ON onboarding_plans(new_hire_user_id);
CREATE INDEX idx_assigned_tasks_plan_id ON assigned_tasks(plan_id);
CREATE INDEX idx_assigned_tasks_assignee_id_status ON assigned_tasks(assignee_user_id, status);
CREATE INDEX idx_schedule_events_plan_id_start_time ON schedule_events(plan_id, start_time);