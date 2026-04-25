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
            <a href="/detection-fuite/urgence-bordeaux/">Urgence fuite 24h Bordeaux</a>
            <a href="/detection-fuite/fuite-apres-compteur/">Fuite après compteur</a>
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
    <input type="hidden" name="_subject" value="[recherche-fuite-gironde.fr] Demande détection à {nom}">
    <input type="hidden" name="ville" value="{nom}">
    <input type="hidden" name="site_source" value="">
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
  <div id="form-mini-error" style="display:none;background:#fef2f2;border:1px solid #fca5a5;border-radius:8px;padding:.75rem;text-align:center;margin-bottom:.75rem;"><p style="color:#991b1b;font-size:.85rem;margin:0;">Erreur, veuillez r\u00e9essayer.</p></div>
  <form data-ajax data-error="form-mini-error" class="ville-cta-form">
    <input type="hidden" name="_subject" value="[recherche-fuite-gironde.fr] Demande chemisage à {nom}">
    <input type="hidden" name="ville" value="{nom}">
    <input type="hidden" name="service" value="Chemisage">
    <input type="hidden" name="site_source" value="">
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
        <p>Surconsommation inexpliquée, canalisation enterrée privative. Écrêtement de facture possible (loi Warsmann 2011).</p>
      </a>
    </div>

    <h3 style="font-family:var(--font-title,inherit);margin-top:3rem;margin-bottom:1rem;">Recherche de fuite piscine par ville</h3>
    <p style="margin-bottom:1.5rem;">Le thème piscine est notre première cause d'intervention en Gironde. Pages spécifiques pour les communes à forte densité de bassins privés.</p>
    <div class="grid-3">
      <a href="/detection-fuite/piscine-bordeaux/" class="loc-card" style="text-decoration:none;color:inherit;padding:1rem 1.25rem;background:var(--white);border:1px solid var(--c-border);border-radius:12px;display:block;"><strong>Piscine Bordeaux</strong><span style="display:block;font-size:.85rem;color:var(--c-text-muted);margin-top:.25rem;">33000 · Centre, Caudéran, Médoc</span></a>
      <a href="/detection-fuite/piscine-merignac/" class="loc-card" style="text-decoration:none;color:inherit;padding:1rem 1.25rem;background:var(--white);border:1px solid var(--c-border);border-radius:12px;display:block;"><strong>Piscine Mérignac</strong><span style="display:block;font-size:.85rem;color:var(--c-text-muted);margin-top:.25rem;">33700 · Arlac, Capeyron, Beutre</span></a>
      <a href="/detection-fuite/piscine-arcachon/" class="loc-card" style="text-decoration:none;color:inherit;padding:1rem 1.25rem;background:var(--white);border:1px solid var(--c-border);border-radius:12px;display:block;"><strong>Piscine Arcachon</strong><span style="display:block;font-size:.85rem;color:var(--c-text-muted);margin-top:.25rem;">33120 · Ville d'Hiver, Bassin</span></a>
      <a href="/detection-fuite/piscine-la-teste-de-buch/" class="loc-card" style="text-decoration:none;color:inherit;padding:1rem 1.25rem;background:var(--white);border:1px solid var(--c-border);border-radius:12px;display:block;"><strong>Piscine La Teste-de-Buch</strong><span style="display:block;font-size:.85rem;color:var(--c-text-muted);margin-top:.25rem;">33260 · Cazaux, Pyla</span></a>
      <a href="/detection-fuite/piscine-gujan-mestras/" class="loc-card" style="text-decoration:none;color:inherit;padding:1rem 1.25rem;background:var(--white);border:1px solid var(--c-border);border-radius:12px;display:block;"><strong>Piscine Gujan-Mestras</strong><span style="display:block;font-size:.85rem;color:var(--c-text-muted);margin-top:.25rem;">33470 · Bassin d'Arcachon</span></a>
      <a href="/detection-fuite/piscine-libourne/" class="loc-card" style="text-decoration:none;color:inherit;padding:1rem 1.25rem;background:var(--white);border:1px solid var(--c-border);border-radius:12px;display:block;"><strong>Piscine Libourne</strong><span style="display:block;font-size:.85rem;color:var(--c-text-muted);margin-top:.25rem;">33500 · Libournais, St-Émilion</span></a>
      <a href="/detection-fuite/piscine-le-bouscat/" class="loc-card" style="text-decoration:none;color:inherit;padding:1rem 1.25rem;background:var(--white);border:1px solid var(--c-border);border-radius:12px;display:block;"><strong>Piscine Le Bouscat</strong><span style="display:block;font-size:.85rem;color:var(--c-text-muted);margin-top:.25rem;">33110 · Parc Bordelais, Bourran</span></a>
    </div>

    <h3 style="font-family:var(--font-title,inherit);margin-top:3rem;margin-bottom:1rem;">Pages détection par ville (contenu enrichi)</h3>
    <p style="margin-bottom:1.5rem;">Pages villes avec contenu local détaillé (quartiers, patrimoine, spécificités géologiques) pour les 5 villes stratégiques de Gironde.</p>
    <div class="grid-3">
      <a href="/villes/bordeaux/" class="loc-card" style="text-decoration:none;color:inherit;padding:1rem 1.25rem;background:var(--white);border:1px solid var(--c-border);border-radius:12px;display:block;"><strong>Bordeaux (33000)</strong><span style="display:block;font-size:.85rem;color:var(--c-text-muted);margin-top:.25rem;">Haussmanniens, UNESCO, pierre calcaire</span></a>
      <a href="/villes/merignac/" class="loc-card" style="text-decoration:none;color:inherit;padding:1rem 1.25rem;background:var(--white);border:1px solid var(--c-border);border-radius:12px;display:block;"><strong>Mérignac (33700)</strong><span style="display:block;font-size:.85rem;color:var(--c-text-muted);margin-top:.25rem;">Pavillons, planchers chauffants</span></a>
      <a href="/villes/arcachon/" class="loc-card" style="text-decoration:none;color:inherit;padding:1rem 1.25rem;background:var(--white);border:1px solid var(--c-border);border-radius:12px;display:block;"><strong>Arcachon (33120)</strong><span style="display:block;font-size:.85rem;color:var(--c-text-muted);margin-top:.25rem;">Villas Ville d'Hiver, air salin</span></a>
      <a href="/villes/libourne/" class="loc-card" style="text-decoration:none;color:inherit;padding:1rem 1.25rem;background:var(--white);border:1px solid var(--c-border);border-radius:12px;display:block;"><strong>Libourne (33500)</strong><span style="display:block;font-size:.85rem;color:var(--c-text-muted);margin-top:.25rem;">Chais viticoles, sol argileux</span></a>
      <a href="/villes/pessac/" class="loc-card" style="text-decoration:none;color:inherit;padding:1rem 1.25rem;background:var(--white);border:1px solid var(--c-border);border-radius:12px;display:block;"><strong>Pessac (33600)</strong><span style="display:block;font-size:.85rem;color:var(--c-text-muted);margin-top:.25rem;">Cité Frugès UNESCO, copropriétés</span></a>
      <a href="/plan-du-site/" class="loc-card" style="text-decoration:none;color:inherit;padding:1rem 1.25rem;background:var(--c-bg);border:1px solid var(--c-border);border-radius:12px;display:block;"><strong>+25 autres villes</strong><span style="display:block;font-size:.85rem;color:var(--c-text-muted);margin-top:.25rem;">Toute la Gironde au plan du site &rarr;</span></a>
    </div>

    <div style="text-align:center;margin-top:2rem;">
      <a href="/guide/prix-recherche-fuite-bordeaux/" class="btn btn-outline-green">Voir les prix 2026</a>
      <a href="/devis/" class="btn btn-gold" style="margin-left:1rem;">Demander un devis gratuit</a>
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

      <h2>Pages spécialisées par cas d'usage</h2>
      <p>Pages dédiées aux situations spécifiques que nous traitons quotidiennement, avec contenu approfondi et tarifs détaillés.</p>
      <ul>
        <li><a href="/detection-fuite/urgence-bordeaux/">Recherche de fuite en urgence à Bordeaux (intervention 24h)</a></li>
        <li><a href="/detection-fuite/fuite-apres-compteur/">Fuite d'eau après compteur à Bordeaux (loi Warsmann)</a></li>
        <li><a href="/detection-fuite/canalisation-enterree-bordeaux/">Recherche de fuite canalisation enterrée à Bordeaux (gaz traceur)</a></li>
        <li><a href="/detection-fuite/degats-des-eaux-bordeaux/">Dégât des eaux à Bordeaux (syndics et copropriétés IRSI)</a></li>
        <li><a href="/detection-fuite/chemisage-bordeaux/">Chemisage de canalisation à Bordeaux (immeubles haussmanniens)</a></li>
        <li><a href="/detection-fuite/fuite-plancher-chauffant-bordeaux/">Fuite sur plancher chauffant à Bordeaux (thermographie)</a></li>
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
        <li><a href="/guide/prix-recherche-fuite-bordeaux/">Prix d'une recherche de fuite à Bordeaux en 2026</a></li>
        <li><a href="/guide/recherche-fuite-piscine-tarif/">Tarif recherche de fuite piscine en Gironde par type de bassin</a></li>
        <li><a href="/guide/recherche-fuite-piscine-assurance/">Recherche de fuite piscine et assurance habitation : remboursement</a></li>
        <li><a href="/guide/ma-piscine-perd-de-l-eau-que-faire/">Ma piscine perd de l'eau : guide de diagnostic étape par étape</a></li>
        <li><a href="/guide/fuite-liner-piscine/">Fuite sur liner de piscine : signes, causes et diagnostic</a></li>
        <li><a href="/guide/evaporation-vs-fuite-piscine/">Évaporation ou fuite de piscine : taux mensuels Gironde</a></li>
        <li><a href="/guide/loi-warsmann-ecretement-facture-eau/">Loi Warsmann : écrêtement de facture d'eau après fuite</a></li>
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
</ul>
<h2>Cas particulier : fuite sur canalisation enterrée après compteur</h2>
<p>Si votre fuite se situe entre votre compteur d'eau et votre habitation (zone privative), vous pouvez souvent bénéficier d'un écrêtement de facture auprès de Suez ou de votre régie des eaux (loi Warsmann 2011). Notre page dédiée <a href="/detection-fuite/fuite-apres-compteur/" style="color:var(--green);text-decoration:underline;">fuite d'eau après compteur à Bordeaux</a> détaille la procédure, les justificatifs à fournir et les conditions à remplir pour obtenir ce plafonnement de facturation.</p>"""
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
<p>Nous vous proposons un devis gratuit avant toute intervention. Après un premier échange sur votre situation (type de fuite, configuration du logement, localisation en Gironde), nous pouvons vous donner une estimation précise et sans surprise. Utilisez le formulaire de contact pour nous décrire votre situation.</p>
<p>Pour un détail complet des tarifs 2026 par méthode avec un tableau comparatif, consultez notre guide <a href="/guide/prix-recherche-fuite-bordeaux/" style="color:var(--green);text-decoration:underline;">prix d'une recherche de fuite à Bordeaux</a>, qui couvre également la prise en charge par l'assurance et l'écrêtement de facture d'eau selon la loi Warsmann.</p>"""
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
<p>C'est le document central de votre dossier. Il doit mentionner : la localisation précise de la fuite, la technique utilisée, les photos de l'intervention et les préconisations de réparation. Nous fournissons systématiquement ce rapport à l'issue de chaque intervention en Gironde.</p>
<h2>Cas de la fuite après compteur : la loi Warsmann</h2>
<p>Si la fuite se situe sur votre réseau privatif enterré (entre compteur et habitation), vous pouvez cumuler la prise en charge assurance ET un écrêtement de facture d'eau auprès de votre distributeur. La loi Warsmann de 2011 plafonne la surfacturation due à une fuite enterrée indétectable. Consultez notre guide <a href="/detection-fuite/fuite-apres-compteur/" style="color:var(--green);text-decoration:underline;">fuite d'eau après compteur à Bordeaux</a> pour la procédure complète.</p>"""
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
<p>Une fois l'urgence gérée, il est indispensable de faire localiser la fuite par un professionnel avant toute remise en eau. En Gironde, nous intervenons sous 24h pour une <a href="/detection-fuite/" style="color:var(--green);text-decoration:underline;">recherche de fuite non destructive</a> avec remise du rapport assurance.</p>
<p>Pour les fuites actives importantes sur Bordeaux et sa métropole, consultez notre page dédiée à la <a href="/detection-fuite/urgence-bordeaux/" style="color:var(--green);text-decoration:underline;">recherche de fuite en urgence à Bordeaux</a> : intervention sous 24h, qualification téléphonique dans l'heure, rapport remis le jour même. Si votre surconsommation d'eau est inexpliquée, la fuite se situe peut-être sur le réseau privatif : voir notre guide <a href="/detection-fuite/fuite-apres-compteur/" style="color:var(--green);text-decoration:underline;">fuite après compteur à Bordeaux</a> (écrêtement de facture possible selon loi Warsmann).</p>"""
    },
    {
        "slug": "recherche-fuite-piscine-tarif",
        "title": "Tarif recherche de fuite piscine en Gironde : prix par type de bassin",
        "title_seo": "Tarif recherche fuite piscine Gironde prix type bassin 2026",
        "desc": "Tarif d'une recherche de fuite piscine en Gironde selon le type de bassin (liner, coque, beton), la methode employee et la taille. Grille detaillee 2026.",
        "contenu": """<p>Combien coute reellement une recherche de fuite sur une piscine en Gironde ? La reponse depend fortement du type de bassin que vous avez. Un liner PVC, une coque polyester et un bassin beton armé ne se diagnostiquent pas avec les memes methodes ni le meme temps d'intervention. Cet article detaille la grille tarifaire 2026 par type de bassin, avec les methodes associees et les cas complexes qui peuvent faire varier le prix final.</p>

<h2>Pourquoi le type de bassin determine le tarif ?</h2>
<p>Contrairement aux recherches de fuite sur canalisation d'eau classique (ou la methode principale - gaz traceur ou acoustique - s'applique partout de maniere similaire), le diagnostic d'une fuite de piscine varie fortement selon la structure du bassin. Une coque polyester demande une inspection camera specifique aux defauts structurels (osmose, delaminage). Un liner PVC impose colorant fluoresceine et inspection visuelle des soudures. Un bassin beton arme necessite potentiellement un diagnostic structurel pour distinguer une fissure active d'une fissure stabilisee. Ce parametre technique fait varier notre devis de 30 a 50 pourcent selon les cas.</p>

<h2>Tarif par type de bassin (2026)</h2>

<h3>Piscine liner PVC - tarif 300 a 500 € HT</h3>
<p>Les piscines avec liner PVC 75/100 ou 85/100, dominant le parc girondin des annees 1990-2010, representent notre diagnostic le plus rapide. Methodologie : inspection visuelle du liner en apnee ou camera, colorant fluoresceine sur pieces a sceller (skimmer, buses de refoulement, bonde de fond), test de pression hydraulique sur canalisations. Duree d'intervention : 1h30 a 2h. Tarif moyen : 300 a 500 € HT selon la taille du bassin (4x8m jusqu'a 5x10m couverts dans cette fourchette). Au-dela (piscines familiales de plus de 10m), supplement de 50 a 100 €.</p>

<h3>Piscine coque polyester - tarif 400 a 600 € HT</h3>
<p>Les coques polyester monoblocs installees entre 2000 et 2020 demandent une inspection camera sous-marine plus minutieuse pour detecter les signes d'osmose (cloques sur le gel-coat), les microfissures au niveau des pieces moulees (bondes de fond, marches romaines, escaliers integres) et les delaminages inter-couches de fibre. La fluoresceine confirme les defauts visuels suspectes. Tarif moyen : 400 a 600 € HT, incluant le rapport photo detaille indispensable pour faire jouer la garantie decennale de pose si le bassin a moins de 10 ans.</p>

<h3>Piscine beton arme - tarif 450 a 700 € HT</h3>
<p>Les bassins beton armé, frequents dans les grandes proprietes (villas Arcachon, chais viticoles Libournais, proprietes Caudéran) ou construits sur mesure, necessitent notre diagnostic le plus approfondi. Inspection camera complete, test colorant, ecoute electro-acoustique sur canalisations enterrees, et parfois inspection structurelle si des fissures sont detectees. Tarif moyen : 450 a 700 € HT. Les piscines de plus de 50 m³ (12×5 ou 15×4) ou avec configuration complexe (miroir, debordement periphérique, volet immergé) peuvent monter a 800 € HT.</p>

<h3>Piscine naturelle / bio-phytoepuration - tarif 500 a 800 € HT</h3>
<p>Les piscines naturelles a lagunage vegetal, en croissance en Gironde (Gujan-Mestras, La Teste, quelques installations a Merignac), demandent une approche specifique. Isolation sequentielle des differents compartiments (bassin de baignade, bassin de filtration vegetale, canalisations de transfert), mesure differentielle sur 48h pour identifier la zone fuyante, puis diagnostic fin. Tarif moyen : 500 a 800 € HT, plus eleve en raison du temps d'intervention double sur deux passages.</p>

<h2>Tarif par methode (si diagnostic cible)</h2>
<p>Pour un probleme deja identifie ou suspecte sur un circuit precis, une intervention ciblee sur une seule methode est possible a tarif reduit.</p>

<table style="width:100%;border-collapse:collapse;margin:1.5rem 0;background:#fff;">
<thead><tr style="background:#0D3B2E;color:#fff;"><th style="padding:.75rem;text-align:left;border:1px solid #155740;">Methode isolee</th><th style="padding:.75rem;text-align:left;border:1px solid #155740;">Tarif HT</th><th style="padding:.75rem;text-align:left;border:1px solid #155740;">Cas d'usage</th></tr></thead>
<tbody>
<tr><td style="padding:.75rem;border:1px solid #D8D4CC;">Colorant fluoresceine + visuelle</td><td style="padding:.75rem;border:1px solid #D8D4CC;">250 a 350 €</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Fuite suspectee sur pieces a sceller connues</td></tr>
<tr style="background:#F7F6F2;"><td style="padding:.75rem;border:1px solid #D8D4CC;">Test de pression canalisations</td><td style="padding:.75rem;border:1px solid #D8D4CC;">300 a 400 €</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Chute de pression filtration inexpliquee</td></tr>
<tr><td style="padding:.75rem;border:1px solid #D8D4CC;">Inspection camera sous-marine</td><td style="padding:.75rem;border:1px solid #D8D4CC;">280 a 380 €</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Suspicion de fissure coque ou liner</td></tr>
<tr style="background:#F7F6F2;"><td style="padding:.75rem;border:1px solid #D8D4CC;">Gaz traceur canalisation enterree</td><td style="padding:.75rem;border:1px solid #D8D4CC;">400 a 550 €</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Fuite hors bassin, reseau enterré jardin</td></tr>
<tr><td style="padding:.75rem;border:1px solid #D8D4CC;">Inspection complete + rapport</td><td style="padding:.75rem;border:1px solid #D8D4CC;">450 a 800 €</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Aucune piste, diagnostic exhaustif</td></tr>
</tbody>
</table>

<h2>Supplements possibles</h2>
<ul>
<li><strong>Intervention urgence (24h)</strong> : aucun supplement chez nous, notre planning integre des creneaux prioritaires</li>
<li><strong>Piscine couverte par volet immerge ou abri</strong> : supplement de 50 € pour manipulation securisee</li>
<li><strong>Piscine tres profonde (4m+)</strong> : supplement plongeur professionnel de 300 a 500 € si plongee humaine necessaire</li>
<li><strong>Deplacement hors metropole bordelaise</strong> : forfait 40 € pour Bassin d'Arcachon, Medoc, Libournais</li>
<li><strong>Hivernage en cours</strong> : pas de supplement mais creneau limite (novembre a mars, intervention possible si bassin accessible)</li>
</ul>

<h2>Comparatif : diagnostic moderne vs vidange classique</h2>
<p>Certaines entreprises proposent encore de vider la piscine pour inspecter visuellement le bassin. Cette methode, tres consommatrice en eau et en temps, coute en realite plus cher que notre diagnostic non destructif.</p>

<table style="width:100%;border-collapse:collapse;margin:1.5rem 0;background:#fff;">
<thead><tr style="background:#0D3B2E;color:#fff;"><th style="padding:.75rem;text-align:left;border:1px solid #155740;">Poste</th><th style="padding:.75rem;text-align:left;border:1px solid #155740;">Diagnostic moderne</th><th style="padding:.75rem;text-align:left;border:1px solid #155740;">Vidange classique</th></tr></thead>
<tbody>
<tr><td style="padding:.75rem;border:1px solid #D8D4CC;">Tarif recherche</td><td style="padding:.75rem;border:1px solid #D8D4CC;">300 a 700 €</td><td style="padding:.75rem;border:1px solid #D8D4CC;">500 a 1000 €</td></tr>
<tr style="background:#F7F6F2;"><td style="padding:.75rem;border:1px solid #D8D4CC;">Cout vidange + remise en eau</td><td style="padding:.75rem;border:1px solid #D8D4CC;">0 € (pas de vidange)</td><td style="padding:.75rem;border:1px solid #D8D4CC;">500 a 1500 € (eau + chimie)</td></tr>
<tr><td style="padding:.75rem;border:1px solid #D8D4CC;">Risque structurel sur bassin vide</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Nul</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Eleve en zone nappe phreatique</td></tr>
<tr style="background:#F7F6F2;"><td style="padding:.75rem;border:1px solid #D8D4CC;">Duree totale</td><td style="padding:.75rem;border:1px solid #D8D4CC;">2 a 4 h</td><td style="padding:.75rem;border:1px solid #D8D4CC;">2 a 5 jours</td></tr>
<tr><td style="padding:.75rem;border:1px solid #D8D4CC;">Cout total moyen</td><td style="padding:.75rem;border:1px solid #D8D4CC;"><strong>500 € HT</strong></td><td style="padding:.75rem;border:1px solid #D8D4CC;"><strong>1 500 a 2 500 € HT</strong></td></tr>
</tbody>
</table>

<h2>Prise en charge par l'assurance habitation</h2>
<p>La garantie « recherche de fuite » de votre contrat multirisque habitation rembourse tout ou partie du diagnostic piscine des lors qu'un degat des eaux est constate (degradation du jardin, infiltration dans le local technique, impact sur fondations). Notre rapport technique est accepte par les principaux assureurs francais. Pour le detail de la procedure, consultez notre guide <a href="/guide/recherche-fuite-piscine-assurance/" style="color:var(--green);text-decoration:underline;">recherche de fuite piscine et assurance habitation</a>.</p>

<h2>Interventions groupees (copropriete, residence)</h2>
<p>Pour les copropriétés avec piscine collective (Bassin d'Arcachon, residences touristiques) ou les gestionnaires multi-sites, nous proposons des forfaits d'intervention groupée : diagnostic de plusieurs piscines en une seule visite avec remise minoree. Contactez-nous pour une estimation specifique.</p>

<h2>Notre engagement tarifaire</h2>
<ul>
<li>Devis fixe communique avant intervention, sans surprise</li>
<li>Aucun deplacement facture si vous ne donnez pas suite au devis</li>
<li>Rapport technique detaille inclus dans le tarif annonce</li>
<li>Paiement apres intervention sur facture, aucun acompte demande</li>
</ul>

<p>Obtenez un devis personnalise en decrivant votre situation via notre <a href="/devis/" style="color:var(--green);text-decoration:underline;">formulaire de demande de devis</a>, ou consultez directement notre page <a href="/detection-fuite/piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">recherche de fuite piscine a Bordeaux</a> ou la <a href="/detection-fuite/piscine-arcachon/" style="color:var(--green);text-decoration:underline;">page piscine Arcachon</a> si vous etes sur le Bassin.</p>"""
    },
    {
        "slug": "recherche-fuite-piscine-assurance",
        "title": "Recherche fuite piscine et assurance habitation : le remboursement",
        "title_seo": "Recherche fuite piscine assurance habitation remboursement IRSI",
        "desc": "Comment faire rembourser une recherche de fuite sur piscine par votre assurance habitation en Gironde. Clauses, procedure, IRSI copropriete, cas complexes.",
        "contenu": """<p>La recherche de fuite sur une piscine privee represente un investissement de 300 a 800 euros HT selon les cas. La bonne nouvelle : votre assurance habitation multirisque couvre souvent tout ou partie de cette prestation, sous reserve de connaitre les clauses applicables et de respecter la procedure de declaration. Cet article detaille les modalites propres aux piscines, qui different sensiblement de celles d'un simple degat des eaux en logement.</p>

<h2>Votre piscine est-elle couverte par votre assurance habitation ?</h2>
<p>La majorite des contrats multirisques habitation en France incluent automatiquement la piscine privee dans les biens couverts, avec deux conditions souvent oubliees : declaration initiale au moment de la souscription (ou modification en cours de contrat) et conformite aux normes de securite (alarme, couverture, barriere, abri). Si vous avez installe votre piscine apres la souscription du contrat sans le signaler a votre assureur, la couverture peut etre refusee.</p>

<p>Pour verifier votre couverture piscine, consultez les conditions generales (section « biens exterieurs couverts » ou « annexes du logement ») et les conditions particulieres (montant assure specifique piscine, franchise applicable). En cas de doute, demandez par ecrit a votre assureur une confirmation de votre couverture piscine.</p>

<h2>Ce qui est couvert par votre assurance</h2>
<ul>
<li><strong>Recherche de fuite elle-meme</strong> : diagnostic non destructif par un professionnel, rapport technique</li>
<li><strong>Consommation d'eau perdue</strong> : ecrêtement auprès du distributeur (Suez, Regie des eaux) selon loi Warsmann si canalisation enterrée indetectable</li>
<li><strong>Degats collatéraux</strong> : pelouse abîmee, fondations de la maison affectees, local technique inondé, mobilier exterieur endommagé</li>
<li><strong>Reparation de la fuite</strong> : souvent couverte si la cause est accidentelle (pas due a usure normale ou defaut d'entretien)</li>
<li><strong>Remise en eau du bassin</strong> : pris en charge si une vidange a ete necessaire</li>
</ul>

<h2>Ce qui n'est PAS couvert</h2>
<ul>
<li><strong>Usure normale</strong> : un liner de 25 ans qui fuit par fatigue n'est generalement pas indemnise (releve de l'entretien)</li>
<li><strong>Defaut d'entretien caracterise</strong> : piscine abandonnee plusieurs saisons, hivernage mal realise</li>
<li><strong>Defauts de construction</strong> : pour une piscine neuve (moins de 10 ans), c'est la garantie decennale du constructeur qui s'applique, pas l'assurance habitation</li>
<li><strong>Equipements haut de gamme non declares</strong> : PAC, volet automatique, abri, local technique equipe - a lister specifiquement dans le contrat</li>
</ul>

<h2>Procedure de declaration pour une fuite piscine</h2>

<h3>Etape 1 : Constat et preuves</h3>
<p>Des que vous constatez une perte d'eau anormale (plus de 1 cm par jour, au-dela de l'evaporation naturelle en Gironde), faites le test du seau pour confirmer la fuite. Photographiez le niveau du bassin, les zones humides autour (pelouse, terrasse), les indices de ruissellement. Relevez votre compteur d'eau pour documenter la surconsommation.</p>

<h3>Etape 2 : Declaration sous 5 jours ouvrables</h3>
<p>Votre contrat impose une declaration sous 5 jours ouvrables a compter de la decouverte. Cette declaration peut se faire par courrier recommande, formulaire en ligne sur l'espace client, ou telephone (demandez une confirmation ecrite). Joignez les photos, la date de decouverte, la description des symptomes et si possible une estimation des degats.</p>

<h3>Etape 3 : Mandatement du professionnel</h3>
<p>Votre assureur peut mandater son propre expert, ou vous laisser choisir un prestataire independant. Dans les deux cas, c'est le rapport technique qui justifiera la prise en charge. Nous sommes reconnus par la majorite des assureurs francais (AXA, Allianz, MAAF, Groupama, Matmut, MACIF, MMA, GMF). Contactez-nous directement en mentionnant que votre assurance doit intervenir : nous adaptons le rapport aux exigences du dossier.</p>

<h3>Etape 4 : Remise du rapport et devis de reparation</h3>
<p>Notre rapport technique comprend : photos de la piscine et du point de fuite, methodes employees pour le diagnostic, localisation precise avec schema, estimation du debit de fuite, preconisations de reparation chiffrees. Transmettez ce rapport a votre assureur avec les devis de reparation (liner, coque, canalisations selon la cause).</p>

<h3>Etape 5 : Expertise contradictoire si necessaire</h3>
<p>Pour les sinistres importants (plus de 5 000 € de degats), l'assureur peut diligenter une expertise contradictoire. Vous pouvez etre assiste d'un expert d'assure pour defendre vos interets, notamment si votre assureur conteste la cause ou le montant.</p>

<h2>Convention IRSI en copropriete avec piscine collective</h2>
<p>Les residences bordelaises avec piscine collective (Bassins a Flot, residences des annees 1990-2010, residences touristiques du Bassin d'Arcachon) sont regies par la convention IRSI pour les degats des eaux jusqu'a 5 000 euros HT. Le syndic mandate le prestataire, l'assureur de la copropriete prend en charge le rapport et les dommages, puis se retourne contre l'assureur responsable si un lot individuel est a l'origine du sinistre (tres rare pour une piscine collective).</p>

<p>Notre rapport est specifiquement formate pour les sinistres IRSI : identification precise des responsabilites, chiffrage des dommages par zone (bassin, plage, jardin, lots adjacents), preconisations techniques detaillees.</p>

<h2>Cas complexes specifiques aux piscines</h2>

<h3>Piscine en location saisonniere</h3>
<p>Si vous louez votre residence avec piscine en meublé de tourisme, votre contrat multirisque habitation classique n'est pas suffisant : il vous faut une extension « location meublee » ou un contrat specifique « residence secondaire louee ». Sans cette extension, l'assureur peut refuser la prise en charge d'une fuite survenue pendant une location.</p>

<h3>Residence secondaire (Arcachon, Le Pyla)</h3>
<p>Les fuites decouvertes au retour apres plusieurs mois d'inoccupation posent une question juridique : l'assureur peut arguer que le defaut de surveillance est fautif. Contre-argument : une fuite sur canalisation enterrée etait indetectable visuellement (loi Warsmann). Notre rapport documente explicitement ce point pour faciliter la prise en charge.</p>

<h3>Piscine partagee entre plusieurs lots (copropriete horizontale)</h3>
<p>Quelques copropriétés horizontales dans la metropole (Pessac, Merignac) ont des piscines partagees entre 2 a 10 maisons. Le statut juridique de la piscine est defini dans le reglement de copropriete. Notre rapport identifie la zone de responsabilite pour le reglement entre assureurs des lots concernes.</p>

<h3>Piscine municipale ou publique</h3>
<p>Nous n'intervenons pas sur les piscines municipales (Stade Nautique, Piscine Galin, etc.) qui relevent de marches publics specifiques. Notre scope est exclusivement la piscine privative.</p>

<h2>Courrier type de declaration a l'assureur</h2>
<p>Voici un modele de courrier que vous pouvez adapter :</p>

<blockquote style="background:var(--c-bg);border-left:4px solid var(--c-primary);padding:1rem;margin:1rem 0;font-family:Georgia,serif;">
<p>Madame, Monsieur,</p>
<p>Je vous informe par la presente de la decouverte d'une fuite sur ma piscine privative situee a [adresse], que je constate depuis le [date].</p>
<p>Les signes suivants m'amenent a vous le signaler : [perte d'eau de X cm par jour, consommation d'eau anormale, zones humides dans le jardin, etc.].</p>
<p>Conformement aux dispositions de mon contrat multirisque habitation n° [numero], je vous declare ce sinistre dans le delai contractuel de 5 jours ouvrables. Je vous joins les premiers elements photographiques et numero de police.</p>
<p>Je sollicite la prise en charge au titre de la garantie « recherche de fuite » des frais de diagnostic, ainsi que des degats collateraux eventuels. Un rapport technique par un professionnel qualifie sera etabli et vous sera transmis sous huitaine.</p>
<p>Je vous prie d'agreer, Madame, Monsieur, l'expression de mes salutations distinguees.</p>
</blockquote>

<h2>Combien serez-vous rembourse en pratique ?</h2>
<p>Dans la majorite des dossiers que nous traitons, le remboursement couvre :</p>
<ul>
<li>100 pourcent de la recherche de fuite si un degat des eaux effectif est constate</li>
<li>50 a 100 pourcent des travaux de reparation selon la cause (accidentelle vs usure)</li>
<li>Totalite des degats collateraux (jardin abîmé, mobilier exterieur)</li>
<li>Consommation d'eau perdue via ecretement de facture (loi Warsmann) si fuite enterrée</li>
</ul>
<p>La franchise contractuelle s'applique (souvent 150 a 300 euros sur les degats des eaux). Dans certains cas, si la fuite n'a pas provoque de degat des eaux effectif (ex : fuite localisee rapidement sans impact sur les biens), la garantie « recherche de fuite » peut ne pas etre activee. Un bon rapport technique, qui documente l'impact potentiel si la fuite n'avait pas ete traitee, aide a justifier la prise en charge.</p>

<h2>Besoin d'un diagnostic compatible avec votre assurance ?</h2>
<p>Nous intervenons sur toute la Gironde avec un rapport technique standardise, accepte par les principaux assureurs. Pour obtenir un devis prealable ou coordonner une intervention avec votre assureur, consultez notre page de <a href="/devis/" style="color:var(--green);text-decoration:underline;">demande de devis</a> ou directement l'une de nos <a href="/detection-fuite/piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">pages piscine par ville</a> pour plus de details sur nos methodes d'intervention par zone geographique. Pour les aspects tarifaires, consultez notre guide dedie <a href="/guide/recherche-fuite-piscine-tarif/" style="color:var(--green);text-decoration:underline;">tarif recherche de fuite piscine</a>.</p>"""
    },
    {
        "slug": "ma-piscine-perd-de-l-eau-que-faire",
        "title": "Ma piscine perd de l'eau : que faire ? Guide de diagnostic",
        "title_seo": "Ma piscine perd de l eau que faire diagnostic etapes Gironde",
        "desc": "Votre piscine perd de l'eau et vous ne savez pas par ou commencer ? Arbre de decision etape par etape pour diagnostiquer et agir, avant d'appeler un professionnel en Gironde.",
        "contenu": """<p>Vous constatez une baisse anormale du niveau de votre piscine. Avant de paniquer ou d'appeler un professionnel, quelques verifications simples permettent de qualifier precisement la situation. Cet article est un guide de decision etape par etape : a chaque question, vous saurez ce qu'il faut faire et quand passer a l'etape suivante. L'objectif : arriver chez un pro de la recherche de fuite avec un diagnostic preliminaire solide, ce qui fait gagner du temps et souvent des euros.</p>

<h2>Etape 1 : Combien perdez-vous reellement par jour ?</h2>
<p>La premiere question a se poser est quantitative. La perception "ma piscine baisse rapidement" est tres subjective : une piscine de 8×4 metres avec 1 cm de baisse par jour perd environ 320 litres par jour. A l'echelle d'un ete (3 mois), cela represente 29 m³ d'eau. Est-ce anormal ? Cela depend de beaucoup de facteurs.</p>

<h3>Comment mesurer precisement</h3>
<ol>
<li>Avec un metre ou un niveau laser, marquez au feutre effacable le niveau d'eau sur la paroi (liner) ou sur un carrelage (bassin beton). Choisissez un point facile a retrouver (angle d'escalier, marque de structure).</li>
<li>Attendez exactement 24 heures, sans baignade, sans remplissage automatique en cours, et sans changement meteo majeur (pluie, canicule).</li>
<li>Marquez le nouveau niveau et mesurez la difference en millimetres.</li>
</ol>

<h3>Reperes pour interpretation</h3>
<ul>
<li><strong>0 a 3 mm/jour</strong> : normal en avril-mai, septembre-octobre en Gironde. Pas de fuite a suspecter.</li>
<li><strong>3 a 6 mm/jour</strong> : plage normale en plein ete juillet-aout, surtout en periode de vent et soleil intense.</li>
<li><strong>6 a 10 mm/jour</strong> : suspect en toute saison. Anormal en intersaison. A investiguer.</li>
<li><strong>Plus de 10 mm/jour (1 cm)</strong> : fuite quasi-certaine, sauf tres forte chaleur combinee au vent.</li>
<li><strong>Plus de 3 cm/jour</strong> : fuite active importante, agir sous 48h pour eviter degats collateraux (affouillement, surconsommation importante).</li>
</ul>

<p>Si vos mesures tombent dans les plages normales (0-6 mm/jour selon saison), il n'y a probablement pas de fuite. Continuez vos baignades normales et refaites une mesure dans 2-3 semaines si vous restez inquiet. Si vous etes au-dessus, passez a l'etape 2.</p>

<h2>Etape 2 : Faites le test du seau (fuite ou evaporation)</h2>
<p>Le test du seau est universel, gratuit et incontournable. Il isole le facteur evaporation pour savoir si votre piscine perd plus que ce qu'une simple evaporation expliquerait.</p>

<h3>Protocole precis</h3>
<ol>
<li>Prenez un seau de type "seau de chantier" (10 a 15 litres), rempli d'eau a hauteur similaire a votre piscine (2/3 environ).</li>
<li>Posez-le sur la premiere marche de votre piscine, immerge a sa base mais avec sa paroi interieure au-dessus du niveau d'eau. Le seau est maintenu a la meme temperature que la piscine.</li>
<li>Marquez au feutre : le niveau d'eau a l'interieur du seau, ET le niveau de la piscine sur sa paroi (liner ou margelle).</li>
<li>Laissez 24 a 48 heures : pas de baignade, pas de remplissage automatique (coupez la regulation de niveau), pas de pluie attendue.</li>
<li>Comparez les deux niveaux.</li>
</ol>

<h3>Interpretation des resultats</h3>
<ul>
<li><strong>Le seau et la piscine ont baisse de la meme hauteur</strong> : evaporation normale, pas de fuite. Vous pouvez dormir tranquille.</li>
<li><strong>La piscine a baisse plus que le seau</strong> : la piscine fuit. La difference est l'indicateur du debit de fuite : 1 cm d'ecart = environ 320 L pour un 8×4 m.</li>
<li><strong>La piscine et le seau ont tous deux enormement baisse</strong> (5+ cm en 48h) : canicule extreme, refaire le test en conditions meteo normales.</li>
</ul>

<h2>Etape 3 : Filtration en marche ou a l'arret ?</h2>
<p>Si le test du seau confirme une fuite, l'etape suivante est de savoir si elle se situe sur le bassin lui-meme, sur les canalisations ou sur le local technique. Le test de la filtration le determine partiellement.</p>

<h3>Test avec filtration en marche</h3>
<p>Faites tourner la filtration normalement pendant 24 heures. Mesurez la perte d'eau.</p>

<h3>Test avec filtration a l'arret</h3>
<p>Coupez la filtration pendant 24 heures. Mesurez la perte d'eau.</p>

<h3>Interpretation</h3>
<ul>
<li><strong>Perte plus rapide filtration MARCHE qu'ARRET</strong> : fuite sur le refoulement (canalisation apres la pompe, sous pression). C'est le cas frequent.</li>
<li><strong>Perte plus rapide filtration ARRET qu'MARCHE</strong> : fuite sur l'aspiration (canalisation skimmer/bonde), car la pression negative sous pompe aspire l'air par la fuite au lieu de laisser sortir l'eau.</li>
<li><strong>Perte identique dans les deux cas</strong> : fuite sur le bassin (liner, coque, joint piece a sceller, fissure beton). La filtration n'est pas en cause.</li>
</ul>

<h2>Etape 4 : Ou se situe exactement le niveau quand la perte s'arrete ?</h2>
<p>Si votre piscine perd de l'eau mais que la baisse s'arrete a un certain niveau (ex : niveau du skimmer, niveau de la buse de refoulement), vous avez probablement identifie la zone de fuite.</p>

<ul>
<li><strong>Baisse s'arrete au niveau du skimmer</strong> : fuite au skimmer (joint mastic, bride, fissure de la piece). Tres frequent sur piscines liner de 25+ ans.</li>
<li><strong>Baisse s'arrete au niveau des buses de refoulement</strong> : fuite sur buse ou son raccord cache dans le beton.</li>
<li><strong>Baisse s'arrete au niveau de la prise balai</strong> : joint de prise balai ou raccord defectueux.</li>
<li><strong>Baisse continue sans s'arreter</strong> : fuite sur liner (perforation), bonde de fond, canalisation enterree ou fissure structurelle.</li>
</ul>

<h2>Etape 5 : Inspecter visuellement</h2>
<p>Avec votre propre observation, verifiez plusieurs points :</p>
<ol>
<li><strong>Margelles et plage</strong> : joints fissures, carrelages mobiles, zones anormalement humides ou affaissees.</li>
<li><strong>Local technique</strong> : flaque au sol, pompe qui goutte, filtre qui suinte, echangeur thermique corrode.</li>
<li><strong>Terrain autour</strong> : zone gorgee d'eau, gazon anormalement vert, terre qui s'affaisse sur un trace lineaire.</li>
<li><strong>Liner ou coque</strong> : plis recents, cloques, decoloration localisee, trous visibles (utilisez un masque de plongee si necessaire).</li>
</ol>

<h2>Etape 6 : quand appeler un professionnel</h2>
<p>Si vos diagnostics amateurs convergent vers une zone (skimmer, canalisation, liner) ou au contraire si vous etes perdu, il est temps de faire intervenir un specialiste de la recherche de fuite piscine. Le professionnel arrive avec :</p>
<ul>
<li>Colorant fluoresceine pour tester les pieces a sceller</li>
<li>Ecoute electro-acoustique pour les canalisations enterrees</li>
<li>Test de pression hydraulique pour isoler les circuits</li>
<li>Camera endoscopique sous-marine pour l'inspection visuelle poussee</li>
<li>Gaz traceur si fuite suspectee sur canalisations enterrees longues</li>
</ul>

<h2>Ce qu'il faut preparer avant l'intervention</h2>
<ul>
<li>Vos mesures de perte d'eau (avec dates)</li>
<li>Les resultats de vos tests du seau</li>
<li>L'historique de la piscine (annee de pose, dernier changement liner, interventions anterieures)</li>
<li>Les photos des zones suspectes</li>
<li>Votre contrat d'assurance habitation (pour verifier la garantie recherche de fuite)</li>
</ul>

<p>Cette preparation prealable peut vous faire economiser 30 a 50 % du temps d'intervention, donc potentiellement du tarif final. Pour les tarifs detailles selon le type de bassin, consultez notre guide <a href="/guide/recherche-fuite-piscine-tarif/" style="color:var(--green);text-decoration:underline;">tarif recherche de fuite piscine en Gironde</a>. Pour le remboursement assurance, voir <a href="/guide/recherche-fuite-piscine-assurance/" style="color:var(--green);text-decoration:underline;">recherche de fuite piscine et assurance habitation</a>. Pour faire intervenir nos techniciens, contactez-nous via la page <a href="/detection-fuite/piscine-bordeaux/" style="color:var(--green);text-decoration:underline;">recherche de fuite piscine a Bordeaux</a> ou l'une de nos pages ville dediees.</p>"""
    },
    {
        "slug": "fuite-liner-piscine",
        "title": "Fuite liner piscine : signes, causes et diagnostic",
        "title_seo": "Fuite liner piscine PVC signes causes diagnostic reparation",
        "desc": "Comment detecter et traiter une fuite sur liner PVC de piscine. Signes caracteristiques, causes frequentes, methodes de diagnostic, reparation locale ou changement complet.",
        "contenu": """<p>Le liner PVC est le revêtement le plus repandu sur les piscines privees en Gironde : environ 70 a 80 pourcent du parc existant, particulierement sur les bassins installés entre 1985 et 2015 dans les lotissements pavillonnaires de Merignac, Pessac, Le Bouscat, La Teste et Gujan-Mestras. Apres 20 a 30 ans d'usage, le liner entre dans sa phase critique ou les fuites deviennent frequentes. Cet article detaille comment identifier, diagnostiquer et traiter une fuite sur liner PVC.</p>

<h2>Types de liners concernes par les fuites</h2>
<p>Les liners PVC se declinent en plusieurs epaisseurs qui determinent leur longevite et leur susceptibilite aux fuites.</p>

<h3>Liner 75/100 (0,75 mm d'epaisseur)</h3>
<p>Le plus economique, souvent pose sur bassins familiaux simples (4×8 m, 5×10 m). Duree de vie theorique : 10 a 15 ans. En pratique, les bassins girondins avec liner 75/100 de plus de 12 ans montrent des signes d'usure generalise : plis figes, points de tension visibles, decoloration. Les fuites deviennent probables des 15 ans.</p>

<h3>Liner 85/100 (0,85 mm)</h3>
<p>Intermediaire, frequemment pose dans les annees 2000-2015 en remplacement de liners 75/100 d'origine. Duree de vie 15 a 20 ans. Resistance legerement superieure aux chocs et a l'usure sous-marche.</p>

<h3>Liner 100/100 arme (1 mm d'epaisseur armee)</h3>
<p>Liner renforce par armature textile, pose in situ et soudée. Duree de vie 20 a 30 ans. Frequemment choisi pour les renovations recentes ou les bassins haut de gamme. Tres resistant aux fuites localisees mais complexe a reparer (soudure a chaud specifique).</p>

<h2>Signes caracteristiques d'une fuite de liner</h2>

<h3>Signes visuels</h3>
<ul>
<li><strong>Pli ou boursouflure recente</strong> : decollement local du liner par rapport au support beton. Souvent precurseur d'une micro-perforation.</li>
<li><strong>Tache brune ou noire circulaire</strong> : infiltration d'eau entre le liner et le support, favorisant la moisissure visible par transparence.</li>
<li><strong>Angle qui se creuse</strong> : soudure au niveau des angles (souvent skimmer, marche, bonde) qui cede par fatigue mecanique.</li>
<li><strong>Liner qui flotte localement</strong> : presence d'une lame d'eau ou d'air entre le liner et le support, indiquant une infiltration importante.</li>
<li><strong>Decoloration brutale</strong> : zone localement plus claire ou plus sombre que le reste, signalant un contact different avec le support.</li>
</ul>

<h3>Signes hydrauliques</h3>
<ul>
<li>Baisse de niveau superieure a 1 cm par jour en conditions normales (voir <a href="/guide/ma-piscine-perd-de-l-eau-que-faire/" style="color:var(--green);text-decoration:underline;">guide ma piscine perd de l'eau</a> pour les reperes)</li>
<li>Baisse qui s'arrete a un niveau precis (skimmer, buse), indiquant la zone de fuite</li>
<li>Consommation d'eau en hausse sur la facture Suez ou regie</li>
<li>Deformation de la plage ou des margelles (infiltration sous la dalle)</li>
</ul>

<h2>Causes principales des fuites de liner</h2>

<h3>Vieillissement du PVC</h3>
<p>Le PVC perd sa plasticite apres 15 a 25 ans d'exposition aux UV, aux variations thermiques et au chlore. Il devient rigide, se retracte localement, fissure aux points de tension (angles, bonde, skimmer). Vous ne pouvez pas empecher ce processus : l'age du liner est le premier facteur.</p>

<h3>Brides desserrees</h3>
<p>Les pieces a sceller (skimmer, buses de refoulement, bonde de fond, prise balai) sont solidarisees au liner par des brides inox ou plastique. Apres 10 a 20 ans, ces brides peuvent se desserrer legerement sous l'effet des vibrations et des mouvements thermiques, creant un microgap par ou le liner fuit.</p>

<h3>Objets tranchants</h3>
<p>Chute d'un objet dans la piscine (tournevis, ciseau de jardinage, debris d'elagage), raclures de robot de nettoyage mal etalonne, impact lors de l'hivernage (chute de branche, glace cristalline sous la bache). Ces chocs peuvent percer le liner, parfois de maniere ponctuelle difficile a detecter.</p>

<h3>Chimie de l'eau defaillante</h3>
<p>Un pH trop bas (en dessous de 7,0) ou un taux de chlore excessivement eleve (au-dessus de 3 mg/L en permanence) accelere la degradation chimique du PVC. Le liner devient cassant, se craquelle progressivement. Frequent dans les piscines mal entretenues ou a traitement choc repete.</p>

<h3>Racines de plantes ou arbres</h3>
<p>Les piscines dont les abords sont plantes (bambous, oliviers, pins) peuvent voir des racines pousser sous le liner via un defaut d'etancheite peripherique. Les racines penetrent, souleven le liner et creent des points de fuite.</p>

<h3>Mouvements de terrain</h3>
<p>Les sols argileux de Bordeaux et des environs sont sujets au retrait-gonflement saisonnier. Ces mouvements sollicitent la structure du bassin et peuvent provoquer des fissures du support beton, qui se repercutent sur le liner en le sollicitant localement.</p>

<h2>Methodes de diagnostic pour fuite de liner</h2>

<h3>Colorant fluoresceine (methode de reference)</h3>
<p>On injecte a la seringue quelques gouttes de fluoresceine a proximite des zones suspectes, filtration a l'arret. Le colorant est aspire vers la fuite, revelant son parcours exact. C'est la methode privilegiee pour les fuites de pieces a sceller (skimmer, buses).</p>

<h3>Inspection visuelle en apnée</h3>
<p>Avec un masque et un tuba, inspection systematique des angles, soudures, pieces a sceller. Une perforation punctiforme (0,5 a 2 mm) se detecte par un leger courant d'eau sortant, visible aux debris flottants (poussieres, petites feuilles).</p>

<h3>Camera endoscopique sous-marine</h3>
<p>Camera etanche motorisée qui parcourt les parois et fond du bassin. Utile pour les piscines profondes (3-4 m) ou les zones d'acces difficile en apnée. Permet d'inspecter les soudures d'angles et les bondes de fond invisibles a l'oeil nu.</p>

<h3>Test d'inversion de pression</h3>
<p>On fait varier la pression dans les circuits d'alimentation pour reveler les fuites actives. Combine avec l'injection de colorant, cette methode est tres efficace sur les suspicions de fuites aux pieces a sceller.</p>

<h2>Reparation locale ou changement complet ?</h2>

<h3>Reparation locale (patch PVC)</h3>
<p>Pour une fuite isolee bien localisee (perforation mecanique, decollement de bride), un patch PVC peut etre colle sur le liner. Cout : 100 a 400 euros HT selon la zone. Duree de vie du patch : 5 a 10 ans. Economiquement pertinent si le liner a moins de 20 ans et que le reste est en bon etat.</p>

<h3>Reparation d'angle (soudure)</h3>
<p>Les fuites aux soudures d'angles peuvent etre reparees par nouvelle soudure a chaud specifique. Requiert du materiel professionnel (extrudeur, vent pulse). Cout : 200 a 600 euros HT. Duree de vie : 5 a 10 ans.</p>

<h3>Rejointoiement de piece a sceller</h3>
<p>Pour une fuite au niveau d'un skimmer ou d'une buse, le demontage de la bride, le renouvellement du joint mastic (silicone piscine) et le resserrage de la bride resolvent le probleme sans changer le liner. Cout : 200 a 500 euros HT selon le nombre de pieces.</p>

<h3>Changement complet du liner</h3>
<p>Lorsque le liner presente plusieurs signes d'usure generalisee (plis multiples, decolorations, soudures cedees, perforations multiples), un changement complet est necessaire. Cout : 3 000 a 8 000 euros HT pour un bassin standard 8×4 m, 6 000 a 12 000 euros pour 10×5 m. Le choix de liner peut inclure une montee en gamme (75/100 vers 85/100 ou 100/100 arme) pour prolonger la prochaine duree de vie.</p>

<h2>Decision : reparer ou changer ?</h2>
<p>Trois criteres orientent la decision :</p>
<ol>
<li><strong>Age du liner</strong> : moins de 15 ans = reparation locale privilegiee. Plus de 25 ans = changement recommande meme pour une fuite isolée.</li>
<li><strong>Nombre de fuites</strong> : une seule fuite localisee = reparation. Plusieurs fuites simultanees = le liner est en fin de vie, changement.</li>
<li><strong>Etat visuel general</strong> : decolorations, plis multiples, soudures fatigees = changement. Liner homogene par ailleurs = reparation.</li>
</ol>

<p>Notre rapport de diagnostic evalue objectivement ces criteres et vous remet une preconisation chiffrée. Pour les tarifs detailles selon le type de bassin et la methode retenue, consultez notre guide <a href="/guide/recherche-fuite-piscine-tarif/" style="color:var(--green);text-decoration:underline;">tarif recherche de fuite piscine</a>. Pour faire intervenir nos techniciens, consultez nos pages piscine par ville, notamment <a href="/detection-fuite/piscine-merignac/" style="color:var(--green);text-decoration:underline;">piscine Merignac</a> qui concentre la plus forte densite de liners PVC en fin de vie en Gironde.</p>"""
    },
    {
        "slug": "evaporation-vs-fuite-piscine",
        "title": "Evaporation ou fuite de piscine ? Le guide precis",
        "title_seo": "Evaporation eau piscine vs fuite Gironde climat test seau",
        "desc": "Comment distinguer l'evaporation normale d'une fuite sur votre piscine en Gironde. Taux mensuels selon le climat, protocoles de test, seuils d'alerte.",
        "contenu": """<p>Votre piscine perd de l'eau et la question tombe : est-ce une fuite, ou simplement de l'evaporation ? La reponse n'est pas toujours evidente, surtout en ete en Gironde ou l'evaporation peut etre importante. Cet article detaille les taux d'evaporation mensuels en climat aquitain, les facteurs qui les amplifient, et le protocole precis pour trancher entre evaporation et fuite.</p>

<h2>L'evaporation de piscine : un phenomene physique predictible</h2>
<p>L'evaporation est le passage de l'eau liquide a l'etat gazeux, provoque par la chaleur de l'eau et la sollicitation atmospherique. Contrairement aux idees recues, l'evaporation d'une piscine ne depend pas uniquement de la temperature de l'air : elle resulte d'un calcul complexe impliquant la temperature de l'eau, la temperature de l'air, l'humidite relative et surtout la vitesse du vent.</p>

<h3>Les 4 facteurs qui determinent l'evaporation</h3>
<ul>
<li><strong>Temperature de l'eau</strong> : plus l'eau est chaude, plus elle s'evapore. Une piscine chauffee a 28 degrees evapore plus qu'une piscine a 22 degrees.</li>
<li><strong>Temperature de l'air</strong> : importante mais moins que l'on pense. Une journee a 35 degrees provoque certes plus d'evaporation qu'a 25 degrees, mais l'ecart n'est pas aussi spectaculaire.</li>
<li><strong>Humidite relative</strong> : plus l'air est sec, plus il peut absorber de l'humidite et donc plus l'evaporation est forte. Une journee a 30 pourcent d'humidite fait bien plus evaporer qu'a 80 pourcent.</li>
<li><strong>Vitesse du vent</strong> : facteur le plus sous-estime. Le vent emporte la couche d'air humide a la surface de l'eau et permet a de l'air sec de la remplacer, relancant l'evaporation en continu. Une journee ventee peut quadrupler l'evaporation par rapport a une journee calme.</li>
</ul>

<h2>Taux d'evaporation mensuels en Gironde</h2>
<p>Voici les moyennes mensuelles d'evaporation pour une piscine exterieure non abritee en plaine bordelaise, basees sur les donnees meteo historiques de la region. Valeurs en mm/jour (1 mm = 1 litre par m² de surface de piscine).</p>

<table style="width:100%;border-collapse:collapse;margin:1.5rem 0;background:#fff;">
<thead><tr style="background:#0D3B2E;color:#fff;"><th style="padding:.75rem;text-align:left;border:1px solid #155740;">Mois</th><th style="padding:.75rem;text-align:left;border:1px solid #155740;">Evaporation moy. (mm/jour)</th><th style="padding:.75rem;text-align:left;border:1px solid #155740;">Pic observable</th><th style="padding:.75rem;text-align:left;border:1px solid #155740;">Contexte</th></tr></thead>
<tbody>
<tr><td style="padding:.75rem;border:1px solid #D8D4CC;">Janvier</td><td style="padding:.75rem;border:1px solid #D8D4CC;">0,5 a 1,5</td><td style="padding:.75rem;border:1px solid #D8D4CC;">2 mm</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Hivernage generalise, evaporation minimale</td></tr>
<tr style="background:#F7F6F2;"><td style="padding:.75rem;border:1px solid #D8D4CC;">Fevrier</td><td style="padding:.75rem;border:1px solid #D8D4CC;">0,5 a 2</td><td style="padding:.75rem;border:1px solid #D8D4CC;">3 mm</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Vent d'ouest accentué en cas de depression</td></tr>
<tr><td style="padding:.75rem;border:1px solid #D8D4CC;">Mars</td><td style="padding:.75rem;border:1px solid #D8D4CC;">1 a 3</td><td style="padding:.75rem;border:1px solid #D8D4CC;">5 mm</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Remise en route, eau froide, vent printanier</td></tr>
<tr style="background:#F7F6F2;"><td style="padding:.75rem;border:1px solid #D8D4CC;">Avril</td><td style="padding:.75rem;border:1px solid #D8D4CC;">2 a 4</td><td style="padding:.75rem;border:1px solid #D8D4CC;">6 mm</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Reprise saison, vents d'ouest reguliers</td></tr>
<tr><td style="padding:.75rem;border:1px solid #D8D4CC;">Mai</td><td style="padding:.75rem;border:1px solid #D8D4CC;">3 a 5</td><td style="padding:.75rem;border:1px solid #D8D4CC;">7 mm</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Mois a forte evaporation par forte amplitude thermique</td></tr>
<tr style="background:#F7F6F2;"><td style="padding:.75rem;border:1px solid #D8D4CC;"><strong>Juin</strong></td><td style="padding:.75rem;border:1px solid #D8D4CC;"><strong>4 a 6</strong></td><td style="padding:.75rem;border:1px solid #D8D4CC;"><strong>8 mm</strong></td><td style="padding:.75rem;border:1px solid #D8D4CC;">Pleine saison, chaleur + vents reguliers</td></tr>
<tr><td style="padding:.75rem;border:1px solid #D8D4CC;"><strong>Juillet</strong></td><td style="padding:.75rem;border:1px solid #D8D4CC;"><strong>5 a 7</strong></td><td style="padding:.75rem;border:1px solid #D8D4CC;"><strong>10 mm</strong></td><td style="padding:.75rem;border:1px solid #D8D4CC;">Canicule + vent d'ouest = pic d'evaporation</td></tr>
<tr style="background:#F7F6F2;"><td style="padding:.75rem;border:1px solid #D8D4CC;"><strong>Aout</strong></td><td style="padding:.75rem;border:1px solid #D8D4CC;"><strong>5 a 7</strong></td><td style="padding:.75rem;border:1px solid #D8D4CC;"><strong>10 mm</strong></td><td style="padding:.75rem;border:1px solid #D8D4CC;">Similaire a juillet, possibles orages interrupteurs</td></tr>
<tr><td style="padding:.75rem;border:1px solid #D8D4CC;">Septembre</td><td style="padding:.75rem;border:1px solid #D8D4CC;">3 a 5</td><td style="padding:.75rem;border:1px solid #D8D4CC;">7 mm</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Baisse progressive, encore forte en debut de mois</td></tr>
<tr style="background:#F7F6F2;"><td style="padding:.75rem;border:1px solid #D8D4CC;">Octobre</td><td style="padding:.75rem;border:1px solid #D8D4CC;">1 a 3</td><td style="padding:.75rem;border:1px solid #D8D4CC;">5 mm</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Retrocedence, hivernage imminent</td></tr>
<tr><td style="padding:.75rem;border:1px solid #D8D4CC;">Novembre</td><td style="padding:.75rem;border:1px solid #D8D4CC;">0,5 a 2</td><td style="padding:.75rem;border:1px solid #D8D4CC;">3 mm</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Hivernage en cours</td></tr>
<tr style="background:#F7F6F2;"><td style="padding:.75rem;border:1px solid #D8D4CC;">Decembre</td><td style="padding:.75rem;border:1px solid #D8D4CC;">0,5 a 1,5</td><td style="padding:.75rem;border:1px solid #D8D4CC;">2 mm</td><td style="padding:.75rem;border:1px solid #D8D4CC;">Hivernage, evaporation minimale</td></tr>
</tbody>
</table>

<h3>Facteurs multiplicateurs locaux</h3>
<ul>
<li><strong>Bassin d'Arcachon, Cap-Ferret, front de dune</strong> : vent marin permanent, evaporation augmentee de 20 a 40 pourcent par rapport a la valeur tablee</li>
<li><strong>Pinede dense autour du bassin</strong> : effet de protection du vent, evaporation reduite de 15 a 25 pourcent</li>
<li><strong>Piscine chauffee (PAC ou abri)</strong> : evaporation doublee car l'eau reste a 28-30 degrees toute la saison, augmentant le gradient thermique</li>
<li><strong>Piscine debordement/miroir</strong> : evaporation multipliee par 1,5 a 2 en raison de la surface d'eau en contact avec l'air nettement plus large</li>
</ul>

<h2>Protocole scientifique pour distinguer evaporation et fuite</h2>

<h3>Test de controle sur 48 heures</h3>
<p>Le protocole rigoureux d'observation :</p>
<ol>
<li>Definissez une fenetre de 48 heures sans baignade, sans pluie attendue, sans canicule hors-norme. Idealement, choisissez un week-end normal ou vous n'utilisez pas la piscine.</li>
<li>Arretez la filtration (pour les piscines qui ne necessitent pas de filtration continue) afin de limiter la variabilite.</li>
<li>Relevez le niveau d'eau initial avec precision (millimetre pres) sur la paroi du bassin.</li>
<li>Relevez simultanement le niveau dans un seau immerge aux 2/3 sur la premiere marche.</li>
<li>Notez la meteo : temperature max/min, humidite, vent, absence de pluie.</li>
<li>Apres 48 heures, relevez les deux niveaux et calculez la perte par jour de la piscine et du seau.</li>
</ol>

<h3>Formule de decision</h3>
<p>Calculez le delta : <strong>perte piscine - perte seau = fuite presumee</strong></p>
<ul>
<li>Delta de 0 a 2 mm/jour : pas de fuite significative. Evaporation seule en cause.</li>
<li>Delta de 2 a 5 mm/jour : fuite faible, a investiguer. Pourrait etre un joint qui fatigue.</li>
<li>Delta de 5 a 10 mm/jour : fuite confirmee, intervention professionnelle recommandee sous 2 semaines.</li>
<li>Delta superieur a 10 mm/jour : fuite importante, intervention urgente sous 48 heures pour eviter degats collateraux.</li>
</ul>

<h2>Pieges frequents a eviter</h2>

<h3>Test fait pendant une canicule</h3>
<p>Un test d'evaporation fait pendant un pic de chaleur avec forts vents peut sous-estimer la fuite reelle (car l'evaporation naturelle du seau masque partiellement la fuite). Attendez une periode meteorologique stable.</p>

<h3>Oubli du remplissage automatique</h3>
<p>De nombreuses piscines ont un regulateur de niveau automatique qui compense en permanence les baisses. Si vous ne le coupez pas pendant le test, vous ne verrez jamais la baisse : votre regulateur la masquera. Coupez imperativement cette regulation pendant le test.</p>

<h3>Piscine en plein soleil direct toute la journee</h3>
<p>Une piscine exposée plein sud chauffe vite, ce qui amplifie l'evaporation. Si votre piscine est particulierement exposee, vos taux d'evaporation peuvent depasser les valeurs de table de 30 a 50 pourcent. Faites plusieurs tests sur differents episodes meteo pour calibrer votre cas.</p>

<h3>Confondre evaporation et micro-fuite chronique</h3>
<p>Une fuite tres petite (2-3 mm/jour) sur une piscine en pleine saison peut se confondre avec l'evaporation normale. Seul le test rigoureux du seau tranche. Ne vous fiez pas a votre intuition : mesurer avant de conclure.</p>

<h2>Quand refaire le test</h2>
<p>Si vos premiers tests concluent a une simple evaporation mais que vous restez inquiet, refaites un test :</p>
<ul>
<li>Apres un changement meteo majeur (fin de canicule, arret des vents)</li>
<li>Apres 1 mois, pour voir si la situation evolue</li>
<li>Apres un evenement suspect (orage violent, chute dans la piscine)</li>
</ul>

<p>Si plusieurs tests independants concluent a une fuite, ou si votre consommation d'eau augmente de maniere marquee sans explication, il est temps de faire intervenir un professionnel. Pour en savoir plus sur les etapes a suivre, consultez notre guide <a href="/guide/ma-piscine-perd-de-l-eau-que-faire/" style="color:var(--green);text-decoration:underline;">ma piscine perd de l'eau, que faire</a>. Pour le diagnostic sur un liner PVC, voir l'article <a href="/guide/fuite-liner-piscine/" style="color:var(--green);text-decoration:underline;">fuite sur liner piscine</a>. Pour faire intervenir nos techniciens, consultez nos pages piscine par ville, avec le detail de nos methodes d'intervention non destructives.</p>"""
    },
    {
        "slug": "loi-warsmann-ecretement-facture-eau",
        "title": "Loi Warsmann : ecretement de facture d'eau apres fuite",
        "title_seo": "Loi Warsmann ecretement facture eau fuite canalisation enterree",
        "desc": "Comment beneficier de l'ecretement de facture d'eau apres une fuite sur canalisation enterree. La loi Warsmann 2011 expliquee : conditions, procedure, jurisprudence.",
        "contenu": """<p>Une fuite sur votre canalisation enterrée peut faire exploser votre facture d'eau en quelques semaines. La loi dite Warsmann, adoptee en 2011 et codifiee a l'article L2224-12-4 du Code general des collectivites territoriales, limite le cout supporte par le consommateur dans ce cas precis. Encore faut-il connaître les conditions pour en beneficier. Cet article detaille la procedure, les documents a fournir, les ecueils frequents et les precedents jurisprudentiels.</p>

<h2>Que dit la loi Warsmann ?</h2>
<p>Le texte legal oblige les services publics d'eau a informer tout abonne d'une consommation anormale (superieure au double de la consommation moyenne sur les trois dernieres annees). L'abonne dispose alors d'un mois pour prouver qu'une fuite sur canalisation enterree, invisible et indetectable, est a l'origine de cette surconsommation. Si cette preuve est apportee, sa facture est plafonnee au double de sa consommation habituelle : c'est l'ecretement.</p>

<h3>Le mecanisme d'ecretement en pratique</h3>
<p>Concretement, si votre consommation habituelle est de 120 m³/an (moyenne sur 3 ans), votre facture ne pourra jamais depasser 240 m³/an au tarif de l'eau, meme si votre compteur a enregistre 800 m³ a cause de la fuite. Les 560 m³ restants ne vous sont pas factures. A 4 euros TTC le m³, cela represente une economie de 2 240 euros par rapport a une facturation integrale.</p>

<h2>Les conditions obligatoires pour beneficier de l'ecretement</h2>

<h3>Condition 1 : canalisation enterrée privative</h3>
<p>La fuite doit concerner une canalisation enterrée qui appartient a votre reseau privatif : entre le compteur d'eau et votre habitation, ou reseaux enterres a l'interieur de votre propriete (arrosage, piscine, dependance). Les fuites suivantes <strong>ne sont pas eligibles</strong> :</p>
<ul>
<li>Fuite d'equipement visible (chasse d'eau, robinet, chauffe-eau)</li>
<li>Fuite dans un mur ou sous une dalle (canalisation interieure, meme si invisible)</li>
<li>Fuite sur reseau d'arrosage automatique classique</li>
<li>Fuite sur le reseau public (avant le compteur) : a la charge du distributeur d'eau</li>
</ul>

<h3>Condition 2 : fuite indetectable visuellement</h3>
<p>La fuite doit avoir ete indetectable a l'oeil nu avant sa decouverte par un professionnel. Si elle se manifestait par une flaque, une zone humide evidente, un affaissement du sol ou tout autre signe visuel avant que vous n'interveniez, l'ecretement peut etre refusé. C'est precisement ce qui differencie cette loi : elle protege le consommateur qui n'avait aucun moyen raisonnable de detecter la fuite.</p>

<h3>Condition 3 : intervention d'un professionnel qualifié</h3>
<p>Une attestation de reparation doit etre fournie, etablie par un professionnel (plombier, specialiste de la recherche de fuite). Cette attestation doit mentionner explicitement :</p>
<ul>
<li>La date de l'intervention</li>
<li>La nature de la canalisation defectueuse et sa localisation enterree</li>
<li>Le type de reparation effectuee</li>
<li>L'attestation que la fuite a bien ete resolue</li>
</ul>

<h3>Condition 4 : delai d'un mois</h3>
<p>Vous avez un mois apres notification de surconsommation par votre distributeur pour fournir l'attestation de reparation. Passé ce delai, l'ecretement n'est plus automatiquement accessible (mais un recours reste possible).</p>

<h2>Procedure pas a pas pour obtenir l'ecretement</h2>

<h3>Etape 1 : vous recevez la notification de surconsommation</h3>
<p>Votre distributeur d'eau (Suez, Veolia, Regie des eaux) a l'obligation legale de vous alerter en cas de consommation anormalement elevee. La notification se fait par courrier, email ou via l'espace client. Le courrier indique votre surconsommation (en m³), la moyenne des 3 annees precedentes, et mentionne votre droit a l'ecretement selon la loi Warsmann.</p>

<h3>Etape 2 : vous identifiez la fuite</h3>
<p>Verifiez d'abord si la fuite est avant ou apres le compteur : fermez votre robinet d'arret general. Si le compteur continue de tourner, la fuite est avant (reseau public, pas votre responsabilite). S'il s'arrete mais vous constatez toujours une perte, la fuite est apres le compteur sur votre reseau privatif.</p>

<h3>Etape 3 : localisation par un professionnel</h3>
<p>Pour obtenir l'ecretement, il ne suffit pas de savoir qu'il y a une fuite : il faut la localiser precisement pour pouvoir la reparer. Nous intervenons avec du gaz traceur azote/helium pour localiser les fuites sur canalisations enterrees avec une precision au demi-metre. Notre rapport mentionne explicitement la localisation enterrée et le caractere indetectable visuellement, deux elements cles pour le dossier Warsmann.</p>

<h3>Etape 4 : reparation et attestation</h3>
<p>La reparation peut etre faite par le meme professionnel ou par un plombier mandate. A l'issue, demandez une attestation de reparation mentionnant : canalisation enterrée, localisation, date, certification que la fuite est resolue.</p>

<h3>Etape 5 : envoi du dossier au distributeur</h3>
<p>Envoyez en courrier recommande avec accuse de reception a votre distributeur d'eau :</p>
<ul>
<li>Copie de la notification de surconsommation</li>
<li>Rapport de localisation de fuite</li>
<li>Attestation de reparation</li>
<li>Photos si disponibles (zone de fuite, reparation en cours)</li>
<li>Courrier de demande explicite d'application de la loi Warsmann</li>
</ul>

<h3>Etape 6 : ecretement applique sur la facture suivante</h3>
<p>Si le dossier est complet, le distributeur applique l'ecretement sur votre facture suivante (delai moyen 1 a 2 mois). La part excedentaire au-dessus du double de votre consommation habituelle est soit annulee, soit remboursee si deja payee.</p>

<h2>Modele de courrier a envoyer</h2>

<blockquote style="background:var(--c-bg);border-left:4px solid var(--c-primary);padding:1rem;margin:1rem 0;font-family:Georgia,serif;">
<p>[Votre adresse]</p>
<p>[Date]</p>
<p>Objet : Demande d'ecretement de facture d'eau - Loi Warsmann - Reference client [numero]</p>
<p>Madame, Monsieur,</p>
<p>Suite a votre notification de surconsommation d'eau en date du [date], je vous adresse ci-joint les justificatifs permettant l'application de la loi n° 2011-525 du 17 mai 2011 (dite loi Warsmann) et l'ecretement de ma facture.</p>
<p>Je vous confirme que la fuite concernait une canalisation enterree privative (entre mon compteur d'eau et mon habitation), indetectable a l'oeil nu, comme en atteste le rapport de recherche de fuite etabli par [nom de l'entreprise] le [date]. La reparation a ete effectuee le [date] et est documentee par l'attestation ci-jointe.</p>
<p>Conformement a l'article L2224-12-4 du Code general des collectivites territoriales, je vous demande de bien vouloir plafonner ma facture au double de ma consommation moyenne des trois dernieres annees, soit [X] m³.</p>
<p>Documents joints : rapport de recherche de fuite, attestation de reparation, photos de la zone.</p>
<p>Je vous prie d'agreer, Madame, Monsieur, l'expression de mes salutations distinguees.</p>
</blockquote>

<h2>Cas complexes et jurisprudence</h2>

<h3>Cas 1 : la fuite etait partiellement visible</h3>
<p>Si l'humidite etait visible mais qu'il etait objectivement impossible de suspecter une fuite (ex : zone de pelouse legerement plus verte depuis plusieurs annees, interpretee comme effet d'arrosage naturel), la jurisprudence admet generalement l'ecretement. Notre rapport doit alors argumenter specifiquement pourquoi le signe visible etait ambigu et n'imposait pas intervention.</p>

<h3>Cas 2 : delai depasse d'un mois</h3>
<p>Si vous avez laisse passer le delai d'un mois, un recours est toujours possible en sollicitant le mediateur de l'eau ou en saisissant le tribunal judiciaire. Les distributeurs acceptent souvent l'ecretement apres mediation, meme hors delai, car le contentieux est couteux pour eux.</p>

<h3>Cas 3 : plusieurs fuites dans l'annee</h3>
<p>Si vous avez deja beneficie d'un ecretement dans les 5 annees precedentes, le distributeur peut contester le caractere exceptionnel de la demande. Dans ce cas, une expertise contradictoire peut etre mise en oeuvre.</p>

<h3>Cas 4 : locataire ou proprietaire</h3>
<p>L'ecretement s'applique au titulaire du contrat d'eau, qu'il soit proprietaire ou locataire. En location, le locataire demande l'ecretement mais doit informer le bailleur (qui est responsable de la reparation definitive si la fuite est sur une canalisation enterrée privative).</p>

<h2>Economies realisables concretes</h2>
<p>Quelques exemples reels de dossiers sur lesquels nous sommes intervenus en Gironde en 2025 :</p>
<ul>
<li>Maison Caudéran, fuite enterrée 40 m de canalisation PVC : surconsommation 680 m³ sur 6 mois. Facture initiale 3 200 euros, facture apres ecretement 950 euros. <strong>Economie : 2 250 euros.</strong></li>
<li>Pavillon Merignac, fuite enterrée arrosage automatique: 420 m³ surconsommation. Facture initiale 1 680 euros, apres ecretement 580 euros. <strong>Economie : 1 100 euros.</strong></li>
<li>Villa Arcachon, fuite tres lente 12 mois non detectee : 240 m³ surconsommation. Facture initiale 960 euros, apres ecretement 420 euros. <strong>Economie : 540 euros.</strong></li>
</ul>

<p>Notre intervention (environ 450 euros HT en moyenne pour la recherche de fuite enterrée) est largement rentabilisee par l'ecretement dans la majorite des cas. Pour en savoir plus sur notre methodologie gaz traceur, consultez notre page <a href="/detection-fuite/canalisation-enterree-bordeaux/" style="color:var(--green);text-decoration:underline;">recherche de fuite canalisation enterrée a Bordeaux</a>. Pour les fuites apres compteur plus generalement, voir <a href="/detection-fuite/fuite-apres-compteur/" style="color:var(--green);text-decoration:underline;">fuite d'eau apres compteur</a>. Pour prendre rendez-vous, utilisez notre formulaire de <a href="/devis/" style="color:var(--green);text-decoration:underline;">demande de devis gratuit</a>.</p>"""
    },
    {
        "slug": "prix-recherche-fuite-bordeaux",
        "title": "Prix d'une recherche de fuite à Bordeaux en 2026",
        "title_seo": "Prix recherche de fuite Bordeaux tarif devis intervention 2026",
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
<tr style="background:#F7F6F2;"><td style="padding:.75rem;border:1px solid #D8D4CC;">Diagnostic combiné complexe (plusieurs méthodes)</td><td style="padding:.75rem;border:1px solid #D8D4CC;">600 à 900 €</td><td style="padding:.75rem;border:1px solid #D8D4CC;">3 h à 5 h</td></tr>
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
        <div id="form-devis-error" style="display:none;background:rgba(239,68,68,.2);border:1px solid rgba(239,68,68,.4);border-radius:8px;padding:1rem;text-align:center;margin-bottom:1rem;"><p style="color:#fecaca;font-size:.9rem;margin:0;">Une erreur est survenue. Veuillez r\u00e9essayer ou nous appeler directement.</p></div>
        <form data-ajax data-error="form-devis-error">
          <input type="hidden" name="_subject" value="[recherche-fuite-gironde.fr] Demande de devis">
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
        "specificites": [
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
             "Pas toujours. Dans les immeubles anciens bordelais, la colonne d'évacuation commune (EU/EV) est en cause dans 60 pourcent des cas où un plafond s'humidifie, et non pas directement le logement du dessus. Notre diagnostic identifie précisément l'origine pour éviter les litiges injustifiés avec le voisinage.")
        ],
    },
    "merignac": {
        "ville": "Mérignac",
        "ville_article": "à Mérignac",
        "cp": "33700",
        "image": "ville-merignac-residentiel.webp",
        "image_alt": "Maison individuelle typique de Mérignac, zone d'intervention recherche de fuite en métropole bordelaise",
        "pitch_local": "Deuxième ville de la métropole bordelaise, Mérignac combine zones résidentielles pavillonnaires, quartiers pavillonnaires anciens et grands ensembles récents. Les maisons individuelles des années 1970 à 2000 constituent l'essentiel du parc immobilier, avec des problématiques caractéristiques de fuites sur canalisations enterrées et plancher chauffant.",
        "quartiers": "Mérignac Centre, Arlac, Capeyron, Chemin Long, Beutre, Beaudésert, Le Burck, Les Eyquems, Pichey",
        "zones_voisines": "Bordeaux, Le Haillan, Eysines, Pessac, Saint-Médard-en-Jalles",
        "specificites": [
            ("Pavillons des années 80-2000 et planchers chauffants", "Beaucoup de maisons mérignacaises de cette période ont été équipées de planchers chauffants hydrauliques. Après 20 à 40 ans d'utilisation, les micro-perforations sur les tubes PER ou polybutylène sont fréquentes. Notre thermographie infrarouge localise la fuite au degré près sans toucher à la chape."),
            ("Canalisations d'alimentation enterrées longues", "Les maisons avec grand terrain (plus fréquentes à Arlac ou Beutre) ont des canalisations d'eau enterrées de 10 à 50 mètres entre le regard de compteur et la maison. Une fuite sur ce tronçon peut passer inaperçue pendant des mois et gonfler la facture d'eau avant d'être détectée."),
            ("Piscines privées nombreuses", "Mérignac concentre une forte densité de piscines individuelles, notamment dans les quartiers résidentiels. Les fuites sur pièces à sceller (skimmer, buses) et canalisations enterrées autour du bassin sont notre quotidien."),
            ("Proximité aéroport et réseaux multiples", "La zone aéroportuaire et les zones d'activité génèrent des demandes sur des bâtiments tertiaires, des copropriétés récentes et des résidences en locations saisonnières. Chaque configuration a sa propre signature de fuite que nos techniciens savent identifier.")
        ],
        "cas_frequent": "Scénario classique à Mérignac : pavillon Arlac années 1995, propriétaire qui reçoit une facture d'eau de 1 200 euros sur un trimestre (contre 250 habituellement). Compteur qui tourne en permanence, pas de tache dans la maison. Notre diagnostic : test du robinet d'arrêt général (fuite après compteur), gaz traceur azote/hélium injecté sur la canalisation enterrée compteur vers maison (45 mètres de tracé). La fuite se trouve à 28 mètres du compteur, au droit d'un raccord PVC désaxé par mouvement de terrain. Réparation : ouverture 1 m² au point localisé, remplacement du raccord, rebouchage. Coût total intervention + réparation : 850 euros, remboursables en grande partie par la garantie recherche de fuite de l'assurance.",
        "methodes_focus": "Sur le parc pavillonnaire mérignacais (majoritairement années 1970-2000 avec canalisations enterrées longues), nos deux méthodes de référence sont le gaz traceur azote/hélium pour les alimentations enterrées entre compteur et maison (souvent 20 à 50 mètres), et la thermographie infrarouge pour les planchers chauffants hydrauliques très répandus à Arlac, Capeyron et Chemin Long. L'écoute électro-acoustique complète sur les réseaux sous dalle béton, et le test de pression sur boucle permet d'isoler le circuit en défaut avant localisation fine. Pour les piscines nombreuses de la commune, nous déployons en plus colorant fluorescéine et inspection caméra sous-marine.",
        "faq_locale": [
            ("Le compteur d'eau tourne chez moi à Mérignac : fuite avant ou après compteur ?",
             "Faites le test de fermeture : tournez votre robinet d'arrêt général situé juste après le compteur. Si le compteur continue de tourner, la fuite est AVANT (réseau public Suez), à leur charge. S'il s'arrête mais que vous avez toujours une perte, la fuite est APRÈS (réseau privatif), à votre charge. Ce diagnostic simple oriente immédiatement la suite."),
            ("Peut-on obtenir un écrêtement de facture d'eau avec Suez Mérignac ?",
             "Oui, la loi Warsmann (2011) permet de plafonner la surfacturation liée à une fuite sur canalisation enterrée non détectable. Il faut fournir à Suez une attestation de réparation par un professionnel et un rapport de localisation de fuite (comme celui que nous émettons). Votre facture est alors ramenée à deux fois votre consommation habituelle."),
            ("Ma maison Mérignac a un plancher chauffant qui perd de pression : vous intervenez ?",
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
        "specificites": [
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
        "specificites": [
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
             "Absolument, c'est un piège classique à Libourne. Une cave voûtée humide peut donner l'impression d'une fuite alors qu'il s'agit de remontées capillaires dues à la nappe proche de la Dordogne. Notre humidimètre mesure la teneur précise en eau dans les matériaux et distingue une infiltration ponctuelle (gradient fort, zone localisée) d'une remontée (humidité diffuse et constante). Nous ne lançons une intervention que si la fuite est réellement caractérisée."),
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
        "specificites": [
            ("Cité Frugès et patrimoine XXe siècle", "La Cité Frugès imaginée par Le Corbusier dans les années 1920, classée au patrimoine mondial de l'UNESCO, présente un parc immobilier aux caractéristiques techniques particulières. Toute intervention doit être menée avec la plus grande délicatesse pour respecter l'intégrité architecturale protégée."),
            ("Résidences universitaires et copropriétés", "Les quartiers d'Alouette et de Saige comptent un grand nombre de résidences étudiantes et de copropriétés familiales des années 1960-80. Les colonnes montantes et les évacuations collectives sont souvent à l'origine de fuites récurrentes entre logements, relevant de la convention IRSI en copropriété."),
            ("Domaines viticoles Graves et Pessac-Léognan", "Les appellations Pessac-Léognan comptent des châteaux historiques sur le territoire (Haut-Brion, Pape-Clément, Les Carmes Haut-Brion). Leurs réseaux hydrauliques combinent piscines, arrosage, chais et résidences, ce qui complexifie la recherche de fuite en cas de surconsommation."),
            ("Zone Bersol et bâti tertiaire récent", "Le parc d'activité de Bersol et les zones tertiaires récentes accueillent des bâtiments aux réseaux modernes (multicouche, PE). Les fuites y sont souvent liées à des défauts de pose sur sertissage ou à des mouvements de dalle. Notre écoute électro-acoustique cible précisément ces signatures.")
        ],
        "cas_frequent": "Cas fréquent à Pessac : copropriété familiale de 40 logements à Alouette, construite en 1972. Le syndic signale des fuites récurrentes au dernier étage depuis 6 mois, avec plusieurs logements touchés par intermittence. Notre diagnostic pour le conseil syndical : inspection caméra des colonnes montantes EU/EV communes, écoute acoustique, identification des tronçons corrodés. Rapport remis : 4 zones de fuite identifiées sur la colonne montante principale, matériau fonte gris d'origine fatigué. Préconisation : chemisage de la colonne par manchon résine époxy (durée de vie 50 ans), intervention planifiée en AG extraordinaire avec vote article 25.",
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
          <p>Inspection Télévisée : une caméra motorisée parcourt l'intérieur des canalisations via un accès existant. Identifie fissures, racines, casses, dépôts selon la norme NF EN 13508-2.</p>
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
          <h3>Surconsommation d'eau</h3>
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
          <tr style="background:var(--c-primary);color:var(--white);">
            <th style="padding:.8rem;text-align:left;border:1px solid var(--c-primary-mid);">Critère</th>
            <th style="padding:.8rem;text-align:left;border:1px solid var(--c-primary-mid);">Détection non destructive</th>
            <th style="padding:.8rem;text-align:left;border:1px solid var(--c-primary-mid);">Percement classique</th>
          </tr>
        </thead>
        <tbody>
          <tr><td style="padding:.8rem;border:1px solid var(--c-border);"><strong>Ouverture des murs/sols</strong></td><td style="padding:.8rem;border:1px solid var(--c-border);">Aucune avant localisation</td><td style="padding:.8rem;border:1px solid var(--c-border);">Multiples points au hasard</td></tr>
          <tr style="background:var(--c-bg);"><td style="padding:.8rem;border:1px solid var(--c-border);"><strong>Durée du diagnostic</strong></td><td style="padding:.8rem;border:1px solid var(--c-border);">1h30 à 3h</td><td style="padding:.8rem;border:1px solid var(--c-border);">Plusieurs jours</td></tr>
          <tr><td style="padding:.8rem;border:1px solid var(--c-border);"><strong>Reprise des finitions</strong></td><td style="padding:.8rem;border:1px solid var(--c-border);">Nulle ou très limitée</td><td style="padding:.8rem;border:1px solid var(--c-border);">Lourde (carrelage, plâtre)</td></tr>
          <tr style="background:var(--c-bg);"><td style="padding:.8rem;border:1px solid var(--c-border);"><strong>Coût global</strong></td><td style="padding:.8rem;border:1px solid var(--c-border);">300 à 900 € HT</td><td style="padding:.8rem;border:1px solid var(--c-border);">Souvent &gt; 2 000 €</td></tr>
          <tr><td style="padding:.8rem;border:1px solid var(--c-border);"><strong>Rapport assurance</strong></td><td style="padding:.8rem;border:1px solid var(--c-border);">Inclus, opposable IRSI</td><td style="padding:.8rem;border:1px solid var(--c-border);">Variable, souvent insuffisant</td></tr>
          <tr style="background:var(--c-bg);"><td style="padding:.8rem;border:1px solid var(--c-border);"><strong>Occupation logement</strong></td><td style="padding:.8rem;border:1px solid var(--c-border);">Maintenue</td><td style="padding:.8rem;border:1px solid var(--c-border);">Souvent impossible</td></tr>
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

    # Construction des sections specificites
    specificites_html = '\n'.join([
        f'    <h3>{titre}</h3>\n    <p>{contenu}</p>'
        for titre, contenu in ctx['specificites']
    ])

    # Methodes focus unique par ville
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
      <a href="#methodes" class="btn btn-outline-green">Nos méthodes</a>
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

<section class="section section-alt" id="methodes">
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
    <p>Chaque territoire a ses particularités. Nos techniciens connaissent celles de {ville} pour adapter leurs méthodes à votre configuration.</p>

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

{form_section(ville)}
'''

    return html_base(
        f'Recherche de fuite d\'eau {ville_article} ({cp}) | Sans démolition',
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
    <p>Prévenez-les immédiatement et le syndic si vous êtes en copropriété. Prenez des photos datées avant tout nettoyage. Déclarez le sinistre à votre assurance en mentionnant les voisins impactés : la convention IRSI s'applique automatiquement entre assureurs pour les sinistres dégâts des eaux en copropriété jusqu'à 5 000 € HT.</p>

    <div style="margin-top:2rem;text-align:center;">
      <a href="/devis/" class="btn btn-gold">Demander une intervention urgente</a>
    </div>
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
# PAGE USE CASE : Fuite plancher chauffant Bordeaux
# ═══════════════════════════════════════════════════════════════

def page_plancher_chauffant_bordeaux():
    ld_service = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "Recherche de fuite plancher chauffant",
  "name": "Detection de fuite plancher chauffant a Bordeaux et metropole",
  "description": "Localisation precise d'une fuite sur plancher chauffant hydraulique par thermographie infrarouge et test de pression. Sans casser la chape, pour reparation ciblee.",
  "provider": {
    "@type": "LocalBusiness",
    "name": "Recherche Fuite Gironde",
    "url": "https://recherche-fuite-gironde.fr/"
  },
  "areaServed": { "@type": "Place", "name": "Bordeaux et metropole girondine" },
  "category": "Detection de fuite non destructive"
}
</script>'''

    ld_local = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Recherche Fuite Gironde - Plancher chauffant Bordeaux",
  "description": "Specialiste de la recherche de fuite sur plancher chauffant hydraulique a Bordeaux et sa metropole. Thermographie infrarouge, test de pression, localisation au point.",
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
    { "@type": "ListItem", "position": 2, "name": "Detection de fuite", "item": "https://recherche-fuite-gironde.fr/detection-fuite/" },
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
      "acceptedAnswer": { "@type": "Answer", "text": "Notre methode principale est la thermographie infrarouge : une camera thermique detecte les variations de temperature au sol. Avec le circuit en chauffe, la zone de fuite produit un halo thermique anormal visible a l'ecran. Le test de pression hydraulique sur chaque boucle complete le diagnostic : en isolant les boucles une par une, on identifie celle qui perd de la pression. La combinaison des deux permet une localisation au point en general." }
    },
    {
      "@type": "Question",
      "name": "Quels sont les signes d'une fuite sur plancher chauffant ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Les signes caracteristiques sont : baisse de pression dans le circuit de chauffage sur le manometre, sol anormalement froid par zones (boucle non chauffante), tache d'humidite ou auréole au plafond de l'etage inferieur (en etage), parquet ou carrelage qui se decolle localement, surconsommation d'eau inexpliquee (le circuit se remplit automatiquement), chaudiere qui se met en defaut de pression frequent." }
    },
    {
      "@type": "Question",
      "name": "Combien coute une recherche de fuite sur plancher chauffant a Bordeaux ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Entre 400 et 650 euros HT selon la surface du plancher chauffant et le nombre de boucles a tester. Pour une maison de 80 a 150 m² avec plancher chauffant principal, comptez 450 a 550 euros HT. Le tarif inclut thermographie, test de pression sur chaque boucle, rapport technique avec localisation precise. Devis fixe communique avant intervention." }
    },
    {
      "@type": "Question",
      "name": "La reparation apres diagnostic necessite-t-elle de casser tout le sol ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Non, nous localisons la fuite au point pres, ce qui permet une intervention ciblee. La reparation consiste a ouvrir la chape uniquement au droit de la perforation (zone de 25 a 40 cm de cote typiquement), remplacer 30 a 80 cm de tube PER ou polybutylene, refaire la chape et le revetement de sol localement. Aucun besoin de casser toute la piece." }
    },
    {
      "@type": "Question",
      "name": "Les planchers chauffants a Bordeaux sont-ils frequents ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Oui, particulierement a Merignac, Pessac et dans les pavillons des annees 1985-2005 de la metropole. Environ 40 pourcent des maisons individuelles de cette periode ont un plancher chauffant hydraulique. Apres 20 a 40 ans, les micro-perforations sur tubes PER ou polybutylene deviennent frequentes. Nos techniciens sont specialises sur ce type d'installation." }
    },
    {
      "@type": "Question",
      "name": "La garantie decennale couvre-t-elle mon plancher chauffant ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Si votre installation a moins de 10 ans, la garantie decennale du poseur couvre les defauts de mise en oeuvre et de materiaux. Apres 10 ans, c'est l'assurance habitation multirisque qui prend en charge recherche de fuite et reparation via la garantie degats des eaux. Notre rapport technique est accepte par les principaux assureurs francais." }
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
      <a href="/detection-fuite/">Detection de fuite</a>
      <span>&rsaquo;</span>
      <span>Plancher chauffant Bordeaux</span>
    </nav>
    <h1>Recherche de fuite sur plancher chauffant a Bordeaux</h1>
    <p class="hero-mini-lead">Pression de votre chaudiere qui chute, sol froid par zones, humidite au plafond du voisin du dessous : votre plancher chauffant hydraulique fuit. Nos techniciens le localisent <strong>au point pres grace a la thermographie infrarouge</strong>, sans casser votre chape. Reparation ciblee sur 25 a 40 cm de sol au lieu de refaire toute la piece.</p>
    <div class="hero-mini-cta">
      <a href="/devis/" class="btn btn-gold">Demander un devis plancher chauffant</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <h2>Le plancher chauffant hydraulique : un systeme tres repandu en metropole bordelaise</h2>
    <p>Les pavillons construits a Bordeaux et sa metropole entre 1985 et 2005 ont massivement adopte le plancher chauffant hydraulique comme systeme de chauffage principal. A Merignac (Arlac, Capeyron, Chemin Long, Beutre), a Pessac (Alouette, Saige, Camponac), au Haillan, a Eysines, dans les lotissements de Talence et du Bouscat, environ 40 pourcent des maisons individuelles de cette periode en sont equipees. C'est une proportion nettement superieure aux radiateurs classiques sur ces tranches d'age.</p>

    <p>Le systeme fonctionne par circulation d'eau chaude (35-45 degrees) dans des tubes PER (polyethylene reticulé) ou polybutylene integres dans la chape beton. Chaque piece est alimentee par une ou plusieurs boucles qui partent d'un collecteur central (generalement dans une pièce technique ou un placard). Apres 20 a 40 ans, les micro-perforations et les defaillances de raccordement deviennent frequentes.</p>

    <h2>Les 6 signes d'une fuite de plancher chauffant</h2>

    <div class="grid-3" style="margin-top:1.5rem;">
      <div class="arg-num-card">
        <span class="arg-num">01</span>
        <div class="arg-num-content">
          <h3>Baisse de pression chronique</h3>
          <p>La pression de votre circuit chauffage baisse regulierement sur le manometre de la chaudiere. Vous devez remettre en pression manuellement chaque semaine ou chaque mois. Le circuit perd de l'eau quelque part, presque toujours au niveau du plancher chauffant si c'est votre type d'installation.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">02</span>
        <div class="arg-num-content">
          <h3>Zones de sol froides</h3>
          <p>Une piece ou une zone precise de la maison reste froide malgre le chauffage en marche. Une boucle du plancher chauffant ne circule plus correctement. Posez la main au sol : le contraste thermique entre zones chauffees et zones defaillantes est nettement perceptible.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">03</span>
        <div class="arg-num-content">
          <h3>Tache au plafond (si etage)</h3>
          <p>Pour les maisons a etage avec plancher chauffant a l'etage superieur, une fuite se manifeste par une tache d'humidite ou une auréole au plafond du rez-de-chaussee. Elle peut apparaitre tres localement (au droit exact de la fuite) ou de maniere diffuse (migration de l'eau le long des poutres).</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">04</span>
        <div class="arg-num-content">
          <h3>Parquet ou carrelage qui se decolle</h3>
          <p>Le revetement de sol au-dessus de la zone fuyante montre des signes d'humidite : lame de parquet gonflee, joint de carrelage qui fonce, carrelage qui sonne creux. Ces signes apparaissent souvent des mois avant que la fuite soit clairement identifiee.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">05</span>
        <div class="arg-num-content">
          <h3>Chaudiere en defaut de pression</h3>
          <p>La chaudiere se met en defaut et s'arrete automatiquement, avec un code d'erreur "pression basse" ou equivalent. Cela arrive de plus en plus frequemment. Votre chauffagiste reamorce mais le probleme revient. Le circuit perd de l'eau en permanence par la fuite.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">06</span>
        <div class="arg-num-content">
          <h3>Surconsommation d'eau inexpliquee</h3>
          <p>Le remplissage automatique de votre circuit de chauffage compense en permanence la fuite. Votre compteur d'eau indique une surconsommation sans que vous ne trouviez de point d'eau responsable. C'est la fuite du plancher chauffant qui alimente une fuite d'eau continue dans le sol.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:1080px;">
    <h2>Notre methode : thermographie + test de pression</h2>
    <p>La recherche de fuite sur plancher chauffant hydraulique est notre specialite sur la metropole bordelaise. Nous combinons deux methodes complementaires pour localiser la fuite au point pres sans casser la chape.</p>

    <h3>Etape 1 : preparation du circuit</h3>
    <p>Avant notre arrivee, maintenez votre chauffage en fonctionnement normal pendant au moins 4 heures. Le plancher doit etre a temperature operationnelle pour que la thermographie revele les contrastes thermiques caracteristiques.</p>

    <h3>Etape 2 : thermographie infrarouge du sol</h3>
    <p>Avec une camera thermique haute definition, notre technicien balaie methodiquement la surface des pieces. Une fuite active produit un halo thermique anormal : soit une zone plus chaude (eau chaude qui sort localement sous le revetement) soit une zone plus froide (boucle qui ne circule plus en aval du point de fuite). La lecture experte de ces signatures thermiques permet de pointer la zone a 20-30 cm pres.</p>

    <h3>Etape 3 : identification de la boucle en defaut</h3>
    <p>Au collecteur, chaque boucle alimentant une piece est identifiee. Nous isolons les boucles une par une en fermant les vannes manuelles, et mesurons la pression residuelle dans chacune apres un delai de stabilisation. La boucle qui perd de la pression en isolement est celle qui fuit.</p>

    <h3>Etape 4 : test de pression cible sur la boucle suspecte</h3>
    <p>Avec la boucle suspecte identifiee, nous effectuons un test de pression plus precis avec manometre haute sensibilite. En combinaison avec la thermographie, cela confirme la zone exacte dans la boucle (debut, milieu, fin de la boucle, serpentin chauffant).</p>

    <h3>Etape 5 : marquage et rapport</h3>
    <p>Le point de fuite est marque au sol (scotch ou feutre effacable). Le rapport technique detaille les mesures effectuees, la zone localisee en coordonnees cartesiennes par rapport aux murs, et la preconisation de reparation : ouverture de chape 25-40 cm de cote, remplacement de 30-80 cm de tube, refection chape et revetement.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <h2>Causes frequentes des fuites sur plancher chauffant</h2>

    <div class="grid-3" style="margin-top:1.5rem;">
      <div class="arg-num-card">
        <span class="arg-num">01</span>
        <div class="arg-num-content">
          <h3>Micro-perforation par corrosion interne</h3>
          <p>Les tubes PER des annees 1985-1995 peuvent subir une corrosion interne lente si l'eau du circuit n'a pas ete correctement traitee (absence d'inhibiteur de corrosion). La perforation est souvent punctiforme (0,2 a 1 mm) mais suffit a provoquer une perte de pression continue.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">02</span>
        <div class="arg-num-content">
          <h3>Perforation par clou ou vis</h3>
          <p>Lors de travaux ulterieurs (pose de plinthe, fixation d'un meuble, installation d'une cloison), un clou ou une vis peut perforer le tube. La fuite apparait quelques semaines ou mois plus tard. Cas tres frequent dans les maisons avec historique de reamenagements.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">03</span>
        <div class="arg-num-content">
          <h3>Defaut de raccordement au collecteur</h3>
          <p>Le raccordement entre la boucle et le collecteur (sertissage, collier de serrage) peut lacher par fatigue apres 15 a 25 ans. Cette fuite est souvent visible dans le placard du collecteur si on regarde attentivement.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">04</span>
        <div class="arg-num-content">
          <h3>Mouvement de la chape</h3>
          <p>Un mouvement du support (tassement, fissure de la dalle, mouvement de terrain argileux bordelais) peut cisailler le tube enrobe. Cas moins frequent mais observe sur les maisons anciennes renovees avec plancher chauffant rajoute.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">05</span>
        <div class="arg-num-content">
          <h3>Chocs thermiques repetes</h3>
          <p>Un chauffage pousse regulierement au maximum puis coupe brutalement provoque des dilatations/contractions rapides. Sur 30 ans, cela fatigue les raccords et peut provoquer des fuites aux jonctions.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">06</span>
        <div class="arg-num-content">
          <h3>Polybutylene de la generation 1990</h3>
          <p>Certains lots de tubes polybutylene des annees 1990 ont ete rappeles pour defaut de fabrication. Si votre installation date de cette periode et que vous avez des fuites multiples, un changement complet peut etre plus economique a terme qu'une succession de reparations.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Cas type d'intervention a Merignac</h2>
    <p>Scenario recurrent : pavillon Merignac Arlac construit en 1992, plancher chauffant hydraulique sur rez-de-chaussee (80 m²). Le proprietaire constate depuis 6 mois que la pression de sa chaudiere baisse de 1,5 a 1,0 bar chaque semaine. Il doit reamorcer manuellement. Depuis 2 mois, le salon reste anormalement froid alors que la chambre et la cuisine sont bien chauffees. Sa facture d'eau a augmente de 8 m³ par mois.</p>

    <p>Notre intervention : thermographie infrarouge systematique du sol, boucle par boucle. La boucle salon (42 m lineaires de tube PER dans une serpentin) montre un contraste thermique caracteristique a 4,2 metres du mur nord et 2,8 metres du mur est : zone froide nette au-dela de ce point, preuve que la fuite est localisee la. Test de pression sur cette boucle : perte confirmee de 0,3 bar en 30 minutes en isolement.</p>

    <p>Reparation : ouverture de chape 35×35 cm au point marque, decouverte d'une micro-perforation sur le tube PER a 38 cm de profondeur, remplacement de 60 cm de tube avec raccords mecaniques certifies, refection chape avec mortier fibre, repose du carrelage d'origine (conservé lors de l'ouverture). Duree totale intervention + reparation : 2 jours. Cout total : 1 800 euros HT. Pris en charge a 70 pourcent par l'assurance multirisque habitation apres examen du rapport et devis.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Questions frequentes sur la fuite de plancher chauffant a Bordeaux</h2>

    <h3>Comment detectez-vous une fuite sur un plancher chauffant sans casser la chape ?</h3>
    <p>Notre methode principale est la thermographie infrarouge : une camera thermique detecte les variations de temperature au sol. Avec le circuit en chauffe, la zone de fuite produit un halo thermique anormal. Le test de pression hydraulique sur chaque boucle complete le diagnostic. La combinaison des deux permet une localisation au point en general.</p>

    <h3>Quels sont les signes d'une fuite sur plancher chauffant ?</h3>
    <p>Baisse de pression chronique sur le manometre, sol anormalement froid par zones, tache d'humidite au plafond de l'etage inferieur (en etage), parquet ou carrelage qui se decolle localement, surconsommation d'eau inexpliquee, chaudiere en defaut de pression frequent.</p>

    <h3>Combien coute une recherche de fuite sur plancher chauffant a Bordeaux ?</h3>
    <p>Entre 400 et 650 euros HT selon la surface et le nombre de boucles a tester. Pour une maison de 80 a 150 m² avec plancher chauffant principal, comptez 450 a 550 euros HT. Le tarif inclut thermographie, test de pression sur chaque boucle, rapport technique avec localisation precise.</p>

    <h3>La reparation apres diagnostic necessite-t-elle de casser tout le sol ?</h3>
    <p>Non, nous localisons la fuite au point pres, ce qui permet une intervention ciblee. La reparation consiste a ouvrir la chape uniquement au droit de la perforation (zone de 25 a 40 cm de cote typiquement), remplacer 30 a 80 cm de tube, refaire la chape et le revetement de sol localement.</p>

    <h3>Les planchers chauffants a Bordeaux sont-ils frequents ?</h3>
    <p>Oui, particulierement a Merignac, Pessac et dans les pavillons des annees 1985-2005. Environ 40 pourcent des maisons individuelles de cette periode ont un plancher chauffant hydraulique. Apres 20 a 40 ans, les micro-perforations deviennent frequentes. Pour une intervention specifique a votre ville, consultez <a href="/villes/merignac/" style="color:var(--green);text-decoration:underline;">recherche de fuite Merignac</a> ou <a href="/villes/pessac/" style="color:var(--green);text-decoration:underline;">recherche de fuite Pessac</a>.</p>

    <h3>La garantie decennale couvre-t-elle mon plancher chauffant ?</h3>
    <p>Si votre installation a moins de 10 ans, la garantie decennale du poseur couvre les defauts. Apres 10 ans, c'est l'assurance habitation multirisque qui prend en charge recherche de fuite et reparation via la garantie degats des eaux. Notre rapport technique est accepte par les principaux assureurs.</p>

    <div style="margin-top:2rem;text-align:center;">
      <a href="/devis/" class="btn btn-gold">Demander un diagnostic plancher chauffant</a>
    </div>
  </div>
</section>

{form_section("Bordeaux")}
'''

    return html_base(
        'Fuite plancher chauffant Bordeaux | Thermographie sans casse',
        "Recherche de fuite sur plancher chauffant hydraulique a Bordeaux et sa metropole : thermographie infrarouge, test de pression, localisation au point sans casser la chape.",
        'https://recherche-fuite-gironde.fr/detection-fuite/fuite-plancher-chauffant-bordeaux/',
        body,
        extra_ld=ld_service + ld_local + ld_breadcrumb + ld_faq,
    )


# ═══════════════════════════════════════════════════════════════
# PAGE USE CASE : Degats des eaux Bordeaux (B2B syndics)
# ═══════════════════════════════════════════════════════════════

def page_degats_eaux_bordeaux():
    ld_service = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "Recherche d'origine de degat des eaux",
  "name": "Localisation de degat des eaux a Bordeaux pour syndics et copropriétés",
  "description": "Identification precise de l'origine d'un degat des eaux en copropriete bordelaise. Rapport technique opposable en convention IRSI, intervention sous 24h, coordination avec assureurs et syndic.",
  "provider": {
    "@type": "LocalBusiness",
    "name": "Recherche Fuite Gironde",
    "url": "https://recherche-fuite-gironde.fr/"
  },
  "areaServed": { "@type": "Place", "name": "Bordeaux et metropole girondine" },
  "audience": {
    "@type": "BusinessAudience",
    "audienceType": "Syndics de copropriete, conseils syndicaux, gestionnaires immobiliers"
  },
  "category": "Detection de fuite non destructive B2B"
}
</script>'''

    ld_local = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Recherche Fuite Gironde - Degats des eaux Bordeaux",
  "description": "Specialiste de la localisation d'origine de degat des eaux en copropriete a Bordeaux. Rapport IRSI, intervention 24h, coordination syndic et assureur.",
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
    { "@type": "ListItem", "position": 2, "name": "Detection de fuite", "item": "https://recherche-fuite-gironde.fr/detection-fuite/" },
    { "@type": "ListItem", "position": 3, "name": "Degat des eaux Bordeaux", "item": "https://recherche-fuite-gironde.fr/detection-fuite/degats-des-eaux-bordeaux/" }
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
      "name": "Quelle est la difference entre une fuite et un degat des eaux ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Une fuite est la cause technique : perforation, joint defaillant, raccord desaxe, liner percé. Un degat des eaux est la consequence : tache d'humidite, plafond abîme, parquet gonfle, mobilier endommage. Un degat des eaux implique toujours une fuite à l'origine, mais toutes les fuites n'entraînent pas de degat des eaux (fuite enterree dans le jardin par exemple). Pour l'assurance, c'est le degat des eaux qui declenche la prise en charge." }
    },
    {
      "@type": "Question",
      "name": "Comment fonctionne la convention IRSI en copropriete bordelaise ?",
      "acceptedAnswer": { "@type": "Answer", "text": "La convention IRSI (Indemnisation et Recours des Sinistres Immeuble) s'applique automatiquement entre assureurs pour les degats des eaux en copropriete jusqu'a 5000 euros HT. L'assureur du lot ou du logement 'victime' prend en charge les dommages sans recherche de responsabilite prealable, puis se retourne contre l'assureur du responsable. Cette procedure accelere considerablement l'indemnisation (15 a 30 jours typiquement au lieu de 3 a 6 mois en expertise contradictoire)." }
    },
    {
      "@type": "Question",
      "name": "Un syndic peut-il mandater directement votre intervention ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Oui, nous travaillons regulierement en mandatement direct par syndic professionnel ou conseil syndical pour les degats des eaux en copropriete bordelaise. Le rapport est remis au syndic avec identification precise de la responsabilite (partie privative ou commune). La facturation se fait a la copropriete, qui se retourne ensuite vers l'assurance PNO ou le responsable identifie." }
    },
    {
      "@type": "Question",
      "name": "Combien de temps prend un diagnostic de degat des eaux a Bordeaux ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Intervention sous 24h dans la majorite des cas, avec un diagnostic sur site de 1h30 a 3h. Le rapport technique est remis le jour meme ou sous 24h par email, pret a etre transmis a l'assureur et au syndic. Pour les sinistres complexes impactant plusieurs lots, un diagnostic plus long (demi-journee) peut etre necessaire avec rapport detaille sous 48h." }
    },
    {
      "@type": "Question",
      "name": "Les proprietaires occupants ou les locataires peuvent-ils nous contacter directement ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Oui, tout copropriétaire occupant, locataire ou bailleur peut nous contacter pour un diagnostic individuel. Si le sinistre concerne des parties communes (colonne montante, evacuation collective, toiture), nous informons le syndic apres constat et coordonnons la suite. Le rapport est remis au commanditaire (vous) avec les elements utiles pour l'assureur et le syndic." }
    },
    {
      "@type": "Question",
      "name": "Que faire en attendant l'arrivee du technicien ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Coupez l'arrivee d'eau generale si vous pouvez identifier la source. Prevenez le voisin du dessus ou du dessous si le degat les impacte. Photographiez les dommages des que possible (avant sechage et reparations). Declarez le sinistre a votre assurance dans les 5 jours ouvrables (convention IRSI s'applique des la declaration). Eloignez meubles et objets de valeur de la zone humide pour limiter les degats secondaires." }
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
      <a href="/detection-fuite/">Detection de fuite</a>
      <span>&rsaquo;</span>
      <span>Degats des eaux Bordeaux</span>
    </nav>
    <h1>Recherche d'origine de degat des eaux a Bordeaux</h1>
    <p class="hero-mini-lead">Tache au plafond, infiltration dans un appartement, humidite persistante en copropriete bordelaise ? Nos techniciens identifient precisement l'origine du sinistre pour activer la convention IRSI entre assureurs. <strong>Rapport opposable remis sous 24h</strong>, coordination avec syndic et compagnies d'assurance, intervention prioritaire.</p>
    <div class="hero-mini-cta">
      <a href="/devis/" class="btn btn-gold">Demander une intervention</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <figure style="margin:0 0 2rem;">
      <img src="/assets/fuite-sous-dalle.webp" alt="Degat des eaux en copropriete bordelaise, tache d'humidite au plafond, intervention recherche d'origine" width="700" height="467" loading="eager" style="width:100%;max-height:380px;height:auto;object-fit:cover;border-radius:12px;display:block;">
    </figure>

    <h2>Fuite ou degat des eaux : une distinction essentielle pour l'assurance</h2>
    <p>Un degat des eaux n'est pas une fuite : c'est la consequence d'une fuite. Cette distinction, apparemment semantique, est en realite essentielle car elle conditionne la procedure d'indemnisation et la responsabilite entre assureurs. Comprendre cette logique aide a anticiper la suite d'un sinistre en copropriete bordelaise.</p>

    <ul>
      <li><strong>La fuite</strong> est la cause technique : perforation d'une canalisation, joint de skimmer fissure, raccord PVC desaxe, liner piscine percé, soudure d'etancheite rompue</li>
      <li><strong>Le degat des eaux</strong> est le dommage resultant : plafond tache, parquet gonfle, enduit decolle, mobilier abime, appareils electromenagers hors d'usage</li>
      <li><strong>Le sinistre</strong> est la declaration administrative faite a l'assureur, combinant l'evenement et l'impact financier</li>
    </ul>

    <p>Dans 80 pourcent des cas, quand un proprietaire nous appelle en urgence pour un degat des eaux, il n'a aucune idee de la cause : la tache au plafond peut venir d'une fuite sur la colonne commune EU/EV, d'une infiltration de toiture, d'une canalisation encastree, d'un appareil du voisin. C'est precisement notre role d'identifier la source technique pour que l'assurance puisse etablir les responsabilites.</p>

    <h2>Types de degats des eaux que nous traitons en copropriete bordelaise</h2>

    <div class="grid-3" style="margin-top:1.5rem;">
      <div class="arg-num-card">
        <span class="arg-num">01</span>
        <div class="arg-num-content">
          <h3>Infiltration par colonne montante</h3>
          <p>La tache apparait au plafond ou le long d'un mur porteur. La colonne EU/EV commune a l'etage superieur fuit, provoquant un ecoulement ponctuel ou diffus selon le debit. Frequente dans les immeubles haussmanniens du Centre-Ville, Chartrons et Saint-Pierre ou les colonnes fonte centenaires cedent a la corrosion.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">02</span>
        <div class="arg-num-content">
          <h3>Degat par appartement du dessus</h3>
          <p>Fuite sur installation privative de l'appartement du dessus : flexible de machine a laver, chasse d'eau qui deborde, robinet oublie ouvert, joint de baignoire rompu. Le voisin est souvent responsable mais ne s'en rend pas compte. La convention IRSI s'applique automatiquement jusqu'a 5000 euros HT.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">03</span>
        <div class="arg-num-content">
          <h3>Infiltration de toiture</h3>
          <p>Apres pluies abondantes, de l'eau coule au dernier etage : toiture defectueuse, chéneaux bouches, etancheite de terrasse rompue. Responsabilite copropriete (parties communes). Frequent dans les immeubles des Chartrons, de la Victoire et de la Bastide apres forts episodes pluvieux.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">04</span>
        <div class="arg-num-content">
          <h3>Fuite encastree dans cloison</h3>
          <p>Tache le long d'un mur ou d'une cloison, souvent en salle de bain ou cuisine. Canalisation encastree percee par chute d'objet, vis malencontreuse, corrosion. La localisation par thermographie et ecoute evite la demolition de toute la cloison.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">05</span>
        <div class="arg-num-content">
          <h3>Debordement de gouttiere</h3>
          <p>Gouttiere obstrue par feuilles mortes, debordement sur facade, infiltration dans maconnerie. Frequent dans les immeubles de caudéran et du Parc Bordelais entoures d'arbres. Responsabilite entretien copropriete (contrat nettoyage gouttieres annuel).</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">06</span>
        <div class="arg-num-content">
          <h3>Remontee capillaire confondue</h3>
          <p>Attention aux faux positifs : certaines humidités en sous-sol bordelais ne sont pas des fuites mais des remontees capillaires du terrain argileux. Notre humidimetre distingue precisement une infiltration active (gradient fort, zone localisee) d'une humidite diffuse structurelle.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:1080px;">
    <h2>Convention IRSI : le cadre legal pour les degats des eaux en copropriete</h2>
    <p>Depuis 2018, la convention IRSI (Indemnisation et Recours des Sinistres Immeuble) encadre les degats des eaux en copropriete et en location. Cette convention simplifie considerablement la procedure, a condition de connaître ses regles.</p>

    <h3>Le seuil des 5 000 euros HT</h3>
    <p>Pour les sinistres dont le cout de reparation est inferieur à 5 000 euros HT, la convention IRSI s'applique automatiquement : l'assureur du lot victime indemnise sans recherche de responsabilite prealable. Au-dela de 5 000 euros, une expertise contradictoire peut etre declenchee pour etablir les responsabilites.</p>

    <h3>Les conditions d'application</h3>
    <ul>
      <li>Le sinistre doit concerner au moins 2 lots de la copropriete OU 1 lot + parties communes</li>
      <li>L'origine doit etre dans l'immeuble (pas dans une construction voisine)</li>
      <li>Le sinistre doit etre declare a l'assureur sous 5 jours ouvrables</li>
      <li>Un rapport technique doit identifier la cause (notre prestation)</li>
    </ul>

    <h3>Les acteurs et leurs responsabilites</h3>
    <ul>
      <li><strong>Syndic</strong> : mandate le diagnostic si parties communes concernees, coordonne la procedure IRSI</li>
      <li><strong>Proprietaire occupant ou bailleur</strong> : declare le sinistre a son assureur, facilite l'acces</li>
      <li><strong>Locataire</strong> : declare a son assureur multirisque habitation, informe son bailleur</li>
      <li><strong>Assureurs de chaque lot</strong> : echanges automatiques via la plateforme IRSI</li>
      <li><strong>Professionnel de la recherche de fuite (nous)</strong> : identifie la cause, remet un rapport opposable</li>
    </ul>

    <h3>Notre rapport technique et la convention IRSI</h3>
    <p>Notre rapport standardise pour sinistre IRSI comprend obligatoirement : date et heure du constat, methodes de diagnostic employees (thermographie, gaz traceur, acoustique, humidimetre), photos datees et horodatees, localisation precise de la source (lot responsable ou parties communes), estimation du debit de fuite et de la duree probable, preconisations de reparation chiffrees, elements de coordination entre assureurs. Ce document est reconnu par tous les assureurs de la place, y compris MAAF, Allianz, AXA, Groupama, Matmut, MACIF, MMA, GMF, SMABTP.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <h2>Notre protocole pour les syndics et conseils syndicaux</h2>
    <p>Nous travaillons regulierement en mandatement par syndic professionnel, association syndicale libre (ASL) ou conseil syndical. Notre protocole est adapte aux contraintes B2B de la gestion de copropriete.</p>

    <div class="grid-3" style="margin-top:1.5rem;">
      <div class="arg-num-card">
        <span class="arg-num">01</span>
        <div class="arg-num-content">
          <h3>Mandatement direct</h3>
          <p>Le syndic nous mandate par email ou telephone, avec les references du sinistre (numero de dossier interne, lots concernes, assureur de la copropriete). Devis fixe communique sous l'heure pour validation.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">02</span>
        <div class="arg-num-content">
          <h3>Coordination avec les lots</h3>
          <p>Nous prenons directement contact avec les proprietaires ou locataires des lots concernes pour planifier l'acces. Creneau souvent en journee, avec disponibilite du syndic ou du gardien si access parties communes.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">03</span>
        <div class="arg-num-content">
          <h3>Diagnostic sur site</h3>
          <p>Intervention d'1h30 a 3h selon la complexite. Nos techniciens sont formes a respecter la confidentialite des occupants, les finitions des appartements, la discretion dans les parties communes (pas de travaux genants, pas de bruit excessif).</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">04</span>
        <div class="arg-num-content">
          <h3>Rapport standardise IRSI</h3>
          <p>Rapport technique conforme aux exigences des assureurs, remis au syndic sous 24h. Format PDF avec photos datees, localisation precise, chronologie des constatations, recommandations de reparation.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">05</span>
        <div class="arg-num-content">
          <h3>Facturation a la copropriete</h3>
          <p>Facture emise au nom de la copropriete (syndicat des copropriétaires, numéro SIRET) avec les references du dossier IRSI. Paiement sous 30 jours apres reception. Aucun acompte demande.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">06</span>
        <div class="arg-num-content">
          <h3>Suivi post-intervention</h3>
          <p>Nous restons disponibles pour repondre aux questions de l'expert mandate par l'assurance, produire des complements de rapport si necessaire, temoigner en cas de contentieux. Support gratuit dans la limite de 6 mois apres l'intervention.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Cas type : degat des eaux en immeuble haussmannien</h2>
    <p>Scenario recurrent sur Bordeaux Centre : immeuble haussmannien de la rue Sainte-Catherine, 6 lots sur 5 etages. Mme X au 3e etage signale au syndic une tache d'humidite en expansion sur le plafond de sa chambre, avec ecoulement visible apres fortes chutes d'eau. Le voisin du dessus (M. Y, 4e etage) affirme ne rien constater chez lui. Le syndic nous mandate sous 24h.</p>

    <p>Notre intervention : thermographie infrarouge au plafond du 3e pour cartographier la zone humide, ecoute electro-acoustique sur le tracé de la colonne d'evacuation EU/EV passant dans la cloison mitoyenne, camera endoscopique dans la gaine technique commune via le regard d'acces du palier. Decouverte : fissure sur la colonne fonte commune entre le 3e et le 4e etage, a 1,50 metres au-dessus du plafond de Mme X. Responsabilite copropriete, ni Mme X ni M. Y ne sont directement en cause.</p>

    <p>Rapport transmis au syndic en 24h. L'assurance de la copropriete prend en charge la reparation (remplacement du troncon de colonne, environ 2 800 euros HT). L'assurance multirisque de Mme X prend en charge les dommages dans son logement (repeinture plafond + nettoyage mobilier, 1 400 euros HT) dans le cadre de la convention IRSI. Delai total resolution : 6 semaines entre notre intervention et la fin des reparations.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Questions frequentes sur les degats des eaux a Bordeaux</h2>

    <h3>Quelle est la difference entre une fuite et un degat des eaux ?</h3>
    <p>Une fuite est la cause technique : perforation, joint defaillant, raccord desaxe, liner perce. Un degat des eaux est la consequence : tache d'humidite, plafond abîme, parquet gonfle, mobilier endommage. Un degat des eaux implique toujours une fuite à l'origine, mais toutes les fuites n'entraînent pas de degat des eaux (fuite enterree dans le jardin par exemple). Pour l'assurance, c'est le degat des eaux qui declenche la prise en charge.</p>

    <h3>Comment fonctionne la convention IRSI en copropriete bordelaise ?</h3>
    <p>La convention IRSI s'applique automatiquement entre assureurs pour les degats des eaux en copropriete jusqu'a 5 000 euros HT. L'assureur du lot 'victime' prend en charge les dommages sans recherche de responsabilite prealable, puis se retourne contre l'assureur du responsable. Cette procedure accelere considerablement l'indemnisation (15 a 30 jours typiquement au lieu de 3 a 6 mois en expertise contradictoire).</p>

    <h3>Un syndic peut-il mandater directement votre intervention ?</h3>
    <p>Oui, nous travaillons regulierement en mandatement direct par syndic professionnel ou conseil syndical. Le rapport est remis au syndic avec identification precise de la responsabilite (partie privative ou commune). La facturation se fait a la copropriete, qui se retourne ensuite vers l'assurance PNO ou le responsable identifie.</p>

    <h3>Combien de temps prend un diagnostic de degat des eaux a Bordeaux ?</h3>
    <p>Intervention sous 24h dans la majorite des cas, avec un diagnostic sur site de 1h30 a 3h. Le rapport technique est remis le jour meme ou sous 24h par email, pret a etre transmis a l'assureur et au syndic. Pour les sinistres complexes impactant plusieurs lots, un diagnostic plus long (demi-journee) peut etre necessaire avec rapport detaille sous 48h.</p>

    <h3>Les proprietaires occupants ou les locataires peuvent-ils nous contacter directement ?</h3>
    <p>Oui, tout copropriétaire occupant, locataire ou bailleur peut nous contacter pour un diagnostic individuel. Si le sinistre concerne des parties communes (colonne montante, evacuation collective, toiture), nous informons le syndic apres constat et coordonnons la suite. Le rapport est remis au commanditaire avec les elements utiles pour l'assureur et le syndic.</p>

    <h3>Que faire en attendant l'arrivee du technicien ?</h3>
    <p>Coupez l'arrivee d'eau generale si vous pouvez identifier la source. Prevenez le voisin du dessus ou du dessous si le degat les impacte. Photographiez les dommages des que possible. Declarez le sinistre a votre assurance dans les 5 jours ouvrables. Pour les situations d'urgence avec fuite active, consultez notre page <a href="/detection-fuite/urgence-bordeaux/" style="color:var(--green);text-decoration:underline;">urgence fuite d'eau Bordeaux</a>.</p>

    <div style="margin-top:2rem;text-align:center;">
      <a href="/devis/" class="btn btn-gold">Demander une intervention syndic</a>
    </div>
  </div>
</section>

{form_section("Bordeaux")}
'''

    return html_base(
        'Degat des eaux Bordeaux | Localisation origine pour syndics IRSI',
        "Recherche d'origine de degat des eaux a Bordeaux en copropriete : rapport IRSI opposable, coordination syndic et assureur, intervention 24h. Pour syndics et proprietaires.",
        'https://recherche-fuite-gironde.fr/detection-fuite/degats-des-eaux-bordeaux/',
        body,
        extra_ld=ld_service + ld_local + ld_breadcrumb + ld_faq,
    )


# ═══════════════════════════════════════════════════════════════
# PAGE USE CASE : Chemisage Bordeaux landing (copropriete)
# ═══════════════════════════════════════════════════════════════

def page_chemisage_bordeaux():
    ld_service = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "Chemisage de canalisation",
  "name": "Chemisage de canalisation en copropriete a Bordeaux",
  "description": "Renovation de canalisations sans tranchee pour copropriétés bordelaises. Chemisage tubulaire par resine epoxy, durée de vie 50 ans, garantie decennale. Specialistes des immeubles haussmanniens et bati ancien.",
  "provider": {
    "@type": "LocalBusiness",
    "name": "Recherche Fuite Gironde",
    "url": "https://recherche-fuite-gironde.fr/"
  },
  "areaServed": { "@type": "Place", "name": "Bordeaux et metropole girondine" },
  "category": "Rehabilitation de canalisation sans tranchee"
}
</script>'''

    ld_local = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Recherche Fuite Gironde - Chemisage Bordeaux",
  "description": "Specialiste du chemisage de canalisation en copropriete a Bordeaux. Immeubles haussmanniens, syndics, vote AG, sans tranchee, garantie decennale.",
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
      "name": "Quel est le cout moyen d'un chemisage de colonne en copropriete bordelaise ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Le chemisage d'une colonne d'evacuation EU/EV en copropriete coute en moyenne 400 a 700 euros HT par metre lineaire selon le diametre (63 a 160 mm typiquement), la hauteur de l'immeuble, l'accessibilite des regards techniques. Pour un immeuble haussmannien de 5 etages avec colonne de 15 metres, comptez 6 000 a 10 500 euros HT, a comparer avec un remplacement classique a 15 000-25 000 euros HT (demolition + reconstruction)." }
    },
    {
      "@type": "Question",
      "name": "Le chemisage se vote-t-il en AG ordinaire ou extraordinaire ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Les travaux de chemisage sur parties communes se votent en AG ordinaire a la majorite de l'article 25 (majorite absolue des voix de tous les copropriétaires, presents, représentés ou absents). Si le vote article 25 echoue mais recueille au moins un tiers des voix, un second vote immediat a la majorite simple de l'article 24 peut etre organise lors de la meme AG. La procedure est bien rodée en copropriete bordelaise et ne necessite generalement pas d'AG extraordinaire." }
    },
    {
      "@type": "Question",
      "name": "Le chemisage est-il compatible avec les immeubles UNESCO de Bordeaux ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Oui. Le chemisage est realise a l'interieur des canalisations existantes sans modification de l'aspect exterieur ni ouverture de murs visibles. Aucune autorisation d'urbanisme ni avis de l'Architecte des Batiments de France n'est necessaire pour cette intervention. C'est meme la technique privilegiee pour les immeubles classés UNESCO du Port de la Lune (Triangle d'Or, cours de l'Intendance, place Gambetta) ou toute modification exterieure est strictement encadrée." }
    },
    {
      "@type": "Question",
      "name": "Combien de temps dure un chantier de chemisage sur colonne de 15 metres ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Un chantier de chemisage sur une colonne typique d'immeuble bordelais (15 a 25 metres, diametre 90 a 125 mm) dure 2 a 4 jours, avec coupure d'eau sur la colonne uniquement pendant les heures de polymerisation (6 a 10 heures). Les appartements restent occupes pendant le chantier, les coupures sont coordonnees avec les habitants via affichage dans les parties communes." }
    },
    {
      "@type": "Question",
      "name": "Quelle est la garantie sur un chemisage tubulaire en Gironde ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Le chemisage tubulaire est couvert par la garantie decennale obligatoire sur les travaux de batiment. La duree de vie estimee du liner resine epoxy est de 50 ans dans des conditions normales d'utilisation. Un rapport de fin de chantier avec controle camera est remis au syndic, a annexer au carnet d'entretien obligatoire de l'immeuble (loi ALUR)." }
    },
    {
      "@type": "Question",
      "name": "Intervenez-vous sur les immeubles anciens avec canalisations en plomb ou fonte ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Oui, le chemisage est parfaitement adapte aux canalisations fonte grise (majoritaire dans les immeubles bordelais d'avant 1975), galvanise et meme plomb (interdit depuis 1995 mais encore present dans certaines colonnes non renovées). La technique consiste a creer un nouveau tuyau resine a l'interieur de l'ancien, rendant obsolete le materiau d'origine sans avoir a le demonter." }
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
    <h1>Chemisage de canalisation a Bordeaux et metropole</h1>
    <p class="hero-mini-lead">Renovation des colonnes d'evacuation et canalisations vieillissantes des immeubles bordelais, <strong>sans tranchee ni demolition</strong>. Liner tubulaire en resine epoxy insere dans la canalisation existante, durée de vie 50 ans, garantie decennale. Specialistes des copropriétés haussmanniennes et immeubles classes UNESCO.</p>
    <div class="hero-mini-cta">
      <a href="/devis/" class="btn btn-gold">Demander un devis chemisage</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <h2>Pourquoi le chemisage est la solution pour les immeubles bordelais</h2>
    <p>Le parc immobilier historique de Bordeaux (Triangle d'Or, Chartrons, Saint-Pierre, place Gambetta) compte une part significative d'immeubles haussmanniens construits entre 1830 et 1910. Ces batiments abritent des colonnes d'evacuation EU/EV en fonte grise d'origine, parfois centenaires, dont l'etat se degrade progressivement par corrosion interne. Les fuites multiples deviennent une problematique majeure apres 100 a 120 ans de service.</p>

    <p>Face a cette usure structurelle, la reponse traditionnelle etait le remplacement complet : ouverture des gaines, depose des anciennes canalisations, pose de nouveaux tuyaux, rebouchage et finition. Sur un immeuble de 5 a 6 etages, ce type de travaux dure 3 a 8 semaines, coute 15 000 a 30 000 euros, et implique le logement en chantier des copropriétaires concernes. Le chemisage tubulaire permet d'obtenir le meme resultat technique (colonne etanche durable 50 ans) en 2 a 4 jours, pour 30 a 50 pourcent moins cher, sans aucune demolition.</p>

    <h2>Les immeubles bordelais typiquement concernés</h2>

    <div class="grid-3" style="margin-top:1.5rem;">
      <div class="arg-num-card">
        <span class="arg-num">01</span>
        <div class="arg-num-content">
          <h3>Haussmanniens du Triangle d'Or</h3>
          <p>Immeubles classes UNESCO du Port de la Lune (allees de Tourny, cours de l'Intendance, allees Damour). Colonnes fonte grise d'origine, finitions interieures precieuses (parquets Versailles, moulures, cheminees marbre). Le chemisage preserve integralement ces elements patrimoniaux.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">02</span>
        <div class="arg-num-content">
          <h3>Copropriétés des Chartrons</h3>
          <p>Anciens entrepôts viticoles reconvertis en logements dans les annees 1980-2000, colonnes d'evacuation modernisees en PVC mais raccorde sur reseau fonte d'origine en sous-sol. Points de raccordement fragilizes, cedant apres 30-40 ans d'usage.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">03</span>
        <div class="arg-num-content">
          <h3>Residences des annees 1960-80</h3>
          <p>Grands ensembles de Meriadeck, Bacalan, Benauge, Grand Parc : colonnes EU/EV en fonte grise industrielle qui commencent a ceder aux joints et aux raccords apres 50 a 60 ans. Le chemisage est parfaitement adapte aux grandes sections (100-160 mm) typiques de ces immeubles.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">04</span>
        <div class="arg-num-content">
          <h3>Echoppes bordelaises</h3>
          <p>Echoppes traditionnelles de Saint-Genes, Caudéran, Saint-Augustin avec reseau d'evacuation historique en fonte ou gres vitrifie. Le chemisage permet de renover ces reseaux sans casser les carrelages ciment et parquets point de Hongrie typiques.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">05</span>
        <div class="arg-num-content">
          <h3>Immeubles contemporains Bassins a Flot</h3>
          <p>Rare mais possible : les immeubles recents (2005-2015) avec defauts de pose sur certains raccords PVC. Le chemisage peut intervenir de maniere ciblee sur le troncon defaillant sans changer toute la colonne.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">06</span>
        <div class="arg-num-content">
          <h3>Reseaux enterres en cour interieure</h3>
          <p>De nombreux immeubles bordelais ont des reseaux d'evacuation enterres sous la cour interieure, accessibles uniquement par regards techniques. Le chemisage sans tranchee est ici quasi-obligatoire car la demolition serait irrealisable sans impact lourd sur l'immeuble.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:1080px;">
    <h2>Le chemisage en copropriete : procedure AG et vote</h2>
    <p>Le chemisage sur parties communes (colonnes d'evacuation EU/EV, canalisations d'alimentation generale, reseaux enterres) releve du vote en assemblee generale des copropriétaires. Voici le parcours complet d'un projet chemisage, typique a Bordeaux.</p>

    <h3>Etape 1 : signalement et pre-diagnostic</h3>
    <p>Le syndic reçoit plusieurs signalements de fuites recurrentes dans la meme zone de l'immeuble (plafonds tachés au 3e et 4e etage, par exemple). Il commande un pre-diagnostic par recherche de fuite non destructive (notre prestation). Notre rapport etablit la cause : colonne fonte fatiguee, fuites multiples sur 4 etages, reparation ponctuelle non durable.</p>

    <h3>Etape 2 : devis chemisage et preparation AG</h3>
    <p>Le syndic demande plusieurs devis (au moins 2 obligatoires selon la loi). Notre devis chemisage chiffre precisement le lineaire a traiter, la technique retenue (polymerisation UV ou vapeur), les garanties, le planning. Le devis est inscrit a l'ordre du jour de la prochaine AG ordinaire avec toute la documentation technique.</p>

    <h3>Etape 3 : vote en assemblee generale ordinaire</h3>
    <p>Les travaux de chemisage sur parties communes se votent a la majorite de l'article 25 (majorite absolue de tous les copropriétaires, presents/représentés/absents). Si le vote article 25 echoue mais recueille au moins un tiers des voix, un second vote immediat a la majorite simple de l'article 24 peut etre organise dans la meme AG. Cette procédure articulée en deux temps evite de repasser par une AG extraordinaire.</p>

    <h3>Etape 4 : signature du marche et planning</h3>
    <p>Apres vote, le syndic signe le marche avec nous. Nous etablissons un planning detaille : date de debut, duree par etape (inspection prealable, hydrocurage de la colonne, pose du liner, polymerisation, controle camera final). Information affichée dans les parties communes au moins 15 jours avant le debut.</p>

    <h3>Etape 5 : chantier en 2 a 5 jours</h3>
    <p>L'intervention respecte l'occupation des logements. Les copropriétaires sont informés des creneaux de coupure d'eau sur la colonne concernée (6 a 10 heures pendant la polymerisation). Les equipes interviennent depuis les parties communes (paliers, caves, cour interieure) sans acces aux appartements, sauf si un regard technique est situé dans un logement privatif.</p>

    <h3>Etape 6 : reception et annexion carnet d'entretien</h3>
    <p>A l'issue du chantier, une inspection camera de controle est realisée et filmée. Le rapport final avec video est remis au syndic, qui l'integre au carnet d'entretien obligatoire de l'immeuble (loi ALUR). La garantie decennale court a partir de cette date de reception.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Tarifs du chemisage en copropriete bordelaise</h2>
    <p>Le cout du chemisage depend principalement du lineaire a traiter, du diametre de la canalisation et de l'accessibilite. Voici les fourchettes applicables a Bordeaux en 2026.</p>

    <table style="width:100%;border-collapse:collapse;margin:1.5rem 0;background:#fff;">
    <thead><tr style="background:#0D3B2E;color:#fff;"><th style="padding:.75rem;text-align:left;border:1px solid #155740;">Configuration</th><th style="padding:.75rem;text-align:left;border:1px solid #155740;">Tarif HT par metre lineaire</th><th style="padding:.75rem;text-align:left;border:1px solid #155740;">Exemple sur 15 metres</th></tr></thead>
    <tbody>
    <tr><td style="padding:.75rem;border:1px solid #D8D4CC;">Petit diametre (50-75 mm)</td><td style="padding:.75rem;border:1px solid #D8D4CC;">300 a 450 €</td><td style="padding:.75rem;border:1px solid #D8D4CC;">4 500 a 6 750 €</td></tr>
    <tr style="background:#F7F6F2;"><td style="padding:.75rem;border:1px solid #D8D4CC;">Diametre moyen (90-125 mm)</td><td style="padding:.75rem;border:1px solid #D8D4CC;">400 a 600 €</td><td style="padding:.75rem;border:1px solid #D8D4CC;">6 000 a 9 000 €</td></tr>
    <tr><td style="padding:.75rem;border:1px solid #D8D4CC;">Grand diametre (150-200 mm)</td><td style="padding:.75rem;border:1px solid #D8D4CC;">550 a 800 €</td><td style="padding:.75rem;border:1px solid #D8D4CC;">8 250 a 12 000 €</td></tr>
    <tr style="background:#F7F6F2;"><td style="padding:.75rem;border:1px solid #D8D4CC;">Reseaux enterres complexes</td><td style="padding:.75rem;border:1px solid #D8D4CC;">700 a 1 000 €</td><td style="padding:.75rem;border:1px solid #D8D4CC;">10 500 a 15 000 €</td></tr>
    </tbody>
    </table>

    <h3>Elements inclus dans le tarif</h3>
    <ul>
    <li>Inspection camera prealable pour validation technique (longueur, etat, points critiques)</li>
    <li>Hydrocurage de la canalisation existante (nettoyage haute pression)</li>
    <li>Fourniture et pose du liner imprégné de resine epoxy certifiée ACS (qualite eau potable)</li>
    <li>Polymerisation in situ (vapeur, eau chaude ou UV selon le cas)</li>
    <li>Rapport camera de controle final</li>
    <li>Garantie decennale sur l'intervention</li>
    </ul>

    <h3>Elements en supplement</h3>
    <ul>
    <li>Acces difficile necessitant echafaudage exterieur (rare, pour cheminees ou descentes de gouttieres)</li>
    <li>Traitement prealable d'obstruction massive (racines, amas de depôts) : facture selon etat</li>
    <li>Modification ponctuelle pour chapes ou passages techniques a adapter</li>
    </ul>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Questions frequentes sur le chemisage a Bordeaux</h2>

    <h3>Quel est le cout moyen d'un chemisage de colonne en copropriete bordelaise ?</h3>
    <p>Le chemisage d'une colonne d'evacuation EU/EV en copropriete coute en moyenne 400 a 700 euros HT par metre lineaire selon le diametre (63 a 160 mm typiquement), la hauteur de l'immeuble, l'accessibilite des regards techniques. Pour un immeuble haussmannien de 5 etages avec colonne de 15 metres, comptez 6 000 a 10 500 euros HT, a comparer avec un remplacement classique a 15 000-25 000 euros HT (demolition + reconstruction).</p>

    <h3>Le chemisage se vote-t-il en AG ordinaire ou extraordinaire ?</h3>
    <p>Les travaux de chemisage sur parties communes se votent en AG ordinaire a la majorite de l'article 25. Si le vote echoue mais recueille au moins un tiers des voix, un second vote immediat a la majorite simple (article 24) peut etre organise dans la meme AG. La procedure est bien rodée et ne necessite generalement pas d'AG extraordinaire.</p>

    <h3>Le chemisage est-il compatible avec les immeubles UNESCO de Bordeaux ?</h3>
    <p>Oui. Le chemisage est realise a l'interieur des canalisations existantes sans modification de l'aspect exterieur ni ouverture de murs visibles. Aucune autorisation d'urbanisme ni avis de l'Architecte des Batiments de France n'est necessaire. C'est meme la technique privilegiee pour les immeubles classés UNESCO du Port de la Lune.</p>

    <h3>Combien de temps dure un chantier de chemisage sur colonne de 15 metres ?</h3>
    <p>Un chantier de chemisage sur une colonne typique d'immeuble bordelais dure 2 a 4 jours, avec coupure d'eau sur la colonne uniquement pendant les heures de polymerisation (6 a 10 heures). Les appartements restent occupes pendant le chantier.</p>

    <h3>Quelle est la garantie sur un chemisage tubulaire en Gironde ?</h3>
    <p>Le chemisage tubulaire est couvert par la garantie decennale obligatoire. La duree de vie estimee du liner resine epoxy est de 50 ans dans des conditions normales d'utilisation. Un rapport de fin de chantier avec controle camera est remis au syndic.</p>

    <h3>Intervenez-vous sur les immeubles anciens avec canalisations en plomb ou fonte ?</h3>
    <p>Oui, le chemisage est parfaitement adapte aux canalisations fonte grise (majoritaire dans les immeubles bordelais d'avant 1975), galvanise et meme plomb. La technique consiste a creer un nouveau tuyau resine a l'interieur de l'ancien. Pour plus de details techniques, consultez notre guide <a href="/guide/chemisage-explication/" style="color:var(--green);text-decoration:underline;">chemisage de canalisation explique</a> ou la page service <a href="/chemisage-canalisation/" style="color:var(--green);text-decoration:underline;">chemisage en Gironde</a>.</p>

    <div style="margin-top:2rem;text-align:center;">
      <a href="/devis/" class="btn btn-gold">Demander un devis chemisage Bordeaux</a>
    </div>
  </div>
</section>

{form_section("Bordeaux")}
'''

    return html_base(
        'Chemisage canalisation Bordeaux | Syndic copropriete sans tranchee',
        'Chemisage de canalisation en copropriete a Bordeaux : sans tranchee, garantie decennale, vote AG. Specialistes des immeubles haussmanniens et patrimoine UNESCO.',
        'https://recherche-fuite-gironde.fr/detection-fuite/chemisage-bordeaux/',
        body,
        extra_ld=ld_service + ld_local + ld_breadcrumb + ld_faq,
    )


# ═══════════════════════════════════════════════════════════════
# PAGE USE CASE : Canalisation enterree Bordeaux
# ═══════════════════════════════════════════════════════════════

def page_canalisation_enterree_bordeaux():
    ld_service = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "Recherche de fuite canalisation enterree",
  "name": "Recherche de fuite canalisation enterree a Bordeaux et en Gironde",
  "description": "Localisation precise d'une fuite sur canalisation enterree (jardin, branchement, reseau prive) par gaz traceur azote/helium, sans excavation prealable. Precision au demi-metre pres.",
  "provider": {
    "@type": "LocalBusiness",
    "name": "Recherche Fuite Gironde",
    "url": "https://recherche-fuite-gironde.fr/"
  },
  "areaServed": { "@type": "Place", "name": "Bordeaux et metropole girondine" },
  "category": "Detection de fuite non destructive"
}
</script>'''

    ld_local = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Recherche Fuite Gironde - Canalisation enterree Bordeaux",
  "description": "Specialiste de la recherche de fuite sur canalisation enterree a Bordeaux. Gaz traceur azote/helium, ecoute electro-acoustique, thermographie. Intervention 24h, rapport pour assurance.",
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
    { "@type": "ListItem", "position": 2, "name": "Detection de fuite", "item": "https://recherche-fuite-gironde.fr/detection-fuite/" },
    { "@type": "ListItem", "position": 3, "name": "Canalisation enterree Bordeaux", "item": "https://recherche-fuite-gironde.fr/detection-fuite/canalisation-enterree-bordeaux/" }
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
      "name": "Comment localisez-vous une fuite sur canalisation enterree a Bordeaux sans creuser ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Notre methode principale est le gaz traceur azote/helium : un melange inerte injecte dans la canalisation sous legere pression. Le gaz plus leger que l'air remonte au droit de la perforation et est detecte par un capteur electronique promene au sol. Precision au demi-metre pres, sans aucune excavation prealable. L'ecoute electro-acoustique et la thermographie infrarouge completent le diagnostic si necessaire." }
    },
    {
      "@type": "Question",
      "name": "Quelles sont les canalisations enterrees les plus fragiles a Bordeaux ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Les canalisations PVC collees installees entre 1985 et 2000 sont les plus fragiles sur sol argileux bordelais. Les raccords se desaxent par retrait-gonflement saisonnier de l'argile. Les canalisations PEHD (polyethylene haute densite) posees depuis 2005 sont plus tolerantes aux mouvements de terrain. Les anciennes canalisations plomb et fonte des immeubles du centre historique (avant 1975) sont corrodees et sujettes aux perforations." }
    },
    {
      "@type": "Question",
      "name": "Combien coute une recherche de fuite sur canalisation enterree a Bordeaux ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Entre 400 et 700 euros HT selon la longueur de la canalisation a diagnostiquer et la complexite du reseau. Un forfait gaz traceur classique (jusqu'a 20 metres de canalisation) est a 450 euros HT en moyenne. Au-dela de 30 metres ou pour les reseaux complexes (plusieurs branches), un diagnostic approfondi peut atteindre 700 euros HT. Devis fixe communique avant intervention." }
    },
    {
      "@type": "Question",
      "name": "La recherche de fuite enterree est-elle remboursee par l'assurance ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Oui, dans la majorite des cas. La garantie recherche de fuite de votre contrat multirisque habitation prend en charge le diagnostic des lors qu'un degat des eaux est constate (terrain gorgé d'eau, impact sur fondations, infiltration dans construction). Si la fuite concerne une canalisation enterrée indetectable, vous pouvez en plus obtenir un ecretement de votre facture d'eau aupres de Suez ou votre regie via la loi Warsmann 2011." }
    },
    {
      "@type": "Question",
      "name": "Intervenez-vous dans tous les quartiers de Bordeaux pour les fuites enterrees ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Oui, nous couvrons l'ensemble des 18 quartiers de Bordeaux ainsi que les communes voisines de la metropole. Nous rencontrons les problematiques de fuites enterrees le plus frequemment dans les zones pavillonnaires (Caudéran, Le Bouscat, Bacalan, Saint-Augustin) avec grands jardins, ainsi que dans les copropriétés récentes avec reseaux enterres entre immeuble et regards techniques." }
    },
    {
      "@type": "Question",
      "name": "Faut-il creuser pour reparer apres votre diagnostic ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Oui, mais de maniere tres ciblee. Notre diagnostic localise la fuite au demi-metre pres, ce qui limite l'excavation a 50 cm x 50 cm en moyenne. Pour eviter totalement le creusement, deux alternatives : le chemisage de canalisation (rehabilitation sans tranchee par resine epoxy, adapte aux reseaux de 40 a 600 mm) ou le remplacement de la canalisation existante si son etat general l'exige." }
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
      <a href="/detection-fuite/">Detection de fuite</a>
      <span>&rsaquo;</span>
      <span>Canalisation enterree Bordeaux</span>
    </nav>
    <h1>Recherche de fuite de canalisation enterree a Bordeaux</h1>
    <p class="hero-mini-lead">Zone de jardin anormalement humide, compteur d'eau qui tourne en permanence, facture d'eau qui grimpe sans raison : votre fuite se situe probablement sur une canalisation enterree. Nos techniciens la localisent <strong>au demi-metre pres sans creuser</strong> grace au gaz traceur azote/helium, puis vous remettent un rapport utilisable pour l'assurance et l'ecretement de facture.</p>
    <div class="hero-mini-cta">
      <a href="/devis/" class="btn btn-gold">Demander un devis gratuit</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <figure style="margin:0 0 2rem;">
      <img src="/assets/fuite-canalisation-enterree.webp" alt="Recherche de fuite sur canalisation enterree a Bordeaux avec gaz traceur azote helium, diagnostic sans excavation" width="700" height="467" loading="eager" style="width:100%;max-height:380px;height:auto;object-fit:cover;border-radius:12px;display:block;">
    </figure>

    <h2>Les signes d'une fuite sur canalisation enterree a Bordeaux</h2>
    <p>Sur les proprietes bordelaises avec jardin, branchement d'eau enterre ou reseau d'arrosage, plusieurs symptomes doivent alerter. Contrairement aux fuites interieures visibles par une tache au plafond, les fuites enterrees sont sournoises : elles peuvent couler pendant des mois sans aucun signe au-dessus du sol.</p>

    <ul>
      <li><strong>Zone de jardin anormalement verte</strong> toute l'annee, meme en periode sans arrosage</li>
      <li><strong>Terrain gorgé d'eau ou sol qui s'affaisse</strong> sur un trace lineaire, suggerant le tracé d'une canalisation</li>
      <li><strong>Consommation d'eau qui grimpe</strong> sans changement d'usage, visible sur la facture trimestrielle Suez</li>
      <li><strong>Compteur d'eau qui tourne en permanence</strong> meme robinets fermes, a verifier le soir en coupant tout point d'eau</li>
      <li><strong>Pression d'eau anormalement basse</strong> au robinet alors que les canalisations interieures sont en bon etat</li>
      <li><strong>Flaque au pied de la maison</strong> apres plusieurs jours sans pluie, signe d'infiltration par la canalisation d'alimentation</li>
      <li><strong>Mousse ou champignons</strong> inhabituels en bordure de terrasse ou allee</li>
    </ul>

    <h2>Pourquoi les canalisations enterrees bordelaises lâchent-elles souvent au meme endroit ?</h2>
    <p>La specificite geologique de Bordeaux et sa metropole est determinante. Une large part du territoire repose sur des sols argileux sujets au retrait-gonflement saisonnier : l'argile se retracte en ete sec, gonfle en hiver pluvieux. Sur 20 a 30 ans, ces cycles repetes solliticitent les raccords collés PVC de maniere importante. Resultat observable sur le terrain : les raccords PVC de 25 a 35 ans cedent significativement plus a Bordeaux qu'en sol sableux ou calcaire pur.</p>

    <p>La zone aéroportuaire (Mérignac), la rive droite (Cenon, Lormont, Floirac) et le Grand Parc presentent cette typologie argileuse marquee. Les communes du bassin d'Arcachon sont en sol sableux (autre probleme : micro-tassements permanents), et le Libournais alterne argileux et calcaire selon les zones. Cette connaissance locale oriente notre methodologie de diagnostic.</p>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:1080px;">
    <h2>Notre methode gaz traceur en 5 etapes</h2>
    <p>Le gaz traceur azote/helium est la methode de reference pour les canalisations enterrees. Voici le deroule concret d'une intervention sur votre propriete bordelaise.</p>

    <div class="grid-3" style="margin-top:1.5rem;">
      <div class="arg-num-card">
        <span class="arg-num">01</span>
        <div class="arg-num-content">
          <h3>Reconnaissance du reseau</h3>
          <p>Reperage des regards, compteurs, arrivees et departs d'eau sur la propriete. Traçage approximatif des canalisations enterrees d'apres les plans disponibles ou observation du terrain. Identification des points d'injection possibles pour le gaz.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">02</span>
        <div class="arg-num-content">
          <h3>Mise sous pression et injection</h3>
          <p>La canalisation est isolee et mise sous legere pression avec un melange azote/hélium inerte (80/20). Le melange est plus leger que l'air et migre vers la fuite en prenant le trajet du moindre chemin.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">03</span>
        <div class="arg-num-content">
          <h3>Detection de surface</h3>
          <p>Un detecteur electronique tres sensible (sniffer) est promene au sol le long du trace presume de la canalisation. Le capteur signale la remontee du gaz avec une precision au demi-metre pres, materialisant la position exacte de la fuite.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">04</span>
        <div class="arg-num-content">
          <h3>Confirmation par ecoute</h3>
          <p>En complement, nous ecoutons electro-acoustiquement la zone localisee pour confirmer la fuite par le bruit caracteristique de l'eau sous pression qui s'echappe. Cette double confirmation elimine les faux positifs.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">05</span>
        <div class="arg-num-content">
          <h3>Materialisation et rapport</h3>
          <p>La position exacte de la fuite est marquee au sol (piquet, bombe de couleur non permanente). Le rapport technique photographique documente le trace, la methode, la localisation et les preconisations de reparation. Il est remis sur site ou sous 24h.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">06</span>
        <div class="arg-num-content">
          <h3>Option chemisage sans tranchee</h3>
          <p>Si plusieurs fuites sont identifiees sur le meme reseau, ou si la canalisation est generalement degradee, nous vous proposons une alternative au creusement : le chemisage tubulaire sans tranchee qui cree un nouveau tuyau a l'interieur de l'ancien.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:1080px;">
    <h2>Quartiers de Bordeaux ou nous intervenons le plus sur canalisation enterree</h2>
    <p>Certains quartiers concentrent les demandes pour fuite enterree en raison de leur typologie bâtie et de leur environnement paysager.</p>

    <div class="grid-3" style="margin-top:1.5rem;">
      <div class="arg-num-card">
        <span class="arg-num">01</span>
        <div class="arg-num-content">
          <h3>Caudéran et Le Bouscat</h3>
          <p>Grands jardins des proprietes bourgeoises, nombreux arbres matures (platanes, chenes, tilleuls) dont les racines sollicitent les canalisations. Les raccords PVC de 30 ans y sont particulierement fragiles. Nous intervenons souvent sur le trace d'alimentation compteur-maison.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">02</span>
        <div class="arg-num-content">
          <h3>Saint-Augustin et Grand Parc</h3>
          <p>Maisons individuelles avec jardins moyens, reseaux d'arrosage enterres frequents. Les confusions entre fuite alimentation et fuite arrosage sont courantes : notre diagnostic isole chaque circuit pour eliminer les faux positifs.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">03</span>
        <div class="arg-num-content">
          <h3>Bacalan et Bassins à Flot</h3>
          <p>Residences recentes (2010-2020) avec reseaux enterres entre immeuble et regards techniques. Les canalisations PEHD posees dans les annees 2010 sont robustes mais les raccords mécaniques sont sujets à défaut de serrage.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">04</span>
        <div class="arg-num-content">
          <h3>La Bastide et Cenon (rive droite)</h3>
          <p>Terrains argileux marques, nombreux pavillons des annees 1970-1990 avec canalisations PVC d'origine. Les mouvements de terrain y sont les plus actifs, les fuites enterrees les plus frequentes.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">05</span>
        <div class="arg-num-content">
          <h3>Mérignac et communes métropole</h3>
          <p>Parc pavillonnaire tres dense des annees 1980-2000. Canalisations d'alimentation souvent longues (20 a 50 m entre compteur et maison). Proportion importante de nos interventions enterrees se fait sur Merignac (Arlac, Capeyron, Chemin Long).</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">06</span>
        <div class="arg-num-content">
          <h3>Bordeaux Centre historique</h3>
          <p>Moins de canalisations enterrees individuelles (tissu urbain dense) mais presence de reseaux anciens (plomb, fonte, galvanisé) sous les cours interieures et arrières-cours des immeubles. Diagnostic particulier adaptant nos outils compacts aux configurations restreintes.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:960px;">
    <h2>Cas type d'intervention a Bordeaux</h2>
    <p>Scenario recurrent : maison familiale a Caudéran, canalisation d'alimentation enterrée de 1989 sur 35 metres entre le regard de compteur en façade et l'entrée de la maison. Le propriétaire constate une facture Suez doublée (de 40 m³ a 80 m³ par trimestre), sans changement d'usage. Aucune trace d'humidite visible dans le jardin ni dans la maison.</p>

    <p>Notre intervention : verification du robinet d'arrêt général (compteur qui continue de tourner apres coupure maison = fuite après compteur sur partie privative). Isolation du circuit d'arrosage (compteur qui s'arrête = arrosage hors cause). Mise sous pression du tronçon compteur-maison avec gaz traceur. Detection au sol le long du tracé : remontée du gaz à 22 metres du regard de compteur, sous l'allée gravillonnée. Marquage au sol et materialisation de la fuite.</p>

    <p>Reparation : ouverture localisée 60×60 cm au point marque, remplacement d'un manchon PVC de 40 cm, remblaiement et remise en état gravillons. Coût total intervention + réparation : 850 euros. Dossier transmis à l'assureur qui prend en charge 600 euros au titre de la garantie recherche de fuite, et le client obtient un écretement de sa facture Suez selon la loi Warsmann pour les m³ surconsommés.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:960px;">
    <h2>Questions frequentes sur la recherche de fuite enterree a Bordeaux</h2>

    <h3>Comment localisez-vous une fuite sur canalisation enterree a Bordeaux sans creuser ?</h3>
    <p>Notre methode principale est le gaz traceur azote/helium : un melange inerte injecte dans la canalisation sous legere pression. Le gaz plus leger que l'air remonte au droit de la perforation et est detecte par un capteur electronique promene au sol. Precision au demi-metre pres, sans aucune excavation prealable. L'ecoute electro-acoustique et la thermographie infrarouge completent le diagnostic si necessaire.</p>

    <h3>Quelles sont les canalisations enterrees les plus fragiles a Bordeaux ?</h3>
    <p>Les canalisations PVC collees installees entre 1985 et 2000 sont les plus fragiles sur sol argileux bordelais. Les raccords se desaxent par retrait-gonflement saisonnier de l'argile. Les canalisations PEHD posees depuis 2005 sont plus tolerantes aux mouvements de terrain. Les anciennes canalisations plomb et fonte des immeubles du centre historique (avant 1975) sont corrodees et sujettes aux perforations.</p>

    <h3>Combien coute une recherche de fuite sur canalisation enterree a Bordeaux ?</h3>
    <p>Entre 400 et 700 euros HT selon la longueur de la canalisation a diagnostiquer et la complexite du reseau. Un forfait gaz traceur classique (jusqu'a 20 metres de canalisation) est a 450 euros HT en moyenne. Au-dela de 30 metres ou pour les reseaux complexes (plusieurs branches), un diagnostic approfondi peut atteindre 700 euros HT.</p>

    <h3>La recherche de fuite enterree est-elle remboursee par l'assurance ?</h3>
    <p>Oui, dans la majorite des cas. La garantie recherche de fuite de votre contrat multirisque habitation prend en charge le diagnostic des lors qu'un degat des eaux est constate. Si la fuite concerne une canalisation enterrée indetectable, vous pouvez en plus obtenir un ecretement de votre facture d'eau aupres de Suez ou votre regie via la loi Warsmann 2011. Voir notre page <a href="/detection-fuite/fuite-apres-compteur/" style="color:var(--green);text-decoration:underline;">fuite d'eau apres compteur a Bordeaux</a> pour le detail de la procedure d'ecretement.</p>

    <h3>Intervenez-vous dans tous les quartiers de Bordeaux pour les fuites enterrees ?</h3>
    <p>Oui, nous couvrons l'ensemble des 18 quartiers de Bordeaux ainsi que les communes voisines de la metropole. Pour plus de details sur notre intervention ville par ville, consultez notre page <a href="/villes/bordeaux/" style="color:var(--green);text-decoration:underline;">recherche de fuite a Bordeaux</a>.</p>

    <h3>Faut-il creuser pour reparer apres votre diagnostic ?</h3>
    <p>Oui, mais de maniere tres ciblee. Notre diagnostic localise la fuite au demi-metre pres, ce qui limite l'excavation a 50 cm x 50 cm en moyenne. Pour eviter totalement le creusement, deux alternatives : le <a href="/chemisage-canalisation/" style="color:var(--green);text-decoration:underline;">chemisage de canalisation</a> (rehabilitation sans tranchee par resine epoxy, adapte aux reseaux de 40 a 600 mm) ou le remplacement de la canalisation existante si son etat general l'exige.</p>

    <div style="margin-top:2rem;text-align:center;">
      <a href="/devis/" class="btn btn-gold">Demander un devis canalisation enterree</a>
    </div>
  </div>
</section>

{form_section("Bordeaux")}
'''

    return html_base(
        'Recherche fuite canalisation enterree Bordeaux | Gaz traceur precis',
        'Recherche de fuite sur canalisation enterree a Bordeaux sans excavation : gaz traceur azote/helium, precision demi-metre, rapport pour assurance. Specialistes terrain argileux.',
        'https://recherche-fuite-gironde.fr/detection-fuite/canalisation-enterree-bordeaux/',
        body,
        extra_ld=ld_service + ld_local + ld_breadcrumb + ld_faq,
    )


# ═══════════════════════════════════════════════════════════════
# PAGE USE CASE : Fuite apres compteur d'eau
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
      "acceptedAnswer": { "@type": "Answer", "text": "La partie après compteur relève du propriétaire ou de l'occupant. La recherche de fuite est à votre charge mais souvent remboursée par votre assurance habitation au titre de la garantie recherche de fuite. Certaines communes ou intercommunalités proposent un écrêtement de facture en cas de fuite enterrée non détectable." }
    },
    {
      "@type": "Question",
      "name": "Peut-on faire écrêter la facture d'eau après une fuite ?",
      "acceptedAnswer": { "@type": "Answer", "text": "Oui, la loi Warsmann (2011) permet d'obtenir un écrêtement de la part excédentaire de votre facture si vous prouvez qu'une fuite sur canalisation enterrée (entre compteur et habitation) était indétectable. Il faut fournir une attestation de réparation par un professionnel et un rapport de localisation. Notre rapport technique peut servir de justificatif." }
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
    <p>Depuis 2011, la loi Warsmann impose aux distributeurs d'eau d'appliquer un écrêtement automatique en cas de fuite après compteur sur canalisation enterrée et non détectable. Autrement dit, votre facture est plafonnée au double de votre consommation habituelle, au lieu de payer l'intégralité du volume perdu.</p>

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
    <p>La partie après compteur relève du propriétaire ou de l'occupant. La recherche de fuite est à votre charge mais souvent remboursée par votre assurance habitation au titre de la garantie recherche de fuite. Certaines communes ou intercommunalités proposent un écrêtement de facture en cas de fuite enterrée non détectable.</p>

    <h3>Peut-on faire écrêter la facture d'eau après une fuite ?</h3>
    <p>Oui, la loi Warsmann (2011) permet d'obtenir un écrêtement de la part excédentaire de votre facture si vous prouvez qu'une fuite sur canalisation enterrée (entre compteur et habitation) était indétectable. Il faut fournir une attestation de réparation par un professionnel et un rapport de localisation.</p>

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

{form_section("Bordeaux")}
'''

    return html_base(
        'Fuite d\'eau après compteur à Bordeaux | Recherche et localisation',
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
        "types_piscines": "À Bordeaux et sa périphérie, nous intervenons majoritairement sur trois configurations : les piscines béton des années 1970-1990 dans les propriétés bourgeoises de Caudéran et Saint-Augustin, les coques polyester installées dans les années 1990-2010 dans les jardins plus compacts des quartiers pavillonnaires, et les liners PVC standards sur des bassins rectangulaires classiques. Quelques piscines miroir ou couloirs de nage se rencontrent dans les propriétés haut de gamme de Caudéran, et les chais du Médoc abritent parfois des piscines béton projeté très anciennes, fissurées structurellement.",
        "quartiers_zones": "Les zones de forte densité de piscines sur notre secteur d'intervention direct sont Caudéran et Le Bouscat (propriétés bourgeoises avec jardins matures), Saint-Augustin (maisons avec patio), le Grand Parc (certaines échoppes agrandies avec petit bassin), ainsi que les communes voisines Mérignac, Pessac et Talence. En zone viticole du Médoc, nous intervenons jusqu'à Pauillac et Saint-Julien dans les chais et résidences secondaires.",
        "specificites": [
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
            ("Piscine Le Bouscat + arrosage enterré confus", "Propriété Parc Bordelais, piscine liner 8×4 et arrosage enterré sur 300 m² de jardin. Consommation d'eau +400 m³/an inexpliquée. Diagnostic par fermeture séquentielle : la fuite n'est pas sur la piscine mais sur une vanne d'arrosage enterrée à 12 mètres au sud du bassin. Le propriétaire voulait vidanger sa piscine, ce que nous avons évité."),
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
        "specificites": [
            ("Piscines liner PVC en fin de première vie (25-35 ans)", "La majorité des liners que nous rencontrons à Mérignac ont été posés entre 1985 et 1995. À cet âge, le PVC perd sa plasticité : il se rigidifie, les plis aux angles se figent et se fissurent, les soudures des coins et au droit du skimmer cèdent par fatigue. La recherche de fuite sur ces liners demande un colorant fluorescéine précis et une observation en apnée ou à la caméra, car les perforations sont souvent punctiformes (0,5 à 2 mm)."),
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
        "specificites": [
            ("Corrosion accélérée par air salin", "L'air chargé en embruns marins (le Bassin est à moins d'un kilomètre de la plupart des piscines arcachonaises) corrode à vitesse accélérée tout l'inox du local technique : échangeurs thermiques, vis de brides, raccords de capteurs, nourrices de distribution. Les pompes à chaleur piscine y ont une durée de vie de 7 à 10 ans au lieu de 12-15 ans en intérieur des terres. Nous diagnostiquons régulièrement des fuites de PAC piscine venant d'un condenseur corrodé, pas du bassin lui-même."),
            ("Piscines miroir et débordement complexes", "Sur les piscines à débordement périphérique (très courantes à Abatilles et Pereire), la fuite n'est pas visible par la simple baisse de niveau du bassin : l'eau déborde en permanence dans le bac tampon qui compense. C'est le bac tampon qui baisse, ou la consommation d'eau de remise à niveau automatique qui augmente. Notre méthodologie sur ces bassins : test de coupure de la circulation, isolation séquentielle de chaque buse de débordement, inspection caméra des gouttières."),
            ("Résidences secondaires et dégâts en hivernage", "Une partie importante de notre clientèle arcachonaise sont des résidents secondaires occupant leur villa 2 à 6 semaines par an. Une fuite non détectée à l'automne peut causer des dégâts considérables : 5 à 10 m³ perdus par semaine, affouillement des terres sous la dalle de plage, infiltration dans le local technique, dégradation du jardin. Nous proposons un contrat de diagnostic préventif saisonnier pour ces clients."),
            ("Canalisations enterrées en sable et micro-tassements", "Le sol sableux typique d'Arcachon (sables blancs du Bassin) offre une excellente portance mais subit des tassements différentiels sur la durée. Les canalisations enterrées entre la piscine et le local technique, souvent sur 10 à 25 mètres de tracé, se désaxent lentement au niveau des raccords collés PVC. Le gaz traceur azote/hélium est notre méthode de référence pour localiser ces fuites au demi-mètre près sans excavation.")
        ],
        "cas_frequent": "Cas type arcachonais : villa de la Ville d'Hiver avec piscine béton 11×5 mètres chauffée par PAC, propriétaire résident de l'agglomération bordelaise qui occupe sa résidence secondaire 4-5 semaines par an. Constat à la réouverture printanière : bassin plus bas de 15 cm malgré couverture, compteur d'eau de remise à niveau anormal. Notre diagnostic combine test de pression des canalisations (première suspicion), inspection PAC (condenseur fuyant dans 30 pourcent des cas sur ce profil), puis colorant sur pièces à sceller. Dans 45 pourcent des cas, la fuite vient du réseau hydraulique entre bassin et local technique, au niveau d'un raccord désaxé par tassement sableux.",
        "faq_locale": [
            ("Dois-je hiverner ma piscine Arcachon en hiver ou la laisser en fonctionnement ?",
             "Le climat océanique doux d'Arcachon permet de laisser la piscine en fonctionnement réduit toute l'année, ce que font beaucoup de propriétaires de résidences secondaires. Attention cependant : une fuite non détectée peut générer un sinistre majeur avant votre retour. Nous recommandons a minima un diagnostic préventif tous les 2-3 ans sur ce profil d'usage, et un hivernage actif dès que le propriétaire ne revient pas avant mars."),
            ("La proximité de l'eau salée du Bassin peut-elle polluer ma piscine ?",
             "Non, la piscine utilise de l'eau douce du réseau public, il n'y a pas de contamination directe par le Bassin d'Arcachon. En revanche, l'air salin accélère la corrosion des éléments métalliques : vis des pièces à sceller, brides de skimmer, échangeurs thermiques. Sur une piscine arcachonaise de plus de 15 ans, nous vérifions systématiquement l'état de l'inox au local technique en complément du diagnostic bassin."),
            ("Intervenez-vous sur les piscines des villas classées de la Ville d'Hiver ?",
             "Oui, nous sommes formés à intervenir sur les bâtiments classés et les abords protégés. Notre méthodologie strictement non destructive préserve les margelles en pierre d'origine, les plages carrelées d'époque et les décors paysagers matures. Un devis précis détaille les précautions prises et les limites techniques rencontrées sur ces configurations patrimoniales.")
        ],
        "methodes_focus": "Les piscines arcachonaises, souvent équipées (chauffage PAC, débordement, couverture automatique), demandent une approche méthodique en deux temps. D'abord, vérification complète du local technique : état des pompes, échangeurs thermiques, vannes. En climat salin, une fuite sur équipement (échangeur PAC corrodé, joint d'axe pompe) est aussi probable qu'une fuite de bassin, et se diagnostique visuellement. Ensuite seulement, test du bassin : colorant fluorescéine aux pièces à sceller et inspection caméra sous-marine (les piscines arcachonaises étant souvent de qualité supérieure, les défauts sont plus subtils : micro-fissure d'angle, décollement de carrelage invisible à l'œil nu). Pour les piscines miroir ou débordement, isolation du bac tampon obligatoire.",
        "patterns_frequents": [
            ("Villa Ville d'Hiver PAC corrodée", "Villa 1895, piscine ajoutée 1990, PAC Zodiac installée en 2010. Consommation d'eau anormale constatée au retour printemps. Inspection local technique : condenseur PAC percé, fuite d'eau continue par l'évacuation. Bassin intact. Préconisation : remplacement PAC (8 à 12 000 euros HT neuf), diagnostic 380 euros HT."),
            ("Piscine miroir débordement Abatilles", "Villa récente 2015, piscine 12×4 à débordement périphérique. Bac tampon baisse régulière de 8-10 cm/jour, sans perte apparente sur bassin principal. Diagnostic : gaz traceur sur circuit de remontée, fuite identifiée sur raccord PE de 20 mètres sous la plage. Réparation : ouverture ciblée d'une dalle préfabriquée, reprise raccord, rescellement. 2 600 euros total."),
            ("Villa résidence secondaire Pereire après hiver", "Villa front Bassin, propriétaires parisiens en résidence secondaire. Ouverture printanière : local technique inondé, 15 cm d'eau au sol. Diagnostic : fuite sur clapet de vanne hivernage mal serré. Bassin intact mais pompe noyée à remplacer. Rapport détaillé pour assurance multirisque : prise en charge totale du sinistre.")
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
        "specificites": [
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
            ("Confusion piscine/arrosage enterré Cazaux", "Pavillon 1998, piscine liner + arrosage automatique sur 400 m². Client suspectait fuite bassin (perte niveau). Diagnostic par isolation : fuite réelle sur électrovanne d'arrosage enterrée, pas sur la piscine. Le propriétaire allait vidanger sa piscine. Économie : 1 500 euros de vidange/remise en eau + bonne piscine sauvée.")
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
        "specificites": [
            ("Coques polyester des années 2000-2015 en vieillissement", "Le parc de coques de Gujan-Mestras entre dans la phase de vieillissement où les gel-coats d'origine montrent leurs faiblesses : micro-cloques par osmose, fissures de retrait au niveau des bondes de fond moulées, délaminage entre couches de fibres de verre. Notre inspection caméra sous-marine identifie ces défauts et les différencie d'une simple fuite hydraulique. La fluorescéine complète le diagnostic en confirmant si un défaut visuel est bien fuyant."),
            ("Proximité immédiate du Bassin d'Arcachon", "Une partie des piscines gujanaises se situe à moins de 500 mètres du Bassin, avec les mêmes effets d'air salin et humidité qu'à Arcachon : corrosion des inox, des pompes à chaleur, des éléments métalliques du local technique. Le diagnostic piscine doit systématiquement inclure la vérification du périphérique technique, la fuite pouvant venir d'un équipement corrodé plutôt que du bassin lui-même."),
            ("Piscines naturelles et bio-phytoépuration", "Gujan-Mestras compte un nombre croissant de piscines naturelles à filtration végétale (lagunage, bassin de plantation). Ces installations nécessitent une approche spécifique : la fuite peut être dans le bassin de baignade, le bassin de lagunage, ou les canalisations de transfert entre les deux. Nos méthodes (colorant, acoustique, gaz traceur) s'adaptent à ces configurations non conventionnelles, plus complexes à diagnostiquer."),
            ("Hivernage hétérogène selon usage", "Entre résidents principaux qui hivernent actif (couverture + filtration réduite), résidents secondaires qui hivernent passif (bassin bâché et couvrant) et locations saisonnières qui laissent à l'abandon total, la qualité d'hivernage varie fortement à Gujan. Une mauvaise hivernisation en région Bassin (où le gel est rare mais l'humidité extrême) endommage les joints des pièces à sceller, surtout si la piscine est placée en zone venteuse exposée.")
        ],
        "cas_frequent": "Scénario fréquent à Gujan-Mestras : coque polyester 8×4 mètres installée vers 2008 dans un lotissement de La Hume, propriétaire résident principal. Il constate après ouverture de saison une baisse de 2 cm/jour, sans changement d'usage. Notre méthodologie : inspection caméra complète de la coque (recherche de micro-fissures, cloques, défauts), injection de colorant aux 4 pièces à sceller, test de pression sur chaque circuit. Dans 40 pourcent des cas, la fuite est sur la coque elle-même (micro-fissure près d'une bride), dans 35 pourcent sur un joint, et 25 pourcent sur canalisation enterrée.",
        "faq_locale": [
            ("Ma coque polyester Gujan-Mestras a 15 ans, à quoi dois-je faire attention ?",
             "Les coques polyester de 15 ans atteignent la phase où les défauts structurels apparaissent : osmose (cloques sur le gel-coat, signe d'humidité passée derrière la couche étanche), délaminage inter-couches (décollement entre strates de fibre), fissures au niveau des pièces moulées (bondes, marches). Notre inspection caméra sous-marine systématique sur ces coques détecte les défauts précoces et permet une réparation ciblée avant la fuite majeure."),
            ("Puis-je installer une piscine naturelle malgré la proximité du Bassin ?",
             "Oui, les piscines naturelles fonctionnent très bien sur la commune. Le sol sableux facilite les bassins de lagunage. Attention en revanche à respecter les règles locales d'installation (distance aux arbres, gestion du trop-plein, compatibilité avec la nappe phréatique parfois proche). Pour la recherche de fuite sur ce type d'installation, nous utilisons les mêmes méthodes que sur une piscine classique, avec une attention particulière aux transferts entre compartiments."),
            ("Faut-il un matériel spécifique pour les piscines de résidences secondaires à Gujan ?",
             "Pas de matériel spécifique, mais une méthodologie adaptée : nous combinons systématiquement inspection caméra, test de pression des canalisations et vérification du local technique (corrosion équipements), car les fuites de résidences secondaires peuvent s'être accumulées pendant plusieurs mois sans contrôle. Le rapport final détaille l'état global du bassin, utile pour les propriétaires qui ne sont pas sur place.")
        ],
        "methodes_focus": "À Gujan-Mestras, où le parc de piscines est dominé par les coques polyester de la tranche 2000-2015, l'inspection caméra sous-marine est notre première méthode de diagnostic : elle identifie rapidement les signes d'osmose (cloques), les micro-fissures au niveau des bondes moulées, et les délaminages entre couches de fibre. Le colorant fluorescéine confirme si un défaut visuel est bien fuyant. Pour les piscines proches du Bassin (Larros, Gujan Port), contrôle systématique de l'inox et des équipements PAC au local technique. Les piscines naturelles à lagunage demandent une adaptation : isolation séquentielle des compartiments (baignade, filtration végétale, transferts) avant d'identifier la zone fuyante.",
        "patterns_frequents": [
            ("Coque polyester La Hume osmose + micro-fissure", "Villa 2008 avec coque coco 8×4. Baisse 2 cm/jour. Inspection caméra : osmose diffuse, cloques multiples mais aucune ne fuit. Fluorescéine révèle une micro-fissure punctiforme près de la marche Romaine, invisible à l'œil. Réparation par résine époxy piscine appliquée sous l'eau. Diagnostic + réparation : 550 euros."),
            ("Piscine naturelle lagunage diagnostic complexe", "Installation 2018, bassin baignade 6×4 + bassin lagunage végétal. Perte de niveau globale, localisation incertaine. Méthode : fermeture de la circulation entre bassins, mesure différentielle sur 48h. Fuite isolée sur le bassin de lagunage, au niveau d'une étanchéité PVC dégradée par racines de plantes. Intervention 780 euros."),
            ("Villa front Bassin pompe piscine corrodée", "Maison Larros en bordure de Bassin, piscine 10×5 avec PAC installée en 2012. Baisse niveau + circulation perturbée. Diagnostic : pompe centrifuge corrodée à l'axe, joint mécanique fuyant, eau s'écoule par le siphon de sol du local. Bassin intact. Remplacement pompe + nouveau joint : 1 100 euros.")
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
        "types_piscines": "Le parc libournais se distingue par une forte présence de piscines béton projeté des années 1970-1990, avec enduit ciment d'origine et étanchéité par peinture époxy refaite plusieurs fois. On trouve aussi des bassins plus récents en liner PVC ou coques polyester dans les lotissements de Libourne intra-muros, quelques piscines hors-sol dans les maisons de négociants, et des bassins couloirs de nage dans les domaines viticoles haut de gamme de Saint-Émilion grand cru et Pomerol.",
        "quartiers_zones": "Nos interventions se concentrent à Libourne centre (quartier bourgeois autour de la place Abel-Surchamp), La Ballastière et Verdet (lotissements récents), Fontenelle (résidentiel), et surtout dans les domaines viticoles alentours : Saint-Émilion (Château Cheval Blanc, Château Figeac secteurs), Pomerol (Château Pétrus voisinage), Fronsac et Canon-Fronsac, Côtes de Castillon. Saint-Denis-de-Pile, Coutras et Branne complètent notre zone de déplacement standard.",
        "specificites": [
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
        "methodes_focus": "Sur les bassins du Libournais, souvent anciens (30 à 50 ans) et en béton armé, notre approche technique commence par l'inspection caméra sous-marine pour évaluer l'état structurel : les fissures actives, l'état des enduits d'origine, la présence de fers d'armature affleurants. Le colorant fluorescéine confirme les fissures suspectes et teste les pièces à sceller souvent d'un autre âge. Sur terrain argileux, le test de pression des canalisations enterrées est incontournable : les raccords PVC collés 30 ans auparavant ont subi de multiples cycles retrait-gonflement. L'écoute électro-acoustique est notre outil de confirmation pour localiser précisément un défaut identifié par test de pression sur un long linéaire.",
        "patterns_frequents": [
            ("Château Saint-Émilion piscine béton 1975", "Domaine grand cru, piscine béton 14×6 construite 1975, enduit ciment refait 1998. Perte d'eau accélérée +6 cm/jour après hiver humide. Inspection caméra : 2 fissures actives en paroi nord. Préconisation : rebéton paroi concernée + nouvelle étanchéité membrane armée. Devis 25 000 euros HT (compatible avec budget domaine), diagnostic 580 euros remboursé assurance."),
            ("Maison négociant Libourne fuite cave voûtée", "Maison 1880 centre Libourne, cave voûtée avec humidité croissante au plafond. Propriétaires soupçonnent la piscine du jardin (ajoutée 1995). Diagnostic combiné : humidimètre (cave) + thermographie + colorant piscine. Conclusion : fuite canalisation PVC entre piscine et maison, à 11 mètres du bassin sous la terrasse. Ouverture ciblée, réparation 1 800 euros, cave préservée."),
            ("Bassin Fronsac coque polyester rénovée 2010", "Château Fronsac, ancienne piscine béton rehabilitée par pose coque polyester sur ancienne structure 2010. Baisse 3 cm/jour. Diagnostic : coque intacte, mais raccord entre bondes de fond de la coque et canalisations PVC d'origine était mal collé. Localisation au colorant + confirmation test pression. Reprise 900 euros.")
        ],
    },
    {
        "slug": "piscine-le-bouscat",
        "ville": "Le Bouscat",
        "ville_article": "au Bouscat",
        "cp": "33110",
        "zones_voisines": "Bordeaux, Caudéran, Bruges, Eysines, Mérignac",
        "hero_image_alt": "Piscine traditionnelle dans un jardin mature du Bouscat près du Parc Bordelais, zone d'intervention recherche de fuite",
        "intro_unique": "Le Bouscat, ville résidentielle bourgeoise collée à Bordeaux, concentre un parc de piscines relativement ancien dans ses quartiers les plus cossus : Parc Bordelais, La Châtaigneraie, Bourran. Beaucoup de bassins ont été installés dans les années 1970-1990 au cœur de grands jardins matures, aujourd'hui caractérisés par la proximité d'arbres développés dont les systèmes racinaires sollicitent les canalisations enterrées. Ce contexte demande une approche diagnostique particulière.",
        "types_piscines": "Les piscines bouscataises se répartissent entre plusieurs profils : bassins béton armé classiques des années 1970-1980 (40 pourcent environ), coques polyester des années 1990-2010 posées en rénovation de bassins plus anciens (25 pourcent), liners PVC modernes sur bassins existants (20 pourcent), et quelques couloirs de nage ou piscines cintrées dans les jardins étroits de maisons bourgeoises (15 pourcent). Quelques piscines de caractère à la limite de Caudéran, avec margelles en pierre de Frontenac et décoration soignée.",
        "quartiers_zones": "Les secteurs à forte densité sont Parc Bordelais (hôtels particuliers et grandes propriétés avec bassins historiques), La Châtaigneraie (résidentiel familial avec grands jardins), Bourran (quartier cossu aux frontières de Caudéran), Parc Rivière et Croix de Laubrescas (plus pavillonnaire récent). Les maisons bourgeoises des années 1910-1930 reconverties en résidences familiales présentent souvent des piscines ajoutées dans les années 1980 sans étude de sol contemporaine.",
        "specificites": [
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
             "Oui, sans problème. Nos sondes acoustiques et nos colorants en bouteille lestée atteignent le fond de tout bassin sans nécessiter de plongée humaine. Dans certains cas complexes, nous faisons intervenir un plongeur professionnel équipé (scaphandre autonome), notamment pour une inspection visuelle rapprochée de la bonde de fond. Cette option est facturée en supplément et proposée si le diagnostic acoustique et colorant est insuffisant.")
        ],
        "methodes_focus": "Sur les piscines du Bouscat, presque toutes anciennes et entourées de jardins matures, notre première méthode est l'inspection caméra endoscopique des canalisations enterrées : dans 55 pourcent des diagnostics bouscatais, la fuite vient d'un raccord pénétré par une racine d'arbre (platane, chêne, tilleul ou saule). Quand l'inspection ne révèle pas de racine, nous enchaînons avec le test de pression séquentiel des circuits, puis le colorant fluorescéine sur pièces à sceller du bassin. Pour les piscines de 3-4 mètres de profondeur (rares mais présentes dans les propriétés historiques), utilisation d'une bouteille de colorant lestée qui descend au fond du bassin sans nécessiter de plongée. L'écoute acoustique complète le diagnostic sur les longs tracés de canalisations sous les grandes pelouses.",
        "patterns_frequents": [
            ("Piscine Parc Bordelais racine de platane", "Propriété familiale, piscine béton 10×4 des années 1978, 3 grands platanes à 7-10 mètres. Baisse régulière +2 cm/jour depuis 1 an. Inspection caméra des canalisations : racine de platane de 5 cm de diamètre entrée par un raccord défectueux à 6 m du bassin. Réparation : coupe racinaire, remplacement 60 cm de canalisation, injection inhibiteur racinaire. 1 600 euros total. Suivi tous les 5 ans recommandé."),
            ("Jardin La Châtaigneraie accès étroit", "Maison bourgeoise 1910, piscine couloir de nage 15×2,5 mètres au fond du jardin, accessible uniquement par une porte cochère de 80 cm. Matériel compact déployé : caméra endoscopique sans fil, corrélateur portable, bouteilles gaz traceur 5L. Localisation fuite au niveau bonde de fond, joint torique usé. Remplacement en apnée : 420 euros total."),
            ("Piscine profonde 4m Bourran 1976", "Propriété 1900, piscine béton 12×5 avec point profond 4m (plongeoir d'origine). Baisse 3 cm/jour. Colorant lesté descendu au fond : fissure radiale autour de la grille de bonde, 15 cm de long. Préconisation : réparation en apnée par plongeur pro (nécessaire à cette profondeur) + joint étanche. 1 800 euros + plongeur.")
        ],
    },
]

def page_piscine_ville(p):
    ville = p["ville"]
    ville_article = p["ville_article"]
    cp = p["cp"]
    slug = p["slug"]

    # Construction des specificites uniques
    specificites_html = '\n'.join([
        f'      <div class="arg-num-card"><span class="arg-num">{i:02d}</span><div class="arg-num-content"><h3>{titre}</h3><p>{contenu}</p></div></div>'
        for i, (titre, contenu) in enumerate(p["specificites"], 1)
    ])

    # FAQ locale (questions uniques par ville)
    faq_locale_html = '\n'.join([
        f'    <h3>{q}</h3>\n    <p>{a}</p>'
        for q, a in p["faq_locale"]
    ])

    # Patterns d'interventions frequentes (uniques par ville)
    patterns_html = '\n'.join([
        f'      <div class="arg-num-card"><span class="arg-num">{i:02d}</span><div class="arg-num-content"><h3>{titre}</h3><p>{contenu}</p></div></div>'
        for i, (titre, contenu) in enumerate(p.get("patterns_frequents", []), 1)
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
        f'<a href="/detection-fuite/{p["slug"]}/" class="loc-card" style="text-decoration:none;color:inherit;padding:1rem 1.25rem;background:var(--white);border:1px solid var(--c-border);border-radius:12px;display:block;"><strong>Piscine {p["ville"]}</strong><span style="display:block;font-size:.85rem;color:var(--c-text-muted);margin-top:.25rem;">{p["cp"]}</span></a>'
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
      <a href="#methodes" class="btn btn-outline-green">Nos méthodes</a>
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

    <p style="margin-top:1rem;">Au-delà des piscines, nos techniciens interviennent aussi pour tous types de fuites sur la commune : consultez notre page <a href="/villes/{p.get('ville').lower().replace(' ', '-').replace('é','e').replace('è','e').replace('ê','e')}/" style="color:var(--c-primary-light);text-decoration:underline;">recherche de fuite à {p['ville']}</a> pour les interventions hors piscine (canalisations encastrées, planchers chauffants, dégâts des eaux).</p>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:1080px;">
    <h2>Ma piscine perd de l'eau : fuite ou évaporation ?</h2>
    <p>Avant de parler de fuite, il faut écarter l'évaporation naturelle. En Gironde, une piscine extérieure sans abri perd en moyenne <strong>3 à 5 mm par jour en été</strong> (juin à septembre) et <strong>0 à 2 mm par jour au printemps et à l'automne</strong>. Au-delà, surtout si la perte dépasse 1 cm par jour, une fuite est probable.</p>

    <h3>Le test du seau, première étape gratuite</h3>
    <p>Posez un seau rempli d'eau sur la première marche de votre piscine (pour qu'il soit à la même température). Marquez au feutre le niveau intérieur du seau et le niveau de la piscine sur la paroi. Laissez 24 à 48 heures sans baignade, sans remise à niveau automatique et sans pluie. Si le seau et la piscine baissent de la même hauteur, c'est de l'évaporation. Si la piscine baisse nettement plus que le seau, vous avez une fuite et il est temps de nous contacter.</p>

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

<section class="section" id="methodes">
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
          <p>Un colorant fluorescent non toxique (de qualité alimentaire) est injecté à la seringue près des zones suspectes : skimmer, buses de refoulement, bonde de fond, fissures visibles. La filtration à l'arrêt, le colorant est aspiré vers la fuite et révèle son parcours exact. Méthode rapide pour les fuites de l'enceinte du bassin.</p>
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
          <p>On isole chaque circuit (aspiration, refoulement, balai, bonde de fond) en obturant les bouches puis en mettant sous pression. La perte de pression mesurée identifie le circuit défectueux. Couplé à l'écoute, on localise ensuite le point exact.</p>
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
          <p>Pour les canalisations enterrées longues ou inaccessibles acoustiquement, on injecte un mélange d'azote et d'hélium dans le réseau mis sous pression. Le gaz remonte en surface au droit de la fuite et est détecté par un capteur de surface.</p>
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
          <p>Perforation, accroc, décollement de soudure aux angles, cloque, pli marqué. Le liner fuit le plus souvent au niveau des pièces à sceller (skimmer, prise balai, buses) où les brides peuvent s'être desserrées avec le temps.</p>
        </div>
      </div>
      <div class="arg-num-card">
        <span class="arg-num">02</span>
        <div class="arg-num-content">
          <h3>Fuite skimmer ou refoulement</h3>
          <p>Joint mastic sec et fissuré entre la pièce à sceller et le béton ou la coque, bride mal serrée, fissure de la pièce plastique elle-même. Très fréquent après plusieurs hivernages.</p>
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
          <tr style="background:var(--c-primary);color:var(--white);">
            <th style="padding:.8rem;text-align:left;border:1px solid var(--c-primary-mid);">Type de diagnostic</th>
            <th style="padding:.8rem;text-align:left;border:1px solid var(--c-primary-mid);">Tarif moyen HT</th>
            <th style="padding:.8rem;text-align:left;border:1px solid var(--c-primary-mid);">Durée d'intervention</th>
          </tr>
        </thead>
        <tbody>
          <tr><td style="padding:.8rem;border:1px solid var(--c-border);">Test d'évaporation seul (sans déplacement)</td><td style="padding:.8rem;border:1px solid var(--c-border);">Gratuit, à faire soi-même</td><td style="padding:.8rem;border:1px solid var(--c-border);">24 à 48 h</td></tr>
          <tr style="background:var(--c-bg);"><td style="padding:.8rem;border:1px solid var(--c-border);">Recherche colorant + inspection visuelle</td><td style="padding:.8rem;border:1px solid var(--c-border);">300 à 400 €</td><td style="padding:.8rem;border:1px solid var(--c-border);">1 h 30 à 2 h</td></tr>
          <tr><td style="padding:.8rem;border:1px solid var(--c-border);">Recherche complète (colorant + acoustique + pression)</td><td style="padding:.8rem;border:1px solid var(--c-border);">450 à 600 €</td><td style="padding:.8rem;border:1px solid var(--c-border);">2 à 3 h</td></tr>
          <tr style="background:var(--c-bg);"><td style="padding:.8rem;border:1px solid var(--c-border);">Recherche avancée avec gaz traceur enterré</td><td style="padding:.8rem;border:1px solid var(--c-border);">600 à 800 €</td><td style="padding:.8rem;border:1px solid var(--c-border);">3 à 4 h</td></tr>
          <tr><td style="padding:.8rem;border:1px solid var(--c-border);">Vidange + inspection classique (méthode à éviter)</td><td style="padding:.8rem;border:1px solid var(--c-border);">1 000 à 2 000 €</td><td style="padding:.8rem;border:1px solid var(--c-border);">1 à 3 jours</td></tr>
        </tbody>
      </table>
    </div>

    <p>Un devis fixe vous est communiqué avant intervention après un premier échange téléphonique sur les symptômes observés. Aucun déplacement facturé si vous décidez de ne pas donner suite.</p>

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
    <p style="text-align:center;margin-bottom:1.5rem;">Nous intervenons sur l'ensemble de la métropole bordelaise et du Bassin d'Arcachon.</p>
    <div class="grid-3">
      {autres_html}
    </div>
    <p style="text-align:center;margin-top:1.5rem;"><a href="/detection-fuite/" class="btn btn-outline-green">Voir toutes nos spécialités &rarr;</a></p>
  </div>
</section>

{form_section(p['ville'])}
'''

    return html_base(
        f'Recherche de fuite piscine {ville_article} | Sans vidange ({cp})',
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
  "name": "Recherche Fuite Gironde",
  "description": "Spécialiste de la recherche et de la détection de fuites d'eau en Gironde (33). Méthodes non destructives, intervention rapide.",
  "url": "https://recherche-fuite-gironde.fr/",
  "areaServed": { "@type": "AdministrativeArea", "name": "Gironde" },
  "address": { "@type": "PostalAddress", "addressRegion": "Gironde", "addressCountry": "FR" },
  "serviceType": ["Recherche de fuite", "Détection de fuite", "Chemisage de canalisation"]
}
</script>'''

    return html_base(
        "Entreprise de recherche de fuites en Gironde - détection non destructive",
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
    ]
    urls += [f'https://recherche-fuite-gironde.fr/guide/{a["slug"]}/' for a in GUIDE_PAGES]
    urls += [f'https://recherche-fuite-gironde.fr/villes/{v["slug"]}/' for v in VILLES]
    urls += [f'https://recherche-fuite-gironde.fr/villes/{v["slug"]}/chemisage/' for v in VILLES]
    urls += [f'https://recherche-fuite-gironde.fr/detection-fuite/{p["slug"]}/' for p in PISCINE_PAGES]
    urls += [f'https://recherche-fuite-gironde.fr/detection-fuite/{p["slug"]}/' for p in URGENCE_PAGES]
    urls += ['https://recherche-fuite-gironde.fr/detection-fuite/fuite-apres-compteur/']
    urls += ['https://recherche-fuite-gironde.fr/detection-fuite/canalisation-enterree-bordeaux/']
    urls += ['https://recherche-fuite-gironde.fr/detection-fuite/degats-des-eaux-bordeaux/']
    urls += ['https://recherche-fuite-gironde.fr/detection-fuite/chemisage-bordeaux/']
    urls += ['https://recherche-fuite-gironde.fr/detection-fuite/fuite-plancher-chauffant-bordeaux/']

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
        write(f'villes/{v["slug"]}/chemisage/index.html', page_ville_chemisage(v))

    print('[7b] Pages use case — piscine par ville...')
    for p in PISCINE_PAGES:
        write(f'detection-fuite/{p["slug"]}/index.html', page_piscine_ville(p))

    print('[7c] Pages use case — urgence par ville...')
    for p in URGENCE_PAGES:
        write(f'detection-fuite/{p["slug"]}/index.html', page_urgence_ville(p))

    print('[7d] Page use case — fuite apres compteur...')
    write('detection-fuite/fuite-apres-compteur/index.html', page_fuite_apres_compteur())

    print('[7e] Page use case — canalisation enterree Bordeaux...')
    write('detection-fuite/canalisation-enterree-bordeaux/index.html', page_canalisation_enterree_bordeaux())

    print('[7f] Page use case — degats des eaux Bordeaux...')
    write('detection-fuite/degats-des-eaux-bordeaux/index.html', page_degats_eaux_bordeaux())

    print('[7g] Page use case — chemisage Bordeaux landing...')
    write('detection-fuite/chemisage-bordeaux/index.html', page_chemisage_bordeaux())

    print('[7h] Page use case — fuite plancher chauffant Bordeaux...')
    write('detection-fuite/fuite-plancher-chauffant-bordeaux/index.html', page_plancher_chauffant_bordeaux())

    print('[8/8] Fichiers techniques...')
    write('sitemap.xml', gen_sitemap())
    write('robots.txt', ROBOTS)
    write('vercel.json', VERCEL)

    total = 2 + 3 + 1 + len(GUIDE_PAGES) + 1 + len(VILLES)*2 + 3
    print(f'\n✓ {total} fichiers générés avec succès.\n')

if __name__ == '__main__':
    main()
