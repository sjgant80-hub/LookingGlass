// Cube Router - slug-based with (x,y,z) metadata
const content = document.getElementById('content');
const nav = document.getElementById('nav');
const coordEl = document.getElementById('coord');
const cache = {};
let cube3d = null;

// slug → {name, xyz, file}
const PAGES = {
  home:{n:'Home',xyz:'0,0,0'},arch:{n:'Architecture',xyz:'1,0,0'},
  std:{n:'Standards',xyz:'2,0,0'},frumkin:{n:'Frumkin',xyz:'0,1,0'},
  analysis:{n:'Analysis',xyz:'1,1,0'},pred2026:{n:'2026',xyz:'2,1,0'},
  cmdty:{n:'Commodities',xyz:'0,2,0'},apac:{n:'Asia-Pacific',xyz:'1,2,0'},
  emerging:{n:'Emerging',xyz:'2,2,0'},api:{n:'API',xyz:'0,0,1'},
  g20:{n:'G20',xyz:'1,0,1'},brics:{n:'BRICS+',xyz:'2,0,1'},
  global:{n:'Global Map',xyz:'0,1,1'},americas:{n:'Americas',xyz:'1,1,1'},
  europe:{n:'Europe',xyz:'2,1,1'},latam:{n:'LatAm+Carib',xyz:'0,2,1'},
  seasia:{n:'SE Asia',xyz:'1,2,1'},afrmena:{n:'Africa+MENA',xyz:'2,2,1'},
  risk:{n:'Contagion',xyz:'0,0,2'},cascade:{n:'Cascades',xyz:'1,0,2'},
  anchors:{n:'Stabilizers',xyz:'2,0,2'},near:{n:'2027-2031',xyz:'0,1,2'},
  far:{n:'2032-2036',xyz:'1,1,2'},deciders:{n:'Deciders',xyz:'2,1,2'},
  entropy:{n:'Entropy',xyz:'0,2,2'},forks:{n:'Forks',xyz:'1,2,2'},
  endgame:{n:'2036 Endgame',xyz:'2,2,2'},
  iran:{n:'Iran Crisis',xyz:'0,0,3'},hormuz:{n:'Hormuz Cascade',xyz:'1,0,3'}
};

// expose for 3D module
window.__LG_PAGES = PAGES;

async function loadPage(slug) {
  if (!slug || !PAGES[slug]) slug = 'home';
  const p = PAGES[slug];
  coordEl.textContent = '[' + p.xyz + ']';
  nav.querySelectorAll('a').forEach(a => {
    a.classList.toggle('active', a.dataset.slug === slug);
  });
  document.title = p.n + ' [' + p.xyz + '] - LookingGlass';
  if (cube3d) cube3d.setActive(slug);
  const file = p.xyz.replace(/,/g, '-');
  if (cache[slug]) { content.innerHTML = cache[slug]; return; }
  try {
    const r = await fetch('pages/' + file + '.html');
    if (!r.ok) throw new Error(r.status);
    const html = await r.text();
    cache[slug] = html;
    content.innerHTML = html;
  } catch (e) {
    content.innerHTML = '<main><h1>Void</h1>'
      + '<p>No cube at [' + p.xyz + ']</p></main>';
  }
}

function onHash() { loadPage(location.hash.slice(1)); }
window.addEventListener('hashchange', onHash);
window.addEventListener('DOMContentLoaded', () => {
  if (!location.hash) location.hash = '#home';
  else onHash();
});

// ── 3D cube toggle ──────────────────────────────────
const toggleBtn = document.getElementById('cube-toggle');
const overlay = document.getElementById('cube-overlay');
const cubeCanvas = document.getElementById('cube-canvas');
let cubeOpen = false;

if (toggleBtn && overlay && cubeCanvas) {
  toggleBtn.addEventListener('click', async () => {
    cubeOpen = !cubeOpen;
    overlay.classList.toggle('open', cubeOpen);
    toggleBtn.textContent = cubeOpen ? '[x] Close' : '[3D] Cube';
    if (cubeOpen && !cube3d) {
      const mod = await import('./cube3d.js');
      cube3d = mod;
      cube3d.init(cubeCanvas);
      cube3d.setActive(location.hash.slice(1) || 'home');
    }
    if (cubeOpen && cube3d) {
      const r = overlay.getBoundingClientRect();
      cube3d.resize(r.width, r.height);
    }
  });

  window.addEventListener('resize', () => {
    if (cubeOpen && cube3d) {
      const r = overlay.getBoundingClientRect();
      cube3d.resize(r.width, r.height);
    }
  });
}
