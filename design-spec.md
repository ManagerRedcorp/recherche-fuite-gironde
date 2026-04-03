# Spécification design — recherche-fuite-gironde.fr

## Concept directeur

**"Diagnostic précis, intervention certaine"**

L'identité visuelle s'éloigne des codes visuels classiques de la plomberie (bleu roi, clé à molette, fond gris) pour adopter un registre de **précision technique et de sobriété professionnelle**. La référence n'est pas le plombier de quartier, c'est le cabinet d'expertise qui intervient vite et bien.

Couleur dominante : un **vert profond** (pas de vert criard) évoquant à la fois l'eau, la Gironde, et la résolution — le retour au normal. Typographie sans-serif géométrique pour l'autorité, serif discret pour la chaleur humaine en corps de texte.

---

## 1. Palette de couleurs

### Primaires
| Rôle | Nom | Hex | Usage |
|------|-----|-----|-------|
| Primaire profond | `--c-primary` | `#0D3B2E` | Fond header, footer, blocs forts |
| Primaire moyen | `--c-primary-mid` | `#155740` | Hover boutons, accents secondaires |
| Primaire clair | `--c-primary-light` | `#1E7A57` | Boutons CTA principaux |

### Accent
| Rôle | Nom | Hex | Usage |
|------|-----|-----|-------|
| Accent chaud | `--c-accent` | `#E8A838` | Badges urgence, étoiles, highlights |
| Accent hover | `--c-accent-dark` | `#C48A1A` | Hover état accent |

### Neutres
| Rôle | Nom | Hex | Usage |
|------|-----|-----|-------|
| Fond page | `--c-bg` | `#F7F6F2` | Background général (blanc cassé chaud) |
| Fond section alternée | `--c-bg-alt` | `#EEECEA` | Sections intercalées |
| Fond carte | `--c-surface` | `#FFFFFF` | Cards, formulaires |
| Bordures | `--c-border` | `#D8D4CC` | Séparateurs, contours |
| Texte principal | `--c-text` | `#1A1A18` | Corps de texte |
| Texte secondaire | `--c-text-muted` | `#5C5B55` | Labels, sous-titres, captions |
| Texte clair sur fond sombre | `--c-text-inv` | `#F7F6F2` | Texte sur fond primaire |

### Sémantique
| Rôle | Nom | Hex | Usage |
|------|-----|-----|-------|
| Succès / Confirmation | `--c-success` | `#1E7A57` | (= primary-light) |
| Alerte / Urgence | `--c-alert` | `#C0392B` | Badge "fuite active", alertes |

---

## 2. Typographie

### Familles Google Fonts
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Syne:wght@700;800&display=swap" rel="stylesheet">
```

- **Syne** : titres H1/H2/H3 — géométrique, unique, mémorable sans être décorative
- **DM Sans** : navigation, corps, UI — lisible, moderne, neutre

### Échelle typographique

| Élément | Famille | Weight | Taille | Line-height | Lettre-spacing |
|---------|---------|--------|--------|-------------|----------------|
| H1 hero | Syne | 800 | `clamp(2.25rem, 5vw, 3.5rem)` | 1.1 | -0.02em |
| H1 page ville | Syne | 700 | `clamp(1.75rem, 4vw, 2.75rem)` | 1.15 | -0.015em |
| H2 section | Syne | 700 | `clamp(1.5rem, 3vw, 2.25rem)` | 1.2 | -0.01em |
| H3 card | Syne | 700 | `1.25rem` (20px) | 1.3 | 0 |
| Navigation | DM Sans | 500 | `0.9375rem` (15px) | 1 | 0.04em |
| Paragraphe | DM Sans | 400 | `1rem` (16px) | 1.7 | 0 |
| Paragraphe lead | DM Sans | 400 | `1.125rem` (18px) | 1.65 | 0 |
| Label / Caption | DM Sans | 500 | `0.8125rem` (13px) | 1.4 | 0.06em |
| Bouton | DM Sans | 600 | `0.9375rem` (15px) | 1 | 0.03em |

---

## 3. Design system — Variables CSS

```css
/* === COULEURS === */
--c-primary:       #0D3B2E;
--c-primary-mid:   #155740;
--c-primary-light: #1E7A57;
--c-accent:        #E8A838;
--c-accent-dark:   #C48A1A;
--c-bg:            #F7F6F2;
--c-bg-alt:        #EEECEA;
--c-surface:       #FFFFFF;
--c-border:        #D8D4CC;
--c-text:          #1A1A18;
--c-text-muted:    #5C5B55;
--c-text-inv:      #F7F6F2;
--c-alert:         #C0392B;

/* === TYPOGRAPHIE === */
--font-title: 'Syne', sans-serif;
--font-body:  'DM Sans', sans-serif;

/* === ESPACEMENTS (base 8px) === */
--sp-1:  0.5rem;   /* 8px */
--sp-2:  1rem;     /* 16px */
--sp-3:  1.5rem;   /* 24px */
--sp-4:  2rem;     /* 32px */
--sp-5:  3rem;     /* 48px */
--sp-6:  4rem;     /* 64px */
--sp-7:  6rem;     /* 96px */

/* === RAYONS === */
--radius-sm:  4px;
--radius-md:  8px;
--radius-lg:  16px;
--radius-xl:  24px;

/* === OMBRES === */
--shadow-sm: 0 1px 3px rgba(13,59,46,0.08), 0 1px 2px rgba(13,59,46,0.04);
--shadow-md: 0 4px 12px rgba(13,59,46,0.10), 0 2px 4px rgba(13,59,46,0.06);
--shadow-lg: 0 8px 24px rgba(13,59,46,0.12), 0 4px 8px rgba(13,59,46,0.06);

/* === CONTENEUR === */
--container-max: 1160px;
--container-pad: clamp(1rem, 5vw, 2.5rem);

/* === TRANSITIONS === */
--t-fast:   150ms ease;
--t-normal: 250ms ease;
```

---

## 4. Layout des pages

### 4.1 Header / Navigation

**Structure :**
```
[Logo texte] .................. [Nav liens] [Bouton CTA]
```

**Spécifications :**
- `position: sticky; top: 0; z-index: 100`
- Fond : `var(--c-primary)` — pas de fond blanc (différenciation forte)
- Hauteur : 64px desktop, 56px mobile
- Logo texte : "Recherche Fuite **Gironde**" — "Recherche Fuite" en DM Sans 500, "Gironde" en Syne 800, couleur accent `#E8A838`
- Liens nav : DM Sans 500, `0.9375rem`, couleur `rgba(247,246,242,0.80)`, hover `#F7F6F2`, lettre-spacing 0.04em — pages : Accueil / Nos services / Villes / Contact
- Bouton CTA header : "Demander un devis" — style pill, fond accent `#E8A838`, texte `#0D3B2E`, DM Sans 600
- Border-bottom : `1px solid rgba(255,255,255,0.08)`
- Mobile : hamburger menu, menu overlay fond `#0D3B2E`

---

### 4.2 Section Hero (page accueil)

**Layout :**
```
[Fond : #0D3B2E avec texture légère en motif de gouttes d'eau SVG, très subtile, opacité 4%]

  Badge "Intervention en Gironde • Département 33"
  
  H1 : "Vous avez une fuite d'eau ?
        Nous la trouvons."

  Lead : Détection non destructive, sans démolition inutile.
         Résultat garanti sur toute la Gironde.

  [Bouton primaire : "Demander un devis gratuit"]  [Bouton secondaire : "Nos méthodes"]

  ─────────────────────────────────────────────
  [Icône clock] Intervention  [Icône tick-circle] Sans  [Icône shield] Résultat
  rapide                      démolition               garanti
  ─────────────────────────────────────────────
```

**Spécifications :**
- Fond : `var(--c-primary)` — texte `var(--c-text-inv)`
- Padding : `var(--sp-7)` top/bottom — au moins `min(96px, 12vh)` top
- Badge : fond `rgba(232,168,56,0.15)`, bordure `rgba(232,168,56,0.40)`, texte `#E8A838`, DM Sans 500 13px, uppercase lettre-spacing 0.08em, border-radius pill
- H1 : Syne 800, `clamp(2.25rem, 5vw, 3.5rem)`, couleur blanc `#F7F6F2`, retour à la ligne intentionnel sur "Nous la trouvons." — cette ligne en couleur accent `#E8A838`
- Lead : DM Sans 400 18px, couleur `rgba(247,246,242,0.75)`, max-width 560px
- Bouton primaire : fond `#E8A838`, texte `#0D3B2E`, DM Sans 600 15px, padding `14px 28px`, border-radius 6px
- Bouton secondaire : fond transparent, bordure `rgba(247,246,242,0.30)`, texte `rgba(247,246,242,0.85)`, même padding
- Barre de stats en bas : 3 colonnes, fond `rgba(255,255,255,0.05)`, bordure top `rgba(255,255,255,0.08)`, icônes `#E8A838` 20px

---

### 4.3 Section "Nos services"

**Layout :** Grille 2 colonnes desktop, 1 colonne mobile

**Titre de section :** H2 centré, eyebrow label au-dessus "NOS SERVICES" en DM Sans 500 13px lettre-spacing 0.08em couleur primary-light

**Cards services (2 cards) :**

**Card 1 — Détection de fuites**
- Icône SVG : `search` (24px) dans un carré 48px fond `rgba(30,122,87,0.10)` border-radius 10px
- H3 : "Détection de fuite non destructive"
- Paragraphe : 3-4 lignes de description, DM Sans 400 16px
- Liste à puces (3 items) avec icône tick-circle couleur primary-light
- Lien "En savoir plus →" couleur primary-light

**Card 2 — Chemisage**
- Icône SVG : `refresh` (24px) dans carré identique
- H3 : "Chemisage de canalisation"
- Même structure

**Spécifications cards :**
- Fond `var(--c-surface)`, bordure `1px solid var(--c-border)`, border-radius `var(--radius-lg)`
- Padding : `var(--sp-4)` desktop, `var(--sp-3)` mobile
- Shadow : `var(--shadow-sm)`, hover `var(--shadow-md)`
- Pas de transition sur hover — juste changement d'ombre statique via classe

---

### 4.4 Section "Pourquoi nous choisir"

**Layout :** Grille 3 colonnes desktop → 2 colonnes tablette → 1 colonne mobile

**Fond :** `var(--c-bg-alt)` pour différencier

**6 arguments, chacun composé de :**
- Icône SVG 24px dans cercle 48px fond `rgba(13,59,46,0.08)` couleur `var(--c-primary)`
- H3 court (3-5 mots)
- Paragraphe court (2-3 lignes)

**Arguments :**
1. `clock` — "Réactivité garantie" — Intervention sous 48h sur toute la Gironde
2. `tick-circle` — "Sans démolition" — Techniques non destructives, vos murs restent intacts
3. `search` — "Diagnostic précis" — Caméras endoscopiques et acoustique numérique
4. `map-pin` — "30 villes couvertes" — De Bordeaux à Arcachon, tout le département 33
5. `shield` (tick-badge) — "Travail certifié" — Artisans qualifiés RGE, devis gratuit et transparent
6. `lifebuoy` — "Suivi complet" — De la détection à la réparation, un seul interlocuteur

---

### 4.5 Section "Villes couvertes"

**Layout :** Grille adaptative `repeat(auto-fill, minmax(160px, 1fr))`

**Titre :** H2 + paragraphe intro "Nous intervenons dans 30 communes de Gironde (33)."

**Chaque entrée :** Lien `<a href="/ville-slug/">` — format compact :
```
[map-pin 14px] Bordeaux
               33000
```
- DM Sans 500 14px pour le nom de ville
- DM Sans 400 12px couleur muted pour le code postal
- Fond `var(--c-surface)`, bordure `1px solid var(--c-border)`, border-radius `var(--radius-md)`
- Padding `12px 16px`
- Couleur lien `var(--c-text)`, hover fond `var(--c-primary)` texte `var(--c-text-inv)` icône `var(--c-accent)`
- Pas de soulignement

**Mise en avant de Bordeaux :** card légèrement plus grande avec badge "Principale"

---

### 4.6 Section "Témoignages"

**Layout :** Grille 3 colonnes desktop, 1 colonne mobile

**Sans photos** — Initiales en avatar coloré (fond primaire, texte accent)

**Structure d'une carte témoignage :**
```
★★★★★  (étoiles couleur accent)

"Texte du témoignage entre guillemets typographiques français."

─── Prénom N. · [map-pin 12px] Ville, 33XXX
```

**Spécifications :**
- Fond `var(--c-surface)`, bordure `1px solid var(--c-border)`, border-radius `var(--radius-lg)`
- Padding `var(--sp-3) var(--sp-3)`
- Guillemets ouvrants : pseudo-élément `::before` avec `"` en Syne 800 `4rem` couleur `rgba(30,122,87,0.12)`, position absolue en haut à gauche de la card
- Texte témoignage : DM Sans 400 italic 15px, couleur `var(--c-text)`, line-height 1.65
- Attribution : DM Sans 500 13px, couleur `var(--c-text-muted)`
- Étoiles : `★` character, couleur `#E8A838`, `1rem`

**3 témoignages exemple :**
1. M. Lefebvre · Bordeaux 33000 — "Intervention rapide pour une fuite sous dallage. Aucune destruction, la fuite trouvée en 2h. Résultat parfait."
2. C. Moreau · Mérignac 33700 — "Très professionnel. Devis clair, technique d'acoustique impressionnante. Je recommande vivement."
3. Famille Dupont · Arcachon 33120 — "Fuite sur réseau enterré. Trouvée sans creuser. Chemisage effectué dans la foulée. Merci !"

---

### 4.7 Section "Formulaire de contact" (CTA)

**Layout :** 2 colonnes desktop (texte gauche, formulaire droite) → 1 colonne mobile

**Fond :** `var(--c-primary)` — texte clair

**Côté texte :**
- Badge "Devis gratuit & sans engagement"
- H2 : "Décrivez votre problème, nous vous répondons"
- Checklist 3 items avec tick-circle accent : Gratuit / Rapide / Sans engagement

**Formulaire (FormSubmit) :**
```html
<form action="https://formsubmit.co/VOTRE_EMAIL" method="POST">
  Prénom + Nom (2 colonnes)
  Ville (select liste des 30 villes)
  Type de problème (select)
  Message (textarea)
  [Champs cachés FormSubmit]
  [Bouton "Envoyer ma demande"]
</form>
```

**Spécifications formulaire :**
- Labels : DM Sans 500 13px, uppercase lettre-spacing 0.06em, couleur `rgba(247,246,242,0.70)`
- Inputs : fond `rgba(255,255,255,0.08)`, bordure `1px solid rgba(255,255,255,0.15)`, couleur texte `var(--c-text-inv)`, border-radius `var(--radius-md)`, padding `12px 14px`
- Focus : bordure `var(--c-accent)`, outline none, box-shadow `0 0 0 3px rgba(232,168,56,0.20)`
- Bouton submit : pleine largeur, fond `var(--c-accent)`, texte `var(--c-primary)`, DM Sans 600 15px, padding `15px`, border-radius `var(--radius-md)`
- Placeholder : couleur `rgba(247,246,242,0.35)`

---

### 4.8 Footer

**Layout :** 4 colonnes desktop → 2 colonnes tablette → 1 colonne mobile

**Fond :** `#091F18` (encore plus sombre que --c-primary)

**Colonnes :**
1. **Logo + description** : Logo texte + "Spécialiste de la recherche de fuites en Gironde (33). Intervention sur 30 communes." + Mentions légales
2. **Nos services** : Liens vers /detection-fuite/, /chemisage-canalisation/, /guide/
3. **Villes principales** : 8 villes les plus peuplées en liens
4. **Informations** : Liens internes supplémentaires (Plan du site, Mentions légales, Politique confidentialité)

**Séparateur copyright :**
- Fond `rgba(255,255,255,0.04)`, texte `rgba(247,246,242,0.40)`, DM Sans 400 13px
- "© 2025 Recherche Fuite Gironde — Site d'information et de mise en relation"

**Pas de téléphone ni email visible.**

---

### 4.9 Page ville (template)

**Structure :**
```
[Header sticky]

[Hero mini — fond primary, hauteur 260px desktop]
  Badge département  →  H1 "Recherche de fuite à [Ville] (33XXX)"
  Breadcrumb : Accueil > Villes > [Ville]

[Section intro — 2 colonnes]
  Texte SEO local (H2, paragraphes, quartiers mentionnés)
  | Card CTA flottante (sticky desktop) :
  |   "Intervention à [Ville]"
  |   [Formulaire court : Nom + Message + Submit]

[Section "Nos interventions à [Ville]"]
  Liste services avec contexte local (H2 + 3 cards)

[Section "Zone d'intervention"]
  Paragraphe sur les quartiers de la ville
  Liste des villes voisines (maillage interne)

[Section témoignages locaux]
  2 témoignages filtrés sur la ville ou villes proches

[Section formulaire complet]

[Section maillage — "Autres villes couvertes"]
  Grille compacte des autres villes (max 12 en avant)

[Footer]
```

---

## 5. CSS base complet

Voir fichier `assets/css/style.css` généré à partir de ces spécifications.

**Composants réutilisables :**

### Boutons
```
.btn-primary    → fond accent, texte primary, hover fond accent-dark
.btn-secondary  → fond transparent, bordure 1px surface, texte surface, hover fond rgba blanc 10%
.btn-ghost      → fond transparent, texte primary-light, hover fond rgba primary-light 8%
```
Tous les boutons : DM Sans 600 15px, lettre-spacing 0.03em, border-radius 6px, padding 13px 24px, curseur pointer

### Cards
```
.card           → base card (fond surface, bordure, radius-lg, shadow-sm)
.card-service   → card service avec icône top
.card-ville     → link card compact pour les villes
.card-temoignage → card témoignage sans photo
```

### Badges
```
.badge          → label inline (fond semi-transparent, texte, border-radius pill)
.badge-accent   → variant accent/doré
.badge-alert    → variant rouge urgent
```

### Formulaire
```
.form-group     → wrapper label + input
.form-label     → label stylisé
.form-input     → input/select/textarea
.form-select    → select avec chevron custom SVG
```

### Layout
```
.container      → max-width 1160px, centré, padding horizontal responsive
.section        → padding vertical sp-6/sp-7
.section-alt    → idem sur fond bg-alt
.section-dark   → idem sur fond primary
.grid-2         → CSS grid 2 colonnes, gap sp-4
.grid-3         → CSS grid 3 colonnes, gap sp-3
.grid-villes    → auto-fill minmax(160px,1fr)
```

### Icônes
```
.icon           → taille 20px, display inline-block, vertical-align middle
.icon-sm        → 16px
.icon-lg        → 24px
.icon-xl        → 32px
.icon-circle    → fond semi-transparent, border-radius 50%, padding 12px
```

---

## 6. Arborescence des fichiers

```
/
├── index.html
├── detection-fuite/index.html
├── chemisage-canalisation/index.html
├── contact/index.html
├── mentions-legales/index.html
├── plan-du-site/index.html
├── villes/
│   ├── bordeaux/index.html
│   ├── merignac/index.html
│   ├── pessac/index.html
│   └── ... (30 villes)
├── assets/
│   ├── css/
│   │   └── style.css
│   ├── icons/
│   │   ├── map-pin.svg
│   │   ├── clock.svg
│   │   ├── tick-circle.svg
│   │   ├── alert-circle.svg
│   │   ├── home.svg
│   │   ├── search.svg
│   │   ├── star.svg
│   │   ├── mail.svg
│   │   ├── lock.svg
│   │   ├── tick-badge.svg
│   │   ├── help-circle.svg
│   │   ├── lifebuoy.svg
│   │   ├── refresh.svg
│   │   └── shield.svg → (alias tick-badge.svg)
│   └── images/
│       └── (WebP à ajouter manuellement)
├── sitemap.xml
├── sitemap.html
├── robots.txt
└── _redirects
```

---

## 7. Règles SEO et techniques

### Balises Title
- Format : `[Mot-clé principal] [ville] [33XXX]` — pas de séparateur
- Exemple : `Recherche fuite eau Bordeaux 33000 détection non destructive`
- Max 60 caractères

### Meta descriptions
- 150-160 caractères
- Toujours : ville + code postal + bénéfice + appel à l'action
- Exemple : `Fuite d'eau à Bordeaux ? Détection non destructive en 48h, sans démolition. Devis gratuit, intervention rapide sur toute la Gironde (33). Contactez-nous.`

### Schema.org JSON-LD (par page ville)
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Recherche Fuite Gironde",
  "description": "Spécialiste détection de fuites à [Ville]",
  "areaServed": "[Ville], [Code postal], Gironde",
  "serviceType": ["Détection de fuite", "Chemisage de canalisation"],
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "[Ville]",
    "postalCode": "[Code postal]",
    "addressCountry": "FR"
  }
}
```

### FormSubmit (pas Netlify Forms)
- Action : `https://formsubmit.co/VOTRE_EMAIL`
- Champs cachés : `_subject`, `_captcha`, `_next`, `_template`
- Pas de JavaScript requis

### Canonical
- Chaque page : `<link rel="canonical" href="https://recherche-fuite-gironde.fr/[chemin]/">`

### Redirections `_redirects`
```
/villes/:ville  /villes/:ville/  301
/*.html         /:splat          301
http://recherche-fuite-gironde.fr/*  https://recherche-fuite-gironde.fr/:splat  301
```

---

## 8. Règles rédactionnelles

- **Majuscules H1/H2/H3** : premier mot uniquement (règle typographique française)
- **Guillemets** : « » (guillemets français) — jamais "..."
- **Ponctuation espace** : espace insécable avant : ; ? ! (` ` ou `&nbsp;`)
- **Tirets** : tirets demi-cadratins (–) pour les incises, pas de tirets cadratin (—)
- **Pas de formulations IA** : éviter "Dans un monde où...", "Il est important de...", "N'hésitez pas à..."
- **Tons** : direct, expert, rassurant — jamais commercial agressif
- **Verbes d'action** : "Trouvons", "Détectons", "Intervenons", "Réparons"
