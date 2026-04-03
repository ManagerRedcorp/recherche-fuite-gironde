#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, os

BASE = "C:/Users/Chou/Desktop/recherche-fuite-gironde"

with open(os.path.join(BASE, "villes.json"), encoding="utf-8") as f:
    raw = json.load(f)
villes = raw["villes"] if isinstance(raw, dict) else raw

ROOT = "https://recherche-fuite-gironde.fr"
TODAY = "2025-01-15"

urls = []

# Pages principales
urls.append({"loc": ROOT + "/", "priority": "1.0", "changefreq": "weekly"})
urls.append({"loc": ROOT + "/detection-fuite/", "priority": "0.9", "changefreq": "monthly"})
urls.append({"loc": ROOT + "/chemisage-canalisation/", "priority": "0.9", "changefreq": "monthly"})
urls.append({"loc": ROOT + "/guide/", "priority": "0.8", "changefreq": "monthly"})
urls.append({"loc": ROOT + "/contact/", "priority": "0.8", "changefreq": "monthly"})
urls.append({"loc": ROOT + "/mentions-legales/", "priority": "0.3", "changefreq": "yearly"})
urls.append({"loc": ROOT + "/plan-du-site/", "priority": "0.4", "changefreq": "monthly"})

# Guide
guide_slugs = [
    "comment-detecter-une-fuite",
    "causes-fuites-eau",
    "fuite-sous-dalle",
    "fuite-canalisation-enterree",
    "chemisage-explication",
    "cout-recherche-fuite",
    "assurance-fuite-eau",
    "urgence-fuite-eau",
    "faq",
]
for s in guide_slugs:
    urls.append({"loc": ROOT + "/guide/" + s + "/", "priority": "0.7", "changefreq": "monthly"})

# Villes
for v in villes:
    slug = v["slug"]
    urls.append({"loc": ROOT + "/villes/" + slug + "/", "priority": "0.8", "changefreq": "monthly"})
    urls.append({"loc": ROOT + "/villes/" + slug + "/chemisage/", "priority": "0.7", "changefreq": "monthly"})

lines = ['<?xml version="1.0" encoding="UTF-8"?>']
lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
for u in urls:
    lines.append("  <url>")
    lines.append("    <loc>{}</loc>".format(u["loc"]))
    lines.append("    <lastmod>{}</lastmod>".format(TODAY))
    lines.append("    <changefreq>{}</changefreq>".format(u["changefreq"]))
    lines.append("    <priority>{}</priority>".format(u["priority"]))
    lines.append("  </url>")
lines.append("</urlset>")

with open(os.path.join(BASE, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("sitemap.xml genere avec {} URLs".format(len(urls)))
