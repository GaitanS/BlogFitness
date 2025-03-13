from django.core.management.base import BaseCommand
from django.utils.text import slugify
from blog.models import Category, Article, AdSenseLocation

class Command(BaseCommand):
    help = 'Populează baza de date cu câteva date inițiale'

    def handle(self, *args, **kwargs):
        self.stdout.write('Popularea bazei de date...')
        
        # Adăugare categorii
        categories = {
            'Antrenament': 'fa-dumbbell',
            'Nutriție': 'fa-carrot',
            'Lifestyle': 'fa-heart'
        }
        
        category_objs = {}
        for name, icon in categories.items():
            slug = slugify(name)
            cat, created = Category.objects.get_or_create(
                name=name,
                defaults={
                    'icon': icon,
                    'slug': slug,
                    'description': f'Articole despre {name.lower()}'
                }
            )
            category_objs[name] = cat
            action = 'creată' if created else 'deja există'
            self.stdout.write(f'Categoria "{name}" {action}')
        
        # Adăugare articole pentru Antrenament
        antrenament_articles = [
            {
                'title': '7 Exerciții pentru un abdomen perfect',
                'content': '''
Descoperă rutina completă care activează toate grupele musculare abdominale.

Un abdomen perfect nu se obține doar prin antrenament, ci și printr-o alimentație adecvată. Cu toate acestea, aceste exerciții vor ajuta la dezvoltarea și tonifierea musculaturii abdominale.

## 1. Plank

Poziționează-te în poziția de flotare, sprijinindu-te pe antebrațe. Menține poziția, contractând abdomenul, pentru 30-60 secunde.

## 2. Crunch-uri

Stai pe spate cu genunchii îndoiți. Ridică umerii de la sol, contractând abdomenul. Revino ușor în poziția inițială.

## 3. Bicycle Crunch

Poziționat pe spate, du alternativ cotul drept spre genunchiul stâng și viceversa, simulând pedalarea unei biciclete.

## 4. Mountain Climbers

Din poziția de flotare, adu alternativ genunchii spre piept, menținând abdomenul contractat.

## 5. Leg Raises

Stai pe spate, cu picioarele întinse. Ridică picioarele drept în sus, apoi coboară-le lent, fără a atinge solul.

## 6. Russian Twist

Stai jos cu genunchii îndoiți și partea superioară a corpului înclinată la 45°. Rotește partea superioară a corpului de la stânga la dreapta.

## 7. Hollow Body Hold

Stai pe spate, cu brațele și picioarele întinse. Ridică ușor umerii și picioarele de la sol, menținând poziția.

Efectuează aceste exerciții de 3-4 ori pe săptămână, câte 3 seturi a 12-15 repetări pentru fiecare exercițiu. Nu uita să te odihnești între seturi!
                ''',
                'featured_image': 'placeholder.webp',
                'read_time': 6,
                'is_featured': False,
                'category': category_objs['Antrenament']
            }
        ]
        
        # Adăugare articole pentru Nutriție
        nutritie_articles = [
            {
                'title': 'Ghid complet pentru nutriție pre și post antrenament',
                'content': '''
Alimente care maximizează recuperarea și construiesc masă musculară.

Alimentația înainte și după antrenament joacă un rol crucial în performanța sportivă și în recuperarea musculară. Iată un ghid complet pentru a-ți optimiza nutriția pre și post antrenament.

## Nutriția Pre-Antrenament

### Cu 2-3 ore înainte de antrenament:
- Un prânz echilibrat cu proteine și carbohidrați complecși
- Exemple: piept de pui cu orez integral și legume, paste integrale cu ton și sos de roșii

### Cu 30-60 minute înainte de antrenament:
- O gustare ușoară bogată în carbohidrați și cu conținut moderat de proteine
- Exemple: banană cu unt de arahide, iaurt cu fructe și granola

## Nutriția Post-Antrenament

### În primele 30 minute după antrenament:
- O combinație de proteine și carbohidrați pentru refacerea glicogenului și repararea fibrelor musculare
- Exemple: shake de proteine cu banană, piept de pui cu cartofi dulci

### Cu 2 ore după antrenament:
- O masă completă cu proteine, carbohidrați complecși și grăsimi sănătoase
- Exemple: somon la grătar cu quinoa și avocado, tofu cu orez brun și broccoli

## Hidratarea

- Bea 500-600 ml de apă cu 2-3 ore înainte de antrenament
- Consumă 200-300 ml de apă la fiecare 15-20 minute în timpul antrenamentului
- Bea 500-700 ml de apă pentru fiecare 0.5 kg pierdut în timpul antrenamentului

## Suplimente Recomandate

- Proteine: shake de whey protein post-antrenament
- BCAA: în timpul antrenamentelor intense sau în perioadele de deficit caloric
- Creatină: pentru creșterea forței și performanței
- Electroliți: pentru hidratare optimă în timpul antrenamentelor intense

Reține că nutriția trebuie adaptată în funcție de obiectivele tale, tipul de antrenament și toleranța individuală. Experimentează cu diferite alimente și momente de consum pentru a găsi combinația optimă pentru tine.
                ''',
                'featured_image': 'placeholder.webp',
                'read_time': 8,
                'is_featured': True,
                'category': category_objs['Nutriție']
            }
        ]
        
        # Adăugare articole pentru Lifestyle
        lifestyle_articles = [
            {
                'title': 'Cum să-ți menții motivația pe termen lung',
                'content': '''
Strategii psihologice pentru a rămâne consecvent în obiectivele tale.

Menținerea motivației pe termen lung este una dintre cele mai mari provocări în drumul spre atingerea obiectivelor de fitness și sănătate. Iată strategii dovedite științific care te vor ajuta să rămâi motivat și consecvent.

## 1. Stabilește obiective SMART

Obiectivele SMART (Specifice, Măsurabile, Abordabile, Relevante, Încadrate în Timp) cresc șansele de succes. În loc să spui "Vreau să slăbesc", spune "Vreau să pierd 5 kg în următoarele 3 luni prin antrenamente de 3 ori pe săptămână și reducerea consumului de zahăr".

## 2. Identifică motivația intrinsecă

Motivația care vine din interior (te face să te simți bine, îți oferă satisfacție personală) este mai puternică decât cea externă (recompense, apreciere din partea altora). Întreabă-te de ce vrei cu adevărat să atingi acest obiectiv și cum te va face să te simți.

## 3. Vizualizează succesul

Petrece câteva minute în fiecare zi vizualizând cum ar arăta succesul tău. Imaginează-ți în detaliu cum te vei simți, cum vei arăta și ce vei putea face atunci când îți vei atinge obiectivul.

## 4. Împarte obiectivele mari în pași mici

Obiectivele mari pot părea copleșitoare. Împarte-le în pași mai mici, săptămânali sau chiar zilnici, care sunt mai ușor de gestionat și îți oferă satisfacție constantă.

## 5. Monitorizează-ți progresul

Ține un jurnal sau folosește o aplicație pentru a-ți nota progresul. Această practică te ajută să rămâi responsabil și să observi îmbunătățirile, chiar și pe cele mici.

## 6. Găsește-ți comunitatea

Alătură-te unui grup cu interese similare sau găsește un partener de antrenament. Suportul social crește semnificativ aderența la un program de fitness.

## 7. Recompensează-te pentru efort, nu doar pentru rezultate

Creează un sistem de recompense pentru efortul constant, nu doar pentru atingerea obiectivelor finale. Astfel, vei rămâne motivat pe parcurs.

## 8. Acceptă eșecurile ca parte din proces

Regresele sunt normale și fac parte din orice călătorie de transformare. În loc să renunți când întâmpini obstacole, văzule ca oportunități de învățare și ajustează-ți strategia.

## 9. Implementează "regula de 2 minute"

Când nu ai chef de antrenament, promite-ți să faci doar 2 minute. De cele mai multe ori, odată ce ai început, vei continua întreaga sesiune.

## 10. Conectează-te cu valorile tale profunde

Asigură-te că obiectivele tale de fitness sunt aliniate cu valorile tale personale și cu viziunea ta despre viață. Această conexiune profundă va menține flacăra motivației aprinsă mult timp.

Amintește-ți că motivația fluctuează natural. În zilele când motivația e scăzută, disciplina și obiceiurile bine stabilite sunt cele care te vor ajuta să rămâi pe drumul cel bun.
                ''',
                'featured_image': 'placeholder.webp',
                'read_time': 5,
                'is_featured': False,
                'category': category_objs['Lifestyle']
            }
        ]
        
        all_articles = antrenament_articles + nutritie_articles + lifestyle_articles
        
        for article_data in all_articles:
            # Extragem featured_image
            featured_image = article_data.pop('featured_image')
            
            # Verificăm dacă articolul există deja
            existing = Article.objects.filter(title=article_data['title']).exists()
            
            if not existing:
                # Creăm articolul
                article = Article(
                    **article_data,
                    slug=slugify(article_data['title'])
                )
                
                # Atribuim imaginea
                from django.core.files.images import ImageFile
                from django.conf import settings
                import os
                
                image_path = os.path.join(settings.BASE_DIR, 'static', 'images', featured_image)
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as f:
                        article.featured_image.save(featured_image, ImageFile(f), save=False)
                
                article.save()
                self.stdout.write(f'Articolul "{article_data["title"]}" a fost creat')
            else:
                self.stdout.write(f'Articolul "{article_data["title"]}" există deja')
        
        # Adăugare locații AdSense
        adsense_locations = [
            {
                'name': 'global',
                'description': 'Cod AdSense global pentru toate paginile',
                'ad_code': '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5227061222218296" crossorigin="anonymous"></script>',
            },
            {
                'name': 'below_hero',
                'description': 'Sub secțiunea hero pe pagina principală',
                'ad_code': '<!-- Adsense Below Hero --><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="XXXXXXXXXX" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({});</script>',
            },
            {
                'name': 'middle_page',
                'description': 'În mijlocul paginii principale',
                'ad_code': '<!-- Adsense Middle Page --><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="XXXXXXXXXX" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({});</script>',
            },
            {
                'name': 'before_footer',
                'description': 'Înainte de footer',
                'ad_code': '<!-- Adsense Before Footer --><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="XXXXXXXXXX" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({});</script>',
            },
            {
                'name': 'above_content',
                'description': 'Deasupra conținutului articolului',
                'ad_code': '<!-- Adsense Above Content --><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="XXXXXXXXXX" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({});</script>',
            },
            {
                'name': 'below_content',
                'description': 'Sub conținutul articolului',
                'ad_code': '<!-- Adsense Below Content --><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="XXXXXXXXXX" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({});</script>',
            },
            {
                'name': 'below_header',
                'description': 'Sub header-ul paginii de categorie sau articole',
                'ad_code': '<!-- Adsense Below Header --><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="XXXXXXXXXX" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({});</script>',
            },
        ]
        
        for location_data in adsense_locations:
            location, created = AdSenseLocation.objects.get_or_create(
                name=location_data['name'],
                defaults={
                    'description': location_data['description'],
                    'ad_code': location_data['ad_code'],
                }
            )
            
            action = 'creată' if created else 'deja există'
            self.stdout.write(f'Locația AdSense "{location_data["name"]}" {action}')
        
        self.stdout.write(self.style.SUCCESS('Popularea bazei de date a fost finalizată cu succes!'))
