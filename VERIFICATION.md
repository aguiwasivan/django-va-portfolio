# Verification performed

## Light / Dark mode update

- Theme bootstrap loads before styles on all public pages; shared navigation includes a mobile-accessible Lucide toggle.
- All colors in `site.css` and `skills.css` use theme variables; both stylesheets are readable, formatted source.
- Standalone 500 page uses shared theme assets without database queries. No database changes or new dependencies.
- **26 Django tests passed**, including shared theme markup on all pages and themed 404/500 templates.
- **10 Node theme tests passed**: pre-render initialization, toggling, persistence across simulated page loads, system changes, blocked/invalid storage, tab synchronization, AA contrast for core color pairs, defined CSS tokens, reduced motion, and Lucide icon availability.
- Django system checks and migration drift checks passed; Tailwind build and WhiteNoise collection passed.
- Browser APIs are simulated in Node tests. Real browser screenshot, touch, keyboard, and layout verification remain unavailable in this environment; desktop/mobile appearance still merits a manual review.

## Skills & Tools update

- Added and applied additive migration `core.0002` for descriptions, practical tasks, related tools, and seed-default tracking.
- Preserved Ivan's profile/photo and all existing skills; 8 administrative skills and 12 digital tools have detailed content.
- Added tests for database-rendered details, Admin editing, legacy default upgrades, custom content preservation, intentionally cleared fields, and future default refreshes.
- Native HTML details/summary provides expansion and keyboard behavior without JavaScript; CSS switches View Details / Show Less labels.
- Responsive grid uses three columns on desktop, two below 1050px, and one below 640px. Browser interaction and visual checks remain unavailable; native interaction and responsive appearance require a manual browser check.
- Current suite: **24 tests passed**. System checks, migration drift check, Tailwind build, and static collection passed.

- Python 3.13; Django 5.2.18. Exact installed packages: `requirements.lock.txt`.
- Initial migrations generated and applied to local SQLite.
- `seed_portfolio` run repeatedly; one profile, 18 skills/tools, four practice projects, and two sample attachments.
- Tailwind compiled; Lucide bundle, source map, and license vendored locally.
- `manage.py test`: **19 tests passed**.
- `manage.py check`: no issues.
- `manage.py check --deploy` with `DJANGO_DEBUG=False`: no issues.
- `manage.py makemigrations --check --dry-run`: no changes detected.
- `manage.py collectstatic --noinput`: passed, including manifest hashing and compression.
- `node --check static/js/site.js`: passed.
- Live local HTTP checks: all five main pages, four project detail pages, robots.txt, sitemap.xml, CSS, JavaScript, placeholder image, and social card returned 200 with nonempty bodies.
- CSV and PDF download contents, resume handling, contact validation/CSRF/throttling/honeypot, SMTP fallback, and admin permissions verified by tests.

Browser visual and interaction testing was not available in this environment. SMTP delivery and PostgreSQL connectivity require the owner's production services and were not exercised against live accounts. No production deployment or administrator account was created. Responsive layouts, reduced-motion behavior, and keyboard interactions are implemented but should receive a browser review before public launch.

The machine has an unrelated global `DEBUG=release` variable. This project deliberately uses `DJANGO_DEBUG` so local configuration remains predictable. Test files use Django's in-memory storage to avoid Windows temporary-directory ACL restrictions while still exercising the actual file download views.
