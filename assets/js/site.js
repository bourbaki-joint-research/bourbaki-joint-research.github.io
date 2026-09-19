/* Bourbaki archive — search page rendering and listing filter.
   Data comes from assets/js/projects-data.js, which Jekyll generates
   from the _projects collection at build time. */
(function () {
  "use strict";

  var P = window.BOURBAKI_PROJECTS || [];
  var CATS = window.BOURBAKI_CATS || {};
  var BASE = window.BOURBAKI_BASE || "";
  var PREFIX = window.BOURBAKI_ID_PREFIX || "Bourbaki";

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function searchHref(q, type) {
    return BASE + "/search.html?query=" + encodeURIComponent(q) + "&searchtype=" + encodeURIComponent(type || "all");
  }

  function params() {
    var out = {};
    window.location.search.slice(1).split("&").forEach(function (pair) {
      if (!pair) return;
      var kv = pair.split("=");
      out[decodeURIComponent(kv[0])] = decodeURIComponent((kv[1] || "").replace(/\+/g, " "));
    });
    return out;
  }

  function highlight(text, needle) {
    var safe = esc(text);
    if (!needle) return safe;
    var re = new RegExp("(" + needle.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "ig");
    return safe.replace(re, "<mark>$1</mark>");
  }

  function catName(code) {
    return CATS[code] && CATS[code].name ? CATS[code].name : code;
  }

  function subjectLine(p) {
    return p.subjects
      .map(function (c, i) {
        var label = esc(catName(c) + " (" + c + ")");
        return i === 0 ? '<span class="primary-subject">' + label + "</span>" : label;
      })
      .join("; ");
  }

  function dateText(iso) {
    var d = new Date(iso);
    var m = ["January","February","March","April","May","June","July",
             "August","September","October","November","December"];
    return isNaN(d) ? iso : d.getDate() + " " + m[d.getMonth()] + ", " + d.getFullYear();
  }

  function fullTitle(p) {
    return p.title + (p.title_en ? " (" + p.title_en + ")" : "");
  }

  /* ------------------------------------------------------- search results */
  function matches(p, q, type) {
    if (!q) return true;
    var n = q.toLowerCase();
    var fields = {
      all: [p.title, p.title_en, p.abstract, p.team, p.identifier,
            p.authors.join(" "), p.subjects.join(" ")].join(" "),
      title: [p.title, p.title_en].join(" "),
      abstract: p.abstract,
      team: p.team + " " + p.authors.join(" "),
      id: p.identifier
    };
    return (fields[type] || fields.all).toLowerCase().indexOf(n) !== -1;
  }

  function renderSearch() {
    var host = document.getElementById("search-results");
    if (!host) return;

    var pr = params();
    var q = (pr.query || "").trim();
    var type = pr.searchtype || "all";

    var box = document.querySelector('.search-form input[name="query"]');
    if (box) box.value = q;
    var sel = document.querySelector('.search-form select[name="searchtype"]');
    if (sel) sel.value = type;

    var hits = P.filter(function (p) { return matches(p, q, type); });

    var summary = document.getElementById("search-summary");
    if (summary) {
      summary.innerHTML = q
        ? "Showing <strong>1&ndash;" + hits.length + "</strong> of <strong>" + hits.length +
          "</strong> results for " + esc(type === "all" ? "all fields" : type) +
          ": <strong>" + esc(q) + "</strong>"
        : "Showing all <strong>" + hits.length + "</strong> entries.";
    }

    if (!hits.length) {
      host.innerHTML = '<p class="search-empty">Sorry, your query returned no results. ' +
        '<a href="' + BASE + '/">Back to the full listing</a>.</p>';
      return;
    }

    host.innerHTML = hits.map(function (p) {
      var cut = p.abstract.length > 280;
      var shortA = esc(p.abstract.slice(0, 280)) + (cut ? "&hellip;" : "");
      return '<li class="arxiv-result">' +
        '<div class="list-identifier"><a href="' + esc(p.url) + '"><span class="id">' +
          PREFIX + ":" + esc(p.identifier) + "</span></a> " +
          '[<a href="' + esc(p.slides_url) + '" rel="noopener">slides</a>]</div>' +
        '<p class="list-title"><span class="descriptor">Title:</span> ' + highlight(fullTitle(p), q) + "</p>" +
        '<p class="list-authors"><span class="descriptor">Authors:</span> ' +
          p.authors.map(function (a) {
            return '<a href="' + searchHref(a, "team") + '">' + esc(a) + "</a>";
          }).join(", ") + "</p>" +
        '<p class="abstract-short" data-full="' + esc(p.abstract) + '" data-short="' + shortA + '">' +
          '<span class="descriptor">Abstract:</span> <span class="abs-body">' +
          highlight(p.abstract.slice(0, 280) + (cut ? "\u2026" : ""), q) + "</span> " +
          (cut ? '<a href="#" class="toggle">\u25bd More</a>' : "") + "</p>" +
        (p.comments ? '<p class="list-comments"><span class="descriptor">Comments:</span> ' + esc(p.comments) + "</p>" : "") +
        '<p class="list-subjects"><span class="descriptor">Subjects:</span> ' + subjectLine(p) + "</p>" +
        '<p class="list-comments">Submitted ' + dateText(p.submitted) + "</p>" +
        "</li>";
    }).join("");

    host.querySelectorAll(".toggle").forEach(function (a) {
      a.addEventListener("click", function (ev) {
        ev.preventDefault();
        var para = a.closest(".abstract-short");
        var body = para.querySelector(".abs-body");
        var open = a.textContent.indexOf("Less") !== -1;
        body.innerHTML = open ? para.dataset.short : para.dataset.full;
        a.textContent = open ? "\u25bd More" : "\u25b3 Less";
      });
    });

    if (window.MathJax && window.MathJax.typesetPromise) window.MathJax.typesetPromise([host]);
  }

  /* ------------------------------------------------------- listing filter */
  function initFilter() {
    var bar = document.getElementById("subject-filter");
    if (!bar) return;
    bar.addEventListener("click", function (ev) {
      var a = ev.target.closest("a[data-cat]");
      if (!a) return;
      ev.preventDefault();
      var cat = a.getAttribute("data-cat");
      bar.querySelectorAll("a[data-cat]").forEach(function (x) { x.style.fontWeight = "normal"; });
      a.style.fontWeight = "bold";
      var shown = 0;
      document.querySelectorAll("dl#articles > dt").forEach(function (dt) {
        var cats = (dt.getAttribute("data-cats") || "").split(" ");
        var on = cat === "all" || cats.indexOf(cat) !== -1;
        dt.style.display = on ? "" : "none";
        var dd = dt.nextElementSibling;
        if (dd && dd.tagName === "DD") dd.style.display = on ? "" : "none";
        if (on) shown++;
      });
      var t = document.getElementById("entry-total");
      if (t) t.textContent = String(shown);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initFilter();
    renderSearch();
  });
})();
