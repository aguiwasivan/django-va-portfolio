document.addEventListener('DOMContentLoaded', () => {
  document.documentElement.classList.add('js');
  if (window.lucide) lucide.createIcons();
  const toggle = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('#navigation');
  const closeMenu = () => { navigation.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); };
  toggle?.addEventListener('click', () => {
    const open = navigation.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
  });
  document.addEventListener('keydown', event => { if (event.key === 'Escape' && navigation.classList.contains('open')) { closeMenu(); toggle.focus(); } });
  navigation?.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.remove('pending'); observer.unobserve(entry.target); }
    }), {threshold: 0.08});
    document.querySelectorAll('.reveal').forEach(element => { element.classList.add('pending'); observer.observe(element); });
  }
  const search = document.querySelector('#record-search');
  search?.addEventListener('input', () => {
    const rows = [...document.querySelectorAll('#employee-table tbody tr')];
    rows.forEach(row => { row.hidden = !row.textContent.toLowerCase().includes(search.value.toLowerCase()); });
    document.querySelector('#record-count').textContent = `${rows.filter(row => !row.hidden).length} of ${rows.length} fictional records`;
  });
  const buttons = [...document.querySelectorAll('[data-email]')];
  const selectEmail = button => {
    buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    document.querySelectorAll('.email-panel').forEach(panel => { panel.hidden = panel.id !== button.dataset.email; });
  };
  buttons.forEach(button => button.addEventListener('click', () => selectEmail(button)));
  if (buttons.length) selectEmail(buttons[0]);
});
