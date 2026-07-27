"""Shared bilingual copy for Datara's secondary pages."""


CONTENT_UI = {
    'da': {
        'skip_label': 'Gå til indholdet',
        'nav_label': 'Hovedmenu',
        'home_label': 'Gå til Datara-forsiden',
        'projects': 'Projekter',
        'services': 'Services',
        'contact': 'Kontakt',
        'language_short': 'EN',
        'language_label': 'Læs siden på engelsk',
        'service_eyebrow': 'Det hjælper vi med',
        'benefits_title': 'Det får I ud af arbejdet',
        'process_title': 'Sådan arbejder vi',
        'examples_title': 'Typiske opgaver',
        'contact_label': 'Kontakt os',
        'case_label': 'Se et eksempel',
        'about_eyebrow': 'Om Datara',
        'back_home': 'Til forsiden',
        'footer_text': 'Dataanalyse, automatisering og digitale løsninger bygget omkring jeres arbejdsgange.',
        'email_label': 'Skriv til os',
        'privacy': 'Privatliv',
        'cookies': 'Cookies',
        'terms': 'Vilkår',
        'rights': 'Alle rettigheder forbeholdes.',
        'not_found_title': 'Siden blev ikke fundet',
        'not_found_text': 'Adressen findes ikke længere, eller også er den skrevet forkert.',
    },
    'en': {
        'skip_label': 'Skip to content',
        'nav_label': 'Main navigation',
        'home_label': 'Go to the Datara homepage',
        'projects': 'Projects',
        'services': 'Services',
        'contact': 'Contact',
        'language_short': 'DA',
        'language_label': 'Read this page in Danish',
        'service_eyebrow': 'What we can help with',
        'benefits_title': 'What you get from the work',
        'process_title': 'How we work',
        'examples_title': 'Typical tasks',
        'contact_label': 'Contact us',
        'case_label': 'See an example',
        'about_eyebrow': 'About Datara',
        'back_home': 'Back to the homepage',
        'footer_text': 'Data analysis, automation and digital tools built around the way your team works.',
        'email_label': 'Email us',
        'privacy': 'Privacy',
        'cookies': 'Cookies',
        'terms': 'Terms',
        'rights': 'All rights reserved.',
        'not_found_title': 'Page not found',
        'not_found_text': 'The address no longer exists, or it may have been entered incorrectly.',
    },
}


SERVICE_PAGES = {
    'dataanalyse': {
        'content': {
            'da': {
                'seo_title': 'Dataanalyse, der kan bruges | Datara',
                'meta_description': 'Vi samler, klargør og analyserer data, så resultaterne bliver lettere at forstå og handle på.',
                'title': 'Fra data til klare valg',
                'lead': 'Vi samler og rydder op i jeres data, finder de mønstre, der er relevante for opgaven, og forklarer resultaterne i et format, I kan bruge.',
                'benefits': [
                    {'title': 'Et fælles grundlag', 'text': 'Data fra de relevante kilder bliver samlet og kvalitetstjekket, så alle arbejder ud fra det samme udgangspunkt.'},
                    {'title': 'Svar på det rigtige spørgsmål', 'text': 'Analysen tager udgangspunkt i de beslutninger, I faktisk skal træffe – ikke i metoden for metodens skyld.'},
                    {'title': 'En brugbar leverance', 'text': 'I får grafer, modeller eller en rapport, der er tilpasset dem, som skal bruge resultaterne.'},
                ],
                'steps': [
                    {'title': 'Afgræns spørgsmålet', 'text': 'Vi begynder med det, I skal kunne svare på, og vælger derefter de relevante datakilder.'},
                    {'title': 'Klargør data', 'text': 'Vi retter fejl, dokumenterer mangler og sørger for, at datagrundlaget kan efterprøves.'},
                    {'title': 'Analysér og afprøv', 'text': 'Vi vælger den enkleste metode, der kan besvare spørgsmålet, og undersøger, hvor sikkert resultatet er.'},
                    {'title': 'Forklar og følg op', 'text': 'I får resultater, forbehold og konkrete næste skridt i et format, der er nemt at arbejde videre med.'},
                ],
                'examples': [
                    'Oprydning i og samling af Excel- eller systemdata',
                    'Analyse af kunder, drift eller spørgeskemasvar',
                    'Rapporter, visualiseringer og beslutningsoplæg',
                ],
                'cta_title': 'Har I data, der er svære at bruge?',
                'cta_text': 'Fortæl os, hvad I gerne vil kunne svare på. Så vurderer vi, hvilket datagrundlag og hvilken analyse der er nødvendig.',
                'case_href': '/projekter/2',
                'case_text': 'Se fjernvarmekortlægningen',
            },
            'en': {
                'seo_title': 'Data analysis you can use | Datara',
                'meta_description': 'We bring data together, prepare it and analyse it so the results are easier to understand and act on.',
                'title': 'From data to clearer decisions',
                'lead': 'We bring your data together, clean it, find the patterns that matter and explain the results in a format your team can use.',
                'benefits': [
                    {'title': 'A shared foundation', 'text': 'Data from the relevant sources is combined and checked, giving everyone the same starting point.'},
                    {'title': 'Answers to the right question', 'text': 'The analysis starts with the decision you need to make, rather than using a method for its own sake.'},
                    {'title': 'A useful deliverable', 'text': 'You receive charts, models or a report shaped around the people who will use the results.'},
                ],
                'steps': [
                    {'title': 'Define the question', 'text': 'We begin with what you need to answer, then select the data sources that matter.'},
                    {'title': 'Prepare the data', 'text': 'We correct errors, document gaps and make sure the foundation can be checked.'},
                    {'title': 'Analyse and test', 'text': 'We choose the simplest method that can answer the question and examine how robust the result is.'},
                    {'title': 'Explain and follow up', 'text': 'You receive the findings, limitations and practical next steps in a format that is easy to continue working with.'},
                ],
                'examples': [
                    'Cleaning and combining spreadsheet or system data',
                    'Analysis of customers, operations or survey responses',
                    'Reports, visualisations and decision support',
                ],
                'cta_title': 'Do you have data that is difficult to use?',
                'cta_text': 'Tell us what you need to answer. We will assess the data and analysis required.',
                'case_href': '/projekter/2',
                'case_text': 'See the district-heating project',
            },
        },
    },
    'forretningsudvikling': {
        'content': {
            'da': {
                'seo_title': 'Forretningsudvikling med en klar plan | Datara',
                'meta_description': 'Vi bruger data og indsigt i jeres arbejdsgange til at finde flaskehalse, prioritere muligheder og lægge en plan.',
                'title': 'Fra udfordring til prioriteret plan',
                'lead': 'Vi bruger data og kendskab til jeres forretning til at finde flaskehalse, vurdere muligheder og omsætte dem til en plan, der kan gennemføres.',
                'benefits': [
                    {'title': 'Tydeligere prioriteringer', 'text': 'Muligheder bliver vurderet på samme grundlag, så det er lettere at vælge, hvad der skal ske først.'},
                    {'title': 'Mindre spild i processerne', 'text': 'Vi finder de trin, der skaber ventetid, dobbeltarbejde eller unødvendige omkostninger.'},
                    {'title': 'En fælles retning', 'text': 'Planen samler mål, ansvar og næste skridt, så den kan bruges i den daglige ledelse.'},
                ],
                'steps': [
                    {'title': 'Forstå udfordringen', 'text': 'Vi taler med de relevante personer og kortlægger den nuværende situation uden at gøre opgaven større end nødvendigt.'},
                    {'title': 'Undersøg grundlaget', 'text': 'Vi bruger de data, observationer og erfaringer, der kan vise, hvor problemet eller muligheden ligger.'},
                    {'title': 'Prioritér mulighederne', 'text': 'Tiltag bliver vurderet efter effekt, indsats og risiko, så valget er til at forklare.'},
                    {'title': 'Gør planen anvendelig', 'text': 'Vi samler beslutningerne i konkrete aktiviteter med ansvar, rækkefølge og tydelige opfølgningspunkter.'},
                ],
                'examples': [
                    'Kortlægning af arbejdsgange og flaskehalse',
                    'Vurdering og prioritering af nye muligheder',
                    'Beslutningsoplæg og handlingsplaner',
                ],
                'cta_title': 'Er der en udfordring, der bliver ved med at stå i vejen?',
                'cta_text': 'Fortæl os, hvor arbejdet går i stå. Så hjælper vi med at skabe overblik og finde det næste realistiske skridt.',
            },
            'en': {
                'seo_title': 'Business development with a clear plan | Datara',
                'meta_description': 'We use data and insight into your workflows to identify bottlenecks, prioritise opportunities and create a practical plan.',
                'title': 'From challenge to a prioritised plan',
                'lead': 'We use data and an understanding of your business to identify bottlenecks, assess opportunities and turn them into a plan your team can carry out.',
                'benefits': [
                    {'title': 'Clearer priorities', 'text': 'Opportunities are assessed on the same basis, making it easier to decide what should happen first.'},
                    {'title': 'Less waste in your processes', 'text': 'We identify the steps that create waiting time, duplicate work or unnecessary cost.'},
                    {'title': 'A shared direction', 'text': 'The plan brings goals, responsibilities and next steps together for use in day-to-day management.'},
                ],
                'steps': [
                    {'title': 'Understand the challenge', 'text': 'We speak with the people involved and map the current situation without broadening the scope unnecessarily.'},
                    {'title': 'Examine the evidence', 'text': 'We use the data, observations and experience that can show where the problem or opportunity lies.'},
                    {'title': 'Prioritise the options', 'text': 'Actions are assessed for impact, effort and risk, making the choice easier to explain.'},
                    {'title': 'Make the plan usable', 'text': 'We turn the decisions into practical activities with owners, sequence and clear follow-up points.'},
                ],
                'examples': [
                    'Mapping workflows and bottlenecks',
                    'Assessing and prioritising new opportunities',
                    'Decision material and action plans',
                ],
                'cta_title': 'Does the same challenge keep getting in the way?',
                'cta_text': 'Tell us where the work gets stuck. We will help create an overview and identify the next realistic step.',
            },
        },
    },
    'automatisering': {
        'content': {
            'da': {
                'seo_title': 'Automatisering af gentagne arbejdsgange | Datara',
                'meta_description': 'Vi gennemgår gentagne arbejdsgange og automatiserer de trin, der koster tid eller ofte giver fejl.',
                'title': 'Fjern det gentagne arbejde',
                'lead': 'Vi gennemgår jeres arbejdsgange og automatiserer de trin, der er styret af faste regler, tager tid eller ofte fører til fejl. Løsningen bygges omkring de systemer, I allerede bruger.',
                'benefits': [
                    {'title': 'Tid tilbage', 'text': 'Gentagne trin bliver udført automatisk, så medarbejderne kan bruge tiden på opgaver, der kræver faglig vurdering.'},
                    {'title': 'Færre fejl', 'text': 'Faste regler og kontroller giver et mere ensartet resultat end manuel kopiering og indtastning.'},
                    {'title': 'Plads til flere opgaver', 'text': 'Arbejdsgangen kan håndtere større mængder uden en tilsvarende stigning i rutinearbejdet.'},
                ],
                'steps': [
                    {'title': 'Gå arbejdsgangen igennem', 'text': 'Vi følger opgaven fra start til slut og finder de trin, der egner sig til automatisering.'},
                    {'title': 'Byg en afgrænset prototype', 'text': 'En afgrænset prototype viser hurtigt, om reglerne og integrationerne fungerer i praksis.'},
                    {'title': 'Test med rigtige eksempler', 'text': 'Løsningen bliver prøvet af på realistiske data, også de undtagelser, der normalt skaber problemer.'},
                    {'title': 'Dokumentér og overdrag', 'text': 'I får en løsning, der kan forstås, overvåges og justeres, når arbejdsgangen ændrer sig.'},
                ],
                'examples': [
                    'Indtastning, validering og flytning af data',
                    'Automatisk oprettelse af rapporter og dokumenter',
                    'Behandling af formularer, mails eller regneark',
                ],
                'cta_title': 'Hvilken opgave gentager I hver uge?',
                'cta_text': 'Vis os arbejdsgangen. Så vurderer vi, hvad der kan automatiseres, og hvor gevinsten er størst.',
                'case_href': '/projekter/1',
                'case_text': 'Se automatiseringen af 8.000 skemaer',
            },
            'en': {
                'seo_title': 'Automation of repetitive workflows | Datara',
                'meta_description': 'We review repetitive workflows and automate the steps that cost time or often lead to errors.',
                'title': 'Remove the repetitive work',
                'lead': 'We review your workflows and automate the steps that are rule-based, time-consuming or prone to errors. The solution is built around the systems you already use.',
                'benefits': [
                    {'title': 'Time back', 'text': 'Repetitive steps run automatically, leaving people more time for work that needs professional judgement.'},
                    {'title': 'Fewer errors', 'text': 'Fixed rules and checks create a more consistent result than manual copying and data entry.'},
                    {'title': 'Room for more work', 'text': 'The workflow can handle larger volumes without the same increase in routine work.'},
                ],
                'steps': [
                    {'title': 'Walk through the workflow', 'text': 'We follow the task from start to finish and identify the steps suited to automation.'},
                    {'title': 'Build a focused prototype', 'text': 'A focused prototype quickly shows whether the rules and integrations work in practice.'},
                    {'title': 'Test with real examples', 'text': 'The solution is tested with realistic data, including the exceptions that normally cause problems.'},
                    {'title': 'Document and hand over', 'text': 'You receive a solution that can be understood, monitored and adjusted when the workflow changes.'},
                ],
                'examples': [
                    'Entering, validating and transferring data',
                    'Automatic creation of reports and documents',
                    'Processing forms, emails or spreadsheets',
                ],
                'cta_title': 'Which task does your team repeat every week?',
                'cta_text': 'Show us the workflow. We will assess what can be automated and where it will make the greatest difference.',
                'case_href': '/projekter/1',
                'case_text': 'See the automation of 8,000 forms',
            },
        },
    },
    'it-produktudvikling': {
        'content': {
            'da': {
                'seo_title': 'IT-produktudvikling til jeres arbejdsgang | Datara',
                'meta_description': 'Vi udvikler digitale værktøjer omkring jeres brugere og arbejdsgange, fra den første prototype til en løsning i drift.',
                'title': 'Software, der passer til arbejdet',
                'lead': 'Når standardværktøjer ikke passer til opgaven, udvikler vi en løsning omkring jeres brugere og arbejdsgange – fra den første prototype til en version, der kan tages i brug.',
                'benefits': [
                    {'title': 'Bygget til opgaven', 'text': 'Vi vælger funktioner ud fra det arbejde, løsningen skal støtte – ikke ud fra en lang liste af muligheder, ingen bruger.'},
                    {'title': 'Testet med brugerne', 'text': 'Tidlige skitser og prototyper gør det muligt at opdage misforståelser, før de bliver dyre at rette.'},
                    {'title': 'Klar til at udvikle videre', 'text': 'Løsningen bliver dokumenteret og bygget, så den kan vedligeholdes og udvides, når behovet ændrer sig.'},
                ],
                'steps': [
                    {'title': 'Forstå brugerne og opgaven', 'text': 'Vi ser på brugerne, arbejdsgangen og de systemer, løsningen skal fungere sammen med.'},
                    {'title': 'Afprøv retningen', 'text': 'En prototype gør idéen konkret og giver et fælles grundlag for at vælge og fravælge funktioner.'},
                    {'title': 'Byg i overskuelige dele', 'text': 'De vigtigste funktioner bliver udviklet og testet først, så risikoen holdes nede.'},
                    {'title': 'Sæt i drift og følg op', 'text': 'Vi hjælper med lancering, dokumentation og de justeringer, der bliver nødvendige i den daglige brug.'},
                ],
                'examples': [
                    'Interne værktøjer til særlige arbejdsgange',
                    'Webløsninger og enkle selvbetjeningsforløb',
                    'Prototyper til afprøvning af en produktidé',
                ],
                'cta_title': 'Har I en arbejdsgang, som jeres nuværende værktøjer ikke løser?',
                'cta_text': 'Fortæl os, hvem der skal bruge løsningen, og hvad de skal kunne gøre. Så hjælper vi med at afgrænse en første version.',
            },
            'en': {
                'seo_title': 'IT product development for your workflow | Datara',
                'meta_description': 'We develop digital tools around your users and workflows, from the first prototype to a solution in day-to-day use.',
                'title': 'Software that fits the work',
                'lead': 'When standard tools do not fit the task, we build around your users and workflows – from the first prototype to a version ready for day-to-day use.',
                'benefits': [
                    {'title': 'Built for the task', 'text': 'We choose features based on the work the product needs to support, not a long list of options nobody uses.'},
                    {'title': 'Tested with users', 'text': 'Early sketches and prototypes expose misunderstandings before they become expensive to correct.'},
                    {'title': 'Ready to develop further', 'text': 'The solution is documented and built so it can be maintained and extended as needs change.'},
                ],
                'steps': [
                    {'title': 'Understand the users and the task', 'text': 'We examine the users, workflow and systems the product needs to work with.'},
                    {'title': 'Test the direction', 'text': 'A prototype makes the idea concrete and creates a shared basis for choosing which features matter.'},
                    {'title': 'Build in manageable parts', 'text': 'The most important functions are developed and tested first, keeping the risk under control.'},
                    {'title': 'Launch and follow up', 'text': 'We help with launch, documentation and the adjustments that emerge through day-to-day use.'},
                ],
                'examples': [
                    'Internal tools for specialised workflows',
                    'Web solutions and simple self-service tools',
                    'Prototypes for testing a product idea',
                ],
                'cta_title': 'Is there a workflow your current tools do not handle well?',
                'cta_text': 'Tell us who will use the solution and what they need to do. We will help define a useful first version.',
            },
        },
    },
}


INFO_PAGES = {
    'privatliv': {
        'content': {
            'da': {
                'seo_title': 'Privatlivspolitik | Datara',
                'meta_description': 'Læs hvordan Datara behandler og beskytter personoplysninger.',
                'title': 'Privatlivspolitik',
                'intro': 'Her kan du læse, hvilke personoplysninger vi kan modtage, når du besøger hjemmesiden eller skriver til os.',
                'sections': [
                    {'title': 'Hvilke oplysninger kan vi modtage?', 'items': ['Navn, e-mailadresse og de oplysninger, du selv sender til os i en e-mail', 'Tekniske oplysninger, som webserveren kan registrere for at levere og beskytte hjemmesiden, for eksempel IP-adresse, browser og tidspunkt', 'Dit valgte sprog, som gemmes i en nødvendig cookie']},
                    {'title': 'Hvad bruger vi dem til?', 'items': ['At besvare din henvendelse', 'At levere, sikre og fejlfinde hjemmesiden', 'At overholde krav i lovgivningen']},
                    {'title': 'Deling', 'text': 'Oplysninger kan blive behandlet af de leverandører, der driver hjemmesiden og vores e-mail. Vi videregiver dem ikke med henblik på markedsføring og deler dem kun, når det er nødvendigt eller følger af et lovkrav.'},
                    {'title': 'Opbevaring og sikkerhed', 'text': 'Vi opbevarer kun dine oplysninger, så længe det er nødvendigt, og beskytter dem med passende tekniske og organisatoriske foranstaltninger.'},
                    {'title': 'Dine rettigheder', 'text': 'Du kan kontakte os på shn@datara.dk, hvis du vil bede om indsigt, rettelse eller sletning af dine oplysninger.'},
                ],
            },
            'en': {
                'seo_title': 'Privacy policy | Datara',
                'meta_description': 'Read how Datara processes and protects personal data.',
                'title': 'Privacy policy',
                'intro': 'Here you can read which personal data we may receive when you visit the website or email us.',
                'sections': [
                    {'title': 'Which information may we receive?', 'items': ['Your name, email address and any information you choose to include in an email', 'Technical information that the web server may record to deliver and protect the website, such as IP address, browser and time of visit', 'Your language choice, stored in a necessary cookie']},
                    {'title': 'What do we use it for?', 'items': ['To respond to your enquiry', 'To deliver, secure and troubleshoot the website', 'To comply with legal requirements']},
                    {'title': 'Sharing', 'text': 'Data may be processed by the providers that host our website and email service. We do not share it for marketing and disclose it only when necessary or legally required.'},
                    {'title': 'Storage and security', 'text': 'We store your data only for as long as necessary and protect it with appropriate technical and organisational measures.'},
                    {'title': 'Your rights', 'text': 'You can email shn@datara.dk to request access to, correction of or deletion of your data.'},
                ],
            },
        },
    },
    'cookies': {
        'content': {
            'da': {
                'seo_title': 'Cookies | Datara',
                'meta_description': 'Læs om brugen af cookies på Dataras hjemmeside.',
                'title': 'Cookies',
                'intro': 'Hjemmesiden bruger én nødvendig cookie til at huske, om du har valgt dansk eller engelsk. Vi bruger ikke cookies til annoncering eller statistik.',
                'sections': [
                    {'title': 'Sprogcookien', 'text': 'Cookien hedder “site_lang”, indeholder kun dit sprogvalg og gemmes i 30 dage. Den er nødvendig for, at hjemmesiden kan vise det valgte sprog på de næste sider.'},
                    {'title': 'Sådan sletter du den', 'text': 'Du kan slette eller blokere cookien i din browsers indstillinger. Hvis du sletter den, vælger hjemmesiden dansk igen.'},
                    {'title': 'Eksterne links', 'text': 'Hvis du følger et link til for eksempel LinkedIn, gælder den pågældende tjenestes egen cookie- og privatlivspolitik.'},
                ],
            },
            'en': {
                'seo_title': 'Cookies | Datara',
                'meta_description': 'Read about the use of cookies on the Datara website.',
                'title': 'Cookies',
                'intro': 'The website uses one necessary cookie to remember whether you selected Danish or English. We do not use cookies for advertising or analytics.',
                'sections': [
                    {'title': 'The language cookie', 'text': 'The cookie is named “site_lang”, contains only your language choice and is stored for 30 days. It is necessary for the website to show your chosen language on subsequent pages.'},
                    {'title': 'How to delete it', 'text': 'You can delete or block the cookie in your browser settings. If you delete it, the website will default to Danish again.'},
                    {'title': 'External links', 'text': 'If you follow a link to a service such as LinkedIn, that service’s own cookie and privacy policy applies.'},
                ],
            },
        },
    },
    'vilkar': {
        'content': {
            'da': {
                'seo_title': 'Vilkår for brug | Datara',
                'meta_description': 'Læs vilkårene for brug af Dataras hjemmeside.',
                'title': 'Vilkår for brug',
                'intro': 'Disse vilkår gælder for brugen af hjemmesiden. Ved at benytte siden accepterer du vilkårene.',
                'sections': [
                    {'title': 'Ansvar', 'text': 'Vi tilstræber, at informationen på hjemmesiden er korrekt og opdateret, men påtager os ikke ansvar for eventuelle fejl eller mangler.'},
                    {'title': 'Ophavsret', 'text': 'Medmindre andet er angivet, tilhører indholdet Datara I/S eller de respektive rettighedshavere. Materialet må ikke kopieres eller anvendes uden den nødvendige tilladelse.'},
                    {'title': 'Links', 'text': 'Hjemmesiden kan indeholde links til eksterne sider. Vi påtager os ikke ansvar for indholdet på disse sider.'},
                    {'title': 'Ændringer', 'text': 'Vi forbeholder os retten til at ændre vilkår og indhold på hjemmesiden uden varsel.'},
                ],
            },
            'en': {
                'seo_title': 'Terms of use | Datara',
                'meta_description': 'Read the terms for using the Datara website.',
                'title': 'Terms of use',
                'intro': 'These terms apply to the use of the website. By using the site, you accept the terms.',
                'sections': [
                    {'title': 'Liability', 'text': 'We aim to keep the information on the website correct and up to date, but accept no liability for errors or omissions.'},
                    {'title': 'Copyright', 'text': 'Unless otherwise stated, the content belongs to Datara I/S or the respective rights holders. It may not be copied or used without the necessary permission.'},
                    {'title': 'Links', 'text': 'The website may contain links to external sites. We accept no responsibility for the content of those sites.'},
                    {'title': 'Changes', 'text': 'We reserve the right to change the terms and website content without prior notice.'},
                ],
            },
        },
    },
}
