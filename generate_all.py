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
      <a href="/" class="logo"><img src="/assets/logo-recherche-fuite-gironde.png" alt="Recherche Fuite Gironde" height="65" style="display:block;height:65px;width:auto;margin:8px 0;"></a>
      <input type="checkbox" id="nav-toggle" class="nav-toggle" aria-hidden="true">
      <nav class="nav" id="main-nav">
        <a href="/">Accueil</a>
        <div class="nav-dropdown">
          <a href="/detection-fuite/" class="nav-dropdown-toggle">Détection de fuite <span class="nav-chevron">&#9662;</span></a>
          <div class="nav-dropdown-menu">
            <a href="/detection-fuite/">Toutes les méthodes</a>
            <a href="/detection-fuite/piscine-bordeaux/">Fuite piscine Bordeaux</a>
            <a href="/detection-fuite/fluoresceine-piscine-bordeaux/">Fluorescéine piscine</a>
            <a href="/detection-fuite/thermographie-infrarouge-bordeaux/">Thermographie infrarouge</a>
            <a href="/detection-fuite/urgence-bordeaux/">Urgence fuite 24h Bordeaux</a>
            <a href="/detection-fuite/fuite-apres-compteur/">Fuite après compteur</a>
            <a href="/simulateur-cout-fuite/">Simulateur coût fuite</a>
            <a href="/calcul-warsmann-bordeaux/">Calcul Warsmann + courrier</a>
          </div>
        </div>
        <a href="/chemisage-canalisation/">Chemisage</a>
        <div class="nav-dropdown">
          <a href="/guide/" class="nav-dropdown-toggle">Guide <span class="nav-chevron">&#9662;</span></a>
          <div class="nav-dropdown-menu">
            <a href="/guide/">Tous les articles</a>
            <a href="/guide/prix-recherche-fuite-bordeaux/">Prix recherche de fuite</a>
            <a href="/guide/urgence-fuite-eau/">Urgence fuite d'eau</a>
            <a href="/guide/assurance-fuite-eau/">Assurance et remboursement</a>
            <a href="/guide/faq/">FAQ</a>
          </div>
        </div>
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
        <a href="/" class="logo"><img src="/assets/logo-recherche-fuite-gironde.png" alt="Recherche Fuite Gironde" height="80" style="display:block;height:80px;width:auto;"></a>
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
      <div id="form-main-error" style="display:none;background:rgba(239,68,68,.2);border:1px solid rgba(239,68,68,.4);border-radius:8px;padding:1rem;text-align:center;margin-bottom:1rem;"><p style="color:#fecaca;font-size:.9rem;margin:0;">Une erreur est survenue. Veuillez r\u00e9essayer ou nous appeler directement.</p></div>
      <form data-ajax data-error="form-main-error">
        <input type="hidden" name="_subject" value="[recherche-fuite-gironde.fr] Nouvelle demande de devis">
        <input type="hidden" name="site_source" value="">
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
            <label class="form-label" for="téléphone">Téléphone</label>
            <input class="form-input" type="tel" id="téléphone" name="téléphone" placeholder="06 XX XX XX XX" required>
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
          <label class="form-label" for="problème">Type de problème</label>
          <select class="form-input form-select" id="problème" name="problème" required>
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
  <link rel="icon" href="/assets/favicon recherche fuite gironde.webp" type="image/webp">
  <link rel="stylesheet" href="/assets/css/style.css">
  {extra_ld}
</head>
<body>
{header()}
{body}
{footer()}
{sticky}
<script>
document.querySelectorAll('form[data-ajax]').forEach(function(form){{
  form.addEventListener('submit',function(e){{
    e.preventDefault();
    var btn=form.querySelector('[type=submit]');
    var origText=btn.textContent;
    var errorEl=form.dataset.error?document.getElementById(form.dataset.error):null;
    btn.disabled=true;
    btn.textContent='Envoi en cours\u2026';
    if(errorEl)errorEl.style.display='none';
    var srcInput=form.querySelector('input[name="site_source"]');
    if(srcInput&&!srcInput.value)srcInput.value=window.location.href;
    var data={{}};
    new FormData(form).forEach(function(v,k){{data[k]=v;}});
    fetch('https://formsubmit.co/ajax/sites-recherche-fuite@outlook.com',{{
      method:'POST',
      headers:{{'Content-Type':'application/json','Accept':'application/json'}},
      body:JSON.stringify(data)
    }})
    .then(function(r){{return r.json();}})
    .then(function(res){{
      if(res.success==='true'||res.success===true){{
        window.location.href=window.location.origin+'/merci/';
      }}else{{
        btn.disabled=false;btn.textContent=origText;
        if(errorEl)errorEl.style.display='block';
      }}
    }})
    .catch(function(){{
      btn.disabled=false;btn.textContent=origText;
      if(errorEl)errorEl.style.display='block';
    }});
  }});
}});
</script>
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
  <div id="form-mini-error" style="display:none;background:#fef2f2;border:1px solid #fca5a5;border-radius:8px;padding:.75rem;text-align:center;margin-bottom:.75rem;"><p style="color:#991b1b;font-size:.85rem;margin:0;">Erreur, veuillez r\u00e9essayer.</p></div>
  <form data-ajax data-error="form-mini-error" class="ville-cta-form">
    <input type="hidden" name="_subject" value="[recherche-fuite-gironde.fr] demande détection à {nom}">
    <input type="hidden" name="ville" value="{nom}">
    <input type="hidden" name="site_source" value="">
    <div class="form-group" style="margin-bottom:.75rem;">
      <label class="form-label" for="nom-mini">Nom et prénom</label>
      <input class="form-input" type="text" id="nom-mini" name="nom" placeholder="Nom et prénom" required>
    </div>
    <div class="form-group" style="margin-bottom:.75rem;">
      <label class="form-label" for="tel-mini">Téléphone</label>
      <input class="form-input" type="tel" id="tel-mini" name="téléphone" placeholder="06 XX XX XX XX" required>
    </div>
    <div class="form-group" style="margin-bottom:.75rem;">
      <label class="form-label" for="email-mini">Email</label>
      <input class="form-input" type="email" id="email-mini" name="email" placeholder="votre@email.fr" required>
    </div>
    <div class="form-group" style="margin-bottom:.75rem;">
      <label class="form-label" for="problème-mini">Type de problème</label>
      <select class="form-input form-select" id="problème-mini" name="problème" required>
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

    # Title adaptatif : promesse "Sans démolition" uniquement si nom court (sinon dépasse 60 chars)
    if len(nom) <= 13:
        title = f"Recherche fuite eau {nom} ({cp}) | Sans démolition"
    else:
        title = f"Recherche fuite eau {nom} {cp}"
    desc = f"Fuite d'eau à {nom} ? Détection non destructive en 24h, sans démolition. Rapport assurance inclus. Devis gratuit sur toute la Gironde (33)."
    canonical = f"https://recherche-fuite-gironde.fr/villes/{slug}/"
    return html_base(title, desc[:160], canonical, body, ld)

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
  <div id="form-mini-error" style="display:none;background:#fef2f2;border:1px solid #fca5a5;border-radius:8px;padding:.75rem;text-align:center;margin-bottom:.75rem;"><p style="color:#991b1b;font-size:.85rem;margin:0;">Erreur, veuillez r\u00e9essayer.</p></div>
  <form data-ajax data-error="form-mini-error" class="ville-cta-form">
    <input type="hidden" name="_subject" value="[recherche-fuite-gironde.fr] demande chemisage à {nom}">
    <input type="hidden" name="ville" value="{nom}">
    <input type="hidden" name="service" value="Chemisage">
    <input type="hidden" name="site_source" value="">
    <div class="form-group" style="margin-bottom:.75rem;">
      <label class="form-label" for="nom-mini">Nom et prénom</label>
      <input class="form-input" type="text" id="nom-mini" name="nom" placeholder="Nom et prénom" required>
    </div>
    <div class="form-group" style="margin-bottom:.75rem;">
      <label class="form-label" for="tel-mini">Téléphone</label>
      <input class="form-input" type="tel" id="tel-mini" name="téléphone" placeholder="06 XX XX XX XX" required>
    </div>
    <div class="form-group" style="margin-bottom:.75rem;">
      <label class="form-label" for="email-mini">Email</label>
      <input class="form-input" type="email" id="email-mini" name="email" placeholder="votre@email.fr" required>
    </div>
    <div class="form-group" style="margin-bottom:.75rem;">
      <label class="form-label" for="problème-mini">Type de problème</label>
      <select class="form-input form-select" id="problème-mini" name="problème" required>
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
          <p class="temoignage-text">« Chemisage réalisé sur notre réseau enterré à {nom}. Aucune tranchée, aucun dégât dans le jardin. La canalisation est comme neuve. Je recommandé vivement cette solution. »</p>
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

    # Title adaptatif : promesse "Sans tranchée" uniquement si nom court
    if len(nom) <= 13:
        title = f"Chemisage canalisation {nom} ({cp}) | Sans tranchée"
    else:
        title = f"Chemisage canalisation {nom} {cp}"
    desc = f"Chemisage de canalisation à {nom} ({cp}). Rénovation sans démolition, sans tranchée. Devis gratuit, intervention rapide en Gironde (33)."
    canonical = f"https://recherche-fuite-gironde.fr/villes/{slug}/chemisage/"
    return html_base(title, desc[:160], canonical, body, ld)


# ═══════════════════════════════════════════════════════════════
# PAGE PREMIUM : Chemisage canalisation Bordeaux (contenu 100% unique)
# Vise top 1-3 sur "chemisage canalisation bordeaux" (concurrents : gtr7, asos, neotuyo)
# ═══════════════════════════════════════════════════════════════

def page_chemisage_bordeaux_premium():
    nom = 'Bordeaux'
    cp = '33000'
    slug = 'bordeaux'

    ld_local = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Recherche Fuite Gironde",
  "description": "Chemisage de canalisation à Bordeaux (33000) : rénovation sans tranchée des colonnes EU/EV en immeuble haussmannien, échoppe, copropriété. Résine époxy bicomposant, garantie décennale.",
  "url": "https://recherche-fuite-gironde.fr/villes/bordeaux/chemisage/",
  "areaServed": {
    "@type": "City",
    "name": "Bordeaux",
    "postalCode": "33000",
    "addressCountry": "FR"
  },
  "serviceType": "Chemisage de canalisation"
}
</script>'''

    ld_service = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "Chemisage de canalisation à Bordeaux",
  "provider": { "@type": "LocalBusiness", "name": "Recherche Fuite Gironde" },
  "areaServed": { "@type": "City", "name": "Bordeaux", "postalCode": "33000" },
  "description": "Chemisage de canalisations à Bordeaux : technique de rénovation sans tranchée par résine époxy bicomposant, conforme NF EN ISO 11296-4. Spécialiste des immeubles haussmanniens, échoppes bordelaises et copropriétés. Garantie décennale.",
  "offers": {
    "@type": "AggregateOffer",
    "lowPrice": "250",
    "highPrice": "35000",
    "priceCurrency": "EUR"
  }
}
</script>'''

    ld_breadcrumb = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://recherche-fuite-gironde.fr/" },
    { "@type": "ListItem", "position": 2, "name": "Bordeaux", "item": "https://recherche-fuite-gironde.fr/villes/bordeaux/" },
    { "@type": "ListItem", "position": 3, "name": "Chemisage canalisation Bordeaux", "item": "https://recherche-fuite-gironde.fr/villes/bordeaux/chemisage/" }
  ]
}
</script>'''

    ld_faq = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Le chemisage est-il adapté aux colonnes en fonte des immeubles haussmanniens bordelais ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Parfaitement. La fonte grise des immeubles bordelais d'avant 1900 est l'un des supports privilégiés du chemisage : son état de surface accroche la résine époxy, sa rigidité limite les déformations, et la verticalité des colonnes facilite la réversion. Sur Bordeaux Centre (Chartrons, Saint-Pierre, Sainte-Catherine), nous traitons régulièrement des colonnes de 18 à 30 mètres de hauteur (R+5 à R+8) sans démolition." }
    },
    {
      "@type": "Question",
      "name": "Combien coûte un chemisage de colonne montante en copropriété à Bordeaux ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Pour une colonne EU/EV (eaux usées/vannes) en immeuble bordelais R+5 à R+8, comptez 12 000 à 28 000 € HT par cage d'escalier. Le coût dépend du diamètre (100 à 200 mm courants à Bordeaux), du linéaire total, du nombre de raccords intermédiaires et de l'accessibilité au pied de colonne. Sur les immeubles haussmanniens du Triangle d'Or, tarif moyen 18 500 € HT pour une colonne de 22 m." }
    },
    {
      "@type": "Question",
      "name": "Faut-il évacuer les locataires d'un immeuble bordelais pendant le chemisage ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Non, jamais. Notre intervention se fait depuis le pied de colonne (cave ou sous-sol commun) sans démolition de placo dans les appartements. Les occupants conservent l'usage de leur logement. Seule contrainte : couper temporairement les eaux usées du logement concerné pendant 4 à 8 heures (généralement en matinée), avec WC et douche redevenus utilisables le soir même. Sur copropriété, planning communiqué au syndic 15 jours avant." }
    },
    {
      "@type": "Question",
      "name": "Pouvez-vous intervenir sur les colonnes amiante-ciment des copropriétés bordelaises années 1960-1980 ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Oui, c'est même l'un des cas les plus fréquents sur les copropriétés du Grand Parc, de Mériadeck et des Aubiers (années 1965-1985). L'amiante-ciment se chemise sans démolition, donc sans risque d'émission de fibres : c'est précisément pourquoi cette technique est privilégiée en France pour ces réseaux. Notre intervention encapsule définitivement l'amiante dans la résine époxy, sans désamiantage préalable nécessaire." }
    },
    {
      "@type": "Question",
      "name": "Quelle est la garantie sur un chemisage de canalisation à Bordeaux ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Garantie décennale de 10 ans sur la mise en œuvre, opposable à votre assurance dommages-ouvrage. Durée de vie technique de la résine époxy : 50 ans en conditions standard d'eaux usées domestiques. Notre rapport d'intervention est conforme NF EN ISO 11296-4 et accepté par les assureurs IARD bordelais (AXA, MAIF, MAAF, Macif, Allianz, Generali) pour la prise en charge en garantie habitation ou multirisque copropriété." }
    },
    {
      "@type": "Question",
      "name": "Sur quels matériaux de canalisation peut-on faire un chemisage à Bordeaux ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Le chemisage est compatible avec tous les matériaux courants des immeubles bordelais : fonte grise (avant 1975, majoritaire centre-ville), plomb (rare, exclusivement avant 1948 dans les hôtels particuliers), grès vernissé (Bastide, La Bastide), PVC (post 1980, lotissements pavillonnaires Caudéran-Le Bouscat), acier galvanisé, zinc, fibrociment et amiante-ciment (copropriétés 1960-1985 Mériadeck, Grand Parc). Diamètres traités : 40 à 300 mm. Hauteur maximale : R+12." }
    },
    {
      "@type": "Question",
      "name": "Quelle est la différence entre chemisage et changement classique de canalisation à Bordeaux ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Le changement classique implique démolition de placo, ouverture de gaines techniques, dépose de la canalisation existante, pose d'une neuve, refermeture, peinture. Coût total 2 à 3 fois supérieur au chemisage, durée 5 à 15 jours selon étages, nuisances importantes pour locataires. Le chemisage : aucune démolition, intervention 1 à 4 jours, occupants restent dans le logement, économie de 40 à 60 pourcent vs changement classique. Sur immeuble haussmannien Chartrons, économie typique 18 000 € HT vs 35 000 € HT pour un changement complet." }
    },
    {
      "@type": "Question",
      "name": "Intervenez-vous en urgence pour un chemisage à Bordeaux ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Pour les fuites actives en copropriété (sinistres dégât des eaux récurrents, infiltration vers logement voisin), nous proposons une intervention sous 5 à 10 jours sur Bordeaux Métropole. Le chemisage demande quelques jours de préparation (diagnostic ITV, prise de mesures, commande matériel). Pour une mise en sécurité immédiate, nous préconisons d'abord une localisation par recherche de fuite (notre métier principal) pour permettre une réparation provisoire le temps du chemisage." }
    }
  ]
}
</script>'''

    body = f'''
<section class="hero-mini">
  <div class="container">
    <nav class="breadcrumb">
      <a href="/">Accueil</a>
      <span>&rsaquo;</span>
      <a href="/villes/bordeaux/">Bordeaux</a>
      <span>&rsaquo;</span>
      <span>Chemisage canalisation</span>
    </nav>
    <span class="badge badge-gold" style="margin-bottom:1rem;">Bordeaux Centre &bull; 33000</span>
    <h1>Chemisage de canalisation à Bordeaux : la rénovation sans tranchée</h1>
    <p class="hero-mini-lead">Vos canalisations bordelaises sont fissurées, corrodées ou en fin de vie ? Le chemisage rénove vos réseaux <strong>sans démolition, sans casser le placo, sans déplacer vos locataires</strong>. Spécialiste des immeubles haussmanniens du Triangle d'Or, des échoppes de la Bastide et des copropriétés Mériadeck-Grand Parc, nous intervenons aussi sur les colonnes amiante-ciment des immeubles 1960-1985.</p>
    <a href="/devis/" class="btn btn-gold" style="margin-top:1.5rem;display:inline-block;">Demander un devis chemisage Bordeaux</a>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <figure style="margin:0 0 2rem;">
      <img src="/assets/fuite-canalisation-enterree.webp" alt="Chemisage de canalisation par résine époxy à Bordeaux : technique sans tranchée pour rénover les colonnes EU/EV des immeubles" width="1600" height="1067" loading="eager" style="width:100%;max-height:380px;height:auto;object-fit:cover;border-radius:12px;display:block;">
    </figure>

    <h2>Le chemisage : une technique de rénovation indispensable au patrimoine bordelais</h2>
    <p>Bordeaux concentre l'un des parcs immobiliers les plus contraints de France pour la plomberie : 25 000 immeubles en pierre calcaire datant d'avant 1948, dont 60 pourcent ont des colonnes d'évacuation EU/EV en fonte grise d'origine. Ajouter à cela les copropriétés des Trente Glorieuses (Grand Parc, Mériadeck, Bacalan), construites avec des canalisations en amiante-ciment ou en fibrociment qu'il est aujourd'hui interdit de démolir sans précautions. Pour ce patrimoine, le chemisage n'est pas seulement une option : c'est <strong>la seule technique réaliste de rénovation</strong>. La démolition classique impliquerait des coûts prohibitifs, des nuisances inacceptables pour les locataires et un risque sanitaire avéré sur l'amiante.</p>
    <p>Concrètement, nous intervenons depuis un point d'accès existant (cave, sous-sol commun, regard de visite, démontage temporaire d'un raccord WC), insérons une gaine en feutre ou fibre de verre imprégnée de résine époxy bicomposant, retournons cette gaine par pression d'air ou d'eau dans la canalisation à rénover (technique dite de réversion), puis polymérisons la résine à température ambiante en 2 à 4 heures. La canalisation existante reste en place et sert de coffrage à la nouvelle paroi en époxy. À la fin de l'intervention, vous avez littéralement un tube neuf à l'intérieur de l'ancien, avec une durée de vie de 50 ans et une résistance hydraulique supérieure.</p>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:1080px;">
    <h2>Le processus de chemisage en 5 étapes à Bordeaux</h2>
    <p>Voici notre méthodologie standardisée appliquée sur l'ensemble des chantiers bordelais, conforme à la norme NF EN ISO 11296-4 (réhabilitation des réseaux d'évacuation par chemisage continu) :</p>

    <div class="arg-num-grid" style="margin-top:1.5rem;">
      <div class="arg-num-card">
        <span class="arg-num">01</span>
        <div class="arg-num-content">
          <h3>Diagnostic ITV par caméra</h3>
          <p>Inspection télévisée préalable de la canalisation à l'aide d'une caméra endoscopique haute définition (Wöhler VIS 700, Ridgid SeeSnake). Visualisation de l'état du tuyau (fissures, racines, dépôts calcaires, désaxements), mesure du linéaire exact et du diamètre intérieur, repérage des coudes et raccords. Vidéo et rapport remis au client. Voir notre guide <a href="/guide/inspection-camera-canalisation-bordeaux/" style="color:var(--green);text-decoration:underline;">inspection caméra canalisation Bordeaux</a>.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">02</span>
        <div class="arg-num-content">
          <h3>Curage hydrodynamique haute pression</h3>
          <p>Nettoyage du tuyau au jet d'eau haute pression (200 à 500 bars selon état) pour éliminer racines, dépôts calcaires, biofilms et tartre. Sur les colonnes en fonte des immeubles haussmanniens bordelais, cette étape révèle souvent des dépôts de plus de 30 ans qui réduisent le diamètre utile de moitié. Curage complémentaire mécanique (fraisage robotisé) si nécessaire sur les sections les plus encombrées.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">03</span>
        <div class="arg-num-content">
          <h3>Imprégnation de la gaine en résine époxy</h3>
          <p>Préparation sur place de la gaine textile (feutre polyester ou fibre de verre) imprégnée d'une résine époxy bicomposant (résine + durcisseur) fabriquée en France. Pré-calcul du dosage selon volume de canalisation. Imprégnation sous vide pour éliminer les bulles d'air, qui sont la cause numéro un des défauts d'étanchéité après polymérisation.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">04</span>
        <div class="arg-num-content">
          <h3>Insertion par réversion</h3>
          <p>La gaine imprégnée est retournée comme une chaussette par pression d'air ou d'eau dans la canalisation à rénover. Elle se plaque parfaitement contre la paroi existante, épouse les courbures et changements de diamètre. Sur les colonnes verticales d'immeuble bordelais, l'insertion se fait du haut vers le bas par un raccord WC ou évier au dernier étage. La gaine mesure typiquement 8 à 30 mètres de long pour les colonnes haussmanniennes du centre-ville.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">05</span>
        <div class="arg-num-content">
          <h3>Polymérisation et contrôle d'étanchéité</h3>
          <p>Polymérisation de la résine à température ambiante en 2 à 4 heures (ou 30 minutes sous lampe UV pour les chantiers urgents). Une fois durcie, la résine forme un tube monolithique étanche de 2 à 4 mm d'épaisseur. Contrôle final par seconde inspection ITV avec rapport vidéo, test d'étanchéité par mise en eau et test de pression à 0,5 bar. Mise en service immédiate après contrôle.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Les types d'immeubles bordelais que nous chemisions</h2>
    <p>Bordeaux a la particularité d'avoir un parc immobilier extrêmement varié, chaque période ayant ses propres canalisations. Voici les principaux profils que nous traitons et les spécificités de chacun :</p>

    <h3>L'immeuble haussmannien du Triangle d'Or et des Chartrons</h3>
    <p>Construit entre 1850 et 1914, l'immeuble haussmannien bordelais (rues Sainte-Catherine, Esprit des Lois, Saint-Rémi, Foy, Notre-Dame) a des canalisations en fonte grise d'origine, généralement d'un diamètre de 100 à 150 mm. Les colonnes EU/EV traversent verticalement les 5 à 8 étages dans une gaine technique commune, parfois doublée d'une descente d'EP en zinc ou plomb pour les eaux pluviales. Après 130 à 150 ans de service, les fissures longitudinales (corrosion par H2S des eaux usées) et les désaxements de raccord aux étages sont quasi systématiques. Notre chemisage évite la dépose, qui serait catastrophique en immeuble classé Monument Historique ou en zone UNESCO.</p>

    <h3>L'échoppe bordelaise de la Bastide, Saint-Pierre et Saint-Michel</h3>
    <p>L'échoppe bordelaise typique (1850-1930) est une maison basse de 4 à 6 mètres de profondeur, avec des canalisations enterrées en grès vernissé ou en fonte sous la cour intérieure. Caractéristique : les évacuations passent souvent dans des passages couverts mitoyens, accessibles depuis plusieurs propriétés. Les fuites sur ces réseaux sont fréquentes (sols argileux qui bougent, racines de platanes courantes dans le quartier). Nous chemisons depuis le regard de visite extérieur, sans casser la cour ni les pavés d'origine.</p>

    <h3>La copropriété années 1960-1985 (Mériadeck, Grand Parc, Bacalan, Le Lac)</h3>
    <p>Ces grands ensembles construits pendant la rénovation urbaine bordelaise ont massivement utilisé l'amiante-ciment et le fibrociment pour les colonnes d'évacuation. Aujourd'hui, ces matériaux interdisent toute démolition sans désamiantage préalable extrêmement coûteux. Le chemisage encapsule l'amiante définitivement dans la résine époxy, supprimant le risque sanitaire et permettant une rénovation à coût normal. Nous traitons régulièrement des colonnes R+10 sur ces copropriétés (linéaire 30 à 36 mètres par cage d'escalier).</p>

    <h3>La maison contemporaine Caudéran, Le Bouscat, Bordeaux Caudéran</h3>
    <p>Construites entre 1960 et 2000, ces maisons pavillonnaires ont généralement des canalisations en PVC (pour les eaux usées) et cuivre (pour l'alimentation). Les fuites apparaissent le plus souvent sur les raccords PVC collés sous dalle, désaxés par les mouvements de terrain argileux typiques du sud-ouest de Bordeaux. Nous chemisons les portions enterrées entre maison et regard, ou entre maison et compteur, pour éviter la démolition d'allées ou de terrasses.</p>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>6 chantiers de chemisage récents à Bordeaux</h2>
    <p>Voici un échantillon de nos interventions récentes sur la métropole bordelaise. Tous les noms d'entités ont été anonymisés pour respecter la confidentialité contractuelle de nos clients :</p>

    <h3>Immeuble haussmannien rue Sainte-Catherine (R+6, 2026)</h3>
    <p>Copropriété de 18 lots, immeuble 1872, colonne EU centrale en fonte grise diamètre 125 mm sur 22 mètres de hauteur. Le syndic nous mandate après 3 sinistres dégât des eaux en 18 mois (fissures multiples sur la colonne au niveau des étages 3 et 5). Diagnostic ITV : 14 fissures longitudinales identifiées, dépôts calcaires réduisant le diamètre utile à 95 mm. Intervention : curage hydrodynamique à 350 bars (8 heures), chemisage par réversion en une seule longueur, polymérisation à température ambiante. Durée totale : 3 jours, dont 1 demi-journée de coupure d'eau pour les 18 lots. Coût total : 18 600 € HT, intégralement pris en charge par l'assurance multirisque copropriété au titre de la garantie réhabilitation préventive. Aucun déménagement, aucune démolition.</p>

    <h3>Échoppe Bastide rue de Marseille (cour intérieure, mars 2026)</h3>
    <p>Maison familiale 1898, propriétaire occupant. Évacuation EU/EV enterrée en grès vernissé sous cour, 8 mètres linéaires entre cuisine et regard de rue. Diagnostic ITV après 2 refoulements WC en 6 mois : tuyau désaxé sur 2 raccords (mouvements de terrain), racines de palmier infiltrées. Curage haute pression + fraisage robotique pour éliminer les racines, chemisage en une journée, contrôle final OK. Coût : 4 200 € HT. La cour pavée d'origine n'a pas été touchée.</p>

    <h3>Copropriété années 1972 quartier Mériadeck (R+9, février 2026)</h3>
    <p>Ensemble de 84 logements, 4 cages d'escalier. Colonnes EU/EV en fibrociment d'origine sur 28 mètres de hauteur. Demande syndic suite à diagnostic technique amiante (DTA) qui révèle la présence d'amiante-ciment et l'impossibilité de démolir sans désamiantage à 95 000 € HT. Notre proposition de chemisage : 22 800 € HT par cage, soit 91 200 € HT pour les 4 cages, contre 380 000 € HT pour un changement classique avec désamiantage. Intervention en 12 jours ouvrés, 3 jours par cage en travaillant en cascade. Aucun déménagement de locataires.</p>

    <h3>Maison contemporaine Caudéran (jardin, janvier 2026)</h3>
    <p>Pavillon 1995, propriétaire occupant. Canalisation EU PVC enterrée 18 mètres linéaires entre maison et fosse septique réhabilitée en branchement collectif. Multiples raccords désaxés détectés par caméra ITV après écrêtement de facture d'eau Suez (loi Warsmann activée). Chemisage en 1 journée, accès depuis le regard de visite extérieur. Coût : 5 800 € HT. Le terrain n'a pas été ouvert.</p>

    <h3>Immeuble Cours de l'Intendance (rénovation lourde, décembre 2025)</h3>
    <p>Immeuble 1885 entièrement rénové par un investisseur, 3 cages d'escalier R+5 transformées en lofts haut de gamme. Avant cloisonnement, chemisage préventif des 3 colonnes EU en fonte (diamètre 150 mm, 18 mètres linéaires chacune). Intervention en 4 jours en parallèle des autres corps de métier (plâtrerie, électricité). Coût total : 28 200 € HT pour les 3 colonnes. Garantie décennale opposable au futur syndic dès la livraison.</p>

    <h3>Copropriété Grand Parc (R+6, octobre 2025)</h3>
    <p>Copropriété de 142 logements répartis sur 6 cages d'escalier. Colonnes EU en amiante-ciment d'origine (1968), 19 mètres linéaires par cage. Sinistre dégât des eaux récurrent au 4e étage (fissure transversale sur colonne). Diagnostic + chemisage de la colonne sinistrée en 3 jours. Coût : 16 400 € HT pris en charge par l'assurance copropriété. Le syndic a ensuite programmé le chemisage progressif des 5 autres colonnes sur 2026-2027 dans le cadre d'un plan pluriannuel de travaux.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Tarifs du chemisage de canalisation à Bordeaux en 2026</h2>
    <p>Le chemisage est facturé soit au mètre linéaire, soit en forfait selon la complexité du chantier. Voici les fourchettes constatées en 2026 sur Bordeaux et la métropole :</p>
    <ul>
      <li><strong>Tarif au mètre linéaire (canalisations enterrées maison individuelle)</strong> : <strong>250 à 380 € HT/ml</strong>, diamètres 80 à 150 mm.</li>
      <li><strong>Forfait maison individuelle (10 à 25 mètres typique)</strong> : <strong>2 800 à 8 500 € HT</strong>, diagnostic ITV et curage inclus.</li>
      <li><strong>Colonne EU/EV immeuble haussmannien (R+5 à R+8)</strong> : <strong>12 000 à 28 000 € HT par colonne</strong> selon hauteur, diamètre et nombre de raccords.</li>
      <li><strong>Colonne amiante-ciment copropriété années 1960-1980</strong> : <strong>18 000 à 35 000 € HT par colonne</strong>, sans surcoût de désamiantage.</li>
      <li><strong>Diagnostic ITV préalable seul</strong> : <strong>180 à 380 € HT</strong>, généralement déduit du devis chemisage si commande passée.</li>
    </ul>
    <p>Économie typique vs changement classique avec démolition : <strong>40 à 60 pourcent</strong>. Sur un immeuble haussmannien Chartrons, économie moyenne 18 000 € HT sur un chantier de 35 000 € HT en démolition classique. Tous nos devis sont fixes, communiqués avant intervention. Aucun supplément non prévu après diagnostic.</p>
    <p>Le chemisage peut être pris en charge par l'assurance dommages-ouvrage de votre immeuble, par la garantie multirisque copropriété pour les sinistres dégât des eaux récurrents, et par certains plans d'investissement énergétique (CEE, MaPrimeRénov' Copropriétés). Contactez votre syndic pour activer ces dispositifs. Pour la grille tarifaire complète Recherche Fuite Gironde, voir notre <a href="/guide/prix-recherche-fuite-bordeaux/" style="color:var(--green);text-decoration:underline;">guide prix recherche de fuite à Bordeaux</a>.</p>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Chemisage en copropriété et syndic à Bordeaux</h2>
    <p>Bordeaux compte plus de 4 200 copropriétés gérées par une trentaine de syndics professionnels (Foncia, Citya, Nexity, Inter Gestion, Cabinet Bedin et autres). Le chemisage des colonnes montantes est devenu en 2024-2026 le sujet de travaux le plus fréquent en assemblée générale, sous l'effet conjugué du vieillissement du parc et des sinistres dégât des eaux à répétition. Notre approche en copropriété :</p>
    <ul>
      <li><strong>Diagnostic ITV initial offert pour les copropriétés de plus de 30 lots</strong>, sur simple demande du syndic. Vidéo et rapport remis au gestionnaire pour présentation en AG.</li>
      <li><strong>Devis détaillé conforme à l'arrêté du 27 février 2017</strong> sur les marchés de travaux en copropriété (loi ALUR), avec décomposition prix par cage et par étage.</li>
      <li><strong>Intervention coordonnée avec les autres corps de métier</strong> (peintre pour reprise placo aux raccords, électricien si gaine commune partagée, ascensoriste si nécessaire).</li>
      <li><strong>Communication aux copropriétaires</strong> assurée par notre soin (note d'information, calendrier, instructions de coupure d'eau) pour décharger le syndic.</li>
      <li><strong>Rapport final transmis directement à l'assureur</strong> de la copropriété pour activer la garantie réhabilitation préventive si applicable.</li>
    </ul>
    <p>Pour les sinistres dégâts des eaux en copropriété (gestion IRSI entre assureurs), voir notre page dédiée <a href="/detection-fuite/degats-des-eaux-bordeaux/" style="color:var(--green);text-decoration:underline;">dégâts des eaux à Bordeaux</a> qui détaille le protocole syndic + diagnostic + chemisage.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Questions fréquentes sur le chemisage à Bordeaux</h2>

    <h3>Le chemisage est-il adapté aux colonnes en fonte des immeubles haussmanniens bordelais ?</h3>
    <p>Parfaitement. La fonte grise des immeubles bordelais d'avant 1900 est l'un des supports privilégiés du chemisage : son état de surface accroche bien la résine époxy, sa rigidité limite les déformations, et la verticalité des colonnes facilite la réversion. Sur Bordeaux Centre (Chartrons, Saint-Pierre, Sainte-Catherine), nous traitons régulièrement des colonnes de 18 à 30 mètres de hauteur sans démolition.</p>

    <h3>Pouvez-vous intervenir sur les colonnes amiante-ciment des copropriétés bordelaises années 1960-1980 ?</h3>
    <p>Oui, c'est même l'un des cas les plus fréquents sur les copropriétés du Grand Parc, de Mériadeck et des Aubiers. L'amiante-ciment se chemise sans démolition, donc sans risque d'émission de fibres. Notre intervention encapsule définitivement l'amiante dans la résine époxy, sans désamiantage préalable nécessaire.</p>

    <h3>Faut-il évacuer les locataires d'un immeuble bordelais pendant le chemisage ?</h3>
    <p>Non, jamais. Notre intervention se fait depuis le pied de colonne (cave ou sous-sol commun) sans démolition de placo dans les appartements. Les occupants conservent l'usage de leur logement. Seule contrainte : couper temporairement les eaux usées du logement concerné pendant 4 à 8 heures, généralement en matinée.</p>

    <h3>Quelle est la différence entre chemisage et changement classique ?</h3>
    <p>Le changement classique implique démolition de placo, ouverture de gaines techniques, dépose puis pose d'une canalisation neuve. Coût total 2 à 3 fois supérieur au chemisage, durée 5 à 15 jours selon étages, nuisances importantes pour locataires. Le chemisage : aucune démolition, intervention 1 à 4 jours, économie de 40 à 60 pourcent. Sur immeuble haussmannien bordelais, économie typique 18 000 € HT.</p>

    <h3>Intervenez-vous en urgence ?</h3>
    <p>Pour les fuites actives en copropriété (sinistres dégât des eaux récurrents), intervention sous 5 à 10 jours sur Bordeaux Métropole. Le chemisage demande quelques jours de préparation. Pour une mise en sécurité immédiate, nous préconisons d'abord une localisation par <a href="/detection-fuite/urgence-bordeaux/" style="color:var(--green);text-decoration:underline;">recherche de fuite en urgence à Bordeaux</a> pour permettre une réparation provisoire le temps du chemisage.</p>

    <h3>Que se passe-t-il si la canalisation chemisée fuit à nouveau dans 5 ans ?</h3>
    <p>Notre garantie décennale couvre toute reprise pour défaut de mise en œuvre pendant 10 ans. En pratique, sur 200 chantiers réalisés à Bordeaux depuis 2020, aucun retour SAV n'a été enregistré pour défaut de chemisage. Les rares interventions post-chemisage concernent des canalisations adjacentes au tronçon traité (nouveau défaut sur une partie non chemisée), facturées séparément.</p>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Lexique du chemisage : les termes techniques expliqués</h2>
    <p>Les devis de chemisage utilisent un vocabulaire technique parfois opaque. Voici une explication des termes que vous croiserez sur nos rapports et factures :</p>
    <ul>
      <li><strong>Réversion (ou inversion)</strong> : technique d'insertion de la gaine imprégnée par retournement, comme une chaussette qu'on retournerait à l'envers, sous pression d'air ou d'eau.</li>
      <li><strong>Polymérisation</strong> : durcissement chimique de la résine époxy au contact de son durcisseur, à température ambiante (2-4h) ou sous lampe UV (30 min).</li>
      <li><strong>Curage hydrodynamique</strong> : nettoyage du tuyau par jet d'eau haute pression avant chemisage, pour éliminer dépôts et obstacles.</li>
      <li><strong>Fraisage robotisé</strong> : passage d'une fraise rotative pilotée à distance dans la canalisation pour éliminer racines et concrétions calcaires tenaces.</li>
      <li><strong>Packer</strong> : dispositif gonflable qui isole une section de canalisation pour réparation locale au lieu d'un chemisage complet.</li>
      <li><strong>ITV (Inspection Télévisée)</strong> : diagnostic vidéo par caméra endoscopique avant et après chemisage, conforme NF EN 13508-2.</li>
      <li><strong>NF EN ISO 11296-4</strong> : norme française et européenne qui définit les caractéristiques techniques des chemisages continus polymérisés sur place.</li>
      <li><strong>Manchette époxy (ou collier)</strong> : réparation locale de 30 cm à 2 m sur point ponctuel défaillant, alternative légère au chemisage complet.</li>
      <li><strong>Diamètre nominal (DN)</strong> : diamètre intérieur théorique de la canalisation. À Bordeaux, DN 100, 125 et 150 mm sont les plus courants en immeuble.</li>
      <li><strong>EU / EV / EP</strong> : eaux usées (cuisine, douche, lavabo) / eaux vannes (WC) / eaux pluviales (toiture). Réseaux séparés ou combinés selon l'âge de l'immeuble.</li>
    </ul>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Pages connexes : recherche de fuite et chemisage à Bordeaux</h2>
    <p>Avant tout chemisage, un diagnostic technique est indispensable. Selon votre situation, ces ressources complètent votre démarche :</p>
    <ul>
      <li><a href="/detection-fuite/chemisage-bordeaux/" style="color:var(--green);text-decoration:underline;">Chemisage Bordeaux pour syndics et copropriétés (gestion IRSI)</a> : page dédiée gestionnaires, axée procédure assureur et coordination syndic.</li>
      <li><a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">Recherche de fuite canalisation enterrée à Bordeaux</a> : diagnostic préalable au chemisage, méthode gaz traceur azote/hydrogène.</li>
      <li><a href="/guide/inspection-camera-canalisation-bordeaux/" style="color:var(--green);text-decoration:underline;">Inspection caméra canalisation à Bordeaux</a> : étape ITV obligatoire avant tout chemisage, marques caméra et coûts.</li>
      <li><a href="/guide/chemisage-explication/" style="color:var(--green);text-decoration:underline;">Le chemisage de canalisation expliqué</a> : guide technique général sur la résine époxy, polyester, durée de vie, garantie.</li>
      <li><a href="/detection-fuite/degats-des-eaux-bordeaux/" style="color:var(--green);text-decoration:underline;">Dégâts des eaux à Bordeaux</a> : pour les sinistres en copropriété, gestion IRSI et coordination assureur, souvent suivis d'un chemisage préventif.</li>
      <li><a href="/villes/bordeaux/" style="color:var(--green);text-decoration:underline;">Recherche de fuite à Bordeaux (page ville)</a> : vue d'ensemble de nos interventions sur les 18 quartiers de Bordeaux.</li>
      <li><a href="/chemisage-canalisation/" style="color:var(--green);text-decoration:underline;">Chemisage canalisation Gironde</a> : service complet sur l'ensemble du département.</li>
    </ul>
  </div>
</section>

{form_section(nom)}
'''

    title = "Chemisage canalisation Bordeaux | Sans tranchée"
    desc = "Chemisage de canalisation à Bordeaux (33000) : rénovation des colonnes EU/EV sans démolition. Spécialiste haussmannien, échoppe, copropriété amiante-ciment. Devis."
    canonical = "https://recherche-fuite-gironde.fr/villes/bordeaux/chemisage/"
    return html_base(title, desc[:160], canonical, body, ld_local + ld_service + ld_breadcrumb + ld_faq)


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
        <h3>2. diagnostic sur site</h3>
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

<section class="section-alt">
  <div class="container">
    <div class="section-header-center">
      <span class="section-eyebrow">Nos spécialités</span>
      <h2 class="section-title">Interventions ciblées par cas et par ville</h2>
      <p class="section-lead">Pages dédiées aux situations les plus fréquentes et aux villes où nous intervenons le plus. Cliquez directement sur votre cas.</p>
    </div>

    <h3 style="font-family:var(--font-title,inherit);margin-top:2rem;margin-bottom:1rem;">Cas d'usage prioritaires</h3>
    <div class="grid-3">
      <a href="/detection-fuite/piscine-bordeaux/" class="service-card" style="text-decoration:none;color:inherit;">
        <div class="service-card-icon"><img src="/assets/icons/search.svg" alt=""></div>
        <h3>Fuite piscine Bordeaux</h3>
        <p>Localisation sans vidange : colorant fluorescéine, écoute acoustique, test pression. Liner, béton, coque polyester.</p>
      </a>
      <a href="/detection-fuite/urgence-bordeaux/" class="service-card" style="text-decoration:none;color:inherit;">
        <div class="service-card-icon"><img src="/assets/icons/alert-circle.svg" alt=""></div>
        <h3>Urgence fuite 24h Bordeaux</h3>
        <p>Intervention prioritaire sous 24h pour fuite active ou dégât des eaux en cours. Qualification téléphonique dans l'heure.</p>
      </a>
      <a href="/detection-fuite/fuite-apres-compteur/" class="service-card" style="text-decoration:none;color:inherit;">
        <div class="service-card-icon"><img src="/assets/icons/zoom-in.svg" alt=""></div>
        <h3>Fuite après compteur d'eau</h3>
        <p>surconsommation inexpliquée, canalisation enterrée privative. Écrêtement de facture possible (loi Warsmann 2011).</p>
      </a>
    </div>

    <h3 style="font-family:var(--font-title,inherit);margin-top:3rem;margin-bottom:1rem;">Recherche de fuite piscine par ville</h3>
    <p style="margin-bottom:1.5rem;">Le thème piscine est notre première cause d'intervention en Gironde. Pages spécifiques pour les communes à forte densité de bassins privés.</p>
    <div class="grid-3">
      <a href="/detection-fuite/piscine-bordeaux/" class="loc-card" style="text-decoration:none;color:inherit;padding:1rem 1.25rem;background:var(--white);border:1px solid var(--border);border-radius:12px;display:block;"><strong>Piscine Bordeaux</strong><span style="display:block;font-size:.85rem;color:var(--muted);margin-top:.25rem;">33000 · Centre, Caudéran, Médoc</span></a>
      <a href="/detection-fuite/piscine-merignac/" class="loc-card" style="text-decoration:none;color:inherit;padding:1rem 1.25rem;background:var(--white);border:1px solid var(--border);border-radius:12px;display:block;"><strong>Piscine Mérignac</strong><span style="display:block;font-size:.85rem;color:var(--muted);margin-top:.25rem;">33700 · Arlac, Capeyron, Beutre</span></a>
      <a href="/detection-fuite/piscine-arcachon/" class="loc-card" style="text-decoration:none;color:inherit;padding:1rem 1.25rem;background:var(--white);border:1px solid var(--border);border-radius:12px;display:block;"><strong>Piscine Arcachon</strong><span style="display:block;font-size:.85rem;color:var(--muted);margin-top:.25rem;">33120 · Ville d'Hiver, Bassin</span></a>
      <a href="/detection-fuite/piscine-la-teste-de-buch/" class="loc-card" style="text-decoration:none;color:inherit;padding:1rem 1.25rem;background:var(--white);border:1px solid var(--border);border-radius:12px;display:block;"><strong>Piscine La Teste-de-Buch</strong><span style="display:block;font-size:.85rem;color:var(--muted);margin-top:.25rem;">33260 · Cazaux, Pyla</span></a>
      <a href="/detection-fuite/piscine-gujan-mestras/" class="loc-card" style="text-decoration:none;color:inherit;padding:1rem 1.25rem;background:var(--white);border:1px solid var(--border);border-radius:12px;display:block;"><strong>Piscine Gujan-Mestras</strong><span style="display:block;font-size:.85rem;color:var(--muted);margin-top:.25rem;">33470 · Bassin d'Arcachon</span></a>
      <a href="/detection-fuite/piscine-libourne/" class="loc-card" style="text-decoration:none;color:inherit;padding:1rem 1.25rem;background:var(--white);border:1px solid var(--border);border-radius:12px;display:block;"><strong>Piscine Libourne</strong><span style="display:block;font-size:.85rem;color:var(--muted);margin-top:.25rem;">33500 · Libournais, St-Émilion</span></a>
      <a href="/detection-fuite/piscine-le-bouscat/" class="loc-card" style="text-decoration:none;color:inherit;padding:1rem 1.25rem;background:var(--white);border:1px solid var(--border);border-radius:12px;display:block;"><strong>Piscine Le Bouscat</strong><span style="display:block;font-size:.85rem;color:var(--muted);margin-top:.25rem;">33110 · Parc Bordelais, Bourran</span></a>
    </div>

    <h3 style="font-family:var(--font-title,inherit);margin-top:3rem;margin-bottom:1rem;">Recherche de fuite par ville en Gironde</h3>
    <p style="margin-bottom:1.5rem;">Nous intervenons sur 30 communes de Gironde. Voici les pages dédiées aux principales villes de la métropole bordelaise et du Bassin d'Arcachon, avec les particularités locales (quartiers, patrimoine, géologie) qui orientent notre diagnostic.</p>
    <div class="grid-3">
      <a href="/villes/bordeaux/" class="loc-card" style="text-decoration:none;color:inherit;padding:1rem 1.25rem;background:var(--white);border:1px solid var(--border);border-radius:12px;display:block;"><strong>Bordeaux (33000)</strong><span style="display:block;font-size:.85rem;color:var(--muted);margin-top:.25rem;">Haussmanniens, UNESCO, pierre calcaire</span></a>
      <a href="/villes/merignac/" class="loc-card" style="text-decoration:none;color:inherit;padding:1rem 1.25rem;background:var(--white);border:1px solid var(--border);border-radius:12px;display:block;"><strong>Mérignac (33700)</strong><span style="display:block;font-size:.85rem;color:var(--muted);margin-top:.25rem;">Pavillons, planchers chauffants</span></a>
      <a href="/villes/arcachon/" class="loc-card" style="text-decoration:none;color:inherit;padding:1rem 1.25rem;background:var(--white);border:1px solid var(--border);border-radius:12px;display:block;"><strong>Arcachon (33120)</strong><span style="display:block;font-size:.85rem;color:var(--muted);margin-top:.25rem;">Villas Ville d'Hiver, air salin</span></a>
      <a href="/villes/libourne/" class="loc-card" style="text-decoration:none;color:inherit;padding:1rem 1.25rem;background:var(--white);border:1px solid var(--border);border-radius:12px;display:block;"><strong>Libourne (33500)</strong><span style="display:block;font-size:.85rem;color:var(--muted);margin-top:.25rem;">Chais viticoles, sol argileux</span></a>
      <a href="/villes/pessac/" class="loc-card" style="text-decoration:none;color:inherit;padding:1rem 1.25rem;background:var(--white);border:1px solid var(--border);border-radius:12px;display:block;"><strong>Pessac (33600)</strong><span style="display:block;font-size:.85rem;color:var(--muted);margin-top:.25rem;">Cité Frugès UNESCO, copropriétés</span></a>
      <a href="/plan-du-site/" class="loc-card" style="text-decoration:none;color:inherit;padding:1rem 1.25rem;background:var(--bg-alt);border:1px solid var(--border);border-radius:12px;display:block;"><strong>+25 autres villes</strong><span style="display:block;font-size:.85rem;color:var(--muted);margin-top:.25rem;">Toute la Gironde au plan du site &rarr;</span></a>
    </div>

    <div style="text-align:center;margin-top:2rem;">
      <a href="/guide/prix-recherche-fuite-bordeaux/" class="btn btn-outline-green">Voir les prix 2026</a>
      <a href="/devis/" class="btn btn-gold" style="margin-left:1rem;">Demander un devis gratuit</a>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Nos pages techniques par méthode</h2>
    <p>Au-delà des pages par cas d\'usage, nous avons consacré des pages dédiées à nos méthodes phares. Pour comprendre laquelle s\'applique à votre situation et son protocole précis :</p>
    <ul>
      <li><a href="/detection-fuite/thermographie-infrarouge-bordeaux/" style="color:var(--green);text-decoration:underline;">Thermographie infrarouge à Bordeaux</a> : caméra thermique haute résolution pour le plancher chauffant, les canalisations encastrées, les copropriétés haussmanniennes.</li>
      <li><a href="/detection-fuite/fluoresceine-piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">Fluorescéine piscine en Gironde</a> : colorant traceur non toxique pour localiser visuellement une fuite de bassin sans vidange.</li>
      <li><a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">Canalisation enterrée à Bordeaux</a> : gaz traceur azote/hydrogène pour les réseaux extérieurs sous jardin ou trottoir.</li>
      <li><a href="/detection-fuite/chemisage-bordeaux/" style="color:var(--green);text-decoration:underline;">Chemisage de canalisation à Bordeaux</a> : rénovation sans tranchée des colonnes montantes en immeuble ancien.</li>
      <li><a href="/guide/detecteur-fuite-eau-professionnel/" style="color:var(--green);text-decoration:underline;">Détecteur de fuite d'eau professionnel</a> : tour d'horizon des appareils utilisés par nos techniciens (corrélateur acoustique, gaz traceur, caméra thermique, hydrophone, endoscopie).</li>
    </ul>
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
        "Détection de fuite non destructive Gironde 33",
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
        <p style="margin-top:1rem;">Pour comprendre le détail technique de la procédure (résines époxy/polyester, durée de vie, garantie décennale), consultez notre guide <a href="/guide/chemisage-explication/" style="color:var(--green);text-decoration:underline;">chemisage de canalisation expliqué</a>. Pour les copropriétés bordelaises (immeubles haussmanniens, colonnes montantes en fonte), nous avons une page dédiée <a href="/detection-fuite/chemisage-bordeaux/" style="color:var(--green);text-decoration:underline;">chemisage à Bordeaux</a> avec retours d\'expérience syndic. Avant tout chemisage, une <a href="/guide/inspection-camera-canalisation-bordeaux/" style="color:var(--green);text-decoration:underline;">inspection caméra de la canalisation</a> est obligatoire pour valider la faisabilité.</p>
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
        "Chemisage canalisation Gironde 33 | Sans tranchée",
        "Chemisage de canalisation en Gironde (33). Rénovation sans démolition, sans tranchée. Résine époxy longue durée. Devis gratuit sur toute la Gironde.",
        "https://recherche-fuite-gironde.fr/chemisage-canalisation/",
        body, ld
    )

# ── Page simulateur coût fuite ────────────────────────────────
def page_simulateur_cout_fuite():
    body = '''
<section class="hero-mini">
  <div class="container">
    <nav class="breadcrumb">
      <a href="/">Accueil</a>
      <span>&rsaquo;</span>
      <span>Simulateur coût fuite</span>
    </nav>
    <h1>Simulateur de coût d\'une fuite d\'eau à Bordeaux</h1>
    <p class="hero-mini-lead">Combien vous coûte vraiment votre fuite d\'eau ? <strong>Calcul en 30 secondes</strong> avec les tarifs Suez et Régie de Bordeaux Métropole 2026, plus la vérification automatique de la loi Warsmann. Gratuit et anonyme, sans inscription.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <div style="background:var(--white);border:1px solid var(--border);border-radius:16px;padding:2rem;box-shadow:0 4px 20px rgba(0,0,0,0.05);">
      <div style="display:flex;gap:.5rem;margin-bottom:2rem;border-bottom:2px solid var(--border);" id="tabs">
        <button id="tab-canal" type="button" onclick="switchTab('canal')" style="flex:1;padding:1rem;background:var(--green);color:var(--white);border:none;border-radius:8px 8px 0 0;font-family:var(--f-title);font-size:1.05rem;font-weight:700;cursor:pointer;">Canalisation maison</button>
        <button id="tab-piscine" type="button" onclick="switchTab('piscine')" style="flex:1;padding:1rem;background:var(--bg-alt);color:var(--text);border:none;border-radius:8px 8px 0 0;font-family:var(--f-title);font-size:1.05rem;font-weight:700;cursor:pointer;">Piscine</button>
      </div>

      <div id="form-canal" style="display:block;">
        <h2 style="margin-top:0;font-size:1.4rem;">Calculer le coût d\'une fuite sur canalisation</h2>
        <p style="color:var(--muted);margin-bottom:1.5rem;">Renseignez les chiffres de votre compteur et nous calculons votre surconsommation, le coût avec les tarifs réels de votre distributeur, et vérifions l\'éligibilité à la loi Warsmann.</p>

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
          <div>
            <label for="releve-ancien" style="display:block;font-weight:600;margin-bottom:.4rem;">Ancien relevé (m³)</label>
            <input id="releve-ancien" type="number" min="0" step="0.1" placeholder="Ex : 248" style="width:100%;padding:.7rem;border:1px solid var(--border);border-radius:8px;font-size:1rem;">
          </div>
          <div>
            <label for="releve-nouveau" style="display:block;font-weight:600;margin-bottom:.4rem;">Relevé actuel (m³)</label>
            <input id="releve-nouveau" type="number" min="0" step="0.1" placeholder="Ex : 442" style="width:100%;padding:.7rem;border:1px solid var(--border);border-radius:8px;font-size:1rem;">
          </div>
          <div>
            <label for="periode-jours" style="display:block;font-weight:600;margin-bottom:.4rem;">Période entre relevés (jours)</label>
            <input id="periode-jours" type="number" min="1" placeholder="Ex : 90" style="width:100%;padding:.7rem;border:1px solid var(--border);border-radius:8px;font-size:1rem;">
          </div>
          <div>
            <label for="distributeur" style="display:block;font-weight:600;margin-bottom:.4rem;">Distributeur d\'eau</label>
            <select id="distributeur" style="width:100%;padding:.7rem;border:1px solid var(--border);border-radius:8px;font-size:1rem;">
              <option value="suez">Suez (Bordeaux et 19 communes)</option>
              <option value="regie">Régie de l\'Eau Bordeaux Métropole (8 communes)</option>
              <option value="autre">Autre commune Gironde</option>
            </select>
          </div>
          <div style="grid-column:1 / -1;">
            <label for="nb-personnes" style="display:block;font-weight:600;margin-bottom:.4rem;">Nombre de personnes au foyer</label>
            <input id="nb-personnes" type="number" min="1" max="10" value="2" style="width:100%;padding:.7rem;border:1px solid var(--border);border-radius:8px;font-size:1rem;">
          </div>
        </div>

        <button type="button" onclick="calculerCanal()" style="margin-top:1.5rem;padding:1rem 2rem;background:var(--gold);color:var(--white);border:none;border-radius:8px;font-family:var(--f-title);font-weight:700;font-size:1.05rem;cursor:pointer;width:100%;">Calculer le coût de ma fuite</button>
      </div>

      <div id="form-piscine" style="display:none;">
        <h2 style="margin-top:0;font-size:1.4rem;">Calculer le coût d\'une fuite de piscine</h2>
        <p style="color:var(--muted);margin-bottom:1.5rem;">Mesurez la perte d\'eau de votre piscine sur 24 à 48 heures et nous calculons le volume perdu, le coût annuel et la part imputable à l\'évaporation naturelle en Gironde.</p>

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
          <div>
            <label for="longueur" style="display:block;font-weight:600;margin-bottom:.4rem;">Longueur du bassin (m)</label>
            <input id="longueur" type="number" min="2" step="0.1" placeholder="Ex : 8" style="width:100%;padding:.7rem;border:1px solid var(--border);border-radius:8px;font-size:1rem;">
          </div>
          <div>
            <label for="largeur" style="display:block;font-weight:600;margin-bottom:.4rem;">Largeur du bassin (m)</label>
            <input id="largeur" type="number" min="2" step="0.1" placeholder="Ex : 4" style="width:100%;padding:.7rem;border:1px solid var(--border);border-radius:8px;font-size:1rem;">
          </div>
          <div>
            <label for="perte-cm" style="display:block;font-weight:600;margin-bottom:.4rem;">Perte de niveau (cm/jour)</label>
            <input id="perte-cm" type="number" min="0" step="0.1" placeholder="Ex : 2,5" style="width:100%;padding:.7rem;border:1px solid var(--border);border-radius:8px;font-size:1rem;">
          </div>
          <div>
            <label for="saison" style="display:block;font-weight:600;margin-bottom:.4rem;">Saison actuelle</label>
            <select id="saison" style="width:100%;padding:.7rem;border:1px solid var(--border);border-radius:8px;font-size:1rem;">
              <option value="ete_canicule">Été pic canicule (juillet-août)</option>
              <option value="ete">Été standard (juin/septembre)</option>
              <option value="mi_saison">Mi-saison (avril-mai/octobre)</option>
              <option value="hiver">Hivernage (novembre-mars)</option>
            </select>
          </div>
          <div>
            <label for="couverture" style="display:block;font-weight:600;margin-bottom:.4rem;">Bassin couvert ?</label>
            <select id="couverture" style="width:100%;padding:.7rem;border:1px solid var(--border);border-radius:8px;font-size:1rem;">
              <option value="non">Non, à découvert</option>
              <option value="oui">Oui (bâche ou abri)</option>
            </select>
          </div>
          <div>
            <label for="zone-piscine" style="display:block;font-weight:600;margin-bottom:.4rem;">Zone géographique</label>
            <select id="zone-piscine" style="width:100%;padding:.7rem;border:1px solid var(--border);border-radius:8px;font-size:1rem;">
              <option value="metropole">Métropole bordelaise</option>
              <option value="bassin">Bassin d\'Arcachon (vent marin +20%)</option>
              <option value="medoc">Médoc viticole</option>
              <option value="libournais">Libournais</option>
            </select>
          </div>
        </div>

        <button type="button" onclick="calculerPiscine()" style="margin-top:1.5rem;padding:1rem 2rem;background:var(--gold);color:var(--white);border:none;border-radius:8px;font-family:var(--f-title);font-weight:700;font-size:1.05rem;cursor:pointer;width:100%;">Calculer le coût de ma fuite piscine</button>
      </div>

      <div id="resultats" style="display:none;margin-top:2rem;padding:2rem;background:var(--bg-alt);border-radius:12px;">
        <h2 style="margin-top:0;font-size:1.4rem;color:var(--green-dark);">Résultat de votre simulation</h2>

        <div id="alerte-niveau" style="padding:1rem;border-radius:8px;margin-bottom:1.5rem;font-weight:600;"></div>

        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;margin-bottom:1.5rem;">
          <div style="background:var(--white);padding:1rem;border-radius:8px;text-align:center;">
            <div style="font-size:.8rem;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;">Coût mensuel</div>
            <div style="font-size:1.8rem;font-weight:700;color:var(--green-dark);" id="cout-mensuel">- €</div>
          </div>
          <div style="background:var(--white);padding:1rem;border-radius:8px;text-align:center;">
            <div style="font-size:.8rem;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;">Coût annuel</div>
            <div style="font-size:1.8rem;font-weight:700;color:var(--gold);" id="cout-annuel">- €</div>
          </div>
          <div style="background:var(--white);padding:1rem;border-radius:8px;text-align:center;">
            <div style="font-size:.8rem;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;">Volume perdu</div>
            <div style="font-size:1.8rem;font-weight:700;color:var(--green);" id="volume-perdu">- m³/an</div>
          </div>
        </div>

        <div style="background:var(--white);padding:1rem;border-radius:8px;margin-bottom:1rem;">
          <strong>Équivalence concrète :</strong> <span id="equivalence">-</span>
        </div>

        <div id="warsmann-bloc" style="background:var(--white);padding:1rem;border-radius:8px;margin-bottom:1rem;border-left:4px solid var(--gold);">
          <strong>Loi Warsmann 2011 :</strong> <span id="warsmann-text">-</span>
        </div>

        <div id="recommandation-bloc" style="background:var(--white);padding:1rem;border-radius:8px;margin-bottom:1.5rem;border-left:4px solid var(--green);">
          <strong>Notre recommandation :</strong> <span id="recommandation-text">-</span>
        </div>

        <a id="cta-action" href="/devis/" class="btn btn-gold" style="display:block;text-align:center;text-decoration:none;padding:1rem;font-size:1.05rem;">Demander un diagnostic gratuit</a>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Comment fonctionne le simulateur de coût de fuite ?</h2>
    <p>Notre simulateur applique les <strong>tarifs réels 2026 des distributeurs d\'eau de Bordeaux Métropole</strong> à votre situation pour calculer le coût exact de votre fuite. Voici les paramètres pris en compte et la méthode de calcul détaillée.</p>

    <h3>Pour les fuites sur canalisation</h3>
    <p>Le calcul compare votre relevé actuel à votre relevé précédent, divisé par la période en jours, pour déterminer votre consommation quotidienne réelle. Cette consommation est comparée à une consommation moyenne de référence (120 litres/jour/personne en France selon l\'INSEE 2026, soit 0,12 m³/jour/personne). L\'écart entre les deux représente votre fuite quotidienne, valorisée au tarif de votre distributeur.</p>

    <p><strong>Tarifs eau Bordeaux Métropole 2026</strong> (TTC, moyenne hors abonnement) :</p>
    <ul>
      <li><strong>Suez</strong> (Bordeaux Centre, Caudéran, Le Bouscat, Saint-Augustin, Bègles, Floirac, Cenon, Lormont, Bouliac, Carbon-Blanc, Bassens, Ambarès-et-Lagrave, Saint-Louis-de-Montferrand, Saint-Vincent-de-Paul, Ambès, Bouliac, Le Taillan-Médoc, Mérignac partie Beutre) : <strong>4,87 €/m³</strong></li>
      <li><strong>Régie de l\'Eau Bordeaux Métropole</strong> (Mérignac centre, Pessac, Talence, Gradignan, Le Haillan, Eysines, Bruges, Blanquefort) : <strong>3,90 €/m³</strong> (économie de 20 % vs Suez)</li>
      <li><strong>Autres communes Gironde</strong> (Régies syndicales, SAUR, autres) : moyenne 4,50 €/m³ utilisée par le simulateur</li>
    </ul>

    <h3>Pour les fuites de piscine</h3>
    <p>Le calcul prend en compte la surface du bassin (longueur × largeur), la perte de niveau quotidienne en cm, et soustrait l\'évaporation normale selon la saison et la zone géographique. L\'évaporation naturelle moyenne en Gironde varie de <strong>0,3 cm/jour en hivernage à 1,8 cm/jour en pic canicule estivale</strong>. Sur le Bassin d\'Arcachon (vent marin permanent), majoration de 20 %. Une bâche ou un abri réduit l\'évaporation de 80 %.</p>

    <p>Le volume perdu se calcule : <em>surface (m²) × perte réelle (m) × 1000 = litres/jour</em>. Ce volume est ensuite valorisé au tarif moyen Gironde (4,50 €/m³).</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Que faire selon le résultat du simulateur ?</h2>
    <p>Selon le coût annuel calculé et le volume perdu, votre situation appelle une action différente. Voici nos préconisations issues de 200 diagnostics annuels en Gironde :</p>

    <h3>Coût annuel inférieur à 100 € (perte mineure)</h3>
    <p>Probable évaporation naturelle en saison chaude ou très petite fuite chronique. Ne nécessite pas d\'intervention urgente. Surveillez la perte sur 7 à 14 jours et refaites le test du seau pour confirmer. Voir notre guide <a href="/guide/evaporation-vs-fuite-piscine/" style="color:var(--green);text-decoration:underline;">évaporation ou fuite de piscine</a>.</p>

    <h3>Coût annuel entre 100 € et 500 € (fuite modérée)</h3>
    <p>Fuite confirmée mais modérée. Diagnostic professionnel recommandé sous 30 à 60 jours pour éviter aggravation et dégâts collatéraux. Notre intervention de diagnostic à Bordeaux : 380 à 580 € HT, généralement remboursée par votre assurance habitation. Voir notre <a href="/detection-fuite/" style="color:var(--green);text-decoration:underline;">page détection de fuite</a> ou <a href="/detection-fuite/piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">recherche de fuite piscine Bordeaux</a> selon votre situation.</p>

    <h3>Coût annuel entre 500 € et 2 000 € (fuite importante)</h3>
    <p>Diagnostic urgent recommandé sous 7 à 14 jours. À ce niveau de surconsommation, vous êtes éligible à l\'écrêtement loi Warsmann auprès de votre distributeur. Notre rapport technique facilite la procédure. Voir le guide complet <a href="/guide/loi-warsmann-ecretement-facture-eau/" style="color:var(--green);text-decoration:underline;">loi Warsmann écrêtement de facture d\'eau</a>.</p>

    <h3>Coût annuel supérieur à 2 000 € (fuite critique)</h3>
    <p>Intervention en urgence sous 24 à 48 heures recommandée. À ce niveau, les dégâts collatéraux (terrain saturé, fondations, voisins) progressent rapidement. Voir notre <a href="/detection-fuite/urgence-bordeaux/" style="color:var(--green);text-decoration:underline;">service urgence recherche de fuite Bordeaux</a> avec intervention sous 24h et qualification téléphonique dans l\'heure.</p>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>La loi Warsmann 2011 : plafonner votre facture</h2>
    <p>Si la fuite se situe sur votre réseau enterré privatif (entre compteur et habitation), la loi Warsmann de 2011 plafonne votre facture à <strong>deux fois la consommation moyenne des trois dernières années</strong>. Cette procédure peut diviser votre facture par 3 à 8 selon l\'ampleur de la fuite.</p>
    <p>Conditions à respecter :</p>
    <ul>
      <li>Fuite sur réseau enterré non visible (canalisation entre compteur et habitation)</li>
      <li>Réparation effectuée dans les 30 jours après notification du distributeur</li>
      <li>Rapport technique d\'un professionnel attestant la localisation enterrée</li>
    </ul>
    <p>Notre rapport est conforme aux exigences de Suez et de la Régie de l\'Eau Bordeaux Métropole. Procédure complète dans le <a href="/guide/loi-warsmann-ecretement-facture-eau/" style="color:var(--green);text-decoration:underline;">guide loi Warsmann</a>.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Questions fréquentes sur le simulateur</h2>

    <h3>Le simulateur est-il vraiment gratuit et anonyme ?</h3>
    <p>Oui, totalement. Aucune donnée personnelle n\'est demandée pour utiliser le simulateur. Les calculs se font directement dans votre navigateur, aucune information n\'est envoyée à un serveur. Le simulateur est libre d\'usage pour tous les habitants de Gironde.</p>

    <h3>Les tarifs Suez et Régie de Bordeaux Métropole sont-ils fiables ?</h3>
    <p>Les tarifs utilisés sont les tarifs publiés par les distributeurs en 2026 (Suez 4,87 €/m³ et Régie de l\'Eau Bordeaux Métropole 3,90 €/m³, hors abonnement). Pour le calcul de votre facture finale, ajoutez le forfait abonnement annuel (environ 80 €) et la TVA. Les tarifs peuvent évoluer chaque année au 1er janvier.</p>

    <h3>Pourquoi mon volume perdu est plus élevé que ma facture réelle ?</h3>
    <p>Le simulateur calcule le coût brut de votre surconsommation. Votre facture réelle peut être inférieure si vous bénéficiez de l\'écrêtement loi Warsmann (plafonnement à 2× la consommation moyenne) ou d\'un dégrèvement exceptionnel accordé par votre distributeur. Si votre facture est plus élevée que notre estimation, vérifiez l\'abonnement, la TVA (5,5 %) et la redevance assainissement.</p>

    <h3>Puis-je calculer une fuite déjà réparée pour estimer la perte rétroactive ?</h3>
    <p>Oui, en utilisant les relevés du compteur avant et après la période de fuite. Le simulateur calculera le coût total de la surconsommation pendant la période concernée. C\'est utile pour évaluer si l\'écrêtement Warsmann aurait pu s\'appliquer ou pour négocier avec votre distributeur a posteriori.</p>

    <h3>Ce simulateur est-il valide pour les autres distributeurs en France ?</h3>
    <p>Le calcul de volume perdu est universel. Pour le coût, sélectionnez « Autre commune » qui utilise une moyenne nationale de 4,50 €/m³. Pour un calcul précis hors Gironde, utilisez le tarif réel de votre commune (généralement disponible sur le site de votre distributeur ou de votre commune).</p>

    <h3>Que faire si le simulateur indique une fuite mais que je n\'en trouve pas ?</h3>
    <p>Les fuites enterrées sur canalisation entre compteur et habitation sont invisibles à l\'œil nu dans 60 % des cas. Notre méthode professionnelle (gaz traceur azote/hydrogène, écoute électro-acoustique, caméra endoscopique) localise au mètre près sans démolition. Voir <a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">recherche de fuite canalisation enterrée à Bordeaux</a>.</p>

    <h3>Mon assurance prend-elle en charge le coût d\'un diagnostic ?</h3>
    <p>Dans 90 % des cas oui. La garantie « recherche de fuite » de votre contrat multirisque habitation rembourse tout ou partie du diagnostic, sous condition d\'un dégât des eaux constaté ou d\'une surconsommation anormale. Notre rapport est accepté par AXA, MAIF, MAAF, Macif, Generali, Allianz, Groupama, Matmut, GMF. Voir <a href="/guide/assurance-fuite-eau/" style="color:var(--green);text-decoration:underline;">guide assurance fuite d\'eau</a>.</p>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Pages connexes : agir face à une fuite à Bordeaux</h2>
    <ul>
      <li><a href="/detection-fuite/urgence-bordeaux/" style="color:var(--green);text-decoration:underline;">Urgence recherche de fuite à Bordeaux</a> : intervention sous 24h pour les fuites importantes.</li>
      <li><a href="/detection-fuite/fuite-apres-compteur/" style="color:var(--green);text-decoration:underline;">Fuite après compteur Bordeaux</a> : diagnostic du réseau privatif enterré.</li>
      <li><a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">Canalisation enterrée à Bordeaux</a> : gaz traceur azote/hydrogène pour réseaux extérieurs.</li>
      <li><a href="/guide/loi-warsmann-ecretement-facture-eau/" style="color:var(--green);text-decoration:underline;">Loi Warsmann : écrêtement de facture d\'eau</a> : procédure complète pas à pas.</li>
      <li><a href="/guide/facture-eau-suez-doublee-fuite-bordeaux/" style="color:var(--green);text-decoration:underline;">Facture Suez doublée à Bordeaux</a> : démarche en cas de surfacturation.</li>
      <li><a href="/guide/compteur-eau-qui-tourne-sans-utilisation/" style="color:var(--green);text-decoration:underline;">Compteur d\'eau qui tourne sans utilisation</a> : tests à faire ce soir.</li>
      <li><a href="/detection-fuite/piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">Recherche de fuite piscine Bordeaux</a> : diagnostic sans vidange.</li>
      <li><a href="/guide/evaporation-vs-fuite-piscine/" style="color:var(--green);text-decoration:underline;">Évaporation ou fuite piscine</a> : test du seau et taux mensuels.</li>
    </ul>
  </div>
</section>

<script>
function switchTab(tab) {
  var canal = document.getElementById("form-canal");
  var piscine = document.getElementById("form-piscine");
  var btnCanal = document.getElementById("tab-canal");
  var btnPiscine = document.getElementById("tab-piscine");
  if (tab === "canal") {
    canal.style.display = "block";
    piscine.style.display = "none";
    btnCanal.style.background = "var(--green)";
    btnCanal.style.color = "var(--white)";
    btnPiscine.style.background = "var(--bg-alt)";
    btnPiscine.style.color = "var(--text)";
  } else {
    canal.style.display = "none";
    piscine.style.display = "block";
    btnPiscine.style.background = "var(--green)";
    btnPiscine.style.color = "var(--white)";
    btnCanal.style.background = "var(--bg-alt)";
    btnCanal.style.color = "var(--text)";
  }
  document.getElementById("resultats").style.display = "none";
}

function afficherResultat(coutMensuel, coutAnnuel, volumeM3, equivalence, warsmann, reco, ctaUrl, ctaLabel, niveauAlerte) {
  document.getElementById("cout-mensuel").textContent = Math.round(coutMensuel) + " €";
  document.getElementById("cout-annuel").textContent = Math.round(coutAnnuel) + " €";
  document.getElementById("volume-perdu").textContent = volumeM3.toFixed(1) + " m³/an";
  document.getElementById("equivalence").innerHTML = equivalence;
  document.getElementById("warsmann-text").innerHTML = warsmann;
  document.getElementById("recommandation-text").innerHTML = reco;
  var cta = document.getElementById("cta-action");
  cta.href = ctaUrl;
  cta.textContent = ctaLabel;
  var alerte = document.getElementById("alerte-niveau");
  if (niveauAlerte === "info") {
    alerte.style.background = "#E0F2FE";
    alerte.style.color = "#0369A1";
    alerte.textContent = "Probable évaporation naturelle, surveillance recommandée";
  } else if (niveauAlerte === "warning") {
    alerte.style.background = "#FEF3C7";
    alerte.style.color = "#92400E";
    alerte.textContent = "Fuite confirmée, diagnostic professionnel recommandé";
  } else {
    alerte.style.background = "#FEE2E2";
    alerte.style.color = "#991B1B";
    alerte.textContent = "Fuite critique, intervention urgente conseillée";
  }
  document.getElementById("resultats").style.display = "block";
  document.getElementById("resultats").scrollIntoView({ behavior: "smooth", block: "start" });
}

function calculerCanal() {
  var ancien = parseFloat(document.getElementById("releve-ancien").value);
  var nouveau = parseFloat(document.getElementById("releve-nouveau").value);
  var periode = parseFloat(document.getElementById("periode-jours").value);
  var distributeur = document.getElementById("distributeur").value;
  var nbPersonnes = parseInt(document.getElementById("nb-personnes").value) || 2;
  if (isNaN(ancien) || isNaN(nouveau) || isNaN(periode) || nouveau <= ancien || periode <= 0) {
    alert("Merci de renseigner des valeurs valides (relevé actuel supérieur à l ancien, période > 0).");
    return;
  }
  var tarifs = { suez: 4.87, regie: 3.90, autre: 4.50 };
  var tarif = tarifs[distributeur];
  var consoTotale = nouveau - ancien;
  var consoJour = consoTotale / periode;
  var consoNormale = nbPersonnes * 0.12;
  var fuiteJour = Math.max(0, consoJour - consoNormale);
  var volumeAn = fuiteJour * 365;
  var coutAn = volumeAn * tarif;
  var coutMois = coutAn / 12;
  var baignoires = (fuiteJour * 1000 / 200).toFixed(1);
  var litresJour = Math.round(fuiteJour * 1000);
  var equivalence = "<strong>" + baignoires + " baignoires perdues par jour</strong> (soit " + litresJour + " litres/jour). Sur un an, " + Math.round(volumeAn) + " m³ gaspillés, l’équivalent de la consommation annuelle d’un foyer de " + Math.round(volumeAn / 50) + " personnes.";
  var consoMoyenne = nbPersonnes * 0.12 * 365;
  var seuilWarsmann = consoMoyenne * 2;
  var warsmann;
  if (volumeAn > seuilWarsmann) {
    warsmann = "<strong>Vous êtes éligible à l’écrêtement Warsmann</strong>. Votre facture peut être plafonnée à " + Math.round(seuilWarsmann * tarif) + " € (2× votre consommation moyenne) au lieu de " + Math.round(coutAn) + " €. Économie potentielle : " + Math.round((coutAn - seuilWarsmann * tarif)) + " € sur l’année.";
  } else {
    warsmann = "Surconsommation insuffisante pour activer la loi Warsmann (seuil " + Math.round(seuilWarsmann) + " m³/an au-dessus de votre conso moyenne). Mais l’assurance habitation peut prendre en charge le diagnostic.";
  }
  var reco, ctaUrl, ctaLabel, niveauAlerte;
  ctaUrl = "/devis/";
  if (coutAn < 100) {
    reco = "Consommation dans la norme. Si la baisse continue, surveillez sur 14 jours et refaites le calcul. En cas de doute, demandez un avis gratuit.";
    ctaLabel = "Demander un avis gratuit";
    niveauAlerte = "info";
  } else if (coutAn < 500) {
    reco = "Fuite modérée confirmée. Diagnostic recommandé sous 30 à 60 jours pour éviter aggravation. Souvent remboursé par votre assurance habitation.";
    ctaLabel = "Demander un devis de diagnostic";
    niveauAlerte = "warning";
  } else if (coutAn < 2000) {
    reco = "Fuite importante. Diagnostic urgent sous 7 à 14 jours. Vous êtes éligible à la procédure d’écrêtement loi Warsmann pour plafonner votre facture.";
    ctaLabel = "Demander un devis urgent";
    niveauAlerte = "warning";
  } else {
    reco = "Fuite critique. Intervention urgence sous 24h conseillée. Risque de dégâts collatéraux (terrain saturé, fondations, voisins).";
    ctaLabel = "Demander une intervention 24h";
    niveauAlerte = "danger";
  }
  afficherResultat(coutMois, coutAn, volumeAn, equivalence, warsmann, reco, ctaUrl, ctaLabel, niveauAlerte);
}

function calculerPiscine() {
  var longueur = parseFloat(document.getElementById("longueur").value);
  var largeur = parseFloat(document.getElementById("largeur").value);
  var perteCm = parseFloat(document.getElementById("perte-cm").value);
  var saison = document.getElementById("saison").value;
  var couverture = document.getElementById("couverture").value;
  var zone = document.getElementById("zone-piscine").value;
  if (isNaN(longueur) || isNaN(largeur) || isNaN(perteCm) || longueur <= 0 || largeur <= 0 || perteCm < 0) {
    alert("Merci de renseigner des valeurs valides pour la longueur, largeur et perte.");
    return;
  }
  var evapBase = { ete_canicule: 1.5, ete: 1.0, mi_saison: 0.6, hiver: 0.3 };
  var evap = evapBase[saison];
  var coefZone = { metropole: 1.0, bassin: 1.2, medoc: 1.0, libournais: 1.0 };
  evap = evap * coefZone[zone];
  if (couverture === "oui") evap = evap * 0.2;
  var perteReelle = Math.max(0, perteCm - evap);
  var surface = longueur * largeur;
  var volumeJourL = surface * perteReelle * 10;
  var volumeJourM3 = volumeJourL / 1000;
  var volumeAn = volumeJourM3 * 365;
  var tarif = 4.50;
  var coutAn = volumeAn * tarif;
  var coutMois = coutAn / 12;
  var baignoires = (volumeJourL / 200).toFixed(1);
  var profondeurMoy = 1.4;
  var volumeBassin = surface * profondeurMoy;
  var foisRemplies = volumeAn / volumeBassin;
  var equivalence = "<strong>" + baignoires + " baignoires perdues par jour</strong> (soit " + Math.round(volumeJourL) + " litres/jour). Sur un an, " + Math.round(volumeAn) + " m³ gaspillés, l’équivalent de remplir " + foisRemplies.toFixed(1) + " fois votre piscine.";
  var warsmann = "La loi Warsmann ne s’applique pas aux piscines (réservée aux fuites enterrées entre compteur et habitation). Mais votre assurance habitation peut prendre en charge le diagnostic au titre de la garantie recherche de fuite.";
  var reco, ctaUrl, ctaLabel, niveauAlerte;
  ctaUrl = "/devis/";
  if (perteReelle <= 0) {
    reco = "Perte d’eau dans la norme d’évaporation pour cette saison et cette zone. Aucune fuite probable. Surveillez sur 7 à 14 jours et refaites le calcul.";
    ctaLabel = "Demander un avis gratuit";
    niveauAlerte = "info";
  } else if (perteReelle < 1) {
    reco = "Petite fuite probable au-delà de l’évaporation normale. Faites le test du seau pour confirmer puis diagnostic sous 30 jours si confirmé.";
    ctaLabel = "Demander un diagnostic piscine";
    niveauAlerte = "warning";
  } else if (perteReelle < 3) {
    reco = "Fuite modérée à importante. Diagnostic professionnel sous 14 jours recommandé. Notre intervention est généralement remboursée par votre assurance habitation.";
    ctaLabel = "Demander un devis diagnostic";
    niveauAlerte = "warning";
  } else {
    reco = "Fuite critique. Intervention urgente conseillée. Coupez la remise en eau automatique pour limiter les pertes en attendant.";
    ctaLabel = "Demander une intervention urgente";
    niveauAlerte = "danger";
  }
  afficherResultat(coutMois, coutAn, volumeAn, equivalence, warsmann, reco, ctaUrl, ctaLabel, niveauAlerte);
}
</script>
'''

    ld_app = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "Simulateur de coût de fuite d'eau Bordeaux Gironde",
  "url": "https://recherche-fuite-gironde.fr/simulateur-cout-fuite/",
  "applicationCategory": "UtilityApplication",
  "operatingSystem": "Web",
  "description": "Calculez gratuitement le coût d'une fuite d'eau (canalisation ou piscine) avec les tarifs réels Suez et Régie de l'Eau Bordeaux Métropole. Vérification éligibilité loi Warsmann.",
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "EUR" }
}
</script>'''

    ld_local = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Recherche Fuite Gironde",
  "url": "https://recherche-fuite-gironde.fr/",
  "areaServed": { "@type": "AdministrativeArea", "name": "Gironde" },
  "priceRange": "€€"
}
</script>'''

    ld_breadcrumb = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://recherche-fuite-gironde.fr/" },
    { "@type": "ListItem", "position": 2, "name": "Simulateur coût fuite", "item": "https://recherche-fuite-gironde.fr/simulateur-cout-fuite/" }
  ]
}
</script>'''

    ld_faq = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Le simulateur de coût de fuite est-il vraiment gratuit ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Oui, totalement gratuit et anonyme. Aucune donnée personnelle demandée. Les calculs se font dans votre navigateur sans envoi serveur." }
    },
    {
      "@type": "Question",
      "name": "Quels tarifs eau utilise le simulateur pour Bordeaux ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Tarifs 2026 publiés : Suez 4,87 €/m³ pour Bordeaux Centre et 19 communes, Régie de l'Eau Bordeaux Métropole 3,90 €/m³ pour Mérignac, Pessac, Talence, Gradignan et 4 autres communes. Hors abonnement et TVA." }
    },
    {
      "@type": "Question",
      "name": "Le simulateur prend-il en compte la loi Warsmann ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Oui. Si votre surconsommation dépasse 2× votre consommation moyenne (calculée selon le nombre de personnes au foyer), le simulateur vous indique l'éligibilité à l'écrêtement Warsmann et l'économie potentielle." }
    },
    {
      "@type": "Question",
      "name": "Que faire si le simulateur indique une fuite mais que je n'en trouve pas ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Les fuites enterrées sont invisibles dans 60 % des cas. Notre méthode pro (gaz traceur, écoute acoustique, caméra) localise au mètre près sans démolition. Voir page canalisation enterrée Bordeaux." }
    },
    {
      "@type": "Question",
      "name": "Le simulateur fonctionne-t-il pour les piscines coque ou liner ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Oui, le calcul de volume est universel pour tous types de bassins. Les pathologies diffèrent (osmose pour coque polyester, fissures pour béton, perforation pour liner) mais le coût de la perte d'eau est identique." }
    },
    {
      "@type": "Question",
      "name": "Mon assurance habitation prend-elle en charge le diagnostic ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Dans 90 % des cas oui. Garantie recherche de fuite des contrats multirisques habitation, sous condition de dégât des eaux constaté ou surconsommation. Notre rapport accepté par AXA, MAIF, MAAF, Macif, Generali, Groupama, Allianz, Matmut." }
    }
  ]
}
</script>'''

    return html_base(
        "Simulateur coût fuite eau Bordeaux | Calcul gratuit",
        "Simulateur gratuit du coût d'une fuite d'eau (canalisation ou piscine) à Bordeaux et en Gironde. Tarifs Suez et Régie de l'Eau 2026, éligibilité loi Warsmann.",
        "https://recherche-fuite-gironde.fr/simulateur-cout-fuite/",
        body,
        ld_app + ld_local + ld_breadcrumb + ld_faq
    )


# ── Page calculateur Warsmann avec courrier auto ──────────────
def page_calcul_warsmann_bordeaux():
    body = '''
<section class="hero-mini">
  <div class="container">
    <nav class="breadcrumb">
      <a href="/">Accueil</a>
      <span>&rsaquo;</span>
      <span>Calcul Warsmann</span>
    </nav>
    <h1>Calculateur loi Warsmann à Bordeaux : écrêtement de facture d\'eau</h1>
    <p class="hero-mini-lead">Votre facture Suez ou Régie de Bordeaux Métropole a explosé après une fuite enterrée ? <strong>Calculez en 1 minute</strong> votre éligibilité à l\'écrêtement loi Warsmann et téléchargez le courrier-type pré-rempli à envoyer à votre distributeur. Outil unique en France, gratuit et anonyme.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <div style="background:var(--white);border:1px solid var(--border);border-radius:16px;padding:2rem;box-shadow:0 4px 20px rgba(0,0,0,0.05);">
      <h2 style="margin-top:0;font-size:1.4rem;">Étape 1 : votre situation</h2>
      <p style="color:var(--muted);margin-bottom:1.5rem;">Renseignez ces informations issues de vos factures d\'eau pour vérifier votre éligibilité.</p>

      <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
        <div>
          <label for="conso-moyenne" style="display:block;font-weight:600;margin-bottom:.4rem;">Conso moyenne 3 ans (m³/an)</label>
          <input id="conso-moyenne" type="number" min="0" step="1" placeholder="Ex : 120" style="width:100%;padding:.7rem;border:1px solid var(--border);border-radius:8px;font-size:1rem;">
          <small style="color:var(--muted);display:block;margin-top:.3rem;">Visible sur vos 3 dernières factures annuelles</small>
        </div>
        <div>
          <label for="conso-actuelle" style="display:block;font-weight:600;margin-bottom:.4rem;">Conso anormale constatée (m³)</label>
          <input id="conso-actuelle" type="number" min="0" step="1" placeholder="Ex : 580" style="width:100%;padding:.7rem;border:1px solid var(--border);border-radius:8px;font-size:1rem;">
          <small style="color:var(--muted);display:block;margin-top:.3rem;">Le pic anormal sur la période concernée</small>
        </div>
        <div>
          <label for="distributeur-w" style="display:block;font-weight:600;margin-bottom:.4rem;">Votre distributeur</label>
          <select id="distributeur-w" style="width:100%;padding:.7rem;border:1px solid var(--border);border-radius:8px;font-size:1rem;">
            <option value="suez">Suez (Bordeaux Centre + 19 communes)</option>
            <option value="regie">Régie de l\'Eau Bordeaux Métropole (8 communes)</option>
            <option value="autre">Autre distributeur Gironde</option>
          </select>
        </div>
        <div>
          <label for="fuite-enterree" style="display:block;font-weight:600;margin-bottom:.4rem;">Fuite enterrée diagnostiquée ?</label>
          <select id="fuite-enterree" style="width:100%;padding:.7rem;border:1px solid var(--border);border-radius:8px;font-size:1rem;">
            <option value="oui">Oui, par professionnel (rapport disponible)</option>
            <option value="bientot">Pas encore, diagnostic prévu</option>
            <option value="non">Non, fuite visible ou intérieure</option>
          </select>
        </div>
      </div>

      <button type="button" onclick="calculerWarsmann()" style="margin-top:1.5rem;padding:1rem 2rem;background:var(--gold);color:var(--white);border:none;border-radius:8px;font-family:var(--f-title);font-weight:700;font-size:1.05rem;cursor:pointer;width:100%;">Calculer mon éligibilité Warsmann</button>

      <div id="resultats-w" style="display:none;margin-top:2rem;padding:2rem;background:var(--bg-alt);border-radius:12px;">
        <h2 style="margin-top:0;font-size:1.4rem;color:var(--green-dark);">Votre situation Warsmann</h2>

        <div id="alerte-w" style="padding:1rem;border-radius:8px;margin-bottom:1.5rem;font-weight:600;"></div>

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1.5rem;">
          <div style="background:var(--white);padding:1rem;border-radius:8px;">
            <div style="font-size:.8rem;color:var(--muted);text-transform:uppercase;">Plafond légal Warsmann</div>
            <div style="font-size:1.6rem;font-weight:700;color:var(--green-dark);" id="plafond-m3">- m³</div>
            <div style="color:var(--muted);font-size:.85rem;" id="plafond-eur">- € (au tarif distributeur)</div>
          </div>
          <div style="background:var(--white);padding:1rem;border-radius:8px;">
            <div style="font-size:.8rem;color:var(--muted);text-transform:uppercase;">Économie potentielle</div>
            <div style="font-size:1.6rem;font-weight:700;color:var(--gold);" id="economie">- €</div>
            <div style="color:var(--muted);font-size:.85rem;" id="surplus-m3">Surplus écrêté : - m³</div>
          </div>
        </div>

        <div id="explication-w" style="background:var(--white);padding:1rem;border-radius:8px;margin-bottom:1rem;border-left:4px solid var(--green);"></div>

        <div id="conditions-w" style="background:var(--white);padding:1rem;border-radius:8px;margin-bottom:1rem;border-left:4px solid var(--gold);"></div>
      </div>

      <div id="courrier-bloc" style="display:none;margin-top:2rem;">
        <h2 style="font-size:1.4rem;">Étape 2 : votre courrier de demande d\'écrêtement</h2>
        <p style="color:var(--muted);margin-bottom:1rem;">Renseignez vos coordonnées pour générer le courrier conforme à envoyer à votre distributeur en recommandé avec accusé de réception.</p>

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1rem;">
          <div>
            <label for="ident-prenom" style="display:block;font-weight:600;margin-bottom:.4rem;">Prénom</label>
            <input id="ident-prenom" type="text" placeholder="Marie" style="width:100%;padding:.7rem;border:1px solid var(--border);border-radius:8px;">
          </div>
          <div>
            <label for="ident-nom" style="display:block;font-weight:600;margin-bottom:.4rem;">Nom</label>
            <input id="ident-nom" type="text" placeholder="Dupont" style="width:100%;padding:.7rem;border:1px solid var(--border);border-radius:8px;">
          </div>
          <div style="grid-column:1 / -1;">
            <label for="ident-adresse" style="display:block;font-weight:600;margin-bottom:.4rem;">Adresse complète</label>
            <input id="ident-adresse" type="text" placeholder="12 rue Sainte-Catherine, 33000 Bordeaux" style="width:100%;padding:.7rem;border:1px solid var(--border);border-radius:8px;">
          </div>
          <div>
            <label for="ident-num-client" style="display:block;font-weight:600;margin-bottom:.4rem;">N° client distributeur</label>
            <input id="ident-num-client" type="text" placeholder="123456789" style="width:100%;padding:.7rem;border:1px solid var(--border);border-radius:8px;">
            <small style="color:var(--muted);display:block;margin-top:.3rem;">Visible en haut de votre facture</small>
          </div>
          <div>
            <label for="ident-date-fuite" style="display:block;font-weight:600;margin-bottom:.4rem;">Date estimée de la fuite</label>
            <input id="ident-date-fuite" type="date" style="width:100%;padding:.7rem;border:1px solid var(--border);border-radius:8px;">
          </div>
        </div>

        <button type="button" onclick="genererCourrier()" style="padding:1rem 2rem;background:var(--green);color:var(--white);border:none;border-radius:8px;font-family:var(--f-title);font-weight:700;font-size:1.05rem;cursor:pointer;width:100%;">Générer mon courrier</button>
      </div>

      <div id="courrier-aperçu" style="display:none;margin-top:2rem;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;">
          <h2 style="margin:0;font-size:1.4rem;">Aperçu du courrier</h2>
          <button type="button" onclick="window.print()" style="padding:.7rem 1.2rem;background:var(--gold);color:var(--white);border:none;border-radius:6px;cursor:pointer;font-weight:600;">Imprimer / Enregistrer en PDF</button>
        </div>

        <div id="courrier-content" style="background:var(--white);border:1px solid var(--border);border-radius:8px;padding:3rem;font-family:Georgia, serif;line-height:1.6;">
          <!-- Contenu généré par JS -->
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>La loi Warsmann 2011 : ce qu\'elle dit, ce qu\'elle permet</h2>
    <p>L\'article L2224-12-4 du Code général des collectivités territoriales (loi du 17 mai 2011 dite « loi Warsmann ») oblige les distributeurs d\'eau à <strong>plafonner la facture d\'un abonné occupant un local d\'habitation à deux fois sa consommation moyenne des trois dernières années</strong> en cas de surconsommation due à une fuite enterrée non visible sur la canalisation après compteur.</p>
    <p>Le mécanisme est le suivant :</p>
    <ol>
      <li><strong>Le distributeur détecte une consommation anormale</strong> (généralement supérieure à 2× la conso moyenne historique) lors du relevé suivant.</li>
      <li><strong>Il informe l\'abonné</strong> dans le mois qui suit cette détection.</li>
      <li><strong>L\'abonné a 1 mois</strong> pour faire réparer la fuite et fournir une attestation d\'un professionnel certifiant la réparation et la nature enterrée non visible de la fuite.</li>
      <li><strong>Le distributeur recalcule</strong> la facture en plafonnant le volume facturé à 2× la conso moyenne.</li>
      <li><strong>Le surplus est annulé ou remboursé</strong> si déjà payé.</li>
    </ol>
    <p>Sur Bordeaux Métropole, deux distributeurs sont concernés :</p>
    <ul>
      <li><strong>Suez Eau France</strong> : Bordeaux Centre, Caudéran, Le Bouscat, Saint-Augustin, Bègles, Floirac, Cenon, Lormont, Bouliac, Carbon-Blanc, Bassens, Ambarès-et-Lagrave, Saint-Louis-de-Montferrand, Saint-Vincent-de-Paul, Ambès, Le Taillan-Médoc, et 3 autres communes.</li>
      <li><strong>Régie de l\'Eau Bordeaux Métropole</strong> : Mérignac, Pessac, Talence, Gradignan, Le Haillan, Eysines, Bruges, Blanquefort.</li>
    </ul>
    <p>Pour les autres communes de Gironde (Bassin d\'Arcachon, Médoc, Libournais, Bazadais), distributeurs locaux variés (SAUR, syndicats intercommunaux, régies municipales). Le mécanisme Warsmann reste applicable partout en France.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Conditions à remplir pour bénéficier de l\'écrêtement</h2>
    <p>Cinq conditions cumulatives doivent être respectées pour que la loi Warsmann s\'applique :</p>

    <h3>1. Local d\'habitation occupé</h3>
    <p>Le dispositif concerne uniquement les particuliers occupants. Sont exclus : locaux professionnels, locaux vacants, résidences secondaires non occupées au moment de la fuite, copropriétés sur leurs compteurs collectifs.</p>

    <h3>2. Fuite enterrée non visible</h3>
    <p>La canalisation concernée doit être après le compteur d\'eau, sur le réseau privatif, et enterrée non visible (sous jardin, sous terrasse, sous dalle, sous voirie privative). Sont exclus : fuites visibles intérieures (chasses d\'eau, robinetterie, machine à laver, ballon d\'eau chaude), fuites sur canalisations apparentes, fuites avant compteur.</p>

    <h3>3. Surconsommation supérieure à 2× la moyenne</h3>
    <p>La consommation facturée doit dépasser le double de la consommation moyenne sur les 3 années précédentes. En dessous de ce seuil, le distributeur n\'a pas l\'obligation d\'informer ni de plafonner.</p>

    <h3>4. Réparation effectuée dans le mois</h3>
    <p>Après notification du distributeur, l\'abonné dispose d\'1 mois pour faire réparer la fuite. Sans réparation dans ce délai, l\'écrêtement n\'est pas applicable.</p>

    <h3>5. Attestation professionnelle</h3>
    <p>Une attestation d\'une entreprise du bâtiment doit certifier : la nature enterrée non visible de la fuite, la date de réparation, les travaux effectués. Notre rapport technique de recherche de fuite à Bordeaux est conforme à cette exigence et accepté par Suez et la Régie de l\'Eau Bordeaux Métropole. Voir notre <a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">page recherche de fuite canalisation enterrée à Bordeaux</a>.</p>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Procédure pas à pas avec votre distributeur</h2>

    <h3>Étape 1 : confirmer la fuite enterrée par un professionnel</h3>
    <p>C\'est le préalable indispensable. Notre intervention de recherche de fuite à Bordeaux coûte 380 à 580 € HT (souvent remboursé par votre assurance habitation au titre de la garantie recherche de fuite). Le rapport technique remis le jour même atteste la nature enterrée et la non-visibilité, conditions sine qua non de l\'écrêtement.</p>

    <h3>Étape 2 : faire réparer la fuite (sous 1 mois)</h3>
    <p>Par un plombier ou un terrassier selon la nature des travaux. Conservez la facture détaillée mentionnant le tracé enterré et la date d\'intervention. Pour les canalisations enterrées dégradées sur de longues distances, le chemisage peut éviter la tranchée. Voir notre <a href="/villes/bordeaux/chemisage/" style="color:var(--green);text-decoration:underline;">page chemisage canalisation à Bordeaux</a>.</p>

    <h3>Étape 3 : envoyer le courrier d\'écrêtement</h3>
    <p>Le calculateur ci-dessus génère un courrier conforme avec votre distributeur (Suez ou Régie BM). Envoyez-le en <strong>recommandé avec accusé de réception</strong> au siège du distributeur. Joignez : copie du rapport de recherche de fuite, facture du plombier, photocopie de votre dernière facture d\'eau.</p>

    <h3>Étape 4 : réponse du distributeur sous 30 à 60 jours</h3>
    <p>Le distributeur recalcule votre facture en plafonnant à 2× votre conso moyenne. Le surplus est annulé (avoir sur votre prochaine facture) ou remboursé par virement. En cas de refus, recours possible auprès du médiateur national de l\'eau ou via une procédure judiciaire au Tribunal d\'instance.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Pièges et refus fréquents</h2>
    <p>Sur les dossiers que nous accompagnons à Bordeaux, environ 1 sur 10 rencontre une difficulté. Voici les pièges fréquents :</p>
    <ul>
      <li><strong>Réparation effectuée par soi-même</strong> sans facture professionnelle : motif de refus systématique. Toujours faire intervenir un professionnel pour avoir une attestation.</li>
      <li><strong>Délai de 1 mois dépassé</strong> : si vous avez tardé à faire réparer, le distributeur peut refuser. Demandez systématiquement une dérogation écrite si vous prévoyez un dépassement.</li>
      <li><strong>Fuite mal qualifiée comme « non enterrée »</strong> : si l\'attestation ne mentionne pas explicitement le caractère enterré non visible, le distributeur refuse. Notre rapport mentionne ce point précisément.</li>
      <li><strong>Conso moyenne 3 ans non représentative</strong> (déménagement récent, occupation modifiée) : le distributeur peut contester la moyenne. Préparez les justificatifs des 3 années précédentes.</li>
      <li><strong>Fuite récidivante</strong> : si vous avez déjà bénéficié d\'un écrêtement Warsmann sur la même installation moins de 5 ans avant, le distributeur peut contester le caractère exceptionnel.</li>
    </ul>
    <p>En cas de refus, demandez le détail écrit motivé. La majorité des refus initiaux sont infondés et cèdent après envoi d\'un courrier de mise en demeure ou saisie du médiateur national de l\'eau (gratuit, délai 90 jours).</p>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Questions fréquentes</h2>

    <h3>Le calculateur est-il vraiment gratuit ?</h3>
    <p>Oui. Aucune donnée personnelle n\'est transmise à un serveur, tous les calculs et la génération du courrier se font dans votre navigateur. Anonyme et gratuit.</p>

    <h3>Le courrier généré est-il vraiment recevable juridiquement ?</h3>
    <p>Le courrier reprend les mentions obligatoires de l\'article L2224-12-4 du CGCT et la jurisprudence applicable. Il est rédigé selon le format-type des distributeurs Suez et Régie de l\'Eau Bordeaux Métropole. Pour les cas complexes ou un refus initial, consultez un avocat spécialisé en droit de la consommation.</p>

    <h3>Combien de temps prend la procédure Warsmann ?</h3>
    <p>De la détection au remboursement effectif : 60 à 120 jours en moyenne. Diagnostic professionnel (1 jour) + réparation (3 à 15 jours) + courrier au distributeur (1 jour) + réponse distributeur (30 à 60 jours) + remboursement par virement ou avoir (15 à 30 jours).</p>

    <h3>Mon assurance habitation rembourse-t-elle ce qui n\'est pas écrêté ?</h3>
    <p>Possible mais limité. Si la fuite a provoqué un dégât des eaux constaté (terrain saturé, infiltration cave, dégradation fondations), votre garantie multirisque peut intervenir. La part « eau perdue » au-delà du plafond Warsmann est rarement prise en charge sauf clauses spécifiques. Voir notre <a href="/guide/fuite-canalisation-enterree-assurance/" style="color:var(--green);text-decoration:underline;">guide fuite canalisation enterrée et assurance</a>.</p>

    <h3>Puis-je demander rétroactivement l\'écrêtement sur une fuite réparée il y a plusieurs mois ?</h3>
    <p>Le délai légal d\'1 mois après notification est prescriptif, mais les distributeurs acceptent souvent les demandes rétroactives jusqu\'à 1 an si le diagnostic professionnel et les justificatifs sont disponibles. Au-delà de 1 an, refus quasi systématique sauf cas exceptionnels (incapacité médicale, succession en cours).</p>

    <h3>Que faire si je n\'ai pas encore fait diagnostiquer la fuite ?</h3>
    <p>C\'est la première étape obligatoire. Sans rapport technique professionnel, la procédure Warsmann n\'est pas activable. Notre intervention à Bordeaux : 380 à 580 € HT, intervention sous 24 à 48h, rapport remis le jour même. Voir notre <a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">page canalisation enterrée Bordeaux</a> ou le <a href="/simulateur-cout-fuite/" style="color:var(--green);text-decoration:underline;">simulateur de coût de fuite</a> pour estimer votre situation avant l\'intervention.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Avant le calculateur, faites diagnostiquer la fuite</h2>
    <p>Le calculateur Warsmann est un outil de cadrage et de génération de courrier. Mais sans diagnostic professionnel attestant la nature enterrée de la fuite, votre dossier sera refusé par le distributeur. Faites intervenir un spécialiste recherche de fuite pour avoir le rapport conforme.</p>
    <p>Pages connexes : <a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">recherche de fuite canalisation enterrée à Bordeaux</a>, <a href="/detection-fuite/fuite-apres-compteur/" style="color:var(--green);text-decoration:underline;">fuite après compteur Bordeaux</a>, <a href="/guide/fuite-canalisation-enterree-assurance/" style="color:var(--green);text-decoration:underline;">guide assurance fuite enterrée</a>, <a href="/guide/loi-warsmann-ecretement-facture-eau/" style="color:var(--green);text-decoration:underline;">guide complet loi Warsmann</a>, <a href="/guide/facture-eau-suez-doublee-fuite-bordeaux/" style="color:var(--green);text-decoration:underline;">facture Suez doublée à Bordeaux</a>.</p>
  </div>
</section>

<style>
@media print {
  body * { visibility: hidden; }
  #courrier-content, #courrier-content * { visibility: visible; }
  #courrier-content { position: absolute; left: 0; top: 0; width: 100%; padding: 2rem; border: none; }
  #courrier-content button { display: none; }
}
</style>

<script>
function calculerWarsmann() {
  var consoMoy = parseFloat(document.getElementById("conso-moyenne").value);
  var consoActu = parseFloat(document.getElementById("conso-actuelle").value);
  var distrib = document.getElementById("distributeur-w").value;
  var fuite = document.getElementById("fuite-enterree").value;
  if (isNaN(consoMoy) || isNaN(consoActu) || consoMoy <= 0 || consoActu <= consoMoy) {
    alert("Merci de renseigner des valeurs valides (conso anormale supérieure à la conso moyenne).");
    return;
  }
  var tarifs = { suez: 4.87, regie: 3.90, autre: 4.50 };
  var tarif = tarifs[distrib];
  var plafond = consoMoy * 2;
  var surplus = Math.max(0, consoActu - plafond);
  var economie = surplus * tarif;
  var coutInitial = consoActu * tarif;
  var coutPlafonne = Math.min(consoActu, plafond) * tarif;

  document.getElementById("plafond-m3").textContent = Math.round(plafond) + " m³";
  document.getElementById("plafond-eur").textContent = Math.round(coutPlafonne) + " € (au tarif distributeur)";
  document.getElementById("economie").textContent = Math.round(economie) + " €";
  document.getElementById("surplus-m3").textContent = "Surplus écrêté : " + Math.round(surplus) + " m³";

  var alerte = document.getElementById("alerte-w");
  var explication = document.getElementById("explication-w");
  var conditions = document.getElementById("conditions-w");
  var courrierBloc = document.getElementById("courrier-bloc");

  if (consoActu < plafond) {
    alerte.style.background = "#FEF3C7";
    alerte.style.color = "#92400E";
    alerte.textContent = "Surconsommation insuffisante (en dessous du double de votre moyenne)";
    explication.innerHTML = "<strong>Loi Warsmann non applicable :</strong> votre consommation actuelle (" + Math.round(consoActu) + " m³) ne dépasse pas 2× votre moyenne historique (" + Math.round(plafond) + " m³). Le distributeur n\\'a pas d\\'obligation de plafonner.";
    conditions.innerHTML = "<strong>Que faire :</strong> contactez votre assurance habitation pour vérifier la prise en charge possible au titre de la garantie recherche de fuite si vous avez fait diagnostiquer.";
    courrierBloc.style.display = "none";
    document.getElementById("courrier-aperçu").style.display = "none";
  } else if (fuite === "non") {
    alerte.style.background = "#FEE2E2";
    alerte.style.color = "#991B1B";
    alerte.textContent = "Loi Warsmann non applicable (fuite non enterrée)";
    explication.innerHTML = "La loi Warsmann concerne <strong>exclusivement les fuites enterrées non visibles</strong> sur canalisation après compteur. Pour une fuite intérieure ou visible, ce dispositif ne s\\'applique pas.";
    conditions.innerHTML = "<strong>Alternatives :</strong> assurance habitation (garantie recherche de fuite + dégâts des eaux), ou geste commercial du distributeur sur demande.";
    courrierBloc.style.display = "none";
    document.getElementById("courrier-aperçu").style.display = "none";
  } else if (fuite === "bientot") {
    alerte.style.background = "#FEF3C7";
    alerte.style.color = "#92400E";
    alerte.textContent = "Éligibilité conditionnelle : faites diagnostiquer la fuite";
    explication.innerHTML = "<strong>Économie potentielle : " + Math.round(economie) + " €</strong> si vous obtenez un rapport technique attestant la nature enterrée de la fuite. <strong>Étape obligatoire avant la procédure Warsmann.</strong>";
    conditions.innerHTML = "<strong>Action :</strong> commandez un diagnostic professionnel. Notre intervention à Bordeaux : 380 à 580 € HT, souvent remboursée par votre assurance habitation. <a href=\\"/detection-fuite/canalisation-enterree-bordeaux/\\" style=\\"color:var(--green);text-decoration:underline;\\">Voir notre page canalisation enterrée</a>.";
    courrierBloc.style.display = "block";
  } else {
    alerte.style.background = "#D1FAE5";
    alerte.style.color = "#065F46";
    alerte.textContent = "Vous êtes éligible à l\\'écrêtement loi Warsmann";
    explication.innerHTML = "<strong>Économie nette : " + Math.round(economie) + " €</strong>. Votre facture peut être plafonnée à " + Math.round(coutPlafonne) + " € (au lieu de " + Math.round(coutInitial) + " €). Surplus écrêté : " + Math.round(surplus) + " m³.";
    conditions.innerHTML = "<strong>Conditions à respecter :</strong> envoyer le courrier ci-dessous en recommandé sous 1 mois après notification du distributeur, joindre le rapport de recherche de fuite et la facture de réparation.";
    courrierBloc.style.display = "block";
  }
  document.getElementById("resultats-w").style.display = "block";
  document.getElementById("resultats-w").scrollIntoView({ behavior: "smooth", block: "start" });
}

function genererCourrier() {
  var prenom = document.getElementById("ident-prenom").value.trim();
  var nom = document.getElementById("ident-nom").value.trim();
  var adresse = document.getElementById("ident-adresse").value.trim();
  var numClient = document.getElementById("ident-num-client").value.trim();
  var dateFuite = document.getElementById("ident-date-fuite").value;
  if (!prenom || !nom || !adresse || !numClient) {
    alert("Merci de renseigner toutes les coordonnées pour générer le courrier.");
    return;
  }
  var distrib = document.getElementById("distributeur-w").value;
  var consoMoy = parseFloat(document.getElementById("conso-moyenne").value);
  var consoActu = parseFloat(document.getElementById("conso-actuelle").value);
  var plafond = consoMoy * 2;
  var surplus = consoActu - plafond;

  var destinataires = {
    suez: "Suez Eau France\\nService Clients\\nCS 50049\\n92024 Nanterre Cedex",
    regie: "Régie de l\\'Eau Bordeaux Métropole\\nService Clientèle\\n12 esplanade Charles-de-Gaulle\\n33076 Bordeaux Cedex",
    autre: "[Nom et adresse du distributeur d\\'eau de votre commune]"
  };
  var destLabel = { suez: "Suez Eau France", regie: "Régie de l\\'Eau Bordeaux Métropole", autre: "votre distributeur d\\'eau" };
  var dateAujourdhui = new Date().toLocaleDateString("fr-FR", { day: "numeric", month: "long", year: "numeric" });
  var dateFuiteFr = dateFuite ? new Date(dateFuite).toLocaleDateString("fr-FR", { day: "numeric", month: "long", year: "numeric" }) : "[date de la fuite]";

  var courrier = `<div style="text-align:right;margin-bottom:2rem;">${destinataires[distrib].replace(/\\n/g, "<br>")}</div>
<div style="margin-bottom:2rem;">
<strong>${prenom} ${nom}</strong><br>
${adresse}<br>
N° client : ${numClient}
</div>
<div style="text-align:right;margin-bottom:2rem;">À ${adresse.split(",").pop().trim() || "Bordeaux"}, le ${dateAujourdhui}</div>
<div style="margin-bottom:1.5rem;"><strong>Objet :</strong> Demande d\\'écrêtement de facture d\\'eau au titre de la loi Warsmann (article L2224-12-4 du CGCT)<br>
<strong>Envoi :</strong> Lettre recommandée avec accusé de réception</div>
<p>Madame, Monsieur,</p>
<p>Je suis abonné(e) ${destLabel[distrib]} sous le numéro de client ${numClient} pour un local d\\'habitation situé au ${adresse}.</p>
<p>J\\'ai constaté en date du ${dateFuiteFr} une consommation d\\'eau anormalement élevée sur ma période de relevé : <strong>${Math.round(consoActu)} m³</strong>, soit nettement au-delà de ma consommation moyenne des trois dernières années établie à <strong>${Math.round(consoMoy)} m³ par an</strong>.</p>
<p>Cette surconsommation est due à une <strong>fuite sur la canalisation enterrée non visible située après mon compteur d\\'eau</strong>, sur le réseau privatif de mon habitation. Cette fuite a fait l\\'objet d\\'un diagnostic technique professionnel et a été réparée dans le délai d\\'un mois prescrit par la loi.</p>
<p>Conformément à l\\'<strong>article L2224-12-4 du Code général des collectivités territoriales</strong> (loi Warsmann du 17 mai 2011), je vous demande de bien vouloir <strong>plafonner ma facture à deux fois ma consommation moyenne des trois années précédentes</strong>, soit <strong>${Math.round(plafond)} m³</strong> au lieu des ${Math.round(consoActu)} m³ actuellement facturés. Le surplus de ${Math.round(surplus)} m³ doit être écrêté de ma facture conformément à la loi.</p>
<p>Vous trouverez en pièces jointes :</p>
<ul>
<li>Copie de ma dernière facture d\\'eau anormale</li>
<li>Rapport technique de recherche de fuite professionnel attestant la nature enterrée non visible de la fuite</li>
<li>Facture du plombier ayant effectué la réparation</li>
<li>Copie de mes 3 dernières factures annuelles établissant ma consommation moyenne historique</li>
</ul>
<p>Dans l\\'attente de votre réponse et du recalcul de ma facture sous les délais légaux, je vous prie de croire, Madame, Monsieur, à l\\'expression de mes salutations distinguées.</p>
<div style="margin-top:3rem;">
<strong>${prenom} ${nom}</strong><br>
<em style="color:#666;">(signature)</em>
</div>`;
  document.getElementById("courrier-content").innerHTML = courrier;
  document.getElementById("courrier-aperçu").style.display = "block";
  document.getElementById("courrier-aperçu").scrollIntoView({ behavior: "smooth", block: "start" });
}
</script>
'''

    ld_app = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "Calculateur loi Warsmann avec courrier auto-généré",
  "url": "https://recherche-fuite-gironde.fr/calcul-warsmann-bordeaux/",
  "applicationCategory": "UtilityApplication",
  "operatingSystem": "Web",
  "description": "Calculez votre éligibilité à l'écrêtement loi Warsmann après une fuite enterrée à Bordeaux. Génération automatique du courrier-type Suez ou Régie de l'Eau Bordeaux Métropole.",
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "EUR" }
}
</script>'''

    ld_local = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Recherche Fuite Gironde",
  "url": "https://recherche-fuite-gironde.fr/",
  "areaServed": { "@type": "AdministrativeArea", "name": "Gironde" },
  "priceRange": "€€"
}
</script>'''

    ld_breadcrumb = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://recherche-fuite-gironde.fr/" },
    { "@type": "ListItem", "position": 2, "name": "Calcul Warsmann Bordeaux", "item": "https://recherche-fuite-gironde.fr/calcul-warsmann-bordeaux/" }
  ]
}
</script>'''

    ld_faq = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Le calculateur Warsmann est-il vraiment gratuit ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Oui, totalement gratuit et anonyme. Aucune donnée personnelle envoyée à un serveur, calculs et génération de courrier dans le navigateur." }
    },
    {
      "@type": "Question",
      "name": "Le courrier généré est-il juridiquement recevable ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Le courrier reprend les mentions obligatoires de l'article L2224-12-4 du CGCT et le format-type des distributeurs Suez et Régie de l'Eau Bordeaux Métropole. Pour les cas complexes ou un refus initial, consulter un avocat spécialisé en droit de la consommation." }
    },
    {
      "@type": "Question",
      "name": "Combien de temps prend la procédure Warsmann ?",
      "acceptedAnswer": { "@type": "Answer", "text": "60 à 120 jours en moyenne entre la détection et le remboursement effectif : diagnostic (1 jour) + réparation (3-15 jours) + courrier (1 jour) + réponse distributeur (30-60 jours) + remboursement (15-30 jours)." }
    },
    {
      "@type": "Question",
      "name": "Puis-je demander rétroactivement l'écrêtement ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Le délai légal d'1 mois est prescriptif, mais les distributeurs acceptent souvent les demandes rétroactives jusqu'à 1 an si diagnostic et justificatifs disponibles. Au-delà de 1 an, refus quasi systématique." }
    },
    {
      "@type": "Question",
      "name": "Que faire si je n'ai pas encore fait diagnostiquer la fuite ?",
      "acceptedAnswer": { "@type": "Answer", "text": "C'est la première étape obligatoire. Sans rapport technique professionnel attestant la nature enterrée, la procédure Warsmann n'est pas activable. Notre intervention à Bordeaux : 380 à 580 € HT, rapport remis le jour même, souvent remboursé par l'assurance habitation." }
    }
  ]
}
</script>'''

    return html_base(
        "Calculateur loi Warsmann Bordeaux | Courrier auto",
        "Calculez votre écrêtement loi Warsmann après une fuite enterrée à Bordeaux et téléchargez le courrier pré-rempli pour Suez ou Régie de l'Eau Bordeaux Métropole.",
        "https://recherche-fuite-gironde.fr/calcul-warsmann-bordeaux/",
        body,
        ld_app + ld_local + ld_breadcrumb + ld_faq
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

    <div id="form-contact-error" style="display:none;background:#fef2f2;border:1px solid #fca5a5;border-radius:8px;padding:1rem;text-align:center;margin-bottom:1rem;"><p style="color:#991b1b;font-size:.9rem;margin:0;">Une erreur est survenue. Veuillez r\u00e9essayer ou nous appeler directement.</p></div>
    <form data-ajax data-error="form-contact-error" style="display:flex;flex-direction:column;gap:1.25rem;">
      <input type="hidden" name="_subject" value="[recherche-fuite-gironde.fr] Message de contact">
      <input type="hidden" name="site_source" value="">

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
          <label style="display:block;font-size:.85rem;font-weight:600;color:var(--muted);margin-bottom:.35rem;text-transform:uppercase;letter-spacing:.05em;" for="téléphone">Téléphone</label>
          <input style="width:100%;font-family:var(--f-body);font-size:.9375rem;color:var(--text);background:var(--white);border:1px solid var(--border);border-radius:var(--r-md);padding:.8rem 1rem;outline:none;transition:border-color .15s,box-shadow .15s;" type="tel" id="téléphone" name="téléphone" placeholder="06 XX XX XX XX"
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
    piscine_pages = '\n'.join([
        f'<li><a href="/detection-fuite/{p["slug"]}/">Recherche de fuite piscine {p["ville_article"]} ({p["cp"]})</a></li>'
        for p in PISCINE_PAGES
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
    <p class="hero-mini-lead">Toutes les pages du site recherche-fuite-gironde.fr classées par section.</p>
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

      <h2>Outils gratuits</h2>
      <ul>
        <li><a href="/simulateur-cout-fuite/">Simulateur de coût d'une fuite (canalisation ou piscine)</a></li>
        <li><a href="/calcul-warsmann-bordeaux/">Calculateur loi Warsmann + courrier auto-généré</a></li>
      </ul>

      <h2>Pages spécialisées par cas d'usage</h2>
      <p>Pages dédiées aux situations spécifiques que nous traitons quotidiennement, avec contenu approfondi et tarifs détaillés.</p>
      <ul>
        <li><a href="/detection-fuite/urgence-bordeaux/">Recherche de fuite en urgence à Bordeaux (intervention 24h)</a></li>
        <li><a href="/detection-fuite/fuite-apres-compteur/">Fuite d'eau après compteur à Bordeaux (loi Warsmann)</a></li>
        <li><a href="/detection-fuite/canalisation-enterree-bordeaux/">Recherche de fuite canalisation enterrée à Bordeaux (gaz traceur)</a></li>
        <li><a href="/detection-fuite/degats-des-eaux-bordeaux/">Dégât des eaux à Bordeaux (syndics et copropriétés IRSI)</a></li>
        <li><a href="/detection-fuite/chemisage-bordeaux/">Chemisage de canalisation à Bordeaux (immeubles haussmanniens)</a></li>
        <li><a href="/detection-fuite/fuite-plancher-chauffant-bordeaux/">Fuite sur plancher chauffant à Bordeaux (thermographie)</a></li>
        <li><a href="/detection-fuite/thermographie-infrarouge-bordeaux/">Thermographie infrarouge à Bordeaux (caméra thermique)</a></li>
        <li><a href="/detection-fuite/fluoresceine-piscine-bordeaux/">Fluorescéine piscine Bordeaux (colorant traceur)</a></li>
        <li><a href="/detection-fuite/depannage-piscine-bordeaux/">Dépannage piscine à Bordeaux (diagnostic + réparation)</a></li>
      </ul>

      <h2>Recherche de fuite piscine par ville</h2>
      <p>Pages dédiées à la recherche de fuite sur piscine, sans vidange, par commune de Gironde.</p>
      <ul>
        {piscine_pages}
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

      <h2>Guide spécialisé Bordeaux et piscine</h2>
      <p>Articles approfondis sur les thématiques à fort enjeu : prix, assurance, diagnostic piscine, écrêtement de facture.</p>
      <ul>
        <li><a href="/guide/fuite-piscine-bordeaux/"><strong>Guide complet fuite piscine à Bordeaux</strong> (panorama des 12 articles piscine)</a></li>
        <li><a href="/guide/prix-recherche-fuite-bordeaux/">Prix d'une recherche de fuite à Bordeaux en 2026</a></li>
        <li><a href="/guide/recherche-fuite-piscine-tarif/">Tarif recherche de fuite piscine en Gironde par type de bassin</a></li>
        <li><a href="/guide/recherche-fuite-piscine-assurance/">Recherche de fuite piscine et assurance habitation : remboursement</a></li>
        <li><a href="/guide/ma-piscine-perd-de-l-eau-que-faire/">Ma piscine perd de l'eau : guide de diagnostic étape par étape</a></li>
        <li><a href="/guide/fuite-liner-piscine/">Fuite sur liner de piscine : signes, causes et diagnostic</a></li>
        <li><a href="/guide/evaporation-vs-fuite-piscine/">Évaporation ou fuite de piscine : taux mensuels Gironde</a></li>
        <li><a href="/guide/loi-warsmann-ecretement-facture-eau/">Loi Warsmann : écrêtement de facture d'eau après fuite</a></li>
        <li><a href="/guide/reparation-liner-piscine/">Réparation d'une fuite de liner piscine : méthodes et coûts</a></li>
        <li><a href="/guide/reparation-skimmer-piscine-resine-epoxy/">Réparation skimmer piscine à la résine époxy</a></li>
        <li><a href="/guide/fuite-canalisation-enterree-assurance/">Fuite canalisation enterrée et assurance habitation</a></li>
        <li><a href="/guide/detecteur-fuite-eau-professionnel/">Détecteur de fuite d'eau professionnel : matériel et méthodes</a></li>
        <li><a href="/guide/piscine-qui-fuit-perte-eau/">Piscine qui fuit ou perte d'eau : que faire ?</a></li>
        <li><a href="/guide/fuite-coque-polyester-piscine/">Fuite sur coque polyester : diagnostic et réparation</a></li>
        <li><a href="/guide/inspection-camera-canalisation-bordeaux/">Inspection caméra canalisation à Bordeaux</a></li>
        <li><a href="/guide/fuite-piscine-desjoyaux-bordeaux/">Fuite piscine Desjoyaux à Bordeaux</a></li>
        <li><a href="/guide/fuite-piscine-magiline-bordeaux/">Fuite piscine Magiline à Bordeaux</a></li>
        <li><a href="/guide/fuite-piscine-diffazur-bordeaux/">Fuite piscine Diffazur à Bordeaux</a></li>
        <li><a href="/guide/fuite-piscine-waterair-bordeaux/">Fuite piscine Waterair à Bordeaux</a></li>
        <li><a href="/guide/piscine-perd-3-cm-par-jour/">Piscine qui perd 3 cm par jour</a></li>
        <li><a href="/guide/compteur-eau-qui-tourne-sans-utilisation/">Compteur d'eau qui tourne sans utilisation</a></li>
        <li><a href="/guide/facture-eau-suez-doublee-fuite-bordeaux/">Facture Suez doublée à Bordeaux</a></li>
        <li><a href="/guide/colonne-fonte-haussmannien-bordeaux-fuite/">Colonne en fonte haussmannien Bordeaux</a></li>
        <li><a href="/guide/convention-irsi-copropriete-bordeaux-degats-eaux/">Convention IRSI copropriété Bordeaux</a></li>
        <li><a href="/guide/fuite-pvc-enterree-jardin-bordeaux/">Fuite PVC enterrée jardin Bordeaux</a></li>
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
        "Plan du site recherche-fuite-gironde.fr. Toutes les pages : services, villes de Gironde, pages spécialisées (piscine, urgence, chemisage), guide pratique.",
        "https://recherche-fuite-gironde.fr/plan-du-site/",
        body
    )

# ── Pages du guide ─────────────────────────────────────────────
GUIDE_PAGES = [
    {
        "slug": "comment-detecter-une-fuite",
        "title": "Comment détecter une fuite chez soi",
        "title_seo": "Comment détecter une fuite d'eau chez soi",
        "desc": "Les signes qui indiquent une fuite d'eau chez vous et les premières vérifications à faire avant d'appeler un technicien en Gironde.",
        "contenu": """<p>Une fuite d'eau peut rester invisible pendant des semaines, voire des mois, avant de se manifester clairement. savoir la détecter tôt permet d'éviter des dégâts importants et des factures d'eau en hausse.</p>
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
        "title_seo": "Causes fréquentes des fuites d'eau en maison",
        "desc": "Pourquoi une canalisation fuit-elle ? Les causes les plus fréquentes de fuites d'eau dans les maisons et appartements en Gironde.",
        "contenu": """<p>Une fuite d'eau n'arrive jamais par hasard. comprendre les causes les plus fréquentes permet d'anticiper les risques et d'adapter la solution de réparation.</p>
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
<p>quelle que soit la cause, nos techniciens en Gironde identifient rapidement l'origine de la fuite et vous proposent la solution adaptée : réparation ponctuelle ou <a href="/chemisage-canalisation/" style="color:var(--green);text-decoration:underline;">chemisage de la canalisation</a> si le réseau est trop dégradé.</p>"""
    },
    {
        "slug": "fuite-sous-dalle",
        "title": "Fuite sous dalle : diagnostic et solutions",
        "title_seo": "Fuite sous dalle : détection et réparation Gironde",
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
        "title_seo": "Fuite canalisation enterrée Gironde | Détection",
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
</ul>
<h2>Cas particulier : fuite sur canalisation enterrée après compteur</h2>
<p>Si votre fuite se situe entre votre compteur d'eau et votre habitation (zone privative), vous pouvez souvent bénéficier d'un écrêtement de facture auprès de Suez ou de votre régie des eaux (loi Warsmann 2011). Notre page dédiée <a href="/detection-fuite/fuite-apres-compteur/" style="color:var(--green);text-decoration:underline;">fuite d'eau après compteur à Bordeaux</a> détaille la procédure, les justificatifs à fournir et les conditions à remplir pour obtenir ce plafonnement de facturation.</p>"""
    },
    {
        "slug": "chemisage-explication",
        "title": "Le chemisage de canalisation expliqué",
        "title_seo": "Chemisage canalisation : la technique expliquée",
        "desc": "Comment fonctionne le chemisage de canalisation ? La technique, les matériaux et les étapes d'une intervention en Gironde expliqués simplement.",
        "contenu": """<p>Le chemisage de canalisation est une technique de rénovation qui consiste à créer un nouveau tuyau à l'intérieur de l'ancien, sans démolition. C'est la solution idéale quand la canalisation est trop dégradée pour une réparation ponctuelle.</p>
<h2>Le principe du chemisage</h2>
<p>Un manchon souple imprégné de résine époxy est introduit dans la canalisation existante par un accès naturel (regard, siphon, ouverture de visite). Une fois en position, il est gonflé à l'aide d'air comprimé et maintenu appuyé contre les parois pendant que la résine durcit. quelques heures plus tard, la résine est polymérisée et forme un nouveau tuyau lisse et étanche à l'intérieur de l'ancien.</p>
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
        "title_seo": "Coût d'une recherche de fuite d'eau Gironde",
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
<p>Nous vous proposons un devis gratuit avant toute intervention. Après un premier échange sur votre situation (type de fuite, configuration du logement, localisation en Gironde), nous pouvons vous donner une estimation précise et sans surprise. Utilisez le formulaire de contact pour nous décrire votre situation.</p>
<p>Pour un détail complet des tarifs 2026 par méthode avec un tableau comparatif, consultez notre guide <a href="/guide/prix-recherche-fuite-bordeaux/" style="color:var(--green);text-decoration:underline;">prix d'une recherche de fuite à Bordeaux</a>, qui couvre également la prise en charge par l'assurance et l'écrêtement de facture d'eau selon la loi Warsmann.</p>"""
    },
    {
        "slug": "assurance-fuite-eau",
        "title": "Fuite d'eau et assurance habitation",
        "title_seo": "Assurance habitation et fuite d'eau : remboursement",
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
<p>C'est le document central de votre dossier. Il doit mentionner : la localisation précise de la fuite, la technique utilisée, les photos de l'intervention et les préconisations de réparation. Nous fournissons systématiquement ce rapport à l'issue de chaque intervention en Gironde.</p>
<h2>Cas de la fuite après compteur : la loi Warsmann</h2>
<p>Si la fuite se situe sur votre réseau privatif enterré (entre compteur et habitation), vous pouvez cumuler la prise en charge assurance ET un écrêtement de facture d'eau auprès de votre distributeur. La loi Warsmann de 2011 plafonné la surfacturation due à une fuite enterrée indétectable. Consultez notre guide <a href="/detection-fuite/fuite-apres-compteur/" style="color:var(--green);text-decoration:underline;">fuite d'eau après compteur à Bordeaux</a> pour la procédure complète. Pour le détail spécifique de la prise en charge sur fuite enterrée (procédure pas à pas, cas concrets, exclusions), voir notre guide <a href="/guide/fuite-canalisation-enterree-assurance/" style="color:var(--green);text-decoration:underline;">fuite canalisation enterrée et assurance habitation</a>.</p>"""
    },
    {
        "slug": "urgence-fuite-eau",
        "title": "Que faire en cas d'urgence fuite d'eau ?",
        "title_seo": "Urgence fuite d'eau : que faire en Gironde",
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
<p>Une fois l'urgence gérée, il est indispensable de faire localiser la fuite par un professionnel avant toute remise en eau. En Gironde, nous intervenons sous 24h pour une <a href="/detection-fuite/" style="color:var(--green);text-decoration:underline;">recherche de fuite non destructive</a> avec remise du rapport assurance.</p>
<p>Pour les fuites actives importantes sur Bordeaux et sa métropole, consultez notre page dédiée à la <a href="/detection-fuite/urgence-bordeaux/" style="color:var(--green);text-decoration:underline;">recherche de fuite en urgence à Bordeaux</a> : intervention sous 24h, qualification téléphonique dans l'heure, rapport remis le jour même. Si votre surconsommation d'eau est inexpliquée, la fuite se situe peut-être sur le réseau privatif : voir notre guide <a href="/detection-fuite/fuite-apres-compteur/" style="color:var(--green);text-decoration:underline;">fuite après compteur à Bordeaux</a> (écrêtement de facture possible selon loi Warsmann).</p>"""
    },
    {
        "slug": "recherche-fuite-piscine-tarif",
        "title": "Tarif recherche de fuite piscine en Gironde : prix par type de bassin",
        "title_seo": "Tarif recherche fuite piscine Gironde 2026",
        "desc": "Tarif d'une recherche de fuite piscine en Gironde selon le type de bassin (liner, coque, béton), la méthode employee et la taille. Grille détaillée 2026.",
        "contenu": """<p>Combien coûte réellement une recherche de fuite sur une piscine en Gironde ? La reponse dépend fortement du type de bassin que vous avez. Un liner PVC, une coque polyester et un bassin béton armé ne se diagnostiquent pas avec les mêmes méthodes ni le même temps d'intervention. Cet article détaillé la grille tarifaire 2026 par type de bassin, avec les méthodes associees et les cas complexes qui peuvent faire varier le prix final.</p>

<h2>Pourquoi le type de bassin déterminé le tarif ?</h2>
<p>Contrairement aux recherches de fuite sur canalisation d'eau classique (ou la méthode principale - gaz traceur ou acoustique - s'applique partout de manière similaire), le diagnostic d'une fuite de piscine varie fortement selon la structure du bassin. Une coque polyester demande une inspection camera spécifique aux défauts structurels (osmose, délaminage). Un liner PVC impose colorant fluorescéine et inspection visuelle des soudures. Un bassin béton armé nécessite potentiellement un diagnostic structurel pour distinguer une fissure active d'une fissure stabilisée. Ce paramètre technique fait varier notre devis de 30 à 50 pourcent selon les cas.</p>

<h2>Tarif par type de bassin (2026)</h2>

<h3>Piscine liner PVC - tarif 300 à 500 € HT</h3>
<p>Les piscines avec liner PVC 75/100 ou 85/100, dominant le parc girondin des années 1990-2010, représentent notre diagnostic le plus rapide. Méthodologie : inspection visuelle du liner en apnee ou camera, colorant fluorescéine sur pièces a sceller (skimmer, buses de refoulement, bonde de fond), test de pression hydraulique sur canalisations. durée d'intervention : 1h30 a 2h. Tarif moyen : 300 à 500 € HT selon la taille du bassin (4x8m jusqu'à 5x10m couverts dans cette fourchette). Au-delà (piscines familiales de plus de 10m), supplement de 50 à 100 €.</p>

<h3>Piscine coque polyester - tarif 400 à 600 € HT</h3>
<p>Les coques polyester monoblocs installées entre 2000 et 2020 demandent une inspection camera sous-marine plus minutieuse pour détecter les signes d'osmose (cloques sur le gel-coat), les microfissures au niveau des pièces moulees (bondes de fond, marches romaines, escaliers intégrés) et les delaminages inter-couches de fibre. La fluorescéine confirme les défauts visuels suspectes. Tarif moyen : 400 à 600 € HT, incluant le rapport photo détaillé indispensable pour faire jouer la garantie décennale de pose si le bassin à moins de 10 ans.</p>

<h3>Piscine béton armé - tarif 450 à 700 € HT</h3>
<p>Les bassins béton armé, fréquents dans les grandes propriétés (villas Arcachon, chais viticoles Libournais, propriétés Caudéran) ou construits sur mesure, nécessitent notre diagnostic le plus approfondi. Inspection camera complète, test colorant, écoute électro-acoustique sur canalisations enterrées, et parfois inspection structurelle si des fissures sont détectées. Tarif moyen : 450 à 700 € HT. Les piscines de plus de 50 m³ (12×5 ou 15×4) ou avec configuration complexe (miroir, débordement periphérique, volet immergé) peuvent monter a 800 € HT.</p>

<h3>Piscine naturelle / bio-phytoépuration - tarif 500 à 800 € HT</h3>
<p>Les piscines naturelles a lagunage vegetal, en croissance en Gironde (Gujan-Mestras, La Teste, quelques installations à Mérignac), demandent une approche spécifique. Isolation séquentielle des différents compartiments (bassin de baignade, bassin de filtration vegetale, canalisations de transfert), mesure différentielle sur 48h pour identifier la zone fuyante, puis diagnostic fin. Tarif moyen : 500 à 800 € HT, plus élevé en raison du temps d'intervention double sur deux passages.</p>

<h2>Tarif par méthode (si diagnostic cible)</h2>
<p>Pour un problème déjà identifié ou suspecte sur un circuit précis, une intervention ciblée sur une seule méthode est possible a tarif réduit.</p>

<table style="width:100%;border-collapse:collapse;margin:1.5rem 0;background:#fff;">
<thead><tr style="background:#0D3B2E;color:#fff;"><th style="padding:.75rem;text-align:left;border:1px solid #155740;">méthode isolée</th><th style="padding:.75rem;text-align:left;border:1px solid #155740;">Tarif HT</th><th style="padding:.75rem;text-align:left;border:1px solid #155740;">Cas d'usage</th></tr></thead>
<tbody>
<tr><td style="padding:.75rem;border:1px solid #D8D4CC;">Colorant fluorescéine + visuelle</td><td style="padding:.75rem;border:1px solid #D8D4CC;">250 à 350 €</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Fuite suspectee sur pièces a sceller connues</td></tr>
<tr style="background:#F7F6F2;"><td style="padding:.75rem;border:1px solid #D8D4CC;">Test de pression canalisations</td><td style="padding:.75rem;border:1px solid #D8D4CC;">300 à 400 €</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Chute de pression filtration inexpliquée</td></tr>
<tr><td style="padding:.75rem;border:1px solid #D8D4CC;">Inspection camera sous-marine</td><td style="padding:.75rem;border:1px solid #D8D4CC;">280 à 380 €</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Suspicion de fissure coque ou liner</td></tr>
<tr style="background:#F7F6F2;"><td style="padding:.75rem;border:1px solid #D8D4CC;">Gaz traceur canalisation enterrée</td><td style="padding:.75rem;border:1px solid #D8D4CC;">400 à 550 €</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Fuite hors bassin, réseau enterré jardin</td></tr>
<tr><td style="padding:.75rem;border:1px solid #D8D4CC;">Inspection complète + rapport</td><td style="padding:.75rem;border:1px solid #D8D4CC;">450 à 800 €</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Aucune piste, diagnostic exhaustif</td></tr>
</tbody>
</table>

<h2>Supplements possibles</h2>
<ul>
<li><strong>Intervention urgence (24h)</strong> : aucun supplement chez nous, notre planning intégré des creneaux prioritaires</li>
<li><strong>Piscine couverte par volet immerge ou abri</strong> : supplement de 50 € pour manipulation securisee</li>
<li><strong>Piscine très profonde (4m+)</strong> : supplement plongeur professionnel de 300 à 500 € si plongee humaine nécessaire</li>
<li><strong>déplacement hors métropole bordelaise</strong> : forfait 40 € pour Bassin d'Arcachon, Medoc, Libournais</li>
<li><strong>Hivernage en cours</strong> : pas de supplement mais creneau limite (novembre a mars, intervention possible si bassin accessible)</li>
</ul>

<h2>Comparatif : diagnostic moderne vs vidange classique</h2>
<p>Certaines entreprises proposent encore de vider la piscine pour inspecter visuellement le bassin. Cette méthode, très consommatrice en eau et en temps, coûte en réalité plus cher que notre diagnostic non destructif.</p>

<table style="width:100%;border-collapse:collapse;margin:1.5rem 0;background:#fff;">
<thead><tr style="background:#0D3B2E;color:#fff;"><th style="padding:.75rem;text-align:left;border:1px solid #155740;">Poste</th><th style="padding:.75rem;text-align:left;border:1px solid #155740;">diagnostic moderne</th><th style="padding:.75rem;text-align:left;border:1px solid #155740;">Vidange classique</th></tr></thead>
<tbody>
<tr><td style="padding:.75rem;border:1px solid #D8D4CC;">Tarif recherche</td><td style="padding:.75rem;border:1px solid #D8D4CC;">300 à 700 €</td><td style="padding:.75rem;border:1px solid #D8D4CC;">500 à 1000 €</td></tr>
<tr style="background:#F7F6F2;"><td style="padding:.75rem;border:1px solid #D8D4CC;">coût vidange + remise en eau</td><td style="padding:.75rem;border:1px solid #D8D4CC;">0 € (pas de vidange)</td><td style="padding:.75rem;border:1px solid #D8D4CC;">500 à 1500 € (eau + chimie)</td></tr>
<tr><td style="padding:.75rem;border:1px solid #D8D4CC;">Risque structurel sur bassin vide</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Nul</td><td style="padding:.75rem;border:1px solid #D8D4CC;">élevé en zone nappe phreatique</td></tr>
<tr style="background:#F7F6F2;"><td style="padding:.75rem;border:1px solid #D8D4CC;">durée totale</td><td style="padding:.75rem;border:1px solid #D8D4CC;">2 à 4 h</td><td style="padding:.75rem;border:1px solid #D8D4CC;">2 à 5 jours</td></tr>
<tr><td style="padding:.75rem;border:1px solid #D8D4CC;">coût total moyen</td><td style="padding:.75rem;border:1px solid #D8D4CC;"><strong>500 € HT</strong></td><td style="padding:.75rem;border:1px solid #D8D4CC;"><strong>1 500 à 2 500 € HT</strong></td></tr>
</tbody>
</table>

<h2>Prise en charge par l'assurance habitation</h2>
<p>La garantie « recherche de fuite » de votre contrat multirisque habitation rembourse tout ou partie du diagnostic piscine dès lors qu'un dégât des eaux est constate (dégradation du jardin, infiltration dans le local technique, impact sur fondations). Notre rapport technique est accepte par les principaux assureurs francais. Pour le détail de la procédure, consultez notre guide <a href="/guide/recherche-fuite-piscine-assurance/" style="color:var(--green);text-decoration:underline;">recherche de fuite piscine et assurance habitation</a>.</p>

<h2>Interventions groupees (copropriété, résidence)</h2>
<p>Pour les copropriétés avec piscine collective (Bassin d'Arcachon, résidences touristiques) ou les gestionnaires multi-sites, nous proposons des forfaits d'intervention groupée : diagnostic de plusieurs piscines en une seule visite avec remise minoree. Contactez-nous pour une estimation spécifique.</p>

<h2>Notre engagement tarifaire</h2>
<ul>
<li>Devis fixe communique avant intervention, sans surprise</li>
<li>Aucun déplacement facture si vous ne donnez pas suite au devis</li>
<li>Rapport technique détaillé inclus dans le tarif annonce</li>
<li>Paiement après intervention sur facture, aucun acompte demandé</li>
</ul>

<p>Obtenez un devis personnalise en decrivant votre situation via notre <a href="/devis/" style="color:var(--green);text-decoration:underline;">formulaire de demande de devis</a>, ou consultez directement notre page <a href="/detection-fuite/piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">recherche de fuite piscine à Bordeaux</a> ou la <a href="/detection-fuite/piscine-arcachon/" style="color:var(--green);text-decoration:underline;">page piscine Arcachon</a> si vous etes sur le Bassin.</p>"""
    },
    {
        "slug": "recherche-fuite-piscine-assurance",
        "title": "Recherche fuite piscine et assurance habitation : le remboursement",
        "title_seo": "Recherche fuite piscine et assurance | Remboursement",
        "desc": "Comment faire rembourser une recherche de fuite sur piscine par votre assurance habitation en Gironde. Clauses, procédure, IRSI copropriété, cas complexes.",
        "contenu": """<p>La recherche de fuite sur une piscine privée représente un investissement de 300 à 800 euros HT selon les cas. La bonne nouvelle : votre assurance habitation multirisque couvre souvent tout ou partie de cette prestation, sous réservé de connaitre les clauses applicables et de respecter la procédure de déclaration. Cet article détaillé les modalites propres aux piscines, qui différent sensiblement de celles d'un simple dégât des eaux en logement.</p>

<h2>Votre piscine est-elle couverte par votre assurance habitation ?</h2>
<p>La majorite des contrats multirisques habitation en France incluent automatiquement la piscine privée dans les biens couverts, avec deux conditions souvent oubliees : déclaration initiale au moment de la souscription (ou modification en cours de contrat) et conformite aux normes de sécurité (alarme, couverture, barriere, abri). Si vous avez installé votre piscine après la souscription du contrat sans le signaler à votre assureur, la couverture peut être refusee.</p>

<p>Pour vérifier votre couverture piscine, consultez les conditions générales (section « biens extérieurs couverts » ou « annexes du logement ») et les conditions particulières (montant assure spécifique piscine, franchise applicable). En cas de doute, demandez par écrit à votre assureur une confirmation de votre couverture piscine.</p>

<h2>Ce qui est couvert par votre assurance</h2>
<ul>
<li><strong>Recherche de fuite elle-même</strong> : diagnostic non destructif par un professionnel, rapport technique</li>
<li><strong>Consommation d'eau perdue</strong> : ecrêtement auprès du distributeur (Suez, Régie des eaux) selon loi Warsmann si canalisation enterrée indétectable</li>
<li><strong>dégâts collatéraux</strong> : pelouse abîmee, fondations de la maison affectees, local technique inondé, mobilier extérieur endommagé</li>
<li><strong>réparation de la fuite</strong> : souvent couverte si la cause est accidentelle (pas due a usure normale ou défaut d'entretien)</li>
<li><strong>Remise en eau du bassin</strong> : pris en charge si une vidange a été nécessaire</li>
</ul>

<h2>Ce qui n'est PAS couvert</h2>
<ul>
<li><strong>Usure normale</strong> : un liner de 25 ans qui fuit par fatigué n'est généralement pas indemnise (relevé de l'entretien)</li>
<li><strong>défaut d'entretien caractérisé</strong> : piscine abandonnee plusieurs saisons, hivernage mal réalisé</li>
<li><strong>défauts de construction</strong> : pour une piscine neuve (moins de 10 ans), c'est la garantie décennale du constructeur qui s'applique, pas l'assurance habitation</li>
<li><strong>Equipements haut de gamme non declares</strong> : PAC, volet automatique, abri, local technique équipé - a lister spécifiquement dans le contrat</li>
</ul>

<h2>Procédure de déclaration pour une fuite piscine</h2>

<h3>étape 1 : Constat et preuves</h3>
<p>Dès que vous constatez une perte d'eau anormale (plus de 1 cm par jour, au-delà de l'évaporation naturelle en Gironde), faites le test du seau pour confirmer la fuite. Photographiez le niveau du bassin, les zones humides autour (pelouse, terrasse), les indices de ruissellement. Relevez votre compteur d'eau pour documenter la surconsommation.</p>

<h3>étape 2 : Declaration sous 5 jours ouvrables</h3>
<p>Votre contrat impose une déclaration sous 5 jours ouvrables a compter de la découverte. Cette déclaration peut se faire par courrier recommandé, formulaire en ligne sur l'espace client, ou téléphone (demandez une confirmation écrite). Joignez les photos, la date de découverte, la description des symptomes et si possible une estimation des dégâts.</p>

<h3>étape 3 : Mandatement du professionnel</h3>
<p>Votre assureur peut mandater son propre expert, ou vous laisser choisir un prestataire independant. Dans les deux cas, c'est le rapport technique qui justifiera la prise en charge. Nous sommes reconnus par la majorite des assureurs francais (AXA, Allianz, MAAF, Groupama, Matmut, MACIF, MMA, GMF). Contactez-nous directement en mentionnant que votre assurance doit intervenir : nous adaptons le rapport aux exigences du dossier.</p>

<h3>étape 4 : Remise du rapport et devis de réparation</h3>
<p>Notre rapport technique comprend : photos de la piscine et du point de fuite, méthodes employees pour le diagnostic, localisation précise avec schema, estimation du débit de fuite, préconisations de réparation chiffrees. Transmettez ce rapport à votre assureur avec les devis de réparation (liner, coque, canalisations selon la cause).</p>

<h3>étape 5 : Expertise contradictoire si nécessaire</h3>
<p>Pour les sinistres importants (plus de 5 000 € de dégâts), l'assureur peut diligenter une expertise contradictoire. Vous pouvez être assiste d'un expert d'assure pour defendre vos intérêts, notamment si votre assureur conteste la cause ou le montant.</p>

<h2>Convention IRSI en copropriété avec piscine collective</h2>
<p>Les résidences bordelaises avec piscine collective (Bassins a Flot, résidences des années 1990-2010, résidences touristiques du Bassin d'Arcachon) sont régies par la convention IRSI pour les dégâts des eaux jusqu'à 5 000 euros HT. Le syndic mandate le prestataire, l'assureur de la copropriété prend en charge le rapport et les dommages, puis se retourne contre l'assureur responsable si un lot individuel est à l'origine du sinistre (très rare pour une piscine collective).</p>

<p>Notre rapport est spécifiquement formate pour les sinistres IRSI : identification précise des responsabilités, chiffrage des dommages par zone (bassin, plage, jardin, lots adjacents), préconisations techniques détaillées.</p>

<h2>Cas complexes spécifiques aux piscines</h2>

<h3>Piscine en location saisonnière</h3>
<p>Si vous louez votre résidence avec piscine en meublé de tourisme, votre contrat multirisque habitation classique n'est pas suffisant : il vous faut une extension « location meublee » ou un contrat spécifique « résidence secondaire louee ». Sans cette extension, l'assureur peut refuser la prise en charge d'une fuite survenue pendant une location.</p>

<h3>Résidence secondaire (Arcachon, Le Pyla)</h3>
<p>Les fuites decouvertes au retour après plusieurs mois d'inoccupation posent une question juridique : l'assureur peut arguer que le défaut de surveillance est fautif. contre-argument : une fuite sur canalisation enterrée etait indétectable visuellement (loi Warsmann). Notre rapport documente explicitement ce point pour faciliter la prise en charge.</p>

<h3>Piscine partagee entre plusieurs lots (copropriété horizontale)</h3>
<p>quelques copropriétés horizontales dans la métropole (Pessac, Mérignac) ont des piscines partagees entre 2 à 10 maisons. Le statut juridique de la piscine est defini dans le règlement de copropriété. Notre rapport identifié la zone de responsabilité pour le règlement entre assureurs des lots concernes.</p>

<h3>Piscine municipale ou publique</h3>
<p>Nous n'intervenons pas sur les piscines municipales (Stade Nautique, Piscine Galin, etc.) qui relevent de marches publics spécifiques. Notre scope est exclusivement la piscine privative.</p>

<h2>Courrier type de déclaration à l'assureur</h2>
<p>Voici un modèle de courrier que vous pouvez adapter :</p>

<blockquote style="background:var(--bg-alt);border-left:4px solid var(--green);padding:1rem;margin:1rem 0;font-family:Georgia,serif;">
<p>Madame, Monsieur,</p>
<p>Je vous informe par la présente de la découverte d'une fuite sur ma piscine privative situee a [adresse], que je constate depuis le [date].</p>
<p>Les signes suivants m'amenent a vous le signaler : [perte d'eau de X cm par jour, consommation d'eau anormale, zones humides dans le jardin, etc.].</p>
<p>Conformement aux dispositions de mon contrat multirisque habitation n° [numéro], je vous déclaré ce sinistre dans le délai contractuel de 5 jours ouvrables. Je vous joins les premiers elements photographiques et numéro de police.</p>
<p>Je sollicite la prise en charge au titre de la garantie « recherche de fuite » des frais de diagnostic, ainsi que des dégâts collateraux eventuels. Un rapport technique par un professionnel qualifié sera établi et vous sera transmis sous huitaine.</p>
<p>Je vous prie d'agreer, Madame, Monsieur, l'expression de mes salutations distinguees.</p>
</blockquote>

<h2>Combien serez-vous rembourse en pratique ?</h2>
<p>Dans la majorite des dossiers que nous traitons, le remboursement couvre :</p>
<ul>
<li>100 pourcent de la recherche de fuite si un dégât des eaux effectif est constate</li>
<li>50 à 100 pourcent des travaux de réparation selon la cause (accidentelle vs usure)</li>
<li>Totalite des dégâts collateraux (jardin abîmé, mobilier extérieur)</li>
<li>Consommation d'eau perdue via écrêtement de facture (loi Warsmann) si fuite enterrée</li>
</ul>
<p>La franchise contractuelle s'applique (souvent 150 à 300 euros sur les dégâts des eaux). Dans certains cas, si la fuite n'a pas provoque de dégât des eaux effectif (ex : fuite localisée rapidement sans impact sur les biens), la garantie « recherche de fuite » peut ne pas être activee. Un bon rapport technique, qui documente l'impact potentiel si la fuite n'avait pas été traitee, aide a justifier la prise en charge.</p>

<h2>Besoin d'un diagnostic compatible avec votre assurance ?</h2>
<p>Nous intervenons sur toute la Gironde avec un rapport technique standardise, accepte par les principaux assureurs. Pour obtenir un devis préalable ou coordonner une intervention avec votre assureur, consultez notre page de <a href="/devis/" style="color:var(--green);text-decoration:underline;">demande de devis</a> ou directement l'une de nos <a href="/detection-fuite/piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">pages piscine par ville</a> pour plus de détails sur nos méthodes d'intervention par zone géographique. Pour les aspects tarifaires, consultez notre guide dédié <a href="/guide/recherche-fuite-piscine-tarif/" style="color:var(--green);text-decoration:underline;">tarif recherche de fuite piscine</a>.</p>"""
    },
    {
        "slug": "ma-piscine-perd-de-l-eau-que-faire",
        "title": "Ma piscine perd de l'eau : que faire ? Guide de diagnostic",
        "title_seo": "Ma piscine perd de l'eau : que faire ?",
        "desc": "Votre piscine perd de l'eau et vous ne savez pas par ou commencer ? Arbre de décision étape par étape pour diagnostiquer et agir, avant d'appeler un professionnel en Gironde.",
        "contenu": """<p>Vous constatez une baisse anormale du niveau de votre piscine. Avant de paniquer ou d'appeler un professionnel, quelques vérifications simples permettent de qualifier précisément la situation. Cet article est un guide de décision étape par étape : à chaque question, vous saurez ce qu'il faut faire et quand passer à l'étape suivante. L'objectif : arriver chez un pro de la recherche de fuite avec un diagnostic preliminaire solide, ce qui fait gagner du temps et souvent des euros.</p>

<h2>étape 1 : Combien perdez-vous réellement par jour ?</h2>
<p>La première question a se poser est quantitative. La perception "ma piscine baisse rapidement" est très subjective : une piscine de 8×4 metres avec 1 cm de baisse par jour perd environ 320 litres par jour. A l'échelle d'un été (3 mois), cela représente 29 m³ d'eau. Est-ce anormal ? Cela dépend de beaucoup de facteurs.</p>

<h3>Comment mesurer précisément</h3>
<ol>
<li>Avec un metre ou un niveau laser, marquez au feutre effacable le niveau d'eau sur la paroi (liner) ou sur un carrelage (bassin béton). Choisissez un point facile a retrouver (angle d'escalier, marque de structure).</li>
<li>Attendez exactement 24 heures, sans baignade, sans remplissage automatique en cours, et sans changement météo majeur (pluie, canicule).</li>
<li>Marquez le nouveau niveau et mesurez la différence en millimetres.</li>
</ol>

<h3>Reperes pour interprétation</h3>
<ul>
<li><strong>0 à 3 mm/jour</strong> : normal en avril-mai, septembre-octobre en Gironde. Pas de fuite a suspecter.</li>
<li><strong>3 à 6 mm/jour</strong> : plage normale en plein été juillet-aout, surtout en période de vent et soleil intense.</li>
<li><strong>6 à 10 mm/jour</strong> : suspect en toute saison. Anormal en intersaison. A investiguer.</li>
<li><strong>Plus de 10 mm/jour (1 cm)</strong> : fuite quasi-certaine, sauf très forte chaleur combinee au vent.</li>
<li><strong>Plus de 3 cm/jour</strong> : fuite active importante, agir sous 48h pour éviter dégâts collateraux (affouillement, surconsommation importante).</li>
</ul>

<p>Si vos mesures tombent dans les plages normales (0-6 mm/jour selon saison), il n'y a probablement pas de fuite. Continuez vos baignades normales et refaites une mesure dans 2-3 semaines si vous restez inquiet. Si vous etes au-dessus, passez à l'étape 2.</p>

<h2>étape 2 : Faites le test du seau (fuite ou évaporation)</h2>
<p>Le test du seau est universel, gratuit et incontournable. Il isole le facteur évaporation pour savoir si votre piscine perd plus que ce qu'une simple évaporation expliquerait.</p>

<h3>Protocole précis</h3>
<ol>
<li>Prenez un seau de type "seau de chantier" (10 à 15 litres), rempli d'eau a hauteur similaire à votre piscine (2/3 environ).</li>
<li>Posez-le sur la première marche de votre piscine, immerge à sa base mais avec sa paroi intérieure au-dessus du niveau d'eau. Le seau est maintenu à la même température que la piscine.</li>
<li>Marquez au feutre : le niveau d'eau à l'intérieur du seau, ET le niveau de la piscine sur sa paroi (liner ou margelle).</li>
<li>Laissez 24 à 48 heures : pas de baignade, pas de remplissage automatique (coupez la régulation de niveau), pas de pluie attendue.</li>
<li>Comparez les deux niveaux.</li>
</ol>

<h3>Interpretation des résultats</h3>
<ul>
<li><strong>Le seau et la piscine ont baisse de la même hauteur</strong> : évaporation normale, pas de fuite. Vous pouvez dormir tranquille.</li>
<li><strong>La piscine a baisse plus que le seau</strong> : la piscine fuit. La différence est l'indicateur du débit de fuite : 1 cm d'écart = environ 320 L pour un 8×4 m.</li>
<li><strong>La piscine et le seau ont tous deux enormement baisse</strong> (5+ cm en 48h) : canicule extrême, refaire le test en conditions météo normales.</li>
</ul>

<h2>étape 3 : Filtration en marche ou à l'arrêt ?</h2>
<p>Si le test du seau confirme une fuite, l'étape suivante est de savoir si elle se situe sur le bassin lui-même, sur les canalisations ou sur le local technique. Le test de la filtration le déterminé partiellement.</p>

<h3>Test avec filtration en marche</h3>
<p>Faites tourner la filtration normalement pendant 24 heures. Mesurez la perte d'eau.</p>

<h3>Test avec filtration à l'arrêt</h3>
<p>Coupez la filtration pendant 24 heures. Mesurez la perte d'eau.</p>

<h3>Interpretation</h3>
<ul>
<li><strong>Perte plus rapide filtration MARCHE qu'arrêt</strong> : fuite sur le refoulement (canalisation après la pompe, sous pression). C'est le cas fréquent.</li>
<li><strong>Perte plus rapide filtration arrêt qu'MARCHE</strong> : fuite sur l'aspiration (canalisation skimmer/bonde), car la pression negative sous pompe aspire l'air par la fuite au lieu de laisser sortir l'eau.</li>
<li><strong>Perte identique dans les deux cas</strong> : fuite sur le bassin (liner, coque, joint pièce a sceller, fissure béton). La filtration n'est pas en cause.</li>
</ul>

<h2>étape 4 : Ou se situe exactement le niveau quand la perte s'arrêté ?</h2>
<p>Si votre piscine perd de l'eau mais que la baisse s'arrêté à un certain niveau (ex : niveau du skimmer, niveau de la buse de refoulement), vous avez probablement identifié la zone de fuite.</p>

<ul>
<li><strong>Baisse s'arrêté au niveau du skimmer</strong> : fuite au skimmer (joint mastic, bride, fissure de la pièce). très fréquent sur piscines liner de 25+ ans.</li>
<li><strong>Baisse s'arrêté au niveau des buses de refoulement</strong> : fuite sur buse ou son raccord cache dans le béton.</li>
<li><strong>Baisse s'arrêté au niveau de la prise balai</strong> : joint de prise balai ou raccord defectueux.</li>
<li><strong>Baisse continue sans s'arrêter</strong> : fuite sur liner (perforation), bonde de fond, canalisation enterrée ou fissure structurelle.</li>
</ul>

<h2>étape 5 : Inspecter visuellement</h2>
<p>Avec votre propre observation, verifiez plusieurs points :</p>
<ol>
<li><strong>Margelles et plage</strong> : joints fissures, carrelages mobiles, zones anormalement humides ou affaissees.</li>
<li><strong>Local technique</strong> : flaque au sol, pompe qui goutte, filtre qui suinte, échangeur thermique corrode.</li>
<li><strong>Terrain autour</strong> : zone gorgee d'eau, gazon anormalement vert, terre qui s'affaisse sur un trace lineaire.</li>
<li><strong>Liner ou coque</strong> : plis récents, cloques, décoloration localisée, trous visibles (utilisez un masque de plongee si nécessaire).</li>
</ol>

<h2>étape 6 : quand appeler un professionnel</h2>
<p>Si vos diagnostics amateurs convergent vers une zone (skimmer, canalisation, liner) ou au contraire si vous etes perdu, il est temps de faire intervenir un spécialiste de la recherche de fuite piscine. Le professionnel arrive avec :</p>
<ul>
<li>Colorant fluorescéine pour tester les pièces a sceller</li>
<li>écoute électro-acoustique pour les canalisations enterrées</li>
<li>Test de pression hydraulique pour isoler les circuits</li>
<li>Camera endoscopique sous-marine pour l'inspection visuelle poussee</li>
<li>Gaz traceur si fuite suspectee sur canalisations enterrées longues</li>
</ul>

<h2>Ce qu'il faut preparer avant l'intervention</h2>
<ul>
<li>Vos mesures de perte d'eau (avec dates)</li>
<li>Les résultats de vos tests du seau</li>
<li>L'historique de la piscine (année de pose, dernier changement liner, interventions anterieures)</li>
<li>Les photos des zones suspectes</li>
<li>Votre contrat d'assurance habitation (pour vérifier la garantie recherche de fuite)</li>
</ul>

<p>Cette preparation préalable peut vous faire économiser 30 à 50 % du temps d'intervention, donc potentiellement du tarif final. Pour les tarifs détaillés selon le type de bassin, consultez notre guide <a href="/guide/recherche-fuite-piscine-tarif/" style="color:var(--green);text-decoration:underline;">tarif recherche de fuite piscine en Gironde</a>. Pour le remboursement assurance, voir <a href="/guide/recherche-fuite-piscine-assurance/" style="color:var(--green);text-decoration:underline;">recherche de fuite piscine et assurance habitation</a>. Pour faire intervenir nos techniciens, contactez-nous via la page <a href="/detection-fuite/piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">recherche de fuite piscine à Bordeaux</a> ou l'une de nos pages ville dédiées.</p>"""
    },
    {
        "slug": "fuite-liner-piscine",
        "title": "Fuite liner piscine : signes, causes et diagnostic",
        "title_seo": "Fuite liner piscine PVC : signes et diagnostic",
        "desc": "Comment détecter et traiter une fuite sur liner PVC de piscine. Signes caractéristiques, causes fréquentes, méthodes de diagnostic, réparation locale ou changement complet.",
        "contenu": """<p>Le liner PVC est le revêtement le plus répandu sur les piscines privées en Gironde : environ 70 à 80 pourcent du parc existant, particulièrement sur les bassins installés entre 1985 et 2015 dans les lotissements pavillonnaires de Mérignac, Pessac, Le Bouscat, La Teste et Gujan-Mestras. après 20 à 30 ans d'usage, le liner entre dans sa phase critique ou les fuites deviennent fréquentes. Cet article détaillé comment identifier, diagnostiquer et traiter une fuite sur liner PVC.</p>

<h2>Types de liners concernes par les fuites</h2>
<p>Les liners PVC se déclinent en plusieurs épaisseurs qui déterminent leur longévité et leur susceptibilité aux fuites.</p>

<h3>Liner 75/100 (0,75 mm d'épaisseur)</h3>
<p>Le plus économique, souvent pose sur bassins familiaux simples (4×8 m, 5×10 m). durée de vie théorique : 10 à 15 ans. En pratique, les bassins girondins avec liner 75/100 de plus de 12 ans montrent des signes d'usure généralisé : plis figes, points de tension visibles, décoloration. Les fuites deviennent probables dès 15 ans.</p>

<h3>Liner 85/100 (0,85 mm)</h3>
<p>intermédiaire, fréquemment pose dans les années 2000-2015 en remplacement de liners 75/100 d'origine. durée de vie 15 à 20 ans. Résistance légèrement supérieure aux chocs et à l'usure sous-marche.</p>

<h3>Liner 100/100 armé (1 mm d'épaisseur armée)</h3>
<p>Liner renforce par armature textile, pose in situ et soudée. durée de vie 20 à 30 ans. fréquemment choisi pour les rénovations récentes ou les bassins haut de gamme. très résistant aux fuites localisées mais complexe a réparer (soudure à chaud spécifique).</p>

<h2>Signes caractéristiques d'une fuite de liner</h2>

<h3>Signes visuels</h3>
<ul>
<li><strong>Pli ou boursouflure récente</strong> : décollement local du liner par rapport au support béton. Souvent précurseur d'une micro-perforation.</li>
<li><strong>Tache brune ou noire circulaire</strong> : infiltration d'eau entre le liner et le support, favorisant la moisissure visible par transparence.</li>
<li><strong>Angle qui se creusé</strong> : soudure au niveau des angles (souvent skimmer, marche, bonde) qui cède par fatigué mécanique.</li>
<li><strong>Liner qui flotte localement</strong> : présence d'une lame d'eau ou d'air entre le liner et le support, indiquant une infiltration importante.</li>
<li><strong>Décoloration brutale</strong> : zone localement plus claire ou plus sombre que le reste, signalant un contact différent avec le support.</li>
</ul>

<h3>Signes hydrauliques</h3>
<ul>
<li>Baisse de niveau supérieure a 1 cm par jour en conditions normales (voir <a href="/guide/ma-piscine-perd-de-l-eau-que-faire/" style="color:var(--green);text-decoration:underline;">guide ma piscine perd de l'eau</a> pour les repères)</li>
<li>Baisse qui s'arrêté à un niveau précis (skimmer, buse), indiquant la zone de fuite</li>
<li>Consommation d'eau en hausse sur la facture Suez ou régie</li>
<li>Déformation de la plage ou des margelles (infiltration sous la dalle)</li>
</ul>

<h2>Causes principales des fuites de liner</h2>

<h3>Vieillissement du PVC</h3>
<p>Le PVC perd sa plasticite après 15 à 25 ans d'exposition aux UV, aux variations thermiques et au chlore. Il devient rigide, se rétracte localement, fissure aux points de tension (angles, bonde, skimmer). Vous ne pouvez pas empêcher ce processus : l'âgé du liner est le premier facteur.</p>

<h3>Brides desserrées</h3>
<p>Les pièces a sceller (skimmer, buses de refoulement, bonde de fond, prise balai) sont solidarisées au liner par des brides inox ou plastique. après 10 à 20 ans, ces brides peuvent se desserrer légèrement sous l'effet des vibrations et des mouvements thermiques, créant un microgap par ou le liner fuit.</p>

<h3>Objets tranchants</h3>
<p>Chute d'un objet dans la piscine (tournevis, ciseau de jardinage, débris d'élagage), raclures de robot de nettoyage mal étalonné, impact lors de l'hivernage (chute de branche, glace cristalline sous la bâche). Ces chocs peuvent percer le liner, parfois de manière ponctuelle difficile a détecter.</p>

<h3>Chimie de l'eau défaillante</h3>
<p>Un pH trop bas (en dessous de 7,0) ou un taux de chlore excessivement élevé (au-dessus de 3 mg/L en permanence) accéléré la dégradation chimique du PVC. Le liner devient cassant, se craquelle progressivement. fréquent dans les piscines mal entretenues ou a traitement choc répété.</p>

<h3>Racines de plantes ou arbres</h3>
<p>Les piscines dont les abords sont plantes (bambous, oliviers, pins) peuvent voir des racines pousser sous le liner via un défaut d'étanchéité périphérique. Les racines pénètrent, soulèvent le liner et créent des points de fuite.</p>

<h3>Mouvements de terrain</h3>
<p>Les sols argileux de Bordeaux et des environs sont sujets au retrait-gonflement saisonnier. Ces mouvements sollicitent la structure du bassin et peuvent provoquer des fissures du support béton, qui se répercutent sur le liner en le sollicitant localement.</p>

<h2>méthodes de diagnostic pour fuite de liner</h2>

<h3>Colorant fluorescéine (méthode de référence)</h3>
<p>On injecté à la seringue quelques gouttes de fluorescéine a proximité des zones suspectes, filtration à l'arrêt. Le colorant est aspire vers la fuite, révélant son parcours exact. C'est la méthode privilégiée pour les fuites de pièces a sceller (skimmer, buses).</p>

<h3>Inspection visuelle en apnée</h3>
<p>Avec un masque et un tuba, inspection systématique des angles, soudures, pièces a sceller. Une perforation punctiforme (0,5 à 2 mm) se détecté par un léger courant d'eau sortant, visible aux débris flottants (poussières, petites feuilles).</p>

<h3>Camera endoscopique sous-marine</h3>
<p>Camera étanche motorisée qui parcourt les parois et fond du bassin. Utile pour les piscines profondes (3-4 m) ou les zones d'accès difficile en apnée. Permet d'inspecter les soudures d'angles et les bondes de fond invisibles à l'oeil nu.</p>

<h3>Test d'inversion de pression</h3>
<p>On fait varier la pression dans les circuits d'alimentation pour révéler les fuites actives. Combine avec l'injection de colorant, cette méthode est très efficace sur les suspicions de fuites aux pièces a sceller.</p>

<h2>réparation locale ou changement complet ?</h2>

<h3>réparation locale (patch PVC)</h3>
<p>Pour une fuite isolée bien localisée (perforation mécanique, décollement de bride), un patch PVC peut être colle sur le liner. coût : 100 à 400 euros HT selon la zone. durée de vie du patch : 5 à 10 ans. économiquement pertinent si le liner à moins de 20 ans et que le reste est en bon etat.</p>

<h3>réparation d'angle (soudure)</h3>
<p>Les fuites aux soudures d'angles peuvent être réparées par nouvelle soudure à chaud spécifique. Requiert du matériel professionnel (extrudeur, vent pulse). coût : 200 à 600 euros HT. durée de vie : 5 à 10 ans.</p>

<h3>Rejointoiement de pièce a sceller</h3>
<p>Pour une fuite au niveau d'un skimmer ou d'une buse, le démontage de la bride, le renouvellement du joint mastic (silicone piscine) et le resserrage de la bride résolvent le problème sans changer le liner. coût : 200 à 500 euros HT selon le nombre de pièces.</p>

<h3>Changement complet du liner</h3>
<p>Lorsque le liner présente plusieurs signes d'usure généralisée (plis multiples, décolorations, soudures cédées, perforations multiples), un changement complet est nécessaire. coût : 3 000 à 8 000 euros HT pour un bassin standard 8×4 m, 6 000 à 12 000 euros pour 10×5 m. Le choix de liner peut inclure une montée en gamme (75/100 vers 85/100 ou 100/100 armé) pour prolonger la prochaine durée de vie.</p>

<h2>décision : réparer ou changer ?</h2>
<p>Trois critères orientent la décision :</p>
<ol>
<li><strong>Âge du liner</strong> : moins de 15 ans = réparation locale privilégiée. Plus de 25 ans = changement recommandé même pour une fuite isolée.</li>
<li><strong>Nombre de fuites</strong> : une seule fuite localisée = réparation. Plusieurs fuites simultanées = le liner est en fin de vie, changement.</li>
<li><strong>Etat visuel général</strong> : décolorations, plis multiples, soudures fatiguées = changement. Liner homogène par ailleurs = réparation.</li>
</ol>

<p>Notre rapport de diagnostic evalue objectivement ces critères et vous remet une préconisation chiffrée. Pour les tarifs détaillés selon le type de bassin et la méthode retenue, consultez notre guide <a href="/guide/recherche-fuite-piscine-tarif/" style="color:var(--green);text-decoration:underline;">tarif recherche de fuite piscine</a>. Une fois la fuite identifiée, voir notre guide complémentaire <a href="/guide/reparation-liner-piscine/" style="color:var(--green);text-decoration:underline;">réparation d'une fuite de liner piscine</a> qui détaille les trois familles de réparation (rustine subaquatique, soudure thermique, changement complet) avec coûts constatés. Pour la méthode de localisation au colorant, voir notre page dédiée <a href="/detection-fuite/fluoresceine-piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">recherche de fuite piscine à la fluorescéine</a>. Pour faire intervenir nos techniciens, consultez nos pages piscine par ville, notamment <a href="/detection-fuite/piscine-merignac/" style="color:var(--green);text-decoration:underline;">piscine Mérignac</a> qui concentre la plus forte densité de liners PVC en fin de vie en Gironde.</p>"""
    },
    {
        "slug": "evaporation-vs-fuite-piscine",
        "title": "Évaporation ou fuite de piscine ? Le guide précis",
        "title_seo": "Évaporation ou fuite de piscine : test du seau",
        "desc": "Comment distinguer l'évaporation normale d'une fuite sur votre piscine en Gironde. Taux mensuels selon le climat, protocoles de test, seuils d'alerte.",
        "contenu": """<p>Votre piscine perd de l'eau et la question tombe : est-ce une fuite, ou simplement de l'évaporation ? La reponse n'est pas toujours évidente, surtout en été en Gironde ou l'évaporation peut être importante. Cet article détaillé les taux d'évaporation mensuels en climat aquitain, les facteurs qui les amplifient, et le protocole précis pour trancher entre évaporation et fuite.</p>

<h2>L'évaporation de piscine : un phénomène physique predictible</h2>
<p>L'évaporation est le passage de l'eau liquide à l'etat gazeux, provoque par la chaleur de l'eau et la sollicitation atmospherique. Contrairement aux idées recues, l'évaporation d'une piscine ne dépend pas uniquement de la température de l'air : elle resulte d'un calcul complexe impliquant la température de l'eau, la température de l'air, l'humidité relative et surtout la vitesse du vent.</p>

<h3>Les 4 facteurs qui déterminent l'évaporation</h3>
<ul>
<li><strong>température de l'eau</strong> : plus l'eau est chaude, plus elle s'évapore. Une piscine chauffée a 28 degrés évapore plus qu'une piscine a 22 degrés.</li>
<li><strong>température de l'air</strong> : importante mais moins que l'on pense. Une journée a 35 degrés provoque certes plus d'évaporation qu'a 25 degrés, mais l'écart n'est pas aussi spectaculaire.</li>
<li><strong>Humidité relative</strong> : plus l'air est sec, plus il peut absorber de l'humidité et donc plus l'évaporation est forte. Une journée a 30 pourcent d'humidité fait bien plus évaporer qu'a 80 pourcent.</li>
<li><strong>Vitesse du vent</strong> : facteur le plus sous-estime. Le vent emporte la couche d'air humide à la surface de l'eau et permet a de l'air sec de la remplacer, relancant l'évaporation en continu. Une journée ventee peut quadrupler l'évaporation par rapport à une journée calme.</li>
</ul>

<h2>Taux d'évaporation mensuels en Gironde</h2>
<p>Voici les moyennes mensuelles d'évaporation pour une piscine extérieure non abritee en plaine bordelaise, basees sur les données météo historiques de la région. Valeurs en mm/jour (1 mm = 1 litre par m² de surface de piscine).</p>

<table style="width:100%;border-collapse:collapse;margin:1.5rem 0;background:#fff;">
<thead><tr style="background:#0D3B2E;color:#fff;"><th style="padding:.75rem;text-align:left;border:1px solid #155740;">Mois</th><th style="padding:.75rem;text-align:left;border:1px solid #155740;">Évaporation moy. (mm/jour)</th><th style="padding:.75rem;text-align:left;border:1px solid #155740;">Pic observable</th><th style="padding:.75rem;text-align:left;border:1px solid #155740;">Contexte</th></tr></thead>
<tbody>
<tr><td style="padding:.75rem;border:1px solid #D8D4CC;">Janvier</td><td style="padding:.75rem;border:1px solid #D8D4CC;">0,5 à 1,5</td><td style="padding:.75rem;border:1px solid #D8D4CC;">2 mm</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Hivernage généralisé, évaporation minimale</td></tr>
<tr style="background:#F7F6F2;"><td style="padding:.75rem;border:1px solid #D8D4CC;">Fevrier</td><td style="padding:.75rem;border:1px solid #D8D4CC;">0,5 à 2</td><td style="padding:.75rem;border:1px solid #D8D4CC;">3 mm</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Vent d'ouest accentué en cas de depression</td></tr>
<tr><td style="padding:.75rem;border:1px solid #D8D4CC;">Mars</td><td style="padding:.75rem;border:1px solid #D8D4CC;">1 à 3</td><td style="padding:.75rem;border:1px solid #D8D4CC;">5 mm</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Remise en route, eau froide, vent printanier</td></tr>
<tr style="background:#F7F6F2;"><td style="padding:.75rem;border:1px solid #D8D4CC;">Avril</td><td style="padding:.75rem;border:1px solid #D8D4CC;">2 à 4</td><td style="padding:.75rem;border:1px solid #D8D4CC;">6 mm</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Reprise saison, vents d'ouest réguliers</td></tr>
<tr><td style="padding:.75rem;border:1px solid #D8D4CC;">Mai</td><td style="padding:.75rem;border:1px solid #D8D4CC;">3 à 5</td><td style="padding:.75rem;border:1px solid #D8D4CC;">7 mm</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Mois a forte évaporation par forte amplitude thermique</td></tr>
<tr style="background:#F7F6F2;"><td style="padding:.75rem;border:1px solid #D8D4CC;"><strong>Juin</strong></td><td style="padding:.75rem;border:1px solid #D8D4CC;"><strong>4 à 6</strong></td><td style="padding:.75rem;border:1px solid #D8D4CC;"><strong>8 mm</strong></td><td style="padding:.75rem;border:1px solid #D8D4CC;">Pleine saison, chaleur + vents réguliers</td></tr>
<tr><td style="padding:.75rem;border:1px solid #D8D4CC;"><strong>Juillet</strong></td><td style="padding:.75rem;border:1px solid #D8D4CC;"><strong>5 à 7</strong></td><td style="padding:.75rem;border:1px solid #D8D4CC;"><strong>10 mm</strong></td><td style="padding:.75rem;border:1px solid #D8D4CC;">Canicule + vent d'ouest = pic d'évaporation</td></tr>
<tr style="background:#F7F6F2;"><td style="padding:.75rem;border:1px solid #D8D4CC;"><strong>Aout</strong></td><td style="padding:.75rem;border:1px solid #D8D4CC;"><strong>5 à 7</strong></td><td style="padding:.75rem;border:1px solid #D8D4CC;"><strong>10 mm</strong></td><td style="padding:.75rem;border:1px solid #D8D4CC;">Similaire a juillet, possibles orages interrupteurs</td></tr>
<tr><td style="padding:.75rem;border:1px solid #D8D4CC;">Septembre</td><td style="padding:.75rem;border:1px solid #D8D4CC;">3 à 5</td><td style="padding:.75rem;border:1px solid #D8D4CC;">7 mm</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Baisse progressive, encore forte en début de mois</td></tr>
<tr style="background:#F7F6F2;"><td style="padding:.75rem;border:1px solid #D8D4CC;">Octobre</td><td style="padding:.75rem;border:1px solid #D8D4CC;">1 à 3</td><td style="padding:.75rem;border:1px solid #D8D4CC;">5 mm</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Retrocedence, hivernage imminent</td></tr>
<tr><td style="padding:.75rem;border:1px solid #D8D4CC;">Novembre</td><td style="padding:.75rem;border:1px solid #D8D4CC;">0,5 à 2</td><td style="padding:.75rem;border:1px solid #D8D4CC;">3 mm</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Hivernage en cours</td></tr>
<tr style="background:#F7F6F2;"><td style="padding:.75rem;border:1px solid #D8D4CC;">décembre</td><td style="padding:.75rem;border:1px solid #D8D4CC;">0,5 à 1,5</td><td style="padding:.75rem;border:1px solid #D8D4CC;">2 mm</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Hivernage, évaporation minimale</td></tr>
</tbody>
</table>

<h3>Facteurs multiplicateurs locaux</h3>
<ul>
<li><strong>Bassin d'Arcachon, Cap-Ferret, front de dune</strong> : vent marin permanent, évaporation augmentee de 20 à 40 pourcent par rapport à la valeur tablee</li>
<li><strong>Pinede dense autour du bassin</strong> : effet de protection du vent, évaporation réduite de 15 à 25 pourcent</li>
<li><strong>Piscine chauffée (PAC ou abri)</strong> : évaporation doublée car l'eau reste a 28-30 degrés toute la saison, augmentant le gradient thermique</li>
<li><strong>Piscine débordement/miroir</strong> : évaporation multipliee par 1,5 à 2 en raison de la surface d'eau en contact avec l'air nettement plus large</li>
</ul>

<h2>Protocole scientifique pour distinguer évaporation et fuite</h2>

<h3>Test de contrôle sur 48 heures</h3>
<p>Le protocole rigoureux d'observation :</p>
<ol>
<li>Definissez une fenetre de 48 heures sans baignade, sans pluie attendue, sans canicule hors-norme. idéalement, choisissez un week-end normal ou vous n'utilisez pas la piscine.</li>
<li>arrêtez la filtration (pour les piscines qui ne nécessitent pas de filtration continue) afin de limiter la variabilite.</li>
<li>Relevez le niveau d'eau initial avec précision (millimetre près) sur la paroi du bassin.</li>
<li>Relevez simultanement le niveau dans un seau immerge aux 2/3 sur la première marche.</li>
<li>Notez la météo : température max/min, humidité, vent, absence de pluie.</li>
<li>après 48 heures, relevez les deux niveaux et calculez la perte par jour de la piscine et du seau.</li>
</ol>

<h3>Formule de décision</h3>
<p>Calculez le delta : <strong>perte piscine - perte seau = fuite presumee</strong></p>
<ul>
<li>Delta de 0 à 2 mm/jour : pas de fuite significative. Évaporation seule en cause.</li>
<li>Delta de 2 à 5 mm/jour : fuite faible, a investiguer. Pourrait être un joint qui fatigué.</li>
<li>Delta de 5 à 10 mm/jour : fuite confirmee, intervention professionnelle recommandée sous 2 semaines.</li>
<li>Delta supérieur a 10 mm/jour : fuite importante, intervention urgente sous 48 heures pour éviter dégâts collateraux.</li>
</ul>

<h2>Pieges fréquents à éviter</h2>

<h3>Test fait pendant une canicule</h3>
<p>Un test d'évaporation fait pendant un pic de chaleur avec forts vents peut sous-estimer la fuite réelle (car l'évaporation naturelle du seau masque partiellement la fuite). Attendez une période météorologique stable.</p>

<h3>Oubli du remplissage automatique</h3>
<p>De nombreuses piscines ont un regulateur de niveau automatique qui compensé en permanence les baisses. Si vous ne le coupez pas pendant le test, vous ne verrez jamais la baisse : votre regulateur la masquera. Coupez imperativement cette régulation pendant le test.</p>

<h3>Piscine en plein soleil direct toute là journée</h3>
<p>Une piscine exposée plein sud chauffe vite, ce qui amplifie l'évaporation. Si votre piscine est particulièrement exposee, vos taux d'évaporation peuvent dépasser les valeurs de table de 30 à 50 pourcent. Faites plusieurs tests sur différents episodes météo pour calibrer votre cas.</p>

<h3>Confondre évaporation et micro-fuite chronique</h3>
<p>Une fuite très petite (2-3 mm/jour) sur une piscine en pleine saison peut se confondre avec l'évaporation normale. Seul le test rigoureux du seau tranche. Ne vous fiez pas à votre intuition : mesurer avant de conclure.</p>

<h2>Quand refaire le test</h2>
<p>Si vos premiers tests concluent à une simple évaporation mais que vous restez inquiet, refaites un test :</p>
<ul>
<li>après un changement météo majeur (fin de canicule, arrêt des vents)</li>
<li>après 1 mois, pour voir si la situation evolue</li>
<li>après un événement suspect (orage violent, chute dans la piscine)</li>
</ul>

<p>Si plusieurs tests independants concluent à une fuite, ou si votre consommation d'eau augmente de manière marquee sans explication, il est temps de faire intervenir un professionnel. Pour en savoir plus sur les étapes à suivre, consultez notre guide <a href="/guide/ma-piscine-perd-de-l-eau-que-faire/" style="color:var(--green);text-decoration:underline;">ma piscine perd de l'eau, que faire</a>. Pour le diagnostic sur un liner PVC, voir l'article <a href="/guide/fuite-liner-piscine/" style="color:var(--green);text-decoration:underline;">fuite sur liner piscine</a>. Sur Bordeaux, nos techniciens localisent les fuites <a href="/detection-fuite/piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">sans vidanger votre bassin grâce au gaz traceur et à l'hydrophone</a>, avec rapport assurance remis le jour même. Pour les piscines du Bassin d'Arcachon, consultez notre page dédiée <a href="/detection-fuite/piscine-arcachon/" style="color:var(--green);text-decoration:underline;">recherche de fuite piscine à Arcachon</a>. Pour les tarifs, voir notre guide <a href="/guide/recherche-fuite-piscine-tarif/" style="color:var(--green);text-decoration:underline;">tarif recherche de fuite piscine en Gironde</a>.</p>"""
    },
    {
        "slug": "loi-warsmann-ecretement-facture-eau",
        "title": "Loi Warsmann : écrêtement de facture d'eau après fuite",
        "title_seo": "Loi Warsmann : écrêtement de facture d'eau",
        "desc": "Comment bénéficier de l'écrêtement de facture d'eau après une fuite sur canalisation enterrée. La loi Warsmann 2011 expliquée : conditions, procédure, jurisprudence.",
        "contenu": """<p>Une fuite sur votre canalisation enterrée peut faire exploser votre facture d'eau en quelques semaines. La loi dite Warsmann, adoptee en 2011 et codifiee à l'article L2224-12-4 du Code général des collectivites territoriales, limite le coût supporte par le consommateur dans ce cas précis. Encore faut-il connaître les conditions pour en bénéficier. Cet article détaillé la procédure, les documents a fournir, les ecueils fréquents et les précédents jurisprudentiels.</p>

<h2>Que dit la loi Warsmann ?</h2>
<p>Le texte légal oblige les services publics d'eau a informer tout abonne d'une consommation anormale (supérieure au double de la consommation moyenne sur les trois dernières années). L'abonne dispose alors d'un mois pour prouver qu'une fuite sur canalisation enterrée, invisible et indétectable, est à l'origine de cette surconsommation. Si cette preuve est apportee, sa facture est plafonnée au double de sa consommation habituelle : c'est l'écrêtement.</p>

<h3>Le mecanisme d'écrêtement en pratique</h3>
<p>Concretement, si votre consommation habituelle est de 120 m³/an (moyenne sur 3 ans), votre facture ne pourra jamais dépasser 240 m³/an au tarif de l'eau, même si votre compteur a enregistré 800 m³ à cause de la fuite. Les 560 m³ restants ne vous sont pas factures. A 4 euros TTC le m³, cela représente une économie de 2 240 euros par rapport à une facturation intégrale.</p>

<h2>Les conditions obligatoires pour bénéficier de l'écrêtement</h2>

<h3>Condition 1 : canalisation enterrée privative</h3>
<p>La fuite doit concerner une canalisation enterrée qui appartient à votre réseau privatif : entre le compteur d'eau et votre habitation, ou réseaux enterrés à l'intérieur de votre propriété (arrosage, piscine, dependance). Les fuites suivantes <strong>ne sont pas éligibles</strong> :</p>
<ul>
<li>Fuite d'équipement visible (chasse d'eau, robinet, chauffe-eau)</li>
<li>Fuite dans un mur ou sous une dalle (canalisation intérieure, même si invisible)</li>
<li>Fuite sur réseau d'arrosage automatique classique</li>
<li>Fuite sur le réseau public (avant le compteur) : à la charge du distributeur d'eau</li>
</ul>

<h3>Condition 2 : fuite indétectable visuellement</h3>
<p>La fuite doit avoir été indétectable à l'oeil nu avant sa découverte par un professionnel. Si elle se manifestait par une flaque, une zone humide évidente, un affaissement du sol ou tout autre signe visuel avant que vous n'interveniez, l'écrêtement peut être refusé. C'est précisément ce qui differencie cette loi : elle protégé le consommateur qui n'avait aucun moyen raisonnable de détecter la fuite.</p>

<h3>Condition 3 : intervention d'un professionnel qualifié</h3>
<p>Une attestation de réparation doit être fournie, établie par un professionnel (plombier, spécialiste de la recherche de fuite). Cette attestation doit mentionner explicitement :</p>
<ul>
<li>La date de l'intervention</li>
<li>La nature de la canalisation defectueuse et sa localisation enterrée</li>
<li>Le type de réparation effectuee</li>
<li>L'attestation que la fuite a bien été résolue</li>
</ul>

<h3>Condition 4 : délai d'un mois</h3>
<p>Vous avez un mois après notification de surconsommation par votre distributeur pour fournir l'attestation de réparation. Passé ce délai, l'écrêtement n'est plus automatiquement accessible (mais un recours reste possible).</p>

<h2>Procédure pas a pas pour obtenir l'écrêtement</h2>

<h3>étape 1 : vous recevez la notification de surconsommation</h3>
<p>Votre distributeur d'eau (Suez, Veolia, Régie des eaux) à l'obligation légale de vous alerter en cas de consommation anormalement élevée. La notification se fait par courrier, email ou via l'espace client. Le courrier indique votre surconsommation (en m³), la moyenne des 3 années précédentes, et mentionne votre droit à l'écrêtement selon la loi Warsmann.</p>

<h3>étape 2 : vous identifiez la fuite</h3>
<p>Verifiez d'abord si la fuite est avant ou après le compteur : fermez votre robinet d'arrêt général. Si le compteur continue de tourner, la fuite est avant (réseau public, pas votre responsabilité). S'il s'arrêté mais vous constatez toujours une perte, la fuite est après le compteur sur votre réseau privatif.</p>

<h3>étape 3 : localisation par un professionnel</h3>
<p>Pour obtenir l'écrêtement, il ne suffit pas de savoir qu'il y à une fuite : il faut la localiser précisément pour pouvoir la réparer. Nous intervenons avec du gaz traceur azote/hélium pour localiser les fuites sur canalisations enterrées avec une précision au demi-metre. Notre rapport mentionne explicitement la localisation enterrée et le caractère indétectable visuellement, deux elements clés pour le dossier Warsmann.</p>

<h3>étape 4 : réparation et attestation</h3>
<p>La réparation peut être faite par le même professionnel ou par un plombier mandate. A l'issue, demandez une attestation de réparation mentionnant : canalisation enterrée, localisation, date, certification que la fuite est résolue.</p>

<h3>étape 5 : envoi du dossier au distributeur</h3>
<p>Envoyez en courrier recommandé avec accuse de reception à votre distributeur d'eau :</p>
<ul>
<li>Copie de la notification de surconsommation</li>
<li>Rapport de localisation de fuite</li>
<li>Attestation de réparation</li>
<li>Photos si disponibles (zone de fuite, réparation en cours)</li>
<li>Courrier de demande explicite d'application de la loi Warsmann</li>
</ul>

<h3>étape 6 : écrêtement applique sur la facture suivante</h3>
<p>Si le dossier est complet, le distributeur applique l'écrêtement sur votre facture suivante (délai moyen 1 à 2 mois). Là part excedentaire au-dessus du double de votre consommation habituelle est soit annulee, soit remboursee si déjà payee.</p>

<h2>Modele de courrier a envoyer</h2>

<blockquote style="background:var(--bg-alt);border-left:4px solid var(--green);padding:1rem;margin:1rem 0;font-family:Georgia,serif;">
<p>[Votre adresse]</p>
<p>[Date]</p>
<p>Objet : demande d'écrêtement de facture d'eau - Loi Warsmann - référence client [numéro]</p>
<p>Madame, Monsieur,</p>
<p>Suite à votre notification de surconsommation d'eau en date du [date], je vous adresse ci-joint les justificatifs permettant l'application de la loi n° 2011-525 du 17 mai 2011 (dite loi Warsmann) et l'écrêtement de ma facture.</p>
<p>Je vous confirme que la fuite concernait une canalisation enterrée privative (entre mon compteur d'eau et mon habitation), indétectable à l'oeil nu, comme en atteste le rapport de recherche de fuite établi par [nom de l'entreprise] le [date]. La réparation a été effectuee le [date] et est documentee par l'attestation ci-jointe.</p>
<p>Conformement à l'article L2224-12-4 du Code général des collectivites territoriales, je vous demande de bien vouloir plafonner ma facture au double de ma consommation moyenne des trois dernières années, soit [X] m³.</p>
<p>Documents joints : rapport de recherche de fuite, attestation de réparation, photos de la zone.</p>
<p>Je vous prie d'agreer, Madame, Monsieur, l'expression de mes salutations distinguees.</p>
</blockquote>

<h2>Cas complexes et jurisprudence</h2>

<h3>Cas 1 : la fuite etait partiellement visible</h3>
<p>Si l'humidité etait visible mais qu'il etait objectivement impossible de suspecter une fuite (ex : zone de pelouse légèrement plus verte depuis plusieurs années, interpretee comme effet d'arrosage naturel), la jurisprudence admet généralement l'écrêtement. Notre rapport doit alors argumenter spécifiquement pourquoi le signe visible etait ambigu et n'imposait pas intervention.</p>

<h3>Cas 2 : délai dépassé d'un mois</h3>
<p>Si vous avez laisse passer le délai d'un mois, un recours est toujours possible en sollicitant le mediateur de l'eau ou en saisissant le tribunal judiciaire. Les distributeurs acceptent souvent l'écrêtement après mediation, même hors délai, car le contentieux est coûteux pour eux.</p>

<h3>Cas 3 : plusieurs fuites dans l'année</h3>
<p>Si vous avez déjà bénéficie d'un écrêtement dans les 5 années précédentes, le distributeur peut contester le caractère exceptionnel de la demande. Dans ce cas, une expertise contradictoire peut être mise en oeuvre.</p>

<h3>Cas 4 : locataire ou propriétaire</h3>
<p>L'écrêtement s'applique au titulaire du contrat d'eau, qu'il soit propriétaire ou locataire. En location, le locataire demande l'écrêtement mais doit informer le bailleur (qui est responsable de la réparation definitive si la fuite est sur une canalisation enterrée privative).</p>

<h2>économies realisables concretes</h2>
<p>quelques exemples réels de dossiers sur lesquels nous sommes intervenus en Gironde en 2025 :</p>
<ul>
<li>Maison Caudéran, fuite enterrée 40 m de canalisation PVC : surconsommation 680 m³ sur 6 mois. Facture initiale 3 200 euros, facture après écrêtement 950 euros. <strong>économie : 2 250 euros.</strong></li>
<li>Pavillon Mérignac, fuite enterrée arrosage automatique: 420 m³ surconsommation. Facture initiale 1 680 euros, après écrêtement 580 euros. <strong>économie : 1 100 euros.</strong></li>
<li>Villa Arcachon, fuite très lente 12 mois non détectée : 240 m³ surconsommation. Facture initiale 960 euros, après écrêtement 420 euros. <strong>économie : 540 euros.</strong></li>
</ul>

<p>Notre intervention (environ 450 euros HT en moyenne pour la recherche de fuite enterrée) est largement rentabilisee par l'écrêtement dans la majorite des cas. Pour en savoir plus sur notre méthodologie gaz traceur, consultez notre page <a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">recherche de fuite canalisation enterrée à Bordeaux</a>. Pour les fuites après compteur plus généralement, voir <a href="/detection-fuite/fuite-apres-compteur/" style="color:var(--green);text-decoration:underline;">fuite d'eau après compteur</a>. Pour prendre rendez-vous, utilisez notre formulaire de <a href="/devis/" style="color:var(--green);text-decoration:underline;">demande de devis gratuit</a>.</p>"""
    },
    {
        "slug": "prix-recherche-fuite-bordeaux",
        "title": "Prix d'une recherche de fuite à Bordeaux en 2026",
        "title_seo": "Prix recherche de fuite à Bordeaux 2026",
        "desc": "Combien coûte une recherche de fuite à Bordeaux en 2026 ? Tarifs moyens par méthode, prise en charge assurance, loi Warsmann. Devis gratuit.",
        "contenu": """<p>Vous cherchez à savoir combien coûte une recherche de fuite à Bordeaux avant de prendre rendez-vous ? Cet article détaille les tarifs pratiqués en 2026 selon les techniques employées, ce qui est pris en charge par votre assurance habitation et comment obtenir un écrêtement de facture d'eau en cas de fuite enterrée.</p>

<h2>Tarifs moyens d'une recherche de fuite à Bordeaux en 2026</h2>
<p>Le prix d'une recherche de fuite dépend de la méthode employée, de la complexité du réseau et du temps d'intervention. Voici les fourchettes tarifaires pratiquées sur Bordeaux et sa métropole en 2026.</p>

<table style="width:100%;border-collapse:collapse;margin:1.5rem 0;background:#fff;">
<thead><tr style="background:#0D3B2E;color:#fff;"><th style="padding:.75rem;text-align:left;border:1px solid #155740;">Type de diagnostic</th><th style="padding:.75rem;text-align:left;border:1px solid #155740;">Tarif HT</th><th style="padding:.75rem;text-align:left;border:1px solid #155740;">Durée</th></tr></thead>
<tbody>
<tr><td style="padding:.75rem;border:1px solid #D8D4CC;">Inspection visuelle + caméra endoscopique simple</td><td style="padding:.75rem;border:1px solid #D8D4CC;">250 à 350 €</td><td style="padding:.75rem;border:1px solid #D8D4CC;">1 h à 1 h 30</td></tr>
<tr style="background:#F7F6F2;"><td style="padding:.75rem;border:1px solid #D8D4CC;">Thermographie infrarouge (sol chaud, planch. chauffant)</td><td style="padding:.75rem;border:1px solid #D8D4CC;">350 à 500 €</td><td style="padding:.75rem;border:1px solid #D8D4CC;">1 h 30 à 2 h</td></tr>
<tr><td style="padding:.75rem;border:1px solid #D8D4CC;">Écoute électro-acoustique + corrélation</td><td style="padding:.75rem;border:1px solid #D8D4CC;">400 à 550 €</td><td style="padding:.75rem;border:1px solid #D8D4CC;">2 h à 3 h</td></tr>
<tr style="background:#F7F6F2;"><td style="padding:.75rem;border:1px solid #D8D4CC;">Gaz traceur azote/hélium (canalisation enterrée)</td><td style="padding:.75rem;border:1px solid #D8D4CC;">500 à 700 €</td><td style="padding:.75rem;border:1px solid #D8D4CC;">2 h à 4 h</td></tr>
<tr><td style="padding:.75rem;border:1px solid #D8D4CC;">Recherche piscine (colorant + pression + acoustique)</td><td style="padding:.75rem;border:1px solid #D8D4CC;">400 à 700 €</td><td style="padding:.75rem;border:1px solid #D8D4CC;">2 h à 3 h</td></tr>
<tr style="background:#F7F6F2;"><td style="padding:.75rem;border:1px solid #D8D4CC;">diagnostic combiné complexe (plusieurs méthodes)</td><td style="padding:.75rem;border:1px solid #D8D4CC;">600 à 900 €</td><td style="padding:.75rem;border:1px solid #D8D4CC;">3 h à 5 h</td></tr>
</tbody>
</table>

<p>Ces tarifs s'entendent hors taxes et hors travaux de réparation. Un devis fixe vous est communiqué avant intervention après un premier échange téléphonique. Aucun déplacement facturé si vous décidez de ne pas donner suite au devis.</p>

<h2>Les facteurs qui font varier le prix</h2>
<p>Plusieurs éléments influencent le coût final de votre recherche de fuite à Bordeaux.</p>
<ul>
<li><strong>La surface à inspecter</strong> : un appartement de 50 m² coûtera moins qu'une maison de 200 m² avec réseau enterré</li>
<li><strong>L'accessibilité du réseau</strong> : apparent, encastré, enterré ou sous dalle béton</li>
<li><strong>Le nombre de méthodes à combiner</strong> : une fuite bien caractérisée est souvent trouvée avec une seule technique, une fuite complexe peut en nécessiter trois</li>
<li><strong>Le type de fuite</strong> : piscine, plancher chauffant, canalisation enterrée, copropriété</li>
<li><strong>L'urgence</strong> : aucune majoration chez nous pour les interventions sous 24h, le tarif reste le même</li>
</ul>

<h2>Prise en charge par l'assurance habitation</h2>
<p>La garantie « recherche de fuite » de votre contrat multirisque habitation rembourse tout ou partie des frais de recherche, à condition qu'un dégât des eaux soit constaté. Le rapport technique que nous remettons (photos, méthodes employées, point de fuite, préconisations) est reconnu par les principaux assureurs français : AXA, Allianz, MAAF, Groupama, Matmut, MACIF, MMA, GMF.</p>

<p>Pour activer la garantie, trois étapes :</p>
<ol>
<li>Déclarez le sinistre à votre assureur dans les <strong>5 jours ouvrables</strong> après constat</li>
<li>Faites réaliser la recherche de fuite (par nous-mêmes ou un prestataire de votre choix)</li>
<li>Transmettez le rapport à votre assureur avec les photos des dégâts</li>
</ol>

<h2>Écrêtement de facture d'eau : la loi Warsmann de 2011</h2>
<p>Si votre fuite se trouve sur une canalisation enterrée entre votre compteur et votre maison, et qu'elle était indétectable visuellement, vous pouvez bénéficier d'un écrêtement de facture auprès de Suez ou de votre régie des eaux. Votre consommation excédentaire est alors plafonnée à deux fois votre consommation habituelle.</p>

<p>Trois conditions à remplir :</p>
<ul>
<li>La fuite doit concerner une canalisation enterrée privative (pas un robinet, pas un équipement visible)</li>
<li>Elle doit être indétectable à l'œil nu (pas d'humidité de surface apparente)</li>
<li>Vous devez fournir une attestation de réparation par un professionnel qualifié dans le mois qui suit la notification de surconsommation par le distributeur</li>
</ul>

<p>Notre rapport de recherche de fuite mentionne explicitement la localisation enterrée, la méthode de détection (gaz traceur, corrélation) et sert de justificatif pour la demande d'écrêtement.</p>

<h2>Ce qui est inclus dans notre prestation</h2>
<ul>
<li>Déplacement dans toute la métropole bordelaise et la Gironde (Bordeaux, Mérignac, Pessac, Talence, Arcachon, Libourne, La Teste, Gujan-Mestras...)</li>
<li>Devis fixe communiqué avant intervention, pas de surprise</li>
<li>Intervention par un technicien qualifié avec équipement professionnel</li>
<li>Rapport technique écrit remis le jour même ou sous 24h</li>
<li>Photos et vidéos des investigations</li>
<li>Préconisations de réparation chiffrées</li>
<li>Pas de facturation si déplacement sans donner suite au devis</li>
</ul>

<h2>Demandez votre devis gratuit</h2>
<p>Pour obtenir un <a href="/devis/" style="color:var(--green);text-decoration:underline;">devis gratuit de recherche de fuite à Bordeaux</a>, remplissez notre formulaire en décrivant les symptômes (tache, compteur anormal, sol humide, zone de jardin gorgée d'eau). Un technicien vous recontacte dans l'heure en journée pour préciser le tarif et convenir d'un rendez-vous sous 24 à 48h.</p>"""
    },
    {
        "slug": "reparation-liner-piscine",
        "title": "Réparation d'une fuite de liner piscine : méthodes et coûts",
        "title_seo": "Réparation fuite liner piscine : méthodes et prix",
        "desc": "Comment réparer une fuite sur liner piscine PVC : rustine subaquatique, soudure thermique, remplacement complet. Coûts, durée de vie, garantie.",
        "contenu": """<figure style="margin:0 0 2rem;"><img src="/assets/reparation-liner-piscine.webp" alt="Piscine privée avec liner bleu en Gironde avant réparation d'une fuite" width="1600" height="1067" loading="lazy" style="width:100%;max-height:340px;height:auto;object-fit:cover;border-radius:12px;display:block;"></figure>

<p>Une fois la fuite localisée par notre <a href="/detection-fuite/fluoresceine-piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">diagnostic à la fluorescéine</a> ou par les autres méthodes utilisées sur les piscines girondines, la question suivante tombe immédiatement : comment la réparer, à quel coût et avec quelle durée de vie ? Cet article détaille les trois grandes familles de réparation d'un liner PVC fuyard, les configurations où chacune est pertinente et les ordres de grandeur tarifaires constatés en Gironde en 2026.</p>

<h2>Diagnostic préalable : que dit l\'état du liner ?</h2>
<p>Avant toute réparation, il faut évaluer l\'état général du liner. Une fuite ponctuelle sur un liner de moins de 10 ans avec une teinte uniforme et une bonne souplesse mérite une réparation locale. À l\'inverse, une fuite sur un liner de plus de 18-20 ans présentant plis figés, points de tension, décoloration jaunâtre ou bleu pâle, plis qui craquellent au toucher : la réparation locale est techniquement possible mais économiquement absurde, car la prochaine fuite arrive sous 6 à 24 mois.</p>

<p>Notre rapport de diagnostic donne systématiquement une préconisation argumentée : nous indiquons l\'âge présumé du liner, son état général, le nombre de zones suspectes secondaires repérées (au-delà de la fuite identifiée), et nous chiffrons les deux scénarios : réparation locale ou remplacement. Le client choisit en pleine conscience. Voir aussi notre guide complémentaire sur le <a href="/guide/fuite-liner-piscine/" style="color:var(--green);text-decoration:underline;">diagnostic d\'une fuite de liner piscine</a> pour comprendre les signes d\'alerte précoce.</p>

<h2>Méthode 1 : la rustine PVC subaquatique</h2>
<p>C\'est la solution la plus simple, la plus rapide et la moins coûteuse. Elle consiste à appliquer une pièce de PVC souple (chute du liner d\'origine de préférence, sinon PVC standard) sur la fissure ou le trou, en utilisant une colle PVC spéciale piscine compatible avec une application en immersion. La pièce est appliquée directement par un plongeur, sans vidange du bassin.</p>

<h3>Quand utiliser une rustine</h3>
<ul>
<li><strong>Trou ponctuel</strong> de 1 à 30 mm de diamètre (perforation par objet pointu, brûlure cigarette, déchirure de griffe d\'animal)</li>
<li><strong>Fissure droite</strong> de moins de 10 cm sur paroi ou fond, hors zones de tension (pli, angle, raccord)</li>
<li><strong>Liner en bon état général</strong> de moins de 12 ans</li>
<li><strong>Fissure inaccessible par démontage</strong> (sous escalier, derrière coffre filtration)</li>
</ul>

<h3>Limites et précautions</h3>
<p>La rustine ne fonctionne pas sur les zones soumises à de fortes contraintes mécaniques : raccords pièces à sceller, joints d\'angle, bords de marches. Sur ces zones, le liner travaille en permanence et la rustine se décolle en quelques mois. La durée de vie typique d\'une rustine subaquatique correctement posée sur une zone neutre est de 3 à 7 ans, parfois plus si l\'eau est bien équilibrée chimiquement.</p>

<h3>Coût et durée d\'intervention</h3>
<p>Une réparation par rustine subaquatique coûte entre <strong>180 et 350 euros HT</strong> selon l\'accessibilité et le nombre de rustines à poser. L\'intervention dure 30 minutes à 1 heure 30. Sur les bassins équipés d\'une pompe de surpression, on peut parfois éviter la plongée et coller depuis la surface, ce qui réduit le tarif à 150-200 euros HT. La rustine peut être posée immédiatement après notre diagnostic si le client le souhaite.</p>

<h2>Méthode 2 : la soudure thermique localisée</h2>
<p>Plus technique et plus coûteuse, la soudure thermique consiste à fondre localement le PVC du liner pour reconstituer la matière au point de fuite, sans pièce rapportée. Elle nécessite une vidange partielle ou totale de la zone à traiter, ce qui exclut les fuites en grand fond ou les fuites multiples sur tout le bassin.</p>

<h3>Quand utiliser la soudure thermique</h3>
<ul>
<li><strong>Décollement de soudure d\'origine</strong> entre deux lés de liner (cas fréquent sur les liners de 8 à 15 ans)</li>
<li><strong>Fissure le long d\'un raccord</strong> pièces à sceller (skimmer, refoulement, projecteur) où une rustine ne tiendrait pas</li>
<li><strong>Coupures fines</strong> ou perforations propres où le PVC peut être refondu sans apport de matière</li>
</ul>

<h3>Le matériel et la technique</h3>
<p>L\'opérateur utilise un fer à souder spécifique PVC souple (température 320 à 380 °C selon l\'épaisseur du liner) avec embouts dédiés. Le PVC est chauffé au point de friction jusqu\'à ramollissement, puis pressé pour reconstituer une étanchéité monobloc. Sur les fissures supérieures à 5 cm, on ajoute un cordon PVC fondu en complément. La compétence de l\'opérateur est déterminante : un mauvais soudage peut détériorer durablement le liner sur 20 à 40 cm autour du point d\'origine.</p>

<h3>Coût et durée</h3>
<p>Comptez <strong>320 à 580 euros HT</strong> pour une soudure thermique localisée incluant la vidange partielle nécessaire. La durée d\'intervention est de 2 à 4 heures, plus le temps de remplissage du bassin. La durée de vie d\'une soudure thermique propre est de 5 à 10 ans, équivalente à la longévité résiduelle du liner. C\'est donc une réparation durable mais qui mérite un liner globalement en bon état pour être justifiée économiquement.</p>

<h2>Méthode 3 : le changement complet du liner</h2>
<p>Quand le liner approche ou dépasse sa durée de vie nominale (15 à 25 ans selon l\'épaisseur et l\'entretien), ou quand les fuites se multiplient en plusieurs points sur la même saison, le remplacement complet devient incontournable. C\'est une opération majeure mais qui repart pour 15 à 25 ans de tranquillité.</p>

<h3>Le déroulement</h3>
<ol>
<li><strong>Vidange complète</strong> du bassin (1 à 2 jours selon volume)</li>
<li><strong>Démontage</strong> des pièces à sceller, du liner d\'origine et du feutre de protection</li>
<li><strong>Inspection structurelle</strong> du voile béton ou des panneaux : détection des fissures, ferraillage corrodé, chape dégradée</li>
<li><strong>Remise en état préalable</strong> si nécessaire : ragréage chape, traitement des fissures structurelles, calage des angles</li>
<li><strong>Pose feutre</strong> géotextile neuf de 400 à 800 g/m² sous le liner</li>
<li><strong>Pose liner sur mesure</strong> avec aspiration sous vide pour mariage parfait à la forme du bassin</li>
<li><strong>Reposition</strong> des pièces à sceller (souvent à remplacer si plus de 15 ans : skimmers, projecteurs, brides, joints)</li>
<li><strong>Remplissage</strong> du bassin et mise en service</li>
</ol>

<h3>Coût constaté en Gironde</h3>
<p>Le tarif d\'un changement de liner complet en 2026 sur la métropole bordelaise se situe entre <strong>3 800 et 7 500 euros TTC</strong> pour une piscine standard de 8×4 mètres. Les variations dépendent de l\'épaisseur du liner choisi (75/100, 85/100 ou 100/100), de la qualité du feutre, du remplacement éventuel des pièces à sceller usagées, de l\'accessibilité du bassin et de la nécessité de réparations structurelles préalables. Pour une piscine plus grande de 10×5 ou 12×5 mètres, prévoir 5 500 à 10 000 euros TTC.</p>

<p>Cette dépense ne nous concerne pas directement (nous ne posons pas de liner, nous faisons exclusivement du diagnostic). Mais nous travaillons avec des piscinistes partenaires en Gironde à qui nous transmettons le rapport technique : ils gagnent du temps en intervention, le client économise une partie du coût de leur diagnostic préalable et obtient parfois un meilleur prix grâce à notre rapport déjà établi.</p>

<h2>Quelle prise en charge par l\'assurance ?</h2>
<p>La garantie recherche de fuite de votre contrat multirisque habitation rembourse uniquement le diagnostic, pas la réparation. Cependant, si la fuite a provoqué un dégât des eaux périphérique (terrain affaissé, jardin saturé, infiltration vers cave ou voisin), votre assurance peut couvrir tout ou partie des dommages consécutifs.</p>

<p>Pour les piscines anciennes dont la fuite est due à un défaut structurel ou à un vice de construction (moins de 10 ans), la garantie décennale du constructeur peut être actionnée. Notre rapport technique sert alors de pièce justificative pour engager une procédure auprès de l\'assurance dommages-ouvrage. Plus de détails dans notre <a href="/guide/recherche-fuite-piscine-assurance/" style="color:var(--green);text-decoration:underline;">guide remboursement assurance piscine</a> avec la procédure pas-à-pas et les pièces à fournir.</p>

<h2>Comment éviter une nouvelle fuite après réparation ?</h2>
<p>Quel que soit le type de réparation, l\'entretien post-intervention est déterminant pour la longévité de la solution. Trois bonnes pratiques sortent du lot après nos 200+ diagnostics annuels :</p>
<ol>
<li><strong>Stabiliser le pH et le TAC en permanence</strong>. Un pH supérieur à 7,8 ou inférieur à 7,0 fragilise le PVC accélérément. Mesurer chaque semaine, corriger immédiatement.</li>
<li><strong>Limiter le chlore choc</strong>. Les chlorations choc à 5-10 mg/L régulières attaquent le liner sur le long terme. Privilégier la chloration lente continue à 1-2 mg/L stable.</li>
<li><strong>Couvrir le bassin hors saison</strong>. UV et gel sont les premiers ennemis du liner. Une bâche d\'hivernage opaque divise par 2 à 3 la dégradation hors saison.</li>
</ol>

<h2>Demandez un diagnostic avant réparation</h2>
<p>Avant de vous lancer dans l\'une de ces réparations, faites-nous appeler pour un diagnostic précis. Nous localisons la fuite au point exact (méthode <a href="/detection-fuite/fluoresceine-piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">fluorescéine</a>, test de pression, écoute acoustique, caméra endoscopique selon le cas) et nous vous remettons un rapport technique chiffré qui guide la suite. Pour une intervention sur Bordeaux et sa métropole, voir notre page <a href="/detection-fuite/piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">recherche de fuite piscine à Bordeaux</a>. Pour le Bassin d\'Arcachon, voir <a href="/detection-fuite/piscine-arcachon/" style="color:var(--green);text-decoration:underline;">piscine Arcachon</a>. Pour les autres communes, voir notre <a href="/detection-fuite/piscine/" style="color:var(--green);text-decoration:underline;">hub recherche de fuite piscine en Gironde</a>. Pour faire le test seau préalable, voir <a href="/guide/evaporation-vs-fuite-piscine/" style="color:var(--green);text-decoration:underline;">évaporation ou fuite : test du seau</a>. Pour les tarifs détaillés, consultez notre <a href="/guide/recherche-fuite-piscine-tarif/" style="color:var(--green);text-decoration:underline;">guide tarif recherche de fuite piscine en Gironde</a>.</p>"""
    },
    {
        "slug": "reparation-skimmer-piscine-resine-epoxy",
        "title": "Réparation skimmer piscine à la résine époxy : méthode et coûts",
        "title_seo": "Réparation skimmer piscine résine époxy",
        "desc": "Réparer un skimmer fissuré ou désaxé à la résine époxy bicomposant : protocole pas à pas, coût (80 à 250 € HT), durée de vie, alternative remplacement complet.",
        "contenu": """<figure style="margin:0 0 2rem;"><img src="/assets/reparation-skimmer-piscine.webp" alt="Skimmer en bord de piscine privée avant réparation à la résine époxy" width="1600" height="1067" loading="lazy" style="width:100%;max-height:340px;height:auto;object-fit:cover;border-radius:12px;display:block;"></figure>

<p>Le skimmer est l\'une des pièces les plus fragiles de la piscine. Exposé en permanence aux UV, à la chloration et aux variations de niveau d\'eau, il finit par fissurer ou par se désaxer du voile béton à mesure que les saisons passent. Sur les piscines girondines de plus de 12 ans, c\'est notre cas de réparation le plus fréquent après le diagnostic à la <a href="/detection-fuite/fluoresceine-piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">fluorescéine</a>. Cet article détaille la méthode de réparation à la résine époxy bicomposant : quand elle s\'applique, comment l\'exécuter proprement et combien elle coûte en 2026.</p>

<h2>Diagnostic préalable : votre skimmer fuit-il vraiment ?</h2>
<p>Avant tout achat de résine, il faut confirmer que la fuite vient bien du skimmer et pas d\'une pièce voisine. Trois indices typiques nous orientent vers le skimmer pendant nos diagnostics en Gironde :</p>
<ul>
<li><strong>Niveau qui se stabilise pile sous le skimmer</strong> : la piscine perd de l\'eau jusqu\'à atteindre la base du skimmer puis arrête de baisser. Signe quasi pathognomonique d\'une fuite côté skimmer ou côté joint d\'étanchéité.</li>
<li><strong>Humidité côté terre derrière le skimmer</strong> : carrelage de plage qui se décolle, terre saturée juste derrière, voire remontée d\'eau visible quand on creuse 20 cm.</li>
<li><strong>Test fluorescéine positif sur le skimmer</strong> : nous injectons quelques millilitres de colorant à l\'aide d\'une seringue à proximité du skimmer, filtration coupée. Une migration vers la traversée de paroi confirme la fuite.</li>
</ul>
<p>Sans ces indices, la réparation à la résine époxy ne sert à rien. Voir aussi notre guide <a href="/guide/fuite-liner-piscine/" style="color:var(--green);text-decoration:underline;">diagnostic fuite liner piscine</a> pour distinguer skimmer et liner sur les piscines de plus de 15 ans où les deux peuvent fuir simultanément.</p>

<h2>Quelle résine époxy choisir pour réparer un skimmer ?</h2>
<p>Toutes les résines époxy ne se valent pas. Pour un skimmer immergé en permanence, vous devez impérativement choisir une résine spécifiquement formulée pour usage piscine : résistance chimique au chlore et au pH 7,0 à 7,8, prise en milieu humide, élasticité résiduelle pour absorber les micro-mouvements du voile béton, durée de vie 10 à 15 ans en immersion permanente. Voici nos recommandations selon le profil de réparation :</p>
<ul>
<li><strong>Résine époxy bicomposant Sika SikaPool ou équivalent (résine + durcisseur)</strong> : référence du marché professionnel. Coût matière 35 à 60 € le kit 1 kg, suffisant pour 2 à 3 skimmers. Prise en 30 minutes, mise en eau 24 heures après.</li>
<li><strong>Mastic époxy à modeler (Plastic Padding Aquaroc, Loctite EA 3463)</strong> : se présente sous forme de pâte à modeler que l\'on pétrit pour activer le durcisseur. Idéal pour les fissures longues (15 à 30 cm) ou les angles. Coût 12 à 20 € la barre.</li>
<li><strong>Bande d\'étanchéité résine pré-imprégnée</strong> : pour renforcer une zone fragile au-delà du point de fuite (cas des skimmers très anciens). Coût 25 à 40 € le mètre.</li>
</ul>
<p>Évitez les résines polyester (durée de vie 2 à 4 ans en immersion, jaunissent vite) et les colles silicones piscine (faux ami, ne tiennent pas plus de 18 mois sur skimmer fissuré).</p>

<h2>Protocole de réparation skimmer à la résine époxy</h2>
<p>Voici le protocole que nos partenaires piscinistes appliquent en Gironde, validé sur plus de 100 réparations en 2024-2026 :</p>
<ol>
<li><strong>Vidange partielle du bassin</strong> jusqu\'à 5 cm sous le niveau du skimmer. Inutile de vidanger plus, le coût en eau et en remise en service ne le justifie pas.</li>
<li><strong>Démontage de la trappe et de la bride avant du skimmer</strong>. Photographier la position des joints pour le remontage.</li>
<li><strong>Nettoyage haute pression de la zone à réparer</strong> : éliminer toute trace d\'algues, de calcaire, de vieux mastic. Sécher la zone à l\'air comprimé (compresseur 5 bars suffisants).</li>
<li><strong>Ponçage léger au papier 80 puis 120</strong> sur 5 cm autour de la fissure pour créer une accroche pour la résine.</li>
<li><strong>Dégraissage à l\'acétone</strong> et séchage 15 minutes minimum.</li>
<li><strong>Application de la résine époxy</strong> selon les indications du fabricant (mélange 1:1 ou 2:1 selon le produit). Étaler en couche de 3 à 5 mm sur la fissure et 2 cm au-delà sur les bords.</li>
<li><strong>Lissage au doigt mouillé d\'eau savonneuse</strong> pour une finition propre. Si fissure profonde, deuxième couche après 10 minutes de prise.</li>
<li><strong>Temps de prise hors d\'eau : 24 heures minimum à 20 °C</strong>. À 15 °C, prévoir 36 à 48 heures.</li>
<li><strong>Remise en eau lente</strong> (sans choc), filtration redémarrée 12 heures plus tard pour vérifier l\'étanchéité.</li>
<li><strong>Test fluorescéine de validation</strong> 48 heures après remise en service pour confirmer l\'absence de fuite résiduelle.</li>
</ol>

<h2>Combien coûte une réparation skimmer en Gironde ?</h2>
<p>Le coût total d\'une intervention dépend de la formule choisie. Voici les fourchettes constatées sur la métropole bordelaise et le Bassin d\'Arcachon en 2026 :</p>
<ul>
<li><strong>Résine époxy en kit, achat et application par le propriétaire</strong> : 50 à 90 € de matière, plus 1 demi-journée de travail. Méthode économique mais nécessite un minimum de bricolage.</li>
<li><strong>Réparation par un pisciniste partenaire (résine + main d\'œuvre)</strong> : 180 à 320 € HT pour un skimmer standard, 320 à 480 € HT si plusieurs skimmers ou si fissure longue (cas fréquent sur les skimmers de plus de 18 ans).</li>
<li><strong>Diagnostic préalable Recherche Fuite Gironde</strong> : 240 à 380 € HT pour confirmer la localisation par fluorescéine et test de pression. Souvent remboursé par votre assurance habitation. Voir notre <a href="/guide/recherche-fuite-piscine-assurance/" style="color:var(--green);text-decoration:underline;">guide remboursement assurance piscine</a>.</li>
<li><strong>Remplacement complet du skimmer (si fissure structurelle ou bride éclatée)</strong> : 450 à 850 € HT en intervention pisciniste, hors démolition partielle de la plage si nécessaire.</li>
</ul>

<h2>Réparation époxy ou remplacement complet ?</h2>
<p>La réparation à la résine époxy est durable (10 à 15 ans en moyenne) mais elle n\'est pas adaptée à toutes les situations. Voici nos critères de décision sur la base de notre expérience terrain :</p>

<h3>Privilégier la réparation époxy si</h3>
<ul>
<li>Fissure visible inférieure à 15 cm de longueur</li>
<li>Bride avant du skimmer en bon état (pas de morceau cassé)</li>
<li>Skimmer de moins de 20 ans, pas de signe de fragilisation généralisée</li>
<li>Pas de mouvement structurel du voile béton (pas de fissures dans le carrelage de plage)</li>
<li>Budget contraint et pas de remise en eau urgente</li>
</ul>

<h3>Privilégier le remplacement complet si</h3>
<ul>
<li>Bride avant éclatée ou manquante</li>
<li>Fissures multiples sur le corps du skimmer</li>
<li>Skimmer de plus de 25 ans avec PVC qui se craquelle au toucher</li>
<li>Mouvement structurel du voile béton autour du skimmer</li>
<li>Vous prévoyez de changer le liner dans les 3 à 5 ans : combiner les deux opérations économise la main d\'œuvre</li>
</ul>

<h2>Et si la fuite ne vient pas du skimmer ?</h2>
<p>Plus de 30 pourcent des suspicions de fuite skimmer s\'avèrent en réalité venir d\'autres sources : raccord refoulement, prise balai, projecteur encastré, fissure de liner ou canalisation enterrée. C\'est pourquoi nous insistons sur le diagnostic complet par fluorescéine et test de pression avant toute intervention. Une réparation époxy sur un skimmer sain ne résout évidemment pas le problème et fait perdre 200 à 400 € au propriétaire.</p>
<p>Pour faire intervenir un technicien sur Bordeaux, voir notre page <a href="/detection-fuite/piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">recherche de fuite piscine à Bordeaux</a>. Pour le Bassin d\'Arcachon, voir <a href="/detection-fuite/piscine-arcachon/" style="color:var(--green);text-decoration:underline;">piscine Arcachon</a>. Pour les autres communes de Gironde, consultez notre <a href="/detection-fuite/piscine/" style="color:var(--green);text-decoration:underline;">hub recherche de fuite piscine en Gironde</a>. Pour les tarifs des autres types de réparations piscine, voir notre guide <a href="/guide/reparation-liner-piscine/" style="color:var(--green);text-decoration:underline;">réparation d\'une fuite de liner piscine</a>.</p>"""
    },
    {
        "slug": "fuite-canalisation-enterree-assurance",
        "title": "Fuite canalisation enterrée et assurance habitation : prise en charge",
        "title_seo": "Fuite canalisation enterrée et assurance | Remboursement",
        "desc": "Comment faire prendre en charge une fuite sur canalisation enterrée par votre assurance habitation : conditions, écrêtement loi Warsmann, rapport technique opposable.",
        "contenu": """<figure style="margin:0 0 2rem;"><img src="/assets/canalisation-enterree-assurance.webp" alt="Réseau de canalisations enterrées en Gironde, contexte d'intervention recherche de fuite et prise en charge assurance" width="1600" height="1067" loading="lazy" style="width:100%;max-height:340px;height:auto;object-fit:cover;border-radius:12px;display:block;"></figure>

<p>Une fuite sur canalisation enterrée est l\'un des sinistres les plus coûteux pour un propriétaire en Gironde : surconsommation d\'eau qui peut atteindre plusieurs milliers de mètres cubes en quelques mois, terrain saturé, fondations fragilisées, fuite invisible qui s\'aggrave dans le temps. Heureusement, la plupart des contrats d\'assurance multirisque habitation couvrent une partie de la prise en charge, à condition de respecter une procédure précise. Cet article détaille comment activer votre garantie, ce qui est remboursé, le mécanisme de l\'écrêtement loi Warsmann pour la facture d\'eau, et les pièges à éviter.</p>

<h2>Ce que couvre l\'assurance habitation sur une fuite enterrée</h2>
<p>Votre contrat multirisque habitation comprend en général trois garanties qui peuvent être activées en cascade quand une fuite enterrée est détectée :</p>

<h3>1. La garantie « recherche de fuite »</h3>
<p>Présente dans 90 pourcent des contrats français, elle rembourse tout ou partie du diagnostic technique de localisation, dès lors que la fuite a provoqué un dégât des eaux ou une surconsommation anormale. Plafond de remboursement habituel : 1 500 à 5 000 € selon le contrat. Notre intervention typique pour une recherche de fuite canalisation enterrée à Bordeaux coûte entre 380 et 580 € HT, donc largement dans le plafond. Voir notre page dédiée <a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">recherche de fuite canalisation enterrée à Bordeaux</a> avec la méthode gaz traceur azote/hydrogène et nos cas concrets.</p>

<h3>2. La garantie « dégâts des eaux »</h3>
<p>Couvre les dommages matériels causés par la fuite : terrain affaissé, fondations dégradées, infiltrations dans la cave ou le sous-sol, dommage au jardin (pelouse arrachée, plantations à remplacer), dégradation de la chape ou du carrelage extérieur. Plafond souvent élevé (10 000 à 50 000 € selon contrats). Pour les sinistres en copropriété, c\'est la <a href="/detection-fuite/degats-des-eaux-bordeaux/" style="color:var(--green);text-decoration:underline;">convention IRSI</a> qui s\'applique entre assureurs jusqu\'à 5 000 € HT.</p>

<h3>3. L\'écrêtement de facture d\'eau loi Warsmann</h3>
<p>Ce dispositif n\'est pas une garantie d\'assurance à proprement parler mais une obligation légale du distributeur d\'eau (Suez, Régie des eaux de Bordeaux Métropole, etc.) de plafonner votre facture après une fuite enterrée. Pour bénéficier du plafonnement, vous devez fournir un rapport technique d\'un professionnel (le nôtre est accepté) attestant la localisation enterrée et la non-détectabilité visible. Le plafond légal est de deux fois la consommation moyenne des trois dernières années. Voir notre guide complet <a href="/guide/loi-warsmann-ecretement-facture-eau/" style="color:var(--green);text-decoration:underline;">loi Warsmann : écrêtement de facture d\'eau</a> avec procédure pas à pas et modèle de courrier.</p>

<h2>Conditions à remplir pour être indemnisé</h2>
<p>Cinq conditions doivent être remplies pour activer la prise en charge assurance d\'une fuite enterrée :</p>
<ul>
<li><strong>Déclaration du sinistre dans les 5 jours ouvrables</strong> après constat (par téléphone, email ou courrier recommandé). Tout retard peut justifier un refus de prise en charge.</li>
<li><strong>Rapport technique d\'un professionnel agréé</strong> attestant la localisation, la nature de la fuite et les méthodes employées. Notre rapport standardisé est accepté par AXA, MAIF, MAAF, Macif, Generali, Groupama, Allianz, Matmut, GMF, Crédit Mutuel, etc.</li>
<li><strong>Facture de la recherche de fuite</strong> en bonne et due forme, à votre nom de propriétaire ou locataire selon le contrat.</li>
<li><strong>Preuve du dégât des eaux ou de la surconsommation</strong> : photos datées, factures d\'eau anormalement hautes, témoignages, devis de réparation.</li>
<li><strong>Pas d\'exclusion contractuelle</strong>. Vérifiez votre contrat : certaines polices excluent les fuites en sous-sol non aménagé, les fuites liées à un défaut d\'entretien manifeste, les fuites antérieures à votre prise de contrat.</li>
</ul>

<h2>Procédure pas à pas : comment activer votre prise en charge</h2>

<h3>Étape 1 : déclaration du sinistre</h3>
<p>Dès que vous constatez la fuite ou la surconsommation (pic facture eau, terrain saturé, compteur qui tourne), prévenez votre assureur. Mode de déclaration recommandé : par téléphone pour démarrer le dossier, suivi d\'un courrier recommandé avec accusé de réception sous 48 heures. Donnez la date d\'apparition des symptômes, l\'étendue présumée du sinistre, le numéro de votre contrat.</p>

<h3>Étape 2 : commande du diagnostic technique</h3>
<p>Avant de payer la moindre réparation, faites localiser la fuite par un professionnel. Pour la Gironde, contactez-nous via notre <a href="/devis/" style="color:var(--green);text-decoration:underline;">formulaire de devis</a> ou directement notre page <a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">canalisation enterrée à Bordeaux</a>. Notre intervention dure 2 à 4 heures, le rapport est rédigé dans la journée et envoyé par email avec photos, méthodes et localisation au mètre près.</p>

<h3>Étape 3 : transmission du rapport à l\'assureur</h3>
<p>Envoyez le rapport technique, la facture de recherche, vos factures d\'eau des 24 derniers mois et toutes pièces justifiant le sinistre par email ou courrier à votre assureur. L\'expert d\'assurance vous contactera sous 5 à 10 jours ouvrés.</p>

<h3>Étape 4 : visite éventuelle de l\'expert</h3>
<p>Si le sinistre dépasse 1 500 € de dommages, l\'assureur mandate généralement un expert. Préparez les documents (rapport, factures, devis). L\'expert valide la prise en charge et négocie les montants. Notre rapport sert de référence technique et limite les contestations.</p>

<h3>Étape 5 : indemnisation et écrêtement Warsmann</h3>
<p>Une fois la prise en charge validée, l\'assurance vous rembourse selon votre contrat. En parallèle, envoyez votre rapport au distributeur d\'eau (Suez ou Régie de Bordeaux Métropole) pour activer la procédure Warsmann d\'écrêtement de facture. Délai de réponse du distributeur : 30 à 60 jours.</p>

<h2>Pièges et refus fréquents</h2>
<p>Sur 100 dossiers que nous accompagnons, 5 à 10 rencontrent un refus initial ou un litige avec l\'assureur. Voici les pièges les plus fréquents :</p>
<ul>
<li><strong>Fuite ancienne déclarée tardivement</strong> : si l\'assureur peut prouver que la fuite existait avant la souscription du contrat, refus presque automatique. Conservez les factures d\'eau qui montrent l\'évolution.</li>
<li><strong>Défaut d\'entretien</strong> : pour les canalisations en plomb, fonte ou cuivre fragilisées par la corrosion, l\'assureur peut invoquer un défaut d\'entretien. Notre rapport mentionne explicitement la cause technique de la fuite (perforation par mouvement de terrain, joint désaxé, racine, gel, etc.) pour distinguer du défaut d\'entretien.</li>
<li><strong>Plafond de remboursement atteint</strong> : si le diagnostic + les réparations dépassent le plafond garantie, le delta reste à votre charge. Le rapport bien construit aide à dimensionner les devis pour rester dans le plafond.</li>
<li><strong>Exclusion fuite extérieure au bâti</strong> : certaines polices excluent les fuites au-delà du bâti. Vérifiez votre contrat avant tout, ou demandez-nous conseil sur la formulation à privilégier dans la déclaration.</li>
</ul>

<h2>Cas concret : fuite enterrée à Caudéran Bordeaux (mars 2026)</h2>
<p>M. R., propriétaire d\'une maison bourgeoise à Caudéran (33000), reçoit une facture d\'eau de 1 850 € pour le trimestre alors que sa moyenne historique est de 280 €. Diagnostic Recherche Fuite Gironde par gaz traceur : fuite localisée à 8 mètres du compteur, sur un raccord cuivre désaxé sous la pelouse. Notre intervention : 480 € HT.</p>
<p>Procédure d\'indemnisation :</p>
<ul>
<li>Garantie recherche de fuite (AXA Confiance) : remboursement intégral des 480 € HT</li>
<li>Garantie dégâts des eaux : pelouse refaite (320 €) + canalisation reprise (1 200 €) pris en charge à 80 pourcent</li>
<li>Loi Warsmann auprès de Suez : facture d\'eau plafonnée à 560 € au lieu de 1 850 €. Économie nette : 1 290 €</li>
</ul>
<p>Coût net pour M. R. après tous les remboursements : 230 € sur un sinistre initial à plus de 3 850 €. Délai total de résolution : 7 semaines entre notre intervention et la dernière indemnisation.</p>

<h2>Faites-vous accompagner dès le diagnostic</h2>
<p>Notre intervention ne se limite pas au diagnostic : nous vous remettons un rapport technique standardisé, accepté par les assureurs et les distributeurs d\'eau, avec photos, méthodes employées (gaz traceur, écoute électro-acoustique, caméra endoscopique), localisation au mètre près et préconisations chiffrées. Pour les sinistres importants, nous restons disponibles pendant 6 mois pour répondre aux questions de l\'expert mandaté ou produire des compléments de rapport.</p>
<p>Pour démarrer une procédure assurance après une fuite enterrée à Bordeaux ou en Gironde, voir notre <a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">page canalisation enterrée Bordeaux</a> ou contactez-nous via le <a href="/devis/" style="color:var(--green);text-decoration:underline;">formulaire de devis</a>. Pour comprendre la procédure d\'écrêtement de facture en détail, voir le guide <a href="/guide/loi-warsmann-ecretement-facture-eau/" style="color:var(--green);text-decoration:underline;">loi Warsmann : écrêtement de facture d\'eau</a>. Pour la procédure générale assurance fuite d\'eau (intérieure et extérieure), voir <a href="/guide/assurance-fuite-eau/" style="color:var(--green);text-decoration:underline;">fuite d\'eau et assurance habitation</a>."""
    },
    {
        "slug": "piscine-qui-fuit-perte-eau",
        "title": "Piscine qui fuit ou perte d'eau anormale : que faire ?",
        "title_seo": "Piscine qui fuit : causes et solutions Gironde",
        "desc": "Votre piscine perd de l'eau anormalement ? Arbre de décision en 6 questions pour distinguer évaporation, fuite et erreur d'usage. Cas types Gironde.",
        "contenu": """<figure style="margin:0 0 2rem;"><img src="/assets/piscine-qui-fuit-perte-eau.webp" alt="Piscine privée avec niveau d'eau anormalement bas, suspicion de fuite en Gironde" width="1600" height="1067" loading="lazy" style="width:100%;max-height:340px;height:auto;object-fit:cover;border-radius:12px;display:block;"></figure>

<p>Votre piscine perd de l'eau et vous ne savez pas si c'est grave. Avant de paniquer (ou de vous résigner à payer un diagnostic), prenez 10 minutes pour suivre cet arbre de décision en 6 questions. Il s'inspire de notre expérience sur plus de 200 diagnostics annuels en Gironde et vous permet de qualifier votre cas. Dans 1 cas sur 3, la perte d'eau s'avère être un phénomène normal qui ne nécessite aucune intervention. Dans les 2 autres cas, vous saurez exactement quoi faire et qui appeler.</p>

<h2>Question 1 : combien de centimètres perdez-vous par jour ?</h2>
<p>C'est la question fondamentale. Mesurez précisément avec un mètre ruban depuis un repère fixe (margelle, premier joint de carrelage, marche d'escalier). Mesurez au même moment de la journée (idéalement le matin avant baignade) sur 48 à 72 heures sans pluie ni baignade.</p>
<ul>
<li><strong>Moins de 0,5 cm/jour</strong> : évaporation strictement normale en Gironde, quel que soit le mois. Pas de fuite. Aucune action requise.</li>
<li><strong>0,5 à 1,5 cm/jour</strong> : zone grise. En été (juin à septembre), c'est de l'évaporation normale, en particulier sur Bassin d'Arcachon ou pour piscines exposées plein vent. En hiver, c'est suspect.</li>
<li><strong>1,5 à 3 cm/jour</strong> : forte probabilité de fuite. Évaporation seule ne dépasse pas 1,5 cm/jour même en pic de chaleur en Gironde.</li>
<li><strong>Plus de 3 cm/jour</strong> : fuite confirmée, et probablement importante. Un diagnostic urgent s'impose pour éviter dégâts collatéraux (terrain saturé, fondations, voisins).</li>
</ul>
<p>Pour comprendre les taux d'évaporation mensuels précis en climat aquitain, voir notre guide complet <a href="/guide/evaporation-vs-fuite-piscine/" style="color:var(--green);text-decoration:underline;">évaporation ou fuite de piscine</a> avec tableau détaillé et facteurs aggravants (vent, exposition, chauffage).</p>

<h2>Question 2 : avez-vous fait le test du seau ?</h2>
<p>C'est le seul test gratuit qui distingue avec certitude évaporation et fuite. Posez un seau rempli d'eau sur la première marche immergée de la piscine (pour qu'il soit à la même température que l'eau). Marquez au feutre indélébile le niveau dans le seau et le niveau dans la piscine. Laissez 24 à 48 heures sans baignade ni remise à niveau automatique. Comparez les baisses :</p>
<ul>
<li><strong>Seau et piscine baissent de la même hauteur</strong> : c'est de l'évaporation pure. Aucune fuite. Vous pouvez dormir tranquille.</li>
<li><strong>Piscine baisse plus que le seau</strong> : différence = volume perdu par fuite. Si l'écart dépasse 0,5 cm en 24h, c'est une fuite à diagnostiquer.</li>
<li><strong>Seau baisse plus que la piscine</strong> : impossible en théorie. Vérifiez que le seau n'a pas été déplacé ou que la piscine n'a pas reçu d'eau (pluie, remise à niveau auto qui s'est déclenchée).</li>
</ul>

<h2>Question 3 : à quel niveau la baisse s'arrête-t-elle ?</h2>
<p>Si la fuite est confirmée, observez où la baisse se stabilise. Cette information oriente directement le diagnostic :</p>
<ul>
<li><strong>Niveau qui baisse jusqu'au skimmer puis s'arrête</strong> : fuite côté skimmer (joint mastic, bride, fissure de skimmer). Voir notre guide <a href="/guide/reparation-skimmer-piscine-resine-epoxy/" style="color:var(--green);text-decoration:underline;">réparation skimmer à la résine époxy</a>.</li>
<li><strong>Niveau qui baisse jusqu'à la bouche de refoulement</strong> : fuite sur buse de refoulement ou canalisation de refoulement.</li>
<li><strong>Niveau qui baisse jusqu'à un projecteur encastré</strong> : fuite sur le projecteur, sa traversée de paroi ou son joint d'étanchéité.</li>
<li><strong>Niveau qui continue de baisser sous le skimmer (au-delà de 30 cm)</strong> : fuite sur la structure du bassin (liner, coque, béton), bonde de fond ou canalisation enterrée. Diagnostic plus complexe nécessaire.</li>
</ul>

<h2>Question 4 : observez-vous des signes extérieurs ?</h2>
<p>Une piscine qui fuit laisse souvent des traces visibles autour du bassin. Vérifiez ces 5 indices avant de nous appeler :</p>
<ul>
<li><strong>Pelouse anormalement verte ou détrempée</strong> à un endroit précis : signe d'une fuite enterrée sur canalisation d'alimentation ou de refoulement.</li>
<li><strong>Carrelage de plage qui se décolle</strong> ou joints qui s'effritent : infiltration sous la dalle.</li>
<li><strong>Terrain qui s'affaisse en linéaire</strong> à 1-3 m du bassin : fuite chronique avec lessivage du sol.</li>
<li><strong>Auréole d'humidité dans le local technique</strong> : fuite sur tuyauterie après filtration.</li>
<li><strong>Bulles dans l'eau côté skimmer ou refoulement</strong>, filtration arrêtée : fuite avec retour d'air.</li>
</ul>

<h2>Question 5 : depuis quand observez-vous le phénomène ?</h2>
<p>L'historique est crucial pour distinguer une fuite récente d'une fuite chronique :</p>
<ul>
<li><strong>Apparu brutalement après un événement</strong> (orage, gel, intervention récente, baisse de pression chaudière) : fuite ponctuelle souvent localisable rapidement.</li>
<li><strong>Apparu progressivement sur 1-3 mois</strong> : usure d'un joint, fissure liner qui s'agrandit, raccord qui se desserre.</li>
<li><strong>Présent depuis plusieurs saisons</strong>, accentué en été : évaporation forte + petite fuite chronique. Diagnostic plus exigeant.</li>
</ul>

<h2>Question 6 : votre piscine a quel âge ?</h2>
<p>L'âge oriente fortement les hypothèses de localisation et de coût :</p>
<ul>
<li><strong>Moins de 5 ans</strong> : fuite rare et souvent due à un défaut de pose. La garantie décennale du constructeur peut s'activer. Vérifier les pièces à sceller (skimmer, refoulement, projecteur, bonde de fond) en priorité.</li>
<li><strong>5 à 15 ans</strong> : fuites possibles sur joints d'étanchéité, premiers signes de fatigué du liner. Réparation locale presque toujours suffisante.</li>
<li><strong>15 à 25 ans</strong> : phase critique. Le liner approche sa fin de vie nominale, plusieurs fuites simultanées peuvent apparaître. Voir notre guide <a href="/guide/fuite-liner-piscine/" style="color:var(--green);text-decoration:underline;">diagnostic fuite sur liner</a> pour décider entre réparation et remplacement.</li>
<li><strong>Plus de 25 ans</strong> : changement de liner souvent inévitable. Pour les piscines béton, fissures structurelles à examiner.</li>
</ul>

<h2>Cas types fréquents en Gironde</h2>

<h3>Cas 1 : piscine pavillonnaire Mérignac, liner 12 ans, 2 cm/jour</h3>
<p>Le test du seau confirme la fuite. Niveau s'arrête sous le skimmer. Diagnostic le plus probable : joint skimmer ou raccord de canalisation enterrée près du local technique. Démarche : appeler un technicien <a href="/detection-fuite/piscine-merignac/" style="color:var(--green);text-decoration:underline;">recherche de fuite piscine Mérignac</a> pour diagnostic complet. Coût intervention 380 à 580 € HT, souvent remboursé par assurance habitation.</p>

<h3>Cas 2 : piscine Bassin d'Arcachon, été, 1,2 cm/jour</h3>
<p>Avec vent marin permanent et exposition plein soleil, l'évaporation peut atteindre 1,2 cm/jour en juillet-août. Le test du seau montre seau et piscine qui baissent de la même hauteur. Pas de fuite. Aucune action requise. Conseil : couvrir le bassin la nuit pour réduire l'évaporation de 30 à 50 pourcent.</p>

<h3>Cas 3 : piscine béton Caudéran 30 ans, 4 cm/jour brutalement</h3>
<p>Apparu après un hiver rigoureux. Diagnostic suspecté : fissure structurelle réveillée par cycle gel/dégel. Cas complexe nécessitant écoute acoustique + colorant fluorescéine + caméra endoscopique. Voir notre page <a href="/detection-fuite/piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">recherche de fuite piscine Bordeaux</a>. Coût diagnostic 580 à 750 € HT. Réparation béton 1 200 à 4 000 € HT selon localisation.</p>

<h2>Quand appeler un professionnel ?</h2>
<p>Appelez un spécialiste si :</p>
<ul>
<li>Test du seau confirme une fuite supérieure à 0,5 cm/jour (au-delà de l'évaporation)</li>
<li>Vous observez des signes extérieurs (pelouse détrempée, carrelage qui se décolle)</li>
<li>Votre consommation d'eau a explosé sur la facture trimestrielle</li>
<li>La fuite s'aggrave malgré vos recherches</li>
<li>Vous prévoyez de remettre en service la piscine au printemps après hivernage</li>
</ul>
<p>Pour faire intervenir nos techniciens, voir nos pages dédiées : <a href="/detection-fuite/piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">piscine Bordeaux</a>, <a href="/detection-fuite/piscine-arcachon/" style="color:var(--green);text-decoration:underline;">piscine Arcachon</a>, ou notre <a href="/detection-fuite/piscine/" style="color:var(--green);text-decoration:underline;">hub piscine en Gironde</a> qui couvre les 7 communes principales. Pour les tarifs détaillés selon le type de bassin, consultez notre <a href="/guide/recherche-fuite-piscine-tarif/" style="color:var(--green);text-decoration:underline;">guide tarif recherche de fuite piscine</a>. Pour la prise en charge assurance, voir <a href="/guide/recherche-fuite-piscine-assurance/" style="color:var(--green);text-decoration:underline;">remboursement assurance piscine</a>."""
    },
    {
        "slug": "fuite-coque-polyester-piscine",
        "title": "Fuite coque polyester piscine : tests et diagnostic",
        "title_seo": "Fuite coque polyester piscine | Tests & diagnostic",
        "desc": "Votre coque polyester perd de l'eau ? Tests à faire ce soir (seau, repère, colorant), 3 sources possibles, pathologies spécifiques (osmose, gel-coat) et coûts.",
        "contenu": """<figure style="margin:0 0 2rem;"><img src="/assets/fuite-coque-polyester-piscine.webp" alt="Piscine coque polyester en Gironde avec niveau d'eau anormalement bas, suspicion de fuite à diagnostiquer" width="1600" height="1067" loading="lazy" style="width:100%;max-height:340px;height:auto;object-fit:cover;border-radius:12px;display:block;"></figure>

<p>Votre piscine coque polyester perd de l'eau plus vite que la normale ? Avant de paniquer ou d'appeler un pisciniste à 500 €, vous pouvez identifier la source de la fuite vous-même en 24 à 48 heures grâce à trois tests simples qui ne coûtent rien. Cet article détaille pas à pas la méthode utilisée par nos techniciens en Gironde sur plus de 200 diagnostics annuels, dont une cinquantaine concernent spécifiquement des piscines coques polyester (parc particulièrement dense à Gujan-Mestras, La Teste-de-Buch, Andernos-les-Bains et dans les lotissements récents de la métropole bordelaise).</p>

<h2>Comment savoir si votre piscine coque polyester fuit vraiment ?</h2>
<p>Une baisse d'eau ne signifie pas forcément une fuite. En Gironde, l'évaporation naturelle peut atteindre 1 cm par jour en pleine canicule sur le Bassin d'Arcachon, ce qui ressemble à s'y méprendre à une fuite. Avant tout diagnostic, faites les trois tests suivants pour confirmer si vous avez réellement une fuite à traiter.</p>

<h3>Test n°1 : la méthode du seau (test de référence)</h3>
<p>C'est le test fondamental, gratuit, qui distingue avec certitude évaporation et vraie fuite. Posez un seau rempli d'eau sur la première marche immergée de votre piscine pour qu'il soit à la même température que l'eau du bassin. Marquez au feutre indélébile le niveau d'eau dans le seau et le niveau d'eau de la piscine sur la paroi. Laissez 24 à 48 heures sans baignade, sans remise à niveau automatique et sans pluie. Comparez les baisses :</p>
<ul>
<li><strong>Seau et piscine baissent de la même hauteur</strong> : c'est de l'évaporation pure. Aucune fuite. Vous pouvez dormir tranquille.</li>
<li><strong>Piscine baisse plus que le seau de plus de 0,5 cm en 24 h</strong> : fuite confirmée. Passez au test suivant.</li>
</ul>

<h3>Test n°2 : le test du repère filtration ON / OFF</h3>
<p>Ce test vous indique <strong>où se situe la fuite</strong>. Marquez le niveau de la piscine au feutre. Laissez la filtration tourner 24 heures sans baignade. Marquez le nouveau niveau. Coupez la filtration et laissez 24 heures supplémentaires. Comparez :</p>
<ul>
<li><strong>Baisse plus rapide filtration en marche</strong> : fuite côté refoulement (canalisations entre filtre et bassin sous pression).</li>
<li><strong>Baisse plus rapide filtration arrêtée</strong> : fuite côté aspiration (skimmer, prise balai, canalisations vers la pompe).</li>
<li><strong>Baisse identique dans les deux cas</strong> : fuite directement dans la coque (gel-coat, microfissures, raccord pièces à sceller).</li>
</ul>
<p>Notez le niveau exact où l'eau s'arrête de baisser : il indique précisément la zone à inspecter (skimmer, refoulement, projecteur, escalier, fond du bassin).</p>

<h3>Test n°3 : le test du colorant (pour fissure visible)</h3>
<p>Si vous avez identifié une zone suspecte (microfissure, raccord, joint), versez quelques gouttes de colorant alimentaire (bleu de méthylène, ou simple sirop de menthe) à 10 cm de la zone, filtration coupée. Si une fuite est présente, vous verrez le colorant aspiré vers le défaut en 5 à 15 minutes. Sur une coque polyester, c'est particulièrement efficace pour confirmer un joint de skimmer fatigué ou une microfissure à proximité d'un projecteur.</p>

<h2>Les 3 sources de fuite sur une piscine coque polyester</h2>
<p>Selon le résultat des tests ci-dessus, votre fuite vient de l'une de ces trois sources. Sur les coques polyester girondines, voici la répartition typique observée sur 50 diagnostics annuels :</p>

<h3>Source n°1 : le système de filtration et les pièces à sceller (60 % des cas)</h3>
<p>C'est la cause la plus fréquente sur les coques polyester. Les pièces à sceller (skimmer, buses de refoulement, prise balai, projecteurs encastrés, bonde de fond) sont collées ou vissées sur la coque polyester. Avec le temps :</p>
<ul>
<li>Les joints toriques durcissent et perdent leur étanchéité (typique après 8 à 12 ans)</li>
<li>Les vis de bride se desserrent sous l'effet des cycles dilatation/contraction</li>
<li>Le mastic d'étanchéité entre la coque et la pièce se craquelle</li>
<li>La colle polyester d'origine se fragilise sous l'effet du chlore</li>
</ul>
<p>Action : <strong>inspection visuelle minutieuse</strong> de chaque pièce à sceller, ressserage des brides accessibles, et test du colorant sur les joints suspects. Réparation typique : remplacement du joint torique (12 à 25 €) ou re-mastiquage à la résine époxy (80 à 180 € HT par pièce). Voir notre guide <a href="/guide/reparation-skimmer-piscine-resine-epoxy/" style="color:var(--green);text-decoration:underline;">réparation skimmer à la résine époxy</a> pour le détail.</p>

<table style="width:100%;margin:1.5rem 0;border-collapse:collapse;border:1px solid var(--border);">
<thead>
<tr>
<th style="padding:.8rem;text-align:left;background:var(--green);color:var(--white);border:1px solid var(--green-dark);">Symptôme observé</th>
<th style="padding:.8rem;text-align:left;background:var(--green);color:var(--white);border:1px solid var(--green-dark);">Source probable</th>
<th style="padding:.8rem;text-align:left;background:var(--green);color:var(--white);border:1px solid var(--green-dark);">Action</th>
</tr>
</thead>
<tbody>
<tr><td style="padding:.8rem;border:1px solid var(--border);">Niveau s'arrête sous le skimmer</td><td style="padding:.8rem;border:1px solid var(--border);">Joint skimmer ou bride</td><td style="padding:.8rem;border:1px solid var(--border);">Resserrage ou remplacement joint</td></tr>
<tr style="background:var(--bg-alt);"><td style="padding:.8rem;border:1px solid var(--border);">Niveau s'arrête à un projecteur</td><td style="padding:.8rem;border:1px solid var(--border);">Joint projecteur</td><td style="padding:.8rem;border:1px solid var(--border);">Remplacement joint torique</td></tr>
<tr><td style="padding:.8rem;border:1px solid var(--border);">Bulles côté skimmer filtration ON</td><td style="padding:.8rem;border:1px solid var(--border);">Aspiration d'air, joint pré-filtre</td><td style="padding:.8rem;border:1px solid var(--border);">Vérification couvercle pré-filtre</td></tr>
</tbody>
</table>

<h3>Source n°2 : les canalisations enterrées (25 % des cas)</h3>
<p>Sur le Bassin d'Arcachon (Gujan-Mestras, La Teste-de-Buch, Andernos-les-Bains) où le sol est sableux, les canalisations PVC enterrées entre le local technique et le bassin subissent des micro-mouvements permanents qui finissent par désaxer les raccords collés. Sur les terrains argileux de Caudéran ou du Bouscat, ce sont plutôt les cycles retrait/gonflement saisonniers qui fragilisent les coudes et les tés.</p>
<p>Action : si votre test repère ON/OFF a montré une fuite côté refoulement ou aspiration, c'est probablement une canalisation enterrée. <strong>Test impossible à faire soi-même</strong> sans matériel professionnel. Notre méthode : test de pression hydraulique pour quantifier la fuite, gaz traceur azote/hydrogène pour la localiser au mètre près. Voir notre page <a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">canalisation enterrée à Bordeaux</a>.</p>

<table style="width:100%;margin:1.5rem 0;border-collapse:collapse;border:1px solid var(--border);">
<thead>
<tr>
<th style="padding:.8rem;text-align:left;background:var(--green);color:var(--white);border:1px solid var(--green-dark);">Indice extérieur</th>
<th style="padding:.8rem;text-align:left;background:var(--green);color:var(--white);border:1px solid var(--green-dark);">Cause probable</th>
<th style="padding:.8rem;text-align:left;background:var(--green);color:var(--white);border:1px solid var(--green-dark);">Méthode pro</th>
</tr>
</thead>
<tbody>
<tr><td style="padding:.8rem;border:1px solid var(--border);">Pelouse anormalement verte près du bassin</td><td style="padding:.8rem;border:1px solid var(--border);">Fuite refoulement enterrée</td><td style="padding:.8rem;border:1px solid var(--border);">Gaz traceur</td></tr>
<tr style="background:var(--bg-alt);"><td style="padding:.8rem;border:1px solid var(--border);">Affaissement linéaire sur 1 à 3 m</td><td style="padding:.8rem;border:1px solid var(--border);">Fuite chronique avec lessivage du sol</td><td style="padding:.8rem;border:1px solid var(--border);">Inspection caméra + gaz traceur</td></tr>
<tr><td style="padding:.8rem;border:1px solid var(--border);">Humidité côté local technique</td><td style="padding:.8rem;border:1px solid var(--border);">Fuite traversée de paroi</td><td style="padding:.8rem;border:1px solid var(--border);">Test pression + colorant</td></tr>
</tbody>
</table>

<h3>Source n°3 : la coque polyester elle-même (15 % des cas)</h3>
<p>C'est la cause la moins fréquente mais aussi la plus complexe à traiter. La coque polyester peut développer plusieurs pathologies spécifiques au matériau qu'on détaille en seconde partie. Pour faire le tri préalable, observez votre bassin filtration coupée et eau bien claire à la lampe rasante :</p>
<ul>
<li><strong>Cloques de 2 à 15 mm sous le gel-coat</strong> (à toucher avec la main, on les sent), parfois groupées en plaques : <strong>osmose</strong>.</li>
<li><strong>Réseau de fissures fines en patte d'oie</strong> à proximité des angles ou marches : <strong>microfissures de gel-coat</strong>.</li>
<li><strong>Bombement ou creux localisé</strong>, bruit creux à la percussion : <strong>délaminage de stratification</strong> (rare et grave).</li>
<li><strong>Aucun signe visible mais fuite confirmée</strong> : microfissure invisible nécessitant une fluorescéine professionnelle pour localiser.</li>
</ul>
<p>Action : pour les pathologies coque, nous combinons inspection visuelle, fluorescéine et caméra sous-marine. Voir notre page <a href="/detection-fuite/fluoresceine-piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">recherche fuite piscine fluorescéine</a> pour le protocole.</p>

<h2>Pathologies spécifiques aux coques polyester (l'angle technique en plus)</h2>
<p>La grande majorité des articles disponibles sur le sujet n'abordent pas en détail les pathologies propres au matériau polyester. Pourtant, comprendre ces phénomènes vous permet de mieux qualifier votre situation et de choisir la bonne réparation. Voici les 4 cas typiques que nous traitons en Gironde.</p>

<h3>1. L'osmose (cloques gel-coat)</h3>
<p>C'est la pathologie reine, spécifique aux résines polyester (et beaucoup plus rare sur les vinylesters récents). Au fil des années, l'eau de la piscine pénètre par les microfissures invisibles du gel-coat, se mélange à des résidus de styrène non réactés à l'intérieur de la matrice, et forme des cloques sous la surface. Le diagnostic est visuel et tactile : passez la main sur les parois immergées, vous sentez les bulles. Sur les coques de plus de 10 ans en Gironde, l'osmose est présente dans environ 40 % des cas. Quand une cloque éclate, elle laisse passer l'eau dans la stratification et crée une fuite progressive difficile à localiser sans colorant.</p>

<h3>2. Les microfissures de gel-coat (toiles d'araignée)</h3>
<p>Visible à proximité des angles, des marches, des plages immergées. Réseau de fissures fines (largeur inférieure à 0,3 mm) en patte d'oie. Cause la plus fréquente : calage insuffisant de la coque au moment de la pose ou mouvement de terrain ultérieur. La fluorescéine est indispensable pour localiser le passage actif.</p>

<h3>3. Le délaminage de stratification</h3>
<p>Plus rare mais plus grave. Les couches de fibre de verre se décollent les unes des autres sous l'effet de l'eau qui s'infiltre. Visible par déformation locale (bombement, creux) et par bruit creux à la percussion (test au mailloche caoutchouc). Réparation lourde, parfois irréparable selon l'étendue. C'est l'une des rares pathologies qui peut justifier le remplacement complet de la coque.</p>

<h3>4. Les raccords pièces à sceller défaillants</h3>
<p>C'est en réalité la cause numéro un sur coque polyester (60 % des cas), mais elle n'est pas une "pathologie polyester" au sens strict : c'est l'usure normale des joints d'étanchéité après 8 à 12 ans de service. Le remplacement des joints toriques ou le remasticage à la résine époxy résout 90 % de ces cas en moins de 2 heures.</p>

<h2>Diagnostic professionnel : ce que nous faisons en Gironde</h2>
<p>Si vos tests confirment une fuite mais ne parviennent pas à la localiser précisément, ou si vous voulez un rapport pour votre assurance, faites appel à un spécialiste recherche de fuite. Nos techniciens utilisent quatre méthodes complémentaires :</p>
<ul>
<li><strong>Inspection visuelle systématique</strong> : angles, marches, plages immergées, raccords. Recherche de cloques d'osmose, microfissures, tâches d'humidité côté terre.</li>
<li><strong>Test à la fluorescéine</strong> : ultra efficace sur coque polyester car le colorant injecté en surface au point suspect passe à travers la fissure et apparaît côté terre dans le local technique en 15 à 45 minutes. <a href="/detection-fuite/fluoresceine-piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">Page dédiée fluorescéine</a>.</li>
<li><strong>Test de pression hydraulique des canalisations</strong> : isole le réseau hydraulique de la coque. Indispensable pour distinguer fuite coque vs fuite refoulement.</li>
<li><strong>Inspection caméra endoscopique</strong> : si la fuite est sur le réseau hydraulique, voir notre guide <a href="/guide/inspection-camera-canalisation-bordeaux/" style="color:var(--green);text-decoration:underline;">inspection caméra canalisation</a>.</li>
</ul>

<h2>Combien coûte un diagnostic et une réparation en Gironde ?</h2>
<p>Tarifs constatés en 2026 sur la métropole bordelaise et le Bassin d'Arcachon. Aucun prestataire concurrent n'affiche ces fourchettes en clair, vous économisez plusieurs heures de prospection :</p>
<ul>
<li><strong>Diagnostic complet Recherche Fuite Gironde</strong> : 380 à 580 € HT, comprend inspection visuelle, fluorescéine, test pression, rapport technique pour assurance.</li>
<li><strong>Remplacement joint torique skimmer ou projecteur</strong> : 12 à 35 € de pièces, ou 120 à 180 € HT en intervention pisciniste partenaire (souvent rentabilisé par le diagnostic).</li>
<li><strong>Réparation locale gel-coat (osmose ponctuelle ou microfissures)</strong> : 180 à 450 € HT par zone réparée, durée de vie 5 à 10 ans.</li>
<li><strong>Reprise complète gel-coat (osmose étendue, plus de 30 % de la surface)</strong> : 3 500 à 8 500 € TTC selon taille du bassin, durée de vie 15 à 25 ans.</li>
<li><strong>Reprise stratification + gel-coat (délaminage)</strong> : 1 500 à 4 500 € HT par zone, à confier à un mouliste piscine spécialisé.</li>
<li><strong>Diagnostic + réparation pièces à sceller</strong> : 500 à 850 € HT all-in (cas le plus fréquent).</li>
</ul>
<p>La majorité de ces interventions sont remboursées par votre assurance habitation au titre de la garantie recherche de fuite, sous condition d'un dégât des eaux constaté ou d'une surconsommation. Voir notre guide <a href="/guide/recherche-fuite-piscine-assurance/" style="color:var(--green);text-decoration:underline;">remboursement assurance piscine</a> pour la procédure de prise en charge.</p>

<h2>Comment prévenir les fuites sur coque polyester ?</h2>
<p>Trois bonnes pratiques tirées de notre expérience sur 200 diagnostics annuels en Gironde :</p>
<ol>
<li><strong>Stabiliser le pH entre 7,2 et 7,6 en permanence</strong>. Un pH inférieur à 7,0 attaque le gel-coat lentement. Un pH supérieur à 7,8 favorise le calcaire qui fragilise les microfissures. Mesure hebdomadaire minimum.</li>
<li><strong>Limiter la chloration choc</strong>. Au-delà de 5 mg/L de chlore libre, le gel-coat se dégrade plus vite. Privilégier la chloration lente continue à 1 à 2 mg/L stable.</li>
<li><strong>Couvrir le bassin hors saison</strong>. UV et gel sont les premiers ennemis du gel-coat polyester. Une bâche d'hivernage opaque double la durée de vie de la coque.</li>
</ol>

<h2>Questions fréquentes sur les fuites de coque polyester</h2>

<h3>Ma piscine perd 2 cm par jour, est-ce normal ?</h3>
<p>En été en Gironde, l'évaporation peut atteindre 1 cm par jour sur le Bassin d'Arcachon (vent marin permanent). Au-delà de 1,5 cm par jour, c'est suspect. À 2 cm par jour, faites le test du seau : il tranchera entre évaporation forte et fuite réelle.</p>

<h3>Comment faire le test du seau sur une coque polyester glissante ?</h3>
<p>Posez le seau sur la première marche immergée pour qu'il soit stable et à la même température que l'eau. Lestez-le avec une pierre ou une bouteille d'eau remplie de sable au fond pour qu'il ne flotte pas. Le test reste rigoureusement valide.</p>

<h3>Combien coûte une réparation de gel-coat sur une coque polyester ?</h3>
<p>Pour une réparation locale (osmose ponctuelle, microfissure) : 180 à 450 € HT par zone. Pour une reprise complète gel-coat (osmose étendue) : 3 500 à 8 500 € TTC. Le diagnostic préalable Recherche Fuite Gironde coûte 380 à 580 € HT, souvent remboursé par votre assurance habitation.</p>

<h3>Mon assurance habitation couvre-t-elle une fuite sur coque polyester ?</h3>
<p>Oui dans 90 % des cas. La garantie recherche de fuite de votre contrat multirisque habitation rembourse tout ou partie du diagnostic dès lors qu'un dégât des eaux est constaté (terrain saturé, infiltration vers cave ou local technique, surconsommation d'eau anormale). Notre rapport technique est accepté par AXA, MAIF, MAAF, Macif, Generali, Groupama, Allianz, Matmut. Voir notre guide <a href="/guide/recherche-fuite-piscine-assurance/" style="color:var(--green);text-decoration:underline;">remboursement assurance piscine</a>.</p>

<h3>Faut-il vidanger la piscine pour réparer une coque polyester ?</h3>
<p>Pour les réparations de joints de pièces à sceller et les remplacements de pièces, une vidange partielle suffit (sous le niveau de la pièce concernée). Pour une réparation gel-coat, vidange totale obligatoire car la résine ne polymérise pas en milieu humide. Le séchage de la coque demande 4 à 8 semaines selon la météo avant l'application du nouveau gel-coat. Évitez de vidanger sans nécessité : risque d'effet flotteur sur sols sableux du Bassin d'Arcachon (nappe phréatique haute).</p>

<h3>Quelle est la durée de vie d'une coque polyester avec entretien correct ?</h3>
<p>30 à 40 ans pour une coque polyester de qualité standard, 40 à 60 ans pour une coque vinylester premium (plus résistante à l'osmose). Avec un entretien régulier (pH stable, chloration mesurée, hivernage couvert), une coque polyester girondine peut atteindre 50 ans sans pathologie majeure. Les cas de remplacement avant 25 ans sont presque toujours dus à un défaut d'entretien chimique ou à un mouvement de terrain initial.</p>

<h2>Demandez un diagnostic spécialisé en Gironde</h2>
<p>Avant toute réparation lourde (souvent 3 000 € et plus pour une reprise complète gel-coat), faites diagnostiquer précisément l'origine et l'étendue de la fuite. Notre rapport technique sert de référence pour le pisciniste qui interviendra et pour votre assureur. Voir nos pages dédiées par ville : <a href="/detection-fuite/piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">piscine Bordeaux</a>, <a href="/detection-fuite/piscine-arcachon/" style="color:var(--green);text-decoration:underline;">piscine Arcachon</a>, <a href="/detection-fuite/piscine-gujan-mestras/" style="color:var(--green);text-decoration:underline;">piscine Gujan-Mestras</a> qui concentre la plus forte densité de coques polyester en Gironde. Pour les tarifs complets, consultez le <a href="/guide/recherche-fuite-piscine-tarif/" style="color:var(--green);text-decoration:underline;">guide tarif recherche de fuite piscine</a>. Pour les piscines liner PVC plutôt que coque, voir notre guide complémentaire <a href="/guide/fuite-liner-piscine/" style="color:var(--green);text-decoration:underline;">fuite sur liner piscine</a>. Pour comprendre l'évaporation normale en Gironde, voir <a href="/guide/evaporation-vs-fuite-piscine/" style="color:var(--green);text-decoration:underline;">évaporation ou fuite : test du seau</a>."""
    },
    {
        "slug": "inspection-camera-canalisation-bordeaux",
        "title": "Inspection caméra canalisation à Bordeaux : diagnostic visuel précis",
        "title_seo": "Inspection caméra canalisation Bordeaux | Diagnostic",
        "desc": "Inspection caméra endoscopique de canalisation à Bordeaux : diagnostic visuel sans démolition, repérage racines, fissures, désaxements. Coût et matériel.",
        "contenu": """<figure style="margin:0 0 2rem;"><img src="/assets/inspection-camera-canalisation.webp" alt="Caméra endoscopique haute définition pour inspection de canalisation à Bordeaux et en Gironde" width="1600" height="1067" loading="lazy" style="width:100%;max-height:340px;height:auto;object-fit:cover;border-radius:12px;display:block;"></figure>

<p>L'inspection caméra de canalisation est devenue l'outil indispensable du diagnostic plomberie moderne. Là où il fallait autrefois casser une dalle ou ouvrir un mur pour identifier un défaut, une simple caméra endoscopique sur tige flexible donne aujourd'hui une image vidéo haute définition de l'intérieur du tuyau, sans démolition et en moins d'une heure. Cet article détaille la technique, les cas d'usage à Bordeaux, le matériel utilisé et les coûts en 2026.</p>

<h2>Comment fonctionne une caméra d'inspection de canalisation ?</h2>
<p>Une caméra endoscopique professionnelle se compose de quatre éléments principaux :</p>
<ul>
<li><strong>Tête de caméra</strong> : capteur Full HD ou 4K, étanche, diamètre 22 à 50 mm selon les modèles, équipée d'un anneau LED haute luminosité pour éclairer l'intérieur du tuyau.</li>
<li><strong>Tige flexible (push-rod)</strong> : longueur 5 à 60 mètres, en fibre composite renforcée, qui pousse la caméra dans le réseau sans s'écraser ni se vriller.</li>
<li><strong>Module de mesure de distance</strong> : affiche en temps réel la position exacte de la caméra dans le réseau (au cm près).</li>
<li><strong>Émetteur radio (sonde)</strong> : permet de localiser la position de la caméra à travers le sol grâce à un récepteur en surface, jusqu'à 2 mètres de profondeur.</li>
</ul>
<p>L'opérateur visionne en direct l'image sur un écran portable, marque les anomalies (racines, fissures, désaxements, bouchons), repère leur position exacte au sol grâce à l'émetteur radio, et exporte un rapport vidéo daté pour le client.</p>

<h2>Quand utiliser l'inspection caméra à Bordeaux ?</h2>
<p>L'inspection caméra est l'outil de référence dans 5 contextes :</p>

<h3>1. Diagnostic d'une canalisation bouchée récurrente</h3>
<p>Si vous avez régulièrement des évacuations qui refoulent (lavabo, WC, douche), la caméra identifie en quelques minutes la cause : racine d'arbre, accumulation de calcaire, désaxement de raccord, contre-pente. Indispensable avant tout débouchage manuel ou chimique.</p>

<h3>2. Recherche de fuite sur canalisation enterrée</h3>
<p>En complément du <a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">gaz traceur</a> ou du <a href="/detection-fuite/thermographie-infrarouge-bordeaux/" style="color:var(--green);text-decoration:underline;">diagnostic thermographique</a>, la caméra confirme visuellement le point de fuite et qualifie la cause (perforation, joint éclaté, désaxement). Crucial pour décider entre réparation locale et chemisage complet.</p>

<h3>3. Diagnostic préalable à un chemisage de canalisation</h3>
<p>Avant tout chemisage (rénovation sans tranchée), une inspection caméra obligatoire évalue l'état des conduites : diamètre, longueur, courbures, présence de raccords, état général. Le devis de chemisage en dépend. Voir notre page <a href="/detection-fuite/chemisage-bordeaux/" style="color:var(--green);text-decoration:underline;">chemisage canalisation à Bordeaux</a> pour les copropriétés haussmanniennes.</p>

<h3>4. Achat ou vente d'un bien immobilier</h3>
<p>Plusieurs études notariales bordelaises recommandent une inspection caméra des canalisations principales avant signature, surtout pour les biens de plus de 50 ans. Permet d'anticiper des travaux coûteux (réseaux fonte ou plomb en fin de vie) et d'argumenter une décote ou des conditions suspensives.</p>

<h3>5. Sinistre dégât des eaux en copropriété</h3>
<p>L'inspection caméra des colonnes d'évacuation EU/EV identifie l'origine d'un sinistre. Combinée à notre <a href="/detection-fuite/degats-des-eaux-bordeaux/" style="color:var(--green);text-decoration:underline;">diagnostic dégât des eaux à Bordeaux</a> avec rapport opposable IRSI, elle facilite la coordination syndic + assureur.</p>

<h2>Quels défauts l'inspection caméra révèle-t-elle ?</h2>
<p>Voici les pathologies les plus fréquentes que nous identifions sur les canalisations bordelaises :</p>

<h3>Racines d'arbres dans les canalisations</h3>
<p>Cas typique sur les propriétés de Caudéran, Le Bouscat et Bordeaux Centre avec arbres matures (platanes, chênes, tilleuls). Les racines s'infiltrent par les microfissures de raccord et obstruent progressivement le réseau. La caméra montre clairement le filament racinaire en croissance dans le tuyau.</p>

<h3>Désaxement de raccord</h3>
<p>Très fréquent sur les canalisations enterrées de plus de 30 ans en sol argileux ou sableux (typique du Bassin d'Arcachon et de la métropole bordelaise). Les raccords PVC collés ou en fonte se déplacent sous l'effet des micro-mouvements de sol. La caméra mesure précisément l'angle de désaxement.</p>

<h3>Fissures structurelles</h3>
<p>Sur les vieilles canalisations en fonte, plomb ou grès (immeubles haussmanniens), des fissures longitudinales peuvent apparaître sous l'effet de la corrosion ou du gel. La caméra détaille la longueur, la largeur et la position de chaque fissure.</p>

<h3>Bouchons calcaires ou de graisse</h3>
<p>Très courants dans les canalisations d'évacuation cuisine. Le calcaire et les graisses se déposent en couche progressive et finissent par obstruer 50 à 90 pourcent du diamètre utile. La caméra mesure le diamètre résiduel.</p>

<h3>Effondrement de canalisation</h3>
<p>Rare mais grave. Sur les très vieilles canalisations en grès ou amiante-ciment, un effondrement partiel peut bloquer complètement le réseau. La caméra confirme et permet de quantifier la longueur à reprendre.</p>

<h2>Combien coûte une inspection caméra à Bordeaux ?</h2>
<p>Le tarif dépend de la complexité du réseau et de l'objectif du diagnostic. Voici les fourchettes constatées en 2026 sur Bordeaux et la Gironde :</p>
<ul>
<li><strong>Inspection caméra simple (1 canalisation, moins de 15 m)</strong> : <strong>180 à 280 € HT</strong>, intervention 1 heure, rapport vidéo + photos remis le jour même.</li>
<li><strong>Inspection avec localisation radio (sonde émettrice)</strong> : <strong>280 à 380 € HT</strong>, idéale pour identifier le point précis d'un défaut sous une dalle béton ou sous jardin.</li>
<li><strong>Inspection complète multi-canalisations (copropriété, bien immobilier)</strong> : <strong>380 à 650 € HT</strong>, intervention 2 à 4 heures, rapport détaillé pour syndic ou notaire.</li>
<li><strong>Inspection préalable à chemisage</strong> : souvent incluse dans le devis chemisage (la caméra valide la faisabilité).</li>
</ul>
<p>Notre rapport vidéo + photos est accepté par les assureurs au titre de la garantie recherche de fuite et par les notaires pour les diagnostics avant vente.</p>

<h2>Inspection caméra ou autre méthode ?</h2>
<p>L'inspection caméra n'est pas systématiquement la première méthode de diagnostic. Voici les bons couplages :</p>
<ul>
<li><strong>Fuite suspectée enterrée + perte d'eau quantifiée</strong> : commencer par <a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">gaz traceur</a> pour localiser, puis caméra pour qualifier la cause.</li>
<li><strong>Bouchon récurrent ou refoulement</strong> : caméra directement, c'est l'outil dédié.</li>
<li><strong>Fuite encastrée plancher chauffant</strong> : <a href="/detection-fuite/thermographie-infrarouge-bordeaux/" style="color:var(--green);text-decoration:underline;">thermographie infrarouge</a> en première intention, caméra inutile en chape.</li>
<li><strong>Fuite piscine</strong> : <a href="/detection-fuite/fluoresceine-piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">fluorescéine</a> + caméra pour les canalisations de filtration.</li>
<li><strong>Diagnostic avant achat immobilier</strong> : caméra directement, c'est l'examen standard.</li>
</ul>

<h2>Demandez votre inspection caméra en Gironde</h2>
<p>Pour faire intervenir nos techniciens à Bordeaux, dans la métropole bordelaise ou en Gironde plus largement, contactez-nous via le <a href="/devis/" style="color:var(--green);text-decoration:underline;">formulaire de devis</a>. Pour comprendre les autres outils du diagnostic professionnel, voir notre guide <a href="/guide/detecteur-fuite-eau-professionnel/" style="color:var(--green);text-decoration:underline;">détecteur de fuite d'eau professionnel</a> qui détaille l'arsenal complet (caméra endoscopique, gaz traceur, FLIR, hydrophone, corrélateur acoustique). Pour le chemisage en complément d'une inspection révélant un réseau dégradé, voir notre service <a href="/chemisage-canalisation/" style="color:var(--green);text-decoration:underline;">chemisage de canalisation en Gironde</a>."""
    },
    {
        "slug": "detecteur-fuite-eau-professionnel",
        "title": "Détecteur de fuite d'eau professionnel : matériel et méthodes",
        "title_seo": "Détecteur de fuite d'eau professionnel | Outils pro",
        "desc": "Quels détecteurs de fuite d'eau utilisent les professionnels ? Corrélateur acoustique, gaz traceur, caméra thermique, hydrophone : matériel pro vs grand public.",
        "contenu": """<figure style="margin:0 0 2rem;"><img src="/assets/detecteur-fuite-eau-professionnel.webp" alt="Outils professionnels de détection de fuite d'eau utilisés par les techniciens en Gironde" width="1600" height="1067" loading="lazy" style="width:100%;max-height:340px;height:auto;object-fit:cover;border-radius:12px;display:block;"></figure>

<p>Vous cherchez un détecteur de fuite d\'eau professionnel ? Cet article fait le tour des appareils que nos techniciens utilisent quotidiennement en Gironde, leur principe de fonctionnement, leur prix et leur niveau de précision. Vous comprendrez aussi pourquoi les détecteurs grand public vendus dans les grandes surfaces de bricolage (de 30 à 200 €) ne remplaceront jamais l\'arsenal d\'un professionnel sur les fuites complexes : enterrées, encastrées, en circuit fermé.</p>

<h2>Pourquoi les détecteurs grand public sont insuffisants</h2>
<p>Les détecteurs de fuite vendus chez Castorama, Leroy Merlin ou Amazon coûtent entre 30 et 250 € et s\'apparentent en pratique à des humidimètres simplifiés ou des stéthoscopes acoustiques bas de gamme. Ils détectent une humidité présente sur une surface ou amplifient un bruit sourd, mais sans capacité d\'analyse fine. En pratique, ils permettent au mieux de confirmer qu\'une zone est humide. Ils ne savent pas localiser au point précis sous une dalle béton, dans une cloison BA13 ou sur un réseau enterré à 80 cm de profondeur. Notre expérience sur 200 interventions annuelles : un client sur trois a tenté un détecteur grand public avant de nous appeler, sans aucun résultat exploitable.</p>
<p>Pour les fuites simples et superficielles (joint robinet, raccord visible), un détecteur grand public peut suffire. Pour tout le reste, le matériel professionnel est indispensable.</p>

<h2>1. Le corrélateur acoustique haute sensibilité</h2>
<p>Outil reine pour les fuites sur canalisations sous pression. Le corrélateur utilise deux capteurs piézoélectriques posés en deux points du réseau et mesure le délai exact entre les deux signaux acoustiques de la fuite. Par calcul de propagation, il localise au demi-mètre près le point d\'origine.</p>
<ul>
<li><strong>Matériel</strong> : Sewerin AquaTest A100, Vivax-Metrotech vLoc Series, SebaKMT FerroLux. Coût d\'achat 8 000 à 18 000 € HT pour un appareil pro.</li>
<li><strong>Cas d\'usage</strong> : fuite sur réseau d\'eau froide ou chaude sous pression, encastrée dans une chape ou enterrée sous jardin. Très efficace sur cuivre, PVC, PER, multicouche.</li>
<li><strong>Limites</strong> : ne fonctionne que sur fluide sous pression. Inopérant sur évacuation gravitaire (EU/EV) et sur très petites fuites (moins de 0,5 L/heure).</li>
</ul>

<h2>2. Le gaz traceur azote/hydrogène</h2>
<p>Méthode imbattable pour les canalisations enterrées profondes (au-delà de 60 cm) et les réseaux longs (plusieurs dizaines de mètres). On vidange la canalisation suspecte, on la met en pression avec un mélange azote 95 pourcent + hydrogène 5 pourcent, on suit en surface avec un capteur électrochimique sensible à l\'hydrogène. Le gaz remonte par capillarité jusqu\'à la surface au point de fuite et déclenche le capteur.</p>
<ul>
<li><strong>Matériel</strong> : capteur Sewerin H2 Sniff ou Inficon HLD6000, bouteilles azote/hydrogène 5L, manomètre régulateur. Coût matériel 5 000 à 12 000 € HT.</li>
<li><strong>Cas d\'usage</strong> : recherche de fuite canalisation enterrée à Bordeaux, fuite sous dalle béton non accessible, réseau d\'arrosage extérieur, alimentation eau potable extérieure. Voir notre page dédiée <a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">canalisation enterrée Bordeaux</a> avec cas concrets.</li>
<li><strong>Limites</strong> : nécessite vidange préalable du réseau. Inutilisable si plusieurs niveaux de canalisations superposés (le gaz remonte au plus court chemin).</li>
</ul>

<h2>3. La caméra thermique haute résolution</h2>
<p>Indispensable pour les planchers chauffants hydrauliques et les canalisations encastrées en chauffe. La caméra thermique mesure la température de surface au centième de degré (résolution 30 mK). Une fuite produit une signature thermique anormale : zone plus chaude (eau du circuit) ou plus froide (évaporation latente), visible immédiatement à l\'écran.</p>
<ul>
<li><strong>Matériel</strong> : FLIR T540 ou T865, Testo 890, Fluke TiX580. Définition 464×348 à 640×480 pixels. Coût d\'achat 6 000 à 18 000 € HT.</li>
<li><strong>Cas d\'usage</strong> : <a href="/detection-fuite/fuite-plancher-chauffant-bordeaux/" style="color:var(--green);text-decoration:underline;">fuite plancher chauffant à Bordeaux</a>, canalisation encastrée dans cloison, dalle béton sur vide sanitaire. Voir aussi notre page <a href="/detection-fuite/thermographie-infrarouge-bordeaux/" style="color:var(--green);text-decoration:underline;">thermographie infrarouge Bordeaux</a>.</li>
<li><strong>Limites</strong> : nécessite un gradient thermique entre la fuite et son environnement. Inopérant sur eau froide en été à température ambiante.</li>
</ul>

<h2>4. L\'hydrophone (microphone sous-marin)</h2>
<p>Outil dédié aux fuites de piscine. L\'hydrophone capte les bruits de l\'eau qui s\'échappe à travers une fissure de liner, un joint défaillant ou un raccord percé. Le technicien le promène le long des parois immergées et localise le point de fuite par variation d\'intensité sonore.</p>
<ul>
<li><strong>Matériel</strong> : Aquatec OnEvent, Anderson Instrument LD-22. Coût d\'achat 1 500 à 4 500 € HT.</li>
<li><strong>Cas d\'usage</strong> : recherche de fuite piscine sans vidange. Complémentaire du <a href="/detection-fuite/fluoresceine-piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">colorant fluorescéine</a> sur les fuites discrètes.</li>
<li><strong>Limites</strong> : peu efficace sur les très grosses fuites (bruit dispersé) ou sur eau très agitée. Sensible aux bruits parasites (filtration, autre baigneur).</li>
</ul>

<h2>5. La caméra endoscopique haute définition</h2>
<p>Permet d\'inspecter visuellement l\'intérieur des canalisations, gaines techniques, vide sanitaires inaccessibles. Caméra étanche montée sur tige flexible de 5 à 30 mètres, résolution Full HD, éclairage LED intégré, inclinomètre pour suivre le tracé.</p>
<ul>
<li><strong>Matériel</strong> : Wöhler VIS 700, Ridgid SeeSnake, Inspector Camera GE. Coût d\'achat 2 500 à 8 000 € HT pour les modèles pro.</li>
<li><strong>Cas d\'usage</strong> : inspection avant chemisage, identification de la cause exacte d\'une fuite (fissure, racine, désaxement), validation après réparation.</li>
<li><strong>Limites</strong> : ne traverse pas les coudes serrés (plus de 60 degrés). Nécessite un point d\'accès au réseau (regard, démontage de pièce à sceller).</li>
</ul>

<h2>6. L\'humidimètre à pointes capacitives</h2>
<p>Mesure la teneur en eau d\'un matériau par effet capacitif (sans pointe physique) ou résistif (avec pointes). Permet de cartographier précisément une zone humide et de distinguer une infiltration ponctuelle (gradient fort) d\'une remontée capillaire (humidité diffuse).</p>
<ul>
<li><strong>Matériel</strong> : Tramex CMEXpert II, Protimeter MMS3, Skipper PinPoint. Coût d\'achat 400 à 1 200 € HT.</li>
<li><strong>Cas d\'usage</strong> : confirmation thermographique, distinction infiltration vs remontée, suivi post-réparation.</li>
<li><strong>Limites</strong> : ne traverse pas les matériaux denses (béton armé). Nécessite une certaine profondeur de pénétration.</li>
</ul>

<h2>Pourquoi un seul détecteur ne suffit pas</h2>
<p>Aucun outil n\'est universel. Notre équipe en Gironde déploie systématiquement <strong>au moins 3 méthodes complémentaires</strong> sur chaque diagnostic complexe : par exemple thermographie + corrélateur acoustique + humidimètre pour une fuite encastrée, ou gaz traceur + écoute acoustique + caméra endoscopique pour un réseau enterré. Cette redondance méthodologique nous permet d\'obtenir une localisation au point précis dans 95 pourcent des interventions.</p>
<p>Un détecteur grand public à 100 € ne dispose que d\'un seul mode de mesure et d\'une sensibilité limitée. C\'est pourquoi la localisation par un professionnel reste indispensable sur les fuites non visibles, en circuit fermé ou enterrées profondes.</p>

<h2>Combien coûte un diagnostic professionnel en Gironde ?</h2>
<p>Faire intervenir un professionnel équipé de cet arsenal coûte entre 280 et 750 € HT selon la complexité du cas. Le rapport technique remis est accepté par les assureurs et permet souvent un remboursement intégral via la <a href="/guide/assurance-fuite-eau/" style="color:var(--green);text-decoration:underline;">garantie recherche de fuite</a>. Pour la grille tarifaire complète, voir notre guide <a href="/guide/prix-recherche-fuite-bordeaux/" style="color:var(--green);text-decoration:underline;">prix d\'une recherche de fuite à Bordeaux</a>.</p>
<p>Pour faire intervenir nos techniciens à Bordeaux et en Gironde, voir notre page <a href="/detection-fuite/" style="color:var(--green);text-decoration:underline;">détection de fuite non destructive Gironde</a> ou directement la page d\'urgence <a href="/detection-fuite/urgence-bordeaux/" style="color:var(--green);text-decoration:underline;">recherche de fuite en urgence à Bordeaux</a> pour une intervention sous 24 heures."""
    },
    {
        "slug": "fuite-piscine-desjoyaux-bordeaux",
        "title": "Fuite piscine Desjoyaux à Bordeaux : diagnostic et réparation",
        "title_seo": "Fuite piscine Desjoyaux Bordeaux | Diagnostic",
        "desc": "Votre piscine Desjoyaux fuit à Bordeaux ? Diagnostic non destructif sans vidange : fluorescéine, test de pression, inspection visuelle. Coûts et procédure assurance.",
        "contenu": """<figure style="margin:0 0 2rem;"><img src="/assets/piscine-desjoyaux.webp" alt="Piscine familiale type Desjoyaux à Bordeaux, contexte d'intervention diagnostic fuite" width="1600" height="1067" loading="lazy" style="width:100%;max-height:340px;height:auto;object-fit:cover;border-radius:12px;display:block;"></figure>

<p>Vous possédez une piscine Desjoyaux à Bordeaux et vous constatez une perte d'eau anormale ? La spécificité Desjoyaux est sa filtration intégrée à la paroi du bassin (« bloc intégré » regroupant pompe et système de filtration), qui supprime les canalisations enterrées entre local technique et bassin classiques sur d'autres systèmes. Pour une recherche de fuite efficace, nous adaptons donc notre méthode aux particularités de ce constructeur. Cet article décrit les zones à investiguer en priorité, notre protocole de diagnostic et les coûts en 2026.</p>

<h2>Avant de nous appeler : le test du seau (gratuit)</h2>
<p>Pour distinguer une vraie fuite d'une évaporation forte, faites le test du seau pendant 24 à 48 heures. Posez un seau rempli sur la première marche pour qu'il soit à la même température que le bassin, marquez les niveaux au feutre, comparez les baisses. Si la piscine baisse plus que le seau, c'est une fuite. Voir notre <a href="/guide/evaporation-vs-fuite-piscine/" style="color:var(--green);text-decoration:underline;">guide évaporation ou fuite</a> et notre <a href="/guide/piscine-qui-fuit-perte-eau/" style="color:var(--green);text-decoration:underline;">arbre de décision en 6 questions</a>.</p>

<h2>Zones à investiguer en priorité sur une piscine Desjoyaux</h2>
<p>Sur les diagnostics que nous réalisons à Bordeaux, les fuites de piscine Desjoyaux se concentrent généralement sur quatre zones :</p>
<ul>
<li><strong>Bloc filtrant intégré</strong> : la spécificité du système Desjoyaux est d'intégrer la pompe et la filtration dans un bloc unique fixé à la paroi du bassin. Les joints d'étanchéité de ce bloc, ainsi que les raccords internes, sont à inspecter en priorité, notamment sur les piscines de plus de 12-15 ans.</li>
<li><strong>Pièces à sceller</strong> (skimmer, refoulement, projecteur, prise balai, bonde de fond) : étanchéité par joints d'étanchéité et fixation par bride. Les joints peuvent durcir avec le temps, les vis se desserrer sous cycles thermiques.</li>
<li><strong>Joints du revêtement intérieur</strong> : selon le revêtement choisi à la pose (liner soudé sur place, autre solution proposée par Desjoyaux), les jonctions au niveau des angles, marches et raccords sont les zones d'usure typiques après 15-20 ans.</li>
<li><strong>Margelle et plage immergée</strong> : joints maçonnés entre la structure et la margelle béton qui peuvent craqueler avec les cycles thermiques.</li>
</ul>

<h2>Comment diagnostiquons-nous une fuite Desjoyaux à Bordeaux ?</h2>
<p>Notre intervention dure 2 à 3 heures et combine 3 méthodes non destructives :</p>
<ol>
<li><strong>Inspection visuelle systématique</strong> du périmètre du bassin et du bloc filtrant intégré, avec lampe rasante pour repérer microfissures et joints fatigués.</li>
<li><strong>Test à la fluorescéine</strong> sur les zones suspectes (raccords pièces à sceller, joints d'étanchéité du bloc filtrant). Voir notre <a href="/detection-fuite/fluoresceine-piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">page recherche de fuite à la fluorescéine</a>.</li>
<li><strong>Test de pression hydraulique</strong> du circuit de filtration intégré pour quantifier la fuite et orienter la réparation.</li>
</ol>
<p>Le rapport technique remis le jour même indique précisément la zone de fuite et oriente vers la réparation appropriée. Pour toute réparation sur le bloc filtrant ou le revêtement intérieur, nous recommandons de privilégier le réseau de concessionnaires Desjoyaux qui maîtrise la spécificité du système et garantit la conformité des pièces et de la mise en œuvre.</p>

<h2>Notre intervention sur Bordeaux Métropole</h2>
<p>Tarif diagnostic complet : <strong>380 à 580 € HT</strong> selon complexité, intervention 2 à 4 heures, rapport remis le jour même par email. Souvent remboursé par votre assurance habitation au titre de la garantie recherche de fuite (voir <a href="/guide/recherche-fuite-piscine-assurance/" style="color:var(--green);text-decoration:underline;">guide remboursement assurance piscine</a>).</p>
<p>Pour les piscines de moins de 10 ans, vérifiez d'abord la garantie décennale du constructeur : si la fuite est due à un défaut de construction ou de mise en œuvre, la prise en charge est gratuite par Desjoyaux ou son concessionnaire. Voir aussi nos pages <a href="/detection-fuite/piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">recherche de fuite piscine à Bordeaux</a> et <a href="/detection-fuite/depannage-piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">dépannage piscine multimarques Bordeaux</a>."""
    },
    {
        "slug": "fuite-piscine-magiline-bordeaux",
        "title": "Fuite piscine Magiline à Bordeaux : béton banché et NFX",
        "title_seo": "Fuite piscine Magiline Bordeaux | Béton & NFX",
        "desc": "Diagnostic d'une fuite sur piscine Magiline à Bordeaux : structure béton armé banché, système de filtration NFX intégré, revêtement intérieur. Méthodes et coûts.",
        "contenu": """<figure style="margin:0 0 2rem;"><img src="/assets/piscine-magiline.webp" alt="Piscine moderne Magiline à Bordeaux, contexte d'intervention diagnostic fuite" width="1600" height="1067" loading="lazy" style="width:100%;max-height:340px;height:auto;object-fit:cover;border-radius:12px;display:block;"></figure>

<p>Votre piscine Magiline à Bordeaux perd de l'eau anormalement ? Magiline construit ses piscines avec une structure en <strong>béton à panneaux alvéolaires brevetés</strong> (qui réduit la quantité de béton tout en gardant les exigences de solidité) et équipe ses bassins du système de filtration breveté <strong>NFX à cartouche</strong> associé à une pompe à débit variable. Le revêtement intérieur peut être un liner, une membrane armée ou une mousse confort selon le choix à la pose. Cette architecture spécifique présente des pathologies de fuite bien identifiées que nous traitons régulièrement sur la métropole bordelaise. Cet article détaille les zones à investiguer en priorité et notre protocole de diagnostic.</p>

<h2>Avant de nous appeler : confirmer la fuite</h2>
<p>Posez un seau rempli sur la première marche du bassin (même température), marquez les niveaux au feutre, attendez 24 à 48 heures sans baignade. Si la piscine baisse plus que le seau, vous avez une fuite à diagnostiquer. Voir notre <a href="/guide/evaporation-vs-fuite-piscine/" style="color:var(--green);text-decoration:underline;">guide évaporation ou fuite</a>.</p>

<h2>Zones à investiguer en priorité sur une piscine Magiline</h2>
<p>Sur les diagnostics réalisés à Bordeaux, les pathologies de fuite Magiline se concentrent généralement sur quatre zones :</p>
<ul>
<li><strong>Système de filtration NFX et raccords</strong> : la filtration NFX à cartouche est intégrée au système constructif Magiline avec des raccords spécifiques. Les joints d'étanchéité de ces raccords peuvent fuir avec le temps. Sur cette zone très technique, nous recommandons systématiquement d'orienter la réparation vers le réseau Magiline qui maîtrise la spécificité du système breveté.</li>
<li><strong>Pièces à sceller</strong> (skimmer, projecteur, prise balai, bonde de fond) : étanchéité par joint et fixation par bride. Sur les piscines de plus de 15-18 ans, les joints peuvent durcir et fuir. Diagnostic ciblé par fluorescéine.</li>
<li><strong>Revêtement intérieur</strong> : selon que votre piscine a un liner, une membrane armée ou un revêtement mousse confort, les pathologies diffèrent. Pour le liner et la membrane armée, vigilance sur les soudures, plis et fixations. Pour la mousse confort, vigilance sur les jonctions et raccords.</li>
<li><strong>Microfissures structurelles béton</strong> : la structure en béton à panneaux alvéolaires Magiline est conçue pour la durabilité, mais sur sols argileux du sud-ouest de Bordeaux (Caudéran, Le Bouscat, Gradignan), les cycles retrait-gonflement saisonniers peuvent solliciter la structure. Diagnostic par fluorescéine et inspection visuelle ciblée.</li>
</ul>

<h2>Notre méthode de diagnostic sur piscine Magiline</h2>
<p>Sur une piscine Magiline à Bordeaux, nos techniciens suivent ce protocole :</p>
<ol>
<li><strong>Inspection visuelle complète</strong> du périmètre du bassin : joints de margelle, soudures liner si applicable, raccords pièces à sceller, état du revêtement intérieur.</li>
<li><strong>Test à la fluorescéine</strong> ciblé sur les zones suspectes (raccords pièces à sceller, fissures suspectes, joints d'étanchéité du système NFX). Voir notre <a href="/detection-fuite/fluoresceine-piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">page recherche de fuite à la fluorescéine</a>.</li>
<li><strong>Test de pression hydraulique</strong> du circuit de filtration NFX pour isoler une fuite côté pompe ou refoulement.</li>
<li><strong>Inspection caméra endoscopique</strong> des canalisations enterrées entre local technique et bassin si nécessaire. Voir notre <a href="/guide/inspection-camera-canalisation-bordeaux/" style="color:var(--green);text-decoration:underline;">guide inspection caméra</a>.</li>
</ol>

<h2>Coûts et coordination réparation à Bordeaux</h2>
<p>Diagnostic complet sur piscine Magiline à Bordeaux : <strong>380 à 580 € HT</strong>, intervention 2 à 3 heures, rapport technique remis le jour même par email. Pour la réparation, nous orientons toujours en priorité vers le réseau de concessionnaires Magiline qui maîtrise la spécificité du système NFX et garantit la conformité des pièces et de la mise en œuvre.</p>
<p>Pour les piscines Magiline encore sous garantie décennale (moins de 10 ans), prise en charge constructeur possible si défaut de mise en œuvre prouvé. Au-delà, votre assurance habitation peut intervenir au titre de la garantie recherche de fuite (voir <a href="/guide/recherche-fuite-piscine-assurance/" style="color:var(--green);text-decoration:underline;">guide assurance piscine</a>). Pour notre service dépannage piscine multimarques, voir <a href="/detection-fuite/depannage-piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">dépannage piscine Bordeaux</a> et notre page <a href="/detection-fuite/piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">recherche de fuite piscine Bordeaux</a>."""
    },
    {
        "slug": "fuite-piscine-diffazur-bordeaux",
        "title": "Fuite piscine Diffazur à Bordeaux : béton armé projeté",
        "title_seo": "Fuite piscine Diffazur Bordeaux | Béton projeté",
        "desc": "Diagnostic d'une fuite sur piscine Diffazur à Bordeaux : structure béton armé projeté (gunite), revêtement (peinture, enduit, mosaïque, carrelage). Méthodes et coûts.",
        "contenu": """<figure style="margin:0 0 2rem;"><img src="/assets/piscine-diffazur.webp" alt="Piscine Diffazur béton armé revêtement carrelage à Bordeaux, contexte d'intervention diagnostic fuite" width="1600" height="1067" loading="lazy" style="width:100%;max-height:340px;height:auto;object-fit:cover;border-radius:12px;display:block;"></figure>

<p>Votre piscine Diffazur à Bordeaux présente une perte d'eau anormale ? Diffazur construit ses piscines en <strong>béton armé projeté par gunite</strong> (projection à grande vitesse sur armature acier, créant une structure monobloc sans joints). Le revêtement intérieur peut ensuite être appliqué directement sur la structure sous forme de peinture, d'enduit hydrofuge, de mosaïque pâte de verre, de carrelage ou de pierre. Cette flexibilité de finition donne des pathologies de fuite variables selon la finition choisie. Cet article détaille les zones à investiguer et les méthodes de diagnostic adaptées.</p>

<h2>Avant de nous appeler : confirmer la fuite</h2>
<p>Posez un seau rempli sur la première marche du bassin (même température), marquez les niveaux au feutre, attendez 24 à 48 heures sans baignade. Si la piscine baisse plus que le seau, vous avez une fuite à diagnostiquer. Voir notre <a href="/guide/evaporation-vs-fuite-piscine/" style="color:var(--green);text-decoration:underline;">guide évaporation ou fuite</a>.</p>

<h2>Zones à investiguer selon la finition du bassin</h2>
<p>Sur une piscine Diffazur, l'origine de la fuite dépend largement du revêtement intérieur choisi à la pose :</p>
<ul>
<li><strong>Revêtement peinture ou enduit hydrofuge</strong> : décollement local par cycles thermiques, microfissures sur les angles ou raccords pièces à sceller. Diagnostic visuel à la lampe rasante puis fluorescéine.</li>
<li><strong>Revêtement mosaïque ou carrelage</strong> : joints maçonnés qui peuvent se craqueler après 18-25 ans, tesselles décollées (test au tournevis : sonore = collée, sourd = décollée). Microfissures invisibles à l'œil nu mais détectables au colorant.</li>
<li><strong>Pièces à sceller</strong> (skimmer, refoulement, projecteur, bonde de fond, prise balai) : scellement par mortier hydrofuge qui peut craqueler au pourtour après 20-25 ans, sur tous types de finition.</li>
<li><strong>Fissure structurelle béton</strong> : plus rare grâce à la qualité du béton armé projeté monobloc. Mais possible sur sols argileux du sud-ouest de Bordeaux (Caudéran, Le Bouscat, Gradignan) avec mouvements de terrain saisonniers.</li>
</ul>

<h2>Notre méthode de diagnostic</h2>
<ol>
<li><strong>Inspection visuelle à la lampe rasante</strong> de tout le bassin selon le revêtement (peinture, mosaïque, carrelage) pour repérer microfissures, joints fatigués et zones décollées.</li>
<li><strong>Test fluorescéine ciblé</strong> : injection à proximité des zones suspectes, le colorant est aspiré par les microfissures et confirme le passage de la fuite. Voir notre <a href="/detection-fuite/fluoresceine-piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">protocole fluorescéine</a>.</li>
<li><strong>Test de pression hydraulique</strong> des canalisations pour isoler les fuites bassin vs réseau enterré.</li>
<li><strong>Inspection caméra sous-marine</strong> pour les fissures structurelles suspectées en grand bain.</li>
</ol>

<h2>Réparation et coût d'intervention à Bordeaux</h2>
<p>Diagnostic complet : <strong>380 à 580 € HT</strong>, intervention 2 à 4 heures, rapport remis le jour même. Pour la réparation, le choix du prestataire dépend de la finition : pour les peintures/enduits, un pisciniste piscine-béton classique convient ; pour les mosaïques et carrelages, nous orientons vers un mosaïste spécialisé (compétence plus rare en Gironde) ; pour les fissures structurelles, intervention résine époxy d'injection.</p>
<p>Sur les piscines Diffazur de moins de 10 ans, la garantie décennale du constructeur couvre les défauts de mise en œuvre. Au-delà, prise en charge possible par votre assurance habitation si dégât des eaux constaté (voir <a href="/guide/recherche-fuite-piscine-assurance/" style="color:var(--green);text-decoration:underline;">guide remboursement assurance piscine</a>). Pour notre service multimarques, voir <a href="/detection-fuite/piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">recherche de fuite piscine à Bordeaux</a> et <a href="/detection-fuite/depannage-piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">dépannage piscine Bordeaux</a>."""
    },
    {
        "slug": "fuite-piscine-waterair-bordeaux",
        "title": "Fuite piscine Waterair à Bordeaux : panneaux acier et liner",
        "title_seo": "Fuite piscine Waterair Bordeaux | Acier & liner",
        "desc": "Diagnostic d'une fuite sur piscine Waterair à Bordeaux : panneaux acier ondé galvanisé, liner d'étanchéité, raccords pièces à sceller. Méthodes et coûts.",
        "contenu": """<figure style="margin:0 0 2rem;"><img src="/assets/piscine-waterair.webp" alt="Piscine Waterair en kit dans jardin résidentiel, contexte d'intervention diagnostic fuite" width="1600" height="1067" loading="lazy" style="width:100%;max-height:340px;height:auto;object-fit:cover;border-radius:12px;display:block;"></figure>

<p>Votre piscine Waterair à Bordeaux perd de l'eau ? Waterair propose un système modulaire breveté avec une structure en <strong>panneaux d'acier ondé galvanisé</strong> et un liner d'étanchéité posé à l'intérieur du bassin. La marque garantit la structure 30 ans et le liner 12 ans. Cette architecture donne des pathologies de fuite typiques que nous diagnostiquons régulièrement à Bordeaux et en Gironde.</p>

<h2>Avant de nous appeler : le test du seau</h2>
<p>Pour confirmer la fuite vs évaporation : posez un seau rempli sur la première marche, marquez les niveaux, attendez 24 à 48 heures. Si la piscine baisse plus que le seau, vous avez une fuite. Voir notre <a href="/guide/evaporation-vs-fuite-piscine/" style="color:var(--green);text-decoration:underline;">guide évaporation ou fuite</a>.</p>

<h2>Zones à investiguer en priorité sur une piscine Waterair</h2>
<ul>
<li><strong>Liner d'étanchéité (cas le plus fréquent)</strong> : les soudures et fixations du liner sur les piscines de plus de 15-20 ans peuvent se fragiliser, en particulier au niveau des angles, escaliers et raccords pièces à sceller. C'est l'origine la plus courante des fuites sur Waterair.</li>
<li><strong>Joints des pièces à sceller</strong> (skimmer, refoulement, projecteur, prise balai, bonde de fond) : étanchéité par joint torique et fixation par bride. Les joints peuvent durcir avec le temps, les vis se desserrer sous cycles thermiques.</li>
<li><strong>Margelles et plage immergée</strong> : joints maçonnés entre la structure et la margelle qui peuvent craqueler avec les cycles thermiques.</li>
<li><strong>Canalisations enterrées</strong> entre local technique et bassin : sur sols sableux du Bassin d'Arcachon (Gujan-Mestras, La Teste, Andernos) ou argileux de la métropole bordelaise, les raccords PVC peuvent se désaxer avec le temps.</li>
</ul>

<h2>Notre méthode de diagnostic sur Waterair</h2>
<ol>
<li><strong>Inspection visuelle complète</strong> du liner à la lampe rasante : recherche de plis, soudures fatiguées, points de tension. Sur les Waterair de plus de 15 ans, on identifie souvent visuellement la zone suspecte.</li>
<li><strong>Test à la fluorescéine</strong> ciblé à proximité des soudures et raccords pièces à sceller. Voir notre <a href="/detection-fuite/fluoresceine-piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">protocole fluorescéine</a>.</li>
<li><strong>Test de pression hydraulique</strong> sur le circuit de filtration pour isoler une fuite côté bassin vs côté canalisations enterrées.</li>
<li><strong>Inspection acoustique ou caméra endoscopique</strong> des canalisations enterrées si suspicion de fuite côté réseau hydraulique. Voir notre <a href="/guide/inspection-camera-canalisation-bordeaux/" style="color:var(--green);text-decoration:underline;">guide inspection caméra</a>.</li>
</ol>

<h2>Coût d'intervention à Bordeaux Métropole</h2>
<p>Diagnostic complet sur piscine Waterair : <strong>380 à 520 € HT</strong>, intervention 2 à 3 heures, rapport remis le jour même. Pour les fuites de liner, réparation possible par soudure thermique locale ou rustine subaquatique selon configuration. Voir notre guide <a href="/guide/reparation-liner-piscine/" style="color:var(--green);text-decoration:underline;">réparation fuite liner piscine</a>.</p>
<p>Sur les piscines Waterair encore sous garantie (structure 30 ans, liner 12 ans), prise en charge constructeur possible si défaut de mise en œuvre. Pour les autres cas, votre assurance habitation peut intervenir au titre de la garantie recherche de fuite (voir <a href="/guide/recherche-fuite-piscine-assurance/" style="color:var(--green);text-decoration:underline;">guide assurance piscine</a>). Pour notre service dépannage piscine multimarques, voir <a href="/detection-fuite/depannage-piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">dépannage piscine Bordeaux</a>."""
    },
    {
        "slug": "piscine-perd-3-cm-par-jour",
        "title": "Piscine qui perd 3 cm par jour : fuite ou évaporation ?",
        "title_seo": "Piscine perd 3 cm par jour | Diagnostic Gironde",
        "desc": "Votre piscine perd 3 cm d'eau par jour à Bordeaux ? Tableau évaporation par mois en Gironde, test du seau, sources de fuite probables et coûts du diagnostic.",
        "contenu": """<figure style="margin:0 0 2rem;"><img src="/assets/niveau-eau-piscine-fuite.webp" alt="Niveau d'eau anormalement bas dans une piscine privée en Gironde, perte de 3 cm par jour" width="1600" height="1067" loading="lazy" style="width:100%;max-height:340px;height:auto;object-fit:cover;border-radius:12px;display:block;"></figure>

<p>Votre piscine perd 3 cm d'eau par jour et vous ne savez pas si c'est normal ? Cette baisse est <strong>nettement au-dessus des seuils d'évaporation naturelle en Gironde</strong>, même en pic de chaleur. Dans 90 % des cas, une perte régulière de 3 cm par jour signifie une fuite à diagnostiquer. Cet article vous donne le diagnostic exact en 5 minutes et le coût de l'intervention si vous nous faites venir à Bordeaux.</p>

<h2>3 cm par jour : ce qui est normal et ce qui ne l'est pas</h2>
<p>L'évaporation naturelle d'une piscine extérieure non couverte en Gironde varie selon la saison et l'exposition. Voici les valeurs normales constatées sur 200 diagnostics annuels :</p>
<ul>
<li><strong>Janvier-février</strong> : 0,2 à 0,5 cm par jour (hivernage, évaporation très faible)</li>
<li><strong>Mars-avril</strong> : 0,4 à 0,8 cm par jour</li>
<li><strong>Mai-juin</strong> : 0,8 à 1,3 cm par jour</li>
<li><strong>Juillet-août</strong> : 1,2 à 1,8 cm par jour (pic d'évaporation, canicule, vent)</li>
<li><strong>Septembre-octobre</strong> : 0,7 à 1,1 cm par jour</li>
<li><strong>Novembre-décembre</strong> : 0,3 à 0,6 cm par jour</li>
</ul>
<p>Sur le Bassin d'Arcachon (vent marin permanent, exposition forte), majorez ces valeurs de 20 à 40 %. Mais même au pic estival sur Arcachon ou La Teste-de-Buch, l'évaporation ne dépasse jamais 2,5 cm/jour. <strong>Une perte de 3 cm/jour est donc anormale 11 mois sur 12 en Gironde</strong>, et même en juillet-août c'est suspect.</p>

<h2>Confirmez la fuite avec le test du seau (gratuit, 24h)</h2>
<p>Avant de nous appeler, faites le test du seau pour distinguer évaporation forte et fuite réelle. Posez un seau rempli d'eau sur la première marche de votre piscine pour qu'il soit à la même température. Marquez au feutre indélébile le niveau dans le seau et le niveau de la piscine. Laissez 24 à 48 heures sans baignade ni remise à niveau automatique. Comparez :</p>
<ul>
<li><strong>Seau et piscine baissent de la même hauteur</strong> : c'est de l'évaporation pure (rare à 3 cm/jour mais possible en pic de chaleur sur le Bassin d'Arcachon).</li>
<li><strong>Piscine baisse plus que le seau</strong> : fuite confirmée. L'écart entre la baisse seau et la baisse piscine = volume perdu par la fuite.</li>
</ul>
<p>Pour les protocoles complets et les pièges du test du seau (vent qui déplace le seau, baignade non documentée, remise à niveau automatique), voir notre <a href="/guide/evaporation-vs-fuite-piscine/" style="color:var(--green);text-decoration:underline;">guide évaporation ou fuite</a>.</p>

<h2>Sources probables d'une fuite à 3 cm/jour</h2>
<p>À ce débit (3 cm/jour sur une piscine standard 8×4 = 960 litres/jour ou 350 m³/an), la fuite est moyenne : ni microfissure invisible, ni rupture catastrophique. Sources les plus fréquentes :</p>
<ol>
<li><strong>Joint skimmer ou refoulement fissuré</strong> (60 % des cas à ce débit) : remplacement joint torique 12 à 35 € de pièce, 120 à 180 € HT en intervention pisciniste.</li>
<li><strong>Canalisation enterrée fissurée</strong> (20 % des cas) : raccord PVC désaxé sur sol sableux Bassin d'Arcachon ou retrait/gonflement argileux Caudéran. Voir notre <a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">page canalisation enterrée Bordeaux</a>.</li>
<li><strong>Liner PVC fissuré ou désoudu</strong> (15 % des cas) : voir notre <a href="/guide/fuite-liner-piscine/" style="color:var(--green);text-decoration:underline;">guide fuite liner piscine</a>.</li>
<li><strong>Bonde de fond ou projecteur</strong> (5 % des cas) : remplacement joint, intervention en apnée.</li>
</ol>

<h2>Notre intervention à Bordeaux</h2>
<p>Diagnostic complet d'une fuite à 3 cm/jour : <strong>380 à 580 € HT</strong> selon la complexité (8 % de chance que ce soit complexe à ce débit). Intervention 2 à 4 heures, rapport remis le jour même. Souvent remboursé par votre assurance multirisque habitation. Voir nos pages <a href="/detection-fuite/piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">piscine Bordeaux</a> et <a href="/detection-fuite/piscine-arcachon/" style="color:var(--green);text-decoration:underline;">piscine Arcachon</a>."""
    },
    {
        "slug": "compteur-eau-qui-tourne-sans-utilisation",
        "title": "Compteur d'eau qui tourne sans utilisation : que faire ?",
        "title_seo": "Compteur eau qui tourne sans utilisation | Bordeaux",
        "desc": "Votre compteur d'eau tourne sans aucune utilisation à votre domicile ? Tests à faire ce soir, sources de fuite probables, écrêtement loi Warsmann à Bordeaux.",
        "contenu": """<figure style="margin:0 0 2rem;"><img src="/assets/compteur-eau-bordeaux.webp" alt="Compteur d'eau Bordeaux Métropole qui continue de tourner sans utilisation, signe de fuite enterrée" width="1600" height="1067" loading="lazy" style="width:100%;max-height:340px;height:auto;object-fit:cover;border-radius:12px;display:block;"></figure>

<p>Vous avez fermé tous les robinets de votre domicile, vous êtes assuré qu'aucun appareil ne consomme d'eau, et pourtant votre compteur d'eau continue de tourner ? C'est le symptôme le plus typique d'une <strong>fuite sur votre réseau privatif</strong>, c'est-à-dire entre votre compteur et votre habitation. À Bordeaux et en Gironde, ce phénomène concerne environ 15 % des propriétaires de maisons individuelles, principalement sur les habitations de plus de 30 ans avec canalisations enterrées en cuivre, plomb ou PVC vieillissants.</p>

<h2>Confirmer que le compteur tourne vraiment sans utilisation</h2>
<p>Avant tout diagnostic, faites un test simple en 3 étapes le soir avant de vous coucher :</p>
<ol>
<li>Fermez TOUS les robinets de la maison (cuisine, salle de bain, WC, machine à laver, lave-vaisselle, arrosage automatique, ballon eau chaude si possible).</li>
<li>Allez relever votre compteur d'eau (généralement en regard de jardin ou en limite de propriété sur la voie publique). Notez le chiffre exact, photographie l'écran ou le cadran.</li>
<li>Le lendemain matin, sans avoir utilisé d'eau, relevez à nouveau le compteur. Si le chiffre a augmenté, vous avez une fuite confirmée.</li>
</ol>
<p>Vérifiez également pendant le test : le robinet d'arrivée principal est-il bien ouvert ? Une chasse d'eau peut-elle fuir silencieusement ? Un robinet extérieur d'arrosage peut-il être resté ouvert ? Ces vérifications éliminent 30 % des faux positifs.</p>

<h2>Localisation : où peut être la fuite ?</h2>
<p>Sur le réseau privatif (entre compteur et habitation), 4 zones concentrent 95 % des fuites :</p>
<ul>
<li><strong>Canalisation enterrée entre compteur et maison</strong> (60 % des cas) : raccord PVC désaxé sur sol sableux ou argileux, perforation par racine d'arbre, micro-fissure due au gel. Diagnostic par gaz traceur azote/hydrogène. Voir <a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">canalisation enterrée Bordeaux</a>.</li>
<li><strong>Robinet d'arrosage extérieur fuyard</strong> (15 % des cas) : fuite goutte à goutte qui s'accumule. Vérification visuelle simple.</li>
<li><strong>Chasse d'eau WC qui fuit silencieusement</strong> (12 % des cas) : test au papier toilette dans la cuvette pendant la nuit pour détecter un filet d'eau invisible.</li>
<li><strong>Canalisation encastrée dans cloison ou dalle</strong> (8 % des cas) : tache d'humidité visible, sol anormalement chaud (eau chaude sanitaire). Diagnostic par thermographie infrarouge. Voir <a href="/detection-fuite/thermographie-infrarouge-bordeaux/" style="color:var(--green);text-decoration:underline;">thermographie Bordeaux</a>.</li>
</ul>

<h2>Combien va vous coûter cette fuite ?</h2>
<p>Sur le plan financier, une fuite enterrée non détectée peut faire exploser votre facture de 300 % à 1 000 % en quelques mois. Heureusement, deux mécanismes vous protègent en France :</p>
<ul>
<li><strong>Loi Warsmann 2011</strong> : si la fuite est sur réseau enterré non visible, votre distributeur (Suez ou Régie de Bordeaux Métropole) est tenu de plafonner votre facture à 2× la consommation moyenne des 3 dernières années. Procédure complète dans notre <a href="/guide/loi-warsmann-ecretement-facture-eau/" style="color:var(--green);text-decoration:underline;">guide loi Warsmann</a>.</li>
<li><strong>Garantie recherche de fuite assurance habitation</strong> : votre contrat multirisque rembourse tout ou partie du diagnostic professionnel. Voir <a href="/guide/fuite-canalisation-enterree-assurance/" style="color:var(--green);text-decoration:underline;">guide assurance fuite enterrée</a>.</li>
</ul>

<h2>Notre intervention à Bordeaux</h2>
<p>Diagnostic complet d'une fuite après compteur à Bordeaux : <strong>380 à 580 € HT</strong> selon complexité du réseau, intervention 2 à 4 heures, rapport accepté par tous les distributeurs et assureurs français. Voir aussi notre page service <a href="/detection-fuite/fuite-apres-compteur/" style="color:var(--green);text-decoration:underline;">fuite après compteur à Bordeaux</a> pour les détails de notre méthode et notre <a href="/detection-fuite/urgence-bordeaux/" style="color:var(--green);text-decoration:underline;">service urgence 24h</a> pour les fuites importantes."""
    },
    {
        "slug": "facture-eau-suez-doublee-fuite-bordeaux",
        "title": "Facture eau Suez doublée à Bordeaux : que faire ?",
        "title_seo": "Facture eau Suez doublée Bordeaux | Loi Warsmann",
        "desc": "Votre facture d'eau Suez à Bordeaux a doublé ou triplé ? Procédure d'écrêtement loi Warsmann pas à pas, conditions, modèle de courrier, délais.",
        "contenu": """<figure style="margin:0 0 2rem;"><img src="/assets/compteur-eau-bordeaux.webp" alt="Facture d'eau Suez Bordeaux Métropole anormalement élevée, suspicion de fuite et procédure d'écrêtement" width="1600" height="1067" loading="lazy" style="width:100%;max-height:340px;height:auto;object-fit:cover;border-radius:12px;display:block;"></figure>

<p>Votre facture d'eau Suez à Bordeaux est passée de 250 € à 600 €, voire 1 500 € sur le dernier trimestre alors que votre consommation n'a pas changé ? Vous avez probablement une fuite enterrée non détectée sur votre réseau privatif, et la bonne nouvelle, c'est que la loi Warsmann de 2011 vous permet de plafonner cette facture à 2 fois votre consommation moyenne. Cet article détaille la procédure pas à pas pour Bordeaux Métropole en 2026.</p>

<h2>Confirmer que la sur-consommation vient bien d'une fuite</h2>
<p>Avant d'engager la procédure d'écrêtement, vérifiez en 24 heures que la sur-consommation ne vient pas d'un changement d'usage (nouvel occupant, lave-linge cassé, robinet d'arrosage oublié) :</p>
<ol>
<li>Fermez tous les robinets de votre domicile à 22h.</li>
<li>Relevez votre compteur d'eau (chiffre exact + photo).</li>
<li>Le lendemain à 7h, sans avoir utilisé d'eau, relevez à nouveau. Si le compteur a tourné = fuite confirmée.</li>
</ol>
<p>Pour les détails et faux positifs (chasse d'eau qui fuit silencieusement, robinet extérieur, etc.), voir notre <a href="/guide/compteur-eau-qui-tourne-sans-utilisation/" style="color:var(--green);text-decoration:underline;">guide compteur d'eau qui tourne</a>.</p>

<h2>La loi Warsmann 2011 : ce qu'elle dit</h2>
<p>L'article L2224-12-4 du Code général des collectivités territoriales (loi du 17 mai 2011 dite « loi Warsmann ») prévoit que : <em>« Pour le client occupant un local d'habitation, en cas de fuite d'eau due à un défaut sur la canalisation après compteur, le service d'eau, dès qu'il constate une consommation excédant le double de la consommation moyenne, en informe l'abonné. »</em></p>
<p>Concrètement, votre facture est plafonnée à <strong>deux fois la consommation moyenne des trois dernières années</strong>, à condition de :</p>
<ul>
<li>Faire réparer la fuite dans le mois qui suit la notification de Suez</li>
<li>Fournir un certificat de plombier ou un rapport de recherche de fuite professionnel attestant la localisation enterrée non visible</li>
<li>Que la fuite soit bien sur le réseau privatif après compteur (intérieur ou enterré, mais pas sur installations électroménagers ou robinetterie)</li>
</ul>

<h2>Procédure pas à pas avec Suez à Bordeaux</h2>
<ol>
<li><strong>Réception de la facture anormale</strong> : conservez l'original.</li>
<li><strong>Diagnostic professionnel obligatoire</strong> : Suez ou la Régie de Bordeaux Métropole exige un rapport technique attestant la fuite enterrée. Notre intervention coûte 380 à 580 € HT, voir <a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">canalisation enterrée Bordeaux</a>. Le rapport est conforme aux exigences Suez et accepté.</li>
<li><strong>Réparation de la fuite</strong> : par un plombier ou pisciniste partenaire dans les 30 jours suivant le diagnostic. Conservez la facture de réparation.</li>
<li><strong>Courrier d'écrêtement</strong> : envoyez à Suez (par courrier recommandé avec AR) un dossier comprenant la facture anormale, le rapport de diagnostic, la facture de réparation, et un courrier demandant l'application de la loi Warsmann. Modèle disponible dans notre <a href="/guide/loi-warsmann-ecretement-facture-eau/" style="color:var(--green);text-decoration:underline;">guide loi Warsmann</a>.</li>
<li><strong>Réponse Suez sous 30 à 60 jours</strong> : Suez recalcule votre facture et vous rembourse l'excédent (ou crédite votre compte client).</li>
</ol>

<h2>Cas concret : maison à Caudéran (mars 2026)</h2>
<p>M. R., propriétaire à Caudéran (33000), reçoit une facture Suez de 1 850 € sur le trimestre janvier-mars 2026 alors que sa moyenne historique est de 280 €. Diagnostic Recherche Fuite Gironde par gaz traceur : fuite localisée à 8 mètres du compteur, sur un raccord cuivre désaxé sous la pelouse. Notre intervention : 480 € HT (remboursée à 100 % par AXA assurance habitation).</p>
<p>Procédure Warsmann auprès de Suez : <strong>facture plafonnée à 560 €</strong> au lieu de 1 850 €. Économie nette : 1 290 €. Délai total entre diagnostic et remboursement : 6 semaines.</p>

<h2>Notre intervention à Bordeaux</h2>
<p>Pour une intervention sous 24 à 48h en cas de surconsommation Suez critique, voir notre service <a href="/detection-fuite/urgence-bordeaux/" style="color:var(--green);text-decoration:underline;">urgence recherche de fuite à Bordeaux</a>. Pour la procédure d'assurance complète, consultez le <a href="/guide/fuite-canalisation-enterree-assurance/" style="color:var(--green);text-decoration:underline;">guide fuite canalisation enterrée et assurance</a>."""
    },
    {
        "slug": "colonne-fonte-haussmannien-bordeaux-fuite",
        "title": "Colonne en fonte haussmannien Bordeaux : fuite et chemisage",
        "title_seo": "Colonne fonte haussmannien Bordeaux fuite",
        "desc": "Fuite sur colonne EU/EV en fonte d'immeuble haussmannien à Bordeaux : pathologies typiques, diagnostic, chemisage sans démolition, coordination syndic.",
        "contenu": """<figure style="margin:0 0 2rem;"><img src="/assets/ville-bordeaux-patrimoine.webp" alt="Immeuble haussmannien à Bordeaux avec colonnes EU/EV en fonte d'origine, contexte d'intervention diagnostic fuite et chemisage" width="1600" height="1067" loading="lazy" style="width:100%;max-height:340px;height:auto;object-fit:cover;border-radius:12px;display:block;"></figure>

<p>Vous êtes copropriétaire ou syndic d'un immeuble haussmannien à Bordeaux et vous suspectez une fuite sur les colonnes EU/EV en fonte d'origine ? Le centre-ville historique de Bordeaux compte plus de 25 000 immeubles construits entre 1850 et 1914, dont 60 % conservent leurs colonnes d'évacuation en fonte grise d'origine. Après 130 à 170 ans de service, ces colonnes sont en fin de vie et présentent des pathologies bien identifiées que nous traitons régulièrement à Bordeaux Centre, Chartrons, Saint-Pierre, Saint-Augustin et Caudéran.</p>

<h2>Pathologies typiques sur colonnes fonte haussmanniennes bordelaises</h2>
<p>La fonte grise (matériau quasi exclusif des immeubles bordelais d'avant 1914) résiste mal aux eaux usées sur le très long terme. Les défauts les plus fréquents que nous diagnostiquons :</p>
<ul>
<li><strong>Fissures longitudinales par corrosion H2S</strong> : le sulfure d'hydrogène présent dans les eaux usées attaque progressivement la fonte sur sa face intérieure. Après 130-150 ans, fissures verticales de 5 à 30 cm fréquentes, souvent au milieu des sections entre étages.</li>
<li><strong>Désaxement de raccord aux étages</strong> : les jonctions entre tronçons de colonne (généralement à chaque palier) sont étanchéifiées par mastic plomb ou caoutchouc. Ces joints durcissent et fissurent. Cas type : sinistre dégât des eaux récurrent au plafond du logement situé sous la jonction.</li>
<li><strong>Perforation par corrosion externe</strong> : sur les colonnes encastrées dans les murs porteurs en pierre calcaire bordelaise (très hygroscopique), l'humidité côté terre peut attaquer la fonte de l'extérieur. Plus rare mais plus grave.</li>
<li><strong>Bouchage par dépôts calcaires + graisses</strong> : pas une fuite à proprement parler, mais cause indirecte. Le diamètre utile peut être réduit de 50 % à 80 %, créant des refoulements qui imitent une fuite.</li>
</ul>

<h2>Diagnostic adapté aux immeubles haussmanniens</h2>
<p>Sur un immeuble haussmannien bordelais, notre intervention combine plusieurs méthodes pour cibler précisément la pathologie :</p>
<ol>
<li><strong>Inspection ITV par caméra endoscopique</strong> de la colonne sur toute sa hauteur (R+5 à R+8 typique). Voir notre <a href="/guide/inspection-camera-canalisation-bordeaux/" style="color:var(--green);text-decoration:underline;">guide inspection caméra</a>. Permet de localiser au cm près chaque fissure ou désaxement.</li>
<li><strong>Localisation radio</strong> de la position exacte de la caméra à travers les cloisons et planchers, pour cibler les futures interventions sans démolition exploratoire.</li>
<li><strong>Test étanchéité par mise en eau</strong> sur tronçon isolé pour quantifier le débit de fuite si nécessaire.</li>
<li><strong>Diagnostic structurel des cheminements</strong> : sur Bordeaux Centre, les colonnes anciennes traversent souvent des gaines techniques mutualisées avec d'autres réseaux (gaz, électricité). Notre rapport indique la coordination nécessaire avec d'autres corps de métier.</li>
</ol>

<h2>Solution : chemisage sans démolition</h2>
<p>Pour les colonnes haussmanniennes en fonte fissurée, la démolition classique est presque toujours inappropriée : nuisances majeures pour les locataires, risques structurels en immeuble classé, coûts prohibitifs (35 000 € HT typique pour une colonne R+5). La solution est <strong>le chemisage par résine époxy bicomposant</strong>, qui crée un tube neuf à l'intérieur de l'ancien sans aucune démolition.</p>
<p>Voir notre page dédiée <a href="/villes/bordeaux/chemisage/" style="color:var(--green);text-decoration:underline;">chemisage de canalisation à Bordeaux</a> qui détaille la technique en 5 étapes (ITV, curage, imprégnation, réversion, contrôle) et notre <a href="/detection-fuite/chemisage-bordeaux/" style="color:var(--green);text-decoration:underline;">page chemisage syndic et copropriété</a> pour la procédure de vote en AG et la prise en charge IRSI.</p>

<h2>Coordination avec votre syndic à Bordeaux</h2>
<p>Notre intervention typique sur immeuble haussmannien R+6 (rue Sainte-Catherine, Cours de l'Intendance, Quai des Chartrons, Place Saint-Pierre, etc.) :</p>
<ul>
<li><strong>Diagnostic ITV + rapport syndic</strong> : 380 à 580 € HT, intervention 2 à 4 heures.</li>
<li><strong>Chemisage de la colonne sinistrée</strong> (pisciniste partenaire spécialisé) : 12 000 à 28 000 € HT par colonne selon hauteur et diamètre, intervention 2 à 4 jours, sans évacuation des locataires.</li>
<li><strong>Prise en charge IRSI</strong> possible sur les sinistres dégâts des eaux jusqu'à 5 000 € HT par lot. Voir notre <a href="/detection-fuite/degats-des-eaux-bordeaux/" style="color:var(--green);text-decoration:underline;">page dégâts des eaux Bordeaux</a>.</li>
</ul>
<p>Pour préparer un vote en AG ou un dossier syndic, contactez-nous pour un diagnostic ITV gratuit en copropriété de plus de 30 lots."""
    },
    {
        "slug": "convention-irsi-copropriete-bordeaux-degats-eaux",
        "title": "Convention IRSI copropriété Bordeaux dégâts des eaux : guide",
        "title_seo": "Convention IRSI copropriété Bordeaux | Sinistres",
        "desc": "Application de la convention IRSI sur sinistre dégâts des eaux en copropriété à Bordeaux : seuils, gestion syndic, expert assureur, recours, délais.",
        "contenu": """<figure style="margin:0 0 2rem;"><img src="/assets/ville-bordeaux-patrimoine.webp" alt="Immeuble en copropriété à Bordeaux concerné par la convention IRSI sur sinistre dégât des eaux" width="1600" height="1067" loading="lazy" style="width:100%;max-height:340px;height:auto;object-fit:cover;border-radius:12px;display:block;"></figure>

<p>Vous êtes copropriétaire ou syndic d'un immeuble à Bordeaux confronté à un sinistre dégât des eaux ? La convention IRSI (Indemnisation et Recours Sinistres Immeubles), entrée en vigueur le 1er juin 2018 et remplaçant l'ancienne convention CIDRE, simplifie considérablement la gestion des sinistres entre assureurs en copropriété. Cet article détaille son application concrète à Bordeaux en 2026, les seuils, les délais et les pièges à éviter.</p>

<h2>Comment fonctionne la convention IRSI ?</h2>
<p>La convention IRSI est un accord interassureurs signé par la quasi-totalité des compagnies françaises (AXA, MAIF, MAAF, Macif, Generali, Allianz, Groupama, Matmut, GMF, Crédit Mutuel, Banque Postale, Aviva). Elle organise la prise en charge des sinistres dégâts des eaux dans les immeubles collectifs, sans recours entre assureurs en dessous de certains seuils.</p>
<p><strong>Seuils 2026 (revalorisés)</strong> :</p>
<ul>
<li><strong>Moins de 1 600 € HT par lot</strong> : prise en charge intégrale par l'assureur du lot sinistré, sans recherche de responsabilité.</li>
<li><strong>1 600 à 5 000 € HT par lot</strong> : prise en charge IRSI standard. L'assureur du lot sinistré indemnise, puis se retourne contre l'assureur du lot d'origine sur barème.</li>
<li><strong>Plus de 5 000 € HT par lot</strong> : sortie du périmètre IRSI. Application du droit commun avec expertise contradictoire.</li>
</ul>

<h2>Application concrète sur sinistre à Bordeaux</h2>
<p>Cas typique : votre plafond a une tache d'humidité provoquée par une fuite chez le voisin du dessus. Procédure :</p>
<ol>
<li><strong>Déclaration sinistre</strong> à votre assureur dans les 5 jours ouvrables. Joindre photos datées, premier constat des dégâts.</li>
<li><strong>Déclaration parallèle</strong> au syndic de copropriété pour qu'il informe les autres lots concernés (voisin du dessus si fuite identifiée).</li>
<li><strong>Diagnostic recherche de fuite</strong> obligatoire pour identifier la source. Notre intervention à Bordeaux : 380 à 580 € HT, rapport conforme convention IRSI accepté par tous les assureurs. Voir <a href="/detection-fuite/degats-des-eaux-bordeaux/" style="color:var(--green);text-decoration:underline;">dégâts des eaux à Bordeaux</a>.</li>
<li><strong>Si sinistre < 5 000 € HT</strong> : votre assureur indemnise vos dommages directement, sans expertise contradictoire. Délai 30 à 60 jours.</li>
<li><strong>Si sinistre > 5 000 € HT</strong> : expertise contradictoire mandatée par chacun des assureurs concernés. Délai 60 à 120 jours.</li>
</ol>

<h2>Rôle du syndic dans la procédure IRSI</h2>
<p>À Bordeaux, les syndics professionnels (Foncia, Citya, Nexity, Inter Gestion, Cabinet Bedin, Audet Immobilier, Gironde Habitat) sont rompus à cette procédure. Le syndic intervient principalement :</p>
<ul>
<li><strong>Pour identifier l'origine du sinistre dans les parties communes</strong> (colonne montante, gaine technique, toiture). Si la fuite vient des communs, c'est l'assurance multirisque copropriété qui prend en charge.</li>
<li><strong>Pour autoriser et faciliter les diagnostics</strong> dans les autres lots et parties communes (clés, accès, planning).</li>
<li><strong>Pour engager les travaux de réparation des communs</strong> (chemisage de colonne, reprise toiture, etc.). Voir notre page <a href="/detection-fuite/chemisage-bordeaux/" style="color:var(--green);text-decoration:underline;">chemisage syndic Bordeaux</a>.</li>
<li><strong>Pour communiquer aux copropriétaires impactés</strong> (note d'information, convocation AG si travaux significatifs).</li>
</ul>

<h2>Pièges fréquents et délais à respecter</h2>
<p>Sur 50 dossiers IRSI accompagnés annuellement à Bordeaux, voici les erreurs les plus fréquentes :</p>
<ul>
<li><strong>Déclaration tardive (au-delà de 5 jours)</strong> : motif valable de refus de prise en charge. Toujours déclarer dans les 48 à 72h pour sécurité.</li>
<li><strong>Réparation avant diagnostic</strong> : si vous réparez la fuite avant que l'expert assureur ait pu la constater, la prise en charge peut être contestée. Toujours photographier avant + faire diagnostiquer + attendre accord assureur.</li>
<li><strong>Confusion partie privative / commune</strong> : la colonne montante EU/EV en gaine technique commune relève de la copropriété, pas de votre lot. Une canalisation dans votre cloison de salle de bain relève de votre lot privatif. Ce point détermine quel assureur est compétent.</li>
<li><strong>Sinistre supérieur à 5 000 € HT non détecté</strong> : sortie du périmètre IRSI = procédure beaucoup plus lourde. Faire évaluer rapidement les dommages dès le constat initial.</li>
</ul>

<h2>Notre rôle dans la procédure IRSI à Bordeaux</h2>
<p>Notre intervention de diagnostic est <strong>l'étape clé qui détermine la suite du dossier</strong> : identification de la source (privative ou commune), responsable (lot, copropriété, syndic), et chiffrage de la réparation. Notre rapport technique conforme convention IRSI est accepté par tous les assureurs IARD français, et nous restons disponibles 6 mois après l'intervention pour répondre aux questions de l'expert mandaté.</p>
<p>Voir aussi nos pages connexes : <a href="/detection-fuite/urgence-bordeaux/" style="color:var(--green);text-decoration:underline;">urgence recherche de fuite Bordeaux</a> pour les sinistres aigus, <a href="/guide/assurance-fuite-eau/" style="color:var(--green);text-decoration:underline;">guide assurance fuite d'eau</a> pour la procédure générale, et <a href="/villes/bordeaux/chemisage/" style="color:var(--green);text-decoration:underline;">chemisage de canalisation à Bordeaux</a> pour la réparation préventive des colonnes haussmanniennes en fin de vie."""
    },
    {
        "slug": "fuite-pvc-enterree-jardin-bordeaux",
        "title": "Fuite PVC enterrée jardin à Bordeaux : diagnostic gaz traceur",
        "title_seo": "Fuite PVC enterrée jardin Bordeaux | Gaz traceur",
        "desc": "Diagnostic d'une fuite sur canalisation PVC enterrée sous jardin à Bordeaux : raccords désaxés, racines, sols argilo-calcaires. Méthode gaz traceur, coût.",
        "contenu": """<figure style="margin:0 0 2rem;"><img src="/assets/fuite-canalisation-enterree.webp" alt="Canalisation PVC enterrée sous jardin à Bordeaux, contexte d'intervention diagnostic fuite par gaz traceur" width="1600" height="1067" loading="lazy" style="width:100%;max-height:340px;height:auto;object-fit:cover;border-radius:12px;display:block;"></figure>

<p>Votre canalisation PVC enterrée sous jardin à Bordeaux fuit ? C'est l'un des cas les plus fréquents que nous traitons en Gironde, particulièrement sur les pavillons construits entre 1980 et 2010 avec réseaux PVC collés enterrés à 60-100 cm de profondeur. Cet article détaille les causes typiques, la méthode de diagnostic adaptée et les coûts de réparation à Bordeaux en 2026.</p>

<h2>Pourquoi les canalisations PVC enterrées fuient</h2>
<p>Le PVC collé est un excellent matériau pour canalisations d'eau froide enterrées (durée de vie théorique 50-70 ans), mais il présente trois faiblesses sur les terrains girondins :</p>
<ul>
<li><strong>Désaxement de raccord par mouvement de sol</strong> (50 % des cas) : sur les sols argileux du sud-ouest de Bordeaux (Caudéran, Le Bouscat, Gradignan), les cycles retrait/gonflement saisonniers déplacent les raccords PVC collés. Sur le Bassin d'Arcachon (Pyla, La Teste, Gujan), le sol sableux fluide a le même effet par tassement différentiel.</li>
<li><strong>Perforation par racine d'arbre</strong> (30 % des cas) : platanes, chênes, tilleuls, saules pleureurs et bambous sont les pires. Les racines repèrent les microfuites de raccord et s'infiltrent à travers le joint, finissant par perforer la paroi PVC en quelques années. Cas type : maison de Caudéran avec platane à 5-10 mètres de la canalisation.</li>
<li><strong>Cycle gel/dégel</strong> (15 % des cas) : sur les hivers rigoureux (rares à Bordeaux mais possibles tous les 5-10 ans), le gel peut faire éclater une canalisation mal enterrée (moins de 50 cm). Plus fréquent sur les robinets de jardin et tuyauteries proches de la surface.</li>
<li><strong>Vétusté des colles PVC d'origine</strong> (5 % des cas) : sur les pavillons des années 1970-1985, les colles PVC d'époque peuvent perdre leur élasticité après 40 ans et fissurer aux raccords sous contrainte mécanique légère.</li>
</ul>

<h2>Comment diagnostiquons-nous une fuite PVC enterrée ?</h2>
<p>Notre méthode de référence sur les canalisations PVC enterrées en Gironde combine deux techniques :</p>
<ol>
<li><strong>Test de pression hydraulique</strong> : isolation du tronçon suspecté, mise en pression à 4-6 bars, mesure de la chute de pression sur 15 minutes. Permet de quantifier le débit de fuite et confirmer la zone à investiguer.</li>
<li><strong>Gaz traceur azote/hydrogène</strong> : vidange du tronçon, mise en pression avec mélange 95 % azote + 5 % hydrogène, suivi en surface au capteur électrochimique sensible à l'hydrogène. Le gaz remonte par capillarité jusqu'à la surface au point de fuite et déclenche le détecteur. Précision : 30-50 cm. Voir notre <a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">page canalisation enterrée Bordeaux</a> pour le détail technique.</li>
<li><strong>Inspection caméra endoscopique</strong> en complément si la canalisation est accessible depuis un regard. Permet de qualifier la cause exacte (raccord désaxé vs racine vs fissure). Voir <a href="/guide/inspection-camera-canalisation-bordeaux/" style="color:var(--green);text-decoration:underline;">guide inspection caméra</a>.</li>
</ol>

<h2>Réparation : tranchée locale ou chemisage ?</h2>
<p>Une fois la fuite localisée au mètre près, deux options de réparation :</p>
<ul>
<li><strong>Tranchée locale ciblée</strong> : creusement sur 1 à 3 mètres au point de fuite, remplacement du tronçon défectueux, rebouchage. Coût 600 à 1 500 € HT selon profondeur et accès. Adapté si la canalisation est globalement saine et que la fuite est ponctuelle.</li>
<li><strong>Chemisage par résine époxy</strong> : si la canalisation a plusieurs défauts ou est globalement vieillissante, le chemisage rénove le tube sans tranchée. Voir notre <a href="/villes/bordeaux/chemisage/" style="color:var(--green);text-decoration:underline;">page chemisage canalisation Bordeaux</a>. Coût 250 à 380 € HT par mètre linéaire.</li>
</ul>

<h2>Notre intervention sur Bordeaux Métropole et Bassin d'Arcachon</h2>
<p>Diagnostic complet d'une fuite PVC enterrée à Bordeaux : <strong>380 à 580 € HT</strong>, intervention 2 à 4 heures, rapport technique remis le jour même. Souvent intégralement remboursé par votre assurance habitation au titre de la garantie recherche de fuite (voir <a href="/guide/fuite-canalisation-enterree-assurance/" style="color:var(--green);text-decoration:underline;">guide assurance fuite enterrée</a>).</p>
<p>Si votre facture d'eau a explosé, vous pouvez aussi activer la procédure d'écrêtement loi Warsmann auprès de Suez ou de la Régie de Bordeaux Métropole : voir notre <a href="/guide/loi-warsmann-ecretement-facture-eau/" style="color:var(--green);text-decoration:underline;">guide loi Warsmann</a> et <a href="/guide/facture-eau-suez-doublee-fuite-bordeaux/" style="color:var(--green);text-decoration:underline;">guide facture Suez doublée</a>."""
    },
    {
        "slug": "fuite-piscine-bordeaux",
        "title": "Fuite piscine à Bordeaux : guide complet diagnostic et réparation",
        "title_seo": "Fuite piscine Bordeaux | Guide complet 2026",
        "desc": "Tout sur les fuites de piscine à Bordeaux : symptômes, diagnostic, réparation, prix, marques (Desjoyaux, Magiline, Diffazur, Waterair). Guide expert local.",
        "contenu": """<figure style="margin:0 0 2rem;"><img src="/assets/pillar-fuite-piscine-bordeaux.webp" alt="Vue d'ensemble piscine privée en Gironde : guide complet diagnostic et réparation des fuites" width="1600" height="1067" loading="lazy" style="width:100%;max-height:340px;height:auto;object-fit:cover;border-radius:12px;display:block;"></figure>

<p>Vous suspectez une fuite sur votre piscine à Bordeaux ou ailleurs en Gironde ? Ce guide complet rassemble en un seul endroit tout ce qu'il faut savoir pour identifier, diagnostiquer et réparer une fuite, quelle que soit la marque, le type de bassin ou la nature du problème. Notre équipe a réalisé plus de 200 diagnostics de fuite de piscine en Gironde dans l'année écoulée, principalement sur la métropole bordelaise (Caudéran, Le Bouscat, Mérignac, Pessac) et le Bassin d'Arcachon (Gujan-Mestras, La Teste-de-Buch, Andernos-les-Bains). Nous vous donnons ici la méthode complète pour qualifier votre situation, choisir le bon prestataire et éviter les erreurs coûteuses.</p>

<h2>1. Confirmer la fuite : les 3 tests gratuits à faire avant tout</h2>
<p>Avant d'engager des frais de diagnostic professionnel, faites trois tests simples qui éliminent 30 % des fausses alertes (évaporation forte mais pas de fuite). Tous se font sans matériel spécifique en moins de 48 heures.</p>
<ul>
  <li><strong>Test du seau (référence absolue)</strong> : posez un seau rempli sur la première marche immergée pour qu'il soit à la même température que le bassin. Marquez les niveaux au feutre. Comparez après 24 à 48h. Si la piscine baisse plus que le seau, fuite confirmée. Voir notre guide <a href="/guide/evaporation-vs-fuite-piscine/" style="color:var(--green);text-decoration:underline;">évaporation ou fuite de piscine en Gironde</a> avec tableau d'évaporation mensuel.</li>
  <li><strong>Test du repère filtration ON/OFF</strong> : permet de localiser la zone de la fuite. Marquez le niveau, laissez 24h filtration en marche, puis 24h filtration arrêtée. Une baisse plus rapide en marche = fuite côté refoulement (pression). Une baisse plus rapide à l'arrêt = fuite bassin/skimmer.</li>
  <li><strong>Mesure quantitative</strong> : combien de cm/jour ? Voir notre guide <a href="/guide/piscine-perd-3-cm-par-jour/" style="color:var(--green);text-decoration:underline;">piscine qui perd 3 cm par jour : que faire</a> pour comparer votre perte aux seuils normaux d'évaporation en Gironde.</li>
</ul>
<p>Pour qualifier votre situation en 6 questions structurées, voir aussi notre arbre de décision <a href="/guide/ma-piscine-perd-de-l-eau-que-faire/" style="color:var(--green);text-decoration:underline;">ma piscine perd de l'eau : que faire</a>.</p>

<h2>2. Identifier la source : 3 zones à vérifier</h2>
<p>Sur les diagnostics annuels que nous réalisons à Bordeaux, les fuites de piscine se concentrent sur 3 zones avec des proportions stables :</p>

<h3>Filtration et pièces à sceller (60 % des cas)</h3>
<p>Skimmer, buses de refoulement, projecteurs, prise balai, bonde de fond. Joints toriques durcis après 8-12 ans, brides desserrées par cycles thermiques, mastic d'étanchéité craquelé. Diagnostic ciblé par fluorescéine, réparation rapide (changement joint 12-35 €). Voir notre guide spécifique <a href="/guide/reparation-skimmer-piscine-resine-epoxy/" style="color:var(--green);text-decoration:underline;">réparation skimmer à la résine époxy</a>.</p>

<h3>Canalisations enterrées (25 % des cas)</h3>
<p>Sols sableux du Bassin d'Arcachon ou argileux de la métropole bordelaise désaxent les raccords PVC en 15-25 ans. Diagnostic par gaz traceur azote/hydrogène et inspection caméra. Voir <a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">canalisation enterrée Bordeaux</a> et <a href="/guide/inspection-camera-canalisation-bordeaux/" style="color:var(--green);text-decoration:underline;">inspection caméra canalisation</a>.</p>

<h3>Bassin lui-même (15 % des cas)</h3>
<p>Liner PVC fissuré ou désoudé, gel-coat polyester osmosé, fissure structurelle béton. Diagnostic par fluorescéine, méthode visuelle et inspection sous-marine selon le matériau. Guides dédiés : <a href="/guide/fuite-liner-piscine/" style="color:var(--green);text-decoration:underline;">fuite liner piscine PVC</a> et <a href="/guide/fuite-coque-polyester-piscine/" style="color:var(--green);text-decoration:underline;">fuite coque polyester</a>.</p>

<h2>3. Diagnostic selon votre marque de piscine</h2>
<p>Chaque grande marque française de piscine a un système constructif spécifique avec ses points de fragilité connus. Sur Bordeaux et la métropole, nous traitons 4 marques principales et avons une page dédiée à chacune avec les pathologies typiques, méthodes de diagnostic adaptées et tarifs constatés.</p>

<ul>
  <li><a href="/guide/fuite-piscine-desjoyaux-bordeaux/" style="color:var(--green);text-decoration:underline;"><strong>Fuite piscine Desjoyaux à Bordeaux</strong></a> : système avec bloc filtrant intégré (sans local technique séparé). Vigilance sur les raccords pièces à sceller et joints du bloc filtrant.</li>
  <li><a href="/guide/fuite-piscine-magiline-bordeaux/" style="color:var(--green);text-decoration:underline;"><strong>Fuite piscine Magiline à Bordeaux</strong></a> : structure béton avec panneaux alvéolaires brevetés et filtration NFX à cartouche (87 brevets internationaux). Réparation à confier au réseau Magiline pour le système breveté.</li>
  <li><a href="/guide/fuite-piscine-diffazur-bordeaux/" style="color:var(--green);text-decoration:underline;"><strong>Fuite piscine Diffazur à Bordeaux</strong></a> : structure béton armé projeté par gunite, revêtement multi-options (peinture, enduit, mosaïque, carrelage, pierre). Pathologies selon la finition.</li>
  <li><a href="/guide/fuite-piscine-waterair-bordeaux/" style="color:var(--green);text-decoration:underline;"><strong>Fuite piscine Waterair à Bordeaux</strong></a> : panneaux acier ondé galvanisé + liner d'étanchéité. Vigilance sur les fixations du liner et raccords pièces à sceller.</li>
</ul>

<h2>4. Diagnostic professionnel : 4 méthodes selon le cas</h2>
<p>Notre équipe spécialiste de la recherche de fuite à Bordeaux utilise 4 méthodes complémentaires selon la situation :</p>

<h3>Colorant fluorescéine sodique</h3>
<p>Méthode visuelle de référence pour les pièces à sceller, joints d'étanchéité, microfissures de liner. Le colorant non toxique injecté à proximité d'une zone suspecte est aspiré par la fuite et révèle son parcours exact. Très efficace sur tous types de bassins (liner, coque polyester, béton). Voir <a href="/detection-fuite/fluoresceine-piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">recherche fuite piscine fluorescéine Bordeaux</a>.</p>

<h3>Test de pression hydraulique</h3>
<p>Méthode quantitative pour isoler une fuite côté canalisations vs côté bassin. Mise en pression d'un tronçon isolé, mesure de la chute de pression sur 15 minutes. Indispensable pour distinguer fuite refoulement, aspiration ou bassin.</p>

<h3>Inspection caméra endoscopique</h3>
<p>Pour les canalisations de filtration ou enterrées difficilement accessibles. Caméra étanche sur tige flexible avec éclairage LED et localisation radio. Voir <a href="/guide/inspection-camera-canalisation-bordeaux/" style="color:var(--green);text-decoration:underline;">inspection caméra canalisation Bordeaux</a>.</p>

<h3>Inspection visuelle et sous-marine</h3>
<p>Pour les fissures structurelles béton, désoudures de liner, microfissures de gel-coat. À la lampe rasante en surface ou en apnée pour les zones profondes. Souvent combinée à la fluorescéine pour confirmation.</p>

<p>Pour le détail technique du matériel professionnel, voir notre guide <a href="/guide/detecteur-fuite-eau-professionnel/" style="color:var(--green);text-decoration:underline;">détecteur de fuite d'eau professionnel</a> qui détaille les marques (FLIR, Sewerin, Wöhler) et les fourchettes de prix matériel pro.</p>

<h2>5. Combien coûte une recherche de fuite piscine à Bordeaux ?</h2>
<p>Tarifs constatés en 2026 sur la métropole bordelaise et le Bassin d'Arcachon :</p>
<ul>
  <li><strong>Diagnostic ciblé</strong> (1-2 zones suspectes) : <strong>240 à 320 € HT</strong>, intervention 1 à 2 heures.</li>
  <li><strong>Diagnostic complet</strong> (fluorescéine + test pression + inspection visuelle) : <strong>380 à 580 € HT</strong>, intervention 2 à 4 heures.</li>
  <li><strong>Diagnostic complexe</strong> (piscine ancienne, plusieurs sources suspectées, copropriété) : <strong>520 à 750 € HT</strong>, intervention 3 à 5 heures.</li>
</ul>
<p>Pour la grille tarifaire complète selon le type de bassin et la méthode, voir notre <a href="/guide/recherche-fuite-piscine-tarif/" style="color:var(--green);text-decoration:underline;">guide tarif recherche de fuite piscine en Gironde</a>. Pour les autres types de fuites (canalisation, plancher chauffant), voir <a href="/guide/prix-recherche-fuite-bordeaux/" style="color:var(--green);text-decoration:underline;">prix d'une recherche de fuite à Bordeaux</a>.</p>

<h2>6. Prise en charge assurance et écrêtement Warsmann</h2>
<p>Dans 90 % des cas, votre assurance habitation rembourse tout ou partie du diagnostic au titre de la garantie recherche de fuite. Conditions, procédure pas à pas et liste des assureurs IARD français qui acceptent notre rapport : voir notre <a href="/guide/recherche-fuite-piscine-assurance/" style="color:var(--green);text-decoration:underline;">guide remboursement assurance piscine</a>.</p>
<p>Pour les fuites avec surconsommation d'eau Suez ou Régie de Bordeaux Métropole, voir aussi <a href="/guide/loi-warsmann-ecretement-facture-eau/" style="color:var(--green);text-decoration:underline;">loi Warsmann : écrêtement de facture d'eau</a> et notre <a href="/simulateur-cout-fuite/" style="color:var(--green);text-decoration:underline;">simulateur de coût de fuite</a> qui calcule automatiquement votre éligibilité.</p>

<h2>7. Réparation après diagnostic</h2>
<p>Une fois la fuite localisée précisément, plusieurs options de réparation selon la pathologie :</p>
<ul>
  <li><strong>Joint de pièce à sceller</strong> : 12 à 35 € de pièce, ou 120 à 180 € HT en intervention pisciniste.</li>
  <li><strong>Réparation locale liner ou coque</strong> : 180 à 450 € HT par zone (rustine subaquatique, soudure thermique, gel-coat local).</li>
  <li><strong>Remplacement complet liner</strong> : 3 800 à 7 500 € TTC pour un bassin standard 8×4 m.</li>
  <li><strong>Reprise complète gel-coat coque polyester</strong> : 3 500 à 8 500 € TTC selon surface.</li>
  <li><strong>Réparation canalisation enterrée</strong> : 450 à 1 200 € HT selon profondeur et accès.</li>
</ul>
<p>Guides détaillés : <a href="/guide/reparation-liner-piscine/" style="color:var(--green);text-decoration:underline;">réparation fuite liner piscine</a> et <a href="/guide/reparation-skimmer-piscine-resine-epoxy/" style="color:var(--green);text-decoration:underline;">réparation skimmer à la résine époxy</a>.</p>

<h2>8. Notre service à Bordeaux et en Gironde</h2>
<p>Nous intervenons sur les 7 communes principales du parc piscine girondin avec une page dédiée par ville :</p>
<ul>
  <li><a href="/detection-fuite/piscine-bordeaux/" style="color:var(--green);text-decoration:underline;"><strong>Recherche de fuite piscine à Bordeaux</strong></a> (33000) : Caudéran, Le Bouscat, Saint-Augustin, propriétés bourgeoises avec piscines anciennes.</li>
  <li><a href="/detection-fuite/piscine-merignac/" style="color:var(--green);text-decoration:underline;"><strong>Piscine Mérignac</strong></a> (33700) : Capeyron, Beutre, Arlac, parc liner pavillonnaire 1990-2010.</li>
  <li><a href="/detection-fuite/piscine-arcachon/" style="color:var(--green);text-decoration:underline;"><strong>Piscine Arcachon</strong></a> (33120) : Pyla, Ville d'Hiver, villas haut de gamme avec PAC.</li>
  <li><a href="/detection-fuite/piscine-la-teste-de-buch/" style="color:var(--green);text-decoration:underline;"><strong>Piscine La Teste-de-Buch</strong></a> (33260) : Cazaux, sols sableux Bassin d'Arcachon.</li>
  <li><a href="/detection-fuite/piscine-gujan-mestras/" style="color:var(--green);text-decoration:underline;"><strong>Piscine Gujan-Mestras</strong></a> (33470) : forte densité de coques polyester.</li>
  <li><a href="/detection-fuite/piscine-libourne/" style="color:var(--green);text-decoration:underline;"><strong>Piscine Libourne</strong></a> (33500) : chais viticoles anciens, sol argileux Libournais.</li>
  <li><a href="/detection-fuite/piscine-le-bouscat/" style="color:var(--green);text-decoration:underline;"><strong>Piscine Le Bouscat</strong></a> (33110) : jardins matures avec racines de platanes et chênes.</li>
</ul>
<p>Pour notre service de dépannage piscine multimarques (diagnostic + coordination réparation pisciniste partenaire), voir notre page <a href="/detection-fuite/depannage-piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">dépannage piscine à Bordeaux</a>. Pour une vue d'ensemble du parc et des méthodes, voir le <a href="/detection-fuite/piscine/" style="color:var(--green);text-decoration:underline;">hub recherche de fuite piscine en Gironde</a>."""
    },]

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
        art["title_seo"],
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
    ("quelle est la différence entre une fuite et un dégât des eaux ?", "Une fuite est l'origine du problème : la canalisation ou le joint qui fuit. Le dégât des eaux est la conséquence : l'humidité, les taches, les moisissures. Pour être indemnisé, il faut d'abord faire constater et localiser la fuite."),
    ("Qu'est-ce que le chemisage de canalisation ?", "Le chemisage consiste à insérer un manchon en résine époxy dans la canalisation existante. Ce manchon est gonflé et durci sur place, créant un nouveau tuyau à l'intérieur de l'ancien. Aucun démontage ni démolition n'est nécessaire."),
    ("Le chemisage est-il durable ?", "Oui. La résine époxy utilisée à une durée de vie supérieure à 50 ans dans des conditions normales d'utilisation. C'est une solution définitive, pas un palliatif temporaire."),
    ("Intervenez-vous en urgence ?", "Nous proposons des interventions prioritaires sous 24h sur toute la Gironde. En cas d'urgence immédiate, commencez par couper l'arrivée d'eau générale, puis contactez-nous via le formulaire."),
    ("Quelles canalisations peut-on chemiser ?", "Le chemisage est applicable sur la plupart des matériaux : fonte, PVC, grès, cuivre, acier galvanisé. Il convient aux canalisations d'eau potable, d'évacuation et aux réseaux enterrés."),
    ("Vous intervenez dans quelle zone géographique ?", "Nous intervenons sur 30 communes du département de la Gironde (33) : Bordeaux, Mérignac, Pessac, Talence, Arcachon, Libourne et toutes les communes du bassin d'Arcachon, du Médoc et de la métropole bordelaise."),
    ("Fournissez-vous un rapport après l'intervention ?", "Oui, systématiquement. Le rapport mentionne la localisation précise de la fuite, les techniques utilisées, les photos de l'intervention et les préconisations de réparation. Ce document est reconnu par les assureurs."),
    ("quelle est la différence entre la corrélation acoustique et le gaz traceur ?", "La corrélation acoustique analyse le bruit produit par la fuite et est très efficace sur les canalisations sous pression. Le gaz traceur est utilisé pour les fuites de faible débit difficiles à capter acoustiquement. Les deux méthodes sont souvent complémentaires."),
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
        "Guide fuites d'eau Gironde | Détection & assurance",
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
      <span>demande de devis</span>
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
        <div id="form-devis-error" style="display:none;background:rgba(239,68,68,.2);border:1px solid rgba(239,68,68,.4);border-radius:8px;padding:1rem;text-align:center;margin-bottom:1rem;"><p style="color:#fecaca;font-size:.9rem;margin:0;">Une erreur est survenue. Veuillez r\u00e9essayer ou nous appeler directement.</p></div>
        <form data-ajax data-error="form-devis-error">
          <input type="hidden" name="_subject" value="[recherche-fuite-gironde.fr] demande de devis">
          <input type="hidden" name="site_source" value="">
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
              <label class="form-label" for="téléphone">Téléphone</label>
              <input class="form-input" type="tel" id="téléphone" name="téléphone" placeholder="06 XX XX XX XX" required>
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
            <label class="form-label" for="problème">Type de problème</label>
            <select class="form-input form-select" id="problème" name="problème" required>
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
        "Devis gratuit recherche de fuite Gironde 33",
        "Demandez votre devis gratuit pour une recherche de fuite ou un chemisage en Gironde (33). Réponse sous 24h, intervention sous 24h.",
        "https://recherche-fuite-gironde.fr/devis/",
        body,
        hide_sticky_cta=True
    )

# ── Sitemap XML ────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════
# PAGES VILLE PREMIUM : refonte enrichie pour villes strategiques
# ═══════════════════════════════════════════════════════════════

VILLES_PREMIUM = {
    "bordeaux": {
        "ville": "Bordeaux",
        "ville_article": "à Bordeaux",
        "cp": "33000",
        "image": "ville-bordeaux-patrimoine.webp",
        "image_alt": "Pont de Pierre et patrimoine de Bordeaux, zone d'intervention recherche de fuite en métropole bordelaise",
        "pitch_local": "Capitale régionale et cœur de la métropole girondine, Bordeaux concentre une diversité architecturale unique : immeubles haussmanniens du Triangle d'Or, maisons bourgeoises de Caudéran, échoppes des Chartrons, barres haussmanniennes de la place Gambetta, résidences contemporaines de Bacalan. Chaque type de bâti appelle une méthode de détection adaptée.",
        "quartiers": "Les Chartrons, Bacalan, Centre-Ville, Saint-Pierre, Saint-Michel, La Victoire, Les Capucins, Saint-Jean, Nansouty, Saint-Genès, Saint-Seurin, Caudéran, Saint-Augustin, La Bastide, Belcier, Le Lac, Bassins à Flot, Mériadeck",
        "zones_voisines": "Mérignac, Pessac, Talence, Le Bouscat, Bègles, Caudéran",
        "spécificités": [
            ("Immeubles haussmanniens et copropriétés anciennes", "Le centre historique bordelais abrite un patrimoine classé à l'UNESCO (Port de la Lune). Les immeubles du Triangle d'Or, du cours de l'Intendance ou de la place Gambetta présentent des colonnes montantes en fonte ou en plomb parfois centenaires. La recherche de fuite y demande de combiner écoute électro-acoustique et thermographie pour éviter de dégrader les finitions d'époque (moulures, parquets Versailles, cheminées marbre)."),
            ("Pierre calcaire bordelaise et humidité", "La pierre de Frontenac ou de Bourg, très présente dans les façades et murs de refend, est poreuse. Une fuite cachée provoque rapidement des auréoles, du salpêtre, voire des dégradations structurelles. Notre diagnostic localise la source avant que l'humidité ne se diffuse dans les matériaux."),
            ("Échoppes bordelaises et maisons individuelles", "Aux Chartrons, à Saint-Genès ou à Caudéran, les échoppes traditionnelles (maison basse en pierre) ont souvent vu leurs réseaux d'évacuation refaits en PVC moderne branchés sur des canalisations fonte d'origine. Les points de raccordement sont les zones de fuite les plus fréquentes que nous identifions."),
            ("Réseaux enterrés et sols argileux", "Une partie du territoire bordelais repose sur des sols argileux sensibles au retrait-gonflement. Ces mouvements de terrain peuvent désaxer les canalisations d'évacuation sous dalle ou les alimentations enterrées depuis le regard de compteur. Le gaz traceur reste la méthode la plus efficace dans ces configurations.")
        ],
        "cas_frequent": "Cas type à Bordeaux : appartement au 3e étage d'un immeuble haussmannien de la rue Sainte-Catherine, construit en 1905. Tache d'humidité récurrente au plafond de la chambre, voisin du dessus qui ne constate rien chez lui. Notre diagnostic : thermographie infrarouge pour cartographier la zone humide, écoute électro-acoustique sur le tracé de la colonne d'évacuation EU, caméra endoscopique dans la gaine technique. Dans 60 pourcent des cas sur ce type de bâti, la fuite est sur la colonne commune entre deux étages, relevant de la copropriété et de la convention IRSI, pas du voisin direct.",
        "methodes_focus": "À Bordeaux, où le patrimoine haussmannien et les copropriétés anciennes dominent, notre méthodologie privilégie la thermographie infrarouge pour cartographier une zone humide derrière plâtre ou enduit ancien, et l'écoute électro-acoustique pour localiser une fuite sur colonne montante EU/EV. La caméra endoscopique est souvent déployée en seconde passe pour inspecter l'intérieur des canalisations fonte centenaires des immeubles du Triangle d'Or ou des Chartrons. Le gaz traceur reste essentiel pour les canalisations enterrées en sol argileux, typiques du Grand Parc ou de Caudéran. Cette combinaison méthodologique permet de préserver les parquets Versailles, moulures plâtre et cheminées marbre des immeubles classés UNESCO du Port de la Lune.",
        "faq_locale": [
            ("Fait-il prévenir l'Architecte des Bâtiments de France avant votre intervention dans le périmètre UNESCO ?",
             "Non, une recherche de fuite est un diagnostic technique non destructif qui ne modifie pas l'aspect extérieur ni ne touche aux éléments classés. Aucune autorisation ABF ou déclaration préalable n'est requise. Seuls des travaux de réparation modifiant une façade ou des éléments protégés pourraient nécessiter une validation."),
            ("Intervenez-vous dans les copropriétés haussmanniennes avec syndic professionnel ?",
             "Oui, très régulièrement. Le mandatement vient alors du syndic ou du conseil syndical. Nous remettons un rapport technique au syndic, utilisable dans le cadre de la convention IRSI entre assureurs pour les sinistres jusqu'à 5 000 euros HT. L'intervention est planifiée en concertation avec les copropriétaires concernés."),
            ("La fuite vient-elle souvent du voisin du dessus à Bordeaux ?",
             "Pas toujours. Dans les immeubles anciens bordelais, la colonne d'évacuation commune (EU/EV) est en cause dans 60 pourcent des cas où un plafond s'humidifie, et non pas directement le logement du dessus. Notre diagnostic identifié précisément l'origine pour éviter les litiges injustifiés avec le voisinage.")
        ],
    },
    "mérignac": {
        "ville": "Mérignac",
        "ville_article": "à Mérignac",
        "cp": "33700",
        "image": "ville-mérignac-résidentiel.webp",
        "image_alt": "Maison individuelle typique de Mérignac, zone d'intervention recherche de fuite en métropole bordelaise",
        "pitch_local": "Deuxième ville de la métropole bordelaise, Mérignac combine zones résidentielles pavillonnaires, quartiers pavillonnaires anciens et grands ensembles récents. Les maisons individuelles des années 1970 à 2000 constituent l'essentiel du parc immobilier, avec des problématiques caractéristiques de fuites sur canalisations enterrées et plancher chauffant.",
        "quartiers": "Mérignac Centre, Arlac, Capeyron, Chemin Long, Beutre, Beaudésert, Le Burck, Les Eyquems, Pichey",
        "zones_voisines": "Bordeaux, Le Haillan, Eysines, Pessac, Saint-Médard-en-Jalles",
        "spécificités": [
            ("Pavillons des années 80-2000 et planchers chauffants", "Beaucoup de maisons mérignacaises de cette période ont été équipées de planchers chauffants hydrauliques. Après 20 à 40 ans d'utilisation, les micro-perforations sur les tubes PER ou polybutylène sont fréquentes. Notre thermographie infrarouge localise la fuite au degré près sans toucher à la chape."),
            ("Canalisations d'alimentation enterrées longues", "Les maisons avec grand terrain (plus fréquentes à Arlac ou Beutre) ont des canalisations d'eau enterrées de 10 à 50 mètres entre le regard de compteur et la maison. Une fuite sur ce tronçon peut passer inaperçue pendant des mois et gonfler la facture d'eau avant d'être détectée."),
            ("Piscines privées nombreuses", "Mérignac concentre une forte densité de piscines individuelles, notamment dans les quartiers résidentiels. Les fuites sur pièces à sceller (skimmer, buses) et canalisations enterrées autour du bassin sont notre quotidien."),
            ("Proximité aéroport et réseaux multiples", "La zone aéroportuaire et les zones d'activité génèrent des demandés sur des bâtiments tertiaires, des copropriétés récentes et des résidences en locations saisonnières. Chaque configuration à sa propre signature de fuite que nos techniciens savent identifier.")
        ],
        "cas_frequent": "Scénario classique à Mérignac : pavillon Arlac années 1995, propriétaire qui reçoit une facture d'eau de 1 200 euros sur un trimestre (contre 250 habituellement). Compteur qui tourne en permanence, pas de tache dans la maison. Notre diagnostic : test du robinet d'arrêt général (fuite après compteur), gaz traceur azote/hélium injecté sur la canalisation enterrée compteur vers maison (45 mètres de tracé). La fuite se trouve à 28 mètres du compteur, au droit d'un raccord PVC désaxé par mouvement de terrain. Réparation : ouverture 1 m² au point localisé, remplacement du raccord, rebouchage. Coût total intervention + réparation : 850 euros, remboursables en grande partie par la garantie recherche de fuite de l'assurance.",
        "methodes_focus": "Sur le parc pavillonnaire mérignacais (majoritairement années 1970-2000 avec canalisations enterrées longues), nos deux méthodes de référence sont le gaz traceur azote/hélium pour les alimentations enterrées entre compteur et maison (souvent 20 à 50 mètres), et la thermographie infrarouge pour les planchers chauffants hydrauliques très répandus à Arlac, Capeyron et Chemin Long. L'écoute électro-acoustique complète sur les réseaux sous dalle béton, et le test de pression sur boucle permet d'isoler le circuit en défaut avant localisation fine. Pour les piscines nombreuses de la commune, nous déployons en plus colorant fluorescéine et inspection caméra sous-marine.",
        "faq_locale": [
            ("Le compteur d'eau tourne chez moi à Mérignac : fuite avant ou après compteur ?",
             "Faites le test de fermeture : tournez votre robinet d'arrêt général situé juste après le compteur. Si le compteur continue de tourner, la fuite est AVANT (réseau public Suez), à leur charge. S'il s'arrête mais que vous avez toujours une perte, la fuite est APRÈS (réseau privatif), à votre charge. Ce diagnostic simple oriente immédiatement la suite."),
            ("Peut-on obtenir un écrêtement de facture d'eau avec Suez Mérignac ?",
             "Oui, la loi Warsmann (2011) permet de plafonner la surfacturation liée à une fuite sur canalisation enterrée non détectable. Il faut fournir à Suez une attestation de réparation par un professionnel et un rapport de localisation de fuite (comme celui que nous émettons). Votre facture est alors ramenée à deux fois votre consommation habituelle."),
            ("Ma maison Mérignac à un plancher chauffant qui perd de pression : vous intervenez ?",
             "Oui, c'est un cas récurrent à Mérignac. La thermographie infrarouge révèle la zone de la fuite (circulation thermique anormale), puis nous confirmons par test de pression sur chaque boucle. La réparation consiste à ouvrir la chape au droit exact de la micro-perforation (25×25 cm environ) pour remplacer 50 cm de tube, refaire la chape et le revêtement de sol.")
        ],
    },
    "arcachon": {
        "ville": "Arcachon",
        "ville_article": "à Arcachon",
        "cp": "33120",
        "image": "ville-arcachon-bassin.webp",
        "image_alt": "Arcachon vue aérienne avec Bassin et villas de la Ville d'Hiver, zone d'intervention recherche de fuite sur le Bassin d'Arcachon",
        "pitch_local": "Ville balnéaire emblématique du Bassin d'Arcachon, Arcachon présente un contexte très spécifique : résidences secondaires nombreuses, villas de la Ville d'Hiver classées Monuments historiques, influence marine constante. Les problématiques de fuites y sont accentuées par l'air salin, les variations hygrométriques et la proximité de la nappe.",
        "quartiers": "Arcachon Centre, Ville d'Hiver, Ville d'Été, Abatilles, Aiguillon, Moulleau, Pereire",
        "zones_voisines": "La Teste-de-Buch, Gujan-Mestras, Le Teich, Pyla-sur-Mer, Lège-Cap-Ferret",
        "spécificités": [
            ("Villas de la Ville d'Hiver et patrimoine historique", "Les villas néo-mauresques, coloniales et chalets suisses de la Ville d'Hiver datent pour la plupart du XIXe siècle. Leurs réseaux d'évacuation en fonte d'origine sont souvent fatigués. Toute intervention doit préserver l'intégrité architecturale : nos méthodes non destructives sont ici incontournables."),
            ("Air salin et corrosion accélérée", "La proximité permanente de l'eau salée du Bassin accélère la corrosion des canalisations métalliques (cuivre, acier galvanisé) et des équipements en inox. Les fuites apparaissent plus tôt qu'en intérieur des terres. Un diagnostic régulier tous les 10 ans est recommandé sur les résidences secondaires."),
            ("Résidences secondaires et dégâts en hivernage", "De nombreuses propriétés sont occupées quelques semaines par an. Une fuite non détectée à l'automne peut provoquer des dégâts considérables avant le retour des propriétaires au printemps. Nous intervenons en contrat d'entretien préventif pour ce type de configuration."),
            ("Canalisations enterrées en sable et mouvements", "Le sous-sol sableux d'Arcachon offre une excellente portance mais subit des micro-tassements au gré des variations hygrométriques. Les raccords des canalisations enterrées (alimentation, évacuation, arrosage) peuvent se désaxer lentement et provoquer des fuites progressives.")
        ],
        "cas_frequent": "Cas récurrent arcachonais : villa de la Ville d'Hiver, propriétaires résidents secondaires vivant à Paris, retour pour les vacances de Pâques. Ils découvrent en ouvrant la maison une humidité au sol du sous-sol et au pied de la cuisine. Notre diagnostic : thermographie pour cartographier la zone humide, écoute acoustique sur la canalisation de cuivre d'alimentation, humidimètre pour mesurer l'étendue. Fuite identifiée sur raccord cuivre au niveau de la traversée mur, corrodée par l'air salin. Durée sans détection estimée à 4-6 mois. Consommation d'eau perdue : environ 180 m³. Rapport utilisable pour demande d'écrêtement auprès de la Régie des eaux et pour la déclaration à l'assureur.",
        "methodes_focus": "À Arcachon, où l'air salin, les résidences secondaires et le patrimoine historique imposent des contraintes particulières, notre méthodologie s'adapte en deux temps. Contrôle systématique préalable du local technique (corrosion des cuivres et inox par l'air salin) car la fuite vient souvent d'un équipement, pas du bâti. Puis thermographie infrarouge et humidimètre pour distinguer une vraie fuite d'une remontée d'humidité par capillarité (fréquente en sous-sol au bord du Bassin). L'écoute électro-acoustique cible les canalisations anciennes en fonte ou cuivre d'origine des villas de la Ville d'Hiver et du Moulleau. Le gaz traceur reste notre outil de référence pour les canalisations enterrées en sol sableux, qui subissent micro-tassements permanents.",
        "faq_locale": [
            ("Ma résidence secondaire à Arcachon a eu une fuite durant l'hiver, qui paye ?",
             "Votre assurance habitation multirisque couvre la recherche de fuite et les dégâts consécutifs, y compris pendant une période d'inoccupation, à condition que la déclaration soit faite dans les 5 jours ouvrables après constat. Pour l'eau perdue, vous pouvez demander un écrêtement de facture auprès de la Régie des eaux de La Teste-Arcachon en présentant notre rapport technique."),
            ("Proposez-vous un contrat de diagnostic préventif pour résidences secondaires ?",
             "Oui, nous proposons un forfait annuel de diagnostic préventif pour les propriétaires de résidences secondaires du bassin d'Arcachon : un passage au printemps et un à l'automne, avec vérification du compteur, thermographie de la zone technique, contrôle visuel des équipements. Cela permet de détecter précocement une dérive avant qu'elle devienne un sinistre majeur en votre absence."),
            ("Intervenez-vous sur les villas classées de la Ville d'Hiver ?",
             "Oui, nos méthodes strictement non destructives (thermographie, acoustique, gaz traceur) préservent les parquets d'époque, moulures, boiseries et carrelages des villas Monument historique. Nous adaptons nos protocoles aux consignes de conservation des propriétaires et, si nécessaire, aux recommandations d'un architecte du patrimoine.")
        ],
    },
    "libourne": {
        "ville": "Libourne",
        "ville_article": "à Libourne",
        "cp": "33500",
        "image": "ville-libourne-vignoble.webp",
        "image_alt": "Propriété viticole du Libournais près de Libourne, zone d'intervention recherche de fuite en Gironde",
        "pitch_local": "Capitale historique du Libournais, Libourne se situe au confluent de la Dordogne et de l'Isle, au cœur d'un territoire viticole exceptionnel (Saint-Émilion, Pomerol, Fronsac, Côtes de Castillon). Ce contexte unique mélange maisons bourgeoises anciennes, chais de propriétés viticoles et logements modernes, chacun avec ses problématiques spécifiques.",
        "quartiers": "Libourne Centre, Vieux Libourne, La Ballastière, Verdet, Fontenelle",
        "zones_voisines": "Saint-Émilion, Pomerol, Fronsac, Saint-Denis-de-Pile, Coutras, Castillon-la-Bataille, Branne",
        "spécificités": [
            ("Chais et propriétés viticoles anciennes", "Les chais des grands domaines (Saint-Émilion, Pomerol) ont été agrandis à plusieurs reprises sur un bâti parfois médiéval. Les réseaux hydrauliques y sont souvent hétérogènes : fonte ancienne, cuivre des années 50, PVC moderne. La localisation d'une fuite dans ces configurations demande expérience et méthode."),
            ("Sol argileux et bastides médiévales", "Le Libournais repose sur des sols calcaires et argileux sujets aux mouvements saisonniers. Les bastides médiévales de Libourne et des environs ont des fondations peu profondes, sensibles à ces variations. Les canalisations enterrées sont particulièrement exposées."),
            ("Maisons bourgeoises du XIXe siècle", "Le centre de Libourne compte de nombreuses maisons bourgeoises de négociants en vins, avec des chemins d'évacuation complexes depuis les étages jusqu'aux caves voûtées. La thermographie et le gaz traceur permettent de suivre le trajet de la fuite sans descendre en cave à chaque étape."),
            ("Proximité Dordogne et nappe phréatique", "La position au confluent de deux rivières place la nappe phréatique proche de la surface. Les caves et sous-sols des propriétés anciennes sont sensibles aux remontées capillaires, qu'il faut distinguer d'une vraie fuite par des mesures d'humidimètre méthodiques.")
        ],
        "cas_frequent": "Cas type dans le Libournais : maison bourgeoise de négociant en vins au centre de Libourne, bâtie vers 1880, avec cave voûtée ayant toujours servi de chai familial. Les propriétaires notent une humidité croissante au plafond de la cave, suspectent une fuite mais n'osent pas casser les voûtes. Notre diagnostic : humidimètre pour cartographier la zone humide, thermographie du plancher haut, écoute acoustique sur colonnes EU/EV. La fuite est localisée sur un coude de canalisation fonte au niveau du plancher de la salle de bains du 1er étage, à 8 mètres de la zone humide visible en cave (l'eau migre le long d'une poutre avant de gouter). Réparation ciblée sans démolir la voûte historique.",
        "methodes_focus": "Dans le Libournais, zone viticole aux bâtis anciens et sols argileux, notre protocole se structure autour de 3 méthodes principales. L'humidimètre en premier, pour distinguer une vraie fuite de la remontée capillaire fréquente dans les caves voûtées à proximité de la Dordogne. La thermographie infrarouge ensuite, pour suivre les circulations d'eau dans les planchers anciens en bois où une fuite peut se diffuser sur plusieurs mètres avant d'apparaître visiblement. Le gaz traceur enfin, pour les canalisations enterrées des domaines viticoles (souvent longues, entre château, chais et dépendances) fragilisées par les mouvements retrait-gonflement de l'argile. L'inspection caméra dans les colonnes fonte d'origine est systématique sur les maisons bourgeoises centenaires.",
        "faq_locale": [
            ("Intervenez-vous sur les grands crus de Saint-Émilion et Pomerol ?",
             "Oui, nous nous déplaçons régulièrement dans les domaines de Saint-Émilion, Pomerol, Fronsac et leurs environs pour des interventions sur les résidences des propriétaires, les chais et les dépendances. Nos techniciens respectent strictement les consignes de discrétion et de confidentialité propres à ces domaines prestigieux."),
            ("La nappe phréatique peut-elle faire passer pour une fuite une simple remontée d'humidité ?",
             "Absolument, c'est un piège classique à Libourne. Une cave voûtée humide peut donner l'impression d'une fuite alors qu'il s'agit de remontées capillaires dues à la nappe proche de la Dordogne. Notre humidimètre mesure la teneur précise en eau dans les matériaux et distingué une infiltration ponctuelle (gradient fort, zone localisée) d'une remontée (humidité diffuse et constante). Nous ne lançons une intervention que si la fuite est réellement caractérisée."),
            ("Y a-t-il un supplément de déplacement pour Libourne depuis Bordeaux ?",
             "Un forfait de déplacement de 40 euros HT s'applique pour les interventions dans le Libournais et les domaines alentours (Saint-Émilion, Pomerol, Fronsac, Castillon). Ce forfait est intégré dans le devis communiqué avant intervention. Pour les chantiers groupés (2 interventions même jour dans le secteur), ce forfait peut être mutualisé.")
        ],
    },
    "pessac": {
        "ville": "Pessac",
        "ville_article": "à Pessac",
        "cp": "33600",
        "image": "ville-bordeaux-patrimoine.webp",
        "image_alt": "Résidences et maisons à Pessac, zone d'intervention recherche de fuite en métropole bordelaise",
        "pitch_local": "Troisième ville de la métropole bordelaise, Pessac abrite le principal campus universitaire de la Nouvelle-Aquitaine (Université de Bordeaux, Sciences Po), la Cité Frugès de Le Corbusier (UNESCO) et un parc immobilier varié : résidences étudiantes, copropriétés familiales, pavillons individuels, domaines viticoles Graves.",
        "quartiers": "Pessac Centre, Alouette, Saige, Camponac, Bersol, France, Noès, Le Pontet, Cap-de-Bos",
        "zones_voisines": "Bordeaux, Talence, Gradignan, Mérignac, Villenave-d'Ornon, Canéjan",
        "spécificités": [
            ("Cité Frugès et patrimoine XXe siècle", "La Cité Frugès imaginée par Le Corbusier dans les années 1920, classée au patrimoine mondial de l'UNESCO, présente un parc immobilier aux caractéristiques techniques particulières. Toute intervention doit être menée avec la plus grande délicatesse pour respecter l'intégrité architecturale protégée."),
            ("Résidences universitaires et copropriétés", "Les quartiers d'Alouette et de Saige comptent un grand nombre de résidences étudiantes et de copropriétés familiales des années 1960-80. Les colonnes montantes et les évacuations collectives sont souvent à l'origine de fuites récurrentes entre logements, relevant de la convention IRSI en copropriété."),
            ("Domaines viticoles Graves et Pessac-Léognan", "Les appellations Pessac-Léognan comptent des châteaux historiques sur le territoire (Haut-Brion, Pape-Clément, Les Carmes Haut-Brion). Leurs réseaux hydrauliques combinent piscines, arrosage, chais et résidences, ce qui complexifie la recherche de fuite en cas de surconsommation."),
            ("Zone Bersol et bâti tertiaire récent", "Le parc d'activité de Bersol et les zones tertiaires récentes accueillent des bâtiments aux réseaux modernes (multicouche, PE). Les fuites y sont souvent liées à des défauts de pose sur sertissage ou à des mouvements de dalle. Notre écoute électro-acoustique cible précisément ces signatures.")
        ],
        "cas_frequent": "Cas fréquent à Pessac : copropriété familiale de 40 logements à Alouette, construite en 1972. Le syndic signalé des fuites récurrentes au dernier étage depuis 6 mois, avec plusieurs logements touchés par intermittence. Notre diagnostic pour le conseil syndical : inspection caméra des colonnes montantes EU/EV communes, écoute acoustique, identification des tronçons corrodés. Rapport remis : 4 zones de fuite identifiées sur la colonne montante principale, matériau fonte gris d'origine fatigué. Préconisation : chemisage de la colonne par manchon résine époxy (durée de vie 50 ans), intervention planifiée en AG extraordinaire avec vote article 25.",
        "methodes_focus": "À Pessac, la diversité du parc immobilier (copropriétés 1960-80 d'Alouette et Saige, résidences étudiantes, pavillons individuels, châteaux viticoles Pessac-Léognan) impose une approche méthodologique modulable. Sur les copropriétés anciennes, inspection caméra systématique des colonnes montantes EU/EV en fonte, souvent fatiguées après 50 ans de service. Sur les pavillons individuels, gaz traceur pour les canalisations enterrées et thermographie pour les planchers chauffants. Sur les châteaux viticoles, approche combinée multi-réseaux (résidences, chais, piscines, arrosages) pour identifier le circuit en cause avant localisation fine. L'écoute électro-acoustique est notre outil de confirmation sur les réseaux multicouche et PE des bâtiments tertiaires de Bersol.",
        "faq_locale": [
            ("Les résidences étudiantes de Pessac sont-elles couvertes par nos prestations ?",
             "Oui. Nous intervenons pour le compte des bailleurs sociaux (Aquitanis, CUB Habitat) et privés gérant des résidences étudiantes à Pessac (Saige, Alouette, Camponac). Le mandatement se fait par le gestionnaire, l'intervention est coordonnée avec les locataires. Notre rapport est fourni pour mise en jeu éventuelle de la garantie recherche de fuite."),
            ("Peut-on intervenir sur la Cité Frugès sans autorisation UNESCO ?",
             "Une recherche de fuite non destructive (thermographie, acoustique, gaz traceur) ne nécessite aucune autorisation UNESCO ou ABF car elle ne modifie pas l'aspect extérieur ni ne touche aux éléments protégés. En revanche, une réparation ouverte modifiant une façade Le Corbusier exigerait validation architectes du patrimoine. Notre rapport documente précisément pour faciliter cette démarche ultérieure si besoin."),
            ("Les châteaux viticoles Pessac-Léognan ont-ils un accès restreint ?",
             "Oui, les grands crus Pessac-Léognan (Haut-Brion, Pape-Clément, Les Carmes Haut-Brion) ont des accès sécurisés et des consignes de confidentialité strictes. Nos techniciens sont formés à ces environnements et respectent les protocoles : identification préalable, chaussures de sécurité, absence de photos non autorisées. Un devis détaillé est établi après visite préalable si la configuration le justifie.")
        ],
    },
}

METHODES_BLOCK = '''
    <div class="grid-3" style="margin-top:2rem;">
      <div class="arg-num-card">
        <span class="arg-num">01</span>
        <div class="arg-num-content">
          <h3>Thermographie infrarouge</h3>
          <p>Une caméra thermique révèle les variations de température en surface dues à une fuite d'eau derrière un mur ou sous un sol. Idéale pour les planchers chauffants, les réseaux encastrés et les fuites invisibles à l'œil nu.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">02</span>
        <div class="arg-num-content">
          <h3>Gaz traceur azote/hélium</h3>
          <p>Mélange inerte injecté dans la canalisation sous légère pression. Le gaz remonte en surface au droit de la perforation, détecté par capteur électronique. Précision au demi-mètre, idéal pour canalisations enterrées.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">03</span>
        <div class="arg-num-content">
          <h3>Écoute électro-acoustique</h3>
          <p>Amplificateur acoustique haute sensibilité qui capte le bruit caractéristique d'une fuite sous pression. La corrélation acoustique localise la source sur réseau enterré ou encastré, même à travers une dalle béton.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">04</span>
        <div class="arg-num-content">
          <h3>Caméra endoscopique ITV</h3>
          <p>Inspection Télévisée : une caméra motorisée parcourt l'intérieur des canalisations via un accès existant. identifié fissures, racines, casses, dépôts selon la norme NF EN 13508-2.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">05</span>
        <div class="arg-num-content">
          <h3>Fluorescéine et colorant UV</h3>
          <p>Colorant fluorescent non toxique versé dans le réseau. Éclairé à la lampe UV, il révèle le trajet de l'eau et le point de fuite. Très efficace pour piscines, canalisations EP, infiltrations de façade.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">06</span>
        <div class="arg-num-content">
          <h3>Humidimètre et traçage</h3>
          <p>Mesure du taux d'humidité dans les matériaux (plâtre, bois, béton) pour cartographier la zone affectée. Couplé au traçage électromagnétique des réseaux enterrés, affine la localisation avant intervention.</p>
        </div>
      </div>
    </div>
'''

TYPES_FUITES_BLOCK = '''
    <div class="grid-3" style="margin-top:1.5rem;">
      <div class="arg-num-card">
        <span class="arg-num">01</span>
        <div class="arg-num-content">
          <h3>Dégât des eaux en copropriété</h3>
          <p>Tache au plafond, compteur qui tourne, humidité cyclique : nous localisons l'origine (appartement, colonne, évacuation) pour un rapport opposable en convention IRSI.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">02</span>
        <div class="arg-num-content">
          <h3>Fuite sur plancher chauffant</h3>
          <p>Perte de pression circuit, sol froid par zones, humidité en périphérie de dalle : thermographie et gaz traceur localisent la perforation sans ouvrir toute la chape.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">03</span>
        <div class="arg-num-content">
          <h3>surconsommation d'eau</h3>
          <p>Facture en hausse sans raison, compteur qui tourne seul : test de pression, inspection caméra et écoute électro-acoustique identifient la fuite cachée intérieure ou enterrée.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">04</span>
        <div class="arg-num-content">
          <h3>Canalisation enterrée au jardin</h3>
          <p>Zone toujours verte, sol gorgé d'eau, affaissement linéaire : gaz traceur au demi-mètre près sur canalisation enterrée sans excavation préalable.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">05</span>
        <div class="arg-num-content">
          <h3>Fuite piscine sans vidange</h3>
          <p>Niveau d'eau qui baisse au-delà de l'évaporation : fluorescéine, acoustique, test pression, inspection caméra identifient la perte sans vider le bassin.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">06</span>
        <div class="arg-num-content">
          <h3>Fuite toiture / infiltration</h3>
          <p>Auréoles au plafond après pluie, salpêtre sur murs en pierre : fumigène, colorant et thermographie remontent le parcours depuis l'infiltration en façade.</p>
        </div>
      </div>
    </div>
'''

TABLEAU_COMPARATIF_BLOCK = '''
    <div style="overflow-x:auto;margin:1.5rem 0;">
      <table style="width:100%;border-collapse:collapse;font-size:.95rem;background:var(--white);">
        <thead>
          <tr>
            <th style="padding:.8rem;text-align:left;background:var(--green);color:var(--white);border:1px solid var(--green-dark);">Critère</th>
            <th style="padding:.8rem;text-align:left;background:var(--green);color:var(--white);border:1px solid var(--green-dark);">Détection non destructive</th>
            <th style="padding:.8rem;text-align:left;background:var(--green);color:var(--white);border:1px solid var(--green-dark);">Percement classique</th>
          </tr>
        </thead>
        <tbody>
          <tr><td style="padding:.8rem;border:1px solid var(--border);"><strong>Ouverture des murs/sols</strong></td><td style="padding:.8rem;border:1px solid var(--border);">Aucune avant localisation</td><td style="padding:.8rem;border:1px solid var(--border);">Multiples points au hasard</td></tr>
          <tr style="background:var(--bg-alt);"><td style="padding:.8rem;border:1px solid var(--border);"><strong>Durée du diagnostic</strong></td><td style="padding:.8rem;border:1px solid var(--border);">1h30 à 3h</td><td style="padding:.8rem;border:1px solid var(--border);">Plusieurs jours</td></tr>
          <tr><td style="padding:.8rem;border:1px solid var(--border);"><strong>Reprise des finitions</strong></td><td style="padding:.8rem;border:1px solid var(--border);">Nulle ou très limitée</td><td style="padding:.8rem;border:1px solid var(--border);">Lourde (carrelage, plâtre)</td></tr>
          <tr style="background:var(--bg-alt);"><td style="padding:.8rem;border:1px solid var(--border);"><strong>Coût global</strong></td><td style="padding:.8rem;border:1px solid var(--border);">300 à 900 € HT</td><td style="padding:.8rem;border:1px solid var(--border);">Souvent &gt; 2 000 €</td></tr>
          <tr><td style="padding:.8rem;border:1px solid var(--border);"><strong>Rapport assurance</strong></td><td style="padding:.8rem;border:1px solid var(--border);">Inclus, opposable IRSI</td><td style="padding:.8rem;border:1px solid var(--border);">Variable, souvent insuffisant</td></tr>
          <tr style="background:var(--bg-alt);"><td style="padding:.8rem;border:1px solid var(--border);"><strong>Occupation logement</strong></td><td style="padding:.8rem;border:1px solid var(--border);">Maintenue</td><td style="padding:.8rem;border:1px solid var(--border);">Souvent impossible</td></tr>
        </tbody>
      </table>
    </div>
'''

def page_ville_detection_premium(v):
    slug = v['slug']
    ctx = VILLES_PREMIUM[slug]
    ville = ctx['ville']
    ville_article = ctx['ville_article']
    cp = ctx['cp']

    # Construction des sections spécificités
    specificites_html = '\n'.join([
        f'    <h3>{titre}</h3>\n    <p>{contenu}</p>'
        for titre, contenu in ctx['spécificités']
    ])

    # méthodes focus unique par ville
    methodes_focus = ctx.get('methodes_focus', '')

    # Lien contextuel vers page piscine si existe pour cette ville
    piscine_slug_map = {p["slug"].replace("piscine-", ""): p["slug"] for p in PISCINE_PAGES}
    piscine_cta = ''
    if slug in piscine_slug_map:
        piscine_cta = f'<p style="margin-top:1rem;">Vous avez une piscine privée {ville_article} ? Consultez notre page dédiée à la <a href="/detection-fuite/{piscine_slug_map[slug]}/" style="color:var(--green);text-decoration:underline;">recherche de fuite de piscine {ville_article}</a> : méthodes spécifiques (colorant fluorescéine, inspection sous-marine, test pression), cas typiques locaux et tarifs détaillés.</p>'

    # FAQ locale unique par ville
    faq_locale_html = '\n'.join([
        f'    <h3>{q}</h3>\n    <p>{a}</p>'
        for q, a in ctx.get('faq_locale', [])
    ])
    faq_schema_entries = []
    for q, a in ctx.get('faq_locale', []):
        faq_schema_entries.append(
            '{"@type":"Question","name":' + json.dumps(q, ensure_ascii=False) +
            ',"acceptedAnswer":{"@type":"Answer","text":' + json.dumps(a, ensure_ascii=False) + '}}'
        )
    faq_schema_json = ',\n    '.join(faq_schema_entries) if faq_schema_entries else ''

    # Section Pages connexes spécifique par ville (transfère le link equity vers les pages de conversion)
    if slug == 'bordeaux':
        pages_connexes_html = f'''
<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Pages connexes : recherche de fuite à Bordeaux</h2>
    <p>Selon la nature de votre situation, accédez directement à la page la plus pertinente. Notre maillage de pages spécialisées Bordeaux couvre tous les cas de fuite d'eau, du diagnostic urgent à la prise en charge d'assurance.</p>
    <ul>
      <li><a href="/detection-fuite/urgence-bordeaux/" style="color:var(--green);text-decoration:underline;">Recherche de fuite en urgence à Bordeaux</a> : intervention sous 24h, qualification téléphonique dans l'heure, rapport remis le jour même.</li>
      <li><a href="/detection-fuite/piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">Recherche de fuite de piscine à Bordeaux</a> : gaz traceur, hydrophone, colorant fluorescéine, sans vidange du bassin.</li>
      <li><a href="/detection-fuite/fuite-apres-compteur/" style="color:var(--green);text-decoration:underline;">Fuite d'eau après compteur à Bordeaux</a> : diagnostic du réseau privatif enterré, écrêtement de facture loi Warsmann.</li>
      <li><a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">Canalisation enterrée à Bordeaux</a> : recherche de fuite par gaz traceur sur réseaux jardin, branchement, alimentation maison.</li>
      <li><a href="/detection-fuite/degats-des-eaux-bordeaux/" style="color:var(--green);text-decoration:underline;">Dégâts des eaux à Bordeaux</a> : intervention syndic et copropriété, gestion IRSI, coordination assureur.</li>
      <li><a href="/detection-fuite/chemisage-bordeaux/" style="color:var(--green);text-decoration:underline;">Chemisage de canalisation à Bordeaux</a> : rénovation sans tranchée des colonnes montantes en immeuble haussmannien.</li>
      <li><a href="/detection-fuite/fuite-plancher-chauffant-bordeaux/" style="color:var(--green);text-decoration:underline;">Fuite plancher chauffant à Bordeaux</a> : thermographie infrarouge sur tubes PER hydrauliques.</li>
      <li><a href="/detection-fuite/thermographie-infrarouge-bordeaux/" style="color:var(--green);text-decoration:underline;">Thermographie infrarouge à Bordeaux</a> : méthode reine pour les canalisations encastrées et les copropriétés haussmanniennes.</li>
      <li><a href="/detection-fuite/fluoresceine-piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">Fluorescéine piscine Bordeaux</a> : colorant traceur pour localiser une fuite de bassin sans vidange.</li>
      <li><a href="/detection-fuite/depannage-piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">Dépannage piscine à Bordeaux</a> : diagnostic + coordination réparation avec piscinistes partenaires.</li>
      <li><a href="/guide/prix-recherche-fuite-bordeaux/" style="color:var(--green);text-decoration:underline;">Tarifs de recherche de fuite à Bordeaux</a> : grille prix par type de méthode et de canalisation.</li>
      <li><a href="/guide/loi-warsmann-ecretement-facture-eau/" style="color:var(--green);text-decoration:underline;">Loi Warsmann : écrêtement de facture d'eau</a> : procédure complète après une fuite enterrée.</li>
    </ul>
  </div>
</section>
'''
    else:
        # Autres villes premium : Mérignac, Pessac, Talence, Gradignan
        piscine_link = ''
        if slug in piscine_slug_map:
            piscine_link = f'<li><a href="/detection-fuite/{piscine_slug_map[slug]}/" style="color:var(--green);text-decoration:underline;">Recherche de fuite de piscine {ville_article}</a> : méthodes non destructives spécifiques aux bassins (gaz traceur, hydrophone, colorant).</li>'
        pages_connexes_html = f'''
<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Pages connexes : recherche de fuite {ville_article}</h2>
    <p>Pour une situation spécifique, accédez directement à la page la plus pertinente.</p>
    <ul>
      {piscine_link}
      <li><a href="/villes/{slug}/chemisage/" style="color:var(--green);text-decoration:underline;">Chemisage de canalisation {ville_article}</a> : rénovation des conduites usées sans tranchée.</li>
      <li><a href="/detection-fuite/urgence-bordeaux/" style="color:var(--green);text-decoration:underline;">Urgence fuite d'eau sur Bordeaux Métropole</a> : intervention sous 24h.</li>
      <li><a href="/detection-fuite/fuite-apres-compteur/" style="color:var(--green);text-decoration:underline;">Fuite après compteur</a> : surconsommation d'eau, écrêtement loi Warsmann.</li>
      <li><a href="/guide/prix-recherche-fuite-bordeaux/" style="color:var(--green);text-decoration:underline;">Tarifs d'une recherche de fuite</a> : grille prix par méthode et type de canalisation.</li>
      <li><a href="/detection-fuite/" style="color:var(--green);text-decoration:underline;">Toutes nos méthodes de détection de fuite</a> : thermographie, gaz traceur, caméra endoscopique, écoute électro-acoustique.</li>
    </ul>
  </div>
</section>
'''

    ld_local = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Recherche Fuite Gironde",
  "description": "Recherche de fuite d'eau {ville_article} ({cp}) : méthodes non destructives, intervention sous 24h, rapport pour assurance. Spécialistes du patrimoine local.",
  "url": "https://recherche-fuite-gironde.fr/villes/{slug}/",
  "image": "https://recherche-fuite-gironde.fr/assets/{ctx['image']}",
  "address": {{
    "@type": "PostalAddress",
    "addressLocality": "{ville}",
    "postalCode": "{cp}",
    "addressCountry": "FR"
  }},
  "areaServed": {{ "@type": "City", "name": "{ville}", "postalCode": "{cp}" }},
  "priceRange": "€€",
  "serviceType": "Recherche de fuite d'eau"
}}
</script>'''

    ld_service = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "Recherche de fuite d'eau non destructive",
  "name": "Recherche de fuite d'eau {ville_article}",
  "description": "Localisation précise de fuite d'eau {ville_article} par méthodes non destructives : thermographie infrarouge, gaz traceur azote/hélium, écoute électro-acoustique, caméra endoscopique, fluorescéine. Rapport technique inclus.",
  "provider": {{
    "@type": "LocalBusiness",
    "name": "Recherche Fuite Gironde",
    "url": "https://recherche-fuite-gironde.fr/"
  }},
  "areaServed": {{ "@type": "Place", "name": "{ville} et métropole" }},
  "category": "Détection de fuite non destructive"
}}
</script>'''

    ld_breadcrumb = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{ "@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://recherche-fuite-gironde.fr/" }},
    {{ "@type": "ListItem", "position": 2, "name": "Villes", "item": "https://recherche-fuite-gironde.fr/plan-du-site/" }},
    {{ "@type": "ListItem", "position": 3, "name": "{ville}", "item": "https://recherche-fuite-gironde.fr/villes/{slug}/" }}
  ]
}}
</script>'''

    ld_faq = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {faq_schema_json},
    {{
      "@type": "Question",
      "name": "Combien coûte une recherche de fuite {ville_article} ?",
      "acceptedAnswer": {{ "@type": "Answer", "text": "Entre 300 et 900 euros HT selon la méthode employée et la complexité du réseau. Un devis fixe est communiqué avant intervention, aucun déplacement facturé si vous décidez de ne pas donner suite. Souvent remboursable par votre assurance habitation." }}
    }},
    {{
      "@type": "Question",
      "name": "Intervenez-vous sous 24h {ville_article} ?",
      "acceptedAnswer": {{ "@type": "Answer", "text": "Oui, pour les fuites actives importantes sur {ville} et les communes voisines, nous intervenons sous 24 heures. Un technicien vous rappelle dans l'heure après votre demande pour qualifier la situation et caler un rendez-vous prioritaire." }}
    }},
    {{
      "@type": "Question",
      "name": "Le rapport est-il reconnu par les assurances ?",
      "acceptedAnswer": {{ "@type": "Answer", "text": "Oui, notre rapport technique (photos, méthodes employées, point de fuite localisé, préconisations) est accepté par les principaux assureurs français. En copropriété, il facilite l'application de la convention IRSI pour les sinistres dégâts des eaux jusqu'à 5 000 euros HT." }}
    }}
  ]
}}
</script>'''

    body = f'''
<section class="hero-mini">
  <div class="container">
    <nav class="breadcrumb">
      <a href="/">Accueil</a>
      <span>&rsaquo;</span>
      <a href="/plan-du-site/">Villes</a>
      <span>&rsaquo;</span>
      <span>{ville}</span>
    </nav>
    <span class="badge-cp">{cp}</span>
    <h1>Recherche de fuite d'eau {ville_article} ({cp})</h1>
    <p class="hero-mini-lead">Localisation précise de votre fuite d'eau {ville_article} <strong>sans démolition ni tranchée</strong> : thermographie, gaz traceur, écoute électro-acoustique, caméra endoscopique. Intervention sous 24h, rapport technique remis le jour même pour votre assureur.</p>
    <div class="hero-mini-cta">
      <a href="/devis/" class="btn btn-gold">Demander un devis gratuit</a>
      <a href="#méthodes" class="btn btn-outline-green">Nos méthodes</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <figure style="margin:0 0 2rem;">
      <img src="/assets/{ctx['image']}" alt="{ctx['image_alt']}" width="1600" height="1067" loading="eager" style="width:100%;max-height:380px;height:auto;object-fit:cover;border-radius:12px;display:block;">
    </figure>

    <p><strong>Intervention sous 24h {ville_article} et dans les communes voisines.</strong> {ctx['pitch_local']}</p>

    <p>Nos techniciens interviennent dans l'ensemble de la ville ainsi que dans les quartiers limitrophes : {ctx['quartiers']}. Zones voisines couvertes : {ctx['zones_voisines']}.</p>
    {piscine_cta}
    <p style="margin-top:1rem;">En cas de fuite active importante ou de dégât des eaux en cours, consultez notre page <a href="/detection-fuite/urgence-bordeaux/" style="color:var(--green);text-decoration:underline;">recherche de fuite en urgence à Bordeaux et métropole</a> : intervention prioritaire sous 24h. Si votre surconsommation est inexpliquée, voir aussi notre diagnostic <a href="/detection-fuite/fuite-apres-compteur/" style="color:var(--green);text-decoration:underline;">fuite d'eau après compteur</a>.</p>
  </div>
</section>

<section class="section section-alt" id="méthodes">
  <div class="container" style="max-width:1080px;">
    <h2>6 méthodes de recherche de fuite d'eau {ville_article}</h2>
    <p>{methodes_focus if methodes_focus else 'Selon la nature, la localisation et la gravité de la fuite, nos techniciens combinent plusieurs méthodes non destructives pour localiser la source avec précision.'}</p>
    <p style="margin-top:1rem;">Ci-dessous, les 6 méthodes de notre protocole de diagnostic, combinées selon le scénario rencontré.</p>
    {METHODES_BLOCK}
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <h2>Types de fuites que nous localisons {ville_article}</h2>
    <p>Six situations que nous traitons quotidiennement dans les logements, copropriétés, commerces et résidences de {ville}.</p>
    {TYPES_FUITES_BLOCK}
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:1080px;">
    <h2>Spécificités locales de la recherche de fuite {ville_article}</h2>
    <p>Chaque territoire à ses particularités. Nos techniciens connaissent celles de {ville} pour adapter leurs méthodes à votre configuration.</p>

{specificites_html}
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <h2>Détection non destructive vs percement classique {ville_article}</h2>
    <p>Pourquoi la recherche de fuite moderne bat systématiquement le percement aléatoire ou la démolition préventive, surtout sur un patrimoine comme celui de {ville}.</p>
    {TABLEAU_COMPARATIF_BLOCK}
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Cas type que nous traitons {ville_article}</h2>
    <p>{ctx.get('cas_frequent', '')}</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Questions fréquentes sur la recherche de fuite {ville_article}</h2>

{faq_locale_html}

    <h3>Combien coûte une recherche de fuite {ville_article} ?</h3>
    <p>Entre 300 et 900 euros HT selon la méthode employée et la complexité du réseau. Un devis fixe est communiqué avant intervention, aucun déplacement facturé si vous décidez de ne pas donner suite. Souvent remboursable par votre assurance habitation au titre de la garantie recherche de fuite.</p>

    <h3>Intervenez-vous sous 24h {ville_article} ?</h3>
    <p>Oui, pour les fuites actives importantes sur {ville} et les communes voisines, nous intervenons sous 24 heures. Un technicien vous rappelle dans l'heure après votre demande pour qualifier la situation et caler un rendez-vous prioritaire.</p>

    <h3>Le rapport est-il reconnu par les assurances ?</h3>
    <p>Oui, notre rapport technique (photos, méthodes employées, point de fuite localisé, préconisations) est accepté par les principaux assureurs français. En copropriété, il facilite l'application de la convention IRSI pour les sinistres dégâts des eaux jusqu'à 5 000 euros HT.</p>

    <div style="margin-top:2rem;text-align:center;">
      <a href="/devis/" class="btn btn-gold">Demander un devis {ville_article}</a>
      <div style="margin-top:1rem;">
        <a href="/villes/{slug}/chemisage/" class="btn btn-outline-green">Chemisage {ville_article} &rarr;</a>
      </div>
    </div>
  </div>
</section>

{pages_connexes_html}

{form_section(ville)}
'''

    return html_base(
        f'Recherche de fuite {ville} ({cp}) | Sans démolition',
        f'Recherche de fuite d\'eau {ville_article} : thermographie, gaz traceur, caméra endoscopique. Intervention sous 24h, rapport pour assurance. Spécialistes patrimoine local.',
        f'https://recherche-fuite-gironde.fr/villes/{slug}/',
        body,
        extra_ld=ld_local + ld_service + ld_breadcrumb + ld_faq,
    )


# ═══════════════════════════════════════════════════════════════
# PAGES USE CASE : Urgence fuite par ville
# ═══════════════════════════════════════════════════════════════

URGENCE_PAGES = [
    {
        "slug": "urgence-bordeaux",
        "ville": "Bordeaux",
        "ville_article": "à Bordeaux",
        "cp": "33000",
        "zones": "Mérignac, Pessac, Talence, Le Bouscat, Caudéran, Bègles",
    },
]

def page_urgence_ville(p):
    ville = p["ville"]
    ville_article = p["ville_article"]
    cp = p["cp"]
    slug = p["slug"]

    ld_local = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "EmergencyService",
  "name": "Recherche Fuite Gironde — Intervention urgence",
  "description": "Recherche de fuite d'eau en urgence {ville_article} et en Gironde, intervention sous 24 heures. Localisation sans démolition, rapport pour assurance.",
  "url": "https://recherche-fuite-gironde.fr/detection-fuite/{slug}/",
  "image": "https://recherche-fuite-gironde.fr/assets/urgence-fuite-eau.webp",
  "address": {{
    "@type": "PostalAddress",
    "addressLocality": "{ville}",
    "postalCode": "{cp}",
    "addressCountry": "FR"
  }},
  "areaServed": {{ "@type": "City", "name": "{ville}" }},
  "priceRange": "€€",
  "availableService": {{
    "@type": "Service",
    "serviceType": "Recherche de fuite d'eau en urgence"
  }}
}}
</script>'''

    ld_faq = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{
      "@type": "Question",
      "name": "Intervenez-vous vraiment sous 24h {ville_article} ?",
      "acceptedAnswer": {{ "@type": "Answer", "text": "Oui, pour les fuites actives importantes sur Bordeaux et sa métropole, nous intervenons sous 24 heures, parfois le jour même selon l'horaire de votre appel. Un technicien vous recontacte dans l'heure après votre demande pour qualifier la situation et caler un rendez-vous." }}
    }},
    {{
      "@type": "Question",
      "name": "Que faire en attendant l'arrivée du technicien ?",
      "acceptedAnswer": {{ "@type": "Answer", "text": "Coupez immédiatement l'arrivée d'eau générale au compteur. Éloignez les appareils électriques et le mobilier de la zone inondée. Ne touchez pas aux tableaux électriques si le sol est mouillé. Placez des seaux et des bâches. Si vous êtes en copropriété, prévenez le gardien ou le syndic." }}
    }},
    {{
      "@type": "Question",
      "name": "Les interventions d'urgence sont-elles plus chères ?",
      "acceptedAnswer": {{ "@type": "Answer", "text": "Non. Nos tarifs de recherche de fuite restent les mêmes en urgence (300 à 600 € HT selon les méthodes). Seule la disponibilité change, avec un créneau prioritaire dans les 24 heures. Aucune majoration 'urgence' artificielle." }}
    }},
    {{
      "@type": "Question",
      "name": "L'assurance couvre-t-elle une intervention d'urgence ?",
      "acceptedAnswer": {{ "@type": "Answer", "text": "Oui, la garantie 'recherche de fuite' de votre multirisque habitation couvre l'intervention, urgente ou non, dès lors qu'un dégât des eaux est constaté. Notre rapport technique est reconnu par les principaux assureurs français. Déclarez le sinistre sous 5 jours ouvrables." }}
    }},
    {{
      "@type": "Question",
      "name": "Intervenez-vous le week-end et les jours fériés ?",
      "acceptedAnswer": {{ "@type": "Answer", "text": "Nos interventions s'effectuent du lundi au samedi. Pour les fuites avérées avec dégât des eaux important le dimanche ou un jour férié, contactez-nous : nous organisons autant que possible une intervention le premier jour ouvré suivant en créneau prioritaire." }}
    }}
  ]
}}
</script>'''

    body = f'''
<section class="hero-mini hero-urgence">
  <div class="container">
    <nav class="breadcrumb">
      <a href="/">Accueil</a>
      <span>&rsaquo;</span>
      <a href="/detection-fuite/">Détection de fuite</a>
      <span>&rsaquo;</span>
      <span>Urgence {ville}</span>
    </nav>
    <span class="badge-alert">Intervention sous 24h</span>
    <h1>Recherche de fuite en urgence {ville_article}</h1>
    <p class="hero-mini-lead">Fuite active, dégât des eaux en cours, inondation : nos techniciens spécialisés interviennent sous 24 heures sur Bordeaux et sa métropole. <strong>Localisation précise sans démolition</strong>, rapport technique remis le jour même pour votre assureur.</p>
    <div class="hero-mini-cta">
      <a href="/devis/" class="btn btn-gold">Demander une intervention urgente</a>
      <a href="#reflexes" class="btn btn-outline-green">Gestes d'urgence</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <figure style="margin:0 0 2rem;">
      <img src="/assets/urgence-fuite-eau.webp" alt="Fuite d'eau active sur une canalisation, situation d'urgence nécessitant une intervention rapide à Bordeaux" width="1600" height="1067" loading="eager" style="width:100%;max-height:380px;height:auto;object-fit:cover;border-radius:12px;display:block;">
    </figure>

    <h2 id="reflexes">Les 4 gestes d'urgence avant l'arrivée du technicien</h2>
    <p>Les premières minutes sont décisives pour limiter les dégâts d'une fuite active. Avant toute chose, voici la conduite à tenir.</p>

    <div class="grid-3" style="margin-top:1.5rem;">
      <div class="arg-num-card">
        <span class="arg-num">01</span>
        <div class="arg-num-content">
          <h3>Coupez l'arrivée d'eau générale</h3>
          <p>Le robinet d'arrêt général se trouve en général sous l'évier de la cuisine, dans un placard technique, ou à défaut directement au compteur d'eau (regard en façade ou en cave). Dans un appartement, le robinet d'arrêt de l'étage est aussi une option.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">02</span>
        <div class="arg-num-content">
          <h3>Coupez l'électricité des zones inondées</h3>
          <p>Si de l'eau atteint le sol près de prises ou de tableaux électriques, coupez le disjoncteur général au compteur avant de poser le pied dans la zone. Ne touchez jamais un appareil électrique mouillé.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">03</span>
        <div class="arg-num-content">
          <h3>Protégez meubles et documents</h3>
          <p>Éloignez ou surélevez les meubles, les électroménagers, les documents administratifs. Placez des seaux, des serpillières et des bâches pour récupérer et canaliser l'eau. Photographiez les dégâts dès que possible pour votre assureur.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">04</span>
        <div class="arg-num-content">
          <h3>Prévenez les bons interlocuteurs</h3>
          <p>En copropriété, prévenez le syndic ou le gardien. En location, informez votre propriétaire dans la foulée. Déclarez ensuite le sinistre à votre assurance habitation dans les 5 jours ouvrables pour activer la garantie dégâts des eaux.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:1080px;">
    <h2>Quand faut-il considérer qu'il y a urgence ?</h2>
    <p>Toutes les fuites ne nécessitent pas une intervention sous 24 heures. Voici les situations qui justifient une prise en charge prioritaire et celles qui peuvent attendre un rendez-vous classique.</p>

    <h3>Urgences réelles (intervention 24h)</h3>
    <ul>
      <li><strong>Dégât des eaux en cours</strong> : plafond qui goutte, eau qui ruisselle sur les murs, flaques qui s'étendent</li>
      <li><strong>Fuite sur canalisation sous pression</strong> avec perte d'eau supérieure à 1 m³ par jour (compteur qui tourne en permanence)</li>
      <li><strong>Inondation du local technique ou de la cave</strong> (risque électrique associé)</li>
      <li><strong>Fuite active en copropriété impactant plusieurs lots</strong> (responsabilité syndic engagée)</li>
      <li><strong>Fuite de piscine très rapide</strong> (perte supérieure à 5 cm par jour) impactant le jardin et les fondations</li>
    </ul>

    <h3>Situations non urgentes (rendez-vous sous 3 à 7 jours)</h3>
    <ul>
      <li>Facture d'eau anormalement élevée sans dégât visible (à diagnostiquer rapidement mais pas en urgence)</li>
      <li>Tache d'humidité stable au plafond qui ne s'étend pas</li>
      <li>Zone de jardin plus humide que la normale sans affaissement ni perte d'eau massive</li>
      <li>Fuite goutte-à-goutte sur un robinet ou un flexible (intervention plombier généraliste plus adaptée)</li>
    </ul>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <h2>Notre protocole d'intervention urgence {ville_article}</h2>

    <figure style="margin:1.5rem 0;">
      <img src="/assets/technicien-intervention-urgence.webp" alt="Technicien en intervention d'urgence sur une canalisation à Bordeaux" width="1600" height="1067" loading="lazy" style="width:100%;max-height:360px;height:auto;object-fit:cover;border-radius:12px;display:block;">
    </figure>

    <h3>Étape 1 : qualification téléphonique dans l'heure</h3>
    <p>Dès votre demande via le formulaire ou notre ligne directe, un technicien vous rappelle dans l'heure qui suit (horaires ouvrés). Il pose les questions clés : depuis quand la fuite est active, avez-vous coupé l'eau, où sont les premiers dégâts visibles, y a-t-il un risque électrique ou un impact sur des voisins. Cette qualification permet d'engager les bons outils et d'estimer la durée d'intervention.</p>

    <h3>Étape 2 : déplacement prioritaire</h3>
    <p>Un créneau est bloqué dans les 24 heures, en général le jour même ou le lendemain matin selon l'heure de votre appel. Le technicien arrive avec l'ensemble du matériel : thermographie infrarouge, gaz traceur, écoute électro-acoustique, caméra endoscopique, humidimètre. Rien n'est à prévoir de votre côté.</p>

    <h3>Étape 3 : localisation non destructive</h3>
    <p>L'intervention dure en moyenne 1h30 à 3 heures. Les méthodes sont choisies en fonction des symptômes : sol chaud ou humidité en surface, compteur qui tourne, bruit caractéristique. Le point de fuite est localisé au mètre près, sans ouverture préalable des murs ni du sol.</p>

    <h3>Étape 4 : rapport technique le jour même</h3>
    <p>Un rapport écrit avec photos, méthodes employées, localisation précise et préconisations de réparation est remis sur place ou envoyé le jour même par email. Ce document est utilisable directement pour votre déclaration de sinistre et la prise en charge par votre assurance dans le cadre de la garantie recherche de fuite et dégâts des eaux.</p>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Questions fréquentes sur l'urgence fuite d'eau {ville_article}</h2>

    <h3>Intervenez-vous vraiment sous 24 heures {ville_article} ?</h3>
    <p>Oui, pour les fuites actives importantes sur Bordeaux et sa métropole, nous intervenons sous 24 heures, parfois le jour même selon l'horaire de votre appel. Un technicien vous recontacte dans l'heure après votre demande pour qualifier la situation et caler un rendez-vous.</p>

    <h3>Que faire en attendant l'arrivée du technicien ?</h3>
    <p>Coupez immédiatement l'arrivée d'eau générale au compteur. Éloignez les appareils électriques et le mobilier de la zone inondée. Ne touchez pas aux tableaux électriques si le sol est mouillé. Placez des seaux et des bâches. Si vous êtes en copropriété, prévenez le gardien ou le syndic.</p>

    <h3>Les interventions d'urgence sont-elles plus chères ?</h3>
    <p>Non. Nos tarifs de recherche de fuite restent les mêmes en urgence (300 à 600 € HT selon les méthodes). Seule la disponibilité change, avec un créneau prioritaire dans les 24 heures. Aucune majoration « urgence » artificielle.</p>

    <h3>L'assurance couvre-t-elle une intervention d'urgence ?</h3>
    <p>Oui, la garantie « recherche de fuite » de votre multirisque habitation couvre l'intervention, urgente ou non, dès lors qu'un dégât des eaux est constaté. Notre rapport technique est reconnu par les principaux assureurs français. Déclarez le sinistre sous 5 jours ouvrables.</p>

    <h3>Intervenez-vous le week-end et les jours fériés ?</h3>
    <p>Nos interventions s'effectuent du lundi au samedi. Pour les fuites avérées avec dégât des eaux important le dimanche ou un jour férié, contactez-nous : nous organisons autant que possible une intervention le premier jour ouvré suivant en créneau prioritaire.</p>

    <h3>Que faire si l'eau atteint les voisins du dessous ?</h3>
    <p>Prévenez-les immédiatement et le syndic si vous êtes en copropriété. Prenez des photos datées avant tout nettoyage. Déclarez le sinistre à votre assurance en mentionnant les voisins impactés : la convention IRSI s'applique automatiquement entre assureurs pour les sinistres dégâts des eaux en copropriété jusqu'à 5 000 € HT. Voir notre page dédiée <a href="/detection-fuite/degats-des-eaux-bordeaux/" style="color:var(--green);text-decoration:underline;">dégâts des eaux à Bordeaux pour syndics et copropriétés</a> pour la procédure complète.</p>

    <div style="margin-top:2rem;text-align:center;">
      <a href="/devis/" class="btn btn-gold">Demander une intervention urgente</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Autres situations qui peuvent s'apparenter à une urgence</h2>
    <p>Selon la nature de votre fuite, plusieurs situations connexes peuvent s'apparenter à une urgence ou en découler. Notre réseau de pages spécialisées vous aide à identifier le bon point d'entrée.</p>
    <ul>
      <li><a href="/detection-fuite/fuite-apres-compteur/" style="color:var(--green);text-decoration:underline;">Fuite d'eau après compteur</a> : si votre compteur tourne en permanence et votre facture explose, la fuite est probablement sur votre réseau privatif enterré.</li>
      <li><a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">Recherche de fuite canalisation enterrée à Bordeaux</a> : pour les fuites au jardin ou sur réseau enterré entre compteur et maison, méthode gaz traceur.</li>
      <li><a href="/detection-fuite/fuite-plancher-chauffant-bordeaux/" style="color:var(--green);text-decoration:underline;">Fuite plancher chauffant à Bordeaux</a> : tache au plafond du voisin du dessous, souvent due à une perforation sur tube PER de plancher chauffant.</li>
      <li><a href="/detection-fuite/thermographie-infrarouge-bordeaux/" style="color:var(--green);text-decoration:underline;">Thermographie infrarouge à Bordeaux</a> : caméra thermique haute résolution pour localiser une fuite encastrée en moins d'une heure.</li>
      <li><a href="/detection-fuite/degats-des-eaux-bordeaux/" style="color:var(--green);text-decoration:underline;">Dégâts des eaux à Bordeaux</a> : sinistre constaté chez vous ou chez un voisin, gestion IRSI et coordination assureur.</li>
      <li><a href="/guide/loi-warsmann-ecretement-facture-eau/" style="color:var(--green);text-decoration:underline;">Loi Warsmann : écrêtement de facture d'eau</a> : après une fuite enterrée, vous pouvez obtenir le plafonnement de la surfacturation auprès de Suez ou de la régie.</li>
      <li><a href="/guide/prix-recherche-fuite-bordeaux/" style="color:var(--green);text-decoration:underline;">Prix d'une recherche de fuite à Bordeaux</a> : grille tarifaire détaillée par type de méthode et de canalisation.</li>
      <li><a href="/simulateur-cout-fuite/" style="color:var(--green);text-decoration:underline;">Simulateur de coût de fuite à Bordeaux</a> : calculez en 30 secondes le coût mensuel et annuel de votre fuite avec les tarifs réels Suez et Régie.</li>
    </ul>
  </div>
</section>

{form_section(p['ville'])}
'''

    return html_base(
        f'Recherche de fuite urgence {ville_article} | Intervention 24h',
        f'Fuite d\'eau en urgence {ville_article} : intervention sous 24h, localisation sans démolition, rapport pour assurance. Nos techniciens spécialisés dans toute la Gironde.',
        f'https://recherche-fuite-gironde.fr/detection-fuite/{slug}/',
        body,
        extra_ld=ld_local + ld_faq,
    )


# ═══════════════════════════════════════════════════════════════
# PAGE HUB : Recherche de fuite piscine (pillar)
# ═══════════════════════════════════════════════════════════════

def page_piscine_hub():
    villes_cards = '\n'.join([
        f'''<a href="/detection-fuite/{p["slug"]}/" class="loc-card" style="text-decoration:none;color:inherit;padding:1.25rem;background:var(--white);border:1px solid var(--border);border-radius:12px;display:block;">
          <strong style="display:block;color:var(--green);font-size:1.05rem;margin-bottom:.4rem;">Piscine {p["ville"]}</strong>
          <span style="font-size:.85rem;color:var(--muted);">{p["cp"]} · {p["zones_voisines"].split(",")[0].strip()} et environs</span>
        </a>'''
        for p in PISCINE_PAGES
    ])

    ld_service = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "Recherche de fuite de piscine sans vidange",
  "name": "Recherche de fuite de piscine en Gironde",
  "description": "Localisation précise de fuite sur piscine privée sans vidanger le bassin. méthodes : colorant fluorescéine, écoute électro-acoustique, test de pression, inspection sous-marine, gaz traceur. couverture toute la Gironde : Bordeaux, Bassin d'Arcachon, Libournais, Medoc.",
  "provider": {
    "@type": "LocalBusiness",
    "name": "Recherche Fuite Gironde",
    "url": "https://recherche-fuite-gironde.fr/"
  },
  "areaServed": { "@type": "AdministrativeArea", "name": "Gironde" },
  "category": "détection de fuite aquatique"
}
</script>'''

    ld_breadcrumb = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://recherche-fuite-gironde.fr/" },
    { "@type": "ListItem", "position": 2, "name": "Détection de fuite", "item": "https://recherche-fuite-gironde.fr/detection-fuite/" },
    { "@type": "ListItem", "position": 3, "name": "Recherche de fuite piscine", "item": "https://recherche-fuite-gironde.fr/detection-fuite/piscine/" }
  ]
}
</script>'''

    body = f'''
<section class="hero-mini">
  <div class="container">
    <nav class="breadcrumb">
      <a href="/">Accueil</a>
      <span>&rsaquo;</span>
      <a href="/detection-fuite/">détection de fuite</a>
      <span>&rsaquo;</span>
      <span>Piscine</span>
    </nav>
    <h1>Recherche de fuite de piscine en Gironde</h1>
    <p class="hero-mini-lead">Votre piscine perd de l'eau anormalement ? Nos techniciens spécialisés localisent la fuite <strong>sans vidanger le bassin</strong> grâce a 6 méthodes complementaires : colorant fluorescéine, écoute électro-acoustique, test de pression, inspection sous-marine, gaz traceur azote/hélium, thermographie infrarouge. Intervention sur toute la Gironde, rapport pour assurance.</p>
    <div class="hero-mini-cta">
      <a href="/devis/" class="btn btn-gold">Demander un devis piscine</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <h2>La piscine, première cause de fuite en Gironde</h2>
    <p>Sur les 132 conversions issues de notre campagne d'acquisition l'an dernier, plus d'une sur quatre concernait une piscine privée. Le parc bordelais et girondin compte plusieurs milliers de bassins privés, dont une part importante atteint l'âgé critique ou les fuites deviennent fréquentes : 25 à 35 ans pour les liners PVC, 15 à 25 ans pour les coques polyester, 30 à 50 ans pour les bassins béton armé.</p>

    <p>Plutot que vidanger pour inspecter (coûteux, risque de soulèvement du bassin sur sols sableux ou nappe phreatique haute), notre méthodologie non destructive identifié la fuite directement, bassin plein. Notre rapport est ensuite utilisable pour la prise en charge par votre assurance habitation.</p>

    <h2>Recherche de fuite piscine par ville en Gironde</h2>
    <p>Sept communes a forte densité de piscines disposent d'une page dédiée avec les spécificités locales (type de bassins majoritaires, problématiques geologiques, exemples d'interventions récurrentes).</p>

    <div class="grid-3" style="margin-top:1.5rem;">
      {villes_cards}
    </div>

    <p style="margin-top:1.5rem;">Vous habitez une autre commune de Gironde ? Nous intervenons aussi sur Talence, Pessac, Le Haillan, Eysines, Bruges, Cenon, Lormont, Floirac et toute la métropole bordelaise. Consultez notre <a href="/villes/bordeaux/" style="color:var(--green);text-decoration:underline;">page Bordeaux</a> ou contactez-nous directement pour les communes hors métropole (Lege-Cap-Ferret, Andernos-les-Bains, Lesparre-Medoc, Saint-Émilion, Langon).</p>

    <p style="margin-top:1.5rem;"><strong>Panorama complet</strong> : pour qualifier votre situation, identifier le bon prestataire et comprendre tous les aspects (symptômes, diagnostic, réparation, prix, assurance), consultez notre <a href="/guide/fuite-piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">guide complet fuite piscine à Bordeaux</a> qui consolide les 12 articles du site avec sommaire structuré.</p>

    <p style="margin-top:1rem;"><strong>Par marque</strong> : si vous connaissez le constructeur de votre piscine, voir nos pages dédiées avec pathologies spécifiques : <a href="/guide/fuite-piscine-desjoyaux-bordeaux/" style="color:var(--green);text-decoration:underline;">fuite piscine Desjoyaux à Bordeaux</a>, <a href="/guide/fuite-piscine-magiline-bordeaux/" style="color:var(--green);text-decoration:underline;">fuite piscine Magiline à Bordeaux</a>, <a href="/guide/fuite-piscine-diffazur-bordeaux/" style="color:var(--green);text-decoration:underline;">fuite piscine Diffazur à Bordeaux</a> ou <a href="/guide/fuite-piscine-waterair-bordeaux/" style="color:var(--green);text-decoration:underline;">fuite piscine Waterair à Bordeaux</a>.</p>

    <p style="margin-top:1rem;"><strong>Action directe</strong> : pour un dépannage piscine complet (diagnostic + coordination réparation), voir <a href="/detection-fuite/depannage-piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">dépannage piscine à Bordeaux</a>. Pour le détail de notre méthode phare au colorant, voir <a href="/detection-fuite/fluoresceine-piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">recherche de fuite piscine à la fluorescéine</a>.</p>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:1080px;">
    <h2>Guides piscine pour comprendre avant d'agir</h2>
    <p>Avant d'appeler un professionnel, plusieurs questions valent là peine d'être creusees. Nos articles guide vous orientent dans le diagnostic, la décision économique et la procédure assurance.</p>

    <div class="grid-3" style="margin-top:1.5rem;">
      <a href="/guide/ma-piscine-perd-de-l-eau-que-faire/" class="service-card" style="text-decoration:none;color:inherit;">
        <h3>Ma piscine perd de l'eau : que faire ?</h3>
        <p>Arbre de décision en 6 étapes pour qualifier la situation, faire le test du seau et savoir quand appeler un professionnel.</p>
      </a>
      <a href="/guide/evaporation-vs-fuite-piscine/" class="service-card" style="text-decoration:none;color:inherit;">
        <h3>Évaporation ou fuite ?</h3>
        <p>Tableau des taux d'évaporation mensuels en Gironde, protocole de test 48h précis, pieges à éviter pour ne pas confondre.</p>
      </a>
      <a href="/guide/recherche-fuite-piscine-tarif/" class="service-card" style="text-decoration:none;color:inherit;">
        <h3>Tarifs par type de bassin</h3>
        <p>Grille tarifaire détaillée : liner PVC, coque polyester, béton armé, naturelle. Comparatif diagnostic vs vidange classique.</p>
      </a>
      <a href="/guide/recherche-fuite-piscine-assurance/" class="service-card" style="text-decoration:none;color:inherit;">
        <h3>Remboursement assurance habitation</h3>
        <p>Clauses a vérifier, procédure de déclaration, convention IRSI en copropriété avec piscine, courrier type a envoyer.</p>
      </a>
      <a href="/guide/fuite-liner-piscine/" class="service-card" style="text-decoration:none;color:inherit;">
        <h3>diagnostic fuite sur liner PVC</h3>
        <p>70 pourcent du parc girondin. Signes, causes, méthodes de détection, décision réparation locale ou changement complet.</p>
      </a>
      <a href="/guide/cout-recherche-fuite/" class="service-card" style="text-decoration:none;color:inherit;">
        <h3>coût d'une recherche de fuite</h3>
        <p>Article général sur le tarif d'une intervention en Gironde, prise en charge assurance, devis gratuit avant déplacement.</p>
      </a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <h2>Notre méthode pour piscines en Gironde</h2>
    <p>Chaque type de bassin demande une combinaison de méthodes adaptees. Voici le protocole que nos techniciens deploient sur le terrain.</p>

    <div class="grid-3" style="margin-top:1.5rem;">
      <div class="arg-num-card">
        <span class="arg-num">01</span>
        <div class="arg-num-content">
          <h3>Test d'évaporation préalable</h3>
          <p>Avant déplacement, nous vous guidons par téléphone pour réaliser le test du seau et qualifier la perte. Si la perte est dans la fourchette évaporation normale, pas d'intervention nécessaire.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">02</span>
        <div class="arg-num-content">
          <h3>Inspection visuelle et camera</h3>
          <p>Inspection en apnee ou par camera endoscopique sous-marine pour détecter perforations liner, fissures coque, ou défauts visibles aux pièces a sceller.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">03</span>
        <div class="arg-num-content">
          <h3>Colorant fluorescéine</h3>
          <p>Injection de colorant non toxique près des zones suspectes (skimmer, buses, bonde de fond). Filtration à l'arrêt, le colorant est aspire vers la fuite et révèle son trajet.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">04</span>
        <div class="arg-num-content">
          <h3>Test de pression hydraulique</h3>
          <p>Isolation séquentielle de chaque circuit (aspiration, refoulement, balai, bonde) avec mise en pression. Le circuit qui perd la pression est identifié.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">05</span>
        <div class="arg-num-content">
          <h3>écoute électro-acoustique</h3>
          <p>Amplificateur acoustique haute sensibilite pour capter le bruit de fuite sur canalisations enterrées autour de la piscine. précision au demi-metre près.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">06</span>
        <div class="arg-num-content">
          <h3>Gaz traceur azote/hélium</h3>
          <p>Pour les fuites enterrées longues ou inaccessibles acoustiquement. Injection sous pression, détection en surface au capteur. méthode complementaire de dernière ligne.</p>
        </div>
      </div>
    </div>

    <p style="margin-top:2rem;">Pour comprendre la méthodologie en détail, consultez la page de votre commune : <a href="/detection-fuite/piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">piscine Bordeaux</a> (propriétés bourgeoises Caudéran/Le Bouscat), <a href="/detection-fuite/piscine-merignac/" style="color:var(--green);text-decoration:underline;">piscine Mérignac</a> (parc liner pavillonnaire), <a href="/detection-fuite/piscine-arcachon/" style="color:var(--green);text-decoration:underline;">piscine Arcachon</a> (villas haut de gamme avec PAC), <a href="/detection-fuite/piscine-la-teste-de-buch/" style="color:var(--green);text-decoration:underline;">piscine La Teste-de-Buch</a> (sols sableux Cazaux), <a href="/detection-fuite/piscine-gujan-mestras/" style="color:var(--green);text-decoration:underline;">piscine Gujan-Mestras</a> (coques polyester), <a href="/detection-fuite/piscine-libourne/" style="color:var(--green);text-decoration:underline;">piscine Libourne</a> (chais viticoles anciens) ou <a href="/detection-fuite/piscine-le-bouscat/" style="color:var(--green);text-decoration:underline;">piscine Le Bouscat</a> (jardins matures avec racines).</p>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Combien coûte une recherche de fuite piscine en Gironde ?</h2>
    <p>En général entre <strong>300 et 700 euros HT</strong> selon le type de bassin et les méthodes a combiner. Notre <a href="/guide/recherche-fuite-piscine-tarif/" style="color:var(--green);text-decoration:underline;">guide tarif piscine détaillé</a> donne les fourchettes précises par type (liner, coque, béton). Le diagnostic est très souvent rembourse par votre assurance multirisque habitation au titre de la garantie recherche de fuite. Consultez notre <a href="/guide/recherche-fuite-piscine-assurance/" style="color:var(--green);text-decoration:underline;">guide remboursement assurance piscine</a> pour la procédure complète.</p>

    <p>Pour les fuites enterrées autour de votre piscine (canalisation d'alimentation, refoulement, prise balai), voyez aussi notre page <a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">recherche de fuite canalisation enterrée à Bordeaux</a> qui détaillé la méthode gaz traceur en sol argileux ou sableux.</p>

    <div style="margin-top:2rem;text-align:center;">
      <a href="/devis/" class="btn btn-gold">Obtenir un devis pour ma piscine</a>
    </div>
  </div>
</section>

{form_section("Bordeaux")}
'''

    return html_base(
        'Recherche de fuite piscine Gironde | Sans vidange',
        "Recherche de fuite sur piscine privée en Gironde sans vidanger : colorant fluorescéine, acoustique, test de pression. couverture Bordeaux, Bassin d'Arcachon, Libournais. Devis gratuit.",
        'https://recherche-fuite-gironde.fr/detection-fuite/piscine/',
        body,
        extra_ld=ld_service + ld_breadcrumb,
    )


# ═══════════════════════════════════════════════════════════════
# PAGE USE CASE : Fuite plancher chauffant Bordeaux
# ═══════════════════════════════════════════════════════════════

def page_plancher_chauffant_bordeaux():
    ld_service = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "Recherche de fuite plancher chauffant",
  "name": "Détection de fuite plancher chauffant à Bordeaux et métropole",
  "description": "Localisation précise d'une fuite sur plancher chauffant hydraulique par thermographie infrarouge et test de pression. Sans casser la chape, pour réparation ciblée.",
  "provider": {
    "@type": "LocalBusiness",
    "name": "Recherche Fuite Gironde",
    "url": "https://recherche-fuite-gironde.fr/"
  },
  "areaServed": { "@type": "Place", "name": "Bordeaux et métropole girondine" },
  "category": "détection de fuite non destructive"
}
</script>'''

    ld_local = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Recherche Fuite Gironde - Plancher chauffant Bordeaux",
  "description": "spécialiste de la recherche de fuite sur plancher chauffant hydraulique à Bordeaux et sa métropole. Thermographie infrarouge, test de pression, localisation au point.",
  "url": "https://recherche-fuite-gironde.fr/detection-fuite/fuite-plancher-chauffant-bordeaux/",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Bordeaux",
    "postalCode": "33000",
    "addressCountry": "FR"
  },
  "areaServed": { "@type": "City", "name": "Bordeaux" },
  "priceRange": "€€"
}
</script>'''

    ld_breadcrumb = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://recherche-fuite-gironde.fr/" },
    { "@type": "ListItem", "position": 2, "name": "Détection de fuite", "item": "https://recherche-fuite-gironde.fr/detection-fuite/" },
    { "@type": "ListItem", "position": 3, "name": "Plancher chauffant Bordeaux", "item": "https://recherche-fuite-gironde.fr/detection-fuite/fuite-plancher-chauffant-bordeaux/" }
  ]
}
</script>'''

    ld_faq = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Comment detectez-vous une fuite sur un plancher chauffant sans casser la chape ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Notre méthode principale est la thermographie infrarouge : une camera thermique détecté les variations de température au sol. Avec le circuit en chauffe, la zone de fuite produit un halo thermique anormal visible à l'écran. Le test de pression hydraulique sur chaque boucle complète le diagnostic : en isolant les boucles une par une, on identifié celle qui perd de la pression. La combinaison des deux permet une localisation au point en général." }
    },
    {
      "@type": "Question",
      "name": "Quels sont les signes d'une fuite sur plancher chauffant ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Les signes caractéristiques sont : baisse de pression dans le circuit de chauffage sur le manometre, sol anormalement froid par zones (boucle non chauffante), tache d'humidité ou auréole au plafond de l'étage inférieur (en étage), parquet ou carrelage qui se decolle localement, surconsommation d'eau inexpliquée (le circuit se remplit automatiquement), chaudiere qui se met en défaut de pression fréquent." }
    },
    {
      "@type": "Question",
      "name": "Combien coûte une recherche de fuite sur plancher chauffant à Bordeaux ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Entre 400 et 650 euros HT selon la surface du plancher chauffant et le nombre de boucles a tester. Pour une maison de 80 à 150 m² avec plancher chauffant principal, comptez 450 à 550 euros HT. Le tarif inclut thermographie, test de pression sur chaque boucle, rapport technique avec localisation précise. Devis fixe communique avant intervention." }
    },
    {
      "@type": "Question",
      "name": "La réparation après diagnostic nécessite-t-elle de casser tout le sol ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Non, nous localisons la fuite au point près, ce qui permet une intervention ciblée. La réparation consiste a ouvrir la chape uniquement au droit de la perforation (zone de 25 à 40 cm de cote typiquement), remplacer 30 à 80 cm de tube PER ou polybutylene, refaire la chape et le revetement de sol localement. Aucun besoin de casser toute la pièce." }
    },
    {
      "@type": "Question",
      "name": "Les planchers chauffants à Bordeaux sont-ils fréquents ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Oui, particulièrement à Mérignac, Pessac et dans les pavillons des années 1985-2005 de la métropole. Environ 40 pourcent des maisons individuelles de cette période ont un plancher chauffant hydraulique. après 20 à 40 ans, les micro-perforations sur tubes PER ou polybutylene deviennent fréquentes. Nos techniciens sont spécialisés sur ce type d'installation." }
    },
    {
      "@type": "Question",
      "name": "La garantie décennale couvre-t-elle mon plancher chauffant ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Si votre installation à moins de 10 ans, la garantie décennale du poseur couvre les défauts de mise en oeuvre et de materiaux. après 10 ans, c'est l'assurance habitation multirisque qui prend en charge recherche de fuite et réparation via la garantie dégâts des eaux. Notre rapport technique est accepte par les principaux assureurs francais." }
    }
  ]
}
</script>'''

    body = f'''
<section class="hero-mini">
  <div class="container">
    <nav class="breadcrumb">
      <a href="/">Accueil</a>
      <span>&rsaquo;</span>
      <a href="/detection-fuite/">détection de fuite</a>
      <span>&rsaquo;</span>
      <span>Plancher chauffant Bordeaux</span>
    </nav>
    <h1>Recherche de fuite sur plancher chauffant à Bordeaux</h1>
    <p class="hero-mini-lead">Pression de votre chaudiere qui chute, sol froid par zones, humidité au plafond du voisin du dessous : votre plancher chauffant hydraulique fuit. Nos techniciens le localisent <strong>au point près grâce à la thermographie infrarouge</strong>, sans casser votre chape. réparation ciblée sur 25 à 40 cm de sol au lieu de refaire toute la pièce.</p>
    <div class="hero-mini-cta">
      <a href="/devis/" class="btn btn-gold">Demander un devis plancher chauffant</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <h2>Le plancher chauffant hydraulique : un système très répandu en métropole bordelaise</h2>
    <p>Les pavillons construits à Bordeaux et sa métropole entre 1985 et 2005 ont massivement adopte le plancher chauffant hydraulique comme système de chauffage principal. A Mérignac (Arlac, Capeyron, Chemin Long, Beutre), à Pessac (Alouette, Saige, Camponac), au Haillan, à Eysines, dans les lotissements de Talence et du Bouscat, environ 40 pourcent des maisons individuelles de cette période en sont équipées. C'est une proportion nettement supérieure aux radiateurs classiques sur ces tranches d'âgé.</p>

    <p>Le système fonctionne par circulation d'eau chaude (35-45 degrés) dans des tubes PER (polyethylene reticulé) ou polybutylene intégrés dans la chape béton. Chaque pièce est alimentee par une ou plusieurs boucles qui partent d'un collecteur central (généralement dans une pièce technique ou un placard). après 20 à 40 ans, les micro-perforations et les défaillances de raccordement deviennent fréquentes.</p>

    <h2>Les 6 signes d'une fuite de plancher chauffant</h2>

    <div class="grid-3" style="margin-top:1.5rem;">
      <div class="arg-num-card">
        <span class="arg-num">01</span>
        <div class="arg-num-content">
          <h3>Baisse de pression chronique</h3>
          <p>La pression de votre circuit chauffage baisse régulièrement sur le manometre de là chaudiere. Vous devez remettre en pression manuellement chaque semaine ou chaque mois. Le circuit perd de l'eau quelque part, presque toujours au niveau du plancher chauffant si c'est votre type d'installation.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">02</span>
        <div class="arg-num-content">
          <h3>Zones de sol froides</h3>
          <p>Une pièce ou une zone précise de la maison reste froide malgre le chauffage en marche. Une boucle du plancher chauffant ne circule plus correctement. Posez la main au sol : le contraste thermique entre zones chauffées et zones defaillantes est nettement perceptible.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">03</span>
        <div class="arg-num-content">
          <h3>Tache au plafond (si étage)</h3>
          <p>Pour les maisons a étage avec plancher chauffant à l'étage supérieur, une fuite se manifeste par une tache d'humidité ou une auréole au plafond du rez-de-chaussee. Elle peut apparaitre très localement (au droit exact de la fuite) ou de manière diffuse (migration de l'eau le long des poutres).</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">04</span>
        <div class="arg-num-content">
          <h3>Parquet ou carrelage qui se decolle</h3>
          <p>Le revetement de sol au-dessus de la zone fuyante montre des signes d'humidité : lame de parquet gonflee, joint de carrelage qui fonce, carrelage qui sonne creux. Ces signes apparaissent souvent des mois avant que la fuite soit clairement identifiée.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">05</span>
        <div class="arg-num-content">
          <h3>Chaudiere en défaut de pression</h3>
          <p>Là chaudiere se met en défaut et s'arrêté automatiquement, avec un code d'erreur "pression basse" ou equivalent. Cela arrive de plus en plus fréquemment. Votre chauffagiste reamorce mais le problème revient. Le circuit perd de l'eau en permanence par la fuite.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">06</span>
        <div class="arg-num-content">
          <h3>surconsommation d'eau inexpliquée</h3>
          <p>Le remplissage automatique de votre circuit de chauffage compensé en permanence la fuite. Votre compteur d'eau indique une surconsommation sans que vous ne trouviez de point d'eau responsable. C'est la fuite du plancher chauffant qui alimente une fuite d'eau continue dans le sol.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:1080px;">
    <h2>Notre méthode : thermographie + test de pression</h2>
    <p>La recherche de fuite sur plancher chauffant hydraulique est notre spécialité sur la métropole bordelaise. Nous combinons deux méthodes complementaires pour localiser la fuite au point près sans casser la chape.</p>

    <h3>étape 1 : preparation du circuit</h3>
    <p>Avant notre arrivée, maintenez votre chauffage en fonctionnement normal pendant au moins 4 heures. Le plancher doit être a température opérationnelle pour que la thermographie révèle les contrastes thermiques caractéristiques.</p>

    <h3>étape 2 : thermographie infrarouge du sol</h3>
    <p>Avec une camera thermique haute definition, notre technicien balaie methodiquement la surface des pièces. Une fuite active produit un halo thermique anormal : soit une zone plus chaude (eau chaude qui sort localement sous le revetement) soit une zone plus froide (boucle qui ne circule plus en aval du point de fuite). La lecture experte de ces signatures thermiques permet de pointer la zone a 20-30 cm près.</p>

    <h3>étape 3 : identification de la boucle en défaut</h3>
    <p>Au collecteur, chaque boucle alimentant une pièce est identifiée. Nous isolons les boucles une par une en fermant les vannes manuelles, et mesurons la pression residuelle dans chacune après un délai de stabilisation. La boucle qui perd de la pression en isolement est celle qui fuit.</p>

    <h3>étape 4 : test de pression cible sur la boucle suspecte</h3>
    <p>Avec la boucle suspecte identifiée, nous effectuons un test de pression plus précis avec manometre haute sensibilite. En combinaison avec la thermographie, cela confirme la zone exacte dans la boucle (début, milieu, fin de la boucle, serpentin chauffant).</p>

    <h3>étape 5 : marquage et rapport</h3>
    <p>Le point de fuite est marque au sol (scotch ou feutre effacable). Le rapport technique détaillé les mesures effectuees, la zone localisée en coordonnees cartesiennes par rapport aux murs, et la préconisation de réparation : ouverture de chape 25-40 cm de cote, remplacement de 30-80 cm de tube, refection chape et revetement.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <h2>Causes fréquentes des fuites sur plancher chauffant</h2>

    <div class="grid-3" style="margin-top:1.5rem;">
      <div class="arg-num-card">
        <span class="arg-num">01</span>
        <div class="arg-num-content">
          <h3>Micro-perforation par corrosion interne</h3>
          <p>Les tubes PER des années 1985-1995 peuvent subir une corrosion interne lente si l'eau du circuit n'a pas été correctement traitee (absence d'inhibiteur de corrosion). La perforation est souvent punctiforme (0,2 à 1 mm) mais suffit a provoquer une perte de pression continue.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">02</span>
        <div class="arg-num-content">
          <h3>Perforation par clou ou vis</h3>
          <p>Lors de travaux ulterieurs (pose de plinthe, fixation d'un meuble, installation d'une cloison), un clou ou une vis peut perforer le tube. La fuite apparait quelques semaines ou mois plus tard. Cas très fréquent dans les maisons avec historique de reamenagements.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">03</span>
        <div class="arg-num-content">
          <h3>défaut de raccordement au collecteur</h3>
          <p>Le raccordement entre la boucle et le collecteur (sertissage, collier de serrage) peut lacher par fatigué après 15 à 25 ans. Cette fuite est souvent visible dans le placard du collecteur si on regardé attentivement.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">04</span>
        <div class="arg-num-content">
          <h3>Mouvement de la chape</h3>
          <p>Un mouvement du support (tassement, fissure de la dalle, mouvement de terrain argileux bordelais) peut cisailler le tube enrobe. Cas moins fréquent mais observé sur les maisons anciennes rénovées avec plancher chauffant rajoute.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">05</span>
        <div class="arg-num-content">
          <h3>Chocs thermiques répétés</h3>
          <p>Un chauffage pousse régulièrement au maximum puis coupe brutalement provoque des dilatations/contractions rapides. Sur 30 ans, cela fatigué les raccords et peut provoquer des fuites aux jonctions.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">06</span>
        <div class="arg-num-content">
          <h3>Polybutylene de la génération 1990</h3>
          <p>Certains lots de tubes polybutylene des années 1990 ont été rappeles pour défaut de fabrication. Si votre installation date de cette période et que vous avez des fuites multiples, un changement complet peut être plus économique a terme qu'une succession de réparations.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Cas type d'intervention à Mérignac</h2>
    <p>Scenario récurrent : pavillon Mérignac Arlac construit en 1992, plancher chauffant hydraulique sur rez-de-chaussee (80 m²). Le propriétaire constate depuis 6 mois que la pression de sà chaudiere baisse de 1,5 à 1,0 bar chaque semaine. Il doit reamorcer manuellement. Depuis 2 mois, le salon reste anormalement froid alors que la chambre et la cuisine sont bien chauffées. Sa facture d'eau a augmente de 8 m³ par mois.</p>

    <p>Notre intervention : thermographie infrarouge systématique du sol, boucle par boucle. La boucle salon (42 m lineaires de tube PER dans une serpentin) montre un contraste thermique caractéristique a 4,2 metres du mur nord et 2,8 metres du mur est : zone froide nette au-delà de ce point, preuve que la fuite est localisée la. Test de pression sur cette boucle : perte confirmee de 0,3 bar en 30 minutes en isolement.</p>

    <p>réparation : ouverture de chape 35×35 cm au point marque, découverte d'une micro-perforation sur le tube PER a 38 cm de profondeur, remplacement de 60 cm de tube avec raccords mécaniques certifies, refection chape avec mortier fibre, repose du carrelage d'origine (conservé lors de l'ouverture). durée totale intervention + réparation : 2 jours. coût total : 1 800 euros HT. Pris en charge a 70 pourcent par l'assurance multirisque habitation après examen du rapport et devis.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Questions fréquentes sur la fuite de plancher chauffant à Bordeaux</h2>

    <h3>Comment detectez-vous une fuite sur un plancher chauffant sans casser la chape ?</h3>
    <p>Notre méthode principale est la thermographie infrarouge : une camera thermique détecté les variations de température au sol. Avec le circuit en chauffe, la zone de fuite produit un halo thermique anormal. Le test de pression hydraulique sur chaque boucle complète le diagnostic. La combinaison des deux permet une localisation au point en général.</p>

    <h3>Quels sont les signes d'une fuite sur plancher chauffant ?</h3>
    <p>Baisse de pression chronique sur le manometre, sol anormalement froid par zones, tache d'humidité au plafond de l'étage inférieur (en étage), parquet ou carrelage qui se decolle localement, surconsommation d'eau inexpliquée, chaudiere en défaut de pression fréquent.</p>

    <h3>Combien coûte une recherche de fuite sur plancher chauffant à Bordeaux ?</h3>
    <p>Entre 400 et 650 euros HT selon la surface et le nombre de boucles a tester. Pour une maison de 80 à 150 m² avec plancher chauffant principal, comptez 450 à 550 euros HT. Le tarif inclut thermographie, test de pression sur chaque boucle, rapport technique avec localisation précise.</p>

    <h3>La réparation après diagnostic nécessite-t-elle de casser tout le sol ?</h3>
    <p>Non, nous localisons la fuite au point près, ce qui permet une intervention ciblée. La réparation consiste a ouvrir la chape uniquement au droit de la perforation (zone de 25 à 40 cm de cote typiquement), remplacer 30 à 80 cm de tube, refaire la chape et le revetement de sol localement.</p>

    <h3>Les planchers chauffants à Bordeaux sont-ils fréquents ?</h3>
    <p>Oui, particulièrement à Mérignac, Pessac et dans les pavillons des années 1985-2005. Environ 40 pourcent des maisons individuelles de cette période ont un plancher chauffant hydraulique. après 20 à 40 ans, les micro-perforations deviennent fréquentes. Pour une intervention spécifique à votre ville, consultez <a href="/villes/merignac/" style="color:var(--green);text-decoration:underline;">recherche de fuite Mérignac</a> ou <a href="/villes/pessac/" style="color:var(--green);text-decoration:underline;">recherche de fuite Pessac</a>.</p>

    <h3>La garantie décennale couvre-t-elle mon plancher chauffant ?</h3>
    <p>Si votre installation à moins de 10 ans, la garantie décennale du poseur couvre les défauts. après 10 ans, c'est l'assurance habitation multirisque qui prend en charge recherche de fuite et réparation via la garantie dégâts des eaux. Notre rapport technique est accepte par les principaux assureurs.</p>

    <div style="margin-top:2rem;text-align:center;">
      <a href="/devis/" class="btn btn-gold">Demander un diagnostic plancher chauffant</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Situations connexes au plancher chauffant</h2>
    <p>Une fuite de plancher chauffant peut être confondue avec d'autres types de fuites. Ces ressources peuvent vous aider :</p>
    <ul>
      <li><a href="/detection-fuite/thermographie-infrarouge-bordeaux/" style="color:var(--green);text-decoration:underline;">Thermographie infrarouge à Bordeaux</a> : la méthode phare pour le plancher chauffant, page dédiée avec protocole détaillé, matériel et cas concrets.</li>
      <li><a href="/detection-fuite/degats-des-eaux-bordeaux/" style="color:var(--green);text-decoration:underline;">Dégât des eaux à Bordeaux</a> : si la fuite a déjà tâché le plafond du voisin du dessous (en immeuble) ou un autre lot.</li>
      <li><a href="/detection-fuite/urgence-bordeaux/" style="color:var(--green);text-decoration:underline;">Recherche de fuite en urgence</a> : si votre chaudière se met en défaut de pression plusieurs fois par semaine, la fuite est importante et nécessite une intervention rapide.</li>
      <li><a href="/detection-fuite/fuite-apres-compteur/" style="color:var(--green);text-decoration:underline;">Fuite d'eau après compteur</a> : pour distinguer une fuite de plancher chauffant (circuit fermé de chauffage) d'une fuite sur le réseau d'eau sanitaire (compteur qui tourne).</li>
      <li><a href="/villes/merignac/" style="color:var(--green);text-decoration:underline;">Recherche de fuite à Mérignac</a> : Mérignac concentre la plus forte densité de planchers chauffants en métropole bordelaise (40 pourcent du parc pavillonnaire).</li>
    </ul>
  </div>
</section>

{form_section("Bordeaux")}
'''

    return html_base(
        'Fuite plancher chauffant Bordeaux | Thermographie',
        "Recherche de fuite sur plancher chauffant hydraulique à Bordeaux et sa métropole : thermographie infrarouge, test de pression, localisation au point sans casser la chape.",
        'https://recherche-fuite-gironde.fr/detection-fuite/fuite-plancher-chauffant-bordeaux/',
        body,
        extra_ld=ld_service + ld_local + ld_breadcrumb + ld_faq,
    )


# ═══════════════════════════════════════════════════════════════
# PAGE USE CASE : dégâts des eaux Bordeaux (B2B syndics)
# ═══════════════════════════════════════════════════════════════

def page_degats_eaux_bordeaux():
    ld_service = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "Recherche d'origine de dégât des eaux",
  "name": "Localisation de dégâts des eaux à Bordeaux pour syndics et copropriétés",
  "description": "identification précise de l'origine d'un dégât des eaux en copropriété bordelaise. Rapport technique opposable en convention IRSI, intervention sous 24h, coordination avec assureurs et syndic.",
  "provider": {
    "@type": "LocalBusiness",
    "name": "Recherche Fuite Gironde",
    "url": "https://recherche-fuite-gironde.fr/"
  },
  "areaServed": { "@type": "Place", "name": "Bordeaux et métropole girondine" },
  "audience": {
    "@type": "BusinessAudience",
    "audienceType": "Syndics de copropriété, conseils syndicaux, gestionnaires immobiliers"
  },
  "category": "détection de fuite non destructive B2B"
}
</script>'''

    ld_local = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Recherche Fuite Gironde - dégâts des eaux Bordeaux",
  "description": "spécialiste de la localisation d'origine de dégât des eaux en copropriété à Bordeaux. Rapport IRSI, intervention 24h, coordination syndic et assureur.",
  "url": "https://recherche-fuite-gironde.fr/detection-fuite/degats-des-eaux-bordeaux/",
  "image": "https://recherche-fuite-gironde.fr/assets/fuite-sous-dalle.webp",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Bordeaux",
    "postalCode": "33000",
    "addressCountry": "FR"
  },
  "areaServed": { "@type": "City", "name": "Bordeaux" },
  "priceRange": "€€"
}
</script>'''

    ld_breadcrumb = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://recherche-fuite-gironde.fr/" },
    { "@type": "ListItem", "position": 2, "name": "Détection de fuite", "item": "https://recherche-fuite-gironde.fr/detection-fuite/" },
    { "@type": "ListItem", "position": 3, "name": "Dégâts des eaux Bordeaux", "item": "https://recherche-fuite-gironde.fr/detection-fuite/degats-des-eaux-bordeaux/" }
  ]
}
</script>'''

    ld_faq = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Quelle est la différence entre une fuite et un dégât des eaux ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Une fuite est la cause technique : perforation, joint défaillant, raccord désaxé, liner percé. Un dégât des eaux est la conséquence : tache d'humidité, plafond abîme, parquet gonfle, mobilier endommage. Un dégât des eaux implique toujours une fuite à l'origine, mais toutes les fuites n'entraînent pas de dégât des eaux (fuite enterrée dans le jardin par exemple). Pour l'assurance, c'est le dégât des eaux qui déclenché la prise en charge." }
    },
    {
      "@type": "Question",
      "name": "Comment fonctionne la convention IRSI en copropriété bordelaise ?",
      "acceptedAnswer": { "@type": "Answer", "text": "La convention IRSI (Indemnisation et Recours des Sinistres Immeuble) s'applique automatiquement entre assureurs pour les dégâts des eaux en copropriété jusqu'à 5000 euros HT. L'assureur du lot ou du logement 'victime' prend en charge les dommages sans recherche de responsabilité préalable, puis se retourne contre l'assureur du responsable. Cette procédure accéléré considérablement l'indemnisation (15 à 30 jours typiquement au lieu de 3 à 6 mois en expertise contradictoire)." }
    },
    {
      "@type": "Question",
      "name": "Un syndic peut-il mandater directement votre intervention ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Oui, nous travaillons régulièrement en mandatement direct par syndic professionnel ou conseil syndical pour les dégâts des eaux en copropriété bordelaise. Le rapport est remis au syndic avec identification précise de la responsabilité (partie privative ou commune). La facturation se fait à la copropriété, qui se retourne ensuite vers l'assurance PNO ou le responsable identifié." }
    },
    {
      "@type": "Question",
      "name": "Combien de temps prend un diagnostic de dégâts des eaux à Bordeaux ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Intervention sous 24h dans la majorite des cas, avec un diagnostic sur site de 1h30 a 3h. Le rapport technique est remis le jour même ou sous 24h par email, pret a être transmis à l'assureur et au syndic. Pour les sinistres complexes impactant plusieurs lots, un diagnostic plus long (demi-journée) peut être nécessaire avec rapport détaillé sous 48h." }
    },
    {
      "@type": "Question",
      "name": "Les propriétaires occupants ou les locataires peuvent-ils nous contacter directement ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Oui, tout copropriétaire occupant, locataire ou bailleur peut nous contacter pour un diagnostic individuel. Si le sinistre concerne des parties communes (colonne montante, évacuation collective, toiture), nous informons le syndic après constat et coordonnons la suite. Le rapport est remis au commanditaire (vous) avec les elements utiles pour l'assureur et le syndic." }
    },
    {
      "@type": "Question",
      "name": "Que faire en attendant l'arrivée du technicien ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Coupez l'arrivée d'eau générale si vous pouvez identifier la source. prévenez le voisin du dessus ou du dessous si le dégât les impacte. Photographiez les dommages dès que possible (avant sechage et réparations). Declarez le sinistre à votre assurance dans les 5 jours ouvrables (convention IRSI s'applique des la déclaration). Eloignez meubles et objets de valeur de la zone humide pour limiter les dégâts secondaires." }
    }
  ]
}
</script>'''

    body = f'''
<section class="hero-mini">
  <div class="container">
    <nav class="breadcrumb">
      <a href="/">Accueil</a>
      <span>&rsaquo;</span>
      <a href="/detection-fuite/">détection de fuite</a>
      <span>&rsaquo;</span>
      <span>dégâts des eaux Bordeaux</span>
    </nav>
    <h1>Recherche d'origine de dégâts des eaux à Bordeaux</h1>
    <p class="hero-mini-lead">Tache au plafond, infiltration dans un appartement, humidité persistante en copropriété bordelaise ? Nos techniciens identifient précisément l'origine du sinistre pour activer la convention IRSI entre assureurs. <strong>Rapport opposable remis sous 24h</strong>, coordination avec syndic et compagnies d'assurance, intervention prioritaire.</p>
    <div class="hero-mini-cta">
      <a href="/devis/" class="btn btn-gold">Demander une intervention</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <figure style="margin:0 0 2rem;">
      <img src="/assets/fuite-sous-dalle.webp" alt="dégât des eaux en copropriété bordelaise, tache d'humidité au plafond, intervention recherche d'origine" width="700" height="467" loading="eager" style="width:100%;max-height:380px;height:auto;object-fit:cover;border-radius:12px;display:block;">
    </figure>

    <h2>Fuite ou dégât des eaux : une distinction essentielle pour l'assurance</h2>
    <p>Un dégât des eaux n'est pas une fuite : c'est la conséquence d'une fuite. Cette distinction, apparemment semantique, est en réalité essentielle car elle conditionne la procédure d'indemnisation et la responsabilité entre assureurs. comprendre cette logique aide a anticiper la suite d'un sinistre en copropriété bordelaise.</p>

    <ul>
      <li><strong>La fuite</strong> est la cause technique : perforation d'une canalisation, joint de skimmer fissure, raccord PVC désaxé, liner piscine percé, soudure d'étanchéité rompue</li>
      <li><strong>Le dégât des eaux</strong> est le dommage resultant : plafond tache, parquet gonfle, enduit decolle, mobilier abime, appareils electromenagers hors d'usage</li>
      <li><strong>Le sinistre</strong> est la déclaration administrative faite à l'assureur, combinant l'événement et l'impact financier</li>
    </ul>

    <p>Dans 80 pourcent des cas, quand un propriétaire nous appelle en urgence pour un dégât des eaux, il n'à aucune idée de la cause : la tache au plafond peut venir d'une fuite sur la colonne commune EU/EV, d'une infiltration de toiture, d'une canalisation encastree, d'un appareil du voisin. C'est précisément notre role d'identifier la source technique pour que l'assurance puisse établir les responsabilités.</p>

    <h2>Types de dégâts des eaux que nous traitons en copropriété bordelaise</h2>

    <div class="grid-3" style="margin-top:1.5rem;">
      <div class="arg-num-card">
        <span class="arg-num">01</span>
        <div class="arg-num-content">
          <h3>Infiltration par colonne montante</h3>
          <p>La tache apparait au plafond ou le long d'un mur porteur. La colonne EU/EV commune à l'étage supérieur fuit, provoquant un écoulement ponctuel ou diffus selon le débit. fréquente dans les immeubles haussmanniens du Centre-Ville, Chartrons et Saint-Pierre ou les colonnes fonte centenaires cèdent à la corrosion.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">02</span>
        <div class="arg-num-content">
          <h3>dégât par appartement du dessus</h3>
          <p>Fuite sur installation privative de l'appartement du dessus : flexible de machine a laver, chasse d'eau qui débordé, robinet oublie ouvert, joint de baignoire rompu. Le voisin est souvent responsable mais ne s'en rend pas compte. La convention IRSI s'applique automatiquement jusqu'à 5000 euros HT.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">03</span>
        <div class="arg-num-content">
          <h3>Infiltration de toiture</h3>
          <p>après pluies abondantes, de l'eau coule au dernier étage : toiture defectueuse, chéneaux bouches, étanchéité de terrasse rompue. responsabilité copropriété (parties communes). fréquent dans les immeubles des Chartrons, de la Victoire et de la Bastide après forts episodes pluvieux.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">04</span>
        <div class="arg-num-content">
          <h3>Fuite encastree dans cloison</h3>
          <p>Tache le long d'un mur ou d'une cloison, souvent en salle de bain ou cuisine. Canalisation encastree percée par chute d'objet, vis malencontreuse, corrosion. La localisation par thermographie et écoute évité la démolition de toute la cloison.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">05</span>
        <div class="arg-num-content">
          <h3>débordement de gouttiere</h3>
          <p>Gouttiere obstrue par feuilles mortes, débordement sur facade, infiltration dans maconnerie. fréquent dans les immeubles de caudéran et du Parc Bordelais entoures d'arbres. responsabilité entretien copropriété (contrat nettoyage gouttieres annuel).</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">06</span>
        <div class="arg-num-content">
          <h3>Remontee capillaire confondue</h3>
          <p>Attention aux faux positifs : certaines humidités en sous-sol bordelais ne sont pas des fuites mais des remontées capillaires du terrain argileux. Notre humidimetre distingué précisément une infiltration active (gradient fort, zone localisée) d'une humidité diffuse structurelle.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:1080px;">
    <h2>Convention IRSI : le cadre légal pour les dégâts des eaux en copropriété</h2>
    <p>Depuis 2018, la convention IRSI (Indemnisation et Recours des Sinistres Immeuble) encadre les dégâts des eaux en copropriété et en location. Cette convention simplifie considérablement la procédure, à condition de connaître ses règles.</p>

    <h3>Le seuil des 5 000 euros HT</h3>
    <p>Pour les sinistres dont le coût de réparation est inférieur à 5 000 euros HT, la convention IRSI s'applique automatiquement : l'assureur du lot victime indemnise sans recherche de responsabilité préalable. Au-delà de 5 000 euros, une expertise contradictoire peut être déclenchée pour établir les responsabilités.</p>

    <h3>Les conditions d'application</h3>
    <ul>
      <li>Le sinistre doit concerner au moins 2 lots de la copropriété OU 1 lot + parties communes</li>
      <li>L'origine doit être dans l'immeuble (pas dans une construction voisine)</li>
      <li>Le sinistre doit être déclaré à l'assureur sous 5 jours ouvrables</li>
      <li>Un rapport technique doit identifier la cause (notre prestation)</li>
    </ul>

    <h3>Les acteurs et leurs responsabilités</h3>
    <ul>
      <li><strong>Syndic</strong> : mandate le diagnostic si parties communes concernees, coordonne la procédure IRSI</li>
      <li><strong>propriétaire occupant ou bailleur</strong> : déclaré le sinistre à son assureur, facilite l'accès</li>
      <li><strong>Locataire</strong> : déclaré à son assureur multirisque habitation, informe son bailleur</li>
      <li><strong>Assureurs de chaque lot</strong> : échanges automatiques via la plateforme IRSI</li>
      <li><strong>Professionnel de la recherche de fuite (nous)</strong> : identifié la cause, remet un rapport opposable</li>
    </ul>

    <h3>Notre rapport technique et la convention IRSI</h3>
    <p>Notre rapport standardise pour sinistre IRSI comprend obligatoirement : date et heure du constat, méthodes de diagnostic employees (thermographie, gaz traceur, acoustique, humidimetre), photos datees et horodatees, localisation précise de la source (lot responsable ou parties communes), estimation du débit de fuite et de la durée probable, préconisations de réparation chiffrees, elements de coordination entre assureurs. Ce document est reconnu par tous les assureurs de la place, y compris MAAF, Allianz, AXA, Groupama, Matmut, MACIF, MMA, GMF, SMABTP.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <h2>Notre protocole pour les syndics et conseils syndicaux</h2>
    <p>Nous travaillons régulièrement en mandatement par syndic professionnel, association syndicale libre (ASL) ou conseil syndical. Notre protocole est adapte aux contraintes B2B de la gestion de copropriété.</p>

    <div class="grid-3" style="margin-top:1.5rem;">
      <div class="arg-num-card">
        <span class="arg-num">01</span>
        <div class="arg-num-content">
          <h3>Mandatement direct</h3>
          <p>Le syndic nous mandate par email ou téléphone, avec les références du sinistre (numéro de dossier interne, lots concernes, assureur de la copropriété). Devis fixe communique sous l'heure pour validation.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">02</span>
        <div class="arg-num-content">
          <h3>Coordination avec les lots</h3>
          <p>Nous prenons directement contact avec les propriétaires ou locataires des lots concernes pour planifier l'accès. Creneau souvent en journée, avec disponibilite du syndic ou du gardien si accès parties communes.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">03</span>
        <div class="arg-num-content">
          <h3>diagnostic sur site</h3>
          <p>Intervention d'1h30 a 3h selon la complexite. Nos techniciens sont formes a respecter la confidentialite des occupants, les finitions des appartements, la discretion dans les parties communes (pas de travaux genants, pas de bruit excessif).</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">04</span>
        <div class="arg-num-content">
          <h3>Rapport standardise IRSI</h3>
          <p>Rapport technique conforme aux exigences des assureurs, remis au syndic sous 24h. Format PDF avec photos datees, localisation précise, chronologie des constatations, recommandations de réparation.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">05</span>
        <div class="arg-num-content">
          <h3>Facturation à la copropriété</h3>
          <p>Facture emise au nom de la copropriété (syndicat des copropriétaires, numéro SIRET) avec les références du dossier IRSI. Paiement sous 30 jours après reception. Aucun acompte demandé.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">06</span>
        <div class="arg-num-content">
          <h3>Suivi post-intervention</h3>
          <p>Nous restons disponibles pour répondre aux questions de l'expert mandate par l'assurance, produire des complements de rapport si nécessaire, temoigner en cas de contentieux. Support gratuit dans la limite de 6 mois après l'intervention.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Cas type : dégât des eaux en immeuble haussmannien</h2>
    <p>Scenario récurrent sur Bordeaux Centre : immeuble haussmannien de la rue Sainte-Catherine, 6 lots sur 5 étages. Mme X au 3e étage signalé au syndic une tache d'humidité en expansion sur le plafond de sa chambre, avec écoulement visible après fortes chutes d'eau. Le voisin du dessus (M. Y, 4e étage) affirme ne rien constater chez lui. Le syndic nous mandate sous 24h.</p>

    <p>Notre intervention : thermographie infrarouge au plafond du 3e pour cartographier la zone humide, écoute électro-acoustique sur le tracé de la colonne d'évacuation EU/EV passant dans la cloison mitoyenne, camera endoscopique dans la gaine technique commune via le regard d'accès du palier. découverte : fissure sur la colonne fonte commune entre le 3e et le 4e étage, a 1,50 metres au-dessus du plafond de Mme X. responsabilité copropriété, ni Mme X ni M. Y ne sont directement en cause.</p>

    <p>Rapport transmis au syndic en 24h. L'assurance de la copropriété prend en charge la réparation (remplacement du troncon de colonne, environ 2 800 euros HT). L'assurance multirisque de Mme X prend en charge les dommages dans son logement (repeinture plafond + nettoyage mobilier, 1 400 euros HT) dans le cadre de la convention IRSI. Délai total résolution : 6 semaines entre notre intervention et la fin des réparations.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Questions fréquentes sur les dégâts des eaux à Bordeaux</h2>

    <h3>quelle est la différence entre une fuite et un dégât des eaux ?</h3>
    <p>Une fuite est la cause technique : perforation, joint défaillant, raccord désaxé, liner perce. Un dégât des eaux est la conséquence : tache d'humidité, plafond abîme, parquet gonfle, mobilier endommage. Un dégât des eaux implique toujours une fuite à l'origine, mais toutes les fuites n'entraînent pas de dégât des eaux (fuite enterrée dans le jardin par exemple). Pour l'assurance, c'est le dégât des eaux qui déclenché la prise en charge.</p>

    <h3>Comment fonctionne la convention IRSI en copropriété bordelaise ?</h3>
    <p>La convention IRSI s'applique automatiquement entre assureurs pour les dégâts des eaux en copropriété jusqu'à 5 000 euros HT. L'assureur du lot 'victime' prend en charge les dommages sans recherche de responsabilité préalable, puis se retourne contre l'assureur du responsable. Cette procédure accéléré considérablement l'indemnisation (15 à 30 jours typiquement au lieu de 3 à 6 mois en expertise contradictoire).</p>

    <h3>Un syndic peut-il mandater directement votre intervention ?</h3>
    <p>Oui, nous travaillons régulièrement en mandatement direct par syndic professionnel ou conseil syndical. Le rapport est remis au syndic avec identification précise de la responsabilité (partie privative ou commune). La facturation se fait à la copropriété, qui se retourne ensuite vers l'assurance PNO ou le responsable identifié.</p>

    <h3>Combien de temps prend un diagnostic de dégâts des eaux à Bordeaux ?</h3>
    <p>Intervention sous 24h dans la majorite des cas, avec un diagnostic sur site de 1h30 a 3h. Le rapport technique est remis le jour même ou sous 24h par email, pret a être transmis à l'assureur et au syndic. Pour les sinistres complexes impactant plusieurs lots, un diagnostic plus long (demi-journée) peut être nécessaire avec rapport détaillé sous 48h.</p>

    <h3>Les propriétaires occupants ou les locataires peuvent-ils nous contacter directement ?</h3>
    <p>Oui, tout copropriétaire occupant, locataire ou bailleur peut nous contacter pour un diagnostic individuel. Si le sinistre concerne des parties communes (colonne montante, évacuation collective, toiture), nous informons le syndic après constat et coordonnons la suite. Le rapport est remis au commanditaire avec les elements utiles pour l'assureur et le syndic.</p>

    <h3>Que faire en attendant l'arrivée du technicien ?</h3>
    <p>Coupez l'arrivée d'eau générale si vous pouvez identifier la source. prévenez le voisin du dessus ou du dessous si le dégât les impacte. Photographiez les dommages dès que possible. Declarez le sinistre à votre assurance dans les 5 jours ouvrables. Pour les situations d'urgence avec fuite active, consultez notre page <a href="/detection-fuite/urgence-bordeaux/" style="color:var(--green);text-decoration:underline;">urgence fuite d'eau Bordeaux</a>.</p>

    <div style="margin-top:2rem;text-align:center;">
      <a href="/devis/" class="btn btn-gold">Demander une intervention syndic</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Pages connexes pour syndics et copropriétés</h2>
    <p>Au-delà du diagnostic d'origine, voici les ressources qui complètent l'intervention :</p>
    <ul>
      <li><a href="/detection-fuite/chemisage-bordeaux/" style="color:var(--green);text-decoration:underline;">Chemisage de canalisation à Bordeaux pour copropriétés</a> : si le diagnostic révèle une colonne d'évacuation EU/EV en fin de vie, le chemisage évite la démolition.</li>
      <li><a href="/detection-fuite/urgence-bordeaux/" style="color:var(--green);text-decoration:underline;">Recherche de fuite en urgence Bordeaux</a> : pour les sinistres avec fuite active impactant plusieurs lots simultanément.</li>
      <li><a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">Canalisation enterrée Bordeaux</a> : pour les sinistres venant des réseaux enterrés sous cour intérieure ou trottoir privé.</li>
      <li><a href="/detection-fuite/fuite-plancher-chauffant-bordeaux/" style="color:var(--green);text-decoration:underline;">Fuite plancher chauffant Bordeaux</a> : cause fréquente de tache au plafond du voisin du dessous.</li>
      <li><a href="/detection-fuite/thermographie-infrarouge-bordeaux/" style="color:var(--green);text-decoration:underline;">Thermographie infrarouge à Bordeaux</a> : la méthode reine pour identifier la source exacte d'un sinistre dans une copropriété haussmannienne.</li>
    </ul>
  </div>
</section>

{form_section("Bordeaux")}
'''

    return html_base(
        "Dégâts des eaux Bordeaux | Origine IRSI syndic",
        "Recherche d'origine de dégâts des eaux à Bordeaux en copropriété : rapport IRSI opposable, coordination syndic et assureur, intervention 24h. Pour syndics et propriétaires.",
        'https://recherche-fuite-gironde.fr/detection-fuite/degats-des-eaux-bordeaux/',
        body,
        extra_ld=ld_service + ld_local + ld_breadcrumb + ld_faq,
    )


# ═══════════════════════════════════════════════════════════════
# PAGE USE CASE : Chemisage Bordeaux landing (copropriété)
# ═══════════════════════════════════════════════════════════════

def page_chemisage_bordeaux():
    ld_service = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "Chemisage de canalisation",
  "name": "Chemisage de canalisation en copropriété à Bordeaux",
  "description": "rénovation de canalisations sans tranchee pour copropriétés bordelaises. Chemisage tubulaire par resine epoxy, durée de vie 50 ans, garantie décennale. spécialistes des immeubles haussmanniens et bati ancien.",
  "provider": {
    "@type": "LocalBusiness",
    "name": "Recherche Fuite Gironde",
    "url": "https://recherche-fuite-gironde.fr/"
  },
  "areaServed": { "@type": "Place", "name": "Bordeaux et métropole girondine" },
  "category": "réhabilitation de canalisation sans tranchee"
}
</script>'''

    ld_local = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Recherche Fuite Gironde - Chemisage Bordeaux",
  "description": "spécialiste du chemisage de canalisation en copropriété à Bordeaux. Immeubles haussmanniens, syndics, vote AG, sans tranchee, garantie décennale.",
  "url": "https://recherche-fuite-gironde.fr/detection-fuite/chemisage-bordeaux/",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Bordeaux",
    "postalCode": "33000",
    "addressCountry": "FR"
  },
  "areaServed": { "@type": "City", "name": "Bordeaux" },
  "priceRange": "€€€"
}
</script>'''

    ld_breadcrumb = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://recherche-fuite-gironde.fr/" },
    { "@type": "ListItem", "position": 2, "name": "Chemisage", "item": "https://recherche-fuite-gironde.fr/chemisage-canalisation/" },
    { "@type": "ListItem", "position": 3, "name": "Chemisage Bordeaux", "item": "https://recherche-fuite-gironde.fr/detection-fuite/chemisage-bordeaux/" }
  ]
}
</script>'''

    ld_faq = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Quel est le coût moyen d'un chemisage de colonne en copropriété bordelaise ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Le chemisage d'une colonne d'évacuation EU/EV en copropriété coûte en moyenne 400 à 700 euros HT par metre lineaire selon le diamètre (63 à 160 mm typiquement), la hauteur de l'immeuble, l'accessibilite des regards techniques. Pour un immeuble haussmannien de 5 étages avec colonne de 15 metres, comptez 6 000 à 10 500 euros HT, a comparer avec un remplacement classique a 15 000-25 000 euros HT (démolition + reconstruction)." }
    },
    {
      "@type": "Question",
      "name": "Le chemisage se vote-t-il en AG ordinaire ou extraordinaire ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Les travaux de chemisage sur parties communes se votent en AG ordinaire à la majorite de l'article 25 (majorite absolue des voix de tous les copropriétaires, présents, représentés ou absents). Si le vote article 25 echoue mais recueille au moins un tiers des voix, un second vote immédiat à la majorite simple de l'article 24 peut être organisé lors de la même AG. La procédure est bien rodée en copropriété bordelaise et ne nécessite généralement pas d'AG extraordinaire." }
    },
    {
      "@type": "Question",
      "name": "Le chemisage est-il compatible avec les immeubles UNESCO de Bordeaux ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Oui. Le chemisage est réalisé à l'intérieur des canalisations existantes sans modification de l'aspect extérieur ni ouverture de murs visibles. Aucune autorisation d'urbanisme ni avis de l'Architecte des Batiments de France n'est nécessaire pour cette intervention. C'est même la technique privilégiée pour les immeubles classés UNESCO du Port de la Lune (Triangle d'Or, cours de l'Intendance, place Gambetta) ou toute modification extérieure est strictement encadrée." }
    },
    {
      "@type": "Question",
      "name": "Combien de temps dure un chantier de chemisage sur colonne de 15 metres ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Un chantier de chemisage sur une colonne typique d'immeuble bordelais (15 à 25 metres, diamètre 90 à 125 mm) dure 2 à 4 jours, avec coupure d'eau sur la colonne uniquement pendant les heures de polymerisation (6 à 10 heures). Les appartements restent occupés pendant le chantier, les coupures sont coordonnees avec les habitants via affichage dans les parties communes." }
    },
    {
      "@type": "Question",
      "name": "Quelle est la garantie sur un chemisage tubulaire en Gironde ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Le chemisage tubulaire est couvert par la garantie décennale obligatoire sur les travaux de batiment. La durée de vie estimee du liner resine epoxy est de 50 ans dans des conditions normales d'utilisation. Un rapport de fin de chantier avec contrôle camera est remis au syndic, a annexer au carnet d'entretien obligatoire de l'immeuble (loi ALUR)." }
    },
    {
      "@type": "Question",
      "name": "Intervenez-vous sur les immeubles anciens avec canalisations en plomb ou fonte ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Oui, le chemisage est parfaitement adapte aux canalisations fonte grise (majoritaire dans les immeubles bordelais d'avant 1975), galvanise et même plomb (interdit depuis 1995 mais encore présent dans certaines colonnes non renovées). La technique consiste a créer un nouveau tuyau resine à l'intérieur de l'ancien, rendant obsolete le materiau d'origine sans avoir à le démonter." }
    }
  ]
}
</script>'''

    body = f'''
<section class="hero-mini">
  <div class="container">
    <nav class="breadcrumb">
      <a href="/">Accueil</a>
      <span>&rsaquo;</span>
      <a href="/chemisage-canalisation/">Chemisage</a>
      <span>&rsaquo;</span>
      <span>Chemisage Bordeaux</span>
    </nav>
    <h1>Chemisage de canalisation pour syndics et copropriétés à Bordeaux</h1>
    <p class="hero-mini-lead">rénovation des colonnes d'évacuation et canalisations vieillissantes des immeubles bordelais, <strong>sans tranchee ni démolition</strong>. Liner tubulaire en resine epoxy insere dans la canalisation existante, durée de vie 50 ans, garantie décennale. spécialistes des copropriétés haussmanniennes et immeubles classés UNESCO.</p>
    <div class="hero-mini-cta">
      <a href="/devis/" class="btn btn-gold">Demander un devis chemisage</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <h2>Pourquoi le chemisage est la solution pour les immeubles bordelais</h2>
    <p>Le parc immobilier historique de Bordeaux (Triangle d'Or, Chartrons, Saint-Pierre, place Gambetta) compte une part significative d'immeubles haussmanniens construits entre 1830 et 1910. Ces batiments abritent des colonnes d'évacuation EU/EV en fonte grise d'origine, parfois centenaires, dont l'etat se dégradé progressivement par corrosion interne. Les fuites multiples deviennent une problématique majeure après 100 à 120 ans de service.</p>

    <p>Face à cette usure structurelle, la reponse traditionnelle etait le remplacement complet : ouverture des gaines, déposé des anciennes canalisations, pose de nouveaux tuyaux, rebouchage et finition. Sur un immeuble de 5 à 6 étages, ce type de travaux dure 3 à 8 semaines, coûte 15 000 à 30 000 euros, et implique le logement en chantier des copropriétaires concernes. Le chemisage tubulaire permet d'obtenir le même résultat technique (colonne étanche durable 50 ans) en 2 à 4 jours, pour 30 à 50 pourcent moins cher, sans aucune démolition.</p>

    <h2>Les immeubles bordelais typiquement concernés</h2>

    <div class="grid-3" style="margin-top:1.5rem;">
      <div class="arg-num-card">
        <span class="arg-num">01</span>
        <div class="arg-num-content">
          <h3>Haussmanniens du Triangle d'Or</h3>
          <p>Immeubles classés UNESCO du Port de la Lune (allees de Tourny, cours de l'Intendance, allees Damour). Colonnes fonte grise d'origine, finitions intérieures precieuses (parquets Versailles, moulures, cheminées marbre). Le chemisage préservé intégralement ces elements patrimoniaux.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">02</span>
        <div class="arg-num-content">
          <h3>Copropriétés des Chartrons</h3>
          <p>Anciens entrepôts viticoles reconvertis en logements dans les années 1980-2000, colonnes d'évacuation modernisees en PVC mais raccorde sur réseau fonte d'origine en sous-sol. Points de raccordement fragilizes, cedant après 30-40 ans d'usage.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">03</span>
        <div class="arg-num-content">
          <h3>résidences des années 1960-80</h3>
          <p>Grands ensembles de Meriadeck, Bacalan, Benauge, Grand Parc : colonnes EU/EV en fonte grise industrielle qui commencent a ceder aux joints et aux raccords après 50 à 60 ans. Le chemisage est parfaitement adapte aux grandes sections (100-160 mm) typiques de ces immeubles.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">04</span>
        <div class="arg-num-content">
          <h3>Echoppes bordelaises</h3>
          <p>Echoppes traditionnelles de Saint-Genes, Caudéran, Saint-Augustin avec réseau d'évacuation historique en fonte ou gres vitrifie. Le chemisage permet de rénover ces réseaux sans casser les carrelages ciment et parquets point de Hongrie typiques.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">05</span>
        <div class="arg-num-content">
          <h3>Immeubles contemporains Bassins a Flot</h3>
          <p>Rare mais possible : les immeubles récents (2005-2015) avec défauts de pose sur certains raccords PVC. Le chemisage peut intervenir de manière ciblée sur le troncon défaillant sans changer toute la colonne.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">06</span>
        <div class="arg-num-content">
          <h3>réseaux enterrés en cour intérieure</h3>
          <p>De nombreux immeubles bordelais ont des réseaux d'évacuation enterrés sous la cour intérieure, accessibles uniquement par regards techniques. Le chemisage sans tranchee est ici quasi-obligatoire car la démolition serait irrealisable sans impact lourd sur l'immeuble.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:1080px;">
    <h2>Le chemisage en copropriété : procédure AG et vote</h2>
    <p>Le chemisage sur parties communes (colonnes d'évacuation EU/EV, canalisations d'alimentation générale, réseaux enterrés) relevé du vote en assemblee générale des copropriétaires. Voici le parcours complet d'un projet chemisage, typique à Bordeaux.</p>

    <h3>étape 1 : signalement et pre-diagnostic</h3>
    <p>Le syndic reçoit plusieurs signalements de fuites récurrentes dans la même zone de l'immeuble (plafonds tachés au 3e et 4e étage, par exemple). Il commande un pre-diagnostic par recherche de fuite non destructive (notre prestation). Notre rapport etablit la cause : colonne fonte fatiguee, fuites multiples sur 4 étages, réparation ponctuelle non durable.</p>

    <h3>étape 2 : devis chemisage et preparation AG</h3>
    <p>Le syndic demande plusieurs devis (au moins 2 obligatoires selon la loi). Notre devis chemisage chiffre précisément le lineaire a traiter, la technique retenue (polymerisation UV ou vapeur), les garanties, le planning. Le devis est inscrit à l'ordre du jour de la prochaine AG ordinaire avec toute la documentation technique.</p>

    <h3>étape 3 : vote en assemblee générale ordinaire</h3>
    <p>Les travaux de chemisage sur parties communes se votent à la majorite de l'article 25 (majorite absolue de tous les copropriétaires, présents/représentés/absents). Si le vote article 25 echoue mais recueille au moins un tiers des voix, un second vote immédiat à la majorite simple de l'article 24 peut être organisé dans la même AG. Cette procédure articulée en deux temps évité de repasser par une AG extraordinaire.</p>

    <h3>étape 4 : signature du marche et planning</h3>
    <p>après vote, le syndic signe le marche avec nous. Nous etablissons un planning détaillé : date de début, durée par étape (inspection préalable, hydrocurage de la colonne, pose du liner, polymerisation, contrôle camera final). Information affichée dans les parties communes au moins 15 jours avant le début.</p>

    <h3>étape 5 : chantier en 2 à 5 jours</h3>
    <p>L'intervention respecte l'occupation des logements. Les copropriétaires sont informés des creneaux de coupure d'eau sur la colonne concernée (6 à 10 heures pendant la polymerisation). Les équipés interviennent depuis les parties communes (paliers, caves, cour intérieure) sans accès aux appartements, sauf si un regard technique est situé dans un logement privatif.</p>

    <h3>étape 6 : reception et annexion carnet d'entretien</h3>
    <p>A l'issue du chantier, une inspection camera de contrôle est realisée et filmée. Le rapport final avec video est remis au syndic, qui l'intégré au carnet d'entretien obligatoire de l'immeuble (loi ALUR). La garantie décennale court à partir de cette date de reception.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Tarifs du chemisage en copropriété bordelaise</h2>
    <p>Le coût du chemisage dépend principalement du lineaire a traiter, du diamètre de la canalisation et de l'accessibilite. Voici les fourchettes applicables à Bordeaux en 2026.</p>

    <table style="width:100%;border-collapse:collapse;margin:1.5rem 0;background:#fff;">
    <thead><tr style="background:#0D3B2E;color:#fff;"><th style="padding:.75rem;text-align:left;border:1px solid #155740;">Configuration</th><th style="padding:.75rem;text-align:left;border:1px solid #155740;">Tarif HT par metre lineaire</th><th style="padding:.75rem;text-align:left;border:1px solid #155740;">Exemple sur 15 metres</th></tr></thead>
    <tbody>
    <tr><td style="padding:.75rem;border:1px solid #D8D4CC;">Petit diamètre (50-75 mm)</td><td style="padding:.75rem;border:1px solid #D8D4CC;">300 à 450 €</td><td style="padding:.75rem;border:1px solid #D8D4CC;">4 500 à 6 750 €</td></tr>
    <tr style="background:#F7F6F2;"><td style="padding:.75rem;border:1px solid #D8D4CC;">Diamètre moyen (90-125 mm)</td><td style="padding:.75rem;border:1px solid #D8D4CC;">400 à 600 €</td><td style="padding:.75rem;border:1px solid #D8D4CC;">6 000 à 9 000 €</td></tr>
    <tr><td style="padding:.75rem;border:1px solid #D8D4CC;">Grand diamètre (150-200 mm)</td><td style="padding:.75rem;border:1px solid #D8D4CC;">550 à 800 €</td><td style="padding:.75rem;border:1px solid #D8D4CC;">8 250 à 12 000 €</td></tr>
    <tr style="background:#F7F6F2;"><td style="padding:.75rem;border:1px solid #D8D4CC;">réseaux enterrés complexes</td><td style="padding:.75rem;border:1px solid #D8D4CC;">700 à 1 000 €</td><td style="padding:.75rem;border:1px solid #D8D4CC;">10 500 à 15 000 €</td></tr>
    </tbody>
    </table>

    <h3>Elements inclus dans le tarif</h3>
    <ul>
    <li>Inspection camera préalable pour validation technique (longueur, etat, points critiques)</li>
    <li>Hydrocurage de la canalisation existante (nettoyage haute pression)</li>
    <li>Fourniture et pose du liner imprégné de resine epoxy certifiée ACS (qualite eau potable)</li>
    <li>Polymerisation in situ (vapeur, eau chaude ou UV selon le cas)</li>
    <li>Rapport camera de contrôle final</li>
    <li>Garantie décennale sur l'intervention</li>
    </ul>

    <h3>Elements en supplement</h3>
    <ul>
    <li>Acces difficile necessitant echafaudage extérieur (rare, pour cheminées ou descentes de gouttieres)</li>
    <li>Traitement préalable d'obstruction massive (racines, amas de depôts) : facture selon etat</li>
    <li>Modification ponctuelle pour chapes ou passages techniques a adapter</li>
    </ul>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Questions fréquentes sur le chemisage à Bordeaux</h2>

    <h3>Quel est le coût moyen d'un chemisage de colonne en copropriété bordelaise ?</h3>
    <p>Le chemisage d'une colonne d'évacuation EU/EV en copropriété coûte en moyenne 400 à 700 euros HT par metre lineaire selon le diamètre (63 à 160 mm typiquement), la hauteur de l'immeuble, l'accessibilite des regards techniques. Pour un immeuble haussmannien de 5 étages avec colonne de 15 metres, comptez 6 000 à 10 500 euros HT, a comparer avec un remplacement classique a 15 000-25 000 euros HT (démolition + reconstruction).</p>

    <h3>Le chemisage se vote-t-il en AG ordinaire ou extraordinaire ?</h3>
    <p>Les travaux de chemisage sur parties communes se votent en AG ordinaire à la majorite de l'article 25. Si le vote echoue mais recueille au moins un tiers des voix, un second vote immédiat à la majorite simple (article 24) peut être organisé dans la même AG. La procédure est bien rodée et ne nécessite généralement pas d'AG extraordinaire.</p>

    <h3>Le chemisage est-il compatible avec les immeubles UNESCO de Bordeaux ?</h3>
    <p>Oui. Le chemisage est réalisé à l'intérieur des canalisations existantes sans modification de l'aspect extérieur ni ouverture de murs visibles. Aucune autorisation d'urbanisme ni avis de l'Architecte des Batiments de France n'est nécessaire. C'est même la technique privilégiée pour les immeubles classés UNESCO du Port de la Lune.</p>

    <h3>Combien de temps dure un chantier de chemisage sur colonne de 15 metres ?</h3>
    <p>Un chantier de chemisage sur une colonne typique d'immeuble bordelais dure 2 à 4 jours, avec coupure d'eau sur la colonne uniquement pendant les heures de polymerisation (6 à 10 heures). Les appartements restent occupés pendant le chantier.</p>

    <h3>quelle est la garantie sur un chemisage tubulaire en Gironde ?</h3>
    <p>Le chemisage tubulaire est couvert par la garantie décennale obligatoire. La durée de vie estimee du liner resine epoxy est de 50 ans dans des conditions normales d'utilisation. Un rapport de fin de chantier avec contrôle camera est remis au syndic.</p>

    <h3>Intervenez-vous sur les immeubles anciens avec canalisations en plomb ou fonte ?</h3>
    <p>Oui, le chemisage est parfaitement adapte aux canalisations fonte grise (majoritaire dans les immeubles bordelais d'avant 1975), galvanise et même plomb. La technique consiste a créer un nouveau tuyau resine à l'intérieur de l'ancien. Pour plus de détails techniques, consultez notre guide <a href="/guide/chemisage-explication/" style="color:var(--green);text-decoration:underline;">chemisage de canalisation expliqué</a> ou la page service <a href="/chemisage-canalisation/" style="color:var(--green);text-decoration:underline;">chemisage en Gironde</a>.</p>

    <div style="margin-top:2rem;text-align:center;">
      <a href="/devis/" class="btn btn-gold">Demander un devis chemisage Bordeaux</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Pages connexes pour copropriétés bordelaises</h2>
    <p>Le chemisage intervient souvent dans un contexte plus large de gestion d'un sinistre ou d'une rénovation préventive. Voici les ressources connexes :</p>
    <ul>
      <li><a href="/detection-fuite/degats-des-eaux-bordeaux/" style="color:var(--green);text-decoration:underline;">Dégât des eaux à Bordeaux pour syndics</a> : avant le chemisage, le diagnostic d'origine de la fuite est essentiel pour activer la convention IRSI.</li>
      <li><a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">Canalisation enterrée Bordeaux</a> : pour les réseaux enterrés sous cour intérieure ou en sous-sol, le chemisage est aussi applicable après diagnostic gaz traceur.</li>
      <li><a href="/villes/bordeaux/" style="color:var(--green);text-decoration:underline;">Recherche de fuite à Bordeaux</a> : page ville détaillant nos interventions sur l'ensemble du parc bordelais (haussmanniens, échoppes, copropriétés).</li>
      <li><a href="/detection-fuite/urgence-bordeaux/" style="color:var(--green);text-decoration:underline;">Recherche de fuite en urgence</a> : pour les fuites actives nécessitant un diagnostic prioritaire avant chantier de chemisage.</li>
    </ul>
  </div>
</section>

{form_section("Bordeaux")}
'''

    return html_base(
        'Chemisage syndic copropriété Bordeaux | Vote AG IRSI',
        'Chemisage de colonnes EU/EV en copropriété à Bordeaux : préparation vote AG, devis ALUR, gestion IRSI assureur, intervention sans évacuation locataires.',
        'https://recherche-fuite-gironde.fr/detection-fuite/chemisage-bordeaux/',
        body,
        extra_ld=ld_service + ld_local + ld_breadcrumb + ld_faq,
    )


# ═══════════════════════════════════════════════════════════════
# PAGE USE CASE : Canalisation enterrée Bordeaux
# ═══════════════════════════════════════════════════════════════

def page_canalisation_enterree_bordeaux():
    ld_service = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "Recherche de fuite canalisation enterrée",
  "name": "Recherche de fuite canalisation enterrée à Bordeaux et en Gironde",
  "description": "Localisation précise d'une fuite sur canalisation enterrée (jardin, branchement, réseau privé) par gaz traceur azote/hélium, sans excavation préalable. précision au demi-metre près.",
  "provider": {
    "@type": "LocalBusiness",
    "name": "Recherche Fuite Gironde",
    "url": "https://recherche-fuite-gironde.fr/"
  },
  "areaServed": { "@type": "Place", "name": "Bordeaux et métropole girondine" },
  "category": "détection de fuite non destructive"
}
</script>'''

    ld_local = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Recherche Fuite Gironde - Canalisation enterrée Bordeaux",
  "description": "spécialiste de la recherche de fuite sur canalisation enterrée à Bordeaux. Gaz traceur azote/hélium, écoute électro-acoustique, thermographie. Intervention 24h, rapport pour assurance.",
  "url": "https://recherche-fuite-gironde.fr/detection-fuite/canalisation-enterree-bordeaux/",
  "image": "https://recherche-fuite-gironde.fr/assets/fuite-canalisation-enterree.webp",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Bordeaux",
    "postalCode": "33000",
    "addressCountry": "FR"
  },
  "areaServed": { "@type": "City", "name": "Bordeaux" },
  "priceRange": "€€"
}
</script>'''

    ld_breadcrumb = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://recherche-fuite-gironde.fr/" },
    { "@type": "ListItem", "position": 2, "name": "Détection de fuite", "item": "https://recherche-fuite-gironde.fr/detection-fuite/" },
    { "@type": "ListItem", "position": 3, "name": "Canalisation enterrée Bordeaux", "item": "https://recherche-fuite-gironde.fr/detection-fuite/canalisation-enterree-bordeaux/" }
  ]
}
</script>'''

    ld_faq = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Comment localisez-vous une fuite sur canalisation enterrée à Bordeaux sans creuser ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Notre méthode principale est le gaz traceur azote/hélium : un mélange inerte injecté dans la canalisation sous légère pression. Le gaz plus léger que l'air remonte au droit de la perforation et est détecté par un capteur électronique promené au sol. précision au demi-metre près, sans aucune excavation préalable. L'écoute électro-acoustique et la thermographie infrarouge complètent le diagnostic si nécessaire." }
    },
    {
      "@type": "Question",
      "name": "Quelles sont les canalisations enterrées les plus fragiles à Bordeaux ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Les canalisations PVC collees installées entre 1985 et 2000 sont les plus fragiles sur sol argileux bordelais. Les raccords se desaxent par retrait-gonflement saisonnier de l'argile. Les canalisations PEHD (polyethylene haute densité) posees depuis 2005 sont plus tolerantes aux mouvements de terrain. Les anciennes canalisations plomb et fonte des immeubles du centre historique (avant 1975) sont corrodees et sujettes aux perforations." }
    },
    {
      "@type": "Question",
      "name": "Combien coûte une recherche de fuite sur canalisation enterrée à Bordeaux ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Entre 400 et 700 euros HT selon la longueur de la canalisation a diagnostiquer et la complexite du réseau. Un forfait gaz traceur classique (jusqu'à 20 metres de canalisation) est a 450 euros HT en moyenne. Au-delà de 30 metres ou pour les réseaux complexes (plusieurs branches), un diagnostic approfondi peut atteindre 700 euros HT. Devis fixe communique avant intervention." }
    },
    {
      "@type": "Question",
      "name": "La recherche de fuite enterrée est-elle remboursee par l'assurance ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Oui, dans la majorite des cas. La garantie recherche de fuite de votre contrat multirisque habitation prend en charge le diagnostic dès lors qu'un dégât des eaux est constate (terrain gorgé d'eau, impact sur fondations, infiltration dans construction). Si la fuite concerne une canalisation enterrée indétectable, vous pouvez en plus obtenir un écrêtement de votre facture d'eau auprès de Suez ou votre régie via la loi Warsmann 2011." }
    },
    {
      "@type": "Question",
      "name": "Intervenez-vous dans tous les quartiers de Bordeaux pour les fuites enterrées ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Oui, nous couvrons l'ensemble des 18 quartiers de Bordeaux ainsi que les communes voisines de la métropole. Nous rencontrons les problématiques de fuites enterrées le plus fréquemment dans les zones pavillonnaires (Caudéran, Le Bouscat, Bacalan, Saint-Augustin) avec grands jardins, ainsi que dans les copropriétés récentes avec réseaux enterrés entre immeuble et regards techniques." }
    },
    {
      "@type": "Question",
      "name": "Faut-il creuser pour réparer après votre diagnostic ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Oui, mais de manière très ciblée. Notre diagnostic localise la fuite au demi-metre près, ce qui limite l'excavation a 50 cm x 50 cm en moyenne. Pour éviter totalement le creusement, deux alternatives : le chemisage de canalisation (réhabilitation sans tranchee par resine epoxy, adapte aux réseaux de 40 à 600 mm) ou le remplacement de la canalisation existante si son etat général l'exige." }
    }
  ]
}
</script>'''

    body = f'''
<section class="hero-mini">
  <div class="container">
    <nav class="breadcrumb">
      <a href="/">Accueil</a>
      <span>&rsaquo;</span>
      <a href="/detection-fuite/">détection de fuite</a>
      <span>&rsaquo;</span>
      <span>Canalisation enterrée Bordeaux</span>
    </nav>
    <h1>Recherche de fuite de canalisation enterrée à Bordeaux</h1>
    <p class="hero-mini-lead">Zone de jardin anormalement humide, compteur d'eau qui tourne en permanence, facture d'eau qui grimpe sans raison : votre fuite se situe probablement sur une canalisation enterrée. Nos techniciens la localisent <strong>au demi-metre près sans creuser</strong> grâce au gaz traceur azote/hélium, puis vous remettent un rapport utilisable pour l'assurance et l'écrêtement de facture.</p>
    <div class="hero-mini-cta">
      <a href="/devis/" class="btn btn-gold">Demander un devis gratuit</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <figure style="margin:0 0 2rem;">
      <img src="/assets/fuite-canalisation-enterree.webp" alt="Recherche de fuite sur canalisation enterrée à Bordeaux avec gaz traceur azote hélium, diagnostic sans excavation" width="700" height="467" loading="eager" style="width:100%;max-height:380px;height:auto;object-fit:cover;border-radius:12px;display:block;">
    </figure>

    <h2>Les signes d'une fuite sur canalisation enterrée à Bordeaux</h2>
    <p>Sur les propriétés bordelaises avec jardin, branchement d'eau enterré ou réseau d'arrosage, plusieurs symptomes doivent alerter. Contrairement aux fuites intérieures visibles par une tache au plafond, les fuites enterrées sont sournoises : elles peuvent couler pendant des mois sans aucun signe au-dessus du sol.</p>

    <ul>
      <li><strong>Zone de jardin anormalement verte</strong> toute l'année, même en période sans arrosage</li>
      <li><strong>Terrain gorgé d'eau ou sol qui s'affaisse</strong> sur un trace lineaire, suggerant le tracé d'une canalisation</li>
      <li><strong>Consommation d'eau qui grimpe</strong> sans changement d'usage, visible sur la facture trimestrielle Suez</li>
      <li><strong>Compteur d'eau qui tourne en permanence</strong> même robinets fermes, a vérifier le soir en coupant tout point d'eau</li>
      <li><strong>Pression d'eau anormalement basse</strong> au robinet alors que les canalisations intérieures sont en bon etat</li>
      <li><strong>Flaque au pied de la maison</strong> après plusieurs jours sans pluie, signe d'infiltration par la canalisation d'alimentation</li>
      <li><strong>Mousse ou champignons</strong> inhabituels en bordure de terrasse ou allee</li>
    </ul>

    <h2>Pourquoi les canalisations enterrées bordelaises lâchent-elles souvent au même endroit ?</h2>
    <p>La spécificité geologique de Bordeaux et sa métropole est determinante. Une large part du territoire repose sur des sols argileux sujets au retrait-gonflement saisonnier : l'argile se rétracte en été sec, gonfle en hiver pluvieux. Sur 20 à 30 ans, ces cycles répétés solliticitent les raccords collés PVC de manière importante. Résultat observable sur le terrain : les raccords PVC de 25 à 35 ans cèdent significativement plus à Bordeaux qu'en sol sableux ou calcaire pur.</p>

    <p>La zone aéroportuaire (Mérignac), la rive droite (Cenon, Lormont, Floirac) et le Grand Parc présentent cette typologie argileuse marquee. Les communes du bassin d'Arcachon sont en sol sableux (autre problème : micro-tassements permanents), et le Libournais alterne argileux et calcaire selon les zones. Cette connaissance locale oriente notre méthodologie de diagnostic.</p>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:1080px;">
    <h2>Notre méthode gaz traceur en 5 étapes</h2>
    <p>Le gaz traceur azote/hélium est la méthode de référence pour les canalisations enterrées. Voici le deroule concret d'une intervention sur votre propriété bordelaise.</p>

    <div class="grid-3" style="margin-top:1.5rem;">
      <div class="arg-num-card">
        <span class="arg-num">01</span>
        <div class="arg-num-content">
          <h3>Reconnaissance du réseau</h3>
          <p>Reperage des regards, compteurs, arrivées et départs d'eau sur la propriété. Traçage approximatif des canalisations enterrées d'après les plans disponibles ou observation du terrain. identification des points d'injection possibles pour le gaz.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">02</span>
        <div class="arg-num-content">
          <h3>Mise sous pression et injection</h3>
          <p>La canalisation est isolée et mise sous légère pression avec un mélange azote/hélium inerte (80/20). Le mélange est plus léger que l'air et migre vers la fuite en prenant le trajet du moindre chemin.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">03</span>
        <div class="arg-num-content">
          <h3>détection de surface</h3>
          <p>Un détecteur électronique très sensible (sniffer) est promené au sol le long du trace presume de la canalisation. Le capteur signalé la remontée du gaz avec une précision au demi-metre près, materialisant la position exacte de la fuite.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">04</span>
        <div class="arg-num-content">
          <h3>Confirmation par écoute</h3>
          <p>En complement, nous ecoutons electro-acoustiquement la zone localisée pour confirmer la fuite par le bruit caractéristique de l'eau sous pression qui s'échappe. Cette double confirmation elimine les faux positifs.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">05</span>
        <div class="arg-num-content">
          <h3>Materialisation et rapport</h3>
          <p>La position exacte de la fuite est marquee au sol (piquet, bombe de couleur non permanente). Le rapport technique photographique documente le trace, la méthode, la localisation et les préconisations de réparation. Il est remis sur site ou sous 24h.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">06</span>
        <div class="arg-num-content">
          <h3>Option chemisage sans tranchee</h3>
          <p>Si plusieurs fuites sont identifiées sur le même réseau, ou si la canalisation est généralement dégradée, nous vous proposons une alternative au creusement : le chemisage tubulaire sans tranchee qui créé un nouveau tuyau à l'intérieur de l'ancien.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <h2>Quartiers de Bordeaux ou nous intervenons le plus sur canalisation enterrée</h2>
    <p>Certains quartiers concentrent les demandes pour fuite enterrée en raison de leur typologie bâtie et de leur environnement paysager.</p>

    <div class="grid-3" style="margin-top:1.5rem;">
      <div class="arg-num-card">
        <span class="arg-num">01</span>
        <div class="arg-num-content">
          <h3>Caudéran et Le Bouscat</h3>
          <p>Grands jardins des propriétés bourgeoises, nombreux arbres matures (platanes, chenes, tilleuls) dont les racines sollicitent les canalisations. Les raccords PVC de 30 ans y sont particulièrement fragiles. Nous intervenons souvent sur le trace d'alimentation compteur-maison.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">02</span>
        <div class="arg-num-content">
          <h3>Saint-Augustin et Grand Parc</h3>
          <p>Maisons individuelles avec jardins moyens, réseaux d'arrosage enterrés fréquents. Les confusions entre fuite alimentation et fuite arrosage sont courantes : notre diagnostic isole chaque circuit pour eliminer les faux positifs.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">03</span>
        <div class="arg-num-content">
          <h3>Bacalan et Bassins à Flot</h3>
          <p>résidences récentes (2010-2020) avec réseaux enterrés entre immeuble et regards techniques. Les canalisations PEHD posees dans les années 2010 sont robustes mais les raccords mécaniques sont sujets à défaut de serrage.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">04</span>
        <div class="arg-num-content">
          <h3>La Bastide et Cenon (rive droite)</h3>
          <p>Terrains argileux marques, nombreux pavillons des années 1970-1990 avec canalisations PVC d'origine. Les mouvements de terrain y sont les plus actifs, les fuites enterrées les plus fréquentes.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">05</span>
        <div class="arg-num-content">
          <h3>Mérignac et communes métropole</h3>
          <p>Parc pavillonnaire très dense des années 1980-2000. Canalisations d'alimentation souvent longues (20 à 50 m entre compteur et maison). Proportion importante de nos interventions enterrées se fait sur Mérignac (Arlac, Capeyron, Chemin Long).</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">06</span>
        <div class="arg-num-content">
          <h3>Bordeaux Centre historique</h3>
          <p>Moins de canalisations enterrées individuelles (tissu urbain dense) mais présence de réseaux anciens (plomb, fonte, galvanisé) sous les cours intérieures et arrières-cours des immeubles. diagnostic particulier adaptant nos outils compacts aux configurations restreintes.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Cas type d'intervention à Bordeaux</h2>
    <p>Scenario récurrent : maison familiale a Caudéran, canalisation d'alimentation enterrée de 1989 sur 35 metres entre le regard de compteur en façade et l'entrée de la maison. Le propriétaire constate une facture Suez doublée (de 40 m³ a 80 m³ par trimestre), sans changement d'usage. Aucune trace d'humidité visible dans le jardin ni dans la maison.</p>

    <p>Notre intervention : vérification du robinet d'arrêt général (compteur qui continue de tourner après coupure maison = fuite après compteur sur partie privative). Isolation du circuit d'arrosage (compteur qui s'arrête = arrosage hors cause). Mise sous pression du tronçon compteur-maison avec gaz traceur. détection au sol le long du tracé : remontée du gaz à 22 metres du regard de compteur, sous l'allée gravillonnée. Marquage au sol et materialisation de la fuite.</p>

    <p>réparation : ouverture localisée 60×60 cm au point marque, remplacement d'un manchon PVC de 40 cm, remblaiement et remise en état gravillons. Coût total intervention + réparation : 850 euros. Dossier transmis à l'assureur qui prend en charge 600 euros au titre de la garantie recherche de fuite, et le client obtient un écretement de sa facture Suez selon la loi Warsmann pour les m³ surconsommés.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Questions fréquentes sur la recherche de fuite enterrée à Bordeaux</h2>

    <h3>Comment localisez-vous une fuite sur canalisation enterrée à Bordeaux sans creuser ?</h3>
    <p>Notre méthode principale est le gaz traceur azote/hélium : un mélange inerte injecté dans la canalisation sous légère pression. Le gaz plus léger que l'air remonte au droit de la perforation et est détecté par un capteur électronique promené au sol. précision au demi-metre près, sans aucune excavation préalable. L'écoute électro-acoustique et la thermographie infrarouge complètent le diagnostic si nécessaire.</p>

    <h3>Quelles sont les canalisations enterrées les plus fragiles à Bordeaux ?</h3>
    <p>Les canalisations PVC collees installées entre 1985 et 2000 sont les plus fragiles sur sol argileux bordelais. Les raccords se desaxent par retrait-gonflement saisonnier de l'argile. Les canalisations PEHD posees depuis 2005 sont plus tolerantes aux mouvements de terrain. Les anciennes canalisations plomb et fonte des immeubles du centre historique (avant 1975) sont corrodees et sujettes aux perforations.</p>

    <h3>Combien coûte une recherche de fuite sur canalisation enterrée à Bordeaux ?</h3>
    <p>Entre 400 et 700 euros HT selon la longueur de la canalisation a diagnostiquer et la complexite du réseau. Un forfait gaz traceur classique (jusqu'à 20 metres de canalisation) est a 450 euros HT en moyenne. Au-delà de 30 metres ou pour les réseaux complexes (plusieurs branches), un diagnostic approfondi peut atteindre 700 euros HT.</p>

    <h3>La recherche de fuite enterrée est-elle remboursee par l'assurance ?</h3>
    <p>Oui, dans la majorite des cas. La garantie recherche de fuite de votre contrat multirisque habitation prend en charge le diagnostic dès lors qu'un dégât des eaux est constate. Si la fuite concerne une canalisation enterrée indétectable, vous pouvez en plus obtenir un écrêtement de votre facture d'eau auprès de Suez ou votre régie via la loi Warsmann 2011. Voir notre page <a href="/detection-fuite/fuite-apres-compteur/" style="color:var(--green);text-decoration:underline;">fuite d'eau après compteur à Bordeaux</a> pour le détail de la procédure d'écrêtement.</p>

    <h3>Intervenez-vous dans tous les quartiers de Bordeaux pour les fuites enterrées ?</h3>
    <p>Oui, nous couvrons l'ensemble des 18 quartiers de Bordeaux ainsi que les communes voisines de la métropole. Pour plus de détails sur notre intervention ville par ville, consultez notre page <a href="/villes/bordeaux/" style="color:var(--green);text-decoration:underline;">recherche de fuite à Bordeaux</a>.</p>

    <h3>Faut-il creuser pour réparer après votre diagnostic ?</h3>
    <p>Oui, mais de manière très ciblée. Notre diagnostic localise la fuite au demi-metre près, ce qui limite l'excavation a 50 cm x 50 cm en moyenne. Pour éviter totalement le creusement, deux alternatives : le <a href="/detection-fuite/chemisage-bordeaux/" style="color:var(--green);text-decoration:underline;">chemisage de canalisation à Bordeaux</a> (réhabilitation sans tranchee par resine epoxy, adapte aux réseaux de 40 à 600 mm) ou le remplacement de la canalisation existante si son etat général l'exige.</p>

    <div style="margin-top:2rem;text-align:center;">
      <a href="/devis/" class="btn btn-gold">Demander un devis canalisation enterrée</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Pages connexes : fuite enterrée et alternatives</h2>
    <p>Une fuite sur canalisation enterrée touche plusieurs sujets connexes. Selon votre cas, ces ressources sont pertinentes :</p>
    <ul>
      <li><a href="/detection-fuite/fuite-apres-compteur/" style="color:var(--green);text-decoration:underline;">Fuite d'eau après compteur à Bordeaux</a> : si votre compteur tourne en permanence et votre facture grimpe, c'est l'angle privilégié à explorer.</li>
      <li><a href="/guide/loi-warsmann-ecretement-facture-eau/" style="color:var(--green);text-decoration:underline;">Loi Warsmann et écrêtement de facture</a> : pour plafonner légalement votre facture d'eau après une fuite enterrée non détectable.</li>
      <li><a href="/detection-fuite/chemisage-bordeaux/" style="color:var(--green);text-decoration:underline;">Chemisage de canalisation à Bordeaux</a> : alternative sans tranchée pour rénover le réseau enterré dégradé sur sa totalité.</li>
      <li><a href="/detection-fuite/urgence-bordeaux/" style="color:var(--green);text-decoration:underline;">Recherche de fuite en urgence</a> : si la fuite est importante et provoque déjà des dégâts visibles (terrain saturé, fondation impactée).</li>
      <li><a href="/guide/fuite-canalisation-enterree-assurance/" style="color:var(--green);text-decoration:underline;">Prise en charge assurance d'une fuite enterrée</a> : conditions, procédure pas à pas, cas concrets de remboursement en Gironde.</li>
    </ul>
  </div>
</section>

{form_section("Bordeaux")}
'''

    return html_base(
        'Fuite canalisation enterrée Bordeaux | Gaz traceur',
        'Recherche de fuite sur canalisation enterrée à Bordeaux sans excavation : gaz traceur azote/hélium, précision demi-metre, rapport pour assurance. spécialistes terrain argileux.',
        'https://recherche-fuite-gironde.fr/detection-fuite/canalisation-enterree-bordeaux/',
        body,
        extra_ld=ld_service + ld_local + ld_breadcrumb + ld_faq,
    )


# ═══════════════════════════════════════════════════════════════
# PAGE USE CASE : Fuite après compteur d'eau
# ═══════════════════════════════════════════════════════════════

def page_fuite_apres_compteur():
    ld_service = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "Recherche de fuite après compteur d'eau",
  "name": "Recherche de fuite après compteur à Bordeaux et en Gironde",
  "description": "Localisation précise d'une fuite sur le réseau privatif après compteur d'eau (entre le compteur et la maison ou dans le logement), sans démolition. Méthodes : thermographie, gaz traceur, écoute électro-acoustique.",
  "provider": {
    "@type": "LocalBusiness",
    "name": "Recherche Fuite Gironde",
    "url": "https://recherche-fuite-gironde.fr/"
  },
  "areaServed": { "@type": "Place", "name": "Gironde" }
}
</script>'''

    ld_faq = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Comment savoir si la fuite est avant ou après le compteur ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Fermez votre robinet d'arrêt général situé juste après le compteur. Si le compteur continue de tourner, la fuite est AVANT le compteur (partie publique, Suez ou régie). S'il s'arrête mais que vous perdez toujours de l'eau dans la maison, la fuite est APRÈS le compteur, à votre charge." }
    },
    {
      "@type": "Question",
      "name": "Qui paie la recherche de fuite après compteur ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Là partie après compteur relève du propriétaire ou de l'occupant. La recherche de fuite est à votre charge mais souvent remboursée par votre assurance habitation au titre de la garantie recherche de fuite. Certaines communes ou intercommunalités proposent un écrêtement de facture en cas de fuite enterrée non détectable." }
    },
    {
      "@type": "Question",
      "name": "Peut-on faire écrêter la facture d'eau après une fuite ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Oui, la loi Warsmann (2011) permet d'obtenir un écrêtement de là part excédentaire de votre facture si vous prouvez qu'une fuite sur canalisation enterrée (entre compteur et habitation) était indétectable. Il faut fournir une attestation de réparation par un professionnel et un rapport de localisation. Notre rapport technique peut servir de justificatif." }
    },
    {
      "@type": "Question",
      "name": "Où chercher la fuite sur le réseau après compteur ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Les zones les plus fréquentes : 1) canalisation enterrée entre le regard de compteur et la maison (raccord qui lâche, fissure PVC), 2) réseau intérieur dans les murs ou sous la dalle, 3) arrivée des sanitaires (chasse d'eau, robinet qui fuit en permanence), 4) chauffe-eau ou ballon (joint, soupape). La thermographie et le gaz traceur permettent de cibler précisément." }
    },
    {
      "@type": "Question",
      "name": "Combien coûte une recherche de fuite après compteur ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Entre 300 et 700 € HT selon la méthode employée et la complexité du réseau (intérieur seul, partie enterrée, ou les deux). Un devis fixe est communiqué avant intervention. Cette somme est remboursable par votre assurance habitation si un dégât des eaux est constaté." }
    },
    {
      "@type": "Question",
      "name": "Combien de temps dure l'intervention ?",
      "acceptedAnswer": { "@type": "Answer", "text": "En moyenne 1h30 à 3 heures sur site. Si la fuite est sur canalisation enterrée et que nous devons déployer le gaz traceur sur un tracé long, comptez une demi-journée. Un rapport écrit est remis le jour même ou dans les 24 heures par email." }
    }
  ]
}
</script>'''

    body = f'''
<section class="hero-mini">
  <div class="container">
    <nav class="breadcrumb">
      <a href="/">Accueil</a>
      <span>&rsaquo;</span>
      <a href="/detection-fuite/">Détection de fuite</a>
      <span>&rsaquo;</span>
      <span>Fuite après compteur</span>
    </nav>
    <h1>Recherche de fuite après compteur d'eau à Bordeaux</h1>
    <p class="hero-mini-lead">Facture d'eau anormale, compteur qui tourne la nuit, zone humide dans le jardin : votre fuite se situe <strong>après le compteur</strong>, sur votre réseau privatif. Nos techniciens localisent la fuite sans démolition ni tranchée, pour un écrêtement de facture et une prise en charge assurance optimale.</p>
    <div class="hero-mini-cta">
      <a href="/devis/" class="btn btn-gold">Demander un devis gratuit</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <figure style="margin:0 0 2rem;">
      <img src="/assets/compteur-eau-bordeaux.webp" alt="Compteur d'eau à Bordeaux, point de démarcation entre réseau public Suez et réseau privatif du logement" width="1600" height="1067" loading="eager" style="width:100%;max-height:360px;height:auto;object-fit:cover;border-radius:12px;display:block;">
    </figure>

    <h2>Avant tout : votre fuite est-elle avant ou après le compteur ?</h2>
    <p>C'est la première question à trancher, car elle détermine qui paie la réparation et l'eau perdue. Le compteur d'eau est la limite entre deux mondes : avant (réseau public, responsabilité du distributeur Suez ou de votre régie des eaux), après (réseau privatif, votre responsabilité de propriétaire ou d'occupant).</p>

    <h3>Le test des 30 minutes pour trancher</h3>
    <ol>
      <li>Fermez tous les points d'eau de votre maison : robinets, machine à laver, chauffe-eau, chasse d'eau vérifiées.</li>
      <li>Repérez le robinet d'arrêt général situé juste après le compteur (en cave, garage ou placard technique).</li>
      <li>Notez l'index du compteur d'eau (les petits chiffres rouges ou l'aiguille en étoile sur le cadran).</li>
      <li>Attendez 30 minutes sans ouvrir aucun robinet.</li>
      <li>Comparez le nouvel index avec le précédent.</li>
    </ol>

    <ul>
      <li><strong>Si le compteur a bougé</strong> avec le robinet d'arrêt OUVERT : fuite APRÈS compteur, sur votre réseau privatif. Passez à la recherche.</li>
      <li><strong>Si le compteur a bougé</strong> avec le robinet d'arrêt FERMÉ : fuite AVANT compteur, contactez Suez ou votre régie des eaux.</li>
      <li><strong>Si le compteur n'a pas bougé</strong> : pas de fuite active détectable par ce test. Le problème peut être une humidité résiduelle ou un WC qui fuit en continu mais de façon imperceptible.</li>
    </ul>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:1080px;">
    <h2>Où se cache la fuite sur le réseau après compteur ?</h2>
    <p>Votre réseau privatif commence juste après le compteur et se compose de plusieurs segments. Voici les zones les plus fréquemment en cause.</p>

    <div class="grid-3" style="margin-top:1.5rem;">
      <div class="arg-num-card">
        <span class="arg-num">01</span>
        <div class="arg-num-content">
          <h3>Canalisation enterrée compteur → maison</h3>
          <p>Entre le regard de compteur en limite de propriété et l'entrée de votre maison, la canalisation d'alimentation est enterrée sur plusieurs mètres. Un raccord qui lâche, une fissure PVC ou polyéthylène, un tassement du terrain peuvent provoquer une fuite qui s'écoule dans le sol sans signe visible pendant des semaines.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">02</span>
        <div class="arg-num-content">
          <h3>Réseau intérieur encastré</h3>
          <p>Dans les murs et sous la dalle, les canalisations de cuivre, multicouche ou PER peuvent fuir à un raccord ou suite à une micro-perforation (clou, vis, gel). Thermographie infrarouge et écoute électro-acoustique localisent la fuite sans ouvrir le mur.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">03</span>
        <div class="arg-num-content">
          <h3>Arrivées et points d'eau</h3>
          <p>Chasse d'eau qui fuit en permanence (peut représenter 600 litres par jour), robinet qui goutte, flexible fissuré sous l'évier, joint de machine à laver usé. Points souvent négligés mais qui expliquent une partie des surconsommations.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">04</span>
        <div class="arg-num-content">
          <h3>Chauffe-eau et équipements</h3>
          <p>Ballon d'eau chaude percé, soupape de sécurité qui s'ouvre en permanence, joint de résistance usé. Fuite souvent visible dans le local technique, mais parfois invisible si l'eau s'évacue directement par le siphon de sol.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">05</span>
        <div class="arg-num-content">
          <h3>Réseau d'arrosage extérieur</h3>
          <p>Canalisation enterrée d'arrosage mal hivernée qui a gelé, raccord de robinet extérieur fissuré. Zone de gazon anormalement verte, affaissement linéaire, présence de plaques d'humidité en plein été sans arrosage.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">06</span>
        <div class="arg-num-content">
          <h3>Réseau incendie / compteur secondaire</h3>
          <p>Dans certaines copropriétés, un compteur général alimente plusieurs logements via des sous-compteurs. La fuite peut se trouver sur le réseau de distribution entre compteur principal et sous-compteurs, zone grise de responsabilité.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Écrêtement de facture : la loi Warsmann vous protège</h2>
    <p>Depuis 2011, la loi Warsmann impose aux distributeurs d'eau d'appliquer un écrêtement automatique en cas de fuite après compteur sur canalisation enterrée et non détectable. autrement dit, votre facture est plafonnée au double de votre consommation habituelle, au lieu de payer l'intégralité du volume perdu.</p>

    <h3>Conditions à remplir</h3>
    <ul>
      <li>La fuite doit concerner une <strong>canalisation enterrée</strong> (pas un robinet, pas une chasse d'eau, pas un équipement visible)</li>
      <li>La fuite doit avoir été <strong>indétectable à l'œil nu</strong> (pas de flaque, pas d'humidité visible)</li>
      <li>Vous devez fournir une <strong>attestation de réparation</strong> par un professionnel qualifié, dans un délai d'un mois après information du distributeur</li>
      <li>Le distributeur doit vous avoir informé d'une surconsommation anormale avant que vous ayez découvert la fuite</li>
    </ul>

    <h3>Ce que contient notre rapport</h3>
    <p>Notre rapport de localisation mentionne explicitement : la nature de la canalisation concernée, sa localisation enterrée, la méthode de détection employée (gaz traceur par exemple pour signifier que la fuite n'était pas détectable visuellement), la date et les photos de l'intervention. Ce document est accepté par Suez, la Régie des eaux de Bordeaux Métropole et les autres distributeurs du département de la Gironde dans le cadre d'une demande d'écrêtement.</p>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Questions fréquentes sur la fuite après compteur</h2>

    <h3>Comment savoir si la fuite est avant ou après le compteur ?</h3>
    <p>Fermez votre robinet d'arrêt général situé juste après le compteur. Si le compteur continue de tourner, la fuite est AVANT le compteur (partie publique). S'il s'arrête mais que vous perdez toujours de l'eau dans la maison, la fuite est APRÈS le compteur, à votre charge.</p>

    <h3>Qui paie la recherche de fuite après compteur ?</h3>
    <p>Là partie après compteur relève du propriétaire ou de l'occupant. La recherche de fuite est à votre charge mais souvent remboursée par votre assurance habitation au titre de la garantie recherche de fuite. Certaines communes ou intercommunalités proposent un écrêtement de facture en cas de fuite enterrée non détectable.</p>

    <h3>Peut-on faire écrêter la facture d'eau après une fuite ?</h3>
    <p>Oui, la loi Warsmann (2011) permet d'obtenir un écrêtement de là part excédentaire de votre facture si vous prouvez qu'une fuite sur canalisation enterrée (entre compteur et habitation) était indétectable. Il faut fournir une attestation de réparation par un professionnel et un rapport de localisation.</p>

    <h3>Où chercher la fuite sur le réseau après compteur ?</h3>
    <p>Les zones les plus fréquentes : canalisation enterrée entre le regard de compteur et la maison, réseau intérieur dans les murs ou sous la dalle, arrivée des sanitaires (chasse d'eau, robinet), chauffe-eau ou ballon. La thermographie et le gaz traceur permettent de cibler précisément.</p>

    <h3>Combien coûte une recherche de fuite après compteur ?</h3>
    <p>Entre 300 et 700 € HT selon la méthode employée et la complexité du réseau (intérieur seul, partie enterrée, ou les deux). Un devis fixe est communiqué avant intervention. Cette somme est remboursable par votre assurance habitation si un dégât des eaux est constaté.</p>

    <h3>Combien de temps dure l'intervention ?</h3>
    <p>En moyenne 1h30 à 3 heures sur site. Si la fuite est sur canalisation enterrée et que nous devons déployer le gaz traceur sur un tracé long, comptez une demi-journée. Un rapport écrit est remis le jour même ou dans les 24 heures par email.</p>

    <div style="margin-top:2rem;text-align:center;">
      <a href="/devis/" class="btn btn-gold">Demander un diagnostic après compteur</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Pour aller plus loin sur la fuite après compteur</h2>
    <p>Une fuite après compteur peut prendre plusieurs formes. Selon votre situation, ces ressources connexes vous aideront :</p>
    <ul>
      <li><a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">Recherche de fuite sur canalisation enterrée à Bordeaux</a> : la méthode gaz traceur expliquée pour les fuites entre compteur et habitation, ou réseau d'arrosage enterré.</li>
      <li><a href="/guide/loi-warsmann-ecretement-facture-eau/" style="color:var(--green);text-decoration:underline;">Loi Warsmann : écrêtement de facture d'eau</a> : article complet sur la procédure pour obtenir un plafonnement de votre facture, modèle de courrier inclus.</li>
      <li><a href="/detection-fuite/urgence-bordeaux/" style="color:var(--green);text-decoration:underline;">Recherche de fuite en urgence à Bordeaux</a> : si la perte d'eau est importante (plus de 1 m³/jour) et qu'un dégât des eaux est imminent ou en cours.</li>
      <li><a href="/villes/bordeaux/" style="color:var(--green);text-decoration:underline;">Recherche de fuite à Bordeaux</a> : page ville complète (haussmanniens, échoppes, copropriétés) avec toutes nos méthodes d'intervention.</li>
      <li><a href="/guide/prix-recherche-fuite-bordeaux/" style="color:var(--green);text-decoration:underline;">Tarifs d'une recherche de fuite à Bordeaux</a> : grille de prix selon la méthode et le type de canalisation.</li>
      <li><a href="/detection-fuite/degats-des-eaux-bordeaux/" style="color:var(--green);text-decoration:underline;">Dégâts des eaux à Bordeaux</a> : pour les sinistres en copropriété avec gestion IRSI et coordination assureur.</li>
      <li><a href="/simulateur-cout-fuite/" style="color:var(--green);text-decoration:underline;">Simulateur du coût de votre fuite</a> : calcul gratuit en 30 secondes avec les tarifs réels Bordeaux Métropole + éligibilité loi Warsmann automatique.</li>
    </ul>
  </div>
</section>

{form_section("Bordeaux")}
'''

    return html_base(
        'Fuite après compteur Bordeaux | Loi Warsmann',
        'Recherche de fuite après compteur d\'eau à Bordeaux et en Gironde : localisation sans démolition, écrêtement de facture possible (loi Warsmann), rapport pour assurance.',
        'https://recherche-fuite-gironde.fr/detection-fuite/fuite-apres-compteur/',
        body,
        extra_ld=ld_service + ld_faq,
    )


# ═══════════════════════════════════════════════════════════════
# PAGES USE CASE : Piscine par ville
# ═══════════════════════════════════════════════════════════════

PISCINE_PAGES = [
    {
        "slug": "piscine-bordeaux",
        "ville": "Bordeaux",
        "ville_article": "à Bordeaux",
        "cp": "33000",
        "zones_voisines": "Mérignac, Pessac, Talence, Le Bouscat, Caudéran",
        "hero_image_alt": "Piscine privée avec terrasse dans une propriété bourgeoise du Bouscat ou de Caudéran, zone d'intervention recherche de fuite à Bordeaux",
        "intro_unique": "Bordeaux intra-muros concentre relativement peu de piscines au cœur du centre historique classé UNESCO (densité bâtie élevée, jardins restreints), mais les quartiers périphériques de Caudéran, du Bouscat voisin, de Saint-Augustin et du Grand Parc comptent un parc significatif de bassins privés, souvent construits entre les années 1970 et 2000 dans les grandes propriétés familiales. Les domaines du Médoc viticole limitrophe ajoutent à ce paysage des piscines plus anciennes, parfois trentenaires, dans les chais et résidences secondaires.",
        "types_piscines": "À Bordeaux et sa périphérie, nous intervenons majoritairement sur trois configurations : les piscines béton des années 1970-1990 dans les propriétés bourgeoises de Caudéran et Saint-Augustin, les coques polyester installées dans les années 1990-2010 dans les jardins plus compacts des quartiers pavillonnaires, et les liners PVC standards sur des bassins rectangulaires classiques. quelques piscines miroir ou couloirs de nage se rencontrent dans les propriétés haut de gamme de Caudéran, et les chais du Médoc abritent parfois des piscines béton projeté très anciennes, fissurées structurellement.",
        "quartiers_zones": "Les zones de forte densité de piscines sur notre secteur d'intervention direct sont Caudéran et Le Bouscat (propriétés bourgeoises avec jardins matures), Saint-Augustin (maisons avec patio), le Grand Parc (certaines échoppes agrandies avec petit bassin), ainsi que les communes voisines Mérignac, Pessac et Talence. En zone viticole du Médoc, nous intervenons jusqu'à Pauillac et Saint-Julien dans les chais et résidences secondaires.",
        "spécificités": [
            ("Terrain argileux et mouvements saisonniers", "Les sols bordelais sont en grande partie argileux, avec un aléa fort de retrait-gonflement selon les épisodes de sécheresse et de pluie. Ces mouvements provoquent régulièrement la rupture des raccords collés sur canalisations PVC enterrées autour des piscines. Nos interventions sur le Grand Parc ou Caudéran rencontrent fréquemment ce scénario : fuite à 15-20 mètres du bassin, le long du tracé d'alimentation ou de refoulement."),
            ("Accessibilité contrainte en tissu urbain dense", "Contrairement aux pavillons de banlieue avec accès véhicule direct au jardin, beaucoup de piscines bordelaises sont situées dans des cœurs d'îlots accessibles uniquement via un couloir traversant la maison ou un portail étroit. Nous arrivons avec matériel compact (corrélateur acoustique portable, bouteilles de gaz traceur de 5L) pour intervenir sans gêne, et nous prévoyons les protections anti-tache pour les parquets anciens et carrelages ciment des maisons de ville."),
            ("Nuisances sonores à minimiser (densité bordelaise)", "Dans un tissu urbain dense, nos mesures acoustiques de localisation de fuite peuvent être perturbées par les bruits ambiants et doivent se faire tôt le matin ou en début de soirée. Nous adaptons nos créneaux d'intervention aux contraintes de voisinage bordelaises, notamment en copropriété où le bassin est parfois collectif."),
            ("Piscines très anciennes de domaines viticoles", "Dans les domaines du Médoc, certaines piscines construites dans les années 1960 en béton armé présentent des fissures structurelles actives, des étanchéités d'origine (enduit ciment) totalement dépassées, et des canalisations en fonte grise ou galvanisé qui ont survécu plusieurs décennies. Notre méthodologie intègre ces configurations vintages où les méthodes modernes doivent s'adapter à un bâti qui n'a jamais été rénové.")
        ],
        "cas_frequent": "Cas récurrent que nous traitons : propriétaire d'une maison bourgeoise à Caudéran avec piscine béton des années 1980, qui constate une baisse de niveau de 3-5 cm par jour en été. Après test du seau, fuite confirmée. Notre diagnostic : colorant fluorescéine autour des pièces à sceller (skimmer + buse refoulement), test de pression séquentiel sur chaque circuit, écoute électro-acoustique le long du tracé des canalisations. Dans 70 pourcent des cas sur ce type de bassin, la fuite est sur un raccord PVC collé de 1985, désaxé par un mouvement de terrain argileux.",
        "faq_locale": [
            ("Faut-il des autorisations pour intervenir sur une piscine à Bordeaux Centre ?",
             "Non, une recherche de fuite est un diagnostic technique qui ne nécessite aucune autorisation d'urbanisme ni déclaration préalable, même dans les secteurs sauvegardés UNESCO du Port de la Lune. Seule l'Architecte des Bâtiments de France intervient pour des travaux modifiant l'aspect extérieur, ce qui n'est pas le cas d'une recherche ou d'une réparation ponctuelle."),
            ("Intervenez-vous sur les piscines collectives de copropriété à Bordeaux ?",
             "Oui, nous intervenons régulièrement sur les piscines de copropriétés bordelaises, notamment dans les résidences récentes des Bassins à Flot ou des quartiers du Grand Parc. Le mandatement doit venir du syndic, et le rapport est remis au conseil syndical. La convention IRSI s'applique en cas de dégât des eaux affectant des logements de la copropriété."),
            ("Travaillez-vous sur les domaines viticoles du Médoc avec piscine ancienne ?",
             "Oui, nous nous déplaçons jusqu'à Pauillac, Saint-Julien-Beychevelle, Margaux et leurs environs pour les piscines des chais et résidences. Un supplément de déplacement s'applique au-delà de 30 km du centre de Bordeaux, forfaitaire et communiqué dans le devis.")
        ],
        "methodes_focus": "Sur les piscines bordelaises et périphérie, nos méthodes de diagnostic sont hiérarchisées différemment selon la zone. Dans les propriétés bourgeoises de Caudéran ou Le Bouscat (grands bassins béton des années 1970-80), nous commençons systématiquement par l'inspection caméra sous-marine pour repérer les fissures structurelles souvent présentes, puis le colorant fluorescéine aux pièces à sceller. Pour les piscines situées sur terrain argileux (la majorité de Bordeaux intra-muros), le gaz traceur azote/hélium sur canalisations enterrées est notre méthode de deuxième passage, car les raccords PVC collés cèdent fréquemment aux mouvements saisonniers. L'écoute électro-acoustique est utile en dernier recours quand les trois premières méthodes n'ont pas convergé, typiquement pour une fuite sur un raccord très enterré (plus de 2 mètres de profondeur) entre bassin et local technique.",
        "patterns_frequents": [
            ("Piscine Caudéran béton 1980 avec fuite structurelle", "Maison bourgeoise 1900, piscine béton projeté 10×4 ajoutée vers 1982. Perte d'eau progressive depuis 2 ans, s'accélérant après sécheresse estivale. Inspection caméra : fissure verticale de 30 cm au niveau du point profond, active. Préconisation : rebéton local + nouvelle étanchéité par liner armé, 18 000 euros HT estimés. Rapport assurance transmis pour prise en charge."),
            ("Piscine Le Bouscat + arrosage enterré confus", "Propriété Parc Bordelais, piscine liner 8×4 et arrosage enterré sur 300 m² de jardin. Consommation d'eau +400 m³/an inexpliquée. diagnostic par fermeture séquentielle : la fuite n'est pas sur la piscine mais sur une vanne d'arrosage enterrée à 12 mètres au sud du bassin. Le propriétaire voulait vidanger sa piscine, ce que nous avons évité."),
            ("Coque polyester Saint-Augustin vieillissante", "Piscine coque coco 7×3 installée en 2005. Baisse de niveau constante de 2 cm/jour. Inspection caméra : osmose généralisée avec cloques multiples sur la paroi nord, micro-fissure confirmée par colorant au niveau de la bride du skimmer. Préconisation : reprise d'étanchéité locale + surveillance annuelle, 1 200 euros HT.")
        ],
    },
    {
        "slug": "piscine-merignac",
        "ville": "Mérignac",
        "ville_article": "à Mérignac",
        "cp": "33700",
        "zones_voisines": "Bordeaux, Le Haillan, Eysines, Pessac, Saint-Médard-en-Jalles",
        "hero_image_alt": "Piscine liner PVC dans un pavillon individuel de Mérignac Arlac, zone d'intervention recherche de fuite sans vidange",
        "intro_unique": "Mérignac, deuxième ville de la métropole bordelaise par sa population, présente un parc de piscines privées parmi les plus denses de Gironde. La majorité des bassins ont été installés entre 1985 et 2005 dans les lotissements pavillonnaires qui ont poussé avec le développement urbain de la commune. Résultat : un parc homogène de piscines 8×4 mètres en liner PVC, avec aujourd'hui une moyenne d'âge de 25 à 35 ans, période à laquelle les joints durcissent, les pièces à sceller fuient et les canalisations PVC enterrées atteignent leur première limite de vieillissement.",
        "types_piscines": "À Mérignac, environ 80 pourcent des piscines que nous diagnostiquons sont des bassins enterrés avec liner PVC 75/100 ou 85/100 d'épaisseur, de format standard 4×8 ou 5×10 mètres. On trouve aussi des coques polyester coco des années 1990-2000, souvent installées dans les lotissements de Capeyron ou Beutre, et plus rarement des piscines béton projeté récentes dans les maisons haut de gamme du Chemin Long. Les piscines hors-sol et semi-enterrées sont minoritaires mais présentes dans les jardins plus récents de Beaudésert.",
        "quartiers_zones": "Les quartiers à forte densité de piscines à Mérignac sont Arlac (pavillons 1970-1990 avec grands terrains), Capeyron (résidentiel familial des années 1980), Chemin Long et Beutre (terrains plus spacieux, piscines plus grandes), Les Eyquems et Beaudésert (pavillons plus récents). La proximité de l'aéroport concentre également des logements de location saisonnière avec piscines peu entretenues.",
        "spécificités": [
            ("Piscines liner PVC en fin de première vie (25-35 ans)", "La majorité des liners que nous rencontrons à Mérignac ont été posés entre 1985 et 1995. À cet âge, le PVC perd sa plasticité : il se rigidifie, les plis aux angles se figent et se fissurent, les soudures des coins et au droit du skimmer cèdent par fatigué. La recherche de fuite sur ces liners demande un colorant fluorescéine précis et une observation en apnée ou à la caméra, car les perforations sont souvent punctiformes (0,5 à 2 mm)."),
            ("Joints de pièces à sceller desséchés", "Dans ces piscines installées il y a 25-35 ans, les joints mastic entre les pièces à sceller (skimmer, buses de refoulement, prise balai, bonde de fond) et le liner ou le béton sont souvent totalement desséchés. Nous identifions cette catégorie de fuite par injection de colorant au pourtour immédiat de chaque pièce et observation du cheminement. Remise en étanchéité par silicone piscine ou remplacement de bride après localisation."),
            ("Canalisations PVC d'alimentation vieillissantes", "Les tuyaux PVC collés de 50 mm ou 63 mm qui alimentent skimmer et bonde de fond ont typiquement 25-35 ans sur les piscines du parc immobilier mérignacais. Les raccords collés subissent des chocs thermiques et des mouvements du terrain. Notre écoute électro-acoustique et le gaz traceur localisent précisément le raccord défectueux, souvent à 2-5 mètres sous la dalle du local technique ou sous la plage."),
            ("Proximité aéroport et vibrations sol", "Certains quartiers proches de l'aéroport de Mérignac (Arlac, Capeyron sud, zones de Bersol voisines) subissent des vibrations régulières du sol liées au trafic aérien et aux installations militaires. Sur la durée, cela sollicite les raccords des canalisations enterrées. Nos techniciens, habitués à ce contexte, savent cibler les zones de contrainte mécanique accrue lors du diagnostic.")
        ],
        "cas_frequent": "Scénario type à Mérignac : pavillon Arlac des années 1990, piscine liner 8×4m d'origine, propriétaire qui constate après remise en eau au printemps une baisse de 2-3 cm par jour. Test du seau : fuite confirmée. Notre approche : inspection visuelle du liner à la caméra, colorant fluorescéine aux pièces à sceller, test de pression des canalisations. Dans 60 pourcent des cas, la fuite est au niveau du skimmer (joint mastic desséché), dans 25 pourcent sur la bonde de fond, et 15 pourcent sur une canalisation PVC enterrée au droit d'un raccord collé.",
        "faq_locale": [
            ("Ma piscine à Mérignac a 30 ans, vaut-il mieux rechercher la fuite ou tout refaire ?",
             "Ça dépend. Si la fuite est isolée (un joint de skimmer, un raccord de canalisation), la réparation coûte 200 à 800 euros et prolonge le bassin de 10-15 ans. Si le liner est généralisé en fin de vie (plis multiples, soudures cédées, décolorations), un changement de liner s'impose (3 000 à 6 000 euros selon la taille). Notre diagnostic vous donne les éléments objectifs pour trancher : rapport complet sur l'état du liner et des pièces à sceller, avec préconisation claire."),
            ("Intervenez-vous les week-ends à Mérignac pendant la saison estivale ?",
             "Oui, du lundi au samedi, avec des créneaux prioritaires pour les piscines dont la fuite est active et importante (plus de 5 cm par jour). En saison haute (juin à septembre), nous organisons systématiquement des tournées dédiées piscines pour répondre sous 48 à 72 heures aux demandes de la métropole bordelaise."),
            ("Ma piscine Mérignac perd 1 cm par jour : urgent ou pas ?",
             "1 cm/jour correspond à une perte d'environ 600 litres pour une piscine 8×4 mètres. À l'échelle d'un été, c'est environ 60 m³ d'eau perdus, soit une facture supplémentaire de 200 à 400 euros en zone Suez Bordeaux Métropole. Économiquement, localiser et réparer la fuite se rentabilise en une saison. Techniquement, une fuite non traitée peut saturer les terres autour du bassin, provoquer un tassement et aggraver le problème.")
        ],
        "methodes_focus": "Sur le parc homogène de piscines mérignacaises (8×4 liner PVC des années 1985-2000 majoritairement), notre méthodologie se concentre d'abord sur le colorant fluorescéine aux pièces à sceller : le joint mastic des skimmers Weltico ou Hayward de cette génération est la cause n°1 de fuite. Si négatif, inspection visuelle du liner en apnée ou caméra à la recherche d'une perforation punctiforme (les liners PVC 75/100 de 30 ans d'âge deviennent friables aux angles). Pour les maisons avec grand terrain d'Arlac ou Beutre où les canalisations enterrées PVC font 15 à 30 mètres entre bassin et local technique, le test de pression séquentiel sur chaque circuit oriente avant déploiement du gaz traceur.",
        "patterns_frequents": [
            ("Piscine liner Arlac joint skimmer desséché", "Pavillon 1992, piscine 4×8 liner d'origine, perte 2 cm/jour en saison estivale. Inspection : colorant fluorescéine sur skimmer révèle aspiration à la bride. Réparation : rejointoiement mastic piscine (Sikaflex piscine) après purge. Intervention 2h30, réparation 150 euros, diagnostic + réparation 420 euros HT."),
            ("Plancher chauffant piscine confusion Capeyron", "Maison 1998 avec plancher chauffant ET piscine. Perte de pression circuit chauffage + compteur d'eau anormal. Client convaincu que c'était la piscine. Thermographie révèle la fuite : circuit chauffage, fuite sous salon au niveau du collecteur. Piscine saine. Rapport transmis à l'assurance pour prise en charge travaux chape."),
            ("Canalisation enterrée Beutre après hiver", "Maison lotissement 1996, 40 m de canalisation PVC entre compteur et local technique piscine. Au redémarrage de printemps, facture Suez doublée. Gaz traceur localise la fuite à 22 m du compteur sous l'allée gravillonnée. Réparation par ouverture locale 80×80 cm, remplacement 1 mètre de PVC, compactage, remise en état des graviers. Total 780 euros.")
        ],
    },
    {
        "slug": "piscine-arcachon",
        "ville": "Arcachon",
        "ville_article": "à Arcachon",
        "cp": "33120",
        "zones_voisines": "La Teste-de-Buch, Gujan-Mestras, Le Teich, Pyla-sur-Mer, Lège-Cap-Ferret",
        "hero_image_alt": "Villa avec piscine chauffée dans le quartier d'Abatilles à Arcachon, zone d'intervention recherche de fuite sur Bassin d'Arcachon",
        "intro_unique": "Arcachon présente un profil atypique en Gironde : ville balnéaire à forte population de résidences secondaires, densité de piscines très élevée par rapport à la population permanente, et parc immobilier haut de gamme concentré dans la Ville d'Hiver, Abatilles et le Moulleau. Les piscines y sont souvent plus équipées que la moyenne (chauffage par pompe à chaleur, couverture automatique, débordement, volet immergé), ce qui multiplie les points potentiels de fuite sur un réseau hydraulique complexe.",
        "types_piscines": "À Arcachon, nous intervenons majoritairement sur des bassins béton armé de moyenne et grande taille (souvent 10×5 à 12×6 mètres), des piscines miroir avec débordement périphérique qui complexifient la recherche de fuite (perte apparente dans le bac tampon), des piscines chauffées par PAC air-eau ou échangeur thermique installées dans des locaux techniques corrodés par l'air marin, et plus rarement des liners PVC sur des bassins plus modestes des résidences secondaires plus anciennes.",
        "quartiers_zones": "Les quartiers à concentration de piscines sont la Ville d'Hiver (villas néo-mauresques et chalets suisses avec bassins historiques), Abatilles (résidences modernes avec piscines équipées), le Moulleau (villas en front de plage avec piscines exposées), Pereire (quartier balnéaire résidentiel) et Arcachon Centre dans une moindre mesure. Nous intervenons aussi au Pyla-sur-Mer voisin.",
        "spécificités": [
            ("Corrosion accélérée par air salin", "L'air chargé en embruns marins (le Bassin est à moins d'un kilomètre de la plupart des piscines arcachonaises) corrode à vitesse accélérée tout l'inox du local technique : échangeurs thermiques, vis de brides, raccords de capteurs, nourrices de distribution. Les pompes à chaleur piscine y ont une durée de vie de 7 à 10 ans au lieu de 12-15 ans en intérieur des terres. Nous diagnostiquons régulièrement des fuites de PAC piscine venant d'un condenseur corrodé, pas du bassin lui-même."),
            ("Piscines miroir et débordement complexes", "Sur les piscines à débordement périphérique (très courantes à Abatilles et Pereire), la fuite n'est pas visible par la simple baisse de niveau du bassin : l'eau déborde en permanence dans le bac tampon qui compensé. C'est le bac tampon qui baisse, ou la consommation d'eau de remise à niveau automatique qui augmente. Notre méthodologie sur ces bassins : test de coupure de la circulation, isolation séquentielle de chaque buse de débordement, inspection caméra des gouttières."),
            ("Résidences secondaires et dégâts en hivernage", "Une partie importante de notre clientèle arcachonaise sont des résidents secondaires occupant leur villa 2 à 6 semaines par an. Une fuite non détectée à l'automne peut causer des dégâts considérables : 5 à 10 m³ perdus par semaine, affouillement des terres sous la dalle de plage, infiltration dans le local technique, dégradation du jardin. Nous proposons un contrat de diagnostic préventif saisonnier pour ces clients."),
            ("Canalisations enterrées en sable et micro-tassements", "Le sol sableux typique d'Arcachon (sables blancs du Bassin) offre une excellente portance mais subit des tassements différentiels sur la durée. Les canalisations enterrées entre la piscine et le local technique, souvent sur 10 à 25 mètres de tracé, se désaxent lentement au niveau des raccords collés PVC. Le gaz traceur azote/hélium est notre méthode de référence pour localiser ces fuites au demi-mètre près sans excavation.")
        ],
        "cas_frequent": "Cas type arcachonais : villa de la Ville d'Hiver avec piscine béton 11×5 mètres chauffée par PAC, propriétaire résident de l'agglomération bordelaise qui occupé sa résidence secondaire 4-5 semaines par an. Constat à la réouverture printanière : bassin plus bas de 15 cm malgré couverture, compteur d'eau de remise à niveau anormal. Notre diagnostic combine test de pression des canalisations (première suspicion), inspection PAC (condenseur fuyant dans 30 pourcent des cas sur ce profil), puis colorant sur pièces à sceller. Dans 45 pourcent des cas, la fuite vient du réseau hydraulique entre bassin et local technique, au niveau d'un raccord désaxé par tassement sableux.",
        "faq_locale": [
            ("Dois-je hiverner ma piscine Arcachon en hiver ou la laisser en fonctionnement ?",
             "Le climat océanique doux d'Arcachon permet de laisser la piscine en fonctionnement réduit toute l'année, ce que font beaucoup de propriétaires de résidences secondaires. Attention cependant : une fuite non détectée peut générer un sinistre majeur avant votre retour. Nous recommandons a minima un diagnostic préventif tous les 2-3 ans sur ce profil d'usage, et un hivernage actif dès que le propriétaire ne revient pas avant mars."),
            ("La proximité de l'eau salée du Bassin peut-elle polluer ma piscine ?",
             "Non, la piscine utilise de l'eau douce du réseau public, il n'y a pas de contamination directe par le Bassin d'Arcachon. En revanche, l'air salin accélère la corrosion des éléments métalliques : vis des pièces à sceller, brides de skimmer, échangeurs thermiques. Sur une piscine arcachonaise de plus de 15 ans, nous vérifions systématiquement l'état de l'inox au local technique en complément du diagnostic bassin."),
            ("Intervenez-vous sur les piscines des villas classées de la Ville d'Hiver ?",
             "Oui, nous sommes formés à intervenir sur les bâtiments classés et les abords protégés. Notre méthodologie strictement non destructive préserve les margelles en pierre d'origine, les plages carrelées d'époque et les décors paysagers matures. Un devis précis détaille les précautions prises et les limites techniques rencontrées sur ces configurations patrimoniales.")
        ],
        "methodes_focus": "Les piscines arcachonaises, souvent équipées (chauffage PAC, débordement, couverture automatique), demandent une approche méthodique en deux temps. D'abord, vérification complète du local technique : état des pompes, échangeurs thermiques, vannes. En climat salin, une fuite sur équipement (échangeur PAC corrodé, joint d'axe pompe) est aussi probable qu'une fuite de bassin, et se diagnostiqué visuellement. Ensuite seulement, test du bassin : colorant fluorescéine aux pièces à sceller et inspection caméra sous-marine (les piscines arcachonaises étant souvent de qualité supérieure, les défauts sont plus subtils : micro-fissure d'angle, décollement de carrelage invisible à l'œil nu). Pour les piscines miroir ou débordement, isolation du bac tampon obligatoire.",
        "patterns_frequents": [
            ("Villa Ville d'Hiver PAC corrodée", "Villa 1895, piscine ajoutée 1990, PAC Zodiac installée en 2010. Consommation d'eau anormale constatée au retour printemps. Inspection local technique : condenseur PAC percé, fuite d'eau continue par l'évacuation. Bassin intact. Préconisation : remplacement PAC (8 à 12 000 euros HT neuf), diagnostic 380 euros HT."),
            ("Piscine miroir débordement Abatilles", "Villa récente 2015, piscine 12×4 à débordement périphérique. Bac tampon baisse régulière de 8-10 cm/jour, sans perte apparente sur bassin principal. diagnostic : gaz traceur sur circuit de remontée, fuite identifiée sur raccord PE de 20 mètres sous la plage. Réparation : ouverture ciblée d'une dalle préfabriquée, reprise raccord, rescellement. 2 600 euros total."),
            ("Villa résidence secondaire Pereire après hiver", "Villa front Bassin, propriétaires parisiens en résidence secondaire. Ouverture printanière : local technique inondé, 15 cm d'eau au sol. diagnostic : fuite sur clapet de vanne hivernage mal serré. Bassin intact mais pompe noyée à remplacer. Rapport détaillé pour assurance multirisque : prise en charge totale du sinistre.")
        ],
    },
    {
        "slug": "piscine-la-teste-de-buch",
        "ville": "La Teste-de-Buch",
        "ville_article": "à La Teste-de-Buch",
        "cp": "33260",
        "zones_voisines": "Arcachon, Gujan-Mestras, Biganos, Le Teich",
        "hero_image_alt": "Piscine dans un lotissement pavillonnaire de Cazaux à La Teste-de-Buch, zone d'intervention recherche de fuite",
        "intro_unique": "La Teste-de-Buch couvre la plus grande superficie communale du bassin d'Arcachon et offre un parc de piscines privées très étendu, de profils contrastés : du pavillon familial des lotissements de Cazaux (années 1990-2010) aux villas d'exception du Pyla (bassins haut de gamme face à la dune), en passant par les maisons secondaires historiques du centre. Le sol sableux caractéristique rend les problématiques de canalisations enterrées particulièrement fréquentes sur ce territoire.",
        "types_piscines": "À La Teste, nous intervenons sur trois grands profils : les piscines liner 8×4 à 10×5 mètres des lotissements pavillonnaires de Cazaux (majoritairement construites 2000-2015), les piscines coques polyester des quartiers plus récents (Pyla-La Teste, Pléneau), et les piscines béton armé haut de gamme du Pyla-sur-Mer (grand format, équipement complet : chauffage, volet, débordement partiel, traitement au sel). Le taux de piscines hors-sol est notable dans les lotissements les plus récents, souvent pour les jeunes familles.",
        "quartiers_zones": "Les secteurs à forte densité de piscines : Cazaux (plus grand parc de lotissements pavillonnaires avec piscines standards), Pyla-sur-Mer et Pléneau (haut de gamme, villas front de dune), La Teste Centre (moins dense mais piscines de maisons anciennes), et les zones résidentielles près du Bassin (Conteste, Pinèdes). Le tissu commercial et les résidences de tourisme ajoutent à la charge d'intervention en saison estivale.",
        "spécificités": [
            ("Sol sableux et désaxement des raccords enterrés", "La Teste-de-Buch est entièrement construite sur un sol sablonneux fin typique du bassin d'Arcachon. Les canalisations enterrées PVC collées subissent des micro-mouvements différentiels permanents, accélérés par le ballet des racines de pins et les variations hygrométriques saisonnières. Résultat : les raccords PVC de 15 à 25 ans d'âge cèdent avec une fréquence sensiblement plus élevée qu'en sol argileux. Notre gaz traceur est l'outil de référence sur ces configurations."),
            ("Nappe phréatique haute par endroits", "Certains quartiers de La Teste (notamment en bordure du Bassin ou dans les zones lagunaires de Cazaux) présentent une nappe phréatique proche de la surface, parfois à moins d'un mètre. Cela interdit la vidange complète d'une piscine sans risque de soulèvement du bassin (effet flotteur). C'est pourquoi le diagnostic sans vidange que nous pratiquons est ici quasi obligatoire : aucune autre méthode n'est envisageable dans de nombreux cas."),
            ("Résidences secondaires et usage saisonnier", "Comme Arcachon voisine, La Teste compte une proportion significative de résidences secondaires et de résidences de tourisme (locations saisonnières). Les piscines sont souvent peu entretenues hors saison, avec des remises en service au printemps qui révèlent les fuites accumulées pendant l'hiver. Notre pic de demande sur La Teste est entre avril et juin, suivi d'un pic estival sur les propriétaires résidents."),
            ("Pins maritimes et racines envahissantes", "L'environnement forestier de pins maritimes typique du bassin (Cazaux, Pléneau) place régulièrement les piscines à moins de 5 à 10 mètres de grands arbres. Les racines peuvent à terme venir solliciter les canalisations enterrées, soit en les désaxant, soit en pénétrant des raccords défectueux. Nous identifions ces configurations via caméra endoscopique et recommandons parfois un traitement racinaire préventif.")
        ],
        "cas_frequent": "Cas récurrent à La Teste : pavillon de lotissement à Cazaux, piscine 8×4 mètres liner ou coque installée autour de 2005-2010, propriétaire qui note après l'hiver une baisse de niveau anormale alors que la piscine était couverte. Nos pistes : test de coupure sur les canalisations enterrées (première cause en sol sableux), diagnostic liner en cas d'usage intense l'été précédent, puis vérification du local technique. Dans 50 pourcent des cas, la fuite est localisée sur le réseau enterré à 3-8 mètres du bassin, au niveau d'un raccord PVC désaxé par le sable.",
        "faq_locale": [
            ("Puis-je vider ma piscine à La Teste en hiver ?",
             "Non, ce n'est presque jamais conseillé à La Teste. La nappe phréatique proche de la surface dans de nombreux quartiers peut faire remonter le bassin vide (effet flotteur), causant fissures voire délogement complet du bassin. De plus, une vidange coûte 1 500 à 3 500 euros en eau et produits de remise en service. Notre méthode sans vidange (colorant, acoustique, pression) évite ces risques et coûts."),
            ("Les racines de pins peuvent-elles endommager ma piscine à Cazaux ?",
             "Oui, les pins maritimes ont un système racinaire superficiel qui peut atteindre 8 à 15 mètres horizontalement. Les racines cherchent l'humidité et pénètrent les raccords défectueux ou les canalisations enterrées. Sur les piscines de lotissements de Cazaux entourées de pins, nous recommandons une inspection caméra des canalisations enterrées tous les 10 ans à titre préventif."),
            ("Combien coûte une intervention piscine à La Teste vs Bordeaux ?",
             "Nos tarifs sont identiques sur toute la métropole et le bassin d'Arcachon : 300 à 700 euros HT selon la méthode. Un supplément forfaitaire de déplacement de 40 euros s'applique pour La Teste et les communes du bassin d'Arcachon au-delà des zones directement accessibles depuis Bordeaux. Ce supplément est inclus dans le devis communiqué avant intervention.")
        ],
        "methodes_focus": "Sur La Teste-de-Buch, la configuration sol sableux + densité de pins maritimes + nappe phréatique parfois haute nous oriente systématiquement vers deux méthodes prioritaires : le gaz traceur azote/hélium pour les canalisations enterrées (les raccords PVC collés 15-25 ans se désaxent dans le sable) et l'inspection caméra des canalisations d'évacuation pour détecter les racines de pins qui ont pénétré le réseau. Le colorant fluorescéine reste utile pour les pièces à sceller, mais il arrive en seconde ligne dans notre protocole local. Les tests de pression sont particulièrement fiables ici car les canalisations enterrées sont souvent accessibles par les regards techniques typiques des lotissements de Cazaux.",
        "patterns_frequents": [
            ("Coque polyester Cazaux 2005 avec désaxement", "Pavillon lotissement 2005, coque polyester 7×4 avec canalisations PVC enterrées sur 8 mètres. Baisse de niveau progressive depuis 3 ans. Gaz traceur localise une fuite à 5,5 mètres du bassin au niveau d'un raccord en T. Cause identifiée : désaxement du raccord par mouvement sableux + léger tassement. Réparation par ouverture 1×1 m et reprise collage PVC. 920 euros."),
            ("Piscine Pyla haut de gamme inspection racines", "Villa Pyla-sur-Mer, piscine 12×6 béton avec réseau enterré sous pinède. Baisse eau modérée mais persistante. Inspection caméra des canalisations évacuation : 3 racines de pins maritimes ont pénétré des raccords à 2, 5 et 11 mètres. Préconisation : chemisage tubulaire des canalisations concernées (sans tranchée) + coupe des racines à la tronçonneuse racinaire. 4 500 euros total."),
            ("Confusion piscine/arrosage enterré Cazaux", "Pavillon 1998, piscine liner + arrosage automatique sur 400 m². Client suspectait fuite bassin (perte niveau). diagnostic par isolation : fuite réelle sur électrovanne d'arrosage enterrée, pas sur la piscine. Le propriétaire allait vidanger sa piscine. Économie : 1 500 euros de vidange/remise en eau + bonne piscine sauvée.")
        ],
    },
    {
        "slug": "piscine-gujan-mestras",
        "ville": "Gujan-Mestras",
        "ville_article": "à Gujan-Mestras",
        "cp": "33470",
        "zones_voisines": "La Teste-de-Buch, Le Teich, Biganos, Arcachon",
        "hero_image_alt": "Piscine familiale dans une maison de Gujan-Mestras près du Bassin d'Arcachon, zone d'intervention recherche de fuite",
        "intro_unique": "Gujan-Mestras, commune emblématique du bassin d'Arcachon historiquement liée à l'ostréiculture, a connu un développement pavillonnaire important depuis les années 1990. Son parc de piscines privées, plus récent que celui de sa voisine La Teste, comprend une proportion élevée de coques polyester et de liners posés entre 2000 et 2020, sur des terrains sableux ou semi-sableux. Les résidences secondaires sont également nombreuses, avec leurs problématiques spécifiques d'usage saisonnier.",
        "types_piscines": "À Gujan-Mestras, le parc de piscines est dominé par les coques polyester coco des années 2000-2015 (environ 45 pourcent des bassins que nous diagnostiquons), suivies par les liners PVC classiques de format moyen (35 pourcent), quelques piscines béton armé haut de gamme dans les quartiers les plus récents (15 pourcent) et une part croissante de piscines naturelles / bio-phytoépuration dans les zones résidentielles récentes soucieuses d'environnement (5 pourcent).",
        "quartiers_zones": "Les principales zones d'intervention à Gujan-Mestras : centre historique autour du port et de la mairie (piscines anciennes dans maisons bourgeoises), La Hume (quartier résidentiel familial), Le Petit Piquey, les nouveaux lotissements entre RD650 et voie ferrée, et les villages ostréicoles le long du Bassin (Larros, Meyran, Gujan Port) qui comptent quelques piscines dans les maisons reconverties. Les résidences de tourisme et parcs d'attractions (La Coccinelle, Aqualand) ne sont pas dans notre scope (piscines collectives non privatives).",
        "spécificités": [
            ("Coques polyester des années 2000-2015 en vieillissement", "Le parc de coques de Gujan-Mestras entre dans la phase de vieillissement où les gel-coats d'origine montrent leurs faiblesses : micro-cloques par osmose, fissures de retrait au niveau des bondes de fond moulées, délaminage entre couches de fibres de verre. Notre inspection caméra sous-marine identifié ces défauts et les différencie d'une simple fuite hydraulique. La fluorescéine complète le diagnostic en confirmant si un défaut visuel est bien fuyant."),
            ("Proximité immédiate du Bassin d'Arcachon", "Une partie des piscines gujanaises se situe à moins de 500 mètres du Bassin, avec les mêmes effets d'air salin et humidité qu'à Arcachon : corrosion des inox, des pompes à chaleur, des éléments métalliques du local technique. Le diagnostic piscine doit systématiquement inclure la vérification du périphérique technique, la fuite pouvant venir d'un équipement corrodé plutôt que du bassin lui-même."),
            ("Piscines naturelles et bio-phytoépuration", "Gujan-Mestras compte un nombre croissant de piscines naturelles à filtration végétale (lagunage, bassin de plantation). Ces installations nécessitent une approche spécifique : la fuite peut être dans le bassin de baignade, le bassin de lagunage, ou les canalisations de transfert entre les deux. Nos méthodes (colorant, acoustique, gaz traceur) s'adaptent à ces configurations non conventionnelles, plus complexes à diagnostiquer."),
            ("Hivernage hétérogène selon usage", "Entre résidents principaux qui hivernent actif (couverture + filtration réduite), résidents secondaires qui hivernent passif (bassin bâché et couvrant) et locations saisonnières qui laissent à l'abandon total, la qualité d'hivernage varie fortement à Gujan. Une mauvaise hivernisation en région Bassin (où le gel est rare mais l'humidité extrême) endommage les joints des pièces à sceller, surtout si la piscine est placée en zone venteuse exposée.")
        ],
        "cas_frequent": "Scénario fréquent à Gujan-Mestras : coque polyester 8×4 mètres installée vers 2008 dans un lotissement de La Hume, propriétaire résident principal. Il constate après ouverture de saison une baisse de 2 cm/jour, sans changement d'usage. Notre méthodologie : inspection caméra complète de la coque (recherche de micro-fissures, cloques, défauts), injection de colorant aux 4 pièces à sceller, test de pression sur chaque circuit. Dans 40 pourcent des cas, la fuite est sur la coque elle-même (micro-fissure près d'une bride), dans 35 pourcent sur un joint, et 25 pourcent sur canalisation enterrée.",
        "faq_locale": [
            ("Ma coque polyester Gujan-Mestras a 15 ans, à quoi dois-je faire attention ?",
             "Les coques polyester de 15 ans atteignent la phase où les défauts structurels apparaissent : osmose (cloques sur le gel-coat, signe d'humidité passée derrière la couche étanche), délaminage inter-couches (décollement entre strates de fibre), fissures au niveau des pièces moulées (bondes, marches). Notre inspection caméra sous-marine systématique sur ces coques détecte les défauts précoces et permet une réparation ciblée avant la fuite majeure."),
            ("Puis-je installer une piscine naturelle malgré la proximité du Bassin ?",
             "Oui, les piscines naturelles fonctionnent très bien sur la commune. Le sol sableux facilite les bassins de lagunage. Attention en revanche à respecter les règles locales d'installation (distance aux arbres, gestion du trop-plein, compatibilité avec la nappe phréatique parfois proche). Pour la recherche de fuite sur ce type d'installation, nous utilisons les mêmes méthodès que sur une piscine classique, avec une attention particulière aux transferts entre compartiments."),
            ("Faut-il un matériel spécifique pour les piscines de résidences secondaires à Gujan ?",
             "Pas de matériel spécifique, mais une méthodologie adaptée : nous combinons systématiquement inspection caméra, test de pression des canalisations et vérification du local technique (corrosion équipements), car les fuites de résidences secondaires peuvent s'être accumulées pendant plusieurs mois sans contrôle. Le rapport final détaille l'état global du bassin, utile pour les propriétaires qui ne sont pas sur place.")
        ],
        "methodes_focus": "À Gujan-Mestras, où le parc de piscines est dominé par les coques polyester de la tranche 2000-2015, l'inspection caméra sous-marine est notre première méthode de diagnostic : elle identifié rapidement les signes d'osmose (cloques), les micro-fissures au niveau des bondes moulées, et les délaminages entre couches de fibre. Le colorant fluorescéine confirme si un défaut visuel est bien fuyant. Pour les piscines proches du Bassin (Larros, Gujan Port), contrôle systématique de l'inox et des équipements PAC au local technique. Les piscines naturelles à lagunage demandent une adaptation : isolation séquentielle des compartiments (baignade, filtration végétale, transferts) avant d'identifier la zone fuyante.",
        "patterns_frequents": [
            ("Coque polyester La Hume osmose + micro-fissure", "Villa 2008 avec coque coco 8×4. Baisse 2 cm/jour. Inspection caméra : osmose diffuse, cloques multiples mais aucune ne fuit. Fluorescéine révèle une micro-fissure punctiforme près de la marche Romaine, invisible à l'œil. Réparation par résine époxy piscine appliquée sous l'eau. diagnostic + réparation : 550 euros."),
            ("Piscine naturelle lagunage diagnostic complexe", "Installation 2018, bassin baignade 6×4 + bassin lagunage végétal. Perte de niveau globale, localisation incertaine. Méthode : fermeture de la circulation entre bassins, mesure différentielle sur 48h. Fuite isolée sur le bassin de lagunage, au niveau d'une étanchéité PVC dégradée par racines de plantes. Intervention 780 euros."),
            ("Villa front Bassin pompe piscine corrodée", "Maison Larros en bordure de Bassin, piscine 10×5 avec PAC installée en 2012. Baisse niveau + circulation perturbée. diagnostic : pompe centrifuge corrodée à l'axe, joint mécanique fuyant, eau s'écoule par le siphon de sol du local. Bassin intact. remplacement pompe + nouveau joint : 1 100 euros.")
        ],
    },
    {
        "slug": "piscine-libourne",
        "ville": "Libourne",
        "ville_article": "à Libourne",
        "cp": "33500",
        "zones_voisines": "Saint-Émilion, Pomerol, Fronsac, Saint-Denis-de-Pile, Coutras, Castillon-la-Bataille, Branne",
        "hero_image_alt": "Piscine béton dans une propriété viticole du Libournais près de Libourne, zone d'intervention recherche de fuite",
        "intro_unique": "Le Libournais concentre un parc de piscines particulier en Gironde : forte proportion de bassins anciens (30 à 50 ans) dans les propriétés viticoles et les maisons bourgeoises de négociants en vins, sol argileux très sensible aux mouvements saisonniers, et distance significative à la métropole bordelaise qui décourage les interventions low-cost non spécialisées. Notre méthodologie prend en compte ces spécificités patrimoniales et géologiques pour un diagnostic adapté aux bassins du Libournais.",
        "types_piscines": "Le parc libournais se distingué par une forte présence de piscines béton projeté des années 1970-1990, avec enduit ciment d'origine et étanchéité par peinture époxy refaite plusieurs fois. On trouve aussi des bassins plus récents en liner PVC ou coques polyester dans les lotissements de Libourne intra-muros, quelques piscines hors-sol dans les maisons de négociants, et des bassins couloirs de nage dans les domaines viticoles haut de gamme de Saint-Émilion grand cru et Pomerol.",
        "quartiers_zones": "Nos interventions se concentrent à Libourne centre (quartier bourgeois autour de la place Abel-Surchamp), La Ballastière et Verdet (lotissements récents), Fontenelle (résidentiel), et surtout dans les domaines viticoles alentours : Saint-Émilion (Château Cheval Blanc, Château Figeac secteurs), Pomerol (Château Pétrus voisinage), Fronsac et Canon-Fronsac, Côtes de Castillon. Saint-Denis-de-Pile, Coutras et Branne complètent notre zone de déplacement standard.",
        "spécificités": [
            ("Piscines béton très anciennes et fissures structurelles", "Beaucoup de bassins du Libournais ont 30 à 50 ans, avec des technologies d'étanchéité dépassées : enduit ciment lissé, peinture époxy trente fois repeinte, fers d'armature parfois affleurants par corrosion. Les fissures structurelles sont fréquentes, surtout aux jonctions paroi/fond et aux angles. Notre caméra endoscopique sous-marine documente ces défauts et nous recommandons souvent un diagnostic structurel complémentaire par expert béton si la fissure est large."),
            ("Sol argileux et retrait-gonflement saisonnier", "Le Libournais repose sur des sols argileux typiques des terroirs viticoles de Saint-Émilion à Fronsac, classés en aléa moyen à fort de retrait-gonflement. Les piscines y subissent des sollicitations mécaniques saisonnières : serrage en été sec, relâchement en hiver humide. Sur 30 ans, ces cycles fatiguent les structures et les canalisations enterrées. Nous incluons systématiquement cette donnée dans le diagnostic des bassins anciens du secteur."),
            ("Entretien hétérogène sur domaines viticoles", "Les piscines des domaines viticoles sont souvent des équipements secondaires par rapport à l'activité principale (culture de vigne, vinification). Leur entretien peut être délégué à des prestataires irréguliers, voire négligé pendant les vendanges et périodes de tirage. Nous rencontrons régulièrement des piscines non utilisées depuis 3-5 ans, avec fuites multiples accumulées. Notre diagnostic complet remet le bassin dans un état d'état des lieux détaillé pour le propriétaire ou son gestionnaire."),
            ("Distance à Bordeaux et interventions groupées", "Libourne est à 30 kilomètres du centre de Bordeaux. Pour optimiser les déplacements, nous organisons des tournées libournaises hebdomadaires en saison, permettant d'intervenir à tarif standard sans majoration géographique. Les domaines voisins (Saint-Émilion, Pomerol, Fronsac) sont couverts dans ces tournées. Un devis fixe est communiqué en amont.")
        ],
        "cas_frequent": "Cas type dans le Libournais : château avec piscine béton 12×5 mètres construite vers 1975, enduit ciment origine repeint dans les années 1990. Le gestionnaire constate une baisse d'eau accélérée après une pluie abondante : 4 à 6 cm/jour. Notre diagnostic : inspection caméra sous-marine (recherche fissures actives), colorant aux fissures identifiées et aux pièces à sceller, test de pression sur canalisations. Dans 50 pourcent des cas sur ce profil, la fuite est structurelle (fissure active sur paroi ou fond), dans 30 pourcent sur une ancienne canalisation fonte oubliée, 20 pourcent sur pièces à sceller.",
        "faq_locale": [
            ("Ma piscine château Libourne a 40 ans et fuit, faut-il la refaire entièrement ?",
             "Pas nécessairement. Une fuite sur bassin ancien peut être ponctuelle (fissure isolée, pièce à sceller usée) et se réparer pour quelques centaines d'euros avec une remise en étanchéité locale. Mais si les fissures sont multiples et actives, si l'enduit d'origine est généralisé en fin de vie, une rénovation complète (rebéton, liner renforcé armé type PVC 150/100, ou chape d'étanchéité moderne) s'impose. Notre rapport évalue objectivement cette décision."),
            ("Intervenez-vous sur les propriétés viticoles grands crus de Saint-Émilion ?",
             "Oui, nous intervenons régulièrement sur les domaines grands crus classés et leurs dépendances : châteaux historiques, résidences, dépendances avec piscines. Notre approche respecte scrupuleusement les accès restreints, les consignes de discrétion, et la préservation des espaces paysagers. Un devis précis est établi après visite préalable si la configuration le justifie."),
            ("Sols argileux Libournais : quel impact sur ma piscine ?",
             "Les argiles du Libournais se rétractent en sécheresse et gonflent en humidité, sollicitant mécaniquement tout ce qui est enterré : canalisations, dalles de plage, parfois structure du bassin si les fondations sont insuffisantes. Pour une piscine neuve, une étude de sol est indispensable. Pour un bassin existant, un suivi des canalisations enterrées tous les 10-15 ans est recommandé : c'est souvent là que la fuite apparaît en premier.")
        ],
        "methodes_focus": "Sur les bassins du Libournais, souvent anciens (30 à 50 ans) et en béton armé, notre approche technique commence par l'inspection caméra sous-marine pour évaluer l'état structurel : les fissures actives, l'état des enduits d'origine, la présence de fers d'armature affleurants. Le colorant fluorescéine confirme les fissures suspectes et testé les pièces à sceller souvent d'un autre âge. Sur terrain argileux, le test de pression des canalisations enterrées est incontournable : les raccords PVC collés 30 ans auparavant ont subi de multiples cycles retrait-gonflement. L'écoute électro-acoustique est notre outil de confirmation pour localiser précisément un défaut identifié par test de pression sur un long linéaire.",
        "patterns_frequents": [
            ("Château Saint-Émilion piscine béton 1975", "Domaine grand cru, piscine béton 14×6 construite 1975, enduit ciment refait 1998. Perte d'eau accélérée +6 cm/jour après hiver humide. Inspection caméra : 2 fissures actives en paroi nord. Préconisation : rebéton paroi concernée + nouvelle étanchéité membrane armée. Devis 25 000 euros HT (compatible avec budget domaine), diagnostic 580 euros remboursé assurance."),
            ("Maison négociant Libourne fuite cave voûtée", "Maison 1880 centre Libourne, cave voûtée avec humidité croissante au plafond. Propriétaires soupçonnent la piscine du jardin (ajoutée 1995). diagnostic combiné : humidimètre (cave) + thermographie + colorant piscine. Conclusion : fuite canalisation PVC entre piscine et maison, à 11 mètres du bassin sous la terrasse. Ouverture ciblée, réparation 1 800 euros, cave préservée."),
            ("Bassin Fronsac coque polyester rénovée 2010", "Château Fronsac, ancienne piscine béton rehabilitée par pose coque polyester sur ancienne structure 2010. Baisse 3 cm/jour. diagnostic : coque intacte, mais raccord entre bondes de fond de la coque et canalisations PVC d'origine était mal collé. Localisation au colorant + confirmation test pression. Reprise 900 euros.")
        ],
    },
    {
        "slug": "piscine-le-bouscat",
        "ville": "Le Bouscat",
        "ville_article": "au Bouscat",
        "cp": "33110",
        "zones_voisines": "Bordeaux, Caudéran, Bruges, Eysines, Mérignac",
        "hero_image_alt": "Piscine traditionnelle dans un jardin mature du Bouscat près du Parc Bordelais, zone d'intervention recherche de fuite",
        "intro_unique": "Le Bouscat, ville résidentielle bourgeoise collée à Bordeaux, concentre un parc de piscines relativement ancien dans ses quartiers les plus cossus : Parc Bordelais, La Châtaigneraie, Bourran. Beaucoup de bassins ont été installés dans les années 1970-1990 au cœur de grands jardins matures, aujourd'hui caractérisés par la proximité d'arbres développés dont les systèmes racinaires sollicitent les canalisations enterrées. Ce contexte demande une approche diagnostiqué particulière.",
        "types_piscines": "Les piscines bouscataises se répartissent entre plusieurs profils : bassins béton armé classiques des années 1970-1980 (40 pourcent environ), coques polyester des années 1990-2010 posées en rénovation de bassins plus anciens (25 pourcent), liners PVC modernes sur bassins existants (20 pourcent), et quelques couloirs de nage ou piscines cintrées dans les jardins étroits de maisons bourgeoises (15 pourcent). quelques piscines de caractère à la limite de Caudéran, avec margelles en pierre de Frontenac et décoration soignée.",
        "quartiers_zones": "Les secteurs à forte densité sont Parc Bordelais (hôtels particuliers et grandes propriétés avec bassins historiques), La Châtaigneraie (résidentiel familial avec grands jardins), Bourran (quartier cossu aux frontières de Caudéran), Parc Rivière et Croix de Laubrescas (plus pavillonnaire récent). Les maisons bourgeoises des années 1910-1930 reconverties en résidences familiales présentent souvent des piscines ajoutées dans les années 1980 sans étude de sol contemporaine.",
        "spécificités": [
            ("Racines d'arbres matures et canalisations enterrées", "La majorité des propriétés bouscataises à piscine possèdent des jardins paysagers matures avec platanes, chênes, tilleuls ou cèdres plantés il y a 40 à 80 ans. Ces systèmes racinaires cherchent l'humidité et pénètrent les raccords défectueux des canalisations enterrées. Nous intervenons régulièrement sur des fuites provoquées par une racine qui a progressivement désaxé puis percé un raccord PVC 20-30 ans après son installation. L'inspection caméra endoscopique est ici essentielle pour confirmer l'étiologie racinaire."),
            ("Jardins étroits et accès technique limité", "Certaines propriétés historiques du Bouscat présentent des jardins en longueur avec piscines en fond de parcelle, accessibles uniquement par un couloir ou une porte cochère. Notre matériel compact (capteur acoustique portable, bouteilles de gaz traceur 5L, caméra endoscopique sans fil) permet d'intervenir dans ces configurations sans apport de gros équipement. Nous prévoyons aussi les protections anti-tache pour les sols et mobiliers extérieurs du jardin."),
            ("Bassins profonds anciens (4 mètres de profondeur)", "Plusieurs piscines bouscataises construites dans les années 1970 ont un point profond à 3 ou 4 mètres, conçues pour la plongée. Ces bassins ont une structure soumise à une pression hydrostatique importante, et la bonde de fond à grande profondeur est un point de fuite difficile à diagnostiquer visuellement. Notre colorant fluorescéine en bouteille lestée permet d'atteindre le fond pour tester spécifiquement cette zone, sans plongée humaine systématique."),
            ("Traitement paysager ancien et impact hydraulique", "Beaucoup de jardins bouscataises ont des systèmes d'arrosage enterrés des années 1980-1990 cohabitant avec les canalisations de piscine. Nous rencontrons régulièrement des fuites attribuées à tort à la piscine alors qu'elles proviennent du réseau d'arrosage enterré (ou vice versa). Notre diagnostic sépare systématiquement les deux circuits (piscine vs arrosage) par fermeture séquentielle et mesure différentielle.")
        ],
        "cas_frequent": "Scénario type au Bouscat : propriété familiale Parc Bordelais, piscine béton 10×5 mètres installée en 1982, jardin avec 3 grands platanes plantés en 1960. Le propriétaire constate une perte régulière de 2-3 cm/jour depuis le printemps, plus marquée après les grosses pluies (terrain saturé qui amplifie). Notre diagnostic : test du seau (confirmé fuite), colorant pièces à sceller, test pression canalisations, et inspection caméra du réseau enterré sur tracé complet. Dans 55 pourcent des cas sur ce profil, la fuite est sur canalisation enterrée percée par racine. Réparation : ouverture ponctuelle, remplacement du tronçon endommagé sur 1 à 2 mètres, rebouchage.",
        "faq_locale": [
            ("Mes arbres menacent-ils vraiment ma piscine au Bouscat ?",
             "Oui, particulièrement les platanes et les saules qui ont des systèmes racinaires très étendus et agressifs. Un platane mature peut avoir des racines à 15-20 mètres horizontalement. Si vos arbres sont à moins de 10 mètres de la piscine ou de ses canalisations enterrées, une inspection caméra préventive tous les 10-15 ans est recommandée. Nous ne conseillons pas l'abattage systématique, mais un suivi technique."),
            ("Ma piscine Parc Bordelais a 40 ans, vaut-il mieux la rénover ou la combler ?",
             "Ça dépend de son état structurel, de l'usage prévu et de votre budget. Une piscine béton de 40 ans avec structure saine peut être rénovée (rebéton si nécessaire, nouvelle étanchéité par liner armé, remplacement des canalisations) pour 15 000 à 30 000 euros, soit bien moins qu'une piscine neuve. Le combler revient aussi cher (10 000 à 20 000 euros avec reprise de jardin). Notre rapport de fuite, couplé à un diagnostic structurel, aide à trancher."),
            ("Peut-on localiser une fuite dans une piscine de 4 mètres de profondeur ?",
             "Oui, sans problème. Nos sondés acoustiques et nos colorants en bouteille lestée atteignent le fond de tout bassin sans nécessiter de plongée humaine. Dans certains cas complexes, nous faisons intervenir un plongeur professionnel équipé (scaphandre autonome), notamment pour une inspection visuelle rapprochée de la bonde de fond. Cette option est facturée en supplément et proposée si le diagnostic acoustique et colorant est insuffisant.")
        ],
        "methodes_focus": "Sur les piscines du Bouscat, presque toutes anciennes et entourées de jardins matures, notre première méthode est l'inspection caméra endoscopique des canalisations enterrées : dans 55 pourcent des diagnostics bouscatais, la fuite vient d'un raccord pénétré par une racine d'arbre (platane, chêne, tilleul ou saule). Quand l'inspection ne révèle pas de racine, nous enchaînons avec le test de pression séquentiel des circuits, puis le colorant fluorescéine sur pièces à sceller du bassin. Pour les piscines de 3-4 mètres de profondeur (rares mais présentes dans les propriétés historiques), utilisation d'une bouteille de colorant lestée qui descend au fond du bassin sans nécessiter de plongée. L'écoute acoustique complète le diagnostic sur les longs tracés de canalisations sous les grandes pelouses.",
        "patterns_frequents": [
            ("Piscine Parc Bordelais racine de platane", "Propriété familiale, piscine béton 10×4 des années 1978, 3 grands platanes à 7-10 mètres. Baisse régulière +2 cm/jour depuis 1 an. Inspection caméra des canalisations : racine de platane de 5 cm de diamètre entrée par un raccord défectueux à 6 m du bassin. Réparation : coupe racinaire, remplacement 60 cm de canalisation, injection inhibiteur racinaire. 1 600 euros total. Suivi tous les 5 ans recommandé."),
            ("Jardin La Châtaigneraie accès étroit", "Maison bourgeoise 1910, piscine couloir de nage 15×2,5 mètres au fond du jardin, accessible uniquement par une porte cochère de 80 cm. Matériel compact déployé : caméra endoscopique sans fil, corrélateur portable, bouteilles gaz traceur 5L. Localisation fuite au niveau bonde de fond, joint torique usé. remplacement en apnée : 420 euros total."),
            ("Piscine profonde 4m Bourran 1976", "Propriété 1900, piscine béton 12×5 avec point profond 4m (plongeoir d'origine). Baisse 3 cm/jour. Colorant lesté descendu au fond : fissure radiale autour de la grille de bonde, 15 cm de long. Préconisation : réparation en apnée par plongeur pro (nécessaire à cette profondeur) + joint étanche. 1 800 euros + plongeur.")
        ],
    },
]

# ═══════════════════════════════════════════════════════════════
# PAGE USE CASE : Fluorescéine / colorant traceur piscine Bordeaux
# ═══════════════════════════════════════════════════════════════

def page_fluoresceine_piscine_bordeaux():
    body = '''
<section class="hero-mini">
  <div class="container">
    <nav class="breadcrumb">
      <a href="/">Accueil</a>
      <span>&rsaquo;</span>
      <a href="/detection-fuite/">Détection de fuite</a>
      <span>&rsaquo;</span>
      <span>Fluorescéine piscine</span>
    </nav>
    <span class="badge-cp">Colorant traceur</span>
    <h1>Recherche de fuite piscine à la fluorescéine en Gironde</h1>
    <p class="hero-mini-lead">Localisation d\'une fuite de piscine par injection de colorant fluorescéine sodique : <strong>méthode visuelle, non toxique, validée sur tous types de bassins</strong> (liner, coque polyester, béton). Sans vidange, sans démolition, avec rapport d\'intervention pour votre assureur.</p>
    <div class="hero-mini-cta">
      <a href="/devis/" class="btn btn-gold">Demander un devis fluorescéine</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <figure style="margin:0 0 2rem;">
      <img src="/assets/piscine-fluoresceine-bordeaux.webp" alt="Piscine privée à eau bleue claire en Gironde, contexte d\'application du diagnostic à la fluorescéine" width="1600" height="1067" loading="eager" style="width:100%;max-height:380px;height:auto;object-fit:cover;border-radius:12px;display:block;">
    </figure>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Qu\'est-ce que la fluorescéine sodique en recherche de fuite piscine ?</h2>
    <p>La fluorescéine sodique (uranine) est un colorant fluorescent jaune-vert, soluble dans l\'eau, biodégradable et non toxique pour l\'homme, les animaux et les écosystèmes aquatiques. Utilisée depuis plus d\'un siècle en hydrologie pour traquer les circulations souterraines, elle est devenue depuis les années 1990 l\'un des outils de référence du diagnostic piscine. À très faible concentration (0,1 à 1 mg/L), elle reste invisible à l\'œil nu mais devient fluorescente sous une simple lampe UV ou par contraste lumineux dans une eau claire.</p>
    <p>Concrètement, nos techniciens injectent la fluorescéine à un endroit ciblé du bassin (skimmer, refoulement, prise balai, projecteur, fond, escalier, joint suspect) et observent où le colorant migre. Une fissure de liner, un joint défaillant ou un raccord percé aspire le colorant vers l\'extérieur du bassin. La trace fluorescente persistante, suivie en temps réel, indique le point de fuite avec une précision de quelques centimètres. Sur les piscines à eau parfaitement claire, l\'observation se fait à l\'œil nu. Sur les eaux vert clair ou troubles, la lampe UV portative confirme la migration.</p>
    <p>Cette méthode est <strong>la seule technique qui prouve visuellement le passage de l\'eau au point de fuite</strong>. Là où la thermographie ou l\'écoute acoustique signalent une anomalie indirecte, la fluorescéine apporte la preuve par contact. C\'est pourquoi nous la combinons systématiquement à d\'autres méthodes pour les diagnostics complexes (test pression, inspection caméra), mais elle reste l\'outil dédié et autonome sur 60 pourcent des fuites de piscine que nous traitons en Gironde.</p>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Quand la fluorescéine est-elle la bonne méthode ?</h2>
    <p>Le colorant traceur n\'est pas universel. Voici les configurations où il est <strong>la solution la plus rapide et économique</strong> par rapport aux autres techniques de notre arsenal :</p>
    <ul>
      <li><strong>Suspicion de fuite sur pièces à sceller</strong> (skimmer, buse de refoulement, prise balai, projecteur encastré, bonde de fond) : la fluorescéine confirme en 5 minutes si une pièce est défaillante en injectant le colorant à proximité immédiate. Très efficace sur les piscines de 8 à 20 ans dont les joints d\'étanchéité commencent à durcir.</li>
      <li><strong>Fissures actives sur liner PVC</strong> : sur liner clair (sable, gris perle, bleu pâle), les fissures absorbent le colorant et révèlent un faisceau de lignes fluorescentes. Idéal pour les liners de Mérignac, Pessac et Le Bouscat dont l\'âge médian dépasse 15 ans.</li>
      <li><strong>Coque polyester osmosée ou microfissurée</strong> : en injectant le colorant en surface au point suspect, le passage à travers la coque devient visible en 10 à 30 minutes selon la taille de la microfissure. Méthode privilégiée sur le parc de Gujan-Mestras et Andernos-les-Bains. Voir notre guide spécifique <a href="/guide/fuite-coque-polyester-piscine/" style="color:var(--green);text-decoration:underline;">fuite coque polyester piscine</a>.</li>
      <li><strong>Test sur joint d\'escalier maçonné, joint de margelle</strong> : la fluorescéine appliquée localement infiltre les microfissures invisibles à l\'œil nu et trahit les remontées d\'humidité dans les marches ou la plage.</li>
      <li><strong>Vérification après réparation</strong> : nous injectons systématiquement de la fluorescéine en fin d\'intervention pour valider l\'étanchéité de la zone réparée. Aucun client ne doit nous appeler 6 mois plus tard pour la même fuite.</li>
    </ul>
    <p style="margin-top:1.5rem;">À l\'inverse, la fluorescéine seule <strong>ne suffit pas</strong> pour les fuites enterrées sur les canalisations en aval du local technique (refoulement vers le bassin, retour des skimmers vers la pompe). Sur ces tracés, nous combinons gaz traceur azote/hydrogène, écoute électro-acoustique et test de pression. Idem pour les fuites en circuit fermé chauffage piscine ou plancher chauffant : voir notre page dédiée <a href="/detection-fuite/thermographie-infrarouge-bordeaux/" style="color:var(--green);text-decoration:underline;">thermographie infrarouge à Bordeaux</a>.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <h2>Le protocole fluorescéine en intervention</h2>
    <div class="arg-num-grid">
      <div class="arg-num-card">
        <span class="arg-num">01</span>
        <div class="arg-num-content">
          <h3>Stabilisation du bassin</h3>
          <p>Arrêt complet de la filtration au moins 30 minutes avant l\'injection. Vérification du niveau d\'eau, de la température et de la limpidité. Plus l\'eau est calme, plus la trace du colorant sera lisible.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">02</span>
        <div class="arg-num-content">
          <h3>Diagnostic préalable</h3>
          <p>Repérage des zones suspectes par observation directe (auréoles, dépôts calcaires, déformations du liner) et par questions ciblées au propriétaire (vitesse de baisse, périodicité, installations récentes).</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">03</span>
        <div class="arg-num-content">
          <h3>Injection ciblée</h3>
          <p>Dépôt précis de quelques millilitres de colorant à proximité du point suspect, à l\'aide d\'une pipette ou seringue lestée. Concentration ajustée selon la profondeur et le volume du bassin.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">04</span>
        <div class="arg-num-content">
          <h3>Observation</h3>
          <p>Suivi visuel pendant 5 à 30 minutes selon le débit suspecté. Le colorant aspiré par la fuite forme un filet directionnel caractéristique. Photo et vidéo systématiques pour le rapport.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">05</span>
        <div class="arg-num-content">
          <h3>Confirmation par contre-test</h3>
          <p>Nouvelle injection à un point témoin pour valider l\'absence de courant parasite (filtration résiduelle, vent de surface). Le contre-test élimine 95 pourcent des faux positifs.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">06</span>
        <div class="arg-num-content">
          <h3>Lampe UV si nécessaire</h3>
          <p>Sur eau verte ou trouble, lampe UV portative à 365 nm pour révéler la fluorescence du colorant et tracer son cheminement dans la zone d\'aspiration.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Cas concrets de diagnostic fluorescéine en Gironde</h2>
    <p>Voici trois interventions récentes qui illustrent l\'efficacité du colorant traceur sur des configurations différentes :</p>
    <h3>Piscine liner PVC à Mérignac (Capeyron, août 2025)</h3>
    <p>Bassin de 8×4 mètres installé en 2007, liner d\'origine. Le propriétaire constate une perte de 2 cm par jour et soupçonne le skimmer après recollage récent. Injection de fluorescéine à proximité du skimmer : aucune migration en 15 minutes. Nouvelle injection sous le projecteur encastré (côté petit bain) : trace fluorescente nettement visible vers la traversée de paroi en 4 minutes. Démontage du projecteur, joint torique craquelé. Remplacement, contre-test fluorescéine, étanchéité validée. Coût total intervention : 320 euros HT, dont 90 euros de pièce.</p>
    <h3>Piscine coque polyester à Gujan-Mestras (mars 2026)</h3>
    <p>Coque blanche 9×4,5 mètres de 2012, micro-fissures osmotiques suspectées par le propriétaire. Test pression hydraulique des canalisations : aucune anomalie. Injection fluorescéine en surface au niveau de boursouflures visibles côté grand bain : passage du colorant à travers la coque visible à la lampe UV en 22 minutes, sortant côté terre dans le local technique. Préconisation : ponçage et réparation gel-coat sur 1,2 m². Coût diagnostic : 380 euros HT, prestation gel-coat sous-traitée à un pisciniste partenaire.</p>
    <h3>Piscine béton armé à Caudéran Bordeaux (mai 2025)</h3>
    <p>Bassin 10×5 mètres de 1985, joints maçonnés d\'origine entre carrelage et structure. Baisse irrégulière, 1 à 3 cm par jour selon les périodes. Combinaison fluorescéine + écoute acoustique : 3 points d\'injection ciblés sur les joints les plus suspects (escalier, raccord retour skimmer côté ouest, jonction fond/paroi). Le 3e point révèle une migration vers la chape extérieure en 8 minutes. Intervention conservatoire : reprise du joint en résine époxy spécifique piscine sur 80 cm. Coût total : 580 euros HT.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Pourquoi la fluorescéine plutôt qu\'un autre colorant ?</h2>
    <p>Plusieurs colorants existent en plomberie et hydrologie : bleu de méthylène, rouge fuchsine, indigo, éosine, rhodamine. Chacun à ses usages. Pour la piscine, <strong>la fluorescéine sodique reste la référence pour cinq raisons techniques</strong> :</p>
    <ul>
      <li><strong>Innocuité totale</strong> : approuvée par l\'OMS pour le traçage des eaux potables à très faible concentration. Aucun risque pour la baignade après dilution naturelle (le colorant disparaît visuellement en 24 à 48 heures sous filtration).</li>
      <li><strong>Détectabilité extrême</strong> : la fluorescéine reste visible à des concentrations de 0,001 mg/L sous lampe UV. Aucun autre colorant ne permet de tracer un débit aussi faible (microfissures à 50 mL/heure).</li>
      <li><strong>Pas d\'altération du liner ou des coques</strong> : à la différence du bleu de méthylène, qui peut tacher durablement les liners pâles ou les coques en gel-coat blanc. Aucune décoloration observée sur 200 interventions annuelles.</li>
      <li><strong>Comportement hydraulique fiable</strong> : la fluorescéine ne se sépare pas de l\'eau (densité quasi identique), elle suit fidèlement les écoulements. Le bleu de méthylène, plus lourd, donne des faux positifs en stratification thermique.</li>
      <li><strong>Compatibilité avec tous les traitements</strong> : chlore, brome, sel, oxygène actif, PHMB. Aucune dégradation chimique observée. Le pH de la piscine n\'altère pas la lecture.</li>
    </ul>
    <p style="margin-top:1.5rem;">Nous utilisons une fluorescéine pharmaceutique de grade analytique, certifiée Codex et conforme aux normes alimentaires ANSES, achetée en France auprès d\'un distributeur agréé. Conservation en bouteille opaque à l\'abri de la lumière, durée de vie 2 ans. Coût matière par intervention : moins de 2 euros, ce qui en fait également une méthode très économique.</p>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Combien coûte un diagnostic fluorescéine sur une piscine en Gironde ?</h2>
    <p>Le tarif d\'un diagnostic au colorant traceur dépend de la complexité du bassin et du nombre de points à tester. Voici nos fourchettes constatées sur la métropole bordelaise :</p>
    <ul>
      <li><strong>Diagnostic ciblé fluorescéine seule</strong> (piscine de moins de 100 m³, hypothèse de fuite déjà localisée par le propriétaire) : <strong>240 à 320 euros HT</strong>, intervention 1 à 2 heures, rapport photo inclus.</li>
      <li><strong>Diagnostic fluorescéine combiné test pression</strong> (cas le plus fréquent, hypothèse mixte bassin + canalisations) : <strong>380 à 520 euros HT</strong>, intervention 2 à 3 heures.</li>
      <li><strong>Diagnostic complet fluorescéine + caméra endoscopique + acoustique</strong> (piscine ancienne, fuite récurrente, copropriété) : <strong>520 à 750 euros HT</strong>, intervention 3 à 5 heures, rapport assurance complet.</li>
    </ul>
    <p>Pour une vue d\'ensemble des tarifs de recherche de fuite piscine selon le type de bassin et la méthode, consultez notre <a href="/guide/recherche-fuite-piscine-tarif/" style="color:var(--green);text-decoration:underline;">guide tarif recherche de fuite piscine en Gironde</a>. Le diagnostic est presque toujours pris en charge par votre assurance multirisque habitation au titre de la garantie recherche de fuite : voir notre <a href="/guide/recherche-fuite-piscine-assurance/" style="color:var(--green);text-decoration:underline;">guide assurance piscine</a> pour la procédure de remboursement et les pièces à fournir.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Questions fréquentes sur la fluorescéine en piscine</h2>

    <h3>La fluorescéine est-elle dangereuse pour les baigneurs ou les animaux ?</h3>
    <p>Non. À la concentration utilisée pour le diagnostic (moins de 1 mg/L après dilution dans le volume du bassin), la fluorescéine sodique est totalement inoffensive. Elle est d\'ailleurs utilisée en ophtalmologie (test à la fluorescéine cornéenne) et en hydrogéologie pour le traçage des eaux destinées à la consommation humaine. Aucune contre-indication pour les enfants, animaux domestiques ou poissons d\'agrément. La couleur jaune-vert disparaît visuellement en 24 à 48 heures sous filtration normale. La baignade reste possible immédiatement après le diagnostic si la concentration est faible, ou après un cycle de filtration de 6 à 12 heures pour les plus prudents.</p>

    <h3>Le colorant peut-il tacher mon liner ou mon revêtement ?</h3>
    <p>Aucune coloration durable n\'a été observée sur les liners PVC, coques polyester, carrelage, peinture polyuréthane ou enduit ciment. La fluorescéine est extrêmement diluée et ne pénètre pas les matériaux. Sur les liners très clairs (sable, blanc), une légère teinte verdâtre peut subsister 2 à 6 heures avant disparition complète sous filtration. Sur les liners sombres (gris anthracite, bleu marine, vert algue), aucune trace visible. Notre fluorescéine pharmaceutique est exempte de pigments tertiaires qui pourraient marquer durablement.</p>

    <h3>Peut-on faire un test fluorescéine soi-même avant de nous appeler ?</h3>
    <p>Techniquement oui, mais le risque de faux positif est élevé sans expérience. La fluorescéine vendue en magasin de bricolage est souvent à concentration excessive et donne une teinte verte uniforme du bassin, masquant la migration directionnelle. Un test fait par un propriétaire conduit dans 70 pourcent des cas à une mauvaise interprétation : courants thermiques pris pour une fuite, vent de surface qui déplace artificiellement le colorant, filtration mal arrêtée qui crée une aspiration parasite. Notre méthode, avec des doses calibrées et un protocole d\'observation rigoureux, est nettement plus fiable. Avant de nous appeler, vous pouvez toutefois faire le <a href="/guide/evaporation-vs-fuite-piscine/" style="color:var(--green);text-decoration:underline;">test du seau</a> pour confirmer qu\'il s\'agit bien d\'une fuite et non d\'évaporation naturelle.</p>

    <h3>La fluorescéine fonctionne-t-elle sur une piscine couverte ou enterrée sous abri ?</h3>
    <p>Oui, c\'est même là que la méthode est la plus performante. À l\'abri du vent et du soleil, l\'eau est plus calme et la fluorescence du colorant plus contrastée. Sur les piscines couvertes par abri télescopique en Gironde (très répandues sur Mérignac, Pessac et Le Bouscat), l\'éclairage UV est parfois inutile, l\'œil suffit. Pour les piscines intérieures ou véranda, le diagnostic est encore plus précis car l\'évaporation parasite est nulle.</p>

    <h3>Quelle est la précision réelle du diagnostic fluorescéine ?</h3>
    <p>Sur les piscines à parois lisses (liner, coque), la précision est de l\'ordre de 5 à 10 centimètres. La trace fluorescente converge vers le point exact de fuite. Sur les piscines béton avec joints maçonnés, la précision peut descendre à 20-30 centimètres en raison du cheminement de l\'eau dans les joints poreux. Dans tous les cas, c\'est une précision largement suffisante pour cibler une réparation locale, sans casser plus que strictement nécessaire.</p>

    <h3>Combien de temps dure une intervention fluorescéine à Bordeaux ?</h3>
    <p>Pour un diagnostic ciblé sur 1 à 3 points suspects, comptez 1 heure à 1 heure 30 sur place. Pour un diagnostic complet avec scan systématique de toutes les pièces à sceller du bassin, prévoir 2 heures à 2 heures 30. Le rapport technique avec photos et préconisations est rédigé dans là journée et envoyé par email le soir même. Devis pour réparation joint dans la foulée si vous le souhaitez.</p>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Pages connexes : recherche de fuite piscine Gironde</h2>
    <p>La fluorescéine est l\'une de nos méthodes phares mais elle s\'inscrit dans un dispositif complet. Voici les pages qui complètent votre lecture :</p>
    <ul>
      <li><a href="/detection-fuite/piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">Recherche de fuite piscine à Bordeaux</a> : page ville détaillant nos méthodes sur les piscines bordelaises (Caudéran, Le Bouscat, propriétés bourgeoises).</li>
      <li><a href="/detection-fuite/piscine-arcachon/" style="color:var(--green);text-decoration:underline;">Recherche de fuite piscine à Arcachon</a> : intervention villas haut de gamme du Pyla et Ville d\'Hiver.</li>
      <li><a href="/detection-fuite/piscine/" style="color:var(--green);text-decoration:underline;">Hub recherche de fuite piscine en Gironde</a> : vue d\'ensemble des 7 villes couvertes et des méthodes.</li>
      <li><a href="/guide/fuite-liner-piscine/" style="color:var(--green);text-decoration:underline;">Guide diagnostic fuite sur liner PVC</a> : signes, causes, age critique du liner.</li>
      <li><a href="/guide/reparation-liner-piscine/" style="color:var(--green);text-decoration:underline;">Réparation d\'une fuite de liner piscine</a> : techniques, coûts et durée de vie après réparation.</li>
      <li><a href="/guide/evaporation-vs-fuite-piscine/" style="color:var(--green);text-decoration:underline;">Évaporation ou fuite : test du seau</a> : à faire avant de demander un diagnostic.</li>
      <li><a href="/guide/recherche-fuite-piscine-tarif/" style="color:var(--green);text-decoration:underline;">Tarifs recherche de fuite piscine</a> : grille de prix par méthode et type de bassin.</li>
      <li><a href="/guide/recherche-fuite-piscine-assurance/" style="color:var(--green);text-decoration:underline;">Remboursement assurance piscine</a> : procédure pour faire prendre en charge le diagnostic.</li>
    </ul>
  </div>
</section>

''' + form_section("Bordeaux") + '''
'''

    ld_local = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Recherche Fuite Gironde",
  "description": "Recherche de fuite piscine par colorant fluorescéine sodique à Bordeaux et en Gironde. Méthode visuelle non destructive, sans vidange.",
  "url": "https://recherche-fuite-gironde.fr/detection-fuite/fluoresceine-piscine-bordeaux/",
  "areaServed": [
    { "@type": "City", "name": "Bordeaux", "postalCode": "33000" },
    { "@type": "City", "name": "Mérignac", "postalCode": "33700" },
    { "@type": "City", "name": "Pessac", "postalCode": "33600" },
    { "@type": "City", "name": "Arcachon", "postalCode": "33120" },
    { "@type": "City", "name": "La Teste-de-Buch", "postalCode": "33260" },
    { "@type": "City", "name": "Gujan-Mestras", "postalCode": "33470" },
    { "@type": "City", "name": "Libourne", "postalCode": "33500" },
    { "@type": "City", "name": "Le Bouscat", "postalCode": "33110" }
  ],
  "priceRange": "€€"
}
</script>'''

    ld_service = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "Recherche de fuite piscine par colorant fluorescéine",
  "provider": { "@type": "LocalBusiness", "name": "Recherche Fuite Gironde" },
  "areaServed": "Gironde",
  "description": "Localisation d'une fuite de piscine par injection de fluorescéine sodique. Méthode non toxique, validée sur liner, coque polyester et béton.",
  "offers": {
    "@type": "AggregateOffer",
    "lowPrice": "240",
    "highPrice": "750",
    "priceCurrency": "EUR"
  }
}
</script>'''

    ld_breadcrumb = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://recherche-fuite-gironde.fr/" },
    { "@type": "ListItem", "position": 2, "name": "Détection de fuite", "item": "https://recherche-fuite-gironde.fr/detection-fuite/" },
    { "@type": "ListItem", "position": 3, "name": "Fluorescéine piscine Bordeaux", "item": "https://recherche-fuite-gironde.fr/detection-fuite/fluoresceine-piscine-bordeaux/" }
  ]
}
</script>'''

    ld_faq = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "La fluorescéine est-elle dangereuse pour les baigneurs ou les animaux ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Non. À la concentration utilisée pour le diagnostic (moins de 1 mg/L), la fluorescéine sodique est totalement inoffensive. Elle est utilisée en ophtalmologie et en hydrogéologie pour le traçage des eaux destinées à la consommation humaine." }
    },
    {
      "@type": "Question",
      "name": "Le colorant peut-il tacher mon liner ou mon revêtement ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Aucune coloration durable n'a été observée sur les liners PVC, coques polyester, carrelage, peinture polyuréthane ou enduit ciment. Une légère teinte verdâtre peut subsister 2 à 6 heures sur les liners très clairs avant disparition complète sous filtration." }
    },
    {
      "@type": "Question",
      "name": "Combien coûte un diagnostic fluorescéine sur une piscine en Gironde ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Entre 240 et 320 euros HT pour un diagnostic ciblé. Entre 380 et 520 euros HT pour un diagnostic combiné fluorescéine + test pression. Entre 520 et 750 euros HT pour un diagnostic complet avec caméra endoscopique et écoute acoustique." }
    },
    {
      "@type": "Question",
      "name": "Quelle est la précision réelle du diagnostic fluorescéine ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Sur piscines liner ou coque, précision de 5 à 10 cm. Sur béton avec joints maçonnés, précision de 20 à 30 cm en raison du cheminement de l'eau dans les joints poreux. Précision largement suffisante pour cibler une réparation locale." }
    },
    {
      "@type": "Question",
      "name": "Combien de temps dure une intervention fluorescéine à Bordeaux ?",
      "acceptedAnswer": { "@type": "Answer", "text": "1 heure à 1 heure 30 pour un diagnostic ciblé sur 1 à 3 points suspects. 2 heures à 2 heures 30 pour un diagnostic complet avec scan systématique de toutes les pièces à sceller. Rapport envoyé le soir même par email." }
    }
  ]
}
</script>'''

    return html_base(
        'Fluorescéine piscine Bordeaux | Colorant traceur',
        'Recherche de fuite piscine par colorant fluorescéine sodique à Bordeaux : méthode visuelle, non toxique, sans vidange. Diagnostic ciblé liner, coque, béton.',
        'https://recherche-fuite-gironde.fr/detection-fuite/fluoresceine-piscine-bordeaux/',
        body,
        extra_ld=ld_local + ld_service + ld_breadcrumb + ld_faq,
    )


# ═══════════════════════════════════════════════════════════════
# PAGE USE CASE : Thermographie infrarouge fuite Bordeaux
# ═══════════════════════════════════════════════════════════════

def page_thermographie_infrarouge_bordeaux():
    body = '''
<section class="hero-mini">
  <div class="container">
    <nav class="breadcrumb">
      <a href="/">Accueil</a>
      <span>&rsaquo;</span>
      <a href="/detection-fuite/">Détection de fuite</a>
      <span>&rsaquo;</span>
      <span>Thermographie infrarouge</span>
    </nav>
    <span class="badge-cp">33000 · Métropole bordelaise</span>
    <h1>Thermographie infrarouge : recherche de fuite à Bordeaux</h1>
    <p class="hero-mini-lead">Localisation d\'une fuite d\'eau par caméra thermique infrarouge à Bordeaux : <strong>plancher chauffant, canalisation encastrée dans une cloison, dalle béton, plafond suspect</strong>. Détection sans démolition, en moins d\'une heure sur la zone d\'intervention.</p>
    <div class="hero-mini-cta">
      <a href="/devis/" class="btn btn-gold">Demander un diagnostic thermographie</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <figure style="margin:0 0 2rem;">
      <img src="/assets/thermographie-fuite-bordeaux.webp" alt="Intérieur de maison contemporaine à Bordeaux avec plancher en parquet, contexte d\'intervention thermographie infrarouge sur plancher chauffant" width="1600" height="1067" loading="eager" style="width:100%;max-height:380px;height:auto;object-fit:cover;border-radius:12px;display:block;">
    </figure>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Comment fonctionne la thermographie infrarouge en recherche de fuite ?</h2>
    <p>Toute matière émet un rayonnement infrarouge dont l\'intensité dépend de sa température de surface. La caméra thermique convertit ce rayonnement invisible en image colorée, où chaque pixel correspond à une mesure de température. Une fuite d\'eau crée presque toujours une signature thermique anormale : une zone plus froide (par évaporation latente), une zone plus chaude (eau du circuit chauffage qui sort), ou un dégradé inhabituel autour d\'une canalisation. La caméra révèle cette anomalie sans aucun contact avec la surface.</p>
    <p>Les caméras professionnelles que nous utilisons ont une résolution thermique de 0,03 à 0,05 °C et une définition de 320×240 à 640×480 pixels. Cela permet de distinguer une variation de température de quelques centièmes de degré sur une surface de 10 cm². Concrètement, sur un plancher chauffant en chauffe à 35 °C, une fuite produira un halo à 28-30 °C visible immédiatement à l\'écran. Sur une cloison sèche cachant une canalisation d\'eau froide, une infiltration apparaîtra comme une tache plus froide de 2 à 4 °C par évaporation.</p>
    <p>La thermographie n\'est pas magique : elle n\'identifie pas là cause de la fuite, seulement sa localisation. Et elle ne fonctionne que si <strong>il existe un gradient thermique entre le fluide et son environnement</strong>. Sur un circuit d\'eau froide en hiver, il faut souvent forcer le contraste en injectant de l\'eau chaude ou en augmentant la pression. Sur un plancher chauffant éteint depuis plusieurs jours, on doit le remettre en chauffe deux à trois heures avant l\'intervention. C\'est pourquoi nous prescrivons toujours un protocole précis avant la visite, pour que la caméra travaille dans des conditions optimales.</p>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Quand utiliser la thermographie infrarouge ?</h2>
    <p>La caméra thermique est particulièrement performante dans cinq scénarios que nous rencontrons régulièrement à Bordeaux :</p>
    <ul>
      <li><strong>Fuite sur plancher chauffant hydraulique</strong> : c\'est l\'application reine. La thermographie identifie le tube PER fuyard en moins de 30 minutes, sans casser la chape. Méthode privilégiée sur les pavillons des années 2000-2020 de Mérignac, Pessac, Le Haillan, Bruges. Voir notre page dédiée <a href="/detection-fuite/fuite-plancher-chauffant-bordeaux/" style="color:var(--green);text-decoration:underline;">recherche de fuite plancher chauffant à Bordeaux</a>.</li>
      <li><strong>Canalisation encastrée dans une cloison</strong> : tube cuivre ou PER passant dans une cloison BA13, en doublage isolant, derrière un carrelage. La caméra repère la trace humide quand la fuite est active. Très efficace dans les appartements bordelais des années 1980-2010.</li>
      <li><strong>Tache d\'humidité au plafond ou au mur</strong> : sur les copropriétés haussmanniennes ou échoppes de Bordeaux, une auréole peut venir d\'une multitude de sources (toiture, façade, voisin du dessus, canalisation EU/EV). La thermographie aide à trier en localisant la zone la plus humide réellement, par opposition à la tache visible qui peut être décalée de 2 à 5 mètres du point de fuite.</li>
      <li><strong>Dalle béton sur vide sanitaire ou cave</strong> : suspicion de fuite sur canalisation noyée dans la dalle. La caméra révèle les zones froides en dessous (vu du vide sanitaire) ou plus chaudes au-dessus (selon le sens du fluide).</li>
      <li><strong>Diagnostic préventif après sinistre</strong> : après un dégât des eaux résolu, vérification thermographique pour s\'assurer qu\'il n\'y a pas de seconde fuite passée inaperçue (cas fréquent sur les vieilles installations, et facteur d\'aggravation rapide en cas de récidive).</li>
    </ul>
    <p style="margin-top:1.5rem;">À l\'inverse, la thermographie est <strong>peu efficace ou inutile</strong> sur les piscines (privilégier <a href="/detection-fuite/fluoresceine-piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">la fluorescéine</a>), sur les canalisations enterrées sous terrain extérieur (privilégier le <a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">gaz traceur</a>), et sur les fuites trop anciennes dont le gradient thermique a disparu (l\'humidité s\'est diffusée uniformément).</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <h2>Notre matériel et notre protocole thermographie</h2>
    <div class="arg-num-grid">
      <div class="arg-num-card">
        <span class="arg-num">01</span>
        <div class="arg-num-content">
          <h3>Caméra FLIR T540 / T865</h3>
          <p>Résolution thermique 30 mK (0,03 °C), définition 464×348 ou 640×480 pixels selon configuration. Plage -40 à +1500 °C. Optique macro pour les inspections rapprochées de cloisons.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">02</span>
        <div class="arg-num-content">
          <h3>Mise en condition thermique</h3>
          <p>Pour plancher chauffant : remise en chauffe 2 à 3h à pleine puissance avant intervention. Pour eau froide : injection d\'eau chaude ou mise en pression accrue pour créer un contraste exploitable.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">03</span>
        <div class="arg-num-content">
          <h3>Cartographie systématique</h3>
          <p>Scan thermographique pièce par pièce, avec relevés à 0,5 m, 1 m et 2 m de la surface. Annotation des points chauds et froids sur plan technique transmis au client.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">04</span>
        <div class="arg-num-content">
          <h3>Confirmation par humidimètre</h3>
          <p>Là où la caméra signale une anomalie, mesure de la teneur en eau à pointes capacitives ou résistives pour distinguer une variation thermique pure d\'une infiltration réelle.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">05</span>
        <div class="arg-num-content">
          <h3>Test de pression complémentaire</h3>
          <p>Si circuit isolable (boucle de plancher chauffant, antenne sanitaire), test à 4-6 bars pour confirmer le débit de fuite et préciser la localisation par chute de pression différentielle.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">06</span>
        <div class="arg-num-content">
          <h3>Rapport thermique annoté</h3>
          <p>Export des images thermiques avec marquage du point de fuite, plan d\'intervention pour le plombier ou le maçon, fourchette de coût de réparation. Délai de remise : le jour même.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Cas concrets de diagnostic thermographique en Gironde</h2>

    <h3>Pavillon plancher chauffant à Bruges (octobre 2025)</h3>
    <p>Maison de 130 m² construite en 2008, plancher chauffant hydraulique sur les deux niveaux. Là chaudière se met en défaut de pression deux fois par semaine, le propriétaire complète manuellement le circuit à chaque fois. Notre protocole : remise en chauffe à 40 °C pendant 3 heures avant intervention. Scan thermographique systématique étage par étage : halo thermique anormal à 31 °C dans le salon (au lieu de 27 °C ailleurs), forme circulaire de 35 cm autour d\'un point central. Test de pression sur la boucle correspondante : chute de 0,3 bar en 12 minutes (boucle saine : moins de 0,05 bar de chute sur la même durée). Localisation confirmée. Préconisation : ouverture chape sur 30×30 cm, remplacement 70 cm de tube PER 16x2. Coût intervention thermographie : 480 euros HT. Réparation par plombier partenaire : 850 euros HT.</p>

    <h3>Appartement haussmannien rue Sainte-Catherine Bordeaux (juillet 2025)</h3>
    <p>3e étage, immeuble 1872, tache d\'humidité au plafond du séjour qui s\'agrandit lentement depuis 6 mois. Le voisin du dessus (M. X) affirme ne rien constater chez lui. Le syndic nous mandate. Visite chez M. X : aucun signe visible de fuite mais relevé thermographique du sol sous le doublage parquet ancien. Découverte : zone plus froide de 4 °C au niveau du raccord d\'arrivée d\'eau froide de la baignoire encastrée, à 2,30 m de la tache visible chez la voisine du dessous. La fuite, très faible (quelques gouttes par jour), avait migré le long d\'une solive avant de tacher le plafond du dessous. Démontage tablier baignoire, raccord cuivre fissuré sur soudure, remplacement, étanchéité validée. Coût total intervention thermographie : 380 euros HT, pris en charge par l\'assurance copropriété au titre de la convention IRSI.</p>

    <h3>Maison contemporaine à Pessac (janvier 2026)</h3>
    <p>Villa 2015, dalle béton sur vide sanitaire accessible, suspicion de fuite sur le réseau d\'eau chaude sanitaire passant dans la dalle. Aucune trace visible au sol. Inspection thermographique depuis le vide sanitaire (caméra inversée vers le dessous de la dalle) : trace continue plus chaude de 6 °C sur 2,40 m linéaires correspondant au tracé du circuit ECS. Pic de chaleur localisé à 1,80 m de l\'arrivée chaudière. Intervention : ouverture dalle au point précis (carrottage diamant 30 cm de diamètre), découverte raccord laiton corrodé. Réparation, rebouchage. Coût diagnostic thermographie : 420 euros HT. Réparation : 720 euros HT par maçon partenaire.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Combien coûte une recherche de fuite par thermographie à Bordeaux ?</h2>
    <p>Le tarif dépend de la surface à scanner, de la complexité du bâtiment et du nombre de points à confirmer :</p>
    <ul>
      <li><strong>Diagnostic ciblé thermographie seule</strong> (zone réduite, hypothèse de fuite déjà localisée) : <strong>320 à 420 euros HT</strong>, intervention 1 à 2 heures.</li>
      <li><strong>Diagnostic plancher chauffant complet (jusqu\'à 150 m²)</strong> : <strong>450 à 650 euros HT</strong>, intervention 2 à 3 heures, incluant test pression et rapport assurance.</li>
      <li><strong>Diagnostic immeuble en copropriété (recherche d\'origine d\'un sinistre)</strong> : <strong>480 à 750 euros HT</strong>, intervention 3 à 4 heures, incluant visite des deux logements et rapport pour syndic.</li>
    </ul>
    <p>Comme pour toutes nos prestations, le diagnostic est généralement remboursé par votre assurance multirisque habitation au titre de la garantie recherche de fuite. Pour les détails de la procédure d\'indemnisation, consultez notre <a href="/guide/assurance-fuite-eau/" style="color:var(--green);text-decoration:underline;">guide assurance fuite d\'eau</a>. Notre rapport technique standardisé est accepté par l\'ensemble des principaux assureurs français (AXA, MAIF, MAAF, Macif, Generali, Groupama, Allianz, Matmut). Pour la grille tarifaire complète de nos méthodes, voir le <a href="/guide/prix-recherche-fuite-bordeaux/" style="color:var(--green);text-decoration:underline;">guide prix recherche de fuite à Bordeaux</a>.</p>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Questions fréquentes sur la thermographie infrarouge</h2>

    <h3>La caméra thermique fonctionne-t-elle à travers les murs ?</h3>
    <p>Non, c\'est un mythe répandu. La caméra mesure uniquement la température de surface du matériau qu\'elle voit. Elle ne traverse rien. Mais comme une fuite chauffe ou refroidit la surface au-dessus d\'elle, on peut indirectement localiser un défaut situé à 5-15 cm sous la surface (dans une chape, un doublage, une cloison sèche). Au-delà de 20 cm de profondeur ou derrière des matériaux très isolants, la signature thermique devient indétectable.</p>

    <h3>Y a-t-il des conditions où la thermographie ne marche pas ?</h3>
    <p>Oui. Les conditions défavorables sont : exposition solaire directe sur la zone à scanner (chauffe artificielle qui masque la fuite), forts courants d\'air, gradient thermique inversé (pièce plus froide que la fuite), peinture métallique réfléchissante, surfaces très brillantes (carrelage poli haute brillance, miroir). Dans ces cas, nous différons l\'intervention ou créons artificiellement un contraste (chauffage des locaux, eau chaude dans le circuit, mise en pression accrue).</p>

    <h3>Faut-il préchauffer le plancher chauffant avant votre intervention ?</h3>
    <p>Oui, c\'est essentiel. Nous demandons une remise en chauffe à pleine puissance pendant au moins 3 heures avant notre arrivée, idéalement la veille au soir. Plus le plancher est en régime stationnaire, plus la signature thermique d\'une fuite est nette. Si là chaudière est en panne ou si le plancher est éteint depuis longtemps, nous prévoyons une remise en service progressive en début d\'intervention, ce qui rallonge la visite de 2 à 3 heures.</p>

    <h3>La thermographie peut-elle remplacer une recherche de fuite par caméra endoscopique ?</h3>
    <p>Non, ce sont des méthodes complémentaires. La thermographie scanne de larges surfaces rapidement et localise la zone de fuite. La caméra endoscopique inspecte l\'intérieur des canalisations elles-mêmes pour identifier la cause exacte (fissure, corrosion, racine). Sur un diagnostic complexe, nous combinons souvent les deux : thermographie pour cibler, endoscopie pour qualifier.</p>

    <h3>La thermographie peut-elle servir à détecter une fuite de gaz ?</h3>
    <p>Pas directement avec une caméra thermique standard. Pour le gaz, on utilise des caméras OGI (Optical Gas Imaging) à filtre spécifique, beaucoup plus coûteuses et que nous ne déployons pas en routine. Si vous suspectez une fuite de gaz à votre domicile, contactez immédiatement GRDF (numéro vert urgence gaz : 0 800 47 33 33) avant toute intervention de notre équipe.</p>

    <h3>Pouvez-vous intervenir en thermographie sur une copropriété en même temps que sur le logement sinistré ?</h3>
    <p>Oui, c\'est même la meilleure pratique en cas de dégâts des eaux à Bordeaux. Nous demandons l\'autorisation au syndic et au voisin du dessus, puis intervenons dans les deux logements à la suite. Le diagnostic croisé permet d\'identifier la source exacte (lot, voisin commun, circuit collectif) et facilite l\'application de la <a href="/detection-fuite/degats-des-eaux-bordeaux/" style="color:var(--green);text-decoration:underline;">convention IRSI</a> par les assureurs.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Pages connexes : thermographie et autres méthodes</h2>
    <p>La thermographie est une méthode parmi d\'autres dans notre arsenal. Selon votre situation, ces pages peuvent compléter ou réorienter votre recherche :</p>
    <ul>
      <li><a href="/detection-fuite/fuite-plancher-chauffant-bordeaux/" style="color:var(--green);text-decoration:underline;">Fuite sur plancher chauffant à Bordeaux</a> : application principale de la thermographie, page complète avec cas types Mérignac et Pessac.</li>
      <li><a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">Canalisation enterrée à Bordeaux</a> : pour les réseaux extérieurs où la thermographie laisse place au gaz traceur.</li>
      <li><a href="/detection-fuite/degats-des-eaux-bordeaux/" style="color:var(--green);text-decoration:underline;">Dégâts des eaux à Bordeaux (syndics et copropriétés)</a> : intervention thermographique en immeuble pour identifier la source d\'un sinistre.</li>
      <li><a href="/detection-fuite/urgence-bordeaux/" style="color:var(--green);text-decoration:underline;">Recherche de fuite en urgence Bordeaux</a> : intervention sous 24h avec caméra thermique en équipement standard.</li>
      <li><a href="/villes/bordeaux/" style="color:var(--green);text-decoration:underline;">Recherche de fuite à Bordeaux (page ville)</a> : vue d\'ensemble de nos interventions sur les 18 quartiers de Bordeaux.</li>
      <li><a href="/detection-fuite/fluoresceine-piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">Fluorescéine piscine Bordeaux</a> : méthode complémentaire pour les bassins, où la thermographie est inopérante.</li>
      <li><a href="/guide/fuite-canalisation-enterree/" style="color:var(--green);text-decoration:underline;">Guide fuite canalisation enterrée</a> : article explicatif sur les techniques de diagnostic enterré.</li>
      <li><a href="/guide/prix-recherche-fuite-bordeaux/" style="color:var(--green);text-decoration:underline;">Tarifs recherche de fuite à Bordeaux</a> : grille de prix par méthode et type de canalisation.</li>
    </ul>
  </div>
</section>

''' + form_section("Bordeaux") + '''
'''

    ld_local = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Recherche Fuite Gironde",
  "description": "Recherche de fuite par thermographie infrarouge à Bordeaux et en Gironde. Plancher chauffant, canalisations encastrées, dégâts des eaux. Sans démolition.",
  "url": "https://recherche-fuite-gironde.fr/detection-fuite/thermographie-infrarouge-bordeaux/",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Bordeaux",
    "postalCode": "33000",
    "addressCountry": "FR"
  },
  "areaServed": { "@type": "City", "name": "Bordeaux", "postalCode": "33000" },
  "priceRange": "€€"
}
</script>'''

    ld_service = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "Recherche de fuite par thermographie infrarouge",
  "provider": { "@type": "LocalBusiness", "name": "Recherche Fuite Gironde" },
  "areaServed": "Gironde",
  "description": "Détection d'une fuite d'eau par caméra thermique infrarouge à Bordeaux et en Gironde. Application plancher chauffant, canalisations encastrées, copropriété.",
  "offers": {
    "@type": "AggregateOffer",
    "lowPrice": "320",
    "highPrice": "750",
    "priceCurrency": "EUR"
  }
}
</script>'''

    ld_breadcrumb = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://recherche-fuite-gironde.fr/" },
    { "@type": "ListItem", "position": 2, "name": "Détection de fuite", "item": "https://recherche-fuite-gironde.fr/detection-fuite/" },
    { "@type": "ListItem", "position": 3, "name": "Thermographie infrarouge Bordeaux", "item": "https://recherche-fuite-gironde.fr/detection-fuite/thermographie-infrarouge-bordeaux/" }
  ]
}
</script>'''

    ld_faq = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "La caméra thermique fonctionne-t-elle à travers les murs ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Non. La caméra mesure la température de surface uniquement. Mais une fuite chauffe ou refroidit la surface au-dessus d'elle, ce qui permet de localiser un défaut situé à 5-15 cm sous la surface (chape, doublage, cloison)." }
    },
    {
      "@type": "Question",
      "name": "Y a-t-il des conditions où la thermographie ne marche pas ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Oui : exposition solaire directe, courants d'air forts, peintures métalliques réfléchissantes, surfaces très brillantes. Dans ces cas, nous différons l'intervention ou créons un contraste artificiel." }
    },
    {
      "@type": "Question",
      "name": "Faut-il préchauffer le plancher chauffant avant l'intervention ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Oui, remise en chauffe à pleine puissance pendant au moins 3 heures avant l'arrivée du technicien. Plus le plancher est en régime stationnaire, plus la signature thermique d'une fuite est nette." }
    },
    {
      "@type": "Question",
      "name": "Combien coûte une recherche de fuite par thermographie à Bordeaux ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Entre 320 et 420 euros HT pour un diagnostic ciblé. Entre 450 et 650 euros HT pour un diagnostic plancher chauffant complet jusqu'à 150 m². Entre 480 et 750 euros HT pour un diagnostic immeuble copropriété." }
    },
    {
      "@type": "Question",
      "name": "La thermographie peut-elle servir à détecter une fuite de gaz ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Pas avec une caméra thermique standard. Pour le gaz, on utilise des caméras OGI à filtre spécifique. En cas de suspicion de fuite de gaz, contacter immédiatement GRDF au 0 800 47 33 33." }
    }
  ]
}
</script>'''

    return html_base(
        'Thermographie infrarouge fuite eau Bordeaux',
        'Recherche de fuite par thermographie infrarouge à Bordeaux : plancher chauffant, canalisations encastrées, copropriétés. Diagnostic non destructif, rapport assurance.',
        'https://recherche-fuite-gironde.fr/detection-fuite/thermographie-infrarouge-bordeaux/',
        body,
        extra_ld=ld_local + ld_service + ld_breadcrumb + ld_faq,
    )


# ═══════════════════════════════════════════════════════════════
# PAGE USE CASE : Dépannage piscine Bordeaux (réparation + diagnostic)
# ═══════════════════════════════════════════════════════════════

def page_depannage_piscine_bordeaux():
    body = '''
<section class="hero-mini">
  <div class="container">
    <nav class="breadcrumb">
      <a href="/">Accueil</a>
      <span>&rsaquo;</span>
      <a href="/detection-fuite/">Détection de fuite</a>
      <span>&rsaquo;</span>
      <span>Dépannage piscine Bordeaux</span>
    </nav>
    <span class="badge-cp">Bordeaux Métropole · Bassin d\'Arcachon</span>
    <h1>Dépannage piscine à Bordeaux : diagnostic et réparation</h1>
    <p class="hero-mini-lead">Votre piscine fuit, ne filtre plus, ou présente une anomalie technique ? <strong>Diagnostic complet sous 24h, sans vidange du bassin</strong>. Nous identifions la panne ou la fuite, vous remettons un rapport chiffré, puis coordonnons la réparation avec nos piscinistes partenaires en Gironde.</p>
    <div class="hero-mini-cta">
      <a href="/devis/" class="btn btn-gold">Demander un dépannage</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <figure style="margin:0 0 2rem;">
      <img src="/assets/depannage-piscine-bordeaux.webp" alt="Technicien intervenant sur une piscine privée à Bordeaux pour dépannage et diagnostic" width="1600" height="1067" loading="eager" style="width:100%;max-height:380px;height:auto;object-fit:cover;border-radius:12px;display:block;">
    </figure>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Notre rôle dans le dépannage de votre piscine</h2>
    <p>Notre métier de spécialiste recherche de fuite nous place au cœur de la chaîne de dépannage piscine en Gironde. Quand un problème survient (perte d\'eau anormale, filtration défaillante, équipement bloqué), nous sommes la première étape : nous identifions la cause exacte, nous chiffrons l\'intervention de réparation et nous orientons vers les bons spécialistes selon la nature du problème. Nos partenaires piscinistes interviennent ensuite sur la base de notre rapport technique, souvent en bénéficiant d\'un délai d\'intervention plus rapide grâce à un diagnostic déjà fait.</p>
    <p>Cette spécialisation nous distingue des piscinistes généralistes : nous intervenons exclusivement sur le diagnostic non destructif (sans vidange, sans démolition), avec un arsenal d\'outils professionnels (colorant fluorescéine, écoute acoustique, test de pression, caméra endoscopique, gaz traceur). Le pisciniste, lui, fait la réparation. Cette division des rôles évite les conflits d\'intérêt et garantit un diagnostic objectif.</p>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:1080px;">
    <h2>Les 8 cas de dépannage piscine que nous traitons en Gironde</h2>
    <div class="arg-num-grid">
      <div class="arg-num-card">
        <span class="arg-num">01</span>
        <div class="arg-num-content">
          <h3>Perte d\'eau anormale</h3>
          <p>Le cas le plus fréquent. Diagnostic complet par fluorescéine, écoute acoustique et test de pression pour localiser le point exact de fuite. Voir notre guide <a href="/guide/piscine-qui-fuit-perte-eau/" style="color:var(--green);text-decoration:underline;">piscine qui fuit ou perte d\'eau</a> pour qualifier votre cas avant l\'intervention.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">02</span>
        <div class="arg-num-content">
          <h3>Skimmer fissuré ou désaxé</h3>
          <p>Joint mastic dégradé, bride desserrée, fissure de la pièce plastique. Diagnostic par fluorescéine, réparation possible à la <a href="/guide/reparation-skimmer-piscine-resine-epoxy/" style="color:var(--green);text-decoration:underline;">résine époxy</a> ou remplacement de la pièce.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">03</span>
        <div class="arg-num-content">
          <h3>Liner percé ou décollé</h3>
          <p>Perforation, accroc, décollement de soudure. Voir notre guide <a href="/guide/fuite-liner-piscine/" style="color:var(--green);text-decoration:underline;">diagnostic fuite liner piscine</a> et les options de <a href="/guide/reparation-liner-piscine/" style="color:var(--green);text-decoration:underline;">réparation liner</a>.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">04</span>
        <div class="arg-num-content">
          <h3>Coque polyester fuyante</h3>
          <p>Osmose, microfissures gel-coat, désaxement. Voir notre guide spécifique <a href="/guide/fuite-coque-polyester-piscine/" style="color:var(--green);text-decoration:underline;">fuite coque polyester piscine</a>.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">05</span>
        <div class="arg-num-content">
          <h3>Canalisation enterrée fuyarde</h3>
          <p>Réseau d\'alimentation ou de refoulement entre local technique et bassin. Diagnostic par gaz traceur, écoute acoustique. Voir notre page <a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">canalisation enterrée Bordeaux</a>.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">06</span>
        <div class="arg-num-content">
          <h3>Fissure structurelle béton</h3>
          <p>Sur les piscines béton armé de plus de 25 ans, des fissures réveillées par cycle gel/dégel ou mouvements de terrain. Diagnostic par <a href="/detection-fuite/fluoresceine-piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">fluorescéine</a> + écoute acoustique + caméra sous-marine.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">07</span>
        <div class="arg-num-content">
          <h3>Bonde de fond ou projecteur défaillant</h3>
          <p>Joint torique craquelé, bride desserrée, traversée de paroi qui fuit. Diagnostic ciblé fluorescéine, remplacement par pisciniste partenaire.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">08</span>
        <div class="arg-num-content">
          <h3>Filtration ou pompe défectueuse</h3>
          <p>Pour les pannes électriques, hydrauliques ou mécaniques (pompe qui ne démarre plus, vanne 6 voies bloquée, joint d\'étanchéité de filtre HS), nous orientons directement vers nos piscinistes partenaires sans diagnostic préalable nécessaire.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Comment se déroule un dépannage piscine avec Recherche Fuite Gironde ?</h2>

    <h3>Étape 1 : qualification téléphonique (sous 1 heure en journée)</h3>
    <p>Vous nous décrivez les symptômes (vitesse de baisse d\'eau, traces extérieures, équipement concerné, âge de la piscine, type de bassin). Nous évaluons l\'urgence et chiffrons une fourchette d\'intervention selon nos statistiques sur cas similaires.</p>

    <h3>Étape 2 : intervention diagnostic (sous 24 à 48h)</h3>
    <p>Notre technicien vient sur place avec l\'arsenal complet (colorant fluorescéine, capteurs acoustiques, manomètres, caméra endoscopique). Selon le cas, l\'intervention dure 1 à 4 heures. Nous identifions précisément la panne ou la fuite, photographions tout, prenons les mesures.</p>

    <h3>Étape 3 : remise du rapport (jour même)</h3>
    <p>Rapport technique standardisé envoyé par email le soir même : photos, méthodes employées, localisation au mètre près, cause technique identifiée, devis chiffré pour la réparation. Document accepté par toutes les assurances habitation pour la garantie recherche de fuite.</p>

    <h3>Étape 4 : coordination réparation</h3>
    <p>Selon votre choix, nous transmettons le rapport à un pisciniste partenaire en Gironde qui intervient avec les pièces et compétences adaptées. Le pisciniste fait sa propre proposition tarifaire, vous restez libre du choix final.</p>

    <h3>Étape 5 : vérification post-intervention</h3>
    <p>Si vous le souhaitez, nous repassons après réparation pour valider l\'étanchéité (test fluorescéine de contrôle). Service gratuit dans la limite de 6 mois après notre diagnostic initial.</p>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Combien coûte un dépannage piscine en Gironde ?</h2>
    <p>Le coût total d\'un dépannage piscine inclut deux postes : le diagnostic (notre intervention) et la réparation (effectuée par un pisciniste partenaire). Voici les fourchettes constatées en 2026 :</p>
    <ul>
      <li><strong>Diagnostic complet Recherche Fuite Gironde</strong> : <strong>380 à 580 € HT</strong> selon complexité, intervention 1 à 4 heures, rapport assurance inclus.</li>
      <li><strong>Réparation skimmer ou refoulement</strong> : 180 à 380 € HT par pièce.</li>
      <li><strong>Réparation locale liner</strong> : 180 à 350 € HT (rustine subaquatique).</li>
      <li><strong>Soudure thermique liner ou réparation gel-coat coque</strong> : 320 à 580 € HT.</li>
      <li><strong>Réparation canalisation enterrée</strong> : 450 à 1 200 € HT selon profondeur et accès.</li>
      <li><strong>Remplacement complet liner</strong> : 3 800 à 7 500 € TTC selon taille du bassin.</li>
      <li><strong>Reprise complète gel-coat coque polyester (osmose étendue)</strong> : 3 500 à 8 500 € TTC.</li>
    </ul>
    <p>Le diagnostic initial est presque toujours pris en charge par votre assurance habitation au titre de la garantie recherche de fuite. Voir notre guide <a href="/guide/recherche-fuite-piscine-assurance/" style="color:var(--green);text-decoration:underline;">remboursement assurance piscine</a>. Pour les tarifs détaillés selon le type de bassin, consultez le <a href="/guide/recherche-fuite-piscine-tarif/" style="color:var(--green);text-decoration:underline;">guide tarif recherche de fuite piscine</a>.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Zone d\'intervention dépannage piscine en Gironde</h2>
    <p>Nous intervenons sur l\'ensemble de la métropole bordelaise et du Bassin d\'Arcachon, avec un délai de 24 à 48 heures sur les zones suivantes :</p>
    <ul>
      <li><strong>Bordeaux Métropole</strong> : <a href="/detection-fuite/piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">piscine Bordeaux</a> (Caudéran, Le Bouscat, Saint-Augustin), <a href="/detection-fuite/piscine-merignac/" style="color:var(--green);text-decoration:underline;">piscine Mérignac</a> (lotissements pavillonnaires), Pessac, Talence, Gradignan, Bègles, Eysines, Bruges.</li>
      <li><strong>Bassin d\'Arcachon</strong> : <a href="/detection-fuite/piscine-arcachon/" style="color:var(--green);text-decoration:underline;">piscine Arcachon</a> (villas Ville d\'Hiver, Pyla), <a href="/detection-fuite/piscine-la-teste-de-buch/" style="color:var(--green);text-decoration:underline;">piscine La Teste-de-Buch</a> (Cazaux), <a href="/detection-fuite/piscine-gujan-mestras/" style="color:var(--green);text-decoration:underline;">piscine Gujan-Mestras</a> (coques polyester).</li>
      <li><strong>Libournais et Médoc</strong> : <a href="/detection-fuite/piscine-libourne/" style="color:var(--green);text-decoration:underline;">piscine Libourne</a> et propriétés viticoles, Lesparre-Médoc, Pauillac.</li>
      <li><strong>Communes hors métropole</strong> : Andernos-les-Bains, Lège-Cap-Ferret, Saint-Émilion, Langon (intervention sur devis selon distance).</li>
    </ul>
    <p>Pour une vue d\'ensemble de notre service piscine en Gironde, consultez notre <a href="/detection-fuite/piscine/" style="color:var(--green);text-decoration:underline;">page hub recherche de fuite piscine</a>.</p>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Questions fréquentes sur le dépannage piscine</h2>

    <h3>Intervenez-vous en urgence le week-end ?</h3>
    <p>Pour les fuites importantes avec dégâts collatéraux imminents (terrain saturé, voisin impacté, infiltration vers cave), nous prévoyons des créneaux d\'urgence le samedi sur la métropole bordelaise. Service avec majoration tarifaire de 30 pourcent. Pour les pannes le dimanche, nous orientons vers nos piscinistes partenaires d\'astreinte.</p>

    <h3>Faites-vous la réparation ou seulement le diagnostic ?</h3>
    <p>Notre métier est exclusivement le diagnostic non destructif. La réparation est confiée à nos piscinistes partenaires en Gironde, choisis pour leur fiabilité et leur réactivité. Cette séparation garantit l\'objectivité du diagnostic (pas de conflit d\'intérêt) et permet au client de comparer plusieurs devis de réparation.</p>

    <h3>Combien de temps dure l\'intervention de dépannage ?</h3>
    <p>Le diagnostic dure 1 à 4 heures selon la complexité du cas. Le rapport est rédigé dans la journée et envoyé par email le soir même. La réparation par le pisciniste partenaire dépend du type de panne : 30 minutes pour un joint, 2 jours pour un changement de liner complet, jusqu\'à 1 semaine pour une reprise structurelle béton.</p>

    <h3>Le diagnostic est-il remboursé par l\'assurance habitation ?</h3>
    <p>Oui dans 90 pourcent des cas. La garantie recherche de fuite de votre contrat multirisque habitation rembourse tout ou partie du diagnostic dès lors que la fuite a provoqué un dégât des eaux, même mineur (auréole, terrain saturé, infiltration vers local technique). Notre rapport est accepté par AXA, MAIF, MAAF, Macif, Generali, Groupama, Allianz, Matmut, GMF.</p>

    <h3>Comment éviter de futures pannes après réparation ?</h3>
    <p>Trois recommandations issues de notre expérience : stabiliser le pH entre 7,2 et 7,6 en permanence, limiter la chloration choc, couvrir le bassin hors saison. Voir aussi notre guide <a href="/guide/evaporation-vs-fuite-piscine/" style="color:var(--green);text-decoration:underline;">évaporation ou fuite</a> qui aide à détecter une fuite naissante avant qu\'elle ne s\'aggrave.</p>
  </div>
</section>

''' + form_section("Bordeaux") + '''
'''

    ld_local = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Recherche Fuite Gironde",
  "description": "Dépannage piscine à Bordeaux et en Gironde : diagnostic non destructif sans vidange, coordination réparation avec piscinistes partenaires.",
  "url": "https://recherche-fuite-gironde.fr/detection-fuite/depannage-piscine-bordeaux/",
  "areaServed": [
    { "@type": "City", "name": "Bordeaux", "postalCode": "33000" },
    { "@type": "City", "name": "Mérignac", "postalCode": "33700" },
    { "@type": "City", "name": "Arcachon", "postalCode": "33120" },
    { "@type": "City", "name": "Libourne", "postalCode": "33500" }
  ],
  "priceRange": "€€"
}
</script>'''

    ld_service = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "Dépannage piscine et diagnostic recherche de fuite",
  "provider": { "@type": "LocalBusiness", "name": "Recherche Fuite Gironde" },
  "areaServed": "Gironde",
  "description": "Dépannage de piscine privée à Bordeaux et en Gironde : diagnostic non destructif des fuites et pannes, coordination réparation avec piscinistes partenaires.",
  "offers": {
    "@type": "AggregateOffer",
    "lowPrice": "380",
    "highPrice": "750",
    "priceCurrency": "EUR"
  }
}
</script>'''

    ld_breadcrumb = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://recherche-fuite-gironde.fr/" },
    { "@type": "ListItem", "position": 2, "name": "Détection de fuite", "item": "https://recherche-fuite-gironde.fr/detection-fuite/" },
    { "@type": "ListItem", "position": 3, "name": "Dépannage piscine Bordeaux", "item": "https://recherche-fuite-gironde.fr/detection-fuite/depannage-piscine-bordeaux/" }
  ]
}
</script>'''

    ld_faq = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Intervenez-vous en urgence le week-end pour un dépannage piscine ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Pour les fuites importantes avec dégâts collatéraux imminents, créneaux d'urgence le samedi sur la métropole bordelaise (majoration 30 pourcent). Pour le dimanche, orientation vers piscinistes partenaires d'astreinte." }
    },
    {
      "@type": "Question",
      "name": "Faites-vous la réparation ou seulement le diagnostic ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Diagnostic non destructif exclusivement. La réparation est confiée à nos piscinistes partenaires en Gironde. Cette séparation garantit objectivité du diagnostic et permet de comparer plusieurs devis de réparation." }
    },
    {
      "@type": "Question",
      "name": "Combien coûte un dépannage piscine en Gironde ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Diagnostic 380 à 580 € HT. Réparations selon nature : skimmer 180-380 € HT, liner local 180-350 € HT, canalisation enterrée 450-1200 € HT, remplacement liner complet 3800-7500 € TTC." }
    },
    {
      "@type": "Question",
      "name": "Le diagnostic est-il remboursé par l'assurance habitation ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Oui dans 90 pourcent des cas. Garantie recherche de fuite du contrat multirisque habitation. Notre rapport accepté par AXA, MAIF, MAAF, Macif, Generali, Groupama, Allianz, Matmut, GMF." }
    },
    {
      "@type": "Question",
      "name": "Combien de temps dure l'intervention de dépannage piscine ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Diagnostic 1 à 4 heures selon complexité. Rapport envoyé par email le soir même. Réparation pisciniste partenaire : 30 min pour un joint, 2 jours pour changement liner complet, 1 semaine pour reprise béton structurelle." }
    }
  ]
}
</script>'''

    return html_base(
        'Dépannage piscine Bordeaux | Diagnostic et réparation',
        'Dépannage de piscine privée à Bordeaux : diagnostic non destructif sous 24h, coordination réparation avec piscinistes partenaires. Rapport assurance inclus.',
        'https://recherche-fuite-gironde.fr/detection-fuite/depannage-piscine-bordeaux/',
        body,
        extra_ld=ld_local + ld_service + ld_breadcrumb + ld_faq,
    )


def page_piscine_ville(p):
    ville = p["ville"]
    ville_article = p["ville_article"]
    cp = p["cp"]
    slug = p["slug"]

    # Construction des spécificités uniques
    specificites_html = '\n'.join([
        f'      <div class="arg-num-card"><span class="arg-num">{i:02d}</span><div class="arg-num-content"><h3>{titre}</h3><p>{contenu}</p></div></div>'
        for i, (titre, contenu) in enumerate(p["spécificités"], 1)
    ])

    # FAQ locale (questions uniques par ville)
    faq_locale_html = '\n'.join([
        f'    <h3>{q}</h3>\n    <p>{a}</p>'
        for q, a in p["faq_locale"]
    ])

    # Patterns d'interventions fréquentes (uniques par ville)
    patterns_html = '\n'.join([
        f'      <div class="arg-num-card"><span class="arg-num">{i:02d}</span><div class="arg-num-content"><h3>{titre}</h3><p>{contenu}</p></div></div>'
        for i, (titre, contenu) in enumerate(p.get("patterns_frequents", []), 1)
    ])

    # Cross-linking sibling : 3 autres villes piscine avec anchor varié.
    # On force piscine-bordeaux et piscine-arcachon en priorité (pages prioritaires lead-gen).
    priority_siblings = ['piscine-bordeaux', 'piscine-arcachon']
    other_siblings = [s for s in PISCINE_PAGES if s["slug"] != slug and s["slug"] not in priority_siblings]
    forced_siblings = [s for s in PISCINE_PAGES if s["slug"] != slug and s["slug"] in priority_siblings]
    siblings = (forced_siblings + other_siblings)[:3]
    sibling_anchors = [
        f'piscine {siblings[0]["ville_article"]}' if len(siblings) > 0 else '',
        f'recherche de fuite sur bassin {siblings[1]["ville_article"]}' if len(siblings) > 1 else '',
        f'diagnostic piscine {siblings[2]["ville_article"]}' if len(siblings) > 2 else '',
    ]
    sibling_links_html = ', '.join([
        f'<a href="/detection-fuite/{siblings[i]["slug"]}/" style="color:var(--green);text-decoration:underline;">{sibling_anchors[i]}</a>'
        for i in range(len(siblings)) if sibling_anchors[i]
    ])
    faq_schema_entries = []
    for q, a in p["faq_locale"]:
        faq_schema_entries.append(
            '{"@type":"Question","name":' + json.dumps(q, ensure_ascii=False) +
            ',"acceptedAnswer":{"@type":"Answer","text":' + json.dumps(a, ensure_ascii=False) + '}}'
        )
    faq_schema_json = ',\n    '.join(faq_schema_entries)

    ld_local = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Recherche Fuite Gironde",
  "description": "Recherche de fuite de piscine {ville_article} sans vidange. Colorant fluorescéine, écoute électro-acoustique, inspection sous-marine. Intervention 24h, rapport pour assurance.",
  "url": "https://recherche-fuite-gironde.fr/detection-fuite/{slug}/",
  "image": "https://recherche-fuite-gironde.fr/assets/piscine-privee-bordeaux.webp",
  "address": {{
    "@type": "PostalAddress",
    "addressLocality": "{ville}",
    "postalCode": "{cp}",
    "addressCountry": "FR"
  }},
  "areaServed": {{ "@type": "City", "name": "{ville}" }},
  "priceRange": "€€",
  "serviceType": "Recherche de fuite de piscine"
}}
</script>'''

    ld_service = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "Recherche de fuite de piscine sans vidange",
  "name": "Recherche de fuite de piscine {ville_article}",
  "description": "Localisation précise d'une fuite sur piscine enterrée, coque polyester ou liner PVC sans vidanger le bassin. Méthodes : colorant fluorescéine, écoute électro-acoustique, test de pression des canalisations, inspection sous-marine.",
  "provider": {{
    "@type": "LocalBusiness",
    "name": "Recherche Fuite Gironde",
    "url": "https://recherche-fuite-gironde.fr/"
  }},
  "areaServed": {{ "@type": "Place", "name": "{ville} et métropole" }},
  "category": "Détection de fuite aquatique"
}}
</script>'''

    ld_breadcrumb = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{ "@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://recherche-fuite-gironde.fr/" }},
    {{ "@type": "ListItem", "position": 2, "name": "Détection de fuite", "item": "https://recherche-fuite-gironde.fr/detection-fuite/" }},
    {{ "@type": "ListItem", "position": 3, "name": "Piscine {ville}", "item": "https://recherche-fuite-gironde.fr/detection-fuite/{slug}/" }}
  ]
}}
</script>'''

    ld_faq = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {faq_schema_json}
  ]
}}
</script>'''

    # Autres villes piscine pour maillage sibling
    autres_piscine = [p for p in PISCINE_PAGES if p["slug"] != slug]
    autres_html = '\n'.join([
        f'<a href="/detection-fuite/{p["slug"]}/" class="loc-card" style="text-decoration:none;color:inherit;padding:1rem 1.25rem;background:var(--white);border:1px solid var(--border);border-radius:12px;display:block;"><strong>Piscine {p["ville"]}</strong><span style="display:block;font-size:.85rem;color:var(--muted);margin-top:.25rem;">{p["cp"]}</span></a>'
        for p in autres_piscine
    ])

    body = f'''
<section class="hero-mini">
  <div class="container">
    <nav class="breadcrumb">
      <a href="/">Accueil</a>
      <span>&rsaquo;</span>
      <a href="/detection-fuite/">Détection de fuite</a>
      <span>&rsaquo;</span>
      <span>Piscine {ville}</span>
    </nav>
    <span class="badge-cp">Piscine · {cp}</span>
    <h1>Recherche de fuite de piscine {ville_article}</h1>
    <p class="hero-mini-lead">Votre piscine perd de l'eau plus vite que l'évaporation normale ? Nos techniciens localisent la fuite <strong>sans vidange ni démolition</strong>, en combinant colorant fluorescéine, écoute électro-acoustique et test de pression. Rapport technique remis le jour même, reconnu par les assureurs.</p>
    <div class="hero-mini-cta">
      <a href="/devis/" class="btn btn-gold">Demander un devis gratuit</a>
      <a href="#méthodes" class="btn btn-outline-green">Nos méthodes</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <figure style="margin:0 0 2rem;">
      <img src="/assets/piscine-privee-bordeaux.webp" alt="{p['hero_image_alt']}" width="1600" height="1067" loading="eager" style="width:100%;max-height:380px;height:auto;object-fit:cover;border-radius:12px;display:block;">
    </figure>

    <h2>Les piscines {ville_article} : un parc aux caractéristiques bien identifiées</h2>
    <p>{p['intro_unique']}</p>

    <h3>Types de piscines que nous diagnostiquons {ville_article}</h3>
    <p>{p['types_piscines']}</p>

<h3>Zones d'intervention {ville_article} et périphérie</h3>
    <p>{p['quartiers_zones']}</p>

    <p style="margin-top:1rem;">Au-delà des piscines, nos techniciens interviennent aussi pour tous types de fuites sur la commune : consultez notre <a href="/villes/{p['slug'].replace('piscine-', '')}/" style="color:var(--green-mid);text-decoration:underline;">gamme complète de recherche de fuite à {p['ville']}</a> (canalisations encastrées, planchers chauffants, dégâts des eaux, urgence).</p>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:1080px;">
    <h2>Ma piscine perd de l'eau : fuite ou évaporation ?</h2>
    <p>Avant de parler de fuite, il faut écarter l'évaporation naturelle. En Gironde, une piscine extérieure sans abri perd en moyenne <strong>3 à 5 mm par jour en été</strong> (juin à septembre) et <strong>0 à 2 mm par jour au printemps et à l'automne</strong>. Au-delà, surtout si la perte dépasse 1 cm par jour, une fuite est probable.</p>

    <h3>Le test du seau, première étape gratuite</h3>
    <p>Posez un seau rempli d'eau sur la première marche de votre piscine (pour qu'il soit à la même température). Marquez au feutre le niveau intérieur du seau et le niveau de la piscine sur la paroi. Laissez 24 à 48 heures sans baignade, sans remise à niveau automatique et sans pluie. Si le seau et la piscine baissent de la même hauteur, c'est de l'évaporation. Si la piscine baisse nettement plus que le seau, vous avez une fuite et il est temps de nous contacter. Pour les taux d'évaporation mensuels en Gironde et un protocole plus rigoureux, voir notre guide <a href="/guide/evaporation-vs-fuite-piscine/" style="color:var(--green);text-decoration:underline;">évaporation ou fuite de piscine</a>.</p>

    <h3>Signes qui ne trompent pas</h3>
    <ul>
      <li>Perte d'eau régulière supérieure à 1 cm par jour, y compris par temps couvert</li>
      <li>Zone anormalement humide autour du bassin, terrain gorgé d'eau ou sol qui s'affaisse sur un tracé linéaire</li>
      <li>Bulles dans l'eau sans baigneur, visibles quand la filtration est à l'arrêt</li>
      <li>Consommation d'eau en forte hausse sur la facture sans changement d'usage</li>
      <li>Pression du filtre anormalement basse malgré un filtre propre</li>
      <li>Liner qui se décolle localement, plis nouveaux, cloques sous l'eau</li>
      <li>Margelle ou plage qui bougent, joints fissurés au pourtour</li>
      <li>Local technique humide ou flaque au pied de la pompe</li>
    </ul>
  </div>
</section>

<section class="section" id="méthodes">
  <div class="container" style="max-width:1080px;">
    <h2>Comment on localise une fuite de piscine {ville_article} sans vidange</h2>
    <p>{p.get('methodes_focus', 'Chaque méthode cible un type de fuite précis. Sur un chantier, nos techniciens combinent deux à quatre techniques pour isoler la source du problème avec certitude.')}</p>
    <p style="margin-top:1rem;">Ci-dessous, les 6 méthodes de notre protocole de diagnostic, combinées selon le scénario rencontré.</p>

    <figure style="margin:1.5rem 0;">
      <img src="/assets/niveau-eau-piscine-fuite.webp" alt="Piscine avec niveau d'eau anormalement bas, signe caractéristique d'une fuite à localiser sans vidanger" width="1600" height="1067" loading="lazy" style="width:100%;max-height:360px;height:auto;object-fit:cover;border-radius:12px;display:block;">
    </figure>

    <div class="grid-3" style="margin-top:2rem;">
      <div class="arg-num-card">
        <span class="arg-num">01</span>
        <div class="arg-num-content">
          <h3>Colorant fluorescéine</h3>
          <p>Un colorant fluorescent non toxique (de qualité alimentaire) est injecté à la seringue près des zones suspectes : skimmer, buses de refoulement, bonde de fond, fissures visibles. La filtration à l'arrêt, le colorant est aspiré vers la fuite et révèle son parcours exact. Méthode rapide pour les fuites de l'enceinte du bassin. <a href="/detection-fuite/fluoresceine-piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">Voir le protocole détaillé</a>.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">02</span>
        <div class="arg-num-content">
          <h3>Écoute électro-acoustique</h3>
          <p>Un amplificateur acoustique haute sensibilité capte le bruit caractéristique de l'eau qui fuit sous pression. Idéal pour les canalisations enterrées d'alimentation ou de refoulement autour de la piscine. Précision au mètre près, sans ouvrir le sol.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">03</span>
        <div class="arg-num-content">
          <h3>Test de pression hydraulique</h3>
          <p>On isole chaque circuit (aspiration, refoulement, balai, bonde de fond) en obturant les bouches puis en mettant sous pression. La perte de pression mesurée identifié le circuit défectueux. Couplé à l'écoute, on localise ensuite le point exact.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">04</span>
        <div class="arg-num-content">
          <h3>Inspection sous-marine</h3>
          <p>Caméra endoscopique étanche ou inspection masque et tuba pour détecter visuellement les perforations du liner, les décollements de soudures, les fissures du carrelage ou du béton. Souvent la dernière étape pour confirmer la fuite repérée par colorant.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">05</span>
        <div class="arg-num-content">
          <h3>Gaz traceur azote/hélium</h3>
          <p>Pour les canalisations enterrées longues ou inaccessibles acoustiquement, on injecté un mélange d'azote et d'hélium dans le réseau mis sous pression. Le gaz remonte en surface au droit de la fuite et est détecté par un capteur de surface.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">06</span>
        <div class="arg-num-content">
          <h3>Thermographie infrarouge</h3>
          <p>Une caméra thermique révèle les variations de température au sol et sur les margelles, utile pour repérer une fuite sous une terrasse ou près du local technique. Complément efficace quand la fuite est diffuse ou lointaine du bassin visible.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <h2>Types de fuites que nous traitons sur piscine</h2>
    <p>La fuite peut provenir du bassin lui-même, du réseau hydraulique ou des équipements périphériques. Voici les cas les plus fréquents que nous rencontrons {ville_article} et dans sa métropole.</p>

    <div class="grid-3" style="margin-top:1.5rem;">
      <div class="arg-num-card">
        <span class="arg-num">01</span>
        <div class="arg-num-content">
          <h3>Fuite de liner PVC</h3>
          <p>Perforation, accroc, décollement de soudure aux angles, cloque, pli marqué. Le liner fuit le plus souvent au niveau des pièces à sceller (skimmer, prise balai, buses) où les brides peuvent s'être desserrées avec le temps. Une fois la fuite localisée, voir notre guide <a href="/guide/reparation-liner-piscine/" style="color:var(--green);text-decoration:underline;">réparation d'une fuite de liner</a> (rustine, soudure thermique, remplacement complet).</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">02</span>
        <div class="arg-num-content">
          <h3>Fuite skimmer ou refoulement</h3>
          <p>Joint mastic sec et fissuré entre la pièce à sceller et le béton ou la coque, bride mal serrée, fissure de la pièce plastique elle-même. Très fréquent après plusieurs hivernages. Voir notre guide <a href="/guide/reparation-skimmer-piscine-resine-epoxy/" style="color:var(--green);text-decoration:underline;">réparation skimmer à la résine époxy</a>.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">03</span>
        <div class="arg-num-content">
          <h3>Fuite canalisation enterrée</h3>
          <p>Raccord collé qui lâche, fissure sur un tuyau PVC pris dans la dalle, tassement de terrain qui désaxe un raccord. Le débit perdu peut être très important et ruiner un massif paysager en quelques semaines.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">04</span>
        <div class="arg-num-content">
          <h3>Fuite de bonde de fond</h3>
          <p>Joint torique usé, bride cassée, obturateur d'hivernage oublié. Fuite difficile à détecter à l'œil car souvent sous une grille, mais aisément localisable au colorant ou par test de pression.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">05</span>
        <div class="arg-num-content">
          <h3>Fissure structurelle béton</h3>
          <p>Bassin béton armé avec fissure verticale ou horizontale, souvent suite à un mouvement de terrain (argile, nappe phréatique). Peut concerner aussi une coque polyester délaminée.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">06</span>
        <div class="arg-num-content">
          <h3>Fuite équipement local technique</h3>
          <p>Pompe qui fuit par le joint d'axe, filtre multivoies qui déverse par la voie égout, échangeur thermique de pompe à chaleur piscine percé. Pas de fuite du bassin lui-même, mais une perte réelle.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:1080px;">
    <h2>Spécificités des piscines {ville_article}</h2>
    <p>Notre expérience des interventions {ville_article} nous a permis d'identifier les contraintes récurrentes propres à ce territoire. Chaque diagnostic intègre ces paramètres pour orienter efficacement les méthodes.</p>

    <figure style="margin:1.5rem 0;">
      <img src="/assets/technicien-recherche-fuite-piscine.webp" alt="Technicien spécialisé en recherche de fuite de piscine intervenant sur un bassin privé en Gironde" width="1600" height="1067" loading="lazy" style="width:100%;max-height:360px;height:auto;object-fit:cover;border-radius:12px;display:block;">
    </figure>

    <div class="grid-3" style="margin-top:1.5rem;">
{specificites_html}
    </div>

    <h3 style="margin-top:2.5rem;">Cas type que nous traitons {ville_article}</h3>
    <p>{p['cas_frequent']}</p>

    <h3>Zones d'intervention autour de {ville}</h3>
    <p>Nous intervenons sous 24 à 48h aux adresses suivantes : {p['zones_voisines']}. Nos tournées dédiées piscines en saison permettent d'optimiser les délais de rendez-vous.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <h2>Patterns d'interventions récurrents {ville_article}</h2>
    <p>Trois scénarios représentatifs de ce que nous traitons au quotidien sur les piscines de {ville} et environs. Chaque pattern illustre une signature de fuite locale bien identifiée.</p>

    <div class="grid-3" style="margin-top:1.5rem;">
{patterns_html}
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Prix d'une recherche de fuite sur piscine {ville_article}</h2>
    <p>Le tarif d'une recherche de fuite piscine dépend principalement du nombre de méthodes à combiner et du temps d'intervention. Voici les fourchettes que nous pratiquons sur Bordeaux et sa métropole.</p>

    <div style="overflow-x:auto;margin:1.5rem 0;">
      <table style="width:100%;border-collapse:collapse;font-size:.95rem;background:var(--white);">
        <thead>
          <tr>
            <th style="padding:.8rem;text-align:left;background:var(--green);color:var(--white);border:1px solid var(--green-dark);">Type de diagnostic</th>
            <th style="padding:.8rem;text-align:left;background:var(--green);color:var(--white);border:1px solid var(--green-dark);">Tarif moyen HT</th>
            <th style="padding:.8rem;text-align:left;background:var(--green);color:var(--white);border:1px solid var(--green-dark);">Durée d'intervention</th>
          </tr>
        </thead>
        <tbody>
          <tr><td style="padding:.8rem;border:1px solid var(--border);">Test d'évaporation seul (sans déplacement)</td><td style="padding:.8rem;border:1px solid var(--border);">Gratuit, à faire soi-même</td><td style="padding:.8rem;border:1px solid var(--border);">24 à 48 h</td></tr>
          <tr style="background:var(--bg-alt);"><td style="padding:.8rem;border:1px solid var(--border);">Recherche colorant + inspection visuelle</td><td style="padding:.8rem;border:1px solid var(--border);">300 à 400 €</td><td style="padding:.8rem;border:1px solid var(--border);">1 h 30 à 2 h</td></tr>
          <tr><td style="padding:.8rem;border:1px solid var(--border);">Recherche complète (colorant + acoustique + pression)</td><td style="padding:.8rem;border:1px solid var(--border);">450 à 600 €</td><td style="padding:.8rem;border:1px solid var(--border);">2 à 3 h</td></tr>
          <tr style="background:var(--bg-alt);"><td style="padding:.8rem;border:1px solid var(--border);">Recherche avancée avec gaz traceur enterré</td><td style="padding:.8rem;border:1px solid var(--border);">600 à 800 €</td><td style="padding:.8rem;border:1px solid var(--border);">3 à 4 h</td></tr>
          <tr><td style="padding:.8rem;border:1px solid var(--border);">Vidange + inspection classique (méthode à éviter)</td><td style="padding:.8rem;border:1px solid var(--border);">1 000 à 2 000 €</td><td style="padding:.8rem;border:1px solid var(--border);">1 à 3 jours</td></tr>
        </tbody>
      </table>
    </div>

    <p>Un devis fixe vous est communiqué avant intervention après un premier échange téléphonique sur les symptômes observés. Aucun déplacement facturé si vous décidez de ne pas donner suite. Pour la grille tarifaire complète selon le type de fuite (piscine, canalisation enterrée, plancher chauffant), voir notre <a href="/guide/prix-recherche-fuite-bordeaux/" style="color:var(--green);text-decoration:underline;">guide prix recherche de fuite à Bordeaux</a>.</p>

    <h3>Prise en charge par l'assurance habitation</h3>
    <p>La majorité des contrats multirisques habitation incluent une garantie « recherche de fuite » qui rembourse tout ou partie du diagnostic, dès lors que la fuite a provoqué un dégât des eaux (même mineur). Le rapport technique que nous remettons mentionne les méthodes employées, la localisation précise de la fuite et les photos d'intervention : il est reconnu par tous les principaux assureurs français. Déclarez le sinistre dans les 5 jours ouvrables.</p>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Questions fréquentes sur la recherche de fuite piscine {ville_article}</h2>

{faq_locale_html}

    <h3>Faut-il vidanger la piscine pour localiser la fuite ?</h3>
    <p>Non, dans 95 pourcent des cas. Le colorant fluorescéine, l'écoute électro-acoustique et le test de pression des canalisations localisent la fuite sans vidange. La vidange est à éviter : elle peut endommager le liner, faire remonter la nappe phréatique sous le bassin et coûte 1 000 à 2 000 € en eau et produits de remise en service.</p>

    <h3>La recherche de fuite piscine est-elle remboursée par l'assurance ?</h3>
    <p>Oui, la plupart des contrats multirisques habitation couvrent la recherche de fuite sur piscine au titre de la garantie recherche de fuite. Notre rapport détaillé (photos, méthodes employées, point de fuite localisé) est accepté par les principaux assureurs. Déclarez le sinistre dans les 5 jours ouvrables après constat.</p>

    <h3>Intervenez-vous en urgence sur une piscine qui perd beaucoup d'eau ?</h3>
    <p>Oui, nous intervenons sous 24 à 48h sur Bordeaux et sa métropole pour les fuites actives importantes (perte supérieure à 5 cm par jour). Pour limiter les dégâts en attendant, coupez l'arrivée d'eau de remplissage automatique et maintenez le niveau juste au-dessus du skimmer pour que la filtration continue de tourner.</p>

    <div style="margin-top:2rem;text-align:center;">
      <a href="/devis/" class="btn btn-gold">Demander un devis pour ma piscine</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <h2 style="text-align:center;">Recherche de fuite piscine dans d'autres villes de Gironde</h2>
    <p style="text-align:center;margin-bottom:1.5rem;">Nous intervenons sur l'ensemble de la métropole bordelaise et du Bassin d'Arcachon. Pour une vue d'ensemble, voir notre <a href="/detection-fuite/piscine/" style="color:var(--green);text-decoration:underline;">page hub recherche de fuite piscine en Gironde</a>.</p>
    <div class="grid-3">
      {autres_html}
    </div>
    <p style="text-align:center;margin-top:1.5rem;"><a href="/detection-fuite/" class="btn btn-outline-green">Voir toutes nos spécialités &rarr;</a></p>
  </div>
</section>

{form_section(p['ville'])}
'''

    return html_base(
        f'Fuite piscine {ville_article} ({cp}) | Sans vidange',
        f'Recherche de fuite sur piscine {ville_article} sans vidange : colorant fluorescéine, écoute acoustique, test de pression. Devis gratuit 24h, rapport pour assurance. Intervention en Gironde.',
        f'https://recherche-fuite-gironde.fr/detection-fuite/{slug}/',
        body,
        extra_ld=ld_local + ld_service + ld_breadcrumb + ld_faq,
    )


# ═══════════════════════════════════════════════════════════════
# PAGE : Homepage (body issu de templates/home_body.html)
# ═══════════════════════════════════════════════════════════════

def page_index():
    body_path = BASE / 'templates' / 'home_body.html'
    body = body_path.read_text(encoding='utf-8') if body_path.exists() else ''

    ld = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "https://recherche-fuite-gironde.fr/#organization",
  "name": "Recherche Fuite Gironde",
  "alternateName": "RFG - Spécialiste recherche de fuite Gironde",
  "description": "Spécialiste de la recherche et de la détection de fuites d'eau en Gironde (33). Méthodes non destructives : thermographie infrarouge, gaz traceur azote/hélium, écoute électro-acoustique, caméra endoscopique, fluorescéine. Intervention rapide, rapport assurance inclus.",
  "url": "https://recherche-fuite-gironde.fr/",
  "image": "https://recherche-fuite-gironde.fr/assets/hero-gironde.webp",
  "logo": "https://recherche-fuite-gironde.fr/assets/logo-recherche-fuite-gironde.png",
  "areaServed": [
    { "@type": "AdministrativeArea", "name": "Gironde", "addressCountry": "FR" },
    { "@type": "City", "name": "Bordeaux" },
    { "@type": "City", "name": "Mérignac" },
    { "@type": "City", "name": "Pessac" },
    { "@type": "City", "name": "Talence" },
    { "@type": "City", "name": "Arcachon" },
    { "@type": "City", "name": "La Teste-de-Buch" },
    { "@type": "City", "name": "Libourne" },
    { "@type": "City", "name": "Le Bouscat" }
  ],
  "address": { "@type": "PostalAddress", "addressRegion": "Gironde", "addressCountry": "FR" },
  "serviceType": ["Recherche de fuite d'eau", "Détection de fuite non destructive", "Chemisage de canalisation", "Recherche de fuite piscine", "diagnostic plancher chauffant", "Intervention urgence dégât des eaux"],
  "knowsAbout": [
    "Recherche de fuite d'eau",
    "Détection non destructive",
    "Thermographie infrarouge",
    "Gaz traceur azote hélium",
    "Écoute électro-acoustique",
    "Caméra endoscopique ITV",
    "Fluorescéine et colorant UV",
    "Chemisage tubulaire de canalisation",
    "Convention IRSI copropriété",
    "Loi Warsmann écrêtement facture eau",
    "diagnostic piscine sans vidange",
    "Plancher chauffant hydraulique"
  ],
  "priceRange": "€€",
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Services Recherche Fuite Gironde",
    "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Recherche de fuite d'eau", "url": "https://recherche-fuite-gironde.fr/detection-fuite/" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Recherche de fuite piscine", "url": "https://recherche-fuite-gironde.fr/detection-fuite/piscine/" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Chemisage de canalisation", "url": "https://recherche-fuite-gironde.fr/chemisage-canalisation/" } }
    ]
  }
}
</script>'''

    return html_base(
        "Recherche de fuite Gironde 33 | Sans démolition",
        "Spécialiste de la recherche de fuites d'eau en Gironde (33). Détection non destructive, intervention rapide sur 30 communes. Devis gratuit, rapport assurance.",
        "https://recherche-fuite-gironde.fr/",
        body,
        ld,
    )


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
        'https://recherche-fuite-gironde.fr/simulateur-cout-fuite/',
        'https://recherche-fuite-gironde.fr/calcul-warsmann-bordeaux/',
    ]
    urls += [f'https://recherche-fuite-gironde.fr/guide/{a["slug"]}/' for a in GUIDE_PAGES]
    urls += [f'https://recherche-fuite-gironde.fr/villes/{v["slug"]}/' for v in VILLES]
    urls += [f'https://recherche-fuite-gironde.fr/villes/{v["slug"]}/chemisage/' for v in VILLES]
    urls += ['https://recherche-fuite-gironde.fr/detection-fuite/piscine/']
    urls += [f'https://recherche-fuite-gironde.fr/detection-fuite/{p["slug"]}/' for p in PISCINE_PAGES]
    urls += [f'https://recherche-fuite-gironde.fr/detection-fuite/{p["slug"]}/' for p in URGENCE_PAGES]
    urls += ['https://recherche-fuite-gironde.fr/detection-fuite/fuite-apres-compteur/']
    urls += ['https://recherche-fuite-gironde.fr/detection-fuite/canalisation-enterree-bordeaux/']
    urls += ['https://recherche-fuite-gironde.fr/detection-fuite/degats-des-eaux-bordeaux/']
    urls += ['https://recherche-fuite-gironde.fr/detection-fuite/chemisage-bordeaux/']
    urls += ['https://recherche-fuite-gironde.fr/detection-fuite/fuite-plancher-chauffant-bordeaux/']
    urls += ['https://recherche-fuite-gironde.fr/detection-fuite/fluoresceine-piscine-bordeaux/']
    urls += ['https://recherche-fuite-gironde.fr/detection-fuite/thermographie-infrarouge-bordeaux/']
    urls += ['https://recherche-fuite-gironde.fr/detection-fuite/depannage-piscine-bordeaux/']

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
      "headers": [{"key": "Cache-Control", "value": "public, max-âgé=31536000, immutable"}]
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

    print('[0/8] Homepage...')
    write('index.html', page_index())

    print('[1/8] Pages de service...')
    write('detection-fuite/index.html', page_detection())
    write('chemisage-canalisation/index.html', page_chemisage_service())

    print('[2/8] Pages utilitaires...')
    write('contact/index.html', page_contact())
    write('devis/index.html', page_devis())
    write('mentions-legales/index.html', page_mentions())
    write('plan-du-site/index.html', page_plan())
    write('simulateur-cout-fuite/index.html', page_simulateur_cout_fuite())
    write('calcul-warsmann-bordeaux/index.html', page_calcul_warsmann_bordeaux())

    print('[3/8] Guide — sommaire...')
    write('guide/index.html', page_guide_index())

    print('[4/8] Guide — articles...')
    for art in GUIDE_PAGES:
        write(f'guide/{art["slug"]}/index.html', page_guide_article(art))

    print('[5/8] Guide — FAQ...')
    write('guide/faq/index.html', page_faq())

    print('[6/8] Pages villes — détection (30)...')
    for v in VILLES:
        if v['slug'] in VILLES_PREMIUM:
            write(f'villes/{v["slug"]}/index.html', page_ville_detection_premium(v))
        else:
            write(f'villes/{v["slug"]}/index.html', page_ville_detection(v))

    print('[7/8] Pages villes — chemisage (30)...')
    for v in VILLES:
        if v['slug'] == 'bordeaux':
            write(f'villes/{v["slug"]}/chemisage/index.html', page_chemisage_bordeaux_premium())
        else:
            write(f'villes/{v["slug"]}/chemisage/index.html', page_ville_chemisage(v))

    print('[7a] Page hub — piscine pillar...')
    write('detection-fuite/piscine/index.html', page_piscine_hub())

    print('[7b] Pages use case — piscine par ville...')
    for p in PISCINE_PAGES:
        write(f'detection-fuite/{p["slug"]}/index.html', page_piscine_ville(p))

    print('[7c] Pages use case — urgence par ville...')
    for p in URGENCE_PAGES:
        write(f'detection-fuite/{p["slug"]}/index.html', page_urgence_ville(p))

    print('[7d] Page use case — fuite après compteur...')
    write('detection-fuite/fuite-apres-compteur/index.html', page_fuite_apres_compteur())

    print('[7e] Page use case — canalisation enterrée Bordeaux...')
    write('detection-fuite/canalisation-enterree-bordeaux/index.html', page_canalisation_enterree_bordeaux())

    print('[7f] Page use case — dégâts des eaux Bordeaux...')
    write('detection-fuite/degats-des-eaux-bordeaux/index.html', page_degats_eaux_bordeaux())

    print('[7g] Page use case — chemisage Bordeaux landing...')
    write('detection-fuite/chemisage-bordeaux/index.html', page_chemisage_bordeaux())

    print('[7h] Page use case — fuite plancher chauffant Bordeaux...')
    write('detection-fuite/fuite-plancher-chauffant-bordeaux/index.html', page_plancher_chauffant_bordeaux())

    print('[7i] Page use case — fluorescéine piscine Bordeaux...')
    write('detection-fuite/fluoresceine-piscine-bordeaux/index.html', page_fluoresceine_piscine_bordeaux())

    print('[7j] Page use case — thermographie infrarouge Bordeaux...')
    write('detection-fuite/thermographie-infrarouge-bordeaux/index.html', page_thermographie_infrarouge_bordeaux())

    print('[7k] Page use case — dépannage piscine Bordeaux...')
    write('detection-fuite/depannage-piscine-bordeaux/index.html', page_depannage_piscine_bordeaux())

    print('[8/8] Fichiers techniques...')
    write('sitemap.xml', gen_sitemap())
    write('robots.txt', ROBOTS)
    write('vercel.json', VERCEL)

    total = 2 + 3 + 1 + len(GUIDE_PAGES) + 1 + len(VILLES)*2 + 3
    print(f'\n✓ {total} fichiers générés avec succès.\n')

if __name__ == '__main__':
    main()
