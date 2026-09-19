/* Bourbaki archive — shared client-side behaviour.
   Works both as a multi-page GitHub Pages site and inside the single-file
   preview build (body[data-mode="preview"], hash based routing). */
(function () {
  "use strict";

  var P = window.BOURBAKI_PROJECTS || [];
  var MODE = document.body.getAttribute("data-mode") === "preview" ? "preview" : "static";

  /* ------------------------------------------------------------ helpers */
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function absHref(id) {
    return MODE === "preview" ? "#/abs/" + id : "abs/" + id + "/";
  }

  function searchHref(q, type) {
    var qs = "query=" + encodeURIComponent(q) + "&searchtype=" + encodeURIComponent(type || "all");
    return MODE === "preview" ? "#/search?" + qs : "search.html?" + qs;
  }

  function params() {
    var raw = window.location.search.slice(1);
    if (MODE === "preview") {
      var h = window.location.hash;
      var i = h.indexOf("?");
      raw = i === -1 ? "" : h.slice(i + 1);
    }
    var out = {};
    raw.split("&").forEach(function (pair) {
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

  function subjectLine(p) {
    return p.categories
      .map(function (c, i) {
        var name = (window.BOURBAKI_CATS[c] || [c, c])[1] + " (" + c + ")";
        return i === 0 ? '<span class="primary-subject">' + esc(name) + "</span>" : esc(name);
      })
      .join("; ");
  }

  function dateText(iso) {
    var d = new Date(iso);
    var months = ["January","February","March","April","May","June","July","August","September","October","November","December"];
    return d.getDate() + " " + months[d.getMonth()] + ", " + d.getFullYear();
  }

  /* ------------------------------------------------------- search results */
  function matches(p, q, type) {
    if (!q) return true;
    var n = q.toLowerCase();
    var fields = {
      all: [p.title, p.title_en, p.abstract, p.team, p.id, p.authors.join(" "), p.categories.join(" ")].join(" "),
      title: [p.title, p.title_en].join(" "),
      abstract: p.abstract,
      team: p.team + " " + p.authors.join(" "),
      id: p.id
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
          "</strong> results for " + esc(type === "all" ? "all fields" : type) + ": <strong>" + esc(q) + "</strong>"
        : "Showing all <strong>" + hits.length + "</strong> entries.";
    }

    if (!hits.length) {
      host.innerHTML = '<p class="search-empty">Sorry, your query returned no results. ' +
        '<a href="' + (MODE === "preview" ? "#/" : "index.html") + '">Back to the full listing</a>.</p>';
      return;
    }

    host.innerHTML = hits.map(function (p) {
      var title = p.title + (p.title_en ? " (" + p.title_en + ")" : "");
      var full = esc(p.abstract);
      var shortA = p.abstract.length > 280 ? esc(p.abstract.slice(0, 280)) + "&hellip;" : full;
      return '<li class="arxiv-result" style="margin:22px 0;list-style:none">' +
        '<div class="list-identifier"><a href="' + absHref(p.id) + '"><span class="id">Bourbaki:' + p.id + "</span></a> " +
        '[<a href="' + esc(p.slides_url) + '" rel="noopener">slides</a>]</div>' +
        '<p class="list-title"><span class="descriptor">Title:</span> ' + highlight(title, q) + "</p>" +
        '<p class="list-authors"><span class="descriptor">Authors:</span> ' +
          p.authors.map(function (a) { return '<a href="' + searchHref(a, "team") + '">' + esc(a) + "</a>"; }).join(", ") + "</p>" +
        '<p class="abstract-short" data-full="' + full + '" data-short="' + shortA + '">' +
          '<span class="descriptor">Abstract:</span> <span class="abs-body">' + highlight(p.abstract.slice(0, 280) + (p.abstract.length > 280 ? "\u2026" : ""), q) + "</span> " +
          (p.abstract.length > 280 ? '<a href="#" class="toggle">\u25bd More</a>' : "") + "</p>" +
        '<p class="list-comments"><span class="descriptor">Comments:</span> ' + esc(p.comments) + "</p>" +
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

  /* ---------------------------------------------------------- search form */
  function initForms() {
    document.querySelectorAll("form.search-form").forEach(function (f) {
      f.addEventListener("submit", function (ev) {
        if (MODE !== "preview") return; /* static site: normal GET */
        ev.preventDefault();
        var q = f.querySelector('input[name="query"]').value;
        var t = f.querySelector('select[name="searchtype"]').value;
        window.location.hash = "/search?query=" + encodeURIComponent(q) + "&searchtype=" + t;
      });
    });
  }

  /* -------------------------------------------------------------- router */
  function route() {
    if (MODE !== "preview") return;
    var h = window.location.hash.replace(/^#/, "");
    var qi = h.indexOf("?");
    var path = (qi === -1 ? h : h.slice(0, qi)) || "/";
    var target = document.querySelector('[data-route="' + path + '"]') ||
                 document.querySelector('[data-route="/"]');
    document.querySelectorAll("[data-route]").forEach(function (s) {
      s.hidden = s !== target;
    });
    if (path === "/search") renderSearch();
    window.scrollTo(0, 0);
    if (window.MathJax && window.MathJax.typesetPromise) window.MathJax.typesetPromise([target]);
  }

  document.addEventListener("DOMContentLoaded", function () {
    initForms();
    initFilter();
    if (MODE === "preview") {
      window.addEventListener("hashchange", route);
      route();
    } else {
      renderSearch();
    }
  });
})();
