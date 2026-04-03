#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
generate_cities.py
Génère les pages HTML pour chaque ville (détection + chemisage).
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "villes.json"), encoding="utf-8") as f:
    raw = json.load(f)

# Support deux formats : liste directe ou objet {villes: [...]}
if isinstance(raw, list):
    villes = raw
else:
    villes = raw.get("villes", raw.get("cities", []))

VILLES_LIST = villes  # référence globale


def header_html():
    return """  <input type="checkbox" id="nav-check" aria-hidden="true">
  <header class="site-header">
    <div class="container header-inner">
      <a href="/" class="logo">Recherche Fuite <span>Gironde</span></a>
      <nav class="nav" id="main-nav">
        <a href="/">Accueil</a>
        <div class="nav-dropdown">
          <a href="/detection-fuite/">Services</a>
          <div class="nav-dropdown-menu">
            <a href="/detection-fuite/">Détection de fuite</a>
            <a href="/chemisage-canalisation/">Chemisage de canalisation</a>
          </div>
        </div>
        <div class="nav-dropdown">
          <a href="/villes/bordeaux/">Villes</a>
          <div class="nav-dropdown-menu">
            <a href="/villes/bordeaux/">Bordeaux</a>
            <a href="/villes/merignac/">Mérignac</a>
            <a href="/villes/pessac/">Pessac</a>
            <a href="/villes/arcachon/">Arcachon</a>
            <a href="/villes/libourne/">Libourne</a>
            <a href="/plan-du-site/">Toutes les villes &rarr;</a>
          </div>
        </div>
        <a href="/guide/">Guide</a>
        <a href="/contact/">Contact</a>
      </nav>
      <a href="/contact/" class="btn btn--accent btn--sm" style="white-space:nowrap;">Demander un devis</a>
      <label for="nav-check" class="nav-toggle" aria-label="Menu">
        <span></span><span></span><span></span>
      </label>
    </div>
  </header>"""


def footer_html():
    return """  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <a href="/" class="logo">Recherche Fuite <span>Gironde</span></a>
          <p>Spécialistes de la détection et de la recherche de fuites d'eau en Gironde (33). Méthodes non destructives, rapport technique officiel.</p>
        </div>
        <div class="footer-col">
          <h4>Services</h4>
          <ul>
            <li><a href="/detection-fuite/">Détection de fuite</a></li>
            <li><a href="/chemisage-canalisation/">Chemisage de canalisation</a></li>
            <li><a href="/guide/fuite-sous-dalle/">Fuite sous dalle</a></li>
            <li><a href="/guide/fuite-canalisation-enterree/">Fuite enterrée</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Villes</h4>
          <ul>
            <li><a href="/villes/bordeaux/">Bordeaux</a></li>
            <li><a href="/villes/merignac/">Mérignac</a></li>
            <li><a href="/villes/pessac/">Pessac</a></li>
            <li><a href="/villes/arcachon/">Arcachon</a></li>
            <li><a href="/villes/libourne/">Libourne</a></li>
            <li><a href="/plan-du-site/">Toutes les villes</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Informations</h4>
          <ul>
            <li><a href="/guide/">Guide pratique</a></li>
            <li><a href="/guide/faq/">FAQ</a></li>
            <li><a href="/contact/">Contact</a></li>
            <li><a href="/mentions-legales/">Mentions légales</a></li>
            <li><a href="/plan-du-site/">Plan du site</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>&copy; 2025 Recherche Fuite Gironde - Tous droits réservés</span>
        <div style="display:flex;gap:1.5rem">
          <a href="/mentions-legales/">Mentions légales</a>
          <a href="/plan-du-site/">Plan du site</a>
        </div>
      </div>
    </div>
  </footer>"""


def form_html(subject_suffix=""):
    subj = "Nouveau contact - Recherche Fuite Gironde"
    if subject_suffix:
        subj += " - " + subject_suffix
    return """  <section class="section section--dark" id="contact">
    <div class="container">
      <span class="section-label">Contact</span>
      <h2 class="section-title text-inv">Décrivez votre situation, nous vous répondons</h2>
      <p class="section-lead text-inv" style="opacity:.75">Remplissez le formulaire. Un technicien vous contacte pour établir un devis.</p>
      <form action="https://formsubmit.co/PLACEHOLDER_EMAIL" method="POST" style="max-width:680px">
        <input type="hidden" name="_subject" value=\"""" + subj + """\">
        <input type="hidden" name="_captcha" value="false">
        <input type="hidden" name="_next" value="https://recherche-fuite-gironde.fr/contact/merci/">
        <input type="hidden" name="_template" value="table">
        <div class="form-grid">
          <div class="form-group">
            <label for="prenom">Prénom</label>
            <input type="text" id="prenom" name="prenom" placeholder="Votre prénom" required>
          </div>
          <div class="form-group">
            <label for="nom">Nom</label>
            <input type="text" id="nom" name="nom" placeholder="Votre nom" required>
          </div>
          <div class="form-group">
            <label for="ville">Ville</label>
            <select id="ville" name="ville" required>
              <option value="">Choisir une ville</option>
              <option>Bordeaux</option><option>Mérignac</option><option>Pessac</option>
              <option>Talence</option><option>Villenave-d'Ornon</option><option>Libourne</option>
              <option>Bègles</option><option>Bruges</option><option>Le Bouscat</option>
              <option>Blanquefort</option><option>Arès</option><option>Arcachon</option>
              <option>Gujan-Mestras</option><option>La Teste-de-Buch</option>
              <option>Andernos-les-Bains</option><option>Saint-Médard-en-Jalles</option>
              <option>Eysines</option><option>Ambarès-et-Lagrave</option>
              <option>Carbon-Blanc</option><option>Lesparre-Médoc</option>
              <option>Langon</option><option>Saint-André-de-Cubzac</option>
              <option>Pauillac</option><option>Saint-Emilion</option>
              <option>Floirac</option><option>Cenon</option><option>Lormont</option>
              <option>Bassens</option><option>Saint-Louis-de-Montferrand</option>
              <option>Mios</option><option>Autre</option>
            </select>
          </div>
          <div class="form-group">
            <label for="type_probleme">Type de problème</label>
            <select id="type_probleme" name="type_probleme" required>
              <option value="">Choisir</option>
              <option>Fuite visible (tuyau, joint)</option>
              <option>Fuite sous dalle</option>
              <option>Fuite canalisation enterrée</option>
              <option>Compteur qui tourne</option>
              <option>Humidité / dégât des eaux</option>
              <option>Chemisage de canalisation</option>
              <option>Autre</option>
            </select>
          </div>
          <div class="form-group full">
            <label for="message">Décrivez votre situation</label>
            <textarea id="message" name="message" placeholder="Depuis combien de temps, symptômes observés, type de logement..." required></textarea>
          </div>
        </div>
        <button type="submit" class="btn btn--accent mt-3">Envoyer ma demande</button>
        <p class="form-note">Aucune donnée personnelle n'est transmise à des tiers. Réponse sous 24h ouvrées.</p>
      </form>
    </div>
  </section>"""


def get_voisines(current_slug, n=6):
    return [v for v in VILLES_LIST if v["slug"] != current_slug][:n]


def other_cities_grid(current_slug, n=12):
    autres = [v for v in VILLES_LIST if v["slug"] != current_slug][:n]
    items = ""
    for v in autres:
        items += '      <a href="/villes/{slug}/" class="city-link">{nom} ({cp})</a>\n'.format(
            slug=v["slug"], nom=v["nom"], cp=v["code_postal"]
        )
    return """  <section class="section section--alt">
    <div class="container">
      <span class="section-label">Zone d'intervention</span>
      <h2 class="section-title">Autres villes couvertes en Gironde</h2>
      <div class="grid-cities">
{items}      </div>
    </div>
  </section>""".format(items=items)


CONTEXTES = {
    "bordeaux": {
        "intro": (
            "Bordeaux concentre un parc immobilier dense et varié : maisons de négoce du XVIIIe siècle "
            "aux Chartrons, immeubles haussmanniens de Saint-Michel, pavillons récents de Caudéran. "
            "Les réseaux d'eau y sont souvent anciens, en plomb ou en fonte, et les fuites y apparaissent "
            "sous diverses formes. Une hausse inexpliquée de votre facture d'eau ou une humidité persistante "
            "dans un mur sont les premiers signes à traiter."
        ),
        "temoignage": (
            '"Notre appartement aux Chartrons affichait une consommation d\'eau anormale depuis deux mois. '
            'La détection acoustique a localisé la fuite dans la canalisation encastrée derrière la salle de bain '
            'sans aucune démolition. Rapport remis en fin d\'intervention." — M. Perez, Bordeaux Chartrons'
        ),
        "specifique": "Le sol souvent argileux de la rive gauche bordelaise amplifie les effets d'une fuite sur canalisation enterrée.",
    },
    "merignac": {
        "intro": (
            "Mérignac est la deuxième ville de Gironde et présente une grande diversité architecturale : "
            "pavillons des années 1970 à Arlac, résidences récentes à Capeyron, maisons de campagne à "
            "Beaudésert. Les canalisations en polyéthylène réticulé des constructions récentes et les vieux "
            "tuyaux en acier galvanisé des maisons plus anciennes présentent des profils de risques différents."
        ),
        "temoignage": (
            '"Fuite sur canalisation enterrée dans notre jardin à Capeyron. Détection en moins d\'une heure, '
            'creusement au bon endroit du premier coup. Très professionnel." — Famille Bonnet, Mérignac'
        ),
        "specifique": "Les sous-sols de Mérignac, souvent remblayés, nécessitent une approche par corrélation acoustique pour les fuites enterrées.",
    },
    "pessac": {
        "intro": (
            "Pessac abrite le campus universitaire de Bordeaux et des quartiers résidentiels comme Saige "
            "et Bersol. Le parc locatif y est important. Les propriétaires bailleurs font régulièrement "
            "appel à nos services pour traiter des fuites avant une remise en location ou suite à un "
            "signalement de locataire."
        ),
        "temoignage": (
            '"Suite à un signalement de mon locataire à Saige, j\'ai fait intervenir l\'équipe. La fuite '
            'était sous la chape, identifiée en 40 minutes. Le rapport a permis de gérer la situation '
            'avec l\'assurance." — M. Aubert, propriétaire bailleur, Pessac'
        ),
        "specifique": "Pessac concentre de nombreuses copropriétés des années 1980 dont les colonnes montantes méritent une vérification régulière.",
    },
    "talence": {
        "intro": (
            "Talence, ville estudiantine bordée de la forêt de pins, compte de nombreuses maisons "
            "individuelles à Thouars et Médoquine. Les vieilles canalisations en plomb y ont souvent "
            "été remplacées, mais des sections résiduelles posent encore des problèmes de fuites chroniques. "
            "Le terrain sablonneux facilite parfois la détection acoustique."
        ),
        "temoignage": (
            '"Ma maison à Médoquine avait une fuite invisible depuis des semaines. La thermographie a permis '
            'de trouver l\'origine dans la dalle, sans toucher au carrelage. Très satisfait." — M. Gaillard, Talence'
        ),
        "specifique": "Les terrains sablonneux de Talence favorisent l'infiltration latérale en cas de fuite sur réseau enterré.",
    },
    "villenave-d-ornon": {
        "intro": (
            "Villenave-d'Ornon s'étend entre la Garonne et les jalles. Le quartier de Chambéry regroupe "
            "des maisons des années 1960-1980 dont les canalisations encastrées commencent à montrer des "
            "signes de vieillissement. La Salargue et le centre-bourg ont quant à eux accueilli des "
            "constructions plus récentes avec des réseaux en PER ou PVC."
        ),
        "temoignage": (
            '"Compteur qui tournait en permanence à Chambéry. L\'équipe a localisé une fuite sur un té '
            'en cuivre sous la dalle du couloir. Intervention propre et efficace." — Mme Roux, Villenave-d\'Ornon'
        ),
        "specifique": "Villenave-d'Ornon, traversée par des jalles, présente des nappes phréatiques hautes qui compliquent parfois le diagnostic de fuite enterrée.",
    },
    "libourne": {
        "intro": (
            "Libourne, ville historique de l'Entre-Deux-Mers, possède un riche patrimoine bâti dans son "
            "centre historique. Les maisons de ville à colombages et les immeubles du XIXe siècle hébergent "
            "souvent des réseaux d'eau vétustes. À Camérat et aux Déroches, les constructions pavillonnaires "
            "récentes ont des profils différents mais présentent aussi leurs propres risques."
        ),
        "temoignage": (
            '"Fuite dans les murs d\'une maison ancienne dans le centre historique de Libourne. Très '
            'compliqué à localiser sans détériorer le bâti. La détection au gaz traceur a permis de trouver '
            'en deux heures." — M. Faucon, Libourne'
        ),
        "specifique": "Le bâti ancien du centre de Libourne nécessite souvent la détection au gaz traceur pour éviter toute dégradation patrimoniale.",
    },
    "begles": {
        "intro": (
            "Bègles, limitrophe de Bordeaux, est en pleine transformation urbaine. Les quartiers d'Yves "
            "Farges et de Terres Neuves accueillent de nouvelles résidences tandis que le centre-ville "
            "conserve des maisons de ville dont les réseaux datent parfois d'avant-guerre. Les fuites y "
            "prennent souvent la forme d'une humidité rampante difficile à attribuer sans diagnostic précis."
        ),
        "temoignage": (
            '"Humidité persistante dans la cuisine de notre maison de ville à Bègles. La détection a '
            'révélé une micro-fuite sur un coude en cuivre dans le plancher. Réparation propre sans '
            'dommage au carrelage." — Mme Leconte, Bègles'
        ),
        "specifique": "Les maisons de ville de Bègles ont souvent des réseaux partiellement rénovés avec des raccords hétérogènes, sources de fuites chroniques.",
    },
    "bruges": {
        "intro": (
            "Bruges, commune résidentielle au nord de Bordeaux, est essentiellement composée de pavillons "
            "individuels. La Croix de Médoc et le centre-bourg concentrent des maisons des années 1970-1990 "
            "avec des canalisations en polyéthylène ou cuivre. Les jardins y sont souvent grands, "
            "ce qui augmente le risque de fuite sur réseau d'arrosage enterré."
        ),
        "temoignage": (
            '"Fuite sur la canalisation d\'alimentation extérieure de notre piscine à Bruges. Détectée '
            'précisément à 1,80 m de profondeur par corrélation acoustique. Aucun dommage au gazon." '
            '— M. Davoine, Bruges'
        ),
        "specifique": "Les propriétés avec piscine ou réseau d'arrosage enterré à Bruges demandent une expertise adaptée aux réseaux à faible pression.",
    },
    "le-bouscat": {
        "intro": (
            "Le Bouscat est une commune résidentielle cossue, collée à Bordeaux. L'Ermitage et La "
            "Licorne abritent de belles maisons bourgeoises dont les installations d'eau datent parfois "
            "des années 1950. Ces réseaux anciens présentent des risques de corrosion. Le centre, plus "
            "dense, concentre des copropriétés où les fuites sur colonnes partagées sont fréquentes."
        ),
        "temoignage": (
            '"Dégât des eaux dans notre appartement du Bouscat : la fuite provenait de la colonne '
            'commune de l\'immeuble. Le rapport que nous avons reçu a été déterminant pour la gestion '
            'du sinistre en copropriété." — Mme Fontaine, Le Bouscat'
        ),
        "specifique": "Les copropriétés des années 1960 du Bouscat ont des colonnes montantes en acier galvanisé soumises à la corrosion et aux micro-fuites.",
    },
    "blanquefort": {
        "intro": (
            "Blanquefort, ville viticole et industrielle, mêle zones résidentielles autour du centre-ville "
            "et secteurs pavillonnaires près des Jalles. Les canalisations en PVC, polyéthylène ou cuivre "
            "y voisinent selon l'époque de construction. La zone industrielle concentre aussi des besoins "
            "professionnels en détection de fuites sur réseaux d'eau industrielle."
        ),
        "temoignage": (
            '"Notre entrepôt à Blanquefort avait une consommation d\'eau anormale. La détection '
            'thermographique a localisé une fuite sur le réseau sprinkler en 90 minutes." '
            '— Gérant d\'entrepôt, zone industrielle de Blanquefort'
        ),
        "specifique": "La zone industrielle de Blanquefort présente des besoins spécifiques pour les réseaux d'incendie (sprinkler) soumis à pression permanente.",
    },
    "ares": {
        "intro": (
            "Arès, au bord du Bassin d'Arcachon, est une commune touristique avec un parc de résidences "
            "secondaires important. Le quartier du Lac et le centre-bourg concentrent des maisons souvent "
            "inhabitées plusieurs mois dans l'année, ce qui peut retarder la détection d'une fuite. "
            "L'humidité du climat bassinais accélère la dégradation des joints et des raccords."
        ),
        "temoignage": (
            '"Notre résidence secondaire à Arès présentait une consommation anormale au retour des vacances. '
            'La fuite était sur l\'alimentation d\'un chauffe-eau sous la dalle technique." '
            '— Famille Millet, Arès'
        ),
        "specifique": "Les résidences secondaires d'Arès sont particulièrement exposées aux fuites non détectées pendant les longues absences hivernales.",
    },
    "arcachon": {
        "intro": (
            "Arcachon est une ville d'exception avec son architecture Belle Époque en Ville d'Hiver "
            "et ses villas balnéaires en Ville d'Été. Le Moulleau, à l'extrémité sud, concentre "
            "des propriétés luxueuses souvent centenaires. Ces bâtisses historiques ont des réseaux "
            "complexes qui nécessitent une intervention à la fois précise et respectueuse du bâti."
        ),
        "temoignage": (
            '"Villa classée en Ville d\'Hiver avec une fuite sous la terrasse. La technique au gaz traceur '
            'a permis de localiser sans toucher aux pierres. Rapport remis pour l\'assurance." '
            '— Mme de Villars, Arcachon Ville d\'Hiver'
        ),
        "specifique": "Les villas Belle Époque d'Arcachon imposent des méthodes de détection particulièrement douces pour préserver les revêtements patrimoniaux.",
    },
    "gujan-mestras": {
        "intro": (
            "Gujan-Mestras, connue pour ses ports ostréicoles, est une commune résidentielle du Bassin "
            "d'Arcachon en forte croissance. Les nouveaux quartiers de Meyran et de La Barbotière accueillent "
            "des maisons récentes en PER, tandis que Larros concentre un habitat plus ancien. "
            "La proximité de l'eau salée du Bassin peut accélérer la corrosion des réseaux extérieurs."
        ),
        "temoignage": (
            '"Fuite dans le vide sanitaire de notre maison à Meyran. La corrélation acoustique a localisé '
            'le point de fuite en 30 minutes. Excellent rapport remis pour notre assurance." '
            '— M. Auzanneau, Gujan-Mestras'
        ),
        "specifique": "Les vides sanitaires des maisons de Gujan-Mestras concentrent souvent les fuites non détectées qui évoluent en dégradation structurelle.",
    },
    "la-teste-de-buch": {
        "intro": (
            "La Teste-de-Buch est la commune la plus étendue de Gironde. Elle englobe des quartiers "
            "très différents : le centre-ville urbain, la station balnéaire de Pyla-sur-Mer et la base "
            "militaire de Cazaux. Les maisons des années 1960-1980 du centre-ville présentent des réseaux "
            "en cuivre parfois fragilisés, tandis que les propriétés de Pyla concentrent des réseaux récents."
        ),
        "temoignage": (
            '"Notre maison de Pyla-sur-Mer présentait une tache d\'humidité sur un mur intérieur. '
            'La thermographie a révélé une fuite sur un coude encastré. Aucun carrelage abîmé." '
            '— Famille Lestrade, Pyla-sur-Mer'
        ),
        "specifique": "Les propriétés de Pyla-sur-Mer, souvent en bois sur pilotis, nécessitent une expertise spécifique pour les fuites sous plancher.",
    },
    "andernos-les-bains": {
        "intro": (
            "Andernos-les-Bains est une station balnéaire familiale avec un parc immobilier composé "
            "de maisons individuelles et de résidences secondaires. Les Abatilles abritent des propriétés "
            "de haut standing, tandis que le quartier du Port concentre un habitat plus modeste "
            "avec des réseaux parfois anciens. Le taux d'humidité élevé du Bassin favorise les condensations "
            "qui peuvent masquer une vraie fuite."
        ),
        "temoignage": (
            '"Fuite sur le réseau d\'arrosage enterré de notre jardin aux Abatilles. La détection a été '
            'rapide malgré la végétation dense. Aucune dégradation du jardin." '
            '— M. Lacombe, Andernos-les-Bains'
        ),
        "specifique": "À Andernos, la nappe phréatique affleure parfois, ce qui peut fausser le diagnostic entre remontée d'eau et fuite de canalisation.",
    },
    "saint-medard-en-jalles": {
        "intro": (
            "Saint-Médard-en-Jalles, en lisière de la forêt des Landes, est une commune résidentielle "
            "avec de nombreux lotissements pavillonnaires à Le Haillan et Caupian. Le centre-bourg conserve "
            "un tissu de maisons plus anciennes. Les terrains forestiers, souvent sableux, présentent des "
            "caractéristiques particulières pour la détection de fuites enterrées."
        ),
        "temoignage": (
            '"Fuite sur la canalisation principale enterrée de notre maison à Le Haillan. La corrélation '
            'acoustique a fonctionné parfaitement malgré le sol sablonneux." '
            '— Mme Cantin, Saint-Médard-en-Jalles'
        ),
        "specifique": "Les terrains sableux de Saint-Médard-en-Jalles favorisent une propagation rapide des fuites, ce qui rend le diagnostic précoce essentiel.",
    },
    "eysines": {
        "intro": (
            "Eysines est une commune résidentielle de la métropole bordelaise, entre Bordeaux et Mérignac. "
            "Le quartier du Phare et Cantinolle regroupent essentiellement des pavillons de la période "
            "1975-2000, avec des réseaux en cuivre ou en polyéthylène. Le centre d'Eysines présente "
            "des maisons plus anciennes aux installations parfois hétérogènes après rénovations successives."
        ),
        "temoignage": (
            '"Après plusieurs années de factures d\'eau élevées à Eysines, la détection a mis en évidence '
            'deux micro-fuites sur des raccords cuivre sous la dalle. Résolu en une journée." '
            '— M. Brousse, Eysines Centre'
        ),
        "specifique": "Les raccords cuivre-PVC des rénovations partielles des années 1990 à Eysines constituent des points de faiblesse fréquents.",
    },
    "ambares-et-lagrave": {
        "intro": (
            "Ambarès-et-Lagrave, au confluent de la Dordogne et de la Garonne, est une commune en "
            "expansion avec des quartiers résidentiels récents aux Quatre-Chemins. Le secteur de Lagrave "
            "conserve un habitat pavillonnaire des années 1970-1980. La proximité des fleuves implique "
            "un risque de remontée d'eau lors des crues, qui peut se confondre avec une fuite interne."
        ),
        "temoignage": (
            '"Humidité dans le sous-sol de notre maison à Lagrave après une crue. La détection a confirmé '
            'qu\'il ne s\'agissait pas d\'une fuite interne mais d\'une infiltration. Rapport clair et utile." '
            '— M. Vidal, Ambarès-et-Lagrave'
        ),
        "specifique": "La proximité des fleuves à Ambarès rend parfois délicat le diagnostic entre fuite interne et infiltration lors des épisodes de crue.",
    },
    "carbon-blanc": {
        "intro": (
            "Carbon-Blanc est une commune résidentielle de la rive droite de la Garonne. Le centre "
            "et Les Coteaux concentrent un habitat pavillonnaire des années 1970-1990. La zone commerciale "
            "attire aussi des locaux professionnels soumis à des contraintes différentes. "
            "Les réseaux en cuivre y présentent des signes de corrosion après 40 ans."
        ),
        "temoignage": (
            '"Notre maison de Carbon-Blanc présentait une boursouflure sur le carrelage de la cuisine. '
            'La fuite était sous la dalle sur le réseau eau chaude. Intervention rapide et propre." '
            '— Mme Tardieu, Carbon-Blanc'
        ),
        "specifique": "Les maisons de Carbon-Blanc construites dans les années 1975-1985 entrent dans la tranche d'âge critique pour les canalisations en cuivre encastrées.",
    },
    "lesparre-medoc": {
        "intro": (
            "Lesparre-Médoc est la sous-préfecture du Médoc, entourée de vignes et de marais. "
            "Le centre-ville concentre des maisons de ville anciennes tandis que les Vignes "
            "accueillent des maisons récentes. La faible densité de population rend les interventions "
            "plus rapides, mais l'éloignement peut retarder la prise en charge."
        ),
        "temoignage": (
            '"Fuite sous le carrelage de notre salle de bains à Lesparre. Malgré la distance, l\'équipe '
            'est venue rapidement. Détection précise au premier passage." '
            '— M. Magne, Lesparre-Médoc'
        ),
        "specifique": "Les maisons de ville du centre de Lesparre, souvent mitoyennes, concentrent des risques de fuites qui impactent les voisins en cas de non-traitement rapide.",
    },
    "langon": {
        "intro": (
            "Langon, aux portes des Graves et du Sauternais, est une ville active sur les Bords de "
            "Garonne. Son centre-ville mêle immeubles haussmanniens et maisons de bourg. Le quartier "
            "de la gare concentre un habitat ouvrier des années 1900-1930 avec des canalisations "
            "historiques parfois en plomb."
        ),
        "temoignage": (
            '"Notre maison ancienne de Langon centre avait une fuite chronique sur le réseau en plomb. '
            'Le diagnostic a confirmé l\'état du réseau et orienté vers un chemisage complet." '
            '— Mme Pérez, Langon'
        ),
        "specifique": "Langon compte encore des sections de réseau en plomb dans les maisons d'avant-guerre, ce qui nécessite une expertise adaptée.",
    },
    "saint-andre-de-cubzac": {
        "intro": (
            "Saint-André-de-Cubzac, à l'entrée du Bourg, est un carrefour routier entre Bordeaux "
            "et l'estuaire de la Gironde. Le centre-bourg abrite des maisons de caractère, tandis "
            "que le quartier du Port et Les Coteaux offrent un habitat pavillonnaire récent. "
            "Les terrains argileux y favorisent les mouvements de sol qui fragilisent les canalisations."
        ),
        "temoignage": (
            '"Notre maison aux Coteaux a subi un mouvement de sol qui a fissuré une canalisation enterrée. '
            'La détection acoustique a permis de localiser la fuite précisément malgré la profondeur." '
            '— M. Jourdan, Saint-André-de-Cubzac'
        ),
        "specifique": "Les argiles gonflantes de Saint-André-de-Cubzac peuvent provoquer des décalages de canalisation, source de fuites à la jonction des tuyaux.",
    },
    "pauillac": {
        "intro": (
            "Pauillac, capitale du vignoble médocain, est une ville à caractère viticole avec un port "
            "sur la Gironde. Le centre-ville et le Port concentrent des habitations anciennes, "
            "tandis que le quartier des Châteaux abrite des domaines viticoles avec des réseaux "
            "d'eau complexes incluant irrigation et process oenologiques."
        ),
        "temoignage": (
            '"Fuite sur le réseau d\'eau du chai de notre propriété viticole à Pauillac. Détection rapide '
            'et précise, rapport technique adapté pour notre assurance professionnelle." '
            '— Régisseur de château, Pauillac'
        ),
        "specifique": "Les propriétés viticoles de Pauillac ont des réseaux d'eau spécifiques qui nécessitent une expertise professionnelle adaptée.",
    },
    "saint-emilion": {
        "intro": (
            "Saint-Emilion, cité médiévale classée au patrimoine mondial de l'Unesco, impose une "
            "grande rigueur dans les interventions en bâtiment. Les maisons de la cité médiévale, "
            "construites sur des grottes et des carrières calcaires, ont des réseaux d'eau intégrés "
            "dans des murs historiques. Toute intervention doit être menée avec la plus grande précision."
        ),
        "temoignage": (
            '"Fuite dans la cave creusée de notre maison de la cité médiévale de Saint-Emilion. '
            'La détection au gaz traceur a permis de localiser sans toucher aux pierres calcaires." '
            '— Propriétaire, Saint-Emilion'
        ),
        "specifique": "Saint-Emilion, classée Unesco, impose une intervention chirurgicale : la détection non destructive y est indispensable.",
    },
    "floirac": {
        "intro": (
            "Floirac est une commune de la rive droite en pleine transition, entre les quartiers "
            "populaires de Cité Guyenne et les hauteurs résidentielles des Hauts de Floirac. "
            "Dravemont concentre un habitat pavillonnaire récent tandis que les maisons plus anciennes "
            "du bas de Floirac ont souvent des réseaux en acier ou en plomb partiellement remplacés."
        ),
        "temoignage": (
            '"Notre maison de Dravemont avait une consommation anormale depuis plusieurs semaines. '
            'La fuite était sur un raccord cuivre sous la cuisine. Détection en 45 minutes." '
            '— Mme Oum, Floirac'
        ),
        "specifique": "La topographie marquée des Hauts de Floirac génère des pressions d'eau variables, facteur de stress sur les assemblages de canalisations.",
    },
    "cenon": {
        "intro": (
            "Cenon surplombe Bordeaux depuis la rive droite. Les Hauts de Cenon offrent des villas "
            "avec vue sur la métropole, tandis que le quartier Palmer et Grézillac concentrent "
            "un habitat social et des copropriétés. Les réseaux d'eau y sont variés selon les "
            "époques de construction, et les copropriétés concentrent des problèmes de fuites sur "
            "parties communes difficiles à attribuer."
        ),
        "temoignage": (
            '"Fuite dans une copropriété de Cenon : difficile de savoir qui était responsable. '
            'Le rapport de détection a clairement identifié l\'origine et la responsabilité." '
            '— Syndic, Cenon'
        ),
        "specifique": "Dans les copropriétés de Cenon, le rapport de détection fait souvent office d'arbitre pour définir la responsabilité entre parties communes et privatives.",
    },
    "lormont": {
        "intro": (
            "Lormont, ville ouvrière de la rive droite en transformation, concentre à la fois "
            "un habitat social ancien à Génicart et des programmes neufs au Bois Fleuri. "
            "Le centre de Lormont conserve un tissu de maisons de bourg des années 1900-1950 "
            "avec des canalisations parfois en plomb ou en fonte."
        ),
        "temoignage": (
            '"Maison ancienne au centre de Lormont : fuite chronique depuis l\'hiver. Détection précise '
            'sur un coude en fonte corrodé sous la cave. Le rapport a permis de décider du chemisage." '
            '— M. Petit, Lormont'
        ),
        "specifique": "Les maisons de bourg du centre de Lormont ont souvent des caves avec réseaux en fonte ou plomb, matériaux à risque après 60 ans de service.",
    },
    "bassens": {
        "intro": (
            "Bassens est une commune industrielle et portuaire sur la Garonne. En dehors de la zone "
            "industrielle et du port fluvial, le centre-bourg abrite un habitat résidentiel tranquille. "
            "Les besoins en détection de fuites y touchent aussi bien les habitations du centre-bourg "
            "que les installations industrielles du port."
        ),
        "temoignage": (
            '"Fuite sur le réseau d\'eau froide d\'un entrepôt du port de Bassens. Intervention rapide '
            'hors des heures ouvrées pour limiter l\'impact. Rapport conforme pour l\'assurance industrielle." '
            '— Responsable technique, Bassens port'
        ),
        "specifique": "Les installations portuaires de Bassens ont des réseaux sous haute pression dont la détection précoce est économiquement critique.",
    },
    "saint-louis-de-montferrand": {
        "intro": (
            "Saint-Louis-de-Montferrand est une petite commune tranquille du Bec d'Ambès, entre "
            "Dordogne et Garonne. Le bourg historique concentre des maisons de caractère, "
            "tandis que le quartier du Fleuve offre une vue directe sur l'estuaire. "
            "La proximité des fleuves crée une humidité ambiante élevée qui peut masquer "
            "les symptômes d'une fuite interne."
        ),
        "temoignage": (
            '"Difficile de distinguer l\'humidité de l\'estuaire d\'une vraie fuite dans notre maison '
            'du quartier du Fleuve. La détection thermographique a tranché : fuite réelle sur conduite encastrée." '
            '— Mme Granier, Saint-Louis-de-Montferrand'
        ),
        "specifique": "La forte hygrométrie de Saint-Louis-de-Montferrand rend la détection visuelle insuffisante et la détection instrumentale indispensable.",
    },
    "mios": {
        "intro": (
            "Mios est une commune forestière de la haute lande girondine, aux portes du Bassin "
            "d'Arcachon. Le bourg et le hameau de Lège côtoient la zone forestière. "
            "Les maisons individuelles y sont souvent isolées avec des réseaux alimentés "
            "par des forages privés ou le réseau AEP communal. Les canalisations extérieures "
            "traversent des terrains sableux qui facilitent les écoulements non détectés."
        ),
        "temoignage": (
            '"Grosse consommation d\'eau sur notre forage à Mios alors que la maison était inoccupée. '
            'La fuite était sur la canalisation enterrée reliant le forage à la maison, à 60 cm de profondeur." '
            '— M. Lasserre, Mios'
        ),
        "specifique": "Les réseaux sur forage privé de Mios nécessitent une expertise différente des réseaux AEP : pression variable, matériaux souvent en PE.",
    },
}


def get_contexte(slug):
    return CONTEXTES.get(slug, {
        "intro": "Nous intervenons dans cette commune pour toutes les situations de fuites d'eau, qu'elles soient visibles ou cachées.",
        "temoignage": '"Intervention rapide et professionnelle. Fuite localisée sans dégâts. Rapport remis pour l\'assurance." — Client local',
        "specifique": "Chaque intervention est adaptée aux caractéristiques locales du réseau d'eau.",
    })


def page_ville_html(ville):
    nom = ville["nom"]
    cp = ville["code_postal"]
    slug = ville["slug"]
    quartiers = ville.get("quartiers", [])
    quartiers_str = ", ".join(quartiers)
    ctx = get_contexte(slug)
    voisines = get_voisines(slug, 6)

    voisines_links = "".join(
        '<li><a href="/villes/{s}/">Recherche fuite {n}</a></li>'.format(s=v["slug"], n=v["nom"])
        for v in voisines
    )
    quartiers_tags = "".join(
        '<span class="zone-tag">{q}</span>'.format(q=q) for q in quartiers
    )
    autres_html = other_cities_grid(slug, 12)
    form = form_html(nom)
    hdr = header_html()
    ftr = footer_html()

    return """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Recherche fuite eau {nom} {cp} - détection non destructive</title>
  <meta name="description" content="Recherche et détection de fuite d'eau à {nom} ({cp}). Intervention rapide, méthodes non destructives. Rapport officiel pour assurance. Devis gratuit.">
  <link rel="canonical" href="https://recherche-fuite-gironde.fr/villes/{slug}/">
  <link rel="stylesheet" href="/assets/css/style.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "Recherche Fuite Gironde",
    "description": "Détection et recherche de fuites d'eau à {nom} ({cp}). Méthodes non destructives.",
    "url": "https://recherche-fuite-gironde.fr/villes/{slug}/",
    "areaServed": {{
      "@type": "City",
      "name": "{nom}",
      "postalCode": "{cp}",
      "containedIn": "Gironde"
    }}
  }}
  </script>
</head>
<body>

{hdr}

<section class="hero-mini">
  <div class="container">
    <nav class="breadcrumb">
      <a href="/">Accueil</a>
      <span class="breadcrumb-sep">/</span>
      <a href="/villes/bordeaux/">Villes</a>
      <span class="breadcrumb-sep">/</span>
      <span>{nom}</span>
    </nav>
    <h1>Recherche de fuite à {nom} ({cp})</h1>
    <p style="color:rgba(247,246,242,.75);margin-top:.5rem">Détection non destructive - Intervention en Gironde</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="intro-grid">
      <div class="article-body">
        <span class="section-label">Intervention locale</span>
        <h2>Recherche de fuite à {nom}</h2>
        <p>{intro}</p>
        <p>Nos techniciens couvrent tous les secteurs de {nom} : {quartiers_str}. Que la fuite soit visible ou cachée sous une dalle, dans une canalisation encastrée ou enterrée, nous apportons le bon équipement au bon endroit.</p>
        <div class="highlight-box mt-3">
          <strong>Particularité locale :</strong> {specifique}
        </div>
        <h3 style="margin-top:2rem">Nos méthodes d'intervention à {nom}</h3>
        <div class="steps">
          <div class="step">
            <div class="step-num">1</div>
            <div class="step-body">
              <h4>Prise en charge et diagnostic initial</h4>
              <p>À la réception de votre demande, nous analysons votre situation et planifions l'intervention dans les meilleurs délais à {nom}.</p>
            </div>
          </div>
          <div class="step">
            <div class="step-num">2</div>
            <div class="step-body">
              <h4>Détection sur site</h4>
              <p>Le technicien arrive équipé pour la situation décrite. Il utilise la corrélation acoustique, la thermographie ou le gaz traceur selon le type de fuite.</p>
            </div>
          </div>
          <div class="step">
            <div class="step-num">3</div>
            <div class="step-body">
              <h4>Localisation précise</h4>
              <p>La fuite est marquée au sol ou sur le mur, à quelques centimètres près. Aucune démolition n'est effectuée avant cette étape.</p>
            </div>
          </div>
          <div class="step">
            <div class="step-num">4</div>
            <div class="step-body">
              <h4>Rapport technique</h4>
              <p>Un compte-rendu complet est remis en fin d'intervention, utilisable directement auprès de votre assurance.</p>
            </div>
          </div>
        </div>
        <h3 style="margin-top:2rem">Quartiers de {nom} où nous intervenons</h3>
        <div class="zone-list">
          {quartiers_tags}
        </div>
        <h3 style="margin-top:2rem">Villes voisines</h3>
        <ul style="padding-left:1.25rem;list-style:disc">
          {voisines_links}
        </ul>
        <div class="testimonial mt-4">
          <div class="testimonial-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
          <p class="testimonial-text">{temoignage}</p>
        </div>
      </div>
      <aside>
        <div class="cta-card">
          <h3>Devis gratuit à {nom}</h3>
          <p style="font-size:.9rem;color:var(--c-text-muted);margin-bottom:1.25rem">Décrivez votre situation, nous vous rappelons rapidement.</p>
          <form action="https://formsubmit.co/PLACEHOLDER_EMAIL" method="POST">
            <input type="hidden" name="_subject" value="Devis - {nom}">
            <input type="hidden" name="_captcha" value="false">
            <input type="hidden" name="_next" value="https://recherche-fuite-gironde.fr/contact/merci/">
            <input type="hidden" name="_template" value="table">
            <input type="hidden" name="ville" value="{nom}">
            <div class="form-group" style="margin-bottom:.75rem">
              <label class="label-dark" for="prenom-mini">Prénom</label>
              <input type="text" id="prenom-mini" name="prenom" placeholder="Votre prénom" required>
            </div>
            <div class="form-group" style="margin-bottom:.75rem">
              <label class="label-dark" for="nom-mini">Nom</label>
              <input type="text" id="nom-mini" name="nom" placeholder="Votre nom" required>
            </div>
            <div class="form-group" style="margin-bottom:.75rem">
              <label class="label-dark" for="probleme-mini">Type de problème</label>
              <select id="probleme-mini" name="type_probleme" required>
                <option value="">Choisir</option>
                <option>Fuite visible</option>
                <option>Fuite sous dalle</option>
                <option>Canalisation enterrée</option>
                <option>Compteur qui tourne</option>
                <option>Humidité inexpliquée</option>
                <option>Chemisage</option>
              </select>
            </div>
            <div class="form-group" style="margin-bottom:.75rem">
              <label class="label-dark" for="msg-mini">Message</label>
              <textarea id="msg-mini" name="message" rows="3" placeholder="Décrivez votre situation..." required></textarea>
            </div>
            <button type="submit" class="btn btn--accent" style="width:100%">Envoyer</button>
          </form>
        </div>
        <div class="card mt-3" style="margin-top:1rem">
          <h4 style="margin-bottom:.75rem;font-size:1rem">Nos services à {nom}</h4>
          <ul style="display:flex;flex-direction:column;gap:.5rem">
            <li><a href="/detection-fuite/" style="color:var(--c-primary-light);font-size:.9rem">&#8594; Détection non destructive</a></li>
            <li><a href="/chemisage-canalisation/" style="color:var(--c-primary-light);font-size:.9rem">&#8594; Chemisage de canalisation</a></li>
            <li><a href="/villes/{slug}/chemisage/" style="color:var(--c-primary-light);font-size:.9rem">&#8594; Chemisage à {nom}</a></li>
            <li><a href="/guide/faq/" style="color:var(--c-primary-light);font-size:.9rem">&#8594; Questions fréquentes</a></li>
          </ul>
        </div>
      </aside>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <span class="section-label">Nos interventions</span>
    <h2 class="section-title">Nos services de détection à {nom}</h2>
    <div class="grid-3">
      <div class="card">
        <div class="card-icon"><img src="/assets/icons/search.svg" alt="Détection acoustique"></div>
        <h3>Détection acoustique</h3>
        <p>La corrélation acoustique localise les fuites sur canalisations enterrées ou encastrées à {nom}. Elle est précise à quelques centimètres et ne nécessite aucune démolition préalable.</p>
      </div>
      <div class="card">
        <div class="card-icon"><img src="/assets/icons/home.svg" alt="Fuite sous dalle"></div>
        <h3>Fuite sous dalle à {nom}</h3>
        <p>La thermographie infrarouge détecte les anomalies de température liées à une fuite sous carrelage ou sous chape, sans ouvrir la dalle au préalable.</p>
      </div>
      <div class="card">
        <div class="card-icon"><img src="/assets/icons/tick-badge.svg" alt="Rapport assurance"></div>
        <h3>Rapport pour assurance</h3>
        <p>Notre rapport de détection à {nom} est structuré pour être reconnu par les assureurs et accélérer le traitement des sinistres dégât des eaux.</p>
      </div>
    </div>
  </div>
</section>

{form}

{autres_html}

{ftr}

</body>
</html>""".format(
        nom=nom, cp=cp, slug=slug,
        intro=ctx["intro"],
        temoignage=ctx["temoignage"],
        specifique=ctx["specifique"],
        quartiers_str=quartiers_str,
        quartiers_tags=quartiers_tags,
        voisines_links=voisines_links,
        form=form,
        autres_html=autres_html,
        hdr=hdr,
        ftr=ftr,
    )


def page_chemisage_html(ville):
    nom = ville["nom"]
    cp = ville["code_postal"]
    slug = ville["slug"]
    quartiers = ville.get("quartiers", [])
    quartiers_str = ", ".join(quartiers)
    autres_html = other_cities_grid(slug, 12)
    form = form_html("Chemisage " + nom)
    hdr = header_html()
    ftr = footer_html()

    return """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chemisage canalisation {nom} {cp} - rénovation sans travaux</title>
  <meta name="description" content="Chemisage de canalisation à {nom} ({cp}). Rénovation sans tranchée ni démolition. Manchon en résine posé de l'intérieur. Devis gratuit.">
  <link rel="canonical" href="https://recherche-fuite-gironde.fr/villes/{slug}/chemisage/">
  <link rel="stylesheet" href="/assets/css/style.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Service",
    "name": "Chemisage de canalisation à {nom}",
    "description": "Rénovation de canalisations par chemisage sans tranchée à {nom} ({cp}).",
    "provider": {{
      "@type": "LocalBusiness",
      "name": "Recherche Fuite Gironde"
    }},
    "areaServed": {{
      "@type": "City",
      "name": "{nom}",
      "postalCode": "{cp}"
    }}
  }}
  </script>
</head>
<body>

{hdr}

<section class="hero-mini">
  <div class="container">
    <nav class="breadcrumb">
      <a href="/">Accueil</a>
      <span class="breadcrumb-sep">/</span>
      <a href="/villes/{slug}/">Recherche fuite {nom}</a>
      <span class="breadcrumb-sep">/</span>
      <span>Chemisage</span>
    </nav>
    <h1>Chemisage de canalisation à {nom} ({cp})</h1>
    <p style="color:rgba(247,246,242,.75);margin-top:.5rem">Rénovation sans tranchée - Intervention en Gironde</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="intro-grid">
      <div class="article-body">
        <span class="section-label">Sans démolition</span>
        <h2>Chemisage de canalisation à {nom}</h2>
        <p>Le chemisage de canalisation est la solution de rénovation sans travaux destructifs pour les réseaux endommagés à {nom}. Un manchon en résine époxy est inséré dans la canalisation existante, gonflé en place et durci sous chaleur. Le résultat est un nouveau tuyau dans l'ancien, sans ouvrir les murs ni les sols.</p>
        <p>Cette technique est particulièrement adaptée aux canalisations encastrées sous dalle ou dans les murs des habitations et copropriétés de {quartiers_str}. Elle évite des travaux de maçonnerie coûteux et réduit considérablement la durée du chantier.</p>
        <h3>Pourquoi choisir le chemisage à {nom}</h3>
        <ul>
          <li>Aucune tranchée ni démolition : les revêtements (carrelage, parquet, enduit) sont préservés</li>
          <li>Intervention rapide, souvent en une journée pour une section courante</li>
          <li>Durée de vie du manchon en résine : 50 ans minimum selon les fabricants</li>
          <li>Applicable aux canalisations EU, EP, EF, EC, en PVC, fonte, acier, cuivre ou plomb</li>
          <li>Conforme aux normes sanitaires pour l'eau potable</li>
        </ul>
        <h3 style="margin-top:2rem">Les étapes du chemisage à {nom}</h3>
        <div class="steps">
          <div class="step">
            <div class="step-num">1</div>
            <div class="step-body">
              <h4>Inspection par caméra</h4>
              <p>Avant toute intervention, la canalisation est inspectée par caméra endoscopique pour évaluer son état et confirmer la faisabilité du chemisage.</p>
            </div>
          </div>
          <div class="step">
            <div class="step-num">2</div>
            <div class="step-body">
              <h4>Nettoyage haute pression</h4>
              <p>La canalisation est nettoyée et dégraissée pour assurer une adhérence optimale du manchon en résine.</p>
            </div>
          </div>
          <div class="step">
            <div class="step-num">3</div>
            <div class="step-body">
              <h4>Insertion et gonflement du manchon</h4>
              <p>Le manchon imprégné de résine époxy est inséré et gonflé pour s'appliquer contre la paroi intérieure de la canalisation.</p>
            </div>
          </div>
          <div class="step">
            <div class="step-num">4</div>
            <div class="step-body">
              <h4>Polymérisation et contrôle</h4>
              <p>La résine est durcie sous chaleur ou UV. Une caméra de contrôle valide l'étanchéité avant remise en service.</p>
            </div>
          </div>
        </div>
        <h3 style="margin-top:2rem">Types de canalisations traitées à {nom}</h3>
        <div class="zone-list">
          <span class="zone-tag">Canalisation eau froide</span>
          <span class="zone-tag">Canalisation eau chaude</span>
          <span class="zone-tag">Évacuation EU/EP</span>
          <span class="zone-tag">Colonne montante</span>
          <span class="zone-tag">Réseau enterré</span>
          <span class="zone-tag">Tuyau en plomb</span>
        </div>
        <div class="testimonial mt-4">
          <div class="testimonial-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
          <p class="testimonial-text">"Chemisage de la colonne montante de notre immeuble à {nom}. Sans travaux importants, la résine a restauré l'étanchéité complète. L'intervention a duré une journée."</p>
          <div class="testimonial-author">Syndic de copropriété, {nom}</div>
        </div>
      </div>
      <aside>
        <div class="cta-card">
          <h3>Devis chemisage à {nom}</h3>
          <p style="font-size:.9rem;color:var(--c-text-muted);margin-bottom:1.25rem">Décrivez la canalisation concernée, nous vous répondons rapidement.</p>
          <form action="https://formsubmit.co/PLACEHOLDER_EMAIL" method="POST">
            <input type="hidden" name="_subject" value="Devis chemisage - {nom}">
            <input type="hidden" name="_captcha" value="false">
            <input type="hidden" name="_next" value="https://recherche-fuite-gironde.fr/contact/merci/">
            <input type="hidden" name="_template" value="table">
            <input type="hidden" name="ville" value="{nom}">
            <input type="hidden" name="type_probleme" value="Chemisage de canalisation">
            <div class="form-group" style="margin-bottom:.75rem">
              <label class="label-dark" for="prenom-ch">Prénom</label>
              <input type="text" id="prenom-ch" name="prenom" placeholder="Votre prénom" required>
            </div>
            <div class="form-group" style="margin-bottom:.75rem">
              <label class="label-dark" for="nom-ch">Nom</label>
              <input type="text" id="nom-ch" name="nom" placeholder="Votre nom" required>
            </div>
            <div class="form-group" style="margin-bottom:.75rem">
              <label class="label-dark" for="msg-ch">Description</label>
              <textarea id="msg-ch" name="message" rows="4" placeholder="Type de canalisation, longueur estimée, matériau si connu..." required></textarea>
            </div>
            <button type="submit" class="btn btn--accent" style="width:100%">Envoyer</button>
          </form>
        </div>
        <div class="card mt-3" style="margin-top:1rem">
          <h4 style="margin-bottom:.75rem;font-size:1rem">Services associés</h4>
          <ul style="display:flex;flex-direction:column;gap:.5rem">
            <li><a href="/villes/{slug}/" style="color:var(--c-primary-light);font-size:.9rem">&#8594; Recherche de fuite à {nom}</a></li>
            <li><a href="/chemisage-canalisation/" style="color:var(--c-primary-light);font-size:.9rem">&#8594; Guide du chemisage</a></li>
            <li><a href="/guide/chemisage-explication/" style="color:var(--c-primary-light);font-size:.9rem">&#8594; Comment fonctionne le chemisage</a></li>
          </ul>
        </div>
      </aside>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <h2 class="section-title">Quand opter pour le chemisage à {nom}</h2>
    <div class="grid-3">
      <div class="card">
        <div class="card-icon"><img src="/assets/icons/alert-circle.svg" alt=""></div>
        <h3>Canalisation corrodée</h3>
        <p>Un réseau en acier galvanisé ou en fonte âgé de plus de 40 ans perd son étanchéité par points. Le chemisage le consolide sans remplacement coûteux.</p>
      </div>
      <div class="card">
        <div class="card-icon"><img src="/assets/icons/home.svg" alt=""></div>
        <h3>Tuyau sous carrelage</h3>
        <p>Quand une canalisation encastrée sous dalle ou derrière un mur carrelé fuit, le chemisage évite la démolition des revêtements. C'est la solution la moins invasive.</p>
      </div>
      <div class="card">
        <div class="card-icon"><img src="/assets/icons/refresh.svg" alt=""></div>
        <h3>Colonne montante d'immeuble</h3>
        <p>Dans les copropriétés de {nom}, le chemisage de la colonne montante se fait en une journée, sans couper le réseau à tous les occupants pendant une semaine.</p>
      </div>
    </div>
  </div>
</section>

{form}

{autres_html}

{ftr}

</body>
</html>""".format(
        nom=nom, cp=cp, slug=slug,
        quartiers_str=quartiers_str,
        form=form,
        autres_html=autres_html,
        hdr=hdr,
        ftr=ftr,
    )


def generate():
    count_ville = 0
    count_chemisage = 0
    for ville in VILLES_LIST:
        slug = ville["slug"]
        dir_ville = os.path.join(BASE_DIR, "villes", slug)
        os.makedirs(dir_ville, exist_ok=True)
        with open(os.path.join(dir_ville, "index.html"), "w", encoding="utf-8") as f:
            f.write(page_ville_html(ville))
        count_ville += 1
        dir_chemisage = os.path.join(dir_ville, "chemisage")
        os.makedirs(dir_chemisage, exist_ok=True)
        with open(os.path.join(dir_chemisage, "index.html"), "w", encoding="utf-8") as f:
            f.write(page_chemisage_html(ville))
        count_chemisage += 1
    print("Généré : {} pages villes + {} pages chemisage".format(count_ville, count_chemisage))


if __name__ == "__main__":
    generate()
