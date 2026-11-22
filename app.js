const filters = document.querySelector('.category-filters');

if (filters) {
  const buttons = [...filters.querySelectorAll('[data-filter]')];
  const rows = [...document.querySelectorAll('.post-row')];
  const empty = document.getElementById('empty-posts');

  filters.hidden = false;
  buttons.forEach(button => {
    button.addEventListener('click', () => {
      const category = button.dataset.filter;
      buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
      let visible = 0;
      rows.forEach(row => {
        row.hidden = category !== 'All' && row.dataset.category !== category;
        if (!row.hidden) visible += 1;
      });
      empty.hidden = visible !== 0;
    });
  });
}
