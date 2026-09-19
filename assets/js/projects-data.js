---
layout: null
---
{%- assign projects = site.projects | sort: "identifier" -%}
window.BOURBAKI_PROJECTS = [
{%- for p in projects %}
  {
    "identifier": {{ p.identifier | jsonify }},
    "team": {{ p.team | jsonify }},
    "title": {{ p.title | jsonify }},
    "title_en": {{ p.title_en | default: "" | jsonify }},
    "authors": {{ p.authors | jsonify }},
    "subjects": {{ p.subjects | jsonify }},
    "comments": {{ p.comments | default: "" | jsonify }},
    "slides_url": {{ p.slides_url | jsonify }},
    "submitted": {{ p.submitted | date: "%Y-%m-%dT%H:%M:%S" | jsonify }},
    "url": {{ p.url | relative_url | jsonify }},
    "abstract": {{ p.content | strip_html | normalize_whitespace | jsonify }}
  }{% unless forloop.last %},{% endunless %}
{%- endfor %}
];
window.BOURBAKI_CATS = {{ site.data.categories | jsonify }};
window.BOURBAKI_BASE = {{ site.baseurl | default: '' | jsonify }};
window.BOURBAKI_ID_PREFIX = {{ site.id_prefix | jsonify }};
