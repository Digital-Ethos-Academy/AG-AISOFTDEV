INSERT INTO users (full_name, email, sso_identifier, role, manager_id, hire_date, created_at, updated_at) VALUES
('Sarah Chen', 'sarah.chen@momentum.com', 'auth0|sarah.chen', 'hr_admin', NULL, '2022-01-15', '2022-01-10 09:00:00', '2022-01-10 09:00:00'),
('David Martinez', 'david.martinez@momentum.com', 'auth0|david.martinez', 'manager', NULL, '2022-03-20', '2022-03-15 11:30:00', '2022-03-15 11:30:00'),
('Emily White', 'emily.white@momentum.com', 'auth0|emily.white', 'manager', NULL, '2022-05-11', '2022-05-01 14:00:00', '2022-05-01 14:00:00'),
('Amelia Johnson', 'amelia.johnson@momentum.com', 'auth0|amelia.johnson', 'new_hire', 2, '2023-10-23', '2023-10-01 10:00:00', '2023-10-01 10:00:00'),
('Ben Carter', 'ben.carter@momentum.com', 'auth0|ben.carter', 'new_hire', 3, '2023-10-30', '2023-10-15 16:20:00', '2023-10-15 16:20:00'),
('Chloe Davis', 'chloe.davis@momentum.com', 'auth0|chloe.davis', 'new_hire', 2, '2023-11-06', '2023-10-25 09:15:00', '2023-10-25 09:15:00'),
('Michael Lee', 'michael.lee@momentum.com', 'auth0|michael.lee', 'manager', 2, '2023-02-01', '2023-01-20 12:00:00', '2023-01-20 12:00:00'),
('Olivia Rodriguez', 'olivia.rodriguez@momentum.com', 'auth0|olivia.rodriguez', 'manager', 3, '2023-04-10', '2023-04-01 13:45:00', '2023-04-01 13:45:00'),
('Leo Garcia', 'leo.garcia@momentum.com', 'auth0|leo.garcia', 'new_hire', 3, '2023-08-01', '2023-07-20 11:00:00', '2023-09-15 17:00:00');

INSERT INTO templates (name, description, template_type, created_by_user_id, created_at, updated_at) VALUES
('General Company Onboarding', 'Standard tasks for all new hires at Momentum.', 'ONBOARDING_JOURNEY', 1, '2023-01-05 10:00:00', '2023-09-15 14:30:00'),
('Engineering Role Playbook', 'Specific tasks and resources for new software engineers.', 'ROLE_PLAYBOOK', 1, '2023-02-10 11:00:00', '2023-08-20 16:00:00'),
('Sales 30-60-90 Plan', 'A structured plan to ramp up new sales team members.', '30_60_90_PLAN', 1, '2023-03-15 09:30:00', '2023-03-15 09:30:00');

INSERT INTO template_tasks (template_id, title, description, default_due_days_offset, default_assignee_role, is_compliance_task, display_order) VALUES
(1, 'Complete HR Paperwork', 'Fill out I-9, W-4, and direct deposit forms in the HR portal.', -5, 'new_hire', 1, 1),
(1, 'Review Company Handbook', 'Read the employee handbook and sign the acknowledgement form.', 3, 'new_hire', 1, 2),
(1, 'Set up laptop and accounts', 'Work with IT to get your machine and access to key systems.', 0, 'it', 0, 3),
(1, 'Schedule 1-on-1 with manager', 'Set up a recurring weekly check-in with your direct manager.', 1, 'manager', 0, 4),
(1, 'Meet your onboarding buddy', 'Grab coffee or have a virtual chat with your assigned buddy.', 2, 'new_hire', 0, 5),
(2, 'Set up local dev environment', 'Follow the guide on the engineering wiki to get your local environment running.', 2, 'new_hire', 0, 1),
(2, 'Review coding standards', 'Familiarize yourself with our team''s coding conventions and best practices.', 3, 'new_hire', 0, 2),
(2, 'First quick win project: Update team wiki', 'Fix a typo or add a missing link to the team wiki to complete your first PR.', 5, 'new_hire', 0, 3),
(3, 'Complete CRM Training', 'Go through the mandatory Salesforce training modules.', 7, 'new_hire', 0, 1),
(3, 'Shadow a discovery call', 'Listen in on a discovery call with a senior Account Executive.', 10, 'new_hire', 0, 2);

INSERT INTO onboarding_plans (new_hire_user_id, buddy_user_id, start_date, status, created_at, updated_at) VALUES
(4, 7, '2023-10-23', 'active', '2023-10-02 11:00:00', '2023-10-24 09:05:00'),
(5, 8, '2023-10-30', 'active', '2023-10-16 10:00:00', '2023-10-30 14:00:00'),
(6, 7, '2023-11-06', 'preboarding', '2023-10-25 10:00:00', '2023-10-25 10:00:00'),
(9, 8, '2023-08-01', 'completed', '2023-07-21 14:00:00', '2023-09-10 16:00:00');

INSERT INTO plan_templates (plan_id, template_id) VALUES
(1, 1),
(1, 2),
(2, 1),
(2, 3),
(3, 1),
(4, 1);

INSERT INTO assigned_tasks (plan_id, assignee_user_id, template_task_id, title, description, status, due_date, completed_at, created_at, updated_at) VALUES
(1, 4, 1, 'Complete HR Paperwork', 'Fill out I-9, W-4, and direct deposit forms in the HR portal.', 'completed', '2023-10-18', '2023-10-17 15:30:00', '2023-10-02 11:00:01', '2023-10-17 15:30:00'),
(1, 4, 6, 'Set up local dev environment', 'Follow the guide on the engineering wiki to get your local environment running.', 'pending', '2023-10-25', NULL, '2023-10-02 11:00:02', '2023-10-24 10:00:00'),
(1, 2, 4, 'Schedule 1-on-1 with manager', 'Set up a recurring weekly check-in with Amelia.', 'completed', '2023-10-24', '2023-10-23 11:45:00', '2023-10-02 11:00:03', '2023-10-23 11:45:00'),
(1, 4, 5, 'Meet your onboarding buddy', 'Grab coffee or have a virtual chat with Michael.', 'pending', '2023-10-25', NULL, '2023-10-02 11:00:04', '2023-10-02 11:00:04'),
(2, 5, 1, 'Complete HR Paperwork', 'Fill out I-9, W-4, and direct deposit forms in the HR portal.', 'completed', '2023-10-25', '2023-10-24 11:00:00', '2023-10-16 10:00:01', '2023-10-24 11:00:00'),
(2, 5, 9, 'Complete CRM Training', 'Go through the mandatory Salesforce training modules.', 'pending', '2023-11-06', NULL, '2023-10-16 10:00:02', '2023-10-16 10:00:02'),
(3, 6, 1, 'Complete HR Paperwork', 'Fill out I-9, W-4, and direct deposit forms in the HR portal.', 'pending', '2023-11-01', NULL, '2023-10-25 10:00:01', '2023-10-25 10:00:01'),
(4, 9, 2, 'Review Company Handbook', 'Read the employee handbook and sign the acknowledgement form.', 'completed', '2023-08-04', '2023-08-03 10:22:00', '2023-07-21 14:00:01', '2023-08-03 10:22:00'),
(1, 4, NULL, 'Join the #engineering Slack channel', 'Introduce yourself in the main engineering team channel.', 'completed', '2023-10-23', '2023-10-23 09:30:15', '2023-10-23 09:10:00', '2023-10-23 09:30:15');

INSERT INTO resources (title, resource_type, content, created_by_user_id, is_published, created_at, updated_at) VALUES
('Company Handbook 2023', 'DOCUMENT', '/docs/handbook_v4.2.pdf', 1, 1, '2023-01-10 15:00:00', '2023-08-01 11:00:00'),
('Momentum Org Chart', 'PAGE', '<h1>Company Organization</h1><p>Our interactive org chart is hosted on Pingboard...</p>', 1, 1, '2023-02-01 12:00:00', '2023-10-15 10:00:00'),
('Employee Benefits Portal', 'LINK', 'https://benefits.zenefits.com/momentum', 1, 1, '2023-01-15 16:00:00', '2023-01-15 16:00:00'),
('Engineering Team Wiki', 'LINK', 'https://momentum.atlassian.net/wiki/spaces/ENG', 2, 1, '2023-05-20 10:00:00', '2023-09-30 14:00:00');

INSERT INTO schedule_events (plan_id, title, description, start_time, end_time, location_or_link, created_by_user_id, created_at) VALUES
(1, 'Engineering Team Welcome Lunch', 'A casual lunch to welcome Amelia to the team!', '2023-10-24 12:00:00', '2023-10-24 13:00:00', 'Cafeteria, Building A', 2, '2023-10-18 14:00:00'),
(1, 'IT Onboarding & Setup', 'Session with IT to get hardware and accounts configured.', '2023-10-23 09:30:00', '2023-10-23 11:00:00', 'IT Helpdesk, 3rd Floor', 1, '2023-10-10 16:00:00'),
(2, 'Sales Kick-off Meeting', 'Introduction to the sales team and Q4 goals.', '2023-10-30 10:00:00', '2023-10-30 11:00:00', 'https://zoom.us/j/123456789', 3, '2023-10-20 11:30:00'),
(2, 'Intro with Marketing Team', 'Meet the marketing leads to understand collaboration points.', '2023-11-01 14:00:00', '2023-11-01 14:30:00', 'Conference Room 4B', 3, '2023-10-26 09:00:00');

INSERT INTO event_attendees (event_id, user_id) VALUES
(1, 4),
(1, 2),
(1, 7),
(2, 4),
(3, 5),
(3, 3),
(3, 8),
(4, 5);

INSERT INTO survey_responses (plan_id, nps_score, feedback_text, submitted_at) VALUES
(4, 9, 'The entire process was very smooth. My buddy, Olivia, was fantastic and helped me get up to speed quickly. Having a clear task list from day one was a huge help!', '2023-08-31 10:15:00');