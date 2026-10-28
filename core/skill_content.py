"""Editable starter content; all statements describe learning, not employment."""

LEGACY_DESCRIPTIONS = {
    'administrative': 'Practicing clear, consistent workflows through independent sample projects.',
    'tools': 'A tool I am practicing or learning for everyday administrative tasks.',
}
AI_LEGACY = 'Practicing AI-assisted drafting, brainstorming, and task organization, with careful review of outputs.'

# Name, icon, short purpose, detail, practical tasks, commonly used tools.
ADMINISTRATIVE = [
    (
        'Data Entry', 'table-2',
        'Practicing accurate data input and consistent spreadsheet records.',
        'I am developing a careful approach to entering and updating information. Practice includes spreadsheet formatting, sorting and filtering, and checking that records stay complete and consistent with the source.',
        ['Enter fictional records using consistent dates and labels.', 'Format headers and columns for easy scanning.', 'Sort and filter records to find specific information.', 'Check missing values, duplicate IDs, and typing errors.'],
        ['Microsoft Excel', 'Google Sheets'],
    ),
    (
        'Email Management', 'mail',
        'Learning to organize an inbox and draft clear, courteous responses.',
        'I am practicing an inbox routine that separates urgent requests, follow-ups, and reference messages. I focus on meaningful labels, appropriate email etiquette, and reviewing recipients and attachments before sending.',
        ['Group practice messages with folders or labels.', 'Prioritize requests by urgency and required action.', 'Draft concise responses with a clear subject and next step.', 'Prepare polite follow-ups and review tone before sending.'],
        ['Gmail', 'Outlook'],
    ),
    (
        'Calendar Scheduling', 'calendar-days',
        'Practicing organized appointments, reminders, and conflict-free schedules.',
        'I am learning to coordinate meeting times by checking availability, time zones, and existing commitments. My practice calendars include deadlines, preparation time, reminders, and space between appointments.',
        ['Check availability before suggesting appointment times.', 'Add clear meeting titles, dates, time zones, and agendas.', 'Set reminders for meetings and upcoming deadlines.', 'Review overlaps and confirm changes before updating invitations.'],
        ['Google Calendar', 'Outlook Calendar'],
    ),
    (
        'Document Preparation', 'file-text',
        'Developing clear formatting for everyday business documents.',
        'I am practicing documents that are easy to read and update: business letters, reports, meeting agendas, and notes. I focus on consistent headings, spacing, logical structure, and proofreading rather than decorative formatting.',
        ['Draft business letters with an appropriate greeting and closing.', 'Prepare agendas with topics, presenters, and time allocations.', 'Organize notes and reports using headings and bullet lists.', 'Check spelling, dates, layout, and the final exported document.'],
        ['Microsoft Word', 'Google Docs'],
    ),
    (
        'File Organization', 'folder-open',
        'Learning to keep digital records orderly and easy to find.',
        'I am developing habits for maintaining useful folder structures and clear file names. Practice includes organizing cloud documents, distinguishing drafts from final versions, and checking access before sharing a file.',
        ['Group sample documents by project, purpose, and date.', 'Apply consistent file names and version labels.', 'Archive outdated copies while keeping the current version clear.', 'Review sharing permissions and confirm that intended users can access files.'],
        ['Google Drive', 'OneDrive'],
    ),
    (
        'Online Research', 'search',
        'Practicing reliable research and concise, traceable summaries.',
        'I am learning to turn a research question into a structured set of findings. I compare sources for relevance, credibility, and publication date, record links, and distinguish verified information from assumptions.',
        ['Define the question and choose focused search terms.', 'Compare information across reliable sources.', 'Record source links, dates, and key facts in a research table.', 'Prepare a short summary noting gaps or conflicting findings.'],
        ['Google Search', 'Google Docs', 'Google Sheets'],
    ),
    (
        'Task Tracking', 'list-checks',
        'Practicing task lists that make priorities and deadlines visible.',
        'I am learning to break responsibilities into manageable steps and keep progress easy to review. My sample trackers distinguish pending, in-progress, and completed work, with due dates and notes about blockers.',
        ['Record each task with a clear next action and deadline.', 'Prioritize work by urgency, importance, and dependencies.', 'Update progress and flag tasks that need clarification.', 'Review the task list regularly and adjust the plan when priorities change.'],
        ['Google Sheets', 'Trello', 'Notion'],
    ),
    (
        'Professional Communication', 'messages-square',
        'Developing clear, respectful communication for remote teamwork.',
        'I am practicing professional email writing, active listening, and an appropriate workplace tone. I aim to ask useful questions, confirm my understanding, and share concise updates so others can act on the information.',
        ['Write messages with a clear purpose and requested next step.', 'Listen carefully and summarize decisions or instructions.', 'Ask questions when a deadline or expectation is unclear.', 'Prepare brief progress updates and courteous meeting follow-ups.'],
        ['Gmail', 'Zoom', 'Google Meet'],
    ),
]

TOOLS = [
    ('Microsoft Word', 'file-text', 'Practicing polished letters, reports, and meeting agendas.',
     'I am learning to use styles, headings, tables, and page layout to create consistent business documents. I review readability and formatting before exporting a shareable copy.',
     ['Format a business letter with consistent spacing.', 'Build a meeting agenda with timed discussion topics.', 'Organize a short report and proofread the final PDF.']),
    ('Microsoft Excel', 'table-2', 'Developing spreadsheet skills for accurate administrative records.',
     'I am practicing structured worksheets, basic formulas, sorting, and filtering with fictional data. I check formula results against the source and keep formatting consistent so records are easier to review.',
     ['Create an employee or expense tracker with clear headers.', 'Practice SUM and COUNT formulas and check the results.', 'Sort records, filter categories, and review missing information.']),
    ('Google Docs', 'file-pen-line', 'Learning collaborative document creation and clear formatting.',
     'I am practicing headings, lists, tables, and editing workflows for shared documents. I am also learning to use comments and suggestions to keep feedback separate from the original text.',
     ['Draft meeting notes and short business documents.', 'Use comments or suggestions for a practice review.', 'Check sharing permissions before distributing a document.']),
    ('Google Sheets', 'table-2', 'Practicing online spreadsheets and shared task tracking.',
     'I am learning to organize data, use basic formulas, and maintain readable online trackers. Practice includes collaboration habits such as clear column names, consistent entries, and checking access settings.',
     ['Build a task tracker with status and due-date columns.', 'Practice simple formulas, sorting, and filters.', 'Review entries and sharing settings in a sample collaboration workflow.']),
    ('Gmail', 'mail', 'Practicing organized email and professional correspondence.',
     'I am learning to use labels, search, and filters to keep messages accessible. Draft exercises focus on clear subjects, appropriate tone, accurate recipients, and concise follow-up requests.',
     ['Organize sample correspondence with labels and filters.', 'Draft a meeting confirmation and a follow-up email.', 'Review recipients, attachments, and wording before sending.']),
    ('Google Calendar', 'calendar-days', 'Learning scheduling, reminders, and availability management.',
     'I am practicing events with clear timing, time zones, descriptions, and reminders. Sample schedules help me check availability and plan invitations without overlapping commitments.',
     ['Create a fictional weekly schedule with focus time and breaks.', 'Add meeting details, reminders, and deadlines.', 'Check availability before preparing or revising invitations.']),
    ('Google Drive', 'folder-open', 'Practicing cloud file organization and thoughtful sharing.',
     'I am learning to structure folders, name files consistently, and locate documents quickly. I review viewing and editing permissions so a sharing workflow gives people only the access they need.',
     ['Arrange sample files into clearly named project folders.', 'Separate drafts, final documents, and reference material.', 'Check the intended audience and permissions before sharing.']),
    ('Canva', 'palette', 'Learning clear layouts for presentations and simple graphics.',
     'I am practicing simple visual communication using consistent typography, spacing, and colors. The focus is on readable slides and document layouts suitable for everyday administrative support.',
     ['Create a short presentation from a written outline.', 'Lay out a simple information sheet with readable text.', 'Check alignment, contrast, and export settings.']),
    ('Zoom', 'video', 'Practicing preparation and basic controls for virtual meetings.',
     'I am learning to prepare meeting invitations, check audio and video, and use meeting controls appropriately. Practice includes screen-sharing preparation and clear communication when joining a remote call.',
     ['Prepare a meeting invitation with timing and purpose.', 'Check microphone, camera, and mute controls before a call.', 'Practice sharing only the intended window and taking meeting notes.']),
    ('Google Meet', 'video', 'Learning video meeting coordination and screen sharing.',
     'I am practicing joining and organizing video meetings, including scheduling through Google Calendar. I focus on checking meeting details, using audio controls, and preparing the correct content to share.',
     ['Prepare a calendar event with a meeting link and agenda.', 'Check audio, camera, and meeting controls.', 'Practice presenting a document and recording follow-up actions.']),
    ('ChatGPT', 'messages-square', 'Practicing AI-assisted drafting and task organization with review.',
     'I am learning to provide clear instructions and use AI output as a starting draft. I check facts, tone, and relevance myself, and use fictional information rather than private workplace or personal data in practice exercises.',
     ['Brainstorm a checklist for a fictional administrative task.', 'Draft an email and revise it for accuracy and tone.', 'Compare a suggested summary against the original practice notes.']),
    ('Claude', 'messages-square', 'Learning to refine drafts and organize ideas with AI assistance.',
     'I am practicing clear prompts for document outlines, summaries, and correspondence. I review suggestions against the source material and retain responsibility for the final wording, using fictional or public practice content.',
     ['Outline a meeting agenda from fictional planning notes.', 'Review a draft for clarity and unnecessary wording.', 'Check a suggested summary for omissions or unsupported claims.']),
]


def seed_skills():
    """Update only untouched seed values; preserve custom text, even later blanks."""
    from core.models import Skill

    groups = [('administrative', ADMINISTRATIVE), ('tools', TOOLS)]
    for category, entries in groups:
        for order, entry in enumerate(entries):
            name, icon, description, detail, tasks, *related = entry
            content = {
                'description': description,
                'detailed_description': detail,
                'practical_tasks': '\n'.join(tasks),
                'related_tools': '\n'.join(related[0]) if related else '',
            }
            skill, created = Skill.objects.get_or_create(
                name=name,
                defaults={'category': category, 'icon': icon, 'display_order': order, **content},
            )
            baseline = skill.seed_baseline
            changed = []
            for field, default in content.items():
                current = getattr(skill, field)
                if field in baseline:
                    untouched = current == baseline[field]
                else:
                    untouched = not current
                    if field == 'description':
                        untouched |= current == LEGACY_DESCRIPTIONS[category]
                        untouched |= name in {'ChatGPT', 'Claude'} and current == AI_LEGACY
                if (created or untouched) and current != default:
                    setattr(skill, field, default)
                    changed.append(field)
            skill.seed_baseline = content
            skill.save(update_fields=[*changed, 'seed_baseline'])
