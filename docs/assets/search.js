(function(){
  var forms = document.querySelectorAll('.site-search');
  var idx = null, loading = null;
  function load(){
    if (idx) return Promise.resolve(idx);
    if (!loading) loading = fetch('assets/search.json').then(function(r){ return r.json(); })
      .then(function(d){
        d.forEach(function(e){
          var raw = (e.n + ' ' + e.g + ' ' + (e.k || '')).toLowerCase();
          e._h = ' ' + raw.replace(/[^a-z0-9]+/g, ' ') + ' ' + raw.replace(/[^a-z0-9]/g, '');
          e._n = ' ' + e.n.toLowerCase().replace(/[^a-z0-9]+/g, ' ');
        });
        idx = d; return d;
      });
    return loading;
  }
  function tokens(q){ return q.toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim().split(' ').filter(Boolean); }
  var TYPE = {r: 3, f: 2.5, s: 1, p: 0, a: -0.5};
  function search(q){
    var ts = tokens(q); if (!ts.length) return [];
    var out = [];
    idx.forEach(function(e){
      var sc = 0;
      for (var i = 0; i < ts.length; i++){
        var tk = ts[i];
        if (e._h.indexOf(tk) < 0) return;
        sc += e._n.indexOf(' ' + tk) >= 0 ? 4 : (e._n.indexOf(tk) >= 0 ? 3 : (e._h.indexOf(' ' + tk) >= 0 ? 1.5 : 1));
      }
      sc += TYPE[e.t] || 0;
      if (e.t !== 'p' && e.t !== 'a') { var all = ts.every(function(tk){ return e._n.indexOf(tk) >= 0; }); if (all) sc += 4; }
      out.push([sc + (e.s || 0) / 1000, e]);
    });
    out.sort(function(a, b){ return b[0] - a[0]; });
    return out.map(function(x){ return x[1]; });
  }
  function esc(s){ return String(s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function thumb(u){ if (u && u.indexOf('http') !== 0) u = 'https://m.media-amazon.com/images/I/' + u; return u ? u.replace(/\._[^/]*_\.(jpg|png)$/i, '._AC_US80_.$1') : ''; }
  function item(e, full){
    var img = e.i ? '<img src="' + esc(thumb(e.i)) + '" alt=""' + (full ? ' loading="lazy"' : '') + '>' : '<span class="ss-ico">' + (e.t === 'f' ? '&#9638;' : e.t === 'r' ? '&#9733;' : '&#8250;') + '</span>';
    var meta = e.pr != null ? ('$' + e.pr.toFixed(2) + (e.r ? ' &middot; ' + e.r + '&#9733;' : '')) : '';
    var badge = e.a ? '<span class="ss-badge' + (e.t === 'a' ? ' bad' : '') + '">' + esc(e.a) + '</span>' : '';
    return '<a class="ss-item' + (full ? ' full' : '') + '" role="option" href="' + esc(e.u) + '">' + img +
      '<span class="ss-txt"><span class="ss-n">' + esc(e.n) + badge + '</span><span class="ss-g">' + esc(e.g) +
      (meta ? ' &middot; ' + meta : '') + '</span></span></a>';
  }
  forms.forEach(function(form){
    var inp = form.querySelector('input'), panel = form.querySelector('.ss-panel'), sel = -1, timer;
    function close(){ panel.hidden = true; inp.setAttribute('aria-expanded', 'false'); sel = -1; }
    function render(){
      var q = inp.value.trim();
      if (q.length < 2){ close(); return; }
      load().then(function(){
        var res = search(q), pages = res.filter(function(e){ return e.t !== 'p' && e.t !== 'a'; }).slice(0, 3),
            prods = res.filter(function(e){ return e.t === 'p' || e.t === 'a'; }).slice(0, 7);
        var html = pages.concat(prods).map(function(e){ return item(e); }).join('');
        html += res.length ? '<a class="ss-all" href="search.html?q=' + encodeURIComponent(q) + '">' + (res.length === 1 ? 'See 1 result' : 'See all ' + res.length + ' results') + '</a>'
                           : '<div class="ss-none">No matches for "' + esc(q) + '"</div>';
        panel.innerHTML = html; panel.hidden = false; inp.setAttribute('aria-expanded', 'true'); sel = -1;
      });
    }
    inp.addEventListener('focus', load);
    inp.addEventListener('input', function(){ clearTimeout(timer); timer = setTimeout(render, 80); });
    inp.addEventListener('keydown', function(ev){
      var its = panel.querySelectorAll('a');
      if (ev.key === 'ArrowDown' || ev.key === 'ArrowUp'){
        if (panel.hidden || !its.length) return;
        ev.preventDefault();
        sel = (sel + (ev.key === 'ArrowDown' ? 1 : -1) + its.length) % its.length;
        its.forEach(function(a, i){ a.classList.toggle('on', i === sel); });
        its[sel].scrollIntoView({block: 'nearest'});
      } else if (ev.key === 'Enter' && sel >= 0 && its[sel]){ ev.preventDefault(); location.href = its[sel].href; }
      else if (ev.key === 'Escape'){ close(); }
    });
    document.addEventListener('click', function(ev){ if (!form.contains(ev.target)) close(); });
  });
  // full results page
  var list = document.getElementById('sr-list');
  if (list){
    var q = new URLSearchParams(location.search).get('q') || '';
    document.querySelectorAll('.site-search input').forEach(function(i){ i.value = q; });
    if (q.trim()) load().then(function(){
      var res = search(q);
      document.getElementById('sr-h').textContent = 'Results for "' + q + '"';
      document.getElementById('sr-sum').textContent = res.length ? res.length + (res.length === 1 ? ' match.' : ' matches across products and review pages.') : 'No matches. Try a brand, a model number, or a device type like "smart plug".';
      list.innerHTML = res.slice(0, 200).map(function(e){ return item(e, true); }).join('');
    });
  }
})();
