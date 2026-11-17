let map, routeLayer, markersLayer;
const $ = (id) => document.getElementById(id);

function initMap() {
  map = L.map('map').setView([28.6139, 77.2090], 10);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
    maxZoom: 19
  }).addTo(map);
  markersLayer = L.layerGroup().addTo(map);
}
function tableHTML(rows, columns) {
  if (!rows || !rows.length) return '<p class="hint">This method was not selected.</p>';
  return `<table class="method-table"><thead><tr>${columns.map(c=>`<th>${c[0]}</th>`).join('')}</tr></thead><tbody>${
    rows.map(r=>`<tr>${columns.map(c=>`<td>${r[c[1]] ?? '—'}</td>`).join('')}</tr>`).join('')
  }</tbody></table>`;
}
function renderMethod(target, data, type) {
  if (!data) { $(target).innerHTML = '<p class="hint">Not run in this selection.</p>'; return; }
  const cols = type === 'newton'
    ? [['Iter','iteration'],['xₙ','x'],['f(xₙ)','f_x'],['f′(xₙ)','derivative'],['Next x','next_x'],['Error','error']]
    : [['Iter','iteration'],['a','a'],['b','b'],['Midpoint','midpoint'],['f(mid)','f_midpoint'],['Width','interval_width']];
  $(target).innerHTML = `<p class="hint">Root: <b>${data.root.toFixed(7)}</b> · ${data.iterations.length} iteration(s) · ${data.converged ? 'Converged' : 'Maximum iterations reached'}</p>` + tableHTML(data.iterations, cols);
}
function renderResult(data) {
  $('results').classList.remove('hidden');
  $('distance').textContent = data.distance_km.toFixed(1);
  $('time').textContent = data.estimated_minutes;
  $('congestion').textContent = data.congestion_index.toFixed(1) + '/10';
  $('weight').textContent = data.optimal_weight.toFixed(4);
  $('mapTitle').textContent = `${data.source} → ${data.destination}`;
  $('path').innerHTML = data.route.map((p,i)=>`${i ? '<b>→</b>' : ''}<span>${p}</span>`).join('');
  $('modelNote').textContent = data.model_note;
  $('candidates').innerHTML = data.candidates.map(c=>`<div class="candidate"><strong>${c.label}</strong><p>${c.path.join(' → ')}</p><small>${c.distance_km} km · ${c.minutes} min · congestion ${c.congestion}</small></div>`).join('');
  $('rootSummary').innerHTML = `Newton-Raphson: ${data.methods.newton ? data.methods.newton.root.toFixed(7) : 'not run'}<br>Bisection: ${data.methods.bisection ? data.methods.bisection.root.toFixed(7) : 'not run'}<br><br>Both methods solve the same equation, so their roots should be close within the chosen tolerance.`;
  renderMethod('newtonDetails', data.methods.newton, 'newton');
  renderMethod('bisectionDetails', data.methods.bisection, 'bisection');

  markersLayer.clearLayers();
  if (routeLayer) map.removeLayer(routeLayer);
  const coords = data.coordinates.map(p=>[p.lat,p.lng]);
  routeLayer = L.polyline(coords,{color:'#168d78',weight:6,opacity:.9}).addTo(map);
  data.coordinates.forEach((p,i)=>{
    L.circleMarker([p.lat,p.lng],{radius:7,color:'#0b443c',fillColor:i===0?'#7be0bd':(i===data.coordinates.length-1?'#ffb978':'#fff'),fillOpacity:1,weight:2})
      .bindTooltip(`${i+1}. ${p.name}`).addTo(markersLayer);
  });
  map.fitBounds(routeLayer.getBounds(),{padding:[35,35]});
  $('results').scrollIntoView({behavior:'smooth',block:'start'});
}
async function optimize() {
  const button = $('optimizeBtn');
  $('error').textContent = '';
  if ($('source').value === $('destination').value) {
    $('error').textContent = 'Choose two different locations.';
    return;
  }
  button.disabled = true; button.textContent = 'Calculating…';
  try {
    const response = await fetch('/api/optimize',{
      method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({source:$('source').value,destination:$('destination').value,method:$('method').value})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Could not calculate route.');
    renderResult(data);
  } catch (error) {
    $('error').textContent = error.message;
  } finally {
    button.disabled = false; button.innerHTML = 'Optimize route <span>→</span>';
  }
}
document.addEventListener('DOMContentLoaded',()=>{
  initMap();
  $('optimizeBtn').addEventListener('click',optimize);
});
