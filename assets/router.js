// Cube Router - (x,y,z) page addressing
const content = document.getElementById('content');
const nav = document.getElementById('nav');
const coordEl = document.getElementById('coord');
const cache = {};

const CUBE_MAP = {
  '0,0,0':'Home','1,0,0':'Architecture','2,0,0':'Standards',
  '0,1,0':'Frumkin','1,1,0':'Analysis','2,1,0':'2026 Predictions',
  '0,0,1':'API'
};

async function loadCube(xyz) {
  if (!xyz || !CUBE_MAP[xyz]) xyz = '0,0,0';
  coordEl.textContent = '[' + xyz + ']';
  nav.querySelectorAll('a').forEach(a => {
    a.classList.toggle('active', a.dataset.xyz === xyz);
  });
  document.title = CUBE_MAP[xyz] + ' [' + xyz + '] - LookingGlass';
  const file = xyz.replace(/,/g, '-');
  if (cache[file]) { content.innerHTML = cache[file]; return; }
  try {
    const r = await fetch('pages/' + file + '.html');
    if (!r.ok) throw new Error(r.status);
    const html = await r.text();
    cache[file] = html;
    content.innerHTML = html;
  } catch (e) {
    content.innerHTML = '<main><h1>Void</h1>'
      + '<p>No cube at [' + xyz + ']</p></main>';
  }
}

function onHash() { loadCube(location.hash.slice(1)); }
window.addEventListener('hashchange', onHash);
window.addEventListener('DOMContentLoaded', () => {
  if (!location.hash) location.hash = '#0,0,0';
  else onHash();
});
