/**
 * VLESS По Грибы • Smart Hub Frontend App
 */

let allServers = [];
let currentFilter = 'all';
let searchQuery = '';
let isScanning = false;
let pollTimer = null;

document.addEventListener('DOMContentLoaded', () => {
  initSubscriptionUrls();
  setupEventListeners();
  loadData();
});

// Automatically adapts subscription URLs to the actual host/port/IP in user's browser
function initSubscriptionUrls() {
  const origin = window.location.origin;
  const elements = [
    { id: 'sub-url-all', path: '/sub' },
    { id: 'sub-url-whitelist', path: '/sub/whitelist' },
    { id: 'sub-url-clash', path: '/clash' },
    { id: 'sub-url-singbox', path: '/singbox' }
  ];

  elements.forEach(item => {
    const el = document.getElementById(item.id);
    if (el) {
      el.value = `${origin}${item.path}`;
    }
  });
}

function setupEventListeners() {
  // Check button
  const btnCheck = document.getElementById('btn-run-check');
  btnCheck.addEventListener('click', triggerCheck);

  // Quick Action 1-Click Buttons
  const btnBestPing = document.getElementById('btn-best-ping');
  if (btnBestPing) {
    btnBestPing.addEventListener('click', async () => {
      try {
        const res = await fetch('/best');
        const key = await res.text();
        copyToClipboard(key);
        showToast('⚡ Лучший сервер (Мин. пинг) скопирован в буфер!');
      } catch (e) {
        showToast('Ошибка копирования ключа');
      }
    });
  }

  const btnBestWl = document.getElementById('btn-best-whitelist');
  if (btnBestWl) {
    btnBestWl.addEventListener('click', async () => {
      try {
        const res = await fetch('/best-whitelist');
        const key = await res.text();
        copyToClipboard(key);
        showToast('🛡️ Лучший обход (Whitelist) скопирован!');
      } catch (e) {
        showToast('Ошибка копирования ключа');
      }
    });
  }

  const btnBestGame = document.getElementById('btn-best-gaming');
  if (btnBestGame) {
    btnBestGame.addEventListener('click', async () => {
      try {
        const res = await fetch('/best-gaming');
        const key = await res.text();
        copyToClipboard(key);
        showToast('🎮 Игровой сервер скопирован в буфер!');
      } catch (e) {
        showToast('Ошибка копирования ключа');
      }
    });
  }

  const btnCopyTop3 = document.getElementById('btn-copy-top3');
  if (btnCopyTop3) {
    btnCopyTop3.addEventListener('click', () => {
      const origin = window.location.origin;
      copyToClipboard(`${origin}/sub/top3`);
      showToast('🌍 Подписка «Топ-3 по странам» скопирована!');
    });
  }

  // Search input
  const searchInput = document.getElementById('search-input');
  searchInput.addEventListener('input', (e) => {
    searchQuery = e.target.value.toLowerCase().trim();
    renderTable();
  });

  // Filter chips click delegation
  const chipsContainer = document.getElementById('filter-chips');
  chipsContainer.addEventListener('click', (e) => {
    const chip = e.target.closest('.chip');
    if (!chip) return;

    document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
    chip.classList.add('active');
    currentFilter = chip.dataset.filter;
    renderTable();
  });

function copyToClipboard(textToCopy) {
  if (!textToCopy) return;
  navigator.clipboard.writeText(textToCopy).then(() => {
    showToast('Скопировано в буфер обмена!');
  }).catch(() => {
    const ta = document.createElement('textarea');
    ta.value = textToCopy;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    showToast('Скопировано в буфер обмена!');
  });
}

  // Copy buttons
  document.addEventListener('click', (e) => {
    const copyBtn = e.target.closest('.btn-copy');
    if (copyBtn) {
      const targetId = copyBtn.dataset.target;
      let textToCopy = '';
      if (targetId) {
        const input = document.getElementById(targetId);
        if (input) textToCopy = input.value;
      } else if (copyBtn.dataset.clipboard) {
        textToCopy = copyBtn.dataset.clipboard;
      }
      copyToClipboard(textToCopy);
    }

    // QR buttons
    const qrBtn = e.target.closest('.btn-qr');
    if (qrBtn) {
      const targetInputId = qrBtn.dataset.url;
      const input = document.getElementById(targetInputId);
      if (input) {
        openQrModal(input.value);
      }
    }
  });

  // Modal close
  const modal = document.getElementById('qr-modal');
  const btnCloseModal = document.getElementById('btn-close-modal');
  const backdrop = modal.querySelector('.modal-backdrop');

  [btnCloseModal, backdrop].forEach(el => {
    el.addEventListener('click', () => modal.classList.add('hidden'));
  });
}

async function loadData() {
  try {
    const res = await fetch('/api/stats');
    if (!res.ok) throw new Error('API error');
    const data = await res.json();
    updateStats(data);
    allServers = data.servers || [];
    renderCountryChips(allServers);
    renderTable();

    if (data.is_checking) {
      startProgressPolling();
    }
  } catch (err) {
    console.error('Failed to load stats:', err);
  }
}

function updateStats(data) {
  document.getElementById('stat-total').textContent = (data.total_scanned || allServers.length).toLocaleString();
  document.getElementById('stat-alive').textContent = (data.alive_count || allServers.length).toLocaleString();
  document.getElementById('stat-whitelist').textContent = (data.whitelist_count || 0).toLocaleString();

  const alive = data.servers || allServers;
  if (alive.length > 0) {
    const validPings = alive.map(s => s.latency_ms).filter(p => p > 0);
    const avgPing = validPings.length > 0 ? Math.round(validPings.reduce((a, b) => a + b, 0) / validPings.length) : 0;
    document.getElementById('stat-avg-ping').textContent = `${avgPing} ms`;

    const countries = new Set(alive.map(s => s.country_code).filter(c => c && c !== 'OTHER'));
    document.getElementById('stat-countries').textContent = countries.size.toString();
  } else {
    document.getElementById('stat-avg-ping').textContent = '-- ms';
    document.getElementById('stat-countries').textContent = '0';
  }
}

function renderCountryChips(servers) {
  const container = document.getElementById('filter-chips');
  // Retain the standard chips: all, whitelist, fast
  const staticChips = container.querySelectorAll('[data-filter="all"], [data-filter="whitelist"], [data-filter="fast"]');
  container.innerHTML = '';
  staticChips.forEach(c => container.appendChild(c));

  // Count by country
  const counts = {};
  const flagMap = {};
  const nameMap = {};

  servers.forEach(s => {
    const cc = s.country_code;
    if (!cc || cc === 'OTHER') return;
    counts[cc] = (counts[cc] || 0) + 1;
    flagMap[cc] = s.country_flag || '🌐';
    nameMap[cc] = s.country_name || cc;
  });

  // Sort countries by count
  const sorted = Object.keys(counts).sort((a, b) => counts[b] - counts[a]);

  sorted.forEach(cc => {
    const btn = document.createElement('button');
    btn.className = 'chip';
    btn.dataset.filter = `country_${cc}`;
    btn.textContent = `${flagMap[cc]} ${nameMap[cc]} (${counts[cc]})`;
    if (currentFilter === `country_${cc}`) {
      btn.classList.add('active');
    }
    container.appendChild(btn);
  });
}

function renderTable() {
  const tbody = document.getElementById('servers-tbody');
  const countBadge = document.getElementById('filtered-count');

  let filtered = allServers.filter(s => {
    // 1. Filter chips
    if (currentFilter === 'whitelist' && !s.is_whitelist) return false;
    if (currentFilter === 'fast' && (s.latency_ms <= 0 || s.latency_ms > 100)) return false;
    if (currentFilter.startsWith('country_')) {
      const cc = currentFilter.replace('country_', '');
      if (s.country_code !== cc) return false;
    }

    // 2. Search query
    if (searchQuery) {
      const str = `${s.host} ${s.port} ${s.country_name} ${s.country_code} ${s.sni} ${s.remark} ${s.whitelist_label}`.toLowerCase();
      if (!str.includes(searchQuery)) return false;
    }

    return true;
  });

  countBadge.textContent = `${filtered.length} серверов`;

  if (filtered.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="6" class="empty-state">
          <span class="empty-icon">🔍</span>
          <p>По вашему фильтру ничего не найдено</p>
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = filtered.slice(0, 100).map((s, idx) => {
    const flag = s.country_flag || '🌐';
    const cName = s.country_name || s.country_code || 'Неизвестно';

    // Ping class
    let pingClass = 'ping-fast';
    if (s.latency_ms > 250) pingClass = 'ping-slow';
    else if (s.latency_ms > 120) pingClass = 'ping-medium';

    // Whitelist tag
    const wlHtml = s.is_whitelist 
      ? `<span class="badge-wl-target">${s.whitelist_label || '🛡️ Whitelist'}</span>` 
      : `<span style="color:var(--text-muted); font-size:12px;">Обычный</span>`;

    const secHtml = s.security 
      ? `<span class="badge-sec">${s.security.toUpperCase()}</span>` 
      : `<span class="badge-sec">TCP</span>`;

    return `
      <tr>
        <td>
          <div class="country-cell">
            <span class="country-flag">${flag}</span>
            <span>${cName}</span>
          </div>
        </td>
        <td>
          <span class="badge-ping ${pingClass}">${s.latency_ms > 0 ? s.latency_ms + ' ms' : 'OK'}</span>
        </td>
        <td>
          <div style="display:flex; flex-direction:column; gap:4px;">
            ${wlHtml}
            ${s.sni ? `<span style="font-family:var(--font-mono); font-size:11px; color:var(--text-secondary);">${escapeHtml(s.sni)}</span>` : ''}
          </div>
        </td>
        <td>
          <span style="font-family:var(--font-mono); font-size:12px; color:var(--text-primary);">${s.host}:${s.port}</span>
        </td>
        <td>
          ${secHtml}
          ${s.flow ? `<span class="badge-sec" style="color:var(--accent-cyan);">${s.flow}</span>` : ''}
        </td>
        <td>
          <button class="btn btn-copy" data-clipboard="${escapeHtml(s.uri)}" style="padding:6px 12px; font-size:12px;">
            Копировать ключ
          </button>
        </td>
      </tr>
    `;
  }).join('');
}

async function triggerCheck() {
  if (isScanning) return;
  const btn = document.getElementById('btn-run-check');
  const btnText = document.getElementById('btn-check-text');
  const icon = btn.querySelector('.spin-on-active');

  isScanning = true;
  btn.disabled = true;
  btnText.textContent = 'Сканирование...';
  icon.classList.add('spin');

  const card = document.getElementById('scan-progress-card');
  card.classList.remove('hidden');

  try {
    await fetch('/api/check', { method: 'POST' });
    startProgressPolling();
  } catch (err) {
    console.error('Trigger check error:', err);
    isScanning = false;
    btn.disabled = false;
    btnText.textContent = 'Проверить сервера';
    icon.classList.remove('spin');
  }
}

function startProgressPolling() {
  if (pollTimer) clearInterval(pollTimer);

  const card = document.getElementById('scan-progress-card');
  card.classList.remove('hidden');

  pollTimer = setInterval(async () => {
    try {
      const res = await fetch('/api/check/progress');
      const data = await res.json();

      document.getElementById('scan-percent').textContent = `${data.percent}%`;
      document.getElementById('progress-bar-fill').style.width = `${data.percent}%`;
      document.getElementById('scan-detail-counts').textContent = `${data.completed} / ${data.total} проверено`;
      document.getElementById('scan-alive-count').textContent = `Живых: ${data.alive_count}`;

      if (!data.is_running) {
        clearInterval(pollTimer);
        pollTimer = null;
        isScanning = false;

        const btn = document.getElementById('btn-run-check');
        const btnText = document.getElementById('btn-check-text');
        const icon = btn.querySelector('.spin-on-active');
        btn.disabled = false;
        btnText.textContent = 'Проверить сервера';
        icon.classList.remove('spin');

        setTimeout(() => {
          card.classList.add('hidden');
        }, 2000);

        showToast('Проверка серверов успешно завершена!');
        loadData();
      }
    } catch (e) {
      console.error('Polling error:', e);
    }
  }, 600);
}

function openQrModal(url) {
  const modal = document.getElementById('qr-modal');
  const qrImg = document.getElementById('qr-image');
  const qrInput = document.getElementById('qr-url-text');

  qrInput.value = url;
  // Use public QR generator API with high error correction
  qrImg.src = `https://api.qrserver.com/v1/create-qr-code/?size=300x300&ecc=M&data=${encodeURIComponent(url)}`;
  modal.classList.remove('hidden');
}

function showToast(message) {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.classList.remove('hidden');
  toast.style.transform = 'translateY(0)';
  toast.style.opacity = '1';

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => toast.classList.add('hidden'), 300);
  }, 2500);
}

function escapeHtml(text) {
  if (!text) return '';
  return text.replace(/[&<>"']/g, function(m) {
    return {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#039;'
    }[m];
  });
}
