/**
 * UPRT+ Insights Series — self-mounting loader (Webflow-friendly)
 * Usage:
 *   <div id="ud-insights-mount"></div>
 *   <script
 *     src="https://cdn.jsdelivr.net/gh/kcourser/UD-insights-series@main/ud-insights-series.js"
 *     data-series-url="https://cdn.jsdelivr.net/gh/kcourser/UD-insights-series@main/series.json"
 *     defer></script>
 *
 * Or set data-series-url on #ud-insights-mount.
 * Owner: Hermes CTO 2026-08-04
 */
(function () {
  if (window.__UD_INSIGHTS_LOADER__) return;
  window.__UD_INSIGHTS_LOADER__ = true;

  var script = document.currentScript;
  var mount =
    document.getElementById('ud-insights-mount') ||
    document.querySelector('[data-ud-insights-mount]');
  if (!mount) {
    console.warn('[ud-insights] No #ud-insights-mount found');
    return;
  }

  var seriesUrl =
    (mount.getAttribute('data-series-url') ||
      (script && script.getAttribute('data-series-url')) ||
      '') ||
    '';

  // Resolve HTML sibling of this script when possible
  var base = '';
  if (script && script.src) {
    base = script.src.replace(/\/[^/]*$/, '/');
  }

  var htmlUrl = (script && script.getAttribute('data-html-url')) || base + 'ud-insights-series.html';

  function inject(htmlText) {
    // Extract style + body markup + scripts from the embed file
    var tmp = document.createElement('div');
    tmp.innerHTML = htmlText;

    // Move styles to head once
    tmp.querySelectorAll('style').forEach(function (st) {
      if (!document.getElementById('ud-insights-css')) {
        st.id = 'ud-insights-css';
        document.head.appendChild(st);
      } else {
        st.remove();
      }
    });

    var root = tmp.querySelector('#ud-insights');
    if (!root) {
      mount.textContent = 'UPRT+ insights embed missing #ud-insights root.';
      return;
    }
    if (seriesUrl) root.setAttribute('data-series-url', seriesUrl);

    mount.innerHTML = '';
    mount.appendChild(root);

    // Re-run inline scripts (innerHTML does not execute them when parsed via fetch)
    tmp.querySelectorAll('script').forEach(function (oldScript) {
      var s = document.createElement('script');
      if (oldScript.src) s.src = oldScript.src;
      else s.textContent = oldScript.textContent;
      document.body.appendChild(s);
    });
  }

  fetch(htmlUrl, { cache: 'no-cache' })
    .then(function (r) {
      if (!r.ok) throw new Error('HTML ' + r.status);
      return r.text();
    })
    .then(inject)
    .catch(function (err) {
      console.error('[ud-insights] loader failed', err);
      mount.innerHTML =
        '<div style="padding:24px;color:#9FB2CC;font-family:Poppins,system-ui,sans-serif;font-size:13px;">' +
        'Could not load UPRT+ insights embed. Paste <code>ud-insights-series.html</code> directly into the Webflow Embed, or fix the script URL.' +
        '</div>';
    });
})();
