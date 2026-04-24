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
        "ville_locatif": "Bordeaux",
        "cp": "33000",
        "contexte_local": "Des propriétés viticoles du Médoc aux villas de Caudéran, du Bouscat ou de Saint-Augustin, les piscines privées de la métropole bordelaise présentent une grande diversité de configurations : bassins enterrés béton, coques polyester, liners PVC, margelles en pierre de Frontenac. Chaque structure exige une approche adaptée pour localiser une fuite sans vidange.",
        "zones_voisines": "Mérignac, Pessac, Talence, Le Bouscat, Caudéran",
        "hero_image_alt": "Piscine privée avec terrasse dans une propriété de la métropole bordelaise, zone d'intervention recherche de fuite",
    },
    {
        "slug": "piscine-merignac",
        "ville": "Mérignac",
        "ville_article": "à Mérignac",
        "ville_locatif": "Mérignac",
        "cp": "33700",
        "contexte_local": "Mérignac concentre une forte densité de maisons individuelles avec piscine dans les quartiers d'Arlac, Capeyron, Chemin Long et Beutre. Les bassins des années 1980 à 2000, souvent en béton projeté ou liner PVC, présentent des problématiques récurrentes : canalisations PVC vieillissantes, joints de skimmer durcis, liners en fin de vie. Notre diagnostic non destructif s'adapte à chacune de ces configurations.",
        "zones_voisines": "Bordeaux, Le Haillan, Eysines, Pessac, Saint-Médard-en-Jalles",
        "hero_image_alt": "Piscine privée en jardin d'une maison individuelle à Mérignac, zone d'intervention recherche de fuite sans vidange",
    },
    {
        "slug": "piscine-arcachon",
        "ville": "Arcachon",
        "ville_article": "à Arcachon",
        "ville_locatif": "Arcachon",
        "cp": "33120",
        "contexte_local": "Les piscines d'Arcachon et de la Ville d'Hiver subissent un environnement spécifique : proximité de l'eau salée, vents porteurs de sable, variations hygrométriques importantes. Ces conditions accélèrent le vieillissement des joints, des pièces à sceller et des canalisations enterrées. L'air salin corrode aussi les équipements du local technique plus rapidement qu'à l'intérieur des terres.",
        "zones_voisines": "La Teste-de-Buch, Gujan-Mestras, Le Teich, Pyla-sur-Mer",
        "hero_image_alt": "Piscine privée à Arcachon proche du Bassin, zone d'intervention recherche de fuite",
    },
    {
        "slug": "piscine-la-teste-de-buch",
        "ville": "La Teste-de-Buch",
        "ville_article": "à La Teste-de-Buch",
        "ville_locatif": "La Teste-de-Buch",
        "cp": "33260",
        "contexte_local": "La Teste-de-Buch, plus grande commune du bassin d'Arcachon par la superficie, compte une densité exceptionnelle de piscines privées dans les lotissements de Cazaux, du Pyla et du centre. Les sols sableux posent des défis spécifiques : affaissement léger des canalisations enterrées, désaxement des raccords, besoin de reprendre régulièrement l'étanchéité des pièces à sceller.",
        "zones_voisines": "Arcachon, Gujan-Mestras, Biganos, Le Teich",
        "hero_image_alt": "Piscine privée avec sol sableux caractéristique de La Teste-de-Buch, zone d'intervention recherche de fuite",
    },
    {
        "slug": "piscine-gujan-mestras",
        "ville": "Gujan-Mestras",
        "ville_article": "à Gujan-Mestras",
        "ville_locatif": "Gujan-Mestras",
        "cp": "33470",
        "contexte_local": "Commune dynamique du bassin d'Arcachon, Gujan-Mestras compte une forte proportion de résidences secondaires et de maisons familiales équipées de piscines. Le contexte côtier et les sols sableux favorisent des problèmes spécifiques aux canalisations enterrées ainsi qu'aux joints des pièces à sceller, soumis aux variations thermiques importantes entre l'hiver humide et l'été chaud.",
        "zones_voisines": "La Teste-de-Buch, Le Teich, Biganos, Arcachon",
        "hero_image_alt": "Piscine privée dans une maison du Bassin d'Arcachon à Gujan-Mestras, zone d'intervention recherche de fuite",
    },
    {
        "slug": "piscine-libourne",
        "ville": "Libourne",
        "ville_article": "à Libourne",
        "ville_locatif": "Libourne",
        "cp": "33500",
        "contexte_local": "Libourne et les communes du Libournais (Saint-Émilion, Pomerol, Fronsac) comptent de nombreuses piscines dans les propriétés viticoles et les maisons bourgeoises anciennes. Les bassins en béton armé de 20 à 40 ans d'âge nécessitent souvent une attention particulière aux fissures structurelles et à l'étanchéité des angles. Le sol argileux caractéristique de la région peut provoquer des mouvements qui désaxent les canalisations.",
        "zones_voisines": "Saint-Émilion, Saint-Denis-de-Pile, Coutras, Castillon-la-Bataille",
        "hero_image_alt": "Piscine privée dans une propriété du Libournais à Libourne, zone d'intervention recherche de fuite",
    },
    {
        "slug": "piscine-le-bouscat",
        "ville": "Le Bouscat",
        "ville_article": "au Bouscat",
        "ville_locatif": "Le Bouscat",
        "cp": "33110",
        "contexte_local": "Le Bouscat, ville résidentielle limitrophe de Bordeaux, compte de nombreuses piscines dans les quartiers pavillonnaires (Parc Bordelais, La Châtaigneraie, Bourran). Les bassins sont souvent intégrés à des jardins matures avec racines proches, ce qui peut solliciter les canalisations enterrées. Les piscines plus anciennes, avec équipements techniques en sous-sol, nécessitent un diagnostic précis pour distinguer une fuite de bassin d'une fuite de local technique.",
        "zones_voisines": "Bordeaux, Caudéran, Bruges, Eysines, Mérignac",
        "hero_image_alt": "Piscine privée dans un jardin pavillonnaire du Bouscat, zone d'intervention recherche de fuite",
    },
]

def page_piscine_ville(p):
    ville = p["ville"]
    ville_article = p["ville_article"]
    cp = p["cp"]
    slug = p["slug"]

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
    {{
      "@type": "Question",
      "name": "Comment savoir si ma piscine fuit vraiment ou si c'est juste de l'évaporation ?",
      "acceptedAnswer": {{ "@type": "Answer", "text": "Faites le test du seau : posez un seau rempli d'eau sur la première marche de la piscine, marquez le niveau. Après 24 à 48 heures sans baignade et sans remise à niveau, comparez. Si le seau et la piscine baissent pareillement, c'est de l'évaporation. Si la piscine baisse plus, il y a une fuite. L'évaporation normale en Gironde est de 3 à 5 mm par jour l'été, 0 à 2 mm au printemps." }}
    }},
    {{
      "@type": "Question",
      "name": "Faut-il vidanger la piscine pour localiser la fuite ?",
      "acceptedAnswer": {{ "@type": "Answer", "text": "Non, dans 95 pourcent des cas. Le colorant fluorescéine, l'écoute électro-acoustique et le test de pression des canalisations localisent la fuite sans vidange. La vidange est à éviter : elle peut endommager le liner, faire remonter la nappe phréatique sous le bassin et coûte 1000 à 2000€ en eau et produits de remise en service." }}
    }},
    {{
      "@type": "Question",
      "name": "Combien coûte une recherche de fuite sur une piscine à Bordeaux ?",
      "acceptedAnswer": {{ "@type": "Answer", "text": "Le tarif d'une recherche de fuite piscine se situe entre 300 et 700 euros HT selon la taille du bassin, les méthodes à combiner et la complexité de l'installation (piscine miroir, débordement, chauffée). Ce coût est souvent pris en charge par votre assurance habitation dans le cadre de la garantie dégâts des eaux, sur présentation de notre rapport technique." }}
    }},
    {{
      "@type": "Question",
      "name": "La recherche de fuite piscine est-elle remboursée par l'assurance ?",
      "acceptedAnswer": {{ "@type": "Answer", "text": "Oui, la plupart des contrats multirisques habitation couvrent la recherche de fuite sur piscine au titre de la garantie recherche de fuite. Notre rapport détaillé (photos, méthodes employées, point de fuite localisé) est accepté par les principaux assureurs. Déclarez le sinistre dans les 5 jours ouvrables après constat." }}
    }},
    {{
      "@type": "Question",
      "name": "Quelles sont les fuites les plus fréquentes sur piscine ?",
      "acceptedAnswer": {{ "@type": "Answer", "text": "Par ordre de fréquence : fuite sur liner PVC (pli, perforation, soudure), fuite au niveau du skimmer ou de la buse de refoulement (joint fissuré), fuite sur canalisation enterrée (raccord ou fissure), fuite de la bonde de fond, fissure structurelle du bassin béton, fuite sur la ligne d'eau ou les margelles." }}
    }},
    {{
      "@type": "Question",
      "name": "Intervenez-vous en urgence sur une piscine qui perd beaucoup d'eau ?",
      "acceptedAnswer": {{ "@type": "Answer", "text": "Oui, nous intervenons sous 24 à 48h sur Bordeaux et sa métropole pour les fuites actives importantes (perte supérieure à 5 cm par jour). Pour limiter les dégâts en attendant, coupez l'arrivée d'eau de remplissage automatique et maintenez le niveau juste au-dessus du skimmer pour que la filtration continue de tourner." }}
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

<section class="section section-alt" id="methodes">
  <div class="container" style="max-width:1080px;">
    <h2>Comment on localise une fuite de piscine sans vidange</h2>
    <p>Chaque méthode cible un type de fuite précis. Sur un chantier, nos techniciens combinent deux à quatre techniques pour isoler la source du problème avec certitude.</p>

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
    <h2>Piscines à Bordeaux et sa métropole : les spécificités locales</h2>
    <p>{p['contexte_local']}</p>

    <figure style="margin:1.5rem 0;">
      <img src="/assets/technicien-recherche-fuite-piscine.webp" alt="Technicien spécialisé en recherche de fuite de piscine intervenant sur un bassin privé en Gironde" width="1600" height="1067" loading="lazy" style="width:100%;max-height:360px;height:auto;object-fit:cover;border-radius:12px;display:block;">
    </figure>

    <h3>Terrain argileux et mouvements de sol</h3>
    <p>Une partie du territoire bordelais repose sur des sols argileux sensibles au retrait-gonflement selon la pluviométrie. Ces mouvements de terrain peuvent désaxer les canalisations enterrées autour de la piscine, provoquer des fissures sur les dalles de plage et, à terme, sur la structure du bassin. Nous prenons systématiquement en compte ce paramètre géologique lors du diagnostic.</p>

    <h3>Piscines du Bassin d'Arcachon et sable</h3>
    <p>Dans les communes du bassin (La Teste-de-Buch, Gujan-Mestras, Arcachon, Andernos), les piscines posées sur sable nécessitent une attention particulière aux raccords des canalisations enterrées, qui subissent micro-mouvements permanents et corrosion par l'air salin.</p>

    <h3>Piscines anciennes de propriétés viticoles (Médoc)</h3>
    <p>Les piscines en béton projeté des chais et domaines viticoles ont souvent 30 à 50 ans. Les techniques de l'époque (étanchéité par enduit ciment, margelles pierre scellées au mortier) n'ont pas toujours bien vieilli. Notre méthodologie intègre ces bassins anciens où la fuite peut se cacher derrière un simple défaut d'étanchéité aux angles ou au contact margelle/bassin.</p>

    <h3>Zones d'intervention autour de {ville}</h3>
    <p>Nous intervenons sous 24 à 48h sur l'ensemble de la métropole bordelaise : {p['zones_voisines']}, ainsi que dans tout le département de la Gironde pour les piscines du Bassin d'Arcachon, du Médoc et du Libournais.</p>
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
    <h2>Questions fréquentes sur la recherche de fuite piscine</h2>

    <h3>Comment savoir si ma piscine fuit vraiment ou si c'est juste de l'évaporation ?</h3>
    <p>Faites le test du seau : posez un seau rempli d'eau sur la première marche de la piscine, marquez le niveau. Après 24 à 48 heures sans baignade et sans remise à niveau, comparez. Si le seau et la piscine baissent pareillement, c'est de l'évaporation. Si la piscine baisse plus, il y a une fuite. L'évaporation normale en Gironde est de 3 à 5 mm par jour l'été.</p>

    <h3>Faut-il vidanger la piscine pour localiser la fuite ?</h3>
    <p>Non, dans 95 pourcent des cas. Le colorant fluorescéine, l'écoute électro-acoustique et le test de pression des canalisations localisent la fuite sans vidange. La vidange est à éviter : elle peut endommager le liner, faire remonter la nappe phréatique sous le bassin et coûte 1 000 à 2 000 € en eau et produits de remise en service.</p>

    <h3>Combien coûte une recherche de fuite sur une piscine à Bordeaux ?</h3>
    <p>Le tarif d'une recherche de fuite piscine se situe entre 300 et 700 euros HT selon la taille du bassin, les méthodes à combiner et la complexité de l'installation. Ce coût est souvent pris en charge par votre assurance habitation dans le cadre de la garantie dégâts des eaux.</p>

    <h3>La recherche de fuite piscine est-elle remboursée par l'assurance ?</h3>
    <p>Oui, la plupart des contrats multirisques habitation couvrent la recherche de fuite sur piscine au titre de la garantie recherche de fuite. Notre rapport détaillé (photos, méthodes employées, point de fuite localisé) est accepté par les principaux assureurs. Déclarez le sinistre dans les 5 jours ouvrables après constat.</p>

    <h3>Quelles sont les fuites les plus fréquentes sur piscine ?</h3>
    <p>Par ordre de fréquence : fuite sur liner PVC (pli, perforation, soudure), fuite au niveau du skimmer ou de la buse de refoulement (joint fissuré), fuite sur canalisation enterrée (raccord ou fissure), fuite de la bonde de fond, fissure structurelle du bassin béton, fuite sur la ligne d'eau ou les margelles.</p>

    <h3>Intervenez-vous en urgence sur une piscine qui perd beaucoup d'eau ?</h3>
    <p>Oui, nous intervenons sous 24 à 48h sur Bordeaux et sa métropole pour les fuites actives importantes (perte supérieure à 5 cm par jour). Pour limiter les dégâts en attendant, coupez l'arrivée d'eau de remplissage automatique et maintenez le niveau juste au-dessus du skimmer pour que la filtration continue de tourner.</p>

    <div style="margin-top:2rem;text-align:center;">
      <a href="/devis/" class="btn btn-gold">Demander un devis pour ma piscine</a>
    </div>
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

    print('[7b] Pages use case — piscine par ville...')
    for p in PISCINE_PAGES:
        write(f'detection-fuite/{p["slug"]}/index.html', page_piscine_ville(p))

    print('[7c] Pages use case — urgence par ville...')
    for p in URGENCE_PAGES:
        write(f'detection-fuite/{p["slug"]}/index.html', page_urgence_ville(p))

    print('[7d] Page use case — fuite apres compteur...')
    write('detection-fuite/fuite-apres-compteur/index.html', page_fuite_apres_compteur())

    print('[8/8] Fichiers techniques...')
    write('sitemap.xml', gen_sitemap())
    write('robots.txt', ROBOTS)
    write('vercel.json', VERCEL)

    total = 2 + 3 + 1 + len(GUIDE_PAGES) + 1 + len(VILLES)*2 + 3
    print(f'\n✓ {total} fichiers générés avec succès.\n')

if __name__ == '__main__':
    main()
