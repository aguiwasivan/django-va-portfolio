const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const postcss = require('postcss');

const source = fs.readFileSync('static/js/theme.js', 'utf8');

function browser({ saved = null, dark = false, blocked = false } = {}) {
    const documentEvents = {};
    const windowEvents = {};
    const buttonEvents = {};
    const attributes = {};
    let stored = saved;
    const root = { dataset: {} };
    const button = {
        hidden: true,
        setAttribute(key, value) { attributes[key] = value; },
        addEventListener(key, callback) { buttonEvents[key] = callback; },
    };
    const media = {
        matches: dark,
        addEventListener(key, callback) { this.change = callback; },
    };
    const document = {
        documentElement: root,
        querySelectorAll() { return [button]; },
        addEventListener(key, callback) { documentEvents[key] = callback; },
    };
    const window = {
        matchMedia() { return media; },
        localStorage: {
            getItem() {
                if (blocked) throw new Error('Storage unavailable');
                return stored;
            },
            setItem(key, value) {
                if (blocked) throw new Error('Storage unavailable');
                assert.equal(key, 'portfolio-theme');
                stored = value;
            },
        },
        addEventListener(key, callback) { windowEvents[key] = callback; },
    };
    vm.runInNewContext(source, { document, window });
    return {
        root, button, attributes,
        ready() { documentEvents.DOMContentLoaded(); },
        click() { buttonEvents.click(); },
        system(value) { media.matches = value; media.change(); },
        storage(value) { windowEvents.storage({ key: 'portfolio-theme', newValue: value }); },
        saved() { return stored; },
    };
}

test('applies system light or dark before DOMContentLoaded', () => {
    assert.equal(browser().root.dataset.theme, 'light');
    assert.equal(browser({ dark: true }).root.dataset.theme, 'dark');
});

test('saved preference wins over system, including across page reloads', () => {
    const page = browser({ dark: true });
    page.ready();
    page.click();
    assert.equal(page.root.dataset.theme, 'light');
    assert.equal(page.saved(), 'light');
    const nextPage = browser({ saved: page.saved(), dark: true });
    assert.equal(nextPage.root.dataset.theme, 'light');
    assert.equal(browser({ saved: 'dark' }).root.dataset.theme, 'dark');
});

test('switches repeatedly without reload and keeps accessible state in sync', () => {
    const page = browser();
    page.ready();
    assert.equal(page.button.hidden, false);
    assert.equal(page.attributes['aria-pressed'], 'false');
    page.click();
    assert.equal(page.root.dataset.theme, 'dark');
    assert.equal(page.attributes['aria-pressed'], 'true');
    assert.equal(page.attributes.title, 'Switch to light mode');
    page.click();
    assert.equal(page.attributes['aria-pressed'], 'false');
    assert.equal(page.attributes['aria-label'], 'Dark mode');
});

test('system changes apply only without an explicit preference', () => {
    const page = browser();
    page.system(true);
    assert.equal(page.root.dataset.theme, 'dark');
    page.ready();
    page.click();
    page.system(true);
    assert.equal(page.root.dataset.theme, 'light');
});

test('invalid storage values fall back to the system', () => {
    assert.equal(browser({ saved: 'invalid', dark: true }).root.dataset.theme, 'dark');
});

test('blocked storage does not prevent theme switching', () => {
    const page = browser({ blocked: true, dark: true });
    page.ready();
    page.click();
    assert.equal(page.root.dataset.theme, 'light');
    page.click();
    assert.equal(page.root.dataset.theme, 'dark');
});

test('storage changes synchronize tabs and clearing restores system detection', () => {
    const page = browser();
    page.storage('dark');
    assert.equal(page.root.dataset.theme, 'dark');
    page.storage(null);
    assert.equal(page.root.dataset.theme, 'light');
});

const theme = postcss.parse(fs.readFileSync('static/css/theme.css', 'utf8'));
const palettes = {};
theme.walkRules(rule => {
    if (rule.selector === ':root' || rule.selector === '[data-theme="dark"]') {
        palettes[rule.selector] = Object.fromEntries(rule.nodes.map(node => [node.prop, node.value]));
    }
});

function luminance(color) {
    const channels = color.slice(1).match(/../g).map(hex => parseInt(hex, 16) / 255);
    const linear = channels.map(value => value <= .04045 ? value / 12.92 : ((value + .055) / 1.055) ** 2.4);
    return linear[0] * .2126 + linear[1] * .7152 + linear[2] * .0722;
}

test('primary text, secondary text, links, inputs, and buttons meet AA contrast', () => {
    const pairs = [
        ['text-primary', 'page-bg'], ['text-secondary', 'page-bg'],
        ['text-primary', 'card-bg'], ['text-secondary', 'card-bg'],
        ['accent', 'card-bg'], ['button-text', 'button-bg'],
        ['inverse-text', 'inverse-bg'], ['text-primary', 'input-bg'],
        ['available-text', 'available-bg'], ['error-text', 'error-bg'],
    ];
    for (const [name, palette] of Object.entries(palettes)) {
        for (const [text, background] of pairs) {
            const a = luminance(palette[`--${text}`]);
            const b = luminance(palette[`--${background}`]);
            const ratio = (Math.max(a, b) + .05) / (Math.min(a, b) + .05);
            assert.ok(ratio >= 4.5, `${name}: ${text}/${background}: ${ratio}`);
        }
    }
});

test('all site color variables are defined and reduced motion has no transitions', () => {
    const names = new Set(Object.keys(palettes[':root']));
    for (const file of ['static/css/site.css', 'static/css/skills.css', 'static/css/theme.css']) {
        const css = fs.readFileSync(file, 'utf8');
        for (const match of css.matchAll(/var\((--[\w-]+)\)/g)) {
            assert.ok(names.has(match[1]), `Undefined ${match[1]} in ${file}`);
        }
        postcss.parse(css).walkAtRules('media', rule => {
            if (rule.params.includes('prefers-reduced-motion')) {
                rule.walkDecls('transition', decl => assert.equal(decl.value, 'none'));
            }
        });
    }
});

test('Lucide supplies both theme icons and CSS selects the correct icon', () => {
    const lucide = require('../static/js/lucide.min.js');
    assert.ok(lucide.icons.Sun);
    assert.ok(lucide.icons.Moon);
    const css = fs.readFileSync('static/css/theme.css', 'utf8');
    assert.ok(css.includes('[data-theme="dark"] .theme-toggle .theme-moon'));
    assert.ok(css.includes('[data-theme="dark"] .theme-toggle .theme-sun'));
});
