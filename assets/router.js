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
  iran:{n:'Iran Crisis',xyz:'0,0,3'},hormuz:{n:'Hormuz Cascade',xyz:'1,0,3'},
  ukraine:{n:'Ukraine War',xyz:'2,0,3'},taiwan:{n:'Taiwan Strait',xyz:'0,1,3'},
  trade:{n:'Trade War',xyz:'1,1,3'},sahel:{n:'Sahel Crisis',xyz:'2,1,3'},
  debt:{n:'Debt + Dollar',xyz:'0,2,3'},chips:{n:'Chips + AI',xyz:'1,2,3'},
  climate:{n:'Energy + Climate',xyz:'2,2,3'},
  china:{n:'China Deep Dive',xyz:'0,0,4'},japan:{n:'Japan + BOJ',xyz:'1,0,4'},
  uspol:{n:'US Domestic',xyz:'2,0,4'},demog:{n:'Demographics',xyz:'0,1,4'},
  cbanks:{n:'Central Banks',xyz:'1,1,4'},eupol:{n:'EU Politics',xyz:'2,1,4'},
  failed:{n:'Failed States',xyz:'0,2,4'},food:{n:'Food + Water',xyz:'1,2,4'},
  digital:{n:'Digital Finance',xyz:'2,2,4'},
  india:{n:'India Deep Dive',xyz:'0,0,5'},korea:{n:'South Korea',xyz:'1,0,5'},
  russia:{n:'Russia Deep Dive',xyz:'2,0,5'},minerals:{n:'Critical Minerals',xyz:'0,1,5'},
  migration:{n:'Migration',xyz:'1,1,5'},security:{n:'Security Architecture',xyz:'2,1,5'},
  saudi:{n:'Saudi + OPEC+',xyz:'0,2,5'},brazil:{n:'Brazil Deep Dive',xyz:'1,2,5'},
  backtest:{n:'Frumkin Backtesting',xyz:'2,2,5'},
  italy:{n:'Italy Deep Dive',xyz:'0,0,6'},
  h2025:{n:'κ 2025',xyz:'0,0,7'},h2024:{n:'κ 2024',xyz:'1,0,7'},
  h2023:{n:'κ 2023',xyz:'2,0,7'},h2022:{n:'κ 2022',xyz:'0,1,7'},
  h2021:{n:'κ 2021',xyz:'1,1,7'},h2020:{n:'κ 2020',xyz:'2,1,7'},
  h2019:{n:'κ 2019',xyz:'0,2,7'},h2018:{n:'κ 2018',xyz:'1,2,7'},
  h2016:{n:'κ 2016-17',xyz:'2,2,7'},
  h2008:{n:'κ 2008 GFC',xyz:'3,0,7'},h2001:{n:'κ 2001 9/11',xyz:'3,1,7'},
  h1989:{n:'κ 1989 Wall',xyz:'3,2,7'},h1979:{n:'κ 1979 Volcker',xyz:'0,3,7'},
  h1971:{n:'κ 1971 Nixon',xyz:'1,3,7'},h1969:{n:'κ 1969 Peak',xyz:'2,3,7'},
  hmap:{n:'Entropy 1969→2025',xyz:'3,3,7'}
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
