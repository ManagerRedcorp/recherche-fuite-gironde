# -*- coding: utf-8 -*-
"""
Générateur complet du site recherche-fuite-gironde.fr
Génère : 60 pages villes + pages statiques + guide + sitemap
"""

import json, os, sys, re
from pathlib import Path

BASE = Path(__file__).parent
sys.stdout.reconfigure(encoding='utf-8')

# ── Données villes ──────────────────────────────────────────
with open(BASE / 'villes.json', encoding='utf-8') as f:
    data = json.load(f)
VILLES = data['villes']

# ── Header commun ────────────────────────────────────────────
def header(active=''):
    return f'''<header class="site-header">
  <div class="container">
    <div class="header-inner">
      <a href="/" class="logo">Recherche Fuite <strong>Gironde</strong></a>
      <input type="checkbox" id="nav-toggle" class="nav-toggle" aria-hidden="true">
      <nav class="nav" id="main-nav">
        <a href="/">Accueil</a>
        <a href="/detection-fuite/">Détection de fuite</a>
        <a href="/chemisage-canalisation/">Chemisage</a>
        <a href="/guide/">Guide</a>
        <a href="/devis/" class="btn btn-gold">Devis gratuit</a>
      </nav>
      <label for="nav-toggle" class="burger" aria-label="Menu">
        <span></span><span></span><span></span>
      </label>
    </div>
  </div>
</header>'''

# ── Footer commun ─────────────────────────────────────────────
def footer():
    villes_footer = '\n'.join([
        f'<li><a href="/villes/{v["slug"]}/">{v["nom"]}</a></li>'
        for v in VILLES[:8]
    ])
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="/" class="logo">Recherche Fuite <strong>Gironde</strong></a>
        <p class="footer-desc">Spécialiste de la recherche de fuites d'eau en Gironde (33). Intervention sur 30 communes. Méthodes non destructives, rapport assurance.</p>
      </div>
      <div class="footer-col">
        <h4>Nos services</h4>
        <ul>
          <li><a href="/detection-fuite/">Détection de fuite</a></li>
          <li><a href="/chemisage-canalisation/">Chemisage de canalisation</a></li>
          <li><a href="/guide/">Guide pratique</a></li>
          <li><a href="/devis/">Devis gratuit</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Villes principales</h4>
        <ul>
          {villes_footer}
        </ul>
      </div>
      <div class="footer-col">
        <h4>Informations</h4>
        <ul>
          <li><a href="/guide/">Guide fuite d'eau</a></li>
          <li><a href="/guide/faq/">FAQ</a></li>
          <li><a href="/contact/">Contact</a></li>
          <li><a href="/plan-du-site/">Plan du site</a></li>
          <li><a href="/mentions-legales/">Mentions légales</a></li>
        </ul>
      </div>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="container">
      &copy; 2025 Recherche Fuite Gironde &mdash; Site d'information et de mise en relation
    </div>
  </div>
</footer>
<script>
  const toggle = document.getElementById('nav-toggle');
  const nav = document.getElementById('main-nav');
  if (toggle && nav) {{
    toggle.addEventListener('change', () => {{
      nav.classList.toggle('open', toggle.checked);
    }});
  }}
</script>'''

# ── Formulaire contact (version section dark) ─────────────────
def form_section(ville_defaut=''):
    options = '\n'.join([
        f'<option value="{v["nom"]}"{" selected" if v["nom"]==ville_defaut else ""}>{v["nom"]} ({v["code_postal"]})</option>'
        for v in VILLES
    ])
    return f'''<section class="section-dark" id="contact">
  <div class="container">
    <div class="contact-layout">
      <div>
        <span class="badge badge-gold">Devis gratuit &bull; Sans engagement</span>
        <h2 class="section-title" style="margin-top:1.25rem;">Décrivez votre situation, nous vous répondons</h2>
        <p style="color:rgba(247,246,242,.65);font-size:1.0625rem;line-height:1.65;margin-bottom:0;">Remplissez le formulaire. Un technicien vous contacte sous 24h pour valider votre besoin et établir un devis.</p>
        <ul class="contact-check-list">
          <li class="contact-check"><img src="/assets/icons/tick-circle.svg" alt="">Gratuit et sans engagement</li>
          <li class="contact-check"><img src="/assets/icons/clock.svg" alt="">Réponse sous 24h ouvrées</li>
          <li class="contact-check"><img src="/assets/icons/lock.svg" alt="">Vos données restent confidentielles</li>
        </ul>
      </div>
      <form action="https://formsubmit.co/sites-recherche-fuite@outlook.com" method="POST">
        <input type="hidden" name="_subject" value="[recherche-fuite-gironde.fr] Nouvelle demande de devis">
        <input type="hidden" name="_captcha" value="false">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_next" id="next-url" value="/merci/">
        <script>document.getElementById("next-url").value=window.location.origin+"/merci/";</script>
        <input type="hidden" name="site_source" value="recherche-fuite-gironde.fr">
        <div class="form-grid-2" style="margin-bottom:1rem;">
          <div class="form-group">
            <label class="form-label" for="prenom">Prénom</label>
            <input class="form-input" type="text" id="prenom" name="prenom" placeholder="Votre prénom" required>
          </div>
          <div class="form-group">
            <label class="form-label" for="nom">Nom</label>
            <input class="form-input" type="text" id="nom" name="nom" placeholder="Votre nom" required>
          </div>
        </div>
        <div class="form-grid-2" style="margin-bottom:1rem;">
          <div class="form-group">
            <label class="form-label" for="telephone">Téléphone</label>
            <input class="form-input" type="tel" id="telephone" name="telephone" placeholder="06 XX XX XX XX" required>
          </div>
          <div class="form-group">
            <label class="form-label" for="email">Email</label>
            <input class="form-input" type="email" id="email" name="email" placeholder="votre@email.fr" required>
          </div>
        </div>
        <div class="form-group" style="margin-bottom:1rem;">
          <label class="form-label" for="ville-select">Votre ville</label>
          <select class="form-input form-select" id="ville-select" name="ville" required>
            <option value="">Choisir une ville</option>
            {options}
            <option value="Autre">Autre ville de Gironde</option>
          </select>
        </div>
        <div class="form-group" style="margin-bottom:1rem;">
          <label class="form-label" for="probleme">Type de problème</label>
          <select class="form-input form-select" id="probleme" name="probleme" required>
            <option value="">Choisir</option>
            <option value="Fuite visible">Fuite visible (tache, humidité)</option>
            <option value="Compteur anormal">Compteur d'eau anormal</option>
            <option value="Fuite sous dalle">Suspicion de fuite sous dalle</option>
            <option value="Fuite enterrée">Fuite canalisation enterrée</option>
            <option value="Chemisage">Chemisage de canalisation</option>
            <option value="Rapport assurance">Rapport pour assurance</option>
            <option value="Autre">Autre</option>
          </select>
        </div>
        <div class="form-group" style="margin-bottom:1.5rem;">
          <label class="form-label" for="message">Décrivez votre situation</label>
          <textarea class="form-input form-textarea" id="message" name="message" placeholder="Ex : compteur qui tourne la nuit, tache d'humidité au plafond, sol chaud..." required></textarea>
        </div>
        <button type="submit" class="btn btn-gold btn-full">Envoyer ma demande</button>
        <p style="font-size:.8rem;color:rgba(247,246,242,.4);text-align:center;margin-top:.75rem;">Aucune donnée personnelle n'est transmise à des tiers. Réponse sous 24h ouvrées.</p>
      </form>
    </div>
  </div>
</section>'''

# ── Maillage villes (autres villes) ──────────────────────────
def maillage_villes(slug_actuel='', limit=12):
    autres = [v for v in VILLES if v['slug'] != slug_actuel][:limit]
    cards = '\n'.join([
        f'<a href="/villes/{v["slug"]}/" class="ville-card"><img src="/assets/icons/map-pin.svg" alt=""><span>{v["nom"]}</span><span class="ville-card-cp">{v["code_postal"]}</span></a>'
        for v in autres
    ])
    return f'''<section class="section-alt">
  <div class="container">
    <h2 class="maillage-title">Nous intervenons aussi dans ces villes</h2>
    <div class="grid-auto">{cards}</div>
  </div>
</section>'''

def villes_detection_section():
    cards = '\n'.join([
        f'<a href="/villes/{v["slug"]}/" class="ville-card"><img src="/assets/icons/map-pin.svg" alt=""><span>{v["nom"]}</span><span class="ville-card-cp">{v["code_postal"]}</span></a>'
        for v in VILLES
    ])
    return f'''<section class="section-alt">
  <div class="container">
    <div class="section-header-center">
      <span class="section-eyebrow">Zones d\'intervention</span>
      <h2 class="section-title">Détection de fuite dans toute la Gironde</h2>
      <p class="section-lead">Nous intervenons dans les 30 principales communes du département (33). Cliquez sur votre ville pour voir les détails de notre service.</p>
    </div>
    <div class="grid-auto">{cards}</div>
  </div>
</section>'''

def villes_chemisage_section():
    cards = '\n'.join([
        f'<a href="/villes/{v["slug"]}/chemisage/" class="ville-card"><img src="/assets/icons/map-pin.svg" alt=""><span>{v["nom"]}</span><span class="ville-card-cp">{v["code_postal"]}</span></a>'
        for v in VILLES
    ])
    return f'''<section class="section-alt">
  <div class="container">
    <div class="section-header-center">
      <span class="section-eyebrow">Zones d\'intervention</span>
      <h2 class="section-title">Chemisage de canalisation dans toute la Gironde</h2>
      <p class="section-lead">Nous réalisons le chemisage de canalisations dans les 30 principales communes du département (33). Cliquez sur votre ville pour en savoir plus.</p>
    </div>
    <div class="grid-auto">{cards}</div>
  </div>
</section>'''

# ── Template HTML de base ─────────────────────────────────────
def html_base(title, description, canonical, body, extra_ld='', hide_sticky_cta=False):
    sticky = '' if hide_sticky_cta else '''<div class="sticky-cta-mobile">
  <a href="/devis/">Devis gratuit &rarr;</a>
</div>'''
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical}">
  <link rel="stylesheet" href="/assets/css/style.css">
  {extra_ld}
</head>
<body>
{header()}
{body}
{footer()}
{sticky}
</body>
</html>'''

# ── Générateur page ville — détection ────────────────────────
def page_ville_detection(v):
    nom = v['nom']
    cp = v['code_postal']
    slug = v['slug']
    q = v['quartiers']
    quartiers_str = ', '.join(q)

    # Villes voisines (2 villes proches dans la liste)
    idx = next((i for i, x in enumerate(VILLES) if x['slug'] == slug), 0)
    voisines = [VILLES[(idx-1) % len(VILLES)], VILLES[(idx+1) % len(VILLES)]]

    ld = f'''<script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "Recherche Fuite Gironde",
    "description": "Recherche de fuite d'eau à {nom} ({cp}). Détection non destructive, intervention rapide en Gironde.",
    "url": "https://recherche-fuite-gironde.fr/villes/{slug}/",
    "areaServed": {{
      "@type": "City",
      "name": "{nom}",
      "postalCode": "{cp}",
      "addressCountry": "FR"
    }},
    "serviceType": "Recherche de fuite d'eau"
  }}
  </script>'''

    mini_form = f'''<div class="ville-cta-card">
  <h3>Intervention à {nom}</h3>
  <form action="https://formsubmit.co/sites-recherche-fuite@outlook.com" method="POST" class="ville-cta-form">
    <input type="hidden" name="_subject" value="[recherche-fuite-gironde.fr] Demande détection à {nom}">
    <input type="hidden" name="_captcha" value="false">
    <input type="hidden" name="ville" value="{nom}">
    <input type="hidden" name="site_source" value="recherche-fuite-gironde.fr/villes/{slug}/">
    <div class="form-group" style="margin-bottom:.75rem;">
      <label class="form-label" for="nom-mini">Nom et prénom</label>
      <input class="form-input" type="text" id="nom-mini" name="nom" placeholder="Nom et prénom" required>
    </div>
    <div class="form-group" style="margin-bottom:.75rem;">
      <label class="form-label" for="tel-mini">Téléphone</label>
      <input class="form-input" type="tel" id="tel-mini" name="telephone" placeholder="06 XX XX XX XX" required>
    </div>
    <div class="form-group" style="margin-bottom:.75rem;">
      <label class="form-label" for="email-mini">Email</label>
      <input class="form-input" type="email" id="email-mini" name="email" placeholder="votre@email.fr" required>
    </div>
    <div class="form-group" style="margin-bottom:.75rem;">
      <label class="form-label" for="probleme-mini">Type de problème</label>
      <select class="form-input form-select" id="probleme-mini" name="probleme" required>
        <option value="">Choisir</option>
        <option value="Fuite visible">Fuite visible (tache, humidité)</option>
        <option value="Compteur anormal">Compteur d'eau anormal</option>
        <option value="Fuite sous dalle">Suspicion de fuite sous dalle</option>
        <option value="Fuite enterrée">Fuite canalisation enterrée</option>
        <option value="Chemisage">Chemisage de canalisation</option>
        <option value="Rapport assurance">Rapport pour assurance</option>
        <option value="Autre">Autre</option>
      </select>
    </div>
    <div class="form-group" style="margin-bottom:.75rem;">
      <label class="form-label" for="msg-mini">Votre situation</label>
      <textarea class="form-input form-textarea" id="msg-mini" name="message" placeholder="Décrivez votre problème..." style="min-height:80px;" required></textarea>
    </div>
    <button type="submit" class="btn btn-green btn-full">Envoyer ma demande</button>
  </form>
</div>'''

    body = f'''
<section class="hero-mini">
  <div class="container">
    <nav class="breadcrumb">
      <a href="/">Accueil</a>
      <span>&rsaquo;</span>
      <a href="/#villes">Villes</a>
      <span>&rsaquo;</span>
      <span>{nom}</span>
    </nav>
    <span class="badge badge-gold" style="margin-bottom:1rem;">Gironde &bull; {cp}</span>
    <h1>Recherche de fuite à {nom} ({cp})</h1>
    <p class="hero-mini-lead">Détection de fuite non destructive à {nom}. Nos techniciens interviennent dans les quartiers {quartiers_str} et sur l'ensemble de la commune.</p>
    <a href="/devis/" class="btn btn-gold" style="margin-top:1.5rem;display:inline-block;">Demander un devis gratuit</a>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="ville-layout">
      <div class="ville-content">
        <h2 class="section-title">Détection de fuite d'eau à {nom}</h2>
        <p>Une fuite d'eau à {nom} peut rester invisible pendant plusieurs semaines, notamment lorsqu'elle se trouve sous dalle, en canalisation enterrée ou dans une paroi encastrée. Les dégâts s'accumulent : humidité structurelle, moisissures, factures d'eau anormales.</p>
        <p>Nos techniciens interviennent à {nom} et dans les quartiers de {quartiers_str} avec des équipements de détection professionnels : corrélation acoustique, caméra endoscopique, thermographie infrarouge et gaz traceur. La fuite est localisée avec précision avant toute ouverture.</p>

        <h2 class="section-title" style="margin-top:2.5rem;">Nos interventions à {nom}</h2>
        <div class="grid-3" style="margin-top:1.5rem;">
          <div class="arg-card">
            <div class="arg-card-icon"><img src="/assets/icons/search.svg" alt=""></div>
            <h3>Fuite sous dalle</h3>
            <p>Localisation précise sous carrelage ou béton à {nom}, sans démolition préalable.</p>
          </div>
          <div class="arg-card">
            <div class="arg-card-icon"><img src="/assets/icons/map-pin.svg" alt=""></div>
            <h3>Canalisation enterrée</h3>
            <p>Détection acoustique sur les réseaux enterrés dans les jardins et voiries de {nom}.</p>
          </div>
          <div class="arg-card">
            <div class="arg-card-icon"><img src="/assets/icons/tick-badge.svg" alt=""></div>
            <h3>Rapport assurance</h3>
            <p>Document officiel remis après chaque intervention, reconnu par les assureurs.</p>
          </div>
        </div>

        <h2 class="section-title" style="margin-top:2.5rem;">Zone d'intervention à {nom}</h2>
        <p>Nous couvrons l'ensemble des quartiers de {nom} : {quartiers_str}. Nos techniciens se déplacent également dans les communes voisines de {voisines[0]["nom"]} et {voisines[1]["nom"]}.</p>
        <p>Besoin d'une intervention rapide à {nom} ? Remplissez le formulaire ci-contre ou utilisez le formulaire de contact en bas de page.</p>

        <h2 class="section-title" style="margin-top:2.5rem;">Chemisage de canalisation à {nom}</h2>
        <p>Une fois la fuite détectée, nous pouvons également réaliser un <a href="/villes/{slug}/chemisage/" style="color:var(--green);text-decoration:underline;">chemisage de canalisation à {nom}</a>. Cette technique de rénovation sans travaux permet de remettre en état le réseau sans ouvrir les murs ni les sols.</p>

        <div class="temoignage-card" style="margin-top:2rem;">
          <div class="temoignage-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
          <p class="temoignage-text">« Intervention rapide et professionnelle à {nom}. La fuite a été trouvée en moins de deux heures, sans casse. Le rapport fourni a été accepté par notre assurance sans discussion. »</p>
          <div class="temoignage-author">Client à {nom} ({cp})</div>
        </div>
      </div>

      <div class="ville-sidebar">
        {mini_form}
      </div>
    </div>
  </div>
</section>

{form_section(nom)}
{maillage_villes(slug)}'''

    title = f"Recherche fuite eau {nom} {cp} détection non destructive"
    desc = f"Fuite d'eau à {nom} ? Détection non destructive en 24h, sans démolition. Rapport assurance inclus. Devis gratuit sur toute la Gironde (33)."
    canonical = f"https://recherche-fuite-gironde.fr/villes/{slug}/"
    return html_base(title[:60], desc[:160], canonical, body, ld)

# ── Générateur page ville — chemisage ────────────────────────
def page_ville_chemisage(v):
    nom = v['nom']
    cp = v['code_postal']
    slug = v['slug']
    q = v['quartiers']
    quartiers_str = ', '.join(q)

    ld = f'''<script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "Recherche Fuite Gironde",
    "description": "Chemisage de canalisation à {nom} ({cp}). Rénovation sans travaux, sans démolition.",
    "url": "https://recherche-fuite-gironde.fr/villes/{slug}/chemisage/",
    "areaServed": {{
      "@type": "City",
      "name": "{nom}",
      "postalCode": "{cp}",
      "addressCountry": "FR"
    }},
    "serviceType": "Chemisage de canalisation"
  }}
  </script>'''

    mini_form = f'''<div class="ville-cta-card">
  <h3>Chemisage à {nom}</h3>
  <form action="https://formsubmit.co/sites-recherche-fuite@outlook.com" method="POST" class="ville-cta-form">
    <input type="hidden" name="_subject" value="[recherche-fuite-gironde.fr] Demande chemisage à {nom}">
    <input type="hidden" name="_captcha" value="false">
    <input type="hidden" name="ville" value="{nom}">
    <input type="hidden" name="service" value="Chemisage">
    <input type="hidden" name="site_source" value="recherche-fuite-gironde.fr/villes/{slug}/chemisage/">
    <div class="form-group" style="margin-bottom:.75rem;">
      <label class="form-label" for="nom-mini">Nom et prénom</label>
      <input class="form-input" type="text" id="nom-mini" name="nom" placeholder="Nom et prénom" required>
    </div>
    <div class="form-group" style="margin-bottom:.75rem;">
      <label class="form-label" for="tel-mini">Téléphone</label>
      <input class="form-input" type="tel" id="tel-mini" name="telephone" placeholder="06 XX XX XX XX" required>
    </div>
    <div class="form-group" style="margin-bottom:.75rem;">
      <label class="form-label" for="email-mini">Email</label>
      <input class="form-input" type="email" id="email-mini" name="email" placeholder="votre@email.fr" required>
    </div>
    <div class="form-group" style="margin-bottom:.75rem;">
      <label class="form-label" for="probleme-mini">Type de problème</label>
      <select class="form-input form-select" id="probleme-mini" name="probleme" required>
        <option value="">Choisir</option>
        <option value="Fuite visible">Fuite visible (tache, humidité)</option>
        <option value="Compteur anormal">Compteur d'eau anormal</option>
        <option value="Fuite sous dalle">Suspicion de fuite sous dalle</option>
        <option value="Fuite enterrée">Fuite canalisation enterrée</option>
        <option value="Chemisage">Chemisage de canalisation</option>
        <option value="Rapport assurance">Rapport pour assurance</option>
        <option value="Autre">Autre</option>
      </select>
    </div>
    <div class="form-group" style="margin-bottom:.75rem;">
      <label class="form-label" for="msg-mini">Votre situation</label>
      <textarea class="form-input form-textarea" id="msg-mini" name="message" placeholder="Décrivez votre canalisation..." style="min-height:80px;" required></textarea>
    </div>
    <button type="submit" class="btn btn-green btn-full">Demander un devis chemisage</button>
  </form>
</div>'''

    body = f'''
<section class="hero-mini">
  <div class="container">
    <nav class="breadcrumb">
      <a href="/">Accueil</a>
      <span>&rsaquo;</span>
      <a href="/chemisage-canalisation/">Chemisage</a>
      <span>&rsaquo;</span>
      <span>{nom}</span>
    </nav>
    <span class="badge badge-gold" style="margin-bottom:1rem;">Gironde &bull; {cp}</span>
    <h1>Chemisage de canalisation à {nom} ({cp})</h1>
    <p class="hero-mini-lead">Rénovation de canalisations sans travaux à {nom}. Une technique non destructive qui remet en état vos canalisations sans ouvrir les murs ni les sols.</p>
    <a href="/devis/" class="btn btn-gold" style="margin-top:1.5rem;display:inline-block;">Demander un devis gratuit</a>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="ville-layout">
      <div class="ville-content">
        <h2 class="section-title">Le chemisage de canalisation à {nom}</h2>
        <p>Le chemisage est la solution de rénovation de canalisation la plus efficace lorsque les tuyaux sont dégradés, fissuré ou poreux. À {nom}, notamment dans les quartiers de {quartiers_str}, les réseaux anciens sont souvent concernés.</p>
        <p>Le principe : un manchon en résine époxy est inséré dans la canalisation existante puis gonflé et durci sur place. Le tuyau est ainsi gainé de l'intérieur, sans qu'il soit nécessaire de l'extraire. Résultat : une canalisation neuve dans l'ancienne, sans démolition.</p>

        <h2 class="section-title" style="margin-top:2.5rem;">Avantages du chemisage à {nom}</h2>
        <div class="grid-3" style="margin-top:1.5rem;">
          <div class="arg-card">
            <div class="arg-card-icon"><img src="/assets/icons/tick-circle.svg" alt=""></div>
            <h3>Sans démolition</h3>
            <p>Aucun mur ni sol n'est ouvert. Idéal pour les appartements et maisons à {nom}.</p>
          </div>
          <div class="arg-card">
            <div class="arg-card-icon"><img src="/assets/icons/clock.svg" alt=""></div>
            <h3>Intervention rapide</h3>
            <p>Une canalisation chemisée en une journée, sans nuisances prolongées pour les occupants.</p>
          </div>
          <div class="arg-card">
            <div class="arg-card-icon"><img src="/assets/icons/refresh.svg" alt=""></div>
            <h3>Durabilité garantie</h3>
            <p>Le revêtement en résine époxy présente une durée de vie de plusieurs décennies.</p>
          </div>
        </div>

        <h2 class="section-title" style="margin-top:2.5rem;">Quand recourir au chemisage à {nom} ?</h2>
        <p>Le chemisage est recommandé dans plusieurs situations :</p>
        <ul style="margin:1rem 0 1rem 1.5rem;list-style:disc;display:flex;flex-direction:column;gap:.5rem;">
          <li>Canalisation fissurée ou corrodée en fond de cavité inaccessible</li>
          <li>Fuite récurrente malgré des réparations locales</li>
          <li>Réseau enterré dans un jardin ou sous une allée à {nom}</li>
          <li>Canalisation d'immeuble ou copropriété à rénover sans travaux lourds</li>
        </ul>
        <p>Si votre fuite n'a pas encore été localisée, nous proposons d'abord une <a href="/villes/{slug}/" style="color:var(--green);text-decoration:underline;">recherche de fuite à {nom}</a> avant d'engager le chemisage.</p>

        <div class="temoignage-card" style="margin-top:2rem;">
          <div class="temoignage-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
          <p class="temoignage-text">« Chemisage réalisé sur notre réseau enterré à {nom}. Aucune tranchée, aucun dégât dans le jardin. La canalisation est comme neuve. Je recommande vivement cette solution. »</p>
          <div class="temoignage-author">Propriétaire à {nom} ({cp})</div>
        </div>
      </div>

      <div class="ville-sidebar">
        {mini_form}
      </div>
    </div>
  </div>
</section>

{form_section(nom)}
{maillage_villes(slug)}'''

    title = f"Chemisage canalisation {nom} {cp} rénovation sans travaux"
    desc = f"Chemisage de canalisation à {nom} ({cp}). Rénovation sans démolition, sans tranchée. Devis gratuit, intervention rapide en Gironde (33)."
    canonical = f"https://recherche-fuite-gironde.fr/villes/{slug}/chemisage/"
    return html_base(title[:60], desc[:160], canonical, body, ld)

# ── Page service détection ─────────────────────────────────────
def page_detection():
    body = f'''
<section class="hero-mini">
  <div class="container">
    <nav class="breadcrumb">
      <a href="/">Accueil</a>
      <span>&rsaquo;</span>
      <span>Détection de fuite</span>
    </nav>
    <h1>Détection de fuite non destructive en Gironde</h1>
    <p class="hero-mini-lead">Nos techniciens localisent précisément toute fuite d'eau en Gironde, sans casse ni démolition, grâce aux techniques acoustiques, thermographiques et endoscopiques les plus récentes.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header-center">
      <span class="section-eyebrow">Nos méthodes</span>
      <h2 class="section-title">Des techniques adaptées à chaque configuration</h2>
      <p class="section-lead">Chaque situation de fuite est différente. Nous combinons plusieurs technologies pour garantir une localisation précise sans travaux préalables.</p>
    </div>
    <div class="grid-2">
      <div class="service-card">
        <div class="service-card-icon"><img src="/assets/icons/search.svg" alt="Corrélation acoustique"></div>
        <h3>Corrélation acoustique</h3>
        <p>Des capteurs placés aux deux extrémités d'une canalisation permettent de calculer la position exacte de la fuite par analyse du bruit qu'elle produit. Précision à quelques centimètres.</p>
        <ul class="service-card-list">
          <li>Canalisations enterrées et encastrées</li>
          <li>Réseaux d'eau froide et chaude</li>
          <li>Sans destruction de surface</li>
        </ul>
      </div>
      <div class="service-card">
        <div class="service-card-icon"><img src="/assets/icons/zoom-in.svg" alt="Caméra endoscopique"></div>
        <h3>Caméra endoscopique</h3>
        <p>Une mini-caméra est introduite dans la canalisation pour inspecter visuellement l'état du réseau et identifier la zone endommagée ou les infiltrations.</p>
        <ul class="service-card-list">
          <li>Visualisation directe de l'intérieur</li>
          <li>Détection des fissurations et dépôts</li>
          <li>Rapport photo/vidéo fourni</li>
        </ul>
      </div>
      <div class="service-card">
        <div class="service-card-icon"><img src="/assets/icons/alert-circle.svg" alt="Gaz traceur"></div>
        <h3>Gaz traceur</h3>
        <p>Un mélange d'azote et d'hydrogène inoffensif est injecté dans la canalisation. Un détecteur de surface repère précisément l'endroit où le gaz s'échappe.</p>
        <ul class="service-card-list">
          <li>Fuites sur réseaux pressurisés</li>
          <li>Précision millimétrique</li>
          <li>Méthode rapide et non invasive</li>
        </ul>
      </div>
      <div class="service-card">
        <div class="service-card-icon"><img src="/assets/icons/calendar.svg" alt="Thermographie infrarouge"></div>
        <h3>Thermographie infrarouge</h3>
        <p>La caméra thermique détecte les variations de température causées par l'humidité et les infiltrations à travers les murs, dalles et plafonds.</p>
        <ul class="service-card-list">
          <li>Fuites derrière les revêtements</li>
          <li>Sans contact avec les surfaces</li>
          <li>Idéal pour planchers chauffants</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <div class="section-header-center">
      <span class="section-eyebrow">Déroulement</span>
      <h2 class="section-title">Comment se déroule une intervention</h2>
    </div>
    <div class="grid-3">
      <div class="arg-card">
        <div class="arg-card-icon"><img src="/assets/icons/chat-bubble.svg" alt=""></div>
        <h3>1. Prise de contact</h3>
        <p>Vous décrivez votre situation via le formulaire ou par contact direct. Nous évaluons le type d'intervention nécessaire et planifions le déplacement.</p>
      </div>
      <div class="arg-card">
        <div class="arg-card-icon"><img src="/assets/icons/search.svg" alt=""></div>
        <h3>2. Diagnostic sur site</h3>
        <p>Le technicien effectue un premier diagnostic visuel, puis déploie les équipements adaptés à votre configuration (acoustique, thermique, endoscopique).</p>
      </div>
      <div class="arg-card">
        <div class="arg-card-icon"><img src="/assets/icons/tick-badge.svg" alt=""></div>
        <h3>3. Rapport et préconisations</h3>
        <p>Un rapport écrit détaillant la localisation exacte de la fuite, les photos et les préconisations de réparation vous est remis à l'issue de l'intervention.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="img-split">
      <div class="img-split-img">
        <img src="/assets/fuite-sous-dalle.webp" alt="Fuite d\'eau sous dalle détectée en Gironde" loading="lazy" width="700" height="467">
      </div>
      <div class="img-split-content">
        <span class="section-eyebrow">Notre engagement</span>
        <h2>Localisation précise avant toute ouverture</h2>
        <p>Nous ne perçons pas, ne cassons pas, n\'ouvrons rien avant d\'avoir localisé la fuite avec certitude. Cette règle protège vos revêtements et réduit le coût de remise en état après intervention.</p>
        <a href="/devis/" class="btn btn-green">Demander un devis</a>
      </div>
    </div>
  </div>
</section>

{villes_detection_section()}
{form_section()}'''

    ld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Service",
    "name": "Détection de fuite non destructive",
    "provider": {"@type": "LocalBusiness", "name": "Recherche Fuite Gironde"},
    "areaServed": "Gironde",
    "serviceType": "Détection de fuite d'eau"
  }
  </script>'''
    return html_base(
        "Détection fuite non destructive Gironde 33 intervention rapide",
        "Détection de fuite non destructive en Gironde (33). Corrélation acoustique, caméra endoscopique, gaz traceur. Rapport assurance. Devis gratuit.",
        "https://recherche-fuite-gironde.fr/detection-fuite/",
        body, ld
    )

# ── Page service chemisage ─────────────────────────────────────
def page_chemisage_service():
    body = f'''
<section class="hero-mini">
  <div class="container">
    <nav class="breadcrumb">
      <a href="/">Accueil</a>
      <span>&rsaquo;</span>
      <span>Chemisage de canalisation</span>
    </nav>
    <h1>Chemisage de canalisation en Gironde</h1>
    <p class="hero-mini-lead">Rénovez vos canalisations sans travaux de démolition. Le chemisage est la solution durable pour remettre en état un réseau dégradé, fissuré ou poreux en Gironde (33).</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header-center">
      <span class="section-eyebrow">La technique</span>
      <h2 class="section-title">Le chemisage : comment ça fonctionne ?</h2>
      <p class="section-lead">Le chemisage consiste à insérer un manchon en résine époxy à l'intérieur de la canalisation existante. Ce manchon est ensuite gonflé et durci sur place, créant un nouveau tuyau dans l'ancien.</p>
    </div>
    <div class="grid-3">
      <div class="arg-card">
        <div class="arg-card-icon"><img src="/assets/icons/tick-circle.svg" alt=""></div>
        <h3>Sans démolition</h3>
        <p>Aucun mur, carrelage ou sol n'est touché. Le manchon est introduit par un accès existant (regard, siphon, orifice de visite).</p>
      </div>
      <div class="arg-card">
        <div class="arg-card-icon"><img src="/assets/icons/refresh.svg" alt=""></div>
        <h3>Longévité prouvée</h3>
        <p>La résine époxy présente une durée de vie supérieure à 50 ans dans des conditions normales d'utilisation.</p>
      </div>
      <div class="arg-card">
        <div class="arg-card-icon"><img src="/assets/icons/clock.svg" alt=""></div>
        <h3>Intervention rapide</h3>
        <p>Un réseau de 10 à 20 mètres peut être chemisé en une journée, sans nuisances prolongées pour les occupants.</p>
      </div>
      <div class="arg-card">
        <div class="arg-card-icon"><img src="/assets/icons/home.svg" alt=""></div>
        <h3>Tous types de bâtiments</h3>
        <p>Maisons individuelles, appartements, copropriétés, locaux commerciaux en Gironde - le chemisage s'adapte à toutes les configurations.</p>
      </div>
      <div class="arg-card">
        <div class="arg-card-icon"><img src="/assets/icons/map-pin.svg" alt=""></div>
        <h3>Réseaux enterrés</h3>
        <p>Idéal pour les canalisations sous jardin ou voirie à rénover sans ouvrir le sol sur de longues distances.</p>
      </div>
      <div class="arg-card">
        <div class="arg-card-icon"><img src="/assets/icons/tick-badge.svg" alt=""></div>
        <h3>Rapport et garantie</h3>
        <p>Une inspection caméra avant et après intervention, un rapport complet et une garantie sur la durabilité du revêtement.</p>
      </div>
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <div class="img-split reverse">
      <div class="img-split-img">
        <img src="/assets/fuite-canalisation-enterree.webp" alt="Réparation canalisation enterrée Gironde" loading="lazy" width="700" height="467">
      </div>
      <div class="img-split-content">
        <span class="section-eyebrow">Cas concret</span>
        <h2>Le chemisage sur canalisation enterrée : aucune tranchée</h2>
        <p>Qu\'il s\'agisse d\'une canalisation sous jardin, sous dalle ou en sous-sol, le chemisage s\'effectue depuis un accès existant. Le liner en résine est introduit, gonflé et durci sur place en quelques heures.</p>
        <a href="/devis/" class="btn btn-green">Obtenir un devis</a>
      </div>
    </div>
  </div>
</section>

{villes_chemisage_section()}
{form_section()}'''

    ld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Service",
    "name": "Chemisage de canalisation",
    "provider": {"@type": "LocalBusiness", "name": "Recherche Fuite Gironde"},
    "areaServed": "Gironde",
    "serviceType": "Chemisage de canalisation"
  }
  </script>'''
    return html_base(
        "Chemisage canalisation Gironde 33 rénovation sans travaux",
        "Chemisage de canalisation en Gironde (33). Rénovation sans démolition, sans tranchée. Résine époxy longue durée. Devis gratuit sur toute la Gironde.",
        "https://recherche-fuite-gironde.fr/chemisage-canalisation/",
        body, ld
    )

# ── Page contact ───────────────────────────────────────────────
def page_contact():
    body = '''
<section class="hero-mini">
  <div class="container">
    <nav class="breadcrumb">
      <a href="/">Accueil</a>
      <span>&rsaquo;</span>
      <span>Contact</span>
    </nav>
    <h1>Contactez-nous</h1>
    <p class="hero-mini-lead">Une question sur nos services ? Un renseignement avant de faire une demande ? Écrivez-nous, nous vous répondons sous 24h ouvrées.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:720px;">
    <div class="section-header-center" style="margin-bottom:2.5rem;">
      <span class="section-eyebrow">Formulaire de contact</span>
      <h2 class="section-title">Envoyez-nous un message</h2>
      <p class="section-lead" style="margin-bottom:0;">Pour une demande de devis, utilisez plutôt notre <a href="/devis/" style="color:var(--green);text-decoration:underline;">page devis dédiée</a>.</p>
    </div>

    <form action="https://formsubmit.co/sites-recherche-fuite@outlook.com" method="POST" style="display:flex;flex-direction:column;gap:1.25rem;">
      <input type="hidden" name="_subject" value="[recherche-fuite-gironde.fr] Message de contact">
      <input type="hidden" name="_captcha" value="false">
      <input type="hidden" name="_template" value="table">
      <input type="hidden" name="_next" id="next-url" value="/merci/">
        <script>document.getElementById("next-url").value=window.location.origin+"/merci/";</script>
      <input type="hidden" name="site_source" value="recherche-fuite-gironde.fr/contact/">

      <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
        <div class="form-group">
          <label style="display:block;font-size:.85rem;font-weight:600;color:var(--muted);margin-bottom:.35rem;text-transform:uppercase;letter-spacing:.05em;" for="prenom">Prénom</label>
          <input style="width:100%;font-family:var(--f-body);font-size:.9375rem;color:var(--text);background:var(--white);border:1px solid var(--border);border-radius:var(--r-md);padding:.8rem 1rem;outline:none;transition:border-color .15s,box-shadow .15s;" type="text" id="prenom" name="prenom" placeholder="Votre prénom" required
            onfocus="this.style.borderColor='var(--green)';this.style.boxShadow='0 0 0 3px rgba(30,122,87,.15)'"
            onblur="this.style.borderColor='var(--border)';this.style.boxShadow='none'">
        </div>
        <div class="form-group">
          <label style="display:block;font-size:.85rem;font-weight:600;color:var(--muted);margin-bottom:.35rem;text-transform:uppercase;letter-spacing:.05em;" for="nom">Nom</label>
          <input style="width:100%;font-family:var(--f-body);font-size:.9375rem;color:var(--text);background:var(--white);border:1px solid var(--border);border-radius:var(--r-md);padding:.8rem 1rem;outline:none;transition:border-color .15s,box-shadow .15s;" type="text" id="nom" name="nom" placeholder="Votre nom" required
            onfocus="this.style.borderColor='var(--green)';this.style.boxShadow='0 0 0 3px rgba(30,122,87,.15)'"
            onblur="this.style.borderColor='var(--border)';this.style.boxShadow='none'">
        </div>
      </div>

      <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
        <div class="form-group">
          <label style="display:block;font-size:.85rem;font-weight:600;color:var(--muted);margin-bottom:.35rem;text-transform:uppercase;letter-spacing:.05em;" for="telephone">Téléphone</label>
          <input style="width:100%;font-family:var(--f-body);font-size:.9375rem;color:var(--text);background:var(--white);border:1px solid var(--border);border-radius:var(--r-md);padding:.8rem 1rem;outline:none;transition:border-color .15s,box-shadow .15s;" type="tel" id="telephone" name="telephone" placeholder="06 XX XX XX XX"
            onfocus="this.style.borderColor='var(--green)';this.style.boxShadow='0 0 0 3px rgba(30,122,87,.15)'"
            onblur="this.style.borderColor='var(--border)';this.style.boxShadow='none'">
        </div>
        <div class="form-group">
          <label style="display:block;font-size:.85rem;font-weight:600;color:var(--muted);margin-bottom:.35rem;text-transform:uppercase;letter-spacing:.05em;" for="email">Email</label>
          <input style="width:100%;font-family:var(--f-body);font-size:.9375rem;color:var(--text);background:var(--white);border:1px solid var(--border);border-radius:var(--r-md);padding:.8rem 1rem;outline:none;transition:border-color .15s,box-shadow .15s;" type="email" id="email" name="email" placeholder="votre@email.fr" required
            onfocus="this.style.borderColor='var(--green)';this.style.boxShadow='0 0 0 3px rgba(30,122,87,.15)'"
            onblur="this.style.borderColor='var(--border)';this.style.boxShadow='none'">
        </div>
      </div>

      <div class="form-group">
        <label style="display:block;font-size:.85rem;font-weight:600;color:var(--muted);margin-bottom:.35rem;text-transform:uppercase;letter-spacing:.05em;" for="sujet">Sujet</label>
        <input style="width:100%;font-family:var(--f-body);font-size:.9375rem;color:var(--text);background:var(--white);border:1px solid var(--border);border-radius:var(--r-md);padding:.8rem 1rem;outline:none;transition:border-color .15s,box-shadow .15s;" type="text" id="sujet" name="sujet" placeholder="L'objet de votre message" required
          onfocus="this.style.borderColor='var(--green)';this.style.boxShadow='0 0 0 3px rgba(30,122,87,.15)'"
          onblur="this.style.borderColor='var(--border)';this.style.boxShadow='none'">
      </div>

      <div class="form-group">
        <label style="display:block;font-size:.85rem;font-weight:600;color:var(--muted);margin-bottom:.35rem;text-transform:uppercase;letter-spacing:.05em;" for="message">Message</label>
        <textarea style="width:100%;font-family:var(--f-body);font-size:.9375rem;color:var(--text);background:var(--white);border:1px solid var(--border);border-radius:var(--r-md);padding:.8rem 1rem;outline:none;transition:border-color .15s,box-shadow .15s;resize:vertical;min-height:140px;" id="message" name="message" placeholder="Votre message..." required
          onfocus="this.style.borderColor='var(--green)';this.style.boxShadow='0 0 0 3px rgba(30,122,87,.15)'"
          onblur="this.style.borderColor='var(--border)';this.style.boxShadow='none'"></textarea>
      </div>

      <button type="submit" class="btn btn-green btn-full">Envoyer mon message</button>
      <p style="font-size:.8rem;color:var(--muted);text-align:center;">Aucune donnée personnelle n'est transmise à des tiers.</p>
    </form>
  </div>
</section>'''
    return html_base(
        "Contact - Recherche Fuite Gironde",
        "Contactez Recherche Fuite Gironde. Une question sur la détection de fuite ou le chemisage en Gironde (33) ? Nous vous répondons sous 24h.",
        "https://recherche-fuite-gironde.fr/contact/",
        body
    )

# ── Page mentions légales ──────────────────────────────────────
def page_mentions():
    body = '''
<section class="hero-mini">
  <div class="container">
    <nav class="breadcrumb">
      <a href="/">Accueil</a>
      <span>&rsaquo;</span>
      <span>Mentions légales</span>
    </nav>
    <h1>Mentions légales</h1>
  </div>
</section>
<section class="section">
  <div class="container" style="max-width:780px;">
    <div class="article-body">
      <h2>Éditeur du site</h2>
      <p>Le site recherche-fuite-gironde.fr est un site d'information et de mise en relation pour des services de recherche de fuites d'eau en Gironde (département 33, France).</p>
      <h2>Hébergement</h2>
      <p>Le site est hébergé par Vercel Inc., 340 Pine Street, Suite 900, San Francisco, CA 94104, États-Unis.</p>
      <h2>Propriété intellectuelle</h2>
      <p>L'ensemble du contenu de ce site (textes, visuels, structure) est protégé par le droit d'auteur. Toute reproduction sans autorisation est interdite.</p>
      <h2>Données personnelles</h2>
      <p>Les données collectées via le formulaire de contact (nom, ville, message) sont utilisées uniquement pour répondre à votre demande. Elles ne sont jamais transmises à des tiers à des fins commerciales. Conformément au RGPD, vous disposez d'un droit d'accès, de rectification et de suppression de vos données.</p>
      <h2>Cookies</h2>
      <p>Ce site n'utilise pas de cookies de tracking ou de profilage. Aucun outil d'analyse comportementale n'est actif.</p>
      <h2>Responsabilité</h2>
      <p>Les informations présentées sur ce site ont un caractère indicatif. L'éditeur ne saurait être tenu responsable des dommages directs ou indirects résultant de l'utilisation de ces informations.</p>
    </div>
  </div>
</section>'''
    return html_base(
        "Mentions légales - Recherche Fuite Gironde",
        "Mentions légales du site recherche-fuite-gironde.fr. Informations éditeur, données personnelles, RGPD.",
        "https://recherche-fuite-gironde.fr/mentions-legales/",
        body
    )

# ── Plan du site ───────────────────────────────────────────────
def page_plan():
    villes_detection = '\n'.join([
        f'<li><a href="/villes/{v["slug"]}/">Recherche de fuite à {v["nom"]} ({v["code_postal"]})</a></li>'
        for v in VILLES
    ])
    villes_chemisage = '\n'.join([
        f'<li><a href="/villes/{v["slug"]}/chemisage/">Chemisage de canalisation à {v["nom"]} ({v["code_postal"]})</a></li>'
        for v in VILLES
    ])
    body = f'''
<section class="hero-mini">
  <div class="container">
    <nav class="breadcrumb">
      <a href="/">Accueil</a>
      <span>&rsaquo;</span>
      <span>Plan du site</span>
    </nav>
    <h1>Plan du site</h1>
  </div>
</section>
<section class="section">
  <div class="container" style="max-width:900px;">
    <div class="article-body">
      <h2>Pages principales</h2>
      <ul>
        <li><a href="/">Accueil - Recherche Fuite Gironde</a></li>
        <li><a href="/detection-fuite/">Détection de fuite non destructive en Gironde</a></li>
        <li><a href="/chemisage-canalisation/">Chemisage de canalisation en Gironde</a></li>
        <li><a href="/devis/">Devis gratuit</a></li>
        <li><a href="/contact/">Contact</a></li>
        <li><a href="/mentions-legales/">Mentions légales</a></li>
      </ul>
      <h2>Guide pratique fuite d'eau</h2>
      <ul>
        <li><a href="/guide/">Sommaire du guide</a></li>
        <li><a href="/guide/comment-detecter-une-fuite/">Comment détecter une fuite chez soi</a></li>
        <li><a href="/guide/causes-fuites-eau/">Les causes de fuites d'eau les plus fréquentes</a></li>
        <li><a href="/guide/fuite-sous-dalle/">Fuite sous dalle : diagnostic et solutions</a></li>
        <li><a href="/guide/fuite-canalisation-enterree/">Fuite sur canalisation enterrée</a></li>
        <li><a href="/guide/chemisage-explication/">Le chemisage de canalisation expliqué</a></li>
        <li><a href="/guide/cout-recherche-fuite/">Quel est le coût d'une recherche de fuite ?</a></li>
        <li><a href="/guide/assurance-fuite-eau/">Fuite d'eau et assurance habitation</a></li>
        <li><a href="/guide/urgence-fuite-eau/">Que faire en cas d'urgence fuite d'eau ?</a></li>
        <li><a href="/guide/faq/">FAQ - Questions fréquentes sur les fuites d'eau</a></li>
      </ul>
      <h2>Recherche de fuite par ville (30 communes)</h2>
      <ul>
        {villes_detection}
      </ul>
      <h2>Chemisage de canalisation par ville (30 communes)</h2>
      <ul>
        {villes_chemisage}
      </ul>
    </div>
  </div>
</section>'''
    return html_base(
        "Plan du site - Recherche Fuite Gironde",
        "Plan du site recherche-fuite-gironde.fr. Toutes les pages : services, villes de Gironde, guide pratique.",
        "https://recherche-fuite-gironde.fr/plan-du-site/",
        body
    )

# ── Pages du guide ─────────────────────────────────────────────
GUIDE_PAGES = [
    {
        "slug": "comment-detecter-une-fuite",
        "title": "Comment détecter une fuite chez soi",
        "title_seo": "Comment détecter une fuite d'eau chez soi premiers signes",
        "desc": "Les signes qui indiquent une fuite d'eau chez vous et les premières vérifications à faire avant d'appeler un technicien en Gironde.",
        "contenu": """<p>Une fuite d'eau peut rester invisible pendant des semaines, voire des mois, avant de se manifester clairement. Savoir la détecter tôt permet d'éviter des dégâts importants et des factures d'eau en hausse.</p>
<h2>Les signes qui doivent vous alerter</h2>
<p>Plusieurs indices peuvent révéler la présence d'une fuite dans votre logement :</p>
<ul>
<li>Une facture d'eau anormalement élevée sans explication</li>
<li>Un compteur d'eau qui tourne même quand tout est fermé</li>
<li>Des taches d'humidité sur les murs, plafonds ou sols</li>
<li>Un sol anormalement chaud (signe de fuite sur plancher chauffant)</li>
<li>Des moisissures récurrentes sans source d'humidité apparente</li>
<li>Un bruit d'écoulement persistant dans les cloisons</li>
</ul>
<h2>Le test du compteur</h2>
<p>La première vérification à réaliser est simple : coupez tous les robinets de votre logement et notez l'index de votre compteur d'eau. Revenez une heure plus tard sans avoir utilisé d'eau. Si l'index a bougé, il y a bien une fuite quelque part dans votre réseau.</p>
<h2>Localiser la zone suspecte</h2>
<p>Une fois la fuite confirmée, tentez de délimiter sa zone :</p>
<ul>
<li>Fermez la vanne d'arrêt de votre chauffe-eau : si le compteur s'arrête, la fuite est sur le circuit eau chaude</li>
<li>Inspectez visuellement les joints sous les éviers, douches et WC</li>
<li>Vérifiez les raccords apparents sous les lavabos et derrière les appareils électroménagers</li>
</ul>
<h2>Quand faire appel à un professionnel ?</h2>
<p>Si le test du compteur révèle une fuite mais que vous ne trouvez pas de source visible, la fuite est probablement encastrée ou enterrée. Dans ce cas, un technicien spécialisé en détection non destructive est nécessaire. En Gironde, nous intervenons sous 24h pour localiser précisément la fuite sans démolition.</p>"""
    },
    {
        "slug": "causes-fuites-eau",
        "title": "Les causes de fuites d'eau les plus fréquentes",
        "title_seo": "Causes fuites eau maison canalisation défaillance réseau",
        "desc": "Pourquoi une canalisation fuit-elle ? Les causes les plus fréquentes de fuites d'eau dans les maisons et appartements en Gironde.",
        "contenu": """<p>Une fuite d'eau n'arrive jamais par hasard. Comprendre les causes les plus fréquentes permet d'anticiper les risques et d'adapter la solution de réparation.</p>
<h2>La corrosion des canalisations</h2>
<p>Les tuyaux en acier galvanisé ou en cuivre vieillissent et se corrodent de l'intérieur. En Gironde, la qualité de l'eau (pH, calcaire) joue un rôle important dans l'accélération de ce phénomène. Les premières fissurations apparaissent souvent aux points de soudure ou de raccord.</p>
<h2>Les raccords défaillants</h2>
<p>Les joints et raccords de plomberie se dégradent avec le temps et les variations de température. Un raccord mal serré ou dont le joint a vieilli peut générer une fuite lente mais continue, souvent difficile à détecter car localisée dans une paroi ou sous une dalle.</p>
<h2>Les mouvements de terrain</h2>
<p>En Gironde, les sols argileux sont sensibles aux variations d'humidité. En période de sécheresse puis de pluie, les mouvements de retrait-gonflement des argiles peuvent fissurer les canalisations enterrées ou sous dalle.</p>
<h2>Le calcaire et les dépôts</h2>
<p>L'entartrage progressif des canalisations augmente la pression interne et favorise l'apparition de micro-fissurations, notamment sur les coudes et les points de raccord.</p>
<h2>Les travaux de construction ou rénovation</h2>
<p>Percer un mur sans connaitre le tracé des canalisations est l'une des causes les plus fréquentes de fuites accidentelles. De même, des travaux mal réalisés sur le réseau peuvent générer des micro-fuites qui ne se manifestent que des mois plus tard.</p>
<h2>La solution</h2>
<p>Quelle que soit la cause, nos techniciens en Gironde identifient rapidement l'origine de la fuite et vous proposent la solution adaptée : réparation ponctuelle ou <a href="/chemisage-canalisation/" style="color:var(--green);text-decoration:underline;">chemisage de la canalisation</a> si le réseau est trop dégradé.</p>"""
    },
    {
        "slug": "fuite-sous-dalle",
        "title": "Fuite sous dalle : diagnostic et solutions",
        "title_seo": "Fuite sous dalle béton carrelage détection réparation Gironde",
        "desc": "Comment détecter et traiter une fuite sous dalle en Gironde. Techniques non destructives pour localiser et réparer sans casse.",
        "contenu": """<p>La fuite sous dalle est l'une des plus redoutées car elle est invisible, silencieuse et peut causer des dégâts considérables avant d'être détectée. En Gironde, c'est l'une des interventions les plus fréquentes dans notre secteur.</p>
<h2>Comment se manifeste une fuite sous dalle ?</h2>
<ul>
<li>Sol anormalement chaud par endroits (si réseau eau chaude ou plancher chauffant)</li>
<li>Humidité remontante sous les revêtements de sol</li>
<li>Carrelage qui se décolle ou se fissure</li>
<li>Compteur d'eau qui tourne en permanence</li>
<li>Facture d'eau en forte hausse</li>
</ul>
<h2>La détection sans casse</h2>
<p>Pour localiser une fuite sous dalle, nos techniciens utilisent plusieurs méthodes complémentaires :</p>
<p><strong>La corrélation acoustique</strong> permet de positionner la fuite à quelques centimètres près en analysant le bruit produit par l'écoulement. <strong>La thermographie infrarouge</strong> révèle les zones de température anormale liées à l'humidité. <strong>Le gaz traceur</strong> est injecté dans la canalisation et détecté en surface avec précision.</p>
<h2>La réparation</h2>
<p>Une fois la fuite localisée précisément, l'ouverture dans la dalle est réduite au minimum. Dans certains cas, le <a href="/chemisage-canalisation/" style="color:var(--green);text-decoration:underline;">chemisage de la canalisation</a> permet d'éviter totalement l'ouverture du sol.</p>
<h2>Prise en charge assurance</h2>
<p>Les fuites sous dalle sont généralement couvertes par votre assurance habitation dans le cadre d'un dégât des eaux. Le rapport de recherche de fuite que nous vous remettons est le document indispensable pour constituer votre dossier.</p>"""
    },
    {
        "slug": "fuite-canalisation-enterree",
        "title": "Fuite sur canalisation enterrée",
        "title_seo": "Fuite canalisation enterrée jardin voirie détection Gironde",
        "desc": "Comment détecter une fuite sur une canalisation enterrée en Gironde. Méthodes acoustiques et traceur gaz pour localiser sans creuser.",
        "contenu": """<p>Une fuite sur canalisation enterrée est particulièrement difficile à détecter car elle peut courir sur des dizaines de mètres sous un jardin ou une allée avant de se manifester en surface - parfois jamais.</p>
<h2>Les signes d'une fuite enterrée</h2>
<ul>
<li>Zone du jardin anormalement verte ou humide sans pluie récente</li>
<li>Affaissement ou gonflement du sol</li>
<li>Compteur d'eau actif vanne fermée</li>
<li>Pression d'eau réduite dans le logement</li>
</ul>
<h2>La technique de détection acoustique</h2>
<p>La corrélation acoustique est la méthode la plus efficace pour les canalisations enterrées. Deux capteurs sont posés aux extrémités du réseau. L'analyse de la différence de propagation du bruit permet de calculer la position exacte de la fuite à quelques centimètres près - sans aucun creusement préalable.</p>
<h2>Le gaz traceur sur réseaux enterrés</h2>
<p>Pour les fuites de faible débit difficiles à capter acoustiquement, le gaz traceur (mélange azote-hydrogène) est injecté dans la canalisation. Un détecteur de surface très sensible localise l'échappement avec précision, même sous 1 mètre de terre.</p>
<h2>Réparation ou chemisage ?</h2>
<p>Selon l'état général de la canalisation et la localisation de la fuite, deux solutions s'offrent à vous :</p>
<ul>
<li>Réparation ponctuelle : ouverture chirurgicale au point de fuite uniquement</li>
<li><a href="/chemisage-canalisation/" style="color:var(--green);text-decoration:underline;">Chemisage</a> : rénovation de l'ensemble du réseau enterré sans tranchée</li>
</ul>"""
    },
    {
        "slug": "chemisage-explication",
        "title": "Le chemisage de canalisation expliqué",
        "title_seo": "Chemisage canalisation résine epoxy technique explication",
        "desc": "Comment fonctionne le chemisage de canalisation ? La technique, les matériaux et les étapes d'une intervention en Gironde expliqués simplement.",
        "contenu": """<p>Le chemisage de canalisation est une technique de rénovation qui consiste à créer un nouveau tuyau à l'intérieur de l'ancien, sans démolition. C'est la solution idéale quand la canalisation est trop dégradée pour une réparation ponctuelle.</p>
<h2>Le principe du chemisage</h2>
<p>Un manchon souple imprégné de résine époxy est introduit dans la canalisation existante par un accès naturel (regard, siphon, ouverture de visite). Une fois en position, il est gonflé à l'aide d'air comprimé et maintenu appuyé contre les parois pendant que la résine durcit. Quelques heures plus tard, la résine est polymérisée et forme un nouveau tuyau lisse et étanche à l'intérieur de l'ancien.</p>
<h2>Les avantages du chemisage</h2>
<ul>
<li>Aucun mur ni sol à ouvrir</li>
<li>Pas de tranchée pour les canalisations enterrées</li>
<li>Durée de vie supérieure à 50 ans</li>
<li>Résistance chimique et mécanique excellente</li>
<li>Restauration totale de l'étanchéité</li>
<li>Applicable sur fonte, PVC, grès, cuivre</li>
</ul>
<h2>Le déroulement d'une intervention</h2>
<p><strong>Étape 1 : inspection caméra</strong> - L'intérieur de la canalisation est filmé pour évaluer son état et choisir le diamètre de manchon adapté.</p>
<p><strong>Étape 2 : nettoyage</strong> - La canalisation est nettoyée par hydro-curage pour garantir une bonne adhérence de la résine.</p>
<p><strong>Étape 3 : mise en place du manchon</strong> - Le manchon imprégné de résine est inséré et positionné avec précision.</p>
<p><strong>Étape 4 : polymérisation</strong> - La résine durcit (2 à 4 heures selon le diamètre et la longueur).</p>
<p><strong>Étape 5 : inspection finale</strong> - Une caméra vérifie le résultat. Un rapport est remis avec photos avant/après.</p>"""
    },
    {
        "slug": "cout-recherche-fuite",
        "title": "Quel est le coût d'une recherche de fuite ?",
        "title_seo": "Coût prix recherche fuite eau Gironde tarif intervention",
        "desc": "Quel budget prévoir pour une recherche de fuite en Gironde ? Facteurs qui influencent le tarif et prise en charge assurance.",
        "contenu": """<p>Le coût d'une recherche de fuite varie selon plusieurs facteurs. Voici ce qu'il faut savoir pour estimer votre budget et comprendre comment l'assurance peut intervenir.</p>
<h2>Les facteurs qui influencent le tarif</h2>
<p>Il n'existe pas de tarif fixe pour une recherche de fuite car chaque situation est différente. Plusieurs éléments entrent en compte :</p>
<ul>
<li><strong>Le type de réseau</strong> : apparent, encastré, enterré ou sous dalle - l'accessibilité conditionne le temps d'intervention</li>
<li><strong>La technique utilisée</strong> : corrélation acoustique, gaz traceur ou thermographie peuvent être combinées</li>
<li><strong>La complexité de l'installation</strong> : un réseau ancien ou labyrinthique demande plus de temps</li>
<li><strong>La distance</strong> : le déplacement en Gironde est inclus dans nos zones d'intervention</li>
</ul>
<h2>La prise en charge par l'assurance</h2>
<p>Dans la grande majorité des cas, les frais de recherche de fuite non destructive sont pris en charge par votre assurance habitation dans le cadre d'un dégât des eaux. Pour cela, il est impératif de :</p>
<ul>
<li>Déclarer le sinistre à votre assureur dès la découverte de la fuite</li>
<li>Obtenir un rapport officiel de recherche de fuite (ce que nous fournissons systématiquement)</li>
<li>Transmettre ce rapport à votre assureur pour justifier les travaux de réparation</li>
</ul>
<h2>Le devis gratuit</h2>
<p>Nous vous proposons un devis gratuit avant toute intervention. Après un premier échange sur votre situation (type de fuite, configuration du logement, localisation en Gironde), nous pouvons vous donner une estimation précise et sans surprise. Utilisez le formulaire de contact pour nous décrire votre situation.</p>"""
    },
    {
        "slug": "assurance-fuite-eau",
        "title": "Fuite d'eau et assurance habitation",
        "title_seo": "Assurance habitation fuite eau dégât eaux remboursement dossier",
        "desc": "Comment faire prendre en charge une fuite d'eau par votre assurance habitation ? Le dossier, les démarches et le rapport de recherche de fuite.",
        "contenu": """<p>Une fuite d'eau peut générer des dégâts importants. Heureusement, votre assurance habitation couvre dans la plupart des cas les frais de recherche de fuite et les réparations qui en découlent.</p>
<h2>Ce que couvre l'assurance habitation</h2>
<p>La garantie dégâts des eaux de votre contrat d'assurance habitation couvre généralement :</p>
<ul>
<li>Les dommages causés par la fuite sur vos biens mobiliers et immobiliers</li>
<li>Les frais de recherche de fuite non destructive</li>
<li>Dans certains contrats, les frais de remise en état après réparation (revêtements, carrelage)</li>
</ul>
<h2>Les démarches à suivre</h2>
<p><strong>1. Déclarez le sinistre dès que possible</strong> - La plupart des contrats imposent une déclaration dans les 5 jours ouvrés suivant la découverte. Par courrier recommandé ou via l'espace client en ligne.</p>
<p><strong>2. Faites réaliser une recherche de fuite</strong> - Votre assureur peut mandater un expert, mais vous pouvez aussi choisir votre propre prestataire. Le rapport que nous vous remettons est reconnu par l'ensemble des assureurs.</p>
<p><strong>3. Constituez votre dossier</strong> - Rassemblez les photos des dégâts, les factures d'eau des 6 derniers mois, le rapport de recherche de fuite et les devis de réparation.</p>
<h2>Le rapport de recherche de fuite</h2>
<p>C'est le document central de votre dossier. Il doit mentionner : la localisation précise de la fuite, la technique utilisée, les photos de l'intervention et les préconisations de réparation. Nous fournissons systématiquement ce rapport à l'issue de chaque intervention en Gironde.</p>"""
    },
    {
        "slug": "urgence-fuite-eau",
        "title": "Que faire en cas d'urgence fuite d'eau ?",
        "title_seo": "Urgence fuite eau que faire premiers gestes Gironde",
        "desc": "Fuite d'eau soudaine ou importante en Gironde ? Les bons réflexes à avoir immédiatement pour limiter les dégâts en attendant l'intervention.",
        "contenu": """<p>Face à une fuite d'eau importante, chaque minute compte. Voici les bons gestes à adopter pour limiter les dégâts en attendant l'intervention d'un technicien.</p>
<h2>Les gestes immédiats</h2>
<p><strong>1. Coupez l'arrivée d'eau</strong> - La vanne d'arrêt générale se trouve généralement près du compteur d'eau ou sous l'évier. Si vous ne la trouvez pas, contactez votre syndic ou votre gestionnaire.</p>
<p><strong>2. Coupez l'électricité si nécessaire</strong> - Si l'eau atteint des prises électriques ou des installations, coupez le disjoncteur correspondant. Ne touchez jamais une installation électrique en présence d'eau.</p>
<p><strong>3. Récupérez l'eau</strong> - Utilisez des seaux, des serviettes et des serpillières pour limiter la propagation. Protégez les meubles et appareils électroménagers.</p>
<p><strong>4. Documentez les dégâts</strong> - Prenez des photos de tout : la zone touchée, les biens endommagés, l'étendue des dégâts. Ces photos seront indispensables pour votre déclaration d'assurance.</p>
<h2>Prévenez votre assureur rapidement</h2>
<p>La déclaration de sinistre doit être effectuée dans les 5 jours ouvrés. Plus tôt vous la faites, plus vite la prise en charge débutera.</p>
<h2>Prévenez vos voisins si nécessaire</h2>
<p>En appartement, une fuite peut affecter les logements du dessous ou du dessus. Prévenez-les immédiatement et laissez leur vos coordonnées.</p>
<h2>Faites appel à un professionnel pour localiser la fuite</h2>
<p>Une fois l'urgence gérée, il est indispensable de faire localiser la fuite par un professionnel avant toute remise en eau. En Gironde, nous intervenons sous 24h pour une <a href="/detection-fuite/" style="color:var(--green);text-decoration:underline;">recherche de fuite non destructive</a> avec remise du rapport assurance.</p>"""
    },
]

def page_guide_article(art):
    sidebar = f'''<div class="aside-cta">
  <h3>Besoin d'une intervention ?</h3>
  <p>Nos techniciens interviennent dans toute la Gironde sous 24h. Devis gratuit et sans engagement.</p>
  <a href="/devis/" class="btn btn-gold btn-full">Demander un devis</a>
</div>
<div style="background:var(--white);border:1px solid var(--border);border-radius:var(--r-lg);padding:1.5rem;">
  <h3 style="font-family:var(--f-title);font-size:1rem;font-weight:700;color:var(--green-dark);margin-bottom:1rem;">Nos services</h3>
  <ul style="display:flex;flex-direction:column;gap:.5rem;">
    <li><a href="/detection-fuite/" style="color:var(--green);font-size:.9rem;">Détection de fuite non destructive</a></li>
    <li><a href="/chemisage-canalisation/" style="color:var(--green);font-size:.9rem;">Chemisage de canalisation</a></li>
    <li><a href="/guide/faq/" style="color:var(--green);font-size:.9rem;">FAQ fuites d'eau</a></li>
  </ul>
</div>'''

    body = f'''
<section class="hero-mini">
  <div class="container">
    <nav class="breadcrumb">
      <a href="/">Accueil</a>
      <span>&rsaquo;</span>
      <a href="/guide/">Guide</a>
      <span>&rsaquo;</span>
      <span>{art["title"]}</span>
    </nav>
    <h1>{art["title"]}</h1>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="article-layout">
      <div class="article-body">
        {art["contenu"]}
      </div>
      <div class="article-sidebar">
        {sidebar}
      </div>
    </div>
  </div>
</section>
{form_section()}'''

    return html_base(
        art["title_seo"][:60],
        art["desc"][:160],
        f"https://recherche-fuite-gironde.fr/guide/{art['slug']}/",
        body
    )

# ── Page FAQ ───────────────────────────────────────────────────
FAQ_ITEMS = [
    ("Comment savoir si j'ai une fuite d'eau ?", "Faites le test du compteur : coupez tous les robinets, notez l'index et revenez une heure plus tard. Si l'index a bougé, vous avez une fuite. D'autres signes : facture d'eau en hausse, sol chaud, taches d'humidité."),
    ("Combien de temps dure une recherche de fuite ?", "En général, une intervention dure entre 1h30 et 3h selon la complexité de l'installation. Pour les réseaux enterrés complexes, cela peut aller jusqu'à une demi-journée."),
    ("Est-ce que la recherche de fuite est remboursée par l'assurance ?", "Oui, dans la plupart des contrats d'assurance habitation. La garantie dégâts des eaux couvre les frais de recherche de fuite non destructive. Le rapport que nous fournissons est indispensable pour ce remboursement."),
    ("Faut-il démolir pour trouver une fuite ?", "Non. Nos méthodes de détection (acoustique, thermographie, gaz traceur) permettent de localiser la fuite sans aucune démolition préalable. L'ouverture éventuelle est ensuite chirurgicale, au seul endroit de la fuite."),
    ("Quelle est la différence entre une fuite et un dégât des eaux ?", "Une fuite est l'origine du problème : la canalisation ou le joint qui fuit. Le dégât des eaux est la conséquence : l'humidité, les taches, les moisissures. Pour être indemnisé, il faut d'abord faire constater et localiser la fuite."),
    ("Qu'est-ce que le chemisage de canalisation ?", "Le chemisage consiste à insérer un manchon en résine époxy dans la canalisation existante. Ce manchon est gonflé et durci sur place, créant un nouveau tuyau à l'intérieur de l'ancien. Aucun démontage ni démolition n'est nécessaire."),
    ("Le chemisage est-il durable ?", "Oui. La résine époxy utilisée a une durée de vie supérieure à 50 ans dans des conditions normales d'utilisation. C'est une solution définitive, pas un palliatif temporaire."),
    ("Intervenez-vous en urgence ?", "Nous proposons des interventions prioritaires sous 24h sur toute la Gironde. En cas d'urgence immédiate, commencez par couper l'arrivée d'eau générale, puis contactez-nous via le formulaire."),
    ("Quelles canalisations peut-on chemiser ?", "Le chemisage est applicable sur la plupart des matériaux : fonte, PVC, grès, cuivre, acier galvanisé. Il convient aux canalisations d'eau potable, d'évacuation et aux réseaux enterrés."),
    ("Vous intervenez dans quelle zone géographique ?", "Nous intervenons sur 30 communes du département de la Gironde (33) : Bordeaux, Mérignac, Pessac, Talence, Arcachon, Libourne et toutes les communes du bassin d'Arcachon, du Médoc et de la métropole bordelaise."),
    ("Fournissez-vous un rapport après l'intervention ?", "Oui, systématiquement. Le rapport mentionne la localisation précise de la fuite, les techniques utilisées, les photos de l'intervention et les préconisations de réparation. Ce document est reconnu par les assureurs."),
    ("Quelle est la différence entre la corrélation acoustique et le gaz traceur ?", "La corrélation acoustique analyse le bruit produit par la fuite et est très efficace sur les canalisations sous pression. Le gaz traceur est utilisé pour les fuites de faible débit difficiles à capter acoustiquement. Les deux méthodes sont souvent complémentaires."),
    ("Est-ce qu'une fuite peut se résorber seule ?", "Non. Une fuite dans une canalisation n'évolue qu'en s'aggravant. L'eau sous pression élargit progressivement la fissure. Plus on attend, plus les dégâts et les coûts augmentent."),
    ("Comment préparer la venue du technicien ?", "Assurez-vous d'avoir accès aux vannes d'arrêt, au compteur d'eau et aux pièces concernées. Rassemblez si possible les anciennes factures d'eau pour montrer l'évolution de la consommation. Notez les dates d'apparition des premiers signes."),
    ("Pourquoi faire appel à un spécialiste plutôt qu'un plombier généraliste ?", "La recherche de fuite non destructive nécessite des équipements spécifiques (corrélateur acoustique, caméra endoscopique, détecteur de gaz traceur) que la plupart des plombiers généralistes ne possèdent pas. Un spécialiste localise la fuite sans casse, ce qui réduit considérablement les coûts de remise en état."),
]

def page_faq():
    items_html = '\n'.join([
        f'<div style="border:1px solid var(--border);border-radius:var(--r-md);padding:1.25rem 1.5rem;background:var(--white);">'
        f'<h3 style="font-family:var(--f-title);font-size:1rem;font-weight:700;color:var(--green-dark);margin-bottom:.5rem;">{q}</h3>'
        f'<p style="font-size:.9375rem;color:var(--muted);line-height:1.65;">{a}</p>'
        f'</div>'
        for q, a in FAQ_ITEMS
    ])
    faq_ld_items = ',\n'.join([
        f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}'
        for q, a in FAQ_ITEMS
    ])
    ld = f'''<script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [{faq_ld_items}]
  }}
  </script>'''

    body = f'''
<section class="hero-mini">
  <div class="container">
    <nav class="breadcrumb">
      <a href="/">Accueil</a>
      <span>&rsaquo;</span>
      <a href="/guide/">Guide</a>
      <span>&rsaquo;</span>
      <span>FAQ</span>
    </nav>
    <h1>Questions fréquentes sur les fuites d'eau en Gironde</h1>
    <p class="hero-mini-lead">Toutes les réponses aux questions les plus posées sur la détection de fuites, le chemisage et les démarches d'assurance en Gironde (33).</p>
  </div>
</section>
<section class="section">
  <div class="container" style="max-width:820px;">
    <div style="display:flex;flex-direction:column;gap:1rem;">
      {items_html}
    </div>
  </div>
</section>
{form_section()}'''

    return html_base(
        "FAQ fuites d'eau Gironde 33 questions fréquentes",
        "Questions fréquentes sur la recherche de fuite, le chemisage et l'assurance en Gironde (33). Réponses d'experts.",
        "https://recherche-fuite-gironde.fr/guide/faq/",
        body, ld
    )

# ── Page guide — sommaire ──────────────────────────────────────
def page_guide_index():
    articles_html = '\n'.join([
        f'''<a href="/guide/{a["slug"]}/" class="guide-card">
          <div class="guide-card-icon"><img src="/assets/icons/search.svg" alt=""></div>
          <h3>{a["title"]}</h3>
          <p>{a["desc"][:120]}...</p>
          <span class="guide-card-lire">Lire l'article &rarr;</span>
        </a>'''
        for a in GUIDE_PAGES
    ])

    body = f'''
<section class="hero-mini">
  <div class="container">
    <nav class="breadcrumb">
      <a href="/">Accueil</a>
      <span>&rsaquo;</span>
      <span>Guide pratique</span>
    </nav>
    <h1>Guide pratique : fuites d'eau en Gironde</h1>
    <p class="hero-mini-lead">Tout ce qu'il faut savoir sur la détection de fuites, le chemisage et les démarches d'assurance en Gironde (33).</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-header-center">
      <span class="section-eyebrow">Ressources</span>
      <h2 class="section-title">Articles du guide</h2>
      <p class="section-lead">Des réponses précises aux questions que vous vous posez sur les fuites d'eau et leurs solutions.</p>
    </div>
    <div class="grid-3">
      {articles_html}
      <a href="/guide/faq/" class="guide-card">
        <div class="guide-card-icon"><img src="/assets/icons/help-circle.svg" alt=""></div>
        <h3>FAQ - Questions fréquentes</h3>
        <p>15 questions et réponses sur la détection de fuites, le chemisage et les démarches assurance en Gironde.</p>
        <span class="guide-card-lire">Voir la FAQ &rarr;</span>
      </a>
    </div>
  </div>
</section>
{form_section()}'''

    return html_base(
        "Guide fuites d'eau Gironde 33 détection chemisage assurance",
        "Guide complet sur les fuites d'eau en Gironde (33). Détection, chemisage, assurance, urgences. Conseils d'experts.",
        "https://recherche-fuite-gironde.fr/guide/",
        body
    )

# ── Page devis dédiée ─────────────────────────────────────────
def page_devis():
    options = '\n'.join([
        f'<option value="{v["nom"]}">{v["nom"]} ({v["code_postal"]})</option>'
        for v in VILLES
    ])
    body = f'''
<section class="hero-mini">
  <div class="container">
    <nav class="breadcrumb">
      <a href="/">Accueil</a>
      <span>&rsaquo;</span>
      <span>Demande de devis</span>
    </nav>
    <span class="badge badge-gold" style="margin-bottom:1rem;">Gratuit &bull; Sans engagement &bull; Réponse sous 24h</span>
    <h1>Demandez votre devis gratuit</h1>
    <p class="hero-mini-lead">Remplissez le formulaire ci-dessous. Un technicien vous rappelle sous 24h ouvrées pour évaluer votre situation et établir un devis précis.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="devis-layout">
      <div class="devis-arguments">
        <h2 class="section-title">Pourquoi nous choisir ?</h2>
        <ul class="contact-check-list" style="margin-top:1rem;">
          <li class="contact-check" style="color:var(--text);">
            <img src="/assets/icons/tick-circle.svg" alt="" style="filter:brightness(0) saturate(100%) invert(35%) sepia(50%) saturate(400%) hue-rotate(120deg) brightness(90%);">
            Devis gratuit et sans engagement
          </li>
          <li class="contact-check" style="color:var(--text);">
            <img src="/assets/icons/clock.svg" alt="" style="filter:brightness(0) saturate(100%) invert(35%) sepia(50%) saturate(400%) hue-rotate(120deg) brightness(90%);">
            Intervention sous 24h en Gironde
          </li>
          <li class="contact-check" style="color:var(--text);">
            <img src="/assets/icons/search.svg" alt="" style="filter:brightness(0) saturate(100%) invert(35%) sepia(50%) saturate(400%) hue-rotate(120deg) brightness(90%);">
            Détection non destructive - zéro casse
          </li>
          <li class="contact-check" style="color:var(--text);">
            <img src="/assets/icons/tick-badge.svg" alt="" style="filter:brightness(0) saturate(100%) invert(35%) sepia(50%) saturate(400%) hue-rotate(120deg) brightness(90%);">
            Rapport officiel pour votre assurance
          </li>
          <li class="contact-check" style="color:var(--text);">
            <img src="/assets/icons/lock.svg" alt="" style="filter:brightness(0) saturate(100%) invert(35%) sepia(50%) saturate(400%) hue-rotate(120deg) brightness(90%);">
            Données confidentielles, jamais revendues
          </li>
        </ul>
        <div class="temoignage-card" style="margin-top:2rem;">
          <div class="temoignage-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
          <p class="temoignage-text">« Devis reçu le jour même, technicien sur place le lendemain. La fuite sous dalle trouvée en 1h30 sans casse. Rapport parfait pour l'assurance. »</p>
          <div class="temoignage-author">M. Leroy &mdash; Bordeaux (33000)</div>
        </div>
      </div>
      <div class="devis-form" style="background:var(--green-dark);padding:2rem;border-radius:var(--r-lg);">
        <h2 style="font-family:var(--f-title);font-size:1.3rem;font-weight:700;color:var(--text-inv);margin-bottom:1.5rem;">Votre demande de devis</h2>
        <form action="https://formsubmit.co/sites-recherche-fuite@outlook.com" method="POST">
          <input type="hidden" name="_subject" value="[recherche-fuite-gironde.fr] Demande de devis">
          <input type="hidden" name="_captcha" value="false">
          <input type="hidden" name="_template" value="table">
          <input type="hidden" name="_next" id="next-url" value="/merci/">
        <script>document.getElementById("next-url").value=window.location.origin+"/merci/";</script>
          <input type="hidden" name="site_source" value="recherche-fuite-gironde.fr/devis/">
          <div class="form-grid-2" style="margin-bottom:1rem;">
            <div class="form-group">
              <label class="form-label" for="prenom">Prénom</label>
              <input class="form-input" type="text" id="prenom" name="prenom" placeholder="Votre prénom" required>
            </div>
            <div class="form-group">
              <label class="form-label" for="nom">Nom</label>
              <input class="form-input" type="text" id="nom" name="nom" placeholder="Votre nom" required>
            </div>
          </div>
          <div class="form-grid-2" style="margin-bottom:1rem;">
            <div class="form-group">
              <label class="form-label" for="telephone">Téléphone</label>
              <input class="form-input" type="tel" id="telephone" name="telephone" placeholder="06 XX XX XX XX" required>
            </div>
            <div class="form-group">
              <label class="form-label" for="email">Email</label>
              <input class="form-input" type="email" id="email" name="email" placeholder="votre@email.fr" required>
            </div>
          </div>
          <div class="form-group" style="margin-bottom:1rem;">
            <label class="form-label" for="ville-select">Votre ville</label>
            <select class="form-input form-select" id="ville-select" name="ville" required>
              <option value="">Choisir une ville</option>
              {options}
              <option value="Autre">Autre ville de Gironde</option>
            </select>
          </div>
          <div class="form-group" style="margin-bottom:1rem;">
            <label class="form-label" for="probleme">Type de problème</label>
            <select class="form-input form-select" id="probleme" name="probleme" required>
              <option value="">Choisir</option>
              <option value="Fuite visible">Fuite visible (tache, humidité)</option>
              <option value="Compteur anormal">Compteur d'eau anormal</option>
              <option value="Fuite sous dalle">Suspicion de fuite sous dalle</option>
              <option value="Fuite enterrée">Fuite canalisation enterrée</option>
              <option value="Chemisage">Chemisage de canalisation</option>
              <option value="Rapport assurance">Rapport pour assurance</option>
              <option value="Autre">Autre</option>
            </select>
          </div>
          <div class="form-group" style="margin-bottom:1.5rem;">
            <label class="form-label" for="message">Décrivez votre situation</label>
            <textarea class="form-input form-textarea" id="message" name="message" placeholder="Ex : compteur qui tourne la nuit, tache d'humidité au plafond, sol chaud..." required></textarea>
          </div>
          <button type="submit" class="btn btn-gold btn-full">Envoyer ma demande</button>
          <p style="font-size:.8rem;color:rgba(247,246,242,.4);text-align:center;margin-top:.75rem;">Aucune donnée personnelle n'est transmise à des tiers.</p>
        </form>
      </div>
    </div>
  </div>
</section>'''

    return html_base(
        "Devis gratuit recherche fuite Gironde 33 sans engagement",
        "Demandez votre devis gratuit pour une recherche de fuite ou un chemisage en Gironde (33). Réponse sous 24h, intervention sous 24h.",
        "https://recherche-fuite-gironde.fr/devis/",
        body,
        hide_sticky_cta=True
    )

# ── Sitemap XML ────────────────────────────────────────────────
def gen_sitemap():
    urls = ['https://recherche-fuite-gironde.fr/']
    urls += [
        'https://recherche-fuite-gironde.fr/detection-fuite/',
        'https://recherche-fuite-gironde.fr/chemisage-canalisation/',
        'https://recherche-fuite-gironde.fr/devis/',
        'https://recherche-fuite-gironde.fr/guide/',
        'https://recherche-fuite-gironde.fr/contact/',
        'https://recherche-fuite-gironde.fr/mentions-legales/',
        'https://recherche-fuite-gironde.fr/plan-du-site/',
        'https://recherche-fuite-gironde.fr/guide/faq/',
    ]
    urls += [f'https://recherche-fuite-gironde.fr/guide/{a["slug"]}/' for a in GUIDE_PAGES]
    urls += [f'https://recherche-fuite-gironde.fr/villes/{v["slug"]}/' for v in VILLES]
    urls += [f'https://recherche-fuite-gironde.fr/villes/{v["slug"]}/chemisage/' for v in VILLES]

    items = '\n'.join([
        f'  <url><loc>{u}</loc><lastmod>2025-01-01</lastmod><changefreq>monthly</changefreq><priority>{"1.0" if u.endswith(".fr/") else "0.8"}</priority></url>'
        for u in urls
    ])
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{items}
</urlset>'''

# ── robots.txt ─────────────────────────────────────────────────
ROBOTS = """User-agent: *
Allow: /
Sitemap: https://recherche-fuite-gironde.fr/sitemap.xml
"""

# ── vercel.json ────────────────────────────────────────────────
VERCEL = """{
  "cleanUrls": true,
  "trailingSlash": true,
  "headers": [
    {
      "source": "/assets/(.*)",
      "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]
    }
  ],
  "redirects": [
    {"source": "/(.*).html", "destination": "/$1/", "permanent": true}
  ]
}
"""

# ── Écriture des fichiers ──────────────────────────────────────
def write(path, content):
    p = BASE / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding='utf-8')
    print(f'  OK  {path}')

def main():
    print('\n=== Génération du site recherche-fuite-gironde.fr ===\n')

    print('[1/8] Pages de service...')
    write('detection-fuite/index.html', page_detection())
    write('chemisage-canalisation/index.html', page_chemisage_service())

    print('[2/8] Pages utilitaires...')
    write('contact/index.html', page_contact())
    write('devis/index.html', page_devis())
    write('mentions-legales/index.html', page_mentions())
    write('plan-du-site/index.html', page_plan())

    print('[3/8] Guide — sommaire...')
    write('guide/index.html', page_guide_index())

    print('[4/8] Guide — articles...')
    for art in GUIDE_PAGES:
        write(f'guide/{art["slug"]}/index.html', page_guide_article(art))

    print('[5/8] Guide — FAQ...')
    write('guide/faq/index.html', page_faq())

    print('[6/8] Pages villes — détection (30)...')
    for v in VILLES:
        write(f'villes/{v["slug"]}/index.html', page_ville_detection(v))

    print('[7/8] Pages villes — chemisage (30)...')
    for v in VILLES:
        write(f'villes/{v["slug"]}/chemisage/index.html', page_ville_chemisage(v))

    print('[8/8] Fichiers techniques...')
    write('sitemap.xml', gen_sitemap())
    write('robots.txt', ROBOTS)
    write('vercel.json', VERCEL)

    total = 2 + 3 + 1 + len(GUIDE_PAGES) + 1 + len(VILLES)*2 + 3
    print(f'\n✓ {total} fichiers générés avec succès.\n')

if __name__ == '__main__':
    main()
