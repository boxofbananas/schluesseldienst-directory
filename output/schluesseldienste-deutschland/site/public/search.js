// Die Suche im Verzeichnis. Kein Server: der Index ist eine JSON-Datei, die mit der Website gebaut
// wird. Ein Feld für Firmenname oder Leistung, ein Feld für die Stadt. Jedes Feld schlägt während der
// Eingabe vor: zuerst die Leistungen (eine Wahl wird zu einem Schildchen im Feld), dann die Betriebe
// (eine Wahl öffnet den Eintrag), rechts die Städte. Gesucht wird erst beim Klick auf Suchen; die
// Treffer stehen auf /suche/.
// Umlaute: norm() schreibt ä/ö/ü/ß um, damit "Nurnberg" und "Nürnberg" dieselben Treffer finden.
(function () {
  var form = document.getElementById('dir-search');
  if (!form) return;
  var what = form.querySelector('[name=s]'), near = form.querySelector('[name=near]');
  var listWhat = document.getElementById('sugg-what'), listNear = document.getElementById('sugg-near');
  var pickedList = document.getElementById('filter-picked');
  var results = document.getElementById('search-results');
  var onSearchPage = !!(results && results.dataset.page === 'search');
  var boxes = Array.prototype.slice.call(form.querySelectorAll('[name=f]'));
  var index = null, loading = null;

  function load() {
    if (index) return Promise.resolve(index);
    if (!loading) loading = fetch(form.dataset.index).then(function (r) { return r.json(); }).then(function (j) { index = j; return j; });
    return loading;
  }
  function norm(s) {
    return (s || '').toLowerCase()
      .replace(/ä/g, 'ae').replace(/ö/g, 'oe').replace(/ü/g, 'ue').replace(/ß/g, 'ss')
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  }
  function words(s) { return norm(s).split(/[^a-z0-9]+/).filter(Boolean); }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function stars(r) { var f = Math.round(r); return '\u2605'.repeat(f) + '\u2606'.repeat(5 - f); }
  function score(l) { return l.r * Math.log10(l.v + 1); }
  function hide(list) { list.hidden = true; list.innerHTML = ''; }
  function hideAll() { hide(listWhat); hide(listNear); }

  // Leistungsfilter: die unsichtbaren Kästchen halten den Zustand, die Schildchen zeigen ihn.
  function picked() { return boxes.filter(function (i) { return i.checked; }).map(function (i) { return i.value; }); }
  function setFilter(label, on) { boxes.forEach(function (i) { if (i.value === label) i.checked = on; }); renderPicked(); }
  function renderPicked() {
    pickedList.innerHTML = picked().map(function (f) {
      return '<li>' + esc(f) + '<button type="button" data-remove="' + esc(f) + '" aria-label="' + esc(f) + ' entfernen">\u00d7</button></li>';
    }).join('');
  }
  function serviceMatches(q) {
    var n = norm(q), have = picked();
    return boxes.map(function (i) { return i.value; }).filter(function (v) {
      if (have.indexOf(v) !== -1) return false;
      return words(v).some(function (w) { return w.indexOf(n) === 0; }) || norm(v).indexOf(n) === 0;
    });
  }
  function matchFilters(l, fs) { return fs.every(function (f) { return l.a.indexOf(f) !== -1; }); }

  // Jedes eingegebene Wort muss ein Wort im Namen oder in einer bestätigten Leistung beginnen, damit
  // "tue" einen Betrieb mit "Türöffnung" findet und nicht jeden Betrieb, dessen Leistungen "Schlüssel" nennen.
  function matchWhat(l, q) {
    if (!q) return true;
    var hay = ' ' + norm(l.n).replace(/[^a-z0-9]+/g, ' ') + ' ' + norm(l.a.join(' ')).replace(/[^a-z0-9]+/g, ' ') + ' ';
    return words(q).every(function (w) { return hay.indexOf(' ' + w) !== -1; });
  }
  function matchNear(l, q) {
    if (!q) return true;
    var n = norm(q);
    return norm(l.c).indexOf(n) === 0 || norm(l.t).indexOf(n) === 0;
  }
  function cityMatches(q) {
    var n = norm(q);
    return index.cities.filter(function (c) { return norm(c.n).indexOf(n) === 0; }).slice(0, 8);
  }
  function nf(n) { return Number(n || 0).toLocaleString('de-DE'); }
  function rf(n) { return Number(n || 0).toFixed(1).replace('.', ','); }
  function ratingHtml(l) { return l.v ? '<span class="rt"><i aria-hidden="true">\u2605</i> ' + rf(l.r) + ' <small>(' + nf(l.v) + ')</small></span>' : ''; }

  function showWhat() {
    var q = what.value.trim();
    if (q.length < 2) return hide(listWhat);
    load().then(function () {
      var fs = picked(), html = '';
      var services = serviceMatches(q);
      if (services.length) {
        html += '<li class="group">Leistungen</li>' + services.map(function (v) {
          return '<li><button type="button" data-pick="' + esc(v) + '"><b>' + esc(v) + '</b><span>Filter setzen</span></button></li>';
        }).join('');
      }
      var hits = index.listings.filter(function (l) { return matchWhat(l, q) && matchNear(l, near.value.trim()) && matchFilters(l, fs); })
        .sort(function (a, b) { return score(b) - score(a); }).slice(0, 6);
      if (hits.length) {
        html += (services.length ? '<li class="group">Betriebe</li>' : '') + hits.map(function (l) {
          return '<li><a href="' + l.p + '"><b>' + esc(l.n) + '</b><span>' + esc(l.c) + ratingHtml(l) + '</span></a></li>';
        }).join('');
      }
      if (!html) return hide(listWhat);
      listWhat.innerHTML = html; listWhat.hidden = false;
    });
  }
  function showNear() {
    var q = near.value.trim();
    load().then(function () {
      var hits = q ? cityMatches(q) : index.cities.slice(0, 8);
      var html = '';
      if ('geolocation' in navigator) html += '<li><button type="button" class="use-location">In meiner Nähe: Standort verwenden</button></li>';
      html += hits.map(function (c) { return '<li><button type="button" data-city="' + esc(c.n) + '"><b>' + esc(c.n) + '</b><span>' + nf(c.c) + ' eingetragen</span></button></li>'; }).join('');
      listNear.innerHTML = html; listNear.hidden = false;
    });
  }
  function nearestCity(lat, lng) {
    var best = null, bd = Infinity;
    index.cities.forEach(function (c) {
      var d = Math.hypot(c.lat - lat, (c.lng - lng) * Math.cos(lat * Math.PI / 180));
      if (d < bd) { bd = d; best = c; }
    });
    return best;
  }

  // Treffer (nur auf der Suchseite). Die gesuchte Leistung steht auf jeder Karte zuerst.
  function chipsFor(l, q, fs) {
    var ws = words(q);
    var hit = l.a.filter(function (a) { return fs.indexOf(a) !== -1 || ws.some(function (w) { return norm(a).indexOf(w) !== -1; }); });
    var rest = l.a.filter(function (a) { return hit.indexOf(a) === -1; });
    return hit.concat(rest).slice(0, 3);
  }
  function render(hits, q, city, fs) {
    var whatText = (q ? '\u201e' + esc(q) + '\u201c' : '') + (fs.length ? (q ? ' mit ' : '') + fs.map(esc).join(', ') : '');
    var head = (hits.length ? nf(hits.length) + ' Treffer f\u00fcr ' : 'Kein Eintrag passt zu ') + whatText + (city ? ' in der N\u00e4he von ' + esc(city) : '');
    var html = '<div class="results-head"><h2>' + head + '</h2><button type="button" class="btn ghost small" id="search-clear">Zur\u00fccksetzen</button></div>';
    if (hits.length) {
      html += '<div class="grid">' + hits.slice(0, 24).map(function (l) {
        return '<article class="card"><h3><a href="' + l.p + '">' + esc(l.n) + '</a></h3>' +
          (l.v ? '<p class="rating"><span class="stars" aria-hidden="true">' + stars(l.r) + '</span> ' + rf(l.r) + ' <span class="meta">(' + nf(l.v) + (l.v === 1 ? ' Bewertung' : ' Bewertungen') + ' bei Google)</span></p>' : '<p class="meta">Noch keine Bewertungen</p>') +
          '<p class="meta">' + esc(l.c) + (l.t ? ' (Sitz in ' + esc(l.t) + ')' : '') + '</p>' +
          (l.g ? '<p class="garantie ja">Festpreis-Garantie' + (l.gt ? ' \u00b7 T\u00fcr\u00f6ffnung ab ' + l.gt + ' \u20ac' : '') + '</p>' : '<p class="garantie nein">Noch keine Festpreis-Garantie</p>') +
          (l.a.length ? '<ul class="chips">' + chipsFor(l, q, fs).map(function (a) { return '<li>' + esc(a) + '</li>'; }).join('') + '</ul>' : '') + '</article>';
      }).join('') + '</div>';
      if (hits.length > 24) html += '<p class="meta">Die ersten 24 werden gezeigt. Erg\u00e4nzen Sie eine Stadt oder eine Leistung, um die Liste zu k\u00fcrzen.</p>';
    } else {
      html += '<p>Versuchen Sie ein k\u00fcrzeres Wort, eine andere Schreibweise, weniger Leistungen, oder w\u00e4hlen Sie eine Stadt aus der Liste.</p>';
    }
    results.innerHTML = html; results.hidden = false;
  }
  function runSearch(q, n, fs) {
    load().then(function () {
      // Ein eingegebener Anfang wie "Mann" wird zu der Stadt aufgelöst, die er beginnt, damit bei den
      // Treffern "in der Nähe von <dieser Stadt>" steht.
      var city = n ? (cityMatches(n)[0] || {}).n || n : '';
      var hits = index.listings.filter(function (l) { return matchWhat(l, q) && matchNear(l, city) && matchFilters(l, fs); }).sort(function (a, b) { return score(b) - score(a); });
      if (city !== n) near.value = city;
      render(hits, q, city, fs);
    });
  }

  // Es ist immer nur eine Liste offen.
  what.addEventListener('input', function () { hideAll(); showWhat(); });
  what.addEventListener('focus', function () { load(); hideAll(); showWhat(); });
  near.addEventListener('input', function () { hideAll(); showNear(); });
  near.addEventListener('focus', function () { hideAll(); showNear(); });
  what.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') hide(listWhat);
    if (e.key === 'Backspace' && !what.value) { var last = picked().pop(); if (last) setFilter(last, false); }
  });
  near.addEventListener('keydown', function (e) { if (e.key === 'Escape') hide(listNear); });
  document.addEventListener('click', function (e) { if (!form.contains(e.target)) hideAll(); });

  // Eine Wahl füllt die Felder; gesucht wird nur mit Suchen oder Eingabetaste.
  listWhat.addEventListener('click', function (e) {
    var b = e.target.closest('[data-pick]');
    if (b) { setFilter(b.dataset.pick, true); what.value = ''; hide(listWhat); what.focus(); }
  });
  pickedList.addEventListener('click', function (e) {
    var b = e.target.closest('[data-remove]');
    if (b) { setFilter(b.dataset.remove, false); what.focus(); }
  });
  listNear.addEventListener('click', function (e) {
    var a = e.target.closest('[data-city]'), b = e.target.closest('.use-location');
    if (a) { near.value = a.dataset.city; hide(listNear); near.focus(); }
    if (b) {
      b.textContent = 'N\u00e4chste Stadt wird gesucht\u2026';
      navigator.geolocation.getCurrentPosition(function (pos) {
        var c = nearestCity(pos.coords.latitude, pos.coords.longitude);
        if (c) { near.value = c.n; hide(listNear); near.focus(); }
      }, function () { b.textContent = 'Standort nicht verf\u00fcgbar. Geben Sie stattdessen eine Stadt ein.'; }, { timeout: 8000, maximumAge: 600000 });
    }
  });
  form.addEventListener('submit', function (e) {
    e.preventDefault(); hideAll();
    var q = what.value.trim(), n = near.value.trim(), fs = picked();
    if (!q && !fs.length && !n) { what.focus(); return; }
    var qs = new URLSearchParams();
    if (q) qs.set('s', q); if (n) qs.set('near', n); fs.forEach(function (f) { qs.append('f', f); });
    if (onSearchPage) {
      load().then(function () {
        // Nur eine Stadt: direkt auf deren Seite.
        if (!q && !fs.length) { var c = cityMatches(n)[0]; if (c) { location.href = c.p; return; } }
        runSearch(q, n, fs); history.replaceState(null, '', '/suche/?' + qs.toString());
      });
      return;
    }
    location.href = '/suche/?' + qs.toString();
  });
  if (onSearchPage) {
    var qs0 = new URLSearchParams(location.search);
    what.value = qs0.get('s') || ''; near.value = qs0.get('near') || '';
    qs0.getAll('f').forEach(function (f) { setFilter(f, true); });
    var q0 = what.value.trim(), n0 = near.value.trim(), f0 = picked();
    if (q0 || f0.length) runSearch(q0, n0, f0);
    else if (n0) load().then(function () { var c = cityMatches(n0)[0]; if (c) location.href = c.p; });
    results.addEventListener('click', function (e) {
      if (e.target.id === 'search-clear') {
        results.innerHTML = ''; what.value = ''; near.value = '';
        boxes.forEach(function (i) { i.checked = false; }); renderPicked();
        history.replaceState(null, '', '/suche/'); what.focus();
      }
    });
  }
})();
