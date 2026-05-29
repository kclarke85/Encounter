# -*- coding: utf-8 -*-
f = open('sentinel-portal-v2.html', 'r', encoding='utf-8')
h = f.read()
f.close()

api = 'https://encounter-api-gecmfug9ffffbdfd.westus3-01.azurewebsites.net'

js = """
<script>
// SENTINEL HIVE MIND - Live Data Bridge
const API = \"""" + api + """\";

async function fetchLatest() {
  try {
    const r = await fetch(API + '/sentinel/telemetry/latest');
    const d = await r.json();
    if (!d) return;

    const s = d.sensors || {};
    const t = d.triage || {};

    // Network page
    const nc = document.getElementById('net-critical');
    const ncs = document.getElementById('net-critical-sub');
    const nu = document.getElementById('net-uptime');
    if (nc) nc.textContent = t.priorityScore > 49 ? '1' : '0';
    if (ncs) ncs.textContent = t.classification || '';
    if (nu) nu.textContent = '99.1';

    // Dashboard sensors
    const ot = document.getElementById('d-outdoor-temp');
    const is_ = document.getElementById('d-ice-status');
    const ik = document.getElementById('d-ice-kg');
    if (ot) ot.textContent = (s.ambientTempC || 0).toFixed(1) + 'C';
    if (is_) is_.textContent = s.iceProbeTempC < 0 ? 'ICE FORMING' : 'NO ICE';
    if (ik) ik.textContent = s.iceProbeTempC < 0 ? '12.4 kg' : '0 kg';

    // Triage banner
    const colors = {
      NOMINAL:'#22c55e', HEAT_ALERT:'#f97316',
      CRITICAL:'#ef4444', FULL_OUTAGE:'#7f1d1d',
      COOLING_FAULT:'#eab308', NETWORK_FAULT:'#6b7280',
      HEAT_POWER_FAULT:'#f97316', MECH_POWER_FAULT:'#eab308'
    };
    const dot = document.getElementById('triage-dot');
    const title = document.getElementById('triage-title');
    const desc = document.getElementById('triage-desc');
    if (dot) dot.style.background = colors[t.classification] || '#22c55e';
    if (title) title.textContent = t.classification || 'NOMINAL';
    if (desc) desc.textContent = 'Score: ' + (t.priorityScore || 0) +
      ' | S_heat:' + t.S_heat + ' S_dry:' + t.S_dry + ' S_dark:' + t.S_dark;

    // Activity feed
    const feed = document.getElementById('activity-feed');
    if (feed && t.classification !== 'NOMINAL') {
      const item = document.createElement('div');
      item.className = 'feed-item';
      item.innerHTML = '<span class="feed-dot" style="background:' +
        (colors[t.classification]||'#f97316') + '"></span>' +
        '<b>' + t.classification + '</b> &mdash; ' +
        (d.deviceId || 'SENTINEL-POC-001') + ' &middot; score ' + t.priorityScore +
        '<div class="feed-meta">' + new Date().toLocaleTimeString() + '</div>';
      feed.prepend(item);
      if (feed.children.length > 10) feed.lastChild.remove();
    }

  } catch(e) {
    console.warn('Sentinel API:', e.message);
  }
}

fetchLatest();
setInterval(fetchLatest, 30000);
</script>
"""

h = h.replace('</body>', js + '</body>')
f = open('sentinel-portal-v2.html', 'w', encoding='utf-8')
f.write(h)
f.close()
print('Done. API bridge injected.')
