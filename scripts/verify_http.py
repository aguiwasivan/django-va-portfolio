"""Exercise local HTTP routes and assets against an already running server."""
from urllib.request import urlopen

paths = ['/', '/about/', '/skills/', '/projects/', '/contact/', '/projects/employee-data-entry/', '/projects/executive-calendar/', '/projects/professional-email/', '/projects/meeting-agenda/', '/robots.txt', '/sitemap.xml', '/static/css/tailwind.css', '/static/css/site.css', '/static/js/lucide.min.js', '/static/images/profile-placeholder.svg', '/static/images/social-card.png']
for path in paths:
    with urlopen('http://127.0.0.1:8000' + path, timeout=10) as response:
        assert response.status == 200, path
        assert response.read(), path
        print(f'200 {path}')
