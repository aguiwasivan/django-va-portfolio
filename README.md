# Virtual Administrative Assistant Portfolio

A complete Django 5.2 LTS portfolio for an entry-level assistant. Five responsive pages, editable content, four honest practice projects, downloadable CSV/PDF samples, and a protected contact workflow. No professional history, testimonials, certifications, or proficiency scores are invented.

## Quick start (this prepared workspace)

Dependencies, local `.env`, SQLite migrations, sample content, and compiled frontend assets have been prepared. In Windows PowerShell:

```powershell
cd 'C:\Users\Toji(K)\Documents\portfolio'
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

Open http://127.0.0.1:8000/ and http://127.0.0.1:8000/admin/. Choose your own administrator credentials; none are seeded. Commands use the virtual environment directly, so changing PowerShell execution policy is unnecessary.

## Setup on a fresh checkout

Prerequisites: Python 3.12 or newer supported by Django 5.2 (Python 3.13 recommended), pip, and optionally Node.js 20+ to rebuild CSS or vendor icons. SQLite is included with Python. PostgreSQL is supported for deployment.

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/init_local.py
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_portfolio
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

If Python's pip bootstrap is unavailable but `uv` is installed, use `uv pip install --python .venv/Scripts/python.exe -r requirements.txt`. `.env.example` documents settings; `init_local.py` copies it with a cryptographically random secret and never overwrites an existing `.env`. Do not commit `.env`, media, contact data, or your SQLite database.

## Content management

Sign into Django Admin using your superuser account. Django groups and per-model permissions let you grant narrower access to other staff accounts. There is no public registration.

- **Profiles:** edit Your Name, title, biography, email, availability, LinkedIn and optional GitHub. Upload a JPEG/PNG/WebP portrait and a PDF resume. Only one profile can be created through Admin. The first profile supplies shared page content.
- **Skills:** add/edit/delete skills, choose administrative skills or digital tools, enter a Lucide icon name (for example `calendar-days`), short description, and display order. Lower order appears first. Under **Card content**, edit the detailed description, practical tasks (one per line), and related tools (one per line). The Skills & Tools page reads these fields directly from the database. Native **View Details / Show Less** sections work with a keyboard and without JavaScript. Wording should reflect practice or learning.
- **Projects:** edit title, category, slug, descriptions, tools and demonstrated skills (one per line). Select featured projects for the home page, order them, and upload thumbnails. Keep the Practice Project flag enabled for fictional work. Slugs are stable public URLs; changing one changes the URL.
- **Project attachments:** use the inline rows on a project to add a PDF or UTF-8 CSV, label, and matching file type. Download links appear on its detail page.
- **Structured previews:** the preview type selects spreadsheet, calendar, email, agenda, or generic text. Seeded `preview_data` is editable JSON; preserve its object keys and list structure. Use generic text for other project types. Django escapes all entered text; rich HTML is intentionally not accepted.
- **Contact messages:** view submissions, search/filter, mark read/unread individually or in bulk, and delete records according to your retention policy.

Until you upload a resume, the homepage clearly says it is not yet available. Missing email and social links are shown as unavailable, rather than linking to invented accounts. The illustrated portrait is explicitly a placeholder. Add your actual details before sharing publicly.

## Practice projects

1. **Employee Data Entry & Organization:** 15 fictional employees, six consistent columns, searchable preview, and a real UTF-8 CSV download. All addresses use the reserved `example.com` domain. Open the CSV in Excel or Sheets to sort/filter and apply spreadsheet formatting.
2. **Executive Calendar Management:** five non-overlapping days for November 2–6, 2026, in UTC; meetings, administrative tasks, lunch, focus blocks, and deadline reviews. Mobile presents one day per section.
3. **Professional Email Management:** three switchable fictional drafts (confirmation, rescheduling, follow-up), explicitly labeled as a demonstration with no connected inbox. Without JavaScript all drafts remain readable.
4. **Meeting Agenda & Document Preparation:** attendees, timed topics, presenters, and example action items; a real one-page PDF generated with ReportLab.

`seed_portfolio` uses stable slugs and unique skill names. Re-running preserves existing edits and avoids duplicate content and attachments. It recreates missing sample files. Do not rename seed slugs or skill names if you want those seed records to continue matching. The generated documents are initial samples; editing preview JSON does not regenerate a custom attachment—replace the attachment in Admin when updating the sample.

Skills include eight administrative skills and twelve digital tools, including ChatGPT and Claude. Starter descriptions live in `core/skill_content.py`. On the first upgrade, only empty content fields and exact recognized old generic descriptions receive new defaults. A private `seed_baseline` field records supplied defaults; later runs refresh a field only when it still equals its previous default. Customized text, intentionally cleared fields after the first upgrade, icons, order, and unrelated records are preserved. A manually entered value identical to a seed default is indistinguishable from that default. Related tools such as Outlook, OneDrive, Trello, and Notion are presented as common examples, not additional proficiency claims.

## Frontend

Semantic Django templates, Tailwind utilities, custom design CSS, Vanilla JavaScript, locally vendored Lucide, and Inter from Google Fonts with system-font fallback. No React or frontend runtime build service is required. Compiled CSS and the icon bundle are included. Google Fonts is the only third-party browser request; self-host fonts if your privacy policy requires it.

```powershell
npm.cmd ci --offline=false
npm.cmd run vendor
npm.cmd run build:css
```

Run the CSS command after adding Tailwind classes to templates. `static/css/site.css` contains the design system and responsive layouts. The icon license is retained in `static/js/lucide.LICENSE`. `scripts/build_social.py` regenerates the simple social preview image.

Accessibility includes a skip link, visible focus states, labeled forms, keyboard-friendly buttons, mobile menu expanded state and Escape handling, reduced-motion support, horizontally scrollable data tables, and functional navigation without animation. All project content is readable without JavaScript. Custom 404/500 templates, canonical URLs, SEO/Open Graph metadata, sitemap, and robots.txt are provided.

## Light and dark themes

The moon/sun button beside navigation switches the entire public portfolio, including project demonstrations, forms, expandable skill cards, and error pages. It stays visible beside the mobile menu. The accessible toggle has the stable name **Dark mode** and reports its state with `aria-pressed`; its tooltip describes the next action.

`static/js/theme.js` runs synchronously in the page head before styles load to avoid a flash of the wrong theme. It stores `light` or `dark` under the localStorage key `portfolio-theme`. Without a valid saved choice, it follows `prefers-color-scheme`, including live system changes. Explicit preferences survive refreshes and navigation; changes synchronize across tabs. When storage is blocked, switching still works on the current page, but cannot persist to another page. Clear that storage key to return to the system preference. With JavaScript disabled, the site remains usable in light mode and the inactive toggle is hidden.

`static/css/theme.css` defines light/dark semantic color tokens and `color-scheme`; `site.css` and `skills.css` consume these tokens. Color transitions take 250 ms and respect reduced-motion preferences. Images and downloadable documents are not recolored. The standalone 500 page uses the same theme assets without querying the database. Django Admin retains Django's built-in theme controls.

Run `npm.cmd run test:theme` for ten dependency-free runtime tests using Node's built-in test runner (and the existing PostCSS/Lucide build packages for CSS/icon assertions). They cover initialization, switching, storage failure, persistence, system changes, tab synchronization, core AA contrast pairs, defined CSS variables, reduced motion, and icon availability. These tests simulate browser APIs; they do not replace a real-browser visual review at desktop and mobile widths.

## Contact workflow and privacy

POST requests require a CSRF token. Django validates required fields, email, and lengths. A hidden honeypot blocks simple bots. A database-backed limit accepts at most five POST attempts per IP per hour, including invalid attempts. IPs are stored as keyed hashes, not raw addresses; old buckets are pruned on contact attempts. The atomic conditional counter works across workers. This is basic spam mitigation, not a replacement for edge rate limiting under attack.

Only `REMOTE_ADDR` is used; arbitrary forwarded headers are not trusted. Configure your trusted reverse proxy to provide the correct remote address, or visitors behind the proxy may share a limit. Add upstream rate limiting for the admin login and contact endpoint in production.

Valid submissions are stored before notification. Set `EMAIL_HOST`, port, username, password, TLS, `DEFAULT_FROM_EMAIL`, and `CONTACT_NOTIFICATION_EMAIL` in environment variables to enable SMTP notifications. Replies use the visitor's validated address; the sender remains your configured domain. SMTP failures are logged and do not discard messages. Without SMTP, messages remain accessible in Admin and no notification is attempted. Keep database backups private and delete contact records when no longer needed.

## Verification

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe manage.py test
.\.venv\Scripts\python.exe manage.py collectstatic --noinput
```

Tests cover public pages, project details and categories, contact validation/submission/CSRF/honeypot/rate limiting, SMTP success/failure, file downloads and upload validation, admin permissions, fictional schedule data, and idempotent seeding. Test media uses isolated in-memory storage and never overwrites your uploads.

## Production deployment

Use a Python WSGI/ASGI host, not a static site host. The included Waitress server supports Windows and Linux. Django's development server is for local development only. Follow the [Django deployment checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/).

1. Set `DJANGO_DEBUG=False`, a unique random `SECRET_KEY` of at least 50 characters, `ALLOWED_HOSTS=your-domain.example`, `SITE_URL=https://your-domain.example`, and `CSRF_TRUSTED_ORIGINS=https://your-domain.example`. The app refuses an obviously weak production secret. Generate a new secret locally with `python -c "import secrets; print(secrets.token_urlsafe(64))"` and store it in your host's secret manager.
2. Set `DATABASE_URL=postgres://USER:PASSWORD@HOST:5432/DBNAME` (URL-encode special characters). Append `?sslmode=require` when your provider requires TLS. Provision PostgreSQL and maintain encrypted, tested backups. SQLite is the local default.
3. Install requirements, run migrations and `collectstatic`. WhiteNoise serves only collected static assets. Persistent writable storage is required for `media/`; ephemeral hosts must mount a persistent volume or supply an appropriate storage backend. Keep uploaded documents outside the static root.
4. Serve public uploaded **images only** under `/media/profiles/` and `/media/projects/` through a properly configured web server or separate media origin, with `nosniff` and no script execution. Keep `/media/resumes/` and `/media/attachments/` inaccessible directly; the Django download views stream them as attachments. Uploaded files are limited to 5 MB and validated: images by Pillow, documents by allowed extension, PDF signature, and CSV UTF-8 content. Set a request-body limit at the proxy too. These checks are not malware scanning; only trusted staff may upload.
5. Terminate HTTPS at your trusted reverse proxy. Secure cookies, HTTPS redirects, HSTS (including subdomains and preload), nosniff, and frame denial are enabled when DEBUG is false. Use HSTS only with HTTPS on every relevant subdomain. For TLS termination, configure Django's `SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')` **only** if your proxy strips user-provided headers and always sets this header correctly; otherwise redirect loops can occur. This setting is intentionally not trusted by default.
6. Optionally change `ADMIN_URL` (include its trailing slash); this is not a security boundary. Restrict admin access through your host, VPN/IP rules, strong credentials, least privilege, and upstream login throttling. Configure monitoring and SMTP independently. No default admin account exists.
7. Run `check --deploy` with real production environment settings, then start the application behind HTTPS:

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py collectstatic --noinput
.\.venv\Scripts\python.exe manage.py check --deploy
.\.venv\Scripts\waitress-serve.exe --listen=127.0.0.1:8000 config.wsgi:application
```

Do not run local sample seeding automatically in production after replacing your content. Set the public domain correctly so canonical, Open Graph, robots, and sitemap URLs use it. Back up database and media together. Dependency ranges allow security patch upgrades; `requirements.lock.txt` records the versions verified in this workspace. Re-test upgrades and keep both runtime and build dependencies supported.

## Structure

`config/` settings and entrypoints; `core/` profile, skills, contact, validation, management command, and tests; `projects/` project models/views/admin/tests; `templates/` reusable Django pages; `static/` compiled styles, JavaScript, and images; `media/` ignored uploads and generated sample files; `scripts/` local setup and asset helpers. Initial migrations are committed as source files.
