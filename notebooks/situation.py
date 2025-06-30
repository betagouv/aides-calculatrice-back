situation_18yo_moving_away = {
    "id": "18yo-moving-away",
    "description": "Un jeune de 18 ans déménage pour des études à l'université",
    "answers": {
        "statut-professionnel": "etudiant",  # activite
        "situation-professionnelle": "sans-emploi",  # dispatchSituationProfessionnelle
        "etudiant-mobilite": "parcoursup-nouvelle-region",  # dispatchEtudiantMobilite
        "boursier": True,  # boursier
        "date-naissance": "2007-03-01",  # date_naissance
        "handicap": False,  # handicap
        "statut-marital": "celibataire",  # statut_marital
        "code-postal-nouvelle-ville": "75101",  # depcom
        "situation-logement": "locataire",  # dispatchSituationLogement
        "type-logement": "logement-meuble",  # dispatchTypeLogement
        "logement-conventionne": True,  # logement_conventionne
        "colocation": False,  # coloc
        "logement-parente-proprietaire": False,  # proprietaire_proche_famille
        "nombre-personnes-logement": 1,  # 🔥 exclude: True
        "loyer-montant-mensuel": 700,  # loyer
        "loyer-montant-charges": 100,  # charges_locatives
        "loyer-difficile-payer": True,  # exclude: True
        "type-revenus": [
            "aucun-autres-revenus"
        ],
        "confirmation-end": [
            "confirmation-end-oui"
        ]
    },
    "questionsToApi": [
        "locapass-eligibilite",
        "mobilite-master-1",
        "mobilite-parcoursup",
        "aide-personnalisee-logement",
        "garantie-visale-eligibilite",
        "garantie-visale"
    ],
    "results": {
        "locapass": 1200,
        "locapass-eligibilite": True,
        "mobilite-master-1": 0,
        "mobilite-master-1-eligibilite": False,
        "mobilite-parcoursup": 500,
        "mobilite-parcoursup-eligibilite": True,
        "aide-personnalisee-logement": 327,
        "aide-personnalisee-logement-eligibilite": True,
        "garantie-visale": 800,
        "garantie-visale-eligibilite": True
    }
}


to_test = situation_18yo_moving_away
