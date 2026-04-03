#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

BASE = "C:/Users/Chou/Desktop/recherche-fuite-gironde"

HEADER = """<input type="checkbox" id="nav-check" aria-hidden="true">
<header class="site-header">
  <div class="container header-inner">
    <a href="/" class="logo">Recherche Fuite <span>Gironde</span></a>
    <nav class="nav" id="main-nav">
      <a href="/">Accueil</a>
      <div class="nav-dropdown">
        <a href="/detection-fuite/">Services</a>
        <div class="nav-dropdown-menu">
          <a href="/detection-fuite/">D&#233;tection de fuite</a>
          <a href="/chemisage-canalisation/">Chemisage de canalisation</a>
        </div>
      </div>
      <div class="nav-dropdown">
        <a href="/villes/bordeaux/">Villes</a>
        <div class="nav-dropdown-menu">
          <a href="/villes/bordeaux/">Bordeaux</a>
          <a href="/villes/merignac/">M&#233;rignac</a>
          <a href="/villes/pessac/">Pessac</a>
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

FOOTER = """<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="/" class="logo">Recherche Fuite <span>Gironde</span></a>
        <p>Sp&#233;cialistes de la d&#233;tection et de la recherche de fuites d'eau en Gironde (33).</p>
      </div>
      <div class="footer-col">
        <h4>Services</h4>
        <ul>
          <li><a href="/detection-fuite/">D&#233;tection de fuite</a></li>
          <li><a href="/chemisage-canalisation/">Chemisage de canalisation</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Guide</h4>
        <ul>
          <li><a href="/guide/">Sommaire du guide</a></li>
          <li><a href="/guide/faq/">FAQ</a></li>
          <li><a href="/guide/assurance-fuite-eau/">Assurance fuite</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Informations</h4>
        <ul>
          <li><a href="/contact/">Contact</a></li>
          <li><a href="/mentions-legales/">Mentions l&#233;gales</a></li>
          <li><a href="/plan-du-site/">Plan du site</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2025 Recherche Fuite Gironde - Tous droits r&#233;serv&#233;s</span>
    </div>
  </div>
</footer>"""

ASIDE_STD = """<li><a href="/guide/comment-detecter-une-fuite/" style="color:var(--c-primary-light);font-size:.88rem">&#8594; D&#233;tecter une fuite</a></li>
            <li><a href="/guide/causes-fuites-eau/" style="color:var(--c-primary-light);font-size:.88rem">&#8594; Causes des fuites</a></li>
            <li><a href="/guide/fuite-sous-dalle/" style="color:var(--c-primary-light);font-size:.88rem">&#8594; Fuite sous dalle</a></li>
            <li><a href="/guide/fuite-canalisation-enterree/" style="color:var(--c-primary-light);font-size:.88rem">&#8594; Fuite enterr&#233;e</a></li>
            <li><a href="/guide/chemisage-explication/" style="color:var(--c-primary-light);font-size:.88rem">&#8594; Chemisage expliqu&#233;</a></li>
            <li><a href="/guide/cout-recherche-fuite/" style="color:var(--c-primary-light);font-size:.88rem">&#8594; Co&#251;t de la recherche</a></li>
            <li><a href="/guide/assurance-fuite-eau/" style="color:var(--c-primary-light);font-size:.88rem">&#8594; Fuite et assurance</a></li>
            <li><a href="/guide/urgence-fuite-eau/" style="color:var(--c-primary-light);font-size:.88rem">&#8594; Urgence fuite d'eau</a></li>
            <li><a href="/guide/faq/" style="color:var(--c-primary-light);font-size:.88rem">&#8594; FAQ</a></li>"""

def make_page(slug, title, meta, h1, breadcrumb_label, content):
    return """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{meta}">
  <link rel="canonical" href="https://recherche-fuite-gironde.fr/guide/{slug}/">
  <link rel="stylesheet" href="/assets/css/style.css">
</head>
<body>

{header}

<section class="hero-mini">
  <div class="container">
    <nav class="breadcrumb">
      <a href="/">Accueil</a>
      <span class="breadcrumb-sep">/</span>
      <a href="/guide/">Guide</a>
      <span class="breadcrumb-sep">/</span>
      <span>{breadcrumb_label}</span>
    </nav>
    <h1>{h1}</h1>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="article-layout">
      <div class="article-body">
        {content}
      </div>
      <aside class="article-aside">
        <div class="card">
          <h4 style="margin-bottom:.75rem;font-size:1rem">Articles du guide</h4>
          <ul style="display:flex;flex-direction:column;gap:.5rem">
            {aside}
          </ul>
        </div>
        <div class="cta-card" style="margin-top:1rem">
          <h3>Besoin d'un technicien ?</h3>
          <p style="font-size:.9rem;color:var(--c-text-muted);margin-bottom:1rem">Nous intervenons en Gironde sous 48h.</p>
          <a href="/contact/" class="btn btn--accent" style="width:100%;text-align:center;justify-content:center">Demander un devis</a>
        </div>
      </aside>
    </div>
  </div>
</section>

{footer}

</body>
</html>""".format(
        title=title, meta=meta, slug=slug, h1=h1,
        breadcrumb_label=breadcrumb_label,
        content=content, aside=ASIDE_STD,
        header=HEADER, footer=FOOTER
    )

pages = [
    {
        "slug": "comment-detecter-une-fuite",
        "title": "Comment d\u00e9tecter une fuite d'eau chez soi - guide pratique",
        "meta": "Les signes d'une fuite d'eau, les v\u00e9rifications \u00e0 faire et quand appeler un professionnel. Guide pratique pour les particuliers en Gironde.",
        "h1": "Comment d\u00e9tecter une fuite d'eau chez soi",
        "breadcrumb_label": "D\u00e9tecter une fuite",
        "content": """<h2>Les signes qui doivent alerter</h2>
        <p>Une fuite d'eau ne se manifeste pas toujours par une flaque visible. Dans la majorit\u00e9 des cas, elle est silencieuse et progresse dans le b\u00e2ti sans qu'on la remarque pendant des semaines ou des mois.</p>
        <h3>La facture d'eau augmente sans raison</h3>
        <p>Comparez votre consommation mensuelle sur les douze derniers mois. Une hausse de 30\u00a0% ou plus sans changement de comportement est un signal fort. Les compteurs d'eau modernes permettent de consulter sa consommation jour par jour en ligne.</p>
        <h3>Le compteur tourne quand tout est ferm\u00e9</h3>
        <p>Fermez toutes les vannes et robinets de votre logement, puis observez le cadran du compteur d'eau pendant 15 \u00e0 30 minutes. S'il avance, m\u00eame l\u00e9g\u00e8rement, vous avez une fuite active quelque part sur votre r\u00e9seau.</p>
        <h3>Traces d'humidit\u00e9 ou taches sur les murs</h3>
        <p>Des aur\u00e9oles jaunatres sur un mur, un plafond qui se bombe, un parquet qui gondole ou un carrelage qui se d\u00e9colle sont des indicateurs classiques d'une fuite dans ou sous le rev\u00eatement.</p>
        <h3>Pr\u00e9sence de moisissures</h3>
        <p>Des moisissures persistantes sur un mur qui ne donne pas sur l'ext\u00e9rieur, dans un angle de salle de bains ou sous un lavabo signalent une humidit\u00e9 chronique souvent li\u00e9e \u00e0 une micro-fuite de joint ou de raccord.</p>
        <h3>Bruit d'eau inexplliqu\u00e9</h3>
        <p>Un clapotement, un sifflement ou un bruit de ruissellement perceptible dans les murs quand aucun robinet n'est ouvert est un signal direct d'une fuite active sur un r\u00e9seau sous pression.</p>
        <h2>Les v\u00e9rifications \u00e0 faire soi-m\u00eame</h2>
        <div class="steps">
          <div class="step"><div class="step-num">1</div><div class="step-body"><h4>Test du compteur</h4><p>Fermez toutes les vannes int\u00e9rieures (WC inclus). Relevez le compteur. Attendez 1h sans utiliser d'eau. Relevez \u00e0 nouveau. Tout mouvement confirme une fuite.</p></div></div>
          <div class="step"><div class="step-num">2</div><div class="step-body"><h4>Test des WC</h4><p>Versez quelques gouttes de colorant alimentaire dans le r\u00e9servoir. Si la couleur appara\u00eet dans la cuvette sans tirer la chasse, le m\u00e9canisme fuit. Les WC repr\u00e9sentent 20 \u00e0 30\u00a0% des fuites domestiques.</p></div></div>
          <div class="step"><div class="step-num">3</div><div class="step-body"><h4>Inspection visuelle des raccords</h4><p>Sous l'\u00e9vier, derri\u00e8re la machine \u00e0 laver, sous le chauffe-eau : inspectez tous les raccords visibles. Une l\u00e9g\u00e8re humidit\u00e9 ou des traces de calcaire signalent un joint d\u00e9faillant.</p></div></div>
          <div class="step"><div class="step-num">4</div><div class="step-body"><h4>V\u00e9rification des robinets</h4><p>Un robinet qui goutte une fois par seconde repr\u00e9sente 30 litres d'eau gaspill\u00e9e par jour. Remplacer un joint ou une cartouche est souvent suffisant.</p></div></div>
        </div>
        <h2>Quand appeler un professionnel de la d\u00e9tection</h2>
        <p>Appelez un sp\u00e9cialiste de la d\u00e9tection de fuites lorsque :</p>
        <ul>
          <li>Le compteur tourne mais aucune fuite visible n'est trouv\u00e9e</li>
          <li>La consommation est anormale malgr\u00e9 le remplacement des joints \u00e9vidents</li>
          <li>Des traces d'humidit\u00e9 apparaissent sous une dalle ou dans les murs sans source identifiable</li>
          <li>Votre assurance exige un rapport de localisation pour traiter le sinistre</li>
          <li>Vous avez un plancher chauffant qui monte lentement en temp\u00e9rature</li>
        </ul>"""
    },
    {
        "slug": "causes-fuites-eau",
        "title": "Causes des fuites d'eau dans les habitations - guide complet",
        "meta": "Toutes les causes possibles d'une fuite d'eau : mat\u00e9riaux, vieillissement, pression, gel, racines. Comment pr\u00e9venir et agir en Gironde.",
        "h1": "Les causes des fuites d'eau dans les habitations",
        "breadcrumb_label": "Causes des fuites",
        "content": """<h2>Pourquoi les canalisations fuient</h2>
        <p>Une fuite d'eau est rarement le fruit du hasard. Elle r\u00e9sulte presque toujours d'une cause identifiable : vieillissement des mat\u00e9riaux, d\u00e9faut d'installation, agression externe ou ph\u00e9nom\u00e8ne physique.</p>
        <h2>Le vieillissement des mat\u00e9riaux</h2>
        <p>Chaque mat\u00e9riau de canalisation a une dur\u00e9e de vie th\u00e9orique :</p>
        <ul>
          <li><strong>Plomb :</strong> 30 \u00e0 50 ans. Les canalisations en plomb des habitations d'avant 1950 sont souvent corrod\u00e9es et poreuses</li>
          <li><strong>Acier galvanis\u00e9 :</strong> 25 \u00e0 40 ans. La corrosion se d\u00e9veloppe de l'int\u00e9rieur puis perce</li>
          <li><strong>Cuivre :</strong> 50 ans en eau douce. Les raccords soud\u00e9s \u00e0 l'\u00e9tain vieillissent plus vite que le tube</li>
          <li><strong>PVC rigide :</strong> 30 \u00e0 50 ans, fragillis\u00e9 par les UV et les variations thermiques</li>
          <li><strong>PER :</strong> 50 ans et plus, mais les raccords \u00e0 sertir peuvent d\u00e9faillir en cas de mauvaise mise en oeuvre</li>
        </ul>
        <h2>La pression excessive</h2>
        <p>Une pression d'eau trop \u00e9lev\u00e9e (au-del\u00e0 de 3 bars en r\u00e9sidentiel) fragilise les raccords et les joints sur le long terme. En Gironde, la pression du r\u00e9seau public peut d\u00e9passer 4-5 bars dans certains secteurs. Un d\u00e9tendeur est recommand\u00e9 d\u00e8s que la pression d\u00e9passe 3 bars.</p>
        <h2>Les chocs thermiques</h2>
        <p>Les cycles de gel et d\u00e9gel peuvent fissurer les canalisations dans des espaces non chauff\u00e9s. En Gironde, les \u00e9pisodes de gel hivernal sont rares mais existent. Les canalisations dans les garages, les caves non chauff\u00e9es et les vides sanitaires y sont expos\u00e9es.</p>
        <h2>Les mouvements de terrain</h2>
        <p>Les argiles gonflantes pr\u00e9sentes dans certains secteurs de la Gironde (Libournais, rive droite de la Garonne) se r\u00e9tractent et gonflent selon les saisons. Ces mouvements peuvent d\u00e9caler les canalisations enterr\u00e9es et provoquer des ruptures aux jonctions.</p>
        <h2>Les racines d'arbres</h2>
        <p>Les racines d'arbres recherchent activement l'eau et s'infiltrent dans les canalisations d'\u00e9vacuation par les joints ou les fissures existantes. Ce ph\u00e9nom\u00e8ne est fr\u00e9quent sur les r\u00e9seaux d'\u00e9vacuation enterr\u00e9s pr\u00e8s de grands arbres.</p>
        <h2>Les d\u00e9fauts d'installation</h2>
        <p>Un joint mal pos\u00e9, un raccord insuffisamment serr\u00e9, une soudure mal r\u00e9alis\u00e9e : les d\u00e9fauts d'installation sont une cause fr\u00e9quente de fuites dans les 5 premi\u00e8res ann\u00e9es d'un r\u00e9seau.</p>
        <h2>La corrosion galvanique</h2>
        <p>Lorsque deux m\u00e9taux diff\u00e9rents sont en contact direct (cuivre et acier, par exemple), une pile galvanique se forme et acc\u00e9l\u00e8re la corrosion du m\u00e9tal le moins noble. Ce ph\u00e9nom\u00e8ne est courant dans les r\u00e9novations partielles.</p>
        <div class="highlight-box"><strong>\u00c0 retenir :</strong> dans la majorit\u00e9 des cas, une fuite est le r\u00e9sultat de plusieurs facteurs combin\u00e9s. Un diagnostic professionnel identifie non seulement la fuite mais aussi sa cause.</div>"""
    },
    {
        "slug": "fuite-sous-dalle",
        "title": "Fuite sous dalle : diagnostic et solutions sans d\u00e9molition",
        "meta": "Comment d\u00e9tecter et traiter une fuite sous dalle en b\u00e9ton ou carrelage. Thermographie, gaz traceur, chemisage. Gironde (33).",
        "h1": "Fuite sous dalle : diagnostic et solutions",
        "breadcrumb_label": "Fuite sous dalle",
        "content": """<h2>Qu'est-ce qu'une fuite sous dalle</h2>
        <p>Une fuite sous dalle d\u00e9signe toute fuite survenant sur des canalisations noy\u00e9es dans le b\u00e9ton ou la chape, situ\u00e9es sous le carrelage ou le rev\u00eatement de sol. C'est l'une des situations les plus d\u00e9licates, car la fuite est invisible et les solutions classiques impliquent de casser le sol.</p>
        <p>En Gironde, les maisons pavillonnaires des ann\u00e9es 1960-1990 sont particuli\u00e8rement expos\u00e9es. Les canalisations d'eau chaude sont les plus \u00e0 risque : la chaleur et les cycles thermiques fragilisent les raccords encast\u00e9s.</p>
        <h2>Comment reconna\u00eetre une fuite sous dalle</h2>
        <ul>
          <li>Le compteur d'eau tourne m\u00eame quand tout est ferm\u00e9</li>
          <li>La facture d'eau augmente sans raison visible</li>
          <li>Le carrelage se d\u00e9colle localement ou une dalle gonfle</li>
          <li>Une humidit\u00e9 remonte du sol en certains endroits</li>
          <li>Le plancher chauffant chauffe moins bien ou pr\u00e9sente des zones froides</li>
          <li>Un bruit sourd ou un gargouillis s'entend sous le sol</li>
        </ul>
        <h2>Les m\u00e9thodes de d\u00e9tection adapt\u00e9es</h2>
        <h3>Thermographie infrarouge</h3>
        <p>La cam\u00e9ra infrarouge est l'outil de r\u00e9f\u00e9rence pour les fuites sous dalle. L'eau qui s'\u00e9chappe cr\u00e9e une anomalie thermique \u00e0 la surface du sol, visible sur l'image thermique m\u00eame \u00e0 travers plusieurs centim\u00e8tres de b\u00e9ton. L'intervention est id\u00e9alement r\u00e9alis\u00e9e t\u00f4t le matin, quand le gradient thermique est le plus marqu\u00e9.</p>
        <h3>D\u00e9tection au gaz traceur</h3>
        <p>Pour les fuites d'eau froide sous dalle, la d\u00e9tection au gaz traceur est souvent plus efficace. Un m\u00e9lange azote/hydrog\u00e8ne est inject\u00e9 dans la canalisation. Ce gaz l\u00e9ger remonte \u00e0 travers le b\u00e9ton et est capt\u00e9 par un d\u00e9tecteur \u00e9lectronique, localisant la fuite \u00e0 quelques centim\u00e8tres pr\u00e8s.</p>
        <h2>Solutions de r\u00e9paration</h2>
        <h3>Ouverture localis\u00e9e et r\u00e9paration ponctuelle</h3>
        <p>Une fois la fuite localis\u00e9e avec pr\u00e9cision, une ouverture minimale (20-30 cm\u00b2) suffit pour acc\u00e9der \u00e0 la canalisation et effectuer la r\u00e9paration. C'est la solution la plus adapt\u00e9e pour une fuite ponctuelle sur une canalisation en bon \u00e9tat g\u00e9n\u00e9ral.</p>
        <h3>Chemisage de la canalisation concern\u00e9e</h3>
        <p>Si la canalisation est corrod\u00e9e de mani\u00e8re diffuse, le chemisage est pr\u00e9f\u00e9rable. Un manchon en r\u00e9sine est ins\u00e9r\u00e9 dans la canalisation existante et durci sur place, sans qu'il soit n\u00e9cessaire d'ouvrir davantage le sol.</p>
        <div class="highlight-box"><strong>Recommandation :</strong> avant toute ouverture du sol, faites r\u00e9aliser une d\u00e9tection professionnelle. L'investissement dans la localisation pr\u00e9cise est toujours rentabilis\u00e9 par l'\u00e9conomie sur les travaux de d\u00e9molition.</div>
        <h2>Ce que couvre l'assurance</h2>
        <p>La plupart des assurances habitation prennent en charge les dommages caus\u00e9s par une fuite sous dalle. Pour constituer un dossier solide, munissez-vous du rapport de d\u00e9tection avant d'appeler votre assureur.</p>"""
    },
    {
        "slug": "fuite-canalisation-enterree",
        "title": "Fuite sur canalisation enterr\u00e9e : d\u00e9tection et r\u00e9paration",
        "meta": "Comment d\u00e9tecter et r\u00e9parer une fuite sur canalisation enterr\u00e9e dans le jardin ou sous la voirie. M\u00e9thodes acoustiques. Gironde (33).",
        "h1": "Fuite sur canalisation enterr\u00e9e : d\u00e9tecter et agir",
        "breadcrumb_label": "Fuite enterr\u00e9e",
        "content": """<h2>Les sp\u00e9cificit\u00e9s d'une fuite enterr\u00e9e</h2>
        <p>Une fuite sur canalisation enterr\u00e9e est particuli\u00e8rement insidieuse. L'eau s'\u00e9coule en profondeur, dans le sol, loin de tout regard. Les signes de surface apparaissent tardivement : une zone de terrain anormalement verte ou gorg\u00e9e d'eau, ou plus souvent, une hausse incompr\u00e9hensible de la facture d'eau.</p>
        <h2>Identifier le r\u00e9seau en cause</h2>
        <ul>
          <li><strong>Alimentation depuis le compteur :</strong> le tron\u00e7on entre le compteur de rue et la maison est souvent en polym\u00e8re et enterr\u00e9</li>
          <li><strong>R\u00e9seau d'arrosage :</strong> en poly\u00e9thyl\u00e8ne basse pression, souvent \u00e0 faible profondeur. Les fuites sont fr\u00e9quentes aux raccords</li>
          <li><strong>Alimentation piscine :</strong> les fuites sur les r\u00e9seaux enterr\u00e9s de piscine sont fr\u00e9quentes et difficiles \u00e0 localiser sans \u00e9quipement</li>
        </ul>
        <h2>La d\u00e9tection par corr\u00e9lation acoustique</h2>
        <p>La corr\u00e9lation acoustique est la m\u00e9thode de r\u00e9f\u00e9rence pour les fuites sur canalisations enterr\u00e9es sous pression. Deux capteurs acoustiques hypersensibles sont plac\u00e9s sur des points d'acc\u00e8s au r\u00e9seau. Le bruit g\u00e9n\u00e9r\u00e9 par la fuite se propage dans la canalisation. En comparant le temps d'arriv\u00e9e du signal sur chaque capteur, l'algorithme calcule la position de la fuite avec une pr\u00e9cision de 10 \u00e0 30 cm.</p>
        <h2>La d\u00e9tection au gaz traceur sur r\u00e9seaux enterr\u00e9s</h2>
        <p>Pour les canalisations en poly\u00e9thyl\u00e8ne \u00e0 basse pression (r\u00e9seaux d'arrosage, alimentation piscine), la d\u00e9tection au gaz traceur est souvent la m\u00e9thode de choix. Le gaz remonte directement au point de fuite et est capt\u00e9 en surface.</p>
        <h2>Solutions de r\u00e9paration</h2>
        <h3>Fouille localis\u00e9e et r\u00e9paration</h3>
        <p>Gr\u00e2ce \u00e0 la localisation pr\u00e9cise, la fouille est r\u00e9duite \u00e0 quelques d\u00e9cim\u00e8tres carr\u00e9s. La dur\u00e9e de la r\u00e9paration est souvent d'une demi-journ\u00e9e.</p>
        <h3>Chemisage du tron\u00e7on</h3>
        <p>Si la canalisation est vieillissante sur l'ensemble du tron\u00e7on, le chemisage permet de r\u00e9nover l'int\u00e9gralit\u00e9 du r\u00e9seau enterr\u00e9 sans tranch\u00e9e. Id\u00e9al pour les all\u00e9es en b\u00e9ton ou en pav\u00e9s.</p>
        <h2>Responsabilit\u00e9 et prise en charge</h2>
        <p>En France, le r\u00e9seau d'eau potable est \u00e0 la charge du propri\u00e9taire depuis le compteur de rue jusqu'au logement. Certaines assurances habitation couvrent les frais de recherche et de r\u00e9paration d'une fuite enterr\u00e9e.</p>"""
    },
    {
        "slug": "chemisage-explication",
        "title": "Le chemisage de canalisation expliqu\u00e9 simplement",
        "meta": "Comment fonctionne le chemisage de canalisation ? Proc\u00e9d\u00e9, mat\u00e9riaux, dur\u00e9e de vie, co\u00fbt. Guide complet pour comprendre cette technique sans tranch\u00e9e.",
        "h1": "Le chemisage de canalisation expliqu\u00e9 simplement",
        "breadcrumb_label": "Chemisage expliqu\u00e9",
        "content": """<h2>Le principe en une phrase</h2>
        <p>Le chemisage consiste \u00e0 cr\u00e9er un nouveau tuyau \u00e0 l'int\u00e9rieur de l'ancien, sans le retirer ni ouvrir les rev\u00eatements qui l'entourent.</p>
        <h2>Les mat\u00e9riaux utilis\u00e9s</h2>
        <h3>Le manchon</h3>
        <p>Le manchon est une gaine souple en feutre de polyester ou en tissu de verre, impr\u00e9gn\u00e9e de r\u00e9sine \u00e9poxy juste avant la pose. Son \u00e9paisseur varie de 4 \u00e0 12 mm selon le diam\u00e8tre et la pression du r\u00e9seau.</p>
        <h3>La r\u00e9sine</h3>
        <p>La r\u00e9sine \u00e9poxy est la plus courante, appr\u00e9ci\u00e9e pour sa r\u00e9sistance m\u00e9canique et sa compatibilit\u00e9 avec l'eau potable (certifi\u00e9e ACS en France). Une fois polym\u00e9ris\u00e9e, elle atteint une duret\u00e9 comparable \u00e0 celle du PVC rigide.</p>
        <h2>Le processus pas \u00e0 pas</h2>
        <div class="steps">
          <div class="step"><div class="step-num">1</div><div class="step-body"><h4>Inspection cam\u00e9ra pr\u00e9alable</h4><p>Une cam\u00e9ra endoscopique parcourt la canalisation pour \u00e9valuer son \u00e9tat et confirmer la faisabilit\u00e9 du chemisage.</p></div></div>
          <div class="step"><div class="step-num">2</div><div class="step-body"><h4>Hydrocurage</h4><p>Un jet d'eau haute pression nettoie les parois pour assurer l'adh\u00e9rence de la r\u00e9sine.</p></div></div>
          <div class="step"><div class="step-num">3</div><div class="step-body"><h4>Impregn\u00e9ation et insertion du manchon</h4><p>Le manchon impr\u00e9gn\u00e9 est ins\u00e9r\u00e9 dans la canalisation par retournement et gonfl\u00e9 \u00e0 l'air comprim\u00e9.</p></div></div>
          <div class="step"><div class="step-num">4</div><div class="step-body"><h4>Polym\u00e9risation de la r\u00e9sine</h4><p>La r\u00e9sine est durcie par eau chaude, vapeur ou lumi\u00e8re UV. La polym\u00e9risation dure 30 min \u00e0 3h.</p></div></div>
          <div class="step"><div class="step-num">5</div><div class="step-body"><h4>Contr\u00f4le final et remise en service</h4><p>Une cam\u00e9ra de contr\u00f4le valide l'aspect int\u00e9rieur. Un rapport de fin de chantier est remis.</p></div></div>
        </div>
        <h2>Dur\u00e9e de vie et garanties</h2>
        <p>Les manchons en r\u00e9sine \u00e9poxy ont une dur\u00e9e de vie estim\u00e9e \u00e0 50 ans selon les fabricants. Les principaux fabricants proposent des garanties de 10 \u00e0 15 ans sur leurs produits.</p>
        <h2>Limites du chemisage</h2>
        <ul>
          <li>Non applicable si la canalisation est totalement \u00e9cras\u00e9e ou effondr\u00e9e</li>
          <li>R\u00e9duit l\u00e9g\u00e8rement le diam\u00e8tre int\u00e9rieur (perte de section de 10-15\u00a0%)</li>
          <li>N\u00e9cessite des points d'acc\u00e8s aux deux extr\u00e9mit\u00e9s de la section</li>
        </ul>"""
    },
    {
        "slug": "cout-recherche-fuite",
        "title": "Co\u00fbt d'une recherche de fuite d'eau - tarifs et prise en charge",
        "meta": "Combien co\u00fbte une recherche de fuite ? Tarifs selon les m\u00e9thodes, prise en charge assurance, facteurs influençant le prix.",
        "h1": "Co\u00fbt d'une recherche de fuite d'eau",
        "breadcrumb_label": "Co\u00fbt de la recherche",
        "content": """<h2>Comprendre la structure du prix</h2>
        <p>Le tarif d'une recherche de fuite d\u00e9pend de la m\u00e9thode employ\u00e9e, de la complexit\u00e9 de l'acc\u00e8s \u00e0 la canalisation, du temps pass\u00e9 sur site et des \u00e9quipements mobilis\u00e9s.</p>
        <h2>Fourchettes de prix courantes</h2>
        <div class="highlight-box">
          <p><strong>Recherche simple (compteur test + inspection visuelle) :</strong> 80 \u00e0 150 \u20ac</p>
          <p><strong>D\u00e9tection acoustique sur canalisation enterr\u00e9e :</strong> 200 \u00e0 400 \u20ac</p>
          <p><strong>Thermographie infrarouge (fuite sous dalle) :</strong> 200 \u00e0 500 \u20ac</p>
          <p><strong>D\u00e9tection au gaz traceur :</strong> 300 \u00e0 600 \u20ac</p>
          <p><strong>Inspection cam\u00e9ra endoscopique :</strong> 150 \u00e0 350 \u20ac</p>
          <p><strong>Intervention multi-technique (situation complexe) :</strong> 400 \u00e0 900 \u20ac</p>
        </div>
        <h2>Ce que comprend le prix</h2>
        <ul>
          <li>Le d\u00e9placement du technicien</li>
          <li>L'utilisation des \u00e9quipements de d\u00e9tection</li>
          <li>Le temps pass\u00e9 sur site</li>
          <li>La r\u00e9daction et la remise du rapport technique</li>
        </ul>
        <h2>Prise en charge par l'assurance</h2>
        <p>La <strong>garantie "recherche de fuite"</strong>, pr\u00e9sente dans de nombreux contrats MRH, couvre les frais de localisation avec un plafond de 800 \u00e0 2\u202f000\u00a0\u20ac. La <strong>garantie d\u00e9g\u00e2t des eaux</strong> couvre les dommages mat\u00e9riels caus\u00e9s par la fuite. V\u00e9rifiez votre contrat et d\u00e9clarez le sinistre avant de commander une recherche.</p>
        <h2>Calcul de la rentabilit\u00e9</h2>
        <p>Une fuite sous dalle co\u00fbte 350\u00a0\u20ac \u00e0 localiser. Sans localisation pr\u00e9cise, un carreleur doit ouvrir 4\u00a0m\u00b2 de sol \u00e0 l'aveugle (800 \u00e0 1\u202f500\u00a0\u20ac). Avec le rapport de d\u00e9tection, il ouvre 1 dalle de 30\u00a0cm &times; 30\u00a0cm (80 \u00e0 150\u00a0\u20ac). L'\u00e9conomie nette est de 500 \u00e0 1\u202f200\u00a0\u20ac. La d\u00e9tection se rentabilise presque toujours.</p>"""
    },
    {
        "slug": "assurance-fuite-eau",
        "title": "Fuite d'eau et assurance habitation - comment \u00eatre rembours\u00e9",
        "meta": "Ce que couvre votre assurance pour une fuite d'eau : garanties, d\u00e9marches, rapport de d\u00e9tection, d\u00e9lais. Guide pratique pour les particuliers.",
        "h1": "Fuite d'eau et assurance habitation",
        "breadcrumb_label": "Fuite et assurance",
        "content": """<h2>Les garanties qui couvrent les fuites d'eau</h2>
        <p>Face \u00e0 une fuite d'eau, plusieurs garanties de votre contrat MRH peuvent intervenir.</p>
        <h3>La garantie d\u00e9g\u00e2t des eaux</h3>
        <p>C'est la garantie de base, pr\u00e9sente dans tous les contrats MRH. Elle couvre les dommages mat\u00e9riels caus\u00e9s par une fuite accidentelle (eau qui a d\u00e9t\u00e9rior\u00e9 un parquet, un mur, un plafond, des meubles).</p>
        <h3>La garantie recherche de fuite</h3>
        <p>Cette garantie, souvent optionnelle ou incluse dans les formules compl\u00e8tes, couvre les frais engag\u00e9s pour localiser l'origine de la fuite. Le plafond est g\u00e9n\u00e9ralement de 800 \u00e0 2\u202f000\u00a0\u20ac. V\u00e9rifiez si elle figure dans votre contrat.</p>
        <h2>Les d\u00e9marches \u00e0 suivre</h2>
        <div class="steps">
          <div class="step"><div class="step-num">1</div><div class="step-body"><h4>Coupez l'eau et limitez les d\u00e9g\u00e2ts</h4><p>Fermez la vanne g\u00e9n\u00e9rale et, si n\u00e9cessaire, le disjoncteur \u00e9lectrique des pi\u00e8ces concern\u00e9es.</p></div></div>
          <div class="step"><div class="step-num">2</div><div class="step-body"><h4>D\u00e9clarez le sinistre</h4><p>Contactez votre assureur dans les 5 jours ouvr\u00e9s suivant la d\u00e9couverte de la fuite.</p></div></div>
          <div class="step"><div class="step-num">3</div><div class="step-body"><h4>Faites localiser la fuite</h4><p>Mandatez un professionnel de la d\u00e9tection et obtenez le rapport technique.</p></div></div>
          <div class="step"><div class="step-num">4</div><div class="step-body"><h4>Constituez votre dossier</h4><p>Rassemblez : rapport de d\u00e9tection, photos des d\u00e9g\u00e2ts, devis de r\u00e9paration, factures des \u00e9quipements endommag\u00e9s.</p></div></div>
          <div class="step"><div class="step-num">5</div><div class="step-body"><h4>Attendez l'expertise</h4><p>L'assureur peut mandater un expert pour \u00e9valuer les dommages. Vous pouvez contester l'offre si elle vous semble insuffisante.</p></div></div>
        </div>
        <h2>Le rapport de d\u00e9tection : votre meilleur allié</h2>
        <p>Le rapport remis par le technicien est le document central du dossier sinistre. Il doit comporter : l'identification du logement, la description des sympt\u00f4mes, la m\u00e9thode employ\u00e9e, la localisation pr\u00e9cise et les pr\u00e9conisations de r\u00e9paration.</p>
        <div class="highlight-box highlight-box--warning"><strong>Attention :</strong> n'entreprendrez pas de travaux avant que l'expert de l'assurance soit pass\u00e9, sauf urgence absolue. Documentez l'\u00e9tat avant travaux avec des photos.</div>"""
    },
    {
        "slug": "urgence-fuite-eau",
        "title": "Urgence fuite d'eau : que faire dans les premi\u00e8res minutes",
        "meta": "Que faire en cas de fuite d'eau urgente ? Les gestes imm\u00e9diats pour limiter les d\u00e9g\u00e2ts et comment g\u00e9rer la situation sereinement.",
        "h1": "Urgence fuite d'eau : les bons r\u00e9flexes",
        "breadcrumb_label": "Urgence fuite",
        "content": """<h2>Les premi\u00e8res minutes sont d\u00e9cisives</h2>
        <p>Une fuite d'eau active peut causer des dommages consid\u00e9rables en quelques heures : parquet gondol\u00e9, mur satur\u00e9, plafond du dessous effondr\u00e9, court-circuit \u00e9lectrique. Voici les actions \u00e0 encha\u00eener rapidement.</p>
        <h2>Geste 1 : couper l'eau</h2>
        <p>Fermez imm\u00e9diatement la vanne d'arr\u00eat la plus proche de la fuite. Si vous ne trouvez pas, fermez la vanne g\u00e9n\u00e9rale du logement. Elle se trouve g\u00e9n\u00e9ralement sous l'\u00e9vier de la cuisine, dans un placard technique ou dans la cave.</p>
        <h2>Geste 2 : s\u00e9curiser les installations \u00e9lectriques</h2>
        <p>Si l'eau s'approche de prises \u00e9lectriques ou d'un tableau \u00e9lectrique, coupez le disjoncteur des circuits concern\u00e9s avant d'intervenir. L'eau et l'\u00e9lectricit\u00e9 sont une combinaison mortelle.</p>
        <h2>Geste 3 : limiter la propagation de l'eau</h2>
        <ul>
          <li>Placez des serviettes ou des torchons autour de la fuite</li>
          <li>Utilisez des seaux ou des bassines pour recueillir l'eau</li>
          <li>Prot\u00e9gez les meubles avec des b\u00e2ches ou des sacs plastiques</li>
          <li>Si le plafond du dessous est menac\u00e9, faites un trou en son centre pour drainer l'eau en un point contr\u00f4l\u00e9</li>
        </ul>
        <h2>Geste 4 : documenter les d\u00e9g\u00e2ts</h2>
        <p>Avant de nettoyer quoi que ce soit, prenez des photos et des vid\u00e9os de la fuite et des d\u00e9g\u00e2ts. Ces documents sont indispensables pour le dossier assurance.</p>
        <h2>Geste 5 : pr\u00e9venir les personnes concern\u00e9es</h2>
        <p>En appartement, pr\u00e9venez le voisin du dessous si votre plafond est menac\u00e9 et votre syndic s'il y a des parties communes concern\u00e9es.</p>
        <h2>Geste 6 : d\u00e9clarer le sinistre</h2>
        <p>Appelez votre assureur dans les 5 jours ouvr\u00e9s. En situation d'urgence, certains assureurs ont une ligne d'assistance 24h/24.</p>
        <div class="highlight-box"><strong>\u00c0 savoir :</strong> une fuite non trait\u00e9e pendant plusieurs semaines peut co\u00fbter des centaines d'euros en consommation d'eau et des milliers en travaux de remise en \u00e9tat. Agir vite limite toujours la note finale.</div>
        <h2>Trouver l'origine de la fuite</h2>
        <p>Une fois l'urgence g\u00e9r\u00e9e, l'\u00e9tape suivante est de localiser pr\u00e9cis\u00e9ment l'origine de la fuite. Si elle est cach\u00e9e (sous dalle, dans un mur, sur un r\u00e9seau enterr\u00e9), une d\u00e9tection professionnelle s'impose avant tout travaux.</p>"""
    },
]

for page in pages:
    slug = page["slug"]
    path = os.path.join(BASE, "guide", slug)
    os.makedirs(path, exist_ok=True)
    html = make_page(slug, page["title"], page["meta"], page["h1"], page["breadcrumb_label"], page["content"])
    with open(os.path.join(path, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Guide: " + slug)

print("Done.")
