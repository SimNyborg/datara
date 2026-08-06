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
        'benefits_title': 'Det får I',
        'process_title': 'Sådan arbejder vi',
        'examples_title': 'Eksempler',
        'contact_label': 'Kontakt os',
        'case_label': 'Se et eksempel',
        'about_eyebrow': 'Om Datara',
        'back_home': 'Til forsiden',
        'footer_text': 'Dataanalyse, automatisering og digitale løsninger bygget omkring jeres arbejdsgange.',
        'email_label': 'Skriv til os',
        'privacy': 'Privatliv',
        'cookies': 'Cookies',
        'terms': 'Vilkår',
        'footer_nav_label': 'Juridiske links',
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
        'benefits_title': 'What you get',
        'process_title': 'How we work',
        'examples_title': 'Examples',
        'contact_label': 'Contact us',
        'case_label': 'See an example',
        'about_eyebrow': 'About Datara',
        'back_home': 'Back to the homepage',
        'footer_text': 'Data analysis, automation and digital tools built around the way your team works.',
        'email_label': 'Email us',
        'privacy': 'Privacy',
        'cookies': 'Cookies',
        'terms': 'Terms',
        'footer_nav_label': 'Legal links',
        'rights': 'All rights reserved.',
        'not_found_title': 'Page not found',
        'not_found_text': 'The address no longer exists, or it may have been entered incorrectly.',
    },
}


HOME_SERVICE_ORDER = {
    'da': (
        'automatisering',
        'dataanalyse',
        'forretningsudvikling',
        'it-produktudvikling',
    ),
    'en': (
        'automatisering',
        'forretningsudvikling',
        'dataanalyse',
        'it-produktudvikling',
    ),
}


HOME_SERVICE_CARDS = {
    'dataanalyse': {
        'da': {
            'title': 'Dataanalyse',
            'summary': 'Indsamling, strukturering og analyse af data.',
        },
        'en': {
            'title': 'Data analysis',
            'summary': 'Collection, structuring and analysis of data.',
        },
    },
    'forretningsudvikling': {
        'da': {
            'title': 'Forretningsudvikling',
            'summary': 'Analyse af arbejdsgange, muligheder og prioriteringer.',
        },
        'en': {
            'title': 'Business development',
            'summary': 'Analysis of workflows, opportunities and priorities.',
        },
    },
    'automatisering': {
        'da': {
            'title': 'Automatisering',
            'summary': 'Automatisering af faste og gentagne arbejdsgange.',
        },
        'en': {
            'title': 'Automation',
            'summary': 'Automation of fixed, repetitive workflow steps.',
        },
    },
    'it-produktudvikling': {
        'da': {
            'title': 'IT-produktudvikling',
            'summary': 'Udvikling af software til konkrete arbejdsgange.',
        },
        'en': {
            'title': 'IT product development',
            'summary': 'Development of software for specific workflows.',
        },
    },
}


SERVICE_PAGES = {
    'dataanalyse': {
        'content': {
            'da': {
                'seo_title': 'Indsamling og analyse af data | Datara',
                'meta_description': 'Vi indsamler, kontrollerer og analyserer data ud fra et konkret spørgsmål og præsenterer resultatet til videre brug.',
                'title': 'Indsamling og analyse af data',
                'lead': 'Vi starter med det spørgsmål, data skal belyse. Derefter samler, kontrollerer og analyserer vi de relevante data. Resultatet dokumenteres og præsenteres, så det kan bruges i det videre arbejde.',
                'benefits_title': 'Hvad analysen omfatter',
                'process_title': 'Fra spørgsmål til resultat',
                'benefits': [
                    {'title': 'Et kontrolleret datagrundlag', 'text': 'Vi samler data fra de relevante kilder og beskriver fejl, mangler og de valg, der er truffet undervejs.'},
                    {'title': 'En metode til spørgsmålet', 'text': 'Vi vælger metode ud fra spørgsmålet, datamængden og den usikkerhed, der er i data.'},
                    {'title': 'Et resultat til videre brug', 'text': 'Vi viser resultatet i grafer, tabeller, kort eller en kort rapport, alt efter hvordan det skal bruges.'},
                ],
                'steps': [
                    {'title': 'Afgræns spørgsmålet', 'text': 'Vi afklarer, hvad analysen skal belyse, og hvilke data der kan bruges.'},
                    {'title': 'Saml og kontrollér data', 'text': 'Vi samler data, retter fejl og beskriver mangler og usikkerheder.'},
                    {'title': 'Analysér data', 'text': 'Vi vælger en metode, der passer til spørgsmålet, og undersøger, hvor sikkert resultatet er.'},
                    {'title': 'Dokumentér resultatet', 'text': 'Vi samler resultaterne og forklarer, hvordan de besvarer det spørgsmål, analysen begyndte med.'},
                ],
                'cta_title': 'Er jeres data svære at bruge?',
                'cta_text': 'Fortæl os, hvad I vil have svar på. Så vurderer vi, hvilke data og hvilken analyse der er brug for.',
            },
            'en': {
                'seo_title': 'Data collection and analysis | Datara',
                'meta_description': 'We collect, check and analyse data for a defined question and present the result for further use.',
                'title': 'Data collection and analysis',
                'lead': 'We begin with the question the data should help answer. We then collect, check and analyse the relevant data. The result is documented and presented so it can be used in the work that follows.',
                'benefits_title': 'What the analysis includes',
                'process_title': 'From question to result',
                'benefits': [
                    {'title': 'A checked set of data', 'text': 'We bring together data from the relevant sources and describe errors, gaps and the choices made along the way.'},
                    {'title': 'A method for the question', 'text': 'We choose the method according to the question, the amount of data and the uncertainty in it.'},
                    {'title': 'A result for further use', 'text': 'We present the result in charts, tables, maps or a short report, depending on how it will be used.'},
                ],
                'steps': [
                    {'title': 'Define the question', 'text': 'We clarify what the analysis needs to address and which data can be used.'},
                    {'title': 'Collect and check the data', 'text': 'We bring the data together, correct errors and describe gaps and uncertainty.'},
                    {'title': 'Analyse the data', 'text': 'We choose a method suited to the question and examine how reliable the result is.'},
                    {'title': 'Document the result', 'text': 'We bring the findings together and explain how they answer the question that started the analysis.'},
                ],
                'cta_title': 'Is your data hard to use?',
                'cta_text': 'Tell us what you need to answer. We will assess which data and analysis are needed.',
            },
        },
    },
    'forretningsudvikling': {
        'content': {
            'da': {
                'seo_title': 'Analyse, prioritering og planlægning | Datara',
                'meta_description': 'Vi undersøger arbejdsgange og data, sammenligner mulige tiltag og samler de valgte handlinger i en plan.',
                'title': 'Analyse, prioritering og planlægning',
                'lead': 'Vi starter med en konkret udfordring eller mulighed. Derefter samler vi viden om arbejdet, undersøger data og vurderer mulige tiltag. Resultatet er en prioriteret plan med ansvar og næste skridt.',
                'benefits_title': 'Hvad arbejdet omfatter',
                'process_title': 'Fra udfordring til plan',
                'benefits': [
                    {'title': 'Et samlet billede af arbejdet', 'text': 'Vi samler data, observationer og erfaringer fra dem, der kender arbejdsgangen.'},
                    {'title': 'Muligheder på samme grundlag', 'text': 'Vi vurderer mulige tiltag efter effekt, indsats og risiko, så de kan sammenlignes.'},
                    {'title': 'En plan med ansvar', 'text': 'Vi beskriver rækkefølge, ansvar og opfølgning for de tiltag, der bliver valgt.'},
                ],
                'steps': [
                    {'title': 'Afgræns udfordringen', 'text': 'Vi afklarer, hvad der skal ændres, og hvem der bliver berørt.'},
                    {'title': 'Kortlæg arbejdsgangen', 'text': 'Vi gennemgår arbejdet og finder ventetid, dobbeltarbejde og andre flaskehalse.'},
                    {'title': 'Vurder mulighederne', 'text': 'Vi sammenligner mulige tiltag ud fra effekt, indsats og risiko.'},
                    {'title': 'Læg planen', 'text': 'Vi sætter de valgte tiltag i rækkefølge og beskriver ansvar og opfølgning.'},
                ],
                'examples': [
                    'Kortlægning af arbejdsgange og flaskehalse',
                    'Sammenligning og prioritering af mulige tiltag',
                    'Beslutningsoplæg med ansvar og næste skridt',
                ],
                'cta_title': 'Hvor går arbejdet i stå?',
                'cta_text': 'Fortæl os om udfordringen. Så hjælper vi med at skabe overblik og finde et realistisk næste skridt.',
            },
            'en': {
                'seo_title': 'Analysis, prioritisation and planning | Datara',
                'meta_description': 'We examine workflows and data, compare possible actions and bring the selected actions together in a plan.',
                'title': 'Analysis, prioritisation and planning',
                'lead': 'We begin with a specific challenge or opportunity. We then gather knowledge about the work, examine the data and assess possible actions. The result is a prioritised plan with responsibilities and next steps.',
                'benefits_title': 'What the work includes',
                'process_title': 'From challenge to plan',
                'benefits': [
                    {'title': 'A shared view of the work', 'text': 'We bring together data, observations and experience from the people who know the workflow.'},
                    {'title': 'Options assessed on the same basis', 'text': 'We assess possible actions by impact, effort and risk so they can be compared.'},
                    {'title': 'A plan with responsibilities', 'text': 'We set out the order, responsibilities and follow-up for the actions that are selected.'},
                ],
                'steps': [
                    {'title': 'Define the challenge', 'text': 'We clarify what needs to change and who will be affected.'},
                    {'title': 'Map the workflow', 'text': 'We review the work and identify waiting time, duplicate work and other bottlenecks.'},
                    {'title': 'Assess the options', 'text': 'We compare possible actions by impact, effort and risk.'},
                    {'title': 'Make the plan', 'text': 'We put the selected actions in order and describe responsibilities and follow-up.'},
                ],
                'examples': [
                    'Mapping workflows and bottlenecks',
                    'Comparing and prioritising possible actions',
                    'Decision papers with responsibilities and next steps',
                ],
                'cta_title': 'Where does the work get stuck?',
                'cta_text': 'Tell us about the challenge. We will help create an overview and identify a realistic next step.',
            },
        },
    },
    'automatisering': {
        'content': {
            'da': {
                'seo_title': 'Automatisering af gentagne arbejdsgange | Datara',
                'meta_description': 'Vi gennemgår arbejdsgange og automatiserer de trin, der følger faste regler.',
                'title': 'Automatisering af arbejdsgange',
                'lead': 'Vi gennemgår en arbejdsgang trin for trin og automatiserer de dele, der følger faste regler. Når en opgave handler om at læse, sortere eller udtrække oplysninger fra tekst, kan AI indgå som et afgrænset trin. Løsningen kobles til de systemer, I allerede bruger.',
                'benefits_title': 'Hvad automatiseringen ændrer',
                'process_title': 'Fra arbejdsgang til løsning',
                'benefits': [
                    {'title': 'Mindre manuel håndtering', 'text': 'Indtastning og kontrol kan udføres automatisk, mens faglige vurderinger fortsat ligger hos medarbejderne.'},
                    {'title': 'Færre fejl', 'text': 'Faste regler og kontroller mindsker fejl ved kopiering og indtastning.'},
                    {'title': 'Større datamængder', 'text': 'Den samme arbejdsgang kan behandle flere filer eller registreringer, uden at hvert trin skal gentages manuelt.'},
                ],
                'steps': [
                    {'title': 'Afgræns arbejdsgangen', 'text': 'Vi følger opgaven fra start til slut og udpeger de trin, der følger faste regler.'},
                    {'title': 'Afprøv reglerne', 'text': 'Vi bygger en enkel prototype og kontrollerer reglerne og forbindelserne til de eksisterende systemer.'},
                    {'title': 'Test med faktiske eksempler', 'text': 'Vi afprøver løsningen på almindelige sager og på de undtagelser, der normalt kræver manuel håndtering. Hvis AI indgår, kontrollerer vi også svarene mod kendte eksempler.'},
                    {'title': 'Dokumentér løsningen', 'text': 'Vi beskriver, hvordan løsningen kontrolleres og justeres, når arbejdsgangen ændrer sig.'},
                ],
                'examples': [
                    'Indtastning, kontrol og flytning af data',
                    'Automatisk oprettelse af rapporter og dokumenter',
                    'Behandling af formularer, mails og regneark',
                    'Sortering og udtræk af oplysninger fra tekst med AI',
                ],
                'cta_title': 'Hvilken opgave gentager I hver uge?',
                'cta_text': 'Vis os arbejdsgangen. Så vurderer vi, hvad der kan automatiseres, og hvor det kan spare mest tid eller forhindre flest fejl.',
                'case_href': '/projekter/1',
                'case_text': 'Se automatiseringen af 8.000 skemaer',
            },
            'en': {
                'seo_title': 'Automation of repetitive workflows | Datara',
                'meta_description': 'We review workflows and automate the steps governed by fixed rules.',
                'title': 'Workflow automation',
                'lead': 'We review a workflow step by step and automate the parts governed by fixed rules. When a task involves reading, sorting or extracting information from text, AI can be used as a clearly defined step. The solution connects to the systems you already use.',
                'benefits_title': 'What automation changes',
                'process_title': 'From workflow to solution',
                'benefits': [
                    {'title': 'Less manual handling', 'text': 'Data entry and checks can run automatically, while professional judgements remain with your staff.'},
                    {'title': 'Fewer errors', 'text': 'Fixed rules and checks reduce errors in copying and data entry.'},
                    {'title': 'Larger data volumes', 'text': 'The same workflow can process more files or records without each step being repeated manually.'},
                ],
                'steps': [
                    {'title': 'Define the workflow', 'text': 'We follow the task from start to finish and identify the steps governed by fixed rules.'},
                    {'title': 'Test the rules', 'text': 'We build a simple prototype and check the rules and connections to the existing systems.'},
                    {'title': 'Test with actual examples', 'text': 'We test the solution on ordinary cases and on the exceptions that usually require manual handling. If AI is involved, we also check its outputs against known examples.'},
                    {'title': 'Document the solution', 'text': 'We describe how the solution is checked and adjusted when the workflow changes.'},
                ],
                'examples': [
                    'Entering, checking and transferring data',
                    'Automatic creation of reports and documents',
                    'Processing forms, emails and spreadsheets',
                    'Sorting and extracting information from text with AI',
                ],
                'cta_title': 'Which task does your team repeat every week?',
                'cta_text': 'Show us the workflow. We will assess what can be automated and where it can save the most time or prevent the most errors.',
                'case_href': '/projekter/1',
                'case_text': 'See the automation of 8,000 forms',
            },
        },
    },
    'it-produktudvikling': {
        'content': {
            'da': {
                'seo_title': 'Udvikling af software til arbejdsgange | Datara',
                'meta_description': 'Vi afgrænser, udvikler og tester software til konkrete arbejdsgange og bruger AI i udviklingen, når det er relevant.',
                'title': 'Udvikling af software til arbejdsgange',
                'lead': 'Vi starter med den arbejdsgang og de brugere, softwaren skal understøtte. Derefter afgrænser vi funktionerne, bygger en prototype og afprøver den med faktiske opgaver. Når opgaven egner sig til det, bruger vi AI som udviklingsværktøj, fordi det kan forkorte udviklingstiden og reducere omkostningerne.',
                'benefits_title': 'Hvad udviklingen omfatter',
                'process_title': 'Fra behov til software',
                'benefits': [
                    {'title': 'Funktioner afgrænset til opgaven', 'text': 'Vi bygger de funktioner, der er nødvendige for arbejdsgangen, og undlader resten.'},
                    {'title': 'Afprøvning med brugerne', 'text': 'Vi tester skitser og prototyper med faktiske opgaver, før hele løsningen bliver bygget.'},
                    {'title': 'Kode, der kan vedligeholdes', 'text': 'Vi dokumenterer løsningen, så fejl kan rettes og funktioner ændres, når behovet opstår.'},
                ],
                'steps': [
                    {'title': 'Afgræns behovet', 'text': 'Vi gennemgår brugerne, arbejdsgangen og de systemer, løsningen skal fungere sammen med.'},
                    {'title': 'Byg en prototype', 'text': 'Vi bygger en enkel version af de vigtigste funktioner og afprøver den tidligt.'},
                    {'title': 'Udvikl og test', 'text': 'Vi udvikler løsningen trin for trin og tester den med faktiske opgaver. Kode lavet med hjælp fra AI bliver gennemgået og testet som anden kode.'},
                    {'title': 'Sæt løsningen i drift', 'text': 'Vi dokumenterer løsningen, overdrager den og aftaler, hvordan fejl og ændringer håndteres.'},
                ],
                'examples': [
                    'Interne værktøjer til konkrete arbejdsgange',
                    'Webløsninger og enkle selvbetjeningsforløb',
                    'Prototyper til afprøvning af nye funktioner',
                ],
                'cta_title': 'Har I en arbejdsgang, som jeres nuværende værktøjer ikke løser?',
                'cta_text': 'Fortæl os, hvem der skal bruge løsningen, og hvad de skal kunne gøre. Så hjælper vi med at afgrænse den første version.',
            },
            'en': {
                'seo_title': 'Software development for workflows | Datara',
                'meta_description': 'We define, develop and test software for specific workflows and use AI in development when relevant.',
                'title': 'Software development for workflows',
                'lead': 'We begin with the workflow and the people the software needs to support. We then define the features, build a prototype and test it with actual tasks. When the task is suitable, we use AI as a development tool because it can shorten development time and reduce costs.',
                'benefits_title': 'What development includes',
                'process_title': 'From need to software',
                'benefits': [
                    {'title': 'Features defined by the task', 'text': 'We build the features needed for the workflow and leave out the rest.'},
                    {'title': 'Testing with users', 'text': 'We test sketches and prototypes with actual tasks before building the full solution.'},
                    {'title': 'Code that can be maintained', 'text': 'We document the solution so errors can be corrected and features changed when needed.'},
                ],
                'steps': [
                    {'title': 'Define the need', 'text': 'We review the users, workflow and systems the solution needs to work with.'},
                    {'title': 'Build a prototype', 'text': 'We build a simple version of the main features and test it early.'},
                    {'title': 'Develop and test', 'text': 'We develop the solution step by step and test it with actual tasks. Code produced with AI support is reviewed and tested in the same way as other code.'},
                    {'title': 'Put the solution into use', 'text': 'We document and hand over the solution and agree how errors and changes will be handled.'},
                ],
                'examples': [
                    'Internal tools for specific workflows',
                    'Web solutions and simple tools customers can use themselves',
                    'Prototypes for testing new features',
                ],
                'cta_title': 'Is there a workflow your current tools do not handle well?',
                'cta_text': 'Tell us who will use the solution and what they need to do. We will help define the first version.',
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
                    {'title': 'Hvilke oplysninger kan vi modtage?', 'items': ['Navn, e-mailadresse og de oplysninger, du selv sender til os i en e-mail', 'Tekniske oplysninger, som webserveren kan registrere for at levere og beskytte hjemmesiden, for eksempel IP-adresse, browser og tidspunkt']},
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
                    {'title': 'Which information may we receive?', 'items': ['Your name, email address and any information you choose to include in an email', 'Technical information that the web server may record to deliver and protect the website, such as IP address, browser and time of visit']},
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
                'intro': 'Hjemmesiden bruger ikke cookies. Vi bruger heller ikke cookies til annoncering eller statistik.',
                'sections': [
                    {'title': 'Ingen cookies', 'text': 'Hjemmesiden sætter ingen cookies. Dit sprogvalg gemmes ikke i browseren, men fremgår af adressen, hvor de engelske sider ligger under “/en/”.'},
                    {'title': 'Eksterne links', 'text': 'Hvis du følger et link til for eksempel LinkedIn, gælder den pågældende tjenestes egen cookie- og privatlivspolitik.'},
                ],
            },
            'en': {
                'seo_title': 'Cookies | Datara',
                'meta_description': 'Read about the use of cookies on the Datara website.',
                'title': 'Cookies',
                'intro': 'The website does not use cookies. Nor do we use cookies for advertising or analytics.',
                'sections': [
                    {'title': 'No cookies', 'text': 'The website sets no cookies. Your language choice is not stored in the browser; it is reflected in the address instead, with the English pages located under “/en/”.'},
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
