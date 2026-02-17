// SPA router - hash-based page loading
const content = document.getElementById('content');
const nav = document.getElementById('nav');
const cache = {};

async function loadPage(page) {
  if (!page || page === '') page = 'home';
  nav.querySelectorAll('a').forEach(a => {
    a.classList.toggle('active', a.dataset.page === page);
  });
  document.title = page.charAt(0).toUpperCase()
    + page.slice(1) + ' - LookingGlass';
  if (cache[page]) {
    content.innerHTML = cache[page];
    afterLoad();
    return;
  }
  try {
    const resp = await fetch('pages/' + page + '.html');
    if (!resp.ok) throw new Error(resp.status);
    const html = await resp.text();
    cache[page] = html;
    content.innerHTML = html;
  } catch (e) {
    content.innerHTML = '<main><h1>Not Found</h1>'
      + '<p>Page "' + page + '" not found.</p></main>';
  }
  afterLoad();
}

function afterLoad() {
  document.querySelectorAll('.card').forEach(c => {
    c.style.cursor = 'pointer';
    c.onmouseenter = () => c.style.borderColor = '#00cccc';
    c.onmouseleave = () => c.style.borderColor = '#2a2a3a';
  });
}

function onHash() {
  loadPage(location.hash.slice(1));
}

window.addEventListener('hashchange', onHash);
window.addEventListener('DOMContentLoaded', () => {
  if (!location.hash) location.hash = '#home';
  else onHash();
});
