/* Intentionally synchronous in <head>: choose colors before the first paint. */
(() => {
    'use strict';

    const storageKey = 'portfolio-theme';
    const root = document.documentElement;
    const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
    const isTheme = value => value === 'light' || value === 'dark';
    let preference = null;

    try {
        const saved = window.localStorage.getItem(storageKey);
        preference = isTheme(saved) ? saved : null;
    } catch {
        // Private browsing or storage restrictions must not disable the toggle.
    }

    const updateButtons = () => {
        const dark = root.dataset.theme === 'dark';
        document.querySelectorAll('[data-theme-toggle]').forEach(button => {
            button.hidden = false;
            button.setAttribute('aria-pressed', String(dark));
            button.setAttribute('aria-label', 'Dark mode');
            button.setAttribute('title', dark ? 'Switch to light mode' : 'Switch to dark mode');
        });
    };

    const applyTheme = () => {
        root.dataset.theme = preference || (systemTheme.matches ? 'dark' : 'light');
        updateButtons();
    };

    applyTheme();

    systemTheme.addEventListener('change', () => {
        if (!preference) applyTheme();
    });

    window.addEventListener('storage', event => {
        if (event.key === storageKey || event.key === null) {
            preference = isTheme(event.newValue) ? event.newValue : null;
            applyTheme();
        }
    });

    document.addEventListener('DOMContentLoaded', () => {
        updateButtons();
        document.querySelectorAll('[data-theme-toggle]').forEach(button => {
            button.addEventListener('click', () => {
                preference = root.dataset.theme === 'dark' ? 'light' : 'dark';
                try {
                    window.localStorage.setItem(storageKey, preference);
                } catch {
                    // Keep the selected mode for this page even if it cannot be saved.
                }
                applyTheme();
            });
        });
    });
})();
