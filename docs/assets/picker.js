(function(){
  var sys = document.getElementById('pk-sys'), fam = document.getElementById('pk-fam'), go = document.getElementById('pk-go');
  var out = document.getElementById('pk-out'), boxes = [].slice.call(document.querySelectorAll('input[name=pk-wo]'));
  if (!go) return;
  var data = null;
  function load(){ return data ? Promise.resolve(data) : fetch('assets/search.json').then(function(r){ return r.json(); }).then(function(d){ data = d; return d; }); }
  function esc(s){ return String(s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function thumb(u){ if (u && u.indexOf('http') !== 0) u = 'https://m.media-amazon.com/images/I/' + u; return u ? u.replace(/\._[^/]*_\.(jpg|png)$/i, '._AC_US160_.$1') : ''; }
  function wired(){ var o = fam.options[fam.selectedIndex]; return o && o.dataset.wired === '1'; }
  function sync(){
    go.disabled = !fam.value;
    var nb = boxes.filter(function(b){ return b.value === 'neutral'; })[0];
    if (nb){ nb.disabled = !wired(); if (nb.disabled) nb.checked = false; nb.parentNode.classList.toggle('off', nb.disabled); }
  }
  [sys, fam].forEach(function(el){ el.addEventListener('change', function(){ sync(); load(); }); });
  sync();
  function matches(d, s, f, wo){
    var seen = {}, list = [];
    d.forEach(function(e){
      if (e.t !== 'p' || e.f !== f) return;
      if (s && (' ' + e.y + ' ').indexOf(' ' + s + ' ') < 0) return;
      var ok = ' ' + e.o + ' ';
      for (var i = 0; i < wo.length; i++) if (ok.indexOf(' ' + wo[i] + ' ') < 0) return;
      var id = e.u.split('#')[1] || e.n;
      if (seen[id] && seen[id].s >= e.s) return;
      seen[id] = e;
    });
    for (var k in seen) list.push(seen[k]);
    list.sort(function(a, b){ return (b.s - a.s) || (b.c - a.c); });
    return list;
  }
  // top picks: best scores, but one per brand when there's a choice
  function top(list, n){
    var picks = [], brands = {};
    list.forEach(function(e){ var br = e.n.split(' ')[0]; if (picks.length < n && !brands[br]){ brands[br] = 1; picks.push(e); } });
    list.forEach(function(e){ if (picks.length < n && picks.indexOf(e) < 0) picks.push(e); });
    return picks;
  }
  function card(e){
    return '<a class="pk-card" href="' + esc(e.u) + '"><img src="' + esc(thumb(e.i)) + '" alt="">' +
      '<span class="pk-body">' + (e.a ? '<span class="ss-badge">' + esc(e.a) + '</span>' : '') +
      '<b>' + esc(e.n) + '</b><span class="pk-meta">' + esc(e.g) + '</span>' +
      '<span class="pk-meta">$' + e.pr.toFixed(2) + ' &middot; ' + e.r + '&#9733; &middot; score ' + e.s + '</span>' +
      '<span class="pk-link">Read the review &rarr;</span></span></a>';
  }
  go.addEventListener('click', function(){
    var s = sys.value, f = fam.value, wo = boxes.filter(function(b){ return b.checked && !b.disabled; }).map(function(b){ return b.value; });
    var famName = fam.options[fam.selectedIndex].text, sysName = s ? sys.options[sys.selectedIndex].text : '';
    out.innerHTML = '<p class="muted">Finding your picks...</p>';
    load().then(function(d){
      var all = matches(d, '', f, []), hit = matches(d, s, f, wo);
      var params = []; if (s) params.push('system=' + encodeURIComponent(s)); if (wo.length) params.push('without=' + wo.join(','));
      var link = f + '.html' + (params.length ? '?' + params.join('&') : '');
      var what = famName.toLowerCase() + (sysName ? ' that work with ' + sysName : '') +
        (wo.length ? (sysName ? ' and' : ' that') + ' work without ' + wo.map(function(w){ return {neutral: 'a neutral wire', hub: 'a hub', sub: 'a subscription'}[w]; }).join(' or ') : '');
      var html;
      if (!hit.length){
        html = '<p><b>None of the ' + all.length + ' ' + esc(famName.toLowerCase()) + ' we rank match all of that.</b> ' +
          'Try dropping one of the "work without" options' + (s ? ', or pick a different system' : '') + '. Here are the top picks overall:</p>' +
          '<div class="pk-cards">' + top(all, 3).map(card).join('') + '</div>' +
          '<a class="btn ghost" href="' + esc(f) + '.html">Compare all ' + all.length + ' ' + esc(famName.toLowerCase()) + '</a>';
      } else {
        html = '<p><b>' + hit.length + ' of ' + all.length + '</b> ' + esc(what) + (hit.length === 1 ? '. Our pick:</p>' : '. Our top ' + Math.min(3, hit.length) + ':</p>') +
          '<div class="pk-cards">' + top(hit, 3).map(card).join('') + '</div>' +
          '<a class="btn ghost" href="' + esc(link) + '">See all ' + hit.length + ' in one table &rarr;</a>';
        if (!s) html += '<p class="tiny muted pk-tip">Starting fresh? Matter devices work with Apple Home, Google Home, Alexa, SmartThings, and Home Assistant, so you aren\'t locked in.</p>';
      }
      html += '<p class="tiny muted">Ranked by each product\'s score on its own protocol page. <a href="how-we-rank.html">How we rank</a></p>';
      out.innerHTML = html;
      out.scrollIntoView({behavior: 'smooth', block: 'nearest'});
    });
  });
})();
