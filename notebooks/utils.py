def dispatch_situation_logement(answer_situation_logement: str | None):
	if (answer_situation_logement == 'locataire'):
		# TypesStatutOccupationLogement: 'locataire_foyer', 'locataire_hlm', 'locataire_meuble', 'locataire_vide'
		# TODO ici et aides-simulateur-front : prendre en compte 'type-logement' ("logement-foyer"...)
		return 'locataire_vide'
	
	if (answer_situation_logement == 'proprietaire'):
		# TypesStatutOccupationLogement: 'proprietaire' (could also be a subset: 'primo_accedant')
		return 'proprietaire'
	
	if (answer_situation_logement == 'heberge'):
		return 'loge_gratuitement'

	if (answer_situation_logement == 'sans-domicile'):
		return 'sans_domicile'
	
	return 'non_renseigne'


def dispatch_to_activite(
		answer_statut_professionnel: str | None,
		answer_situation_professionnelle: str | None
		):
	
	if answer_statut_professionnel != None:
		return answer_statut_professionnel

	if (answer_situation_professionnelle == 'salarie-hors-alternance'):
		# TypesActivite possible values: https://legislation.fr.openfisca.org/activite
		return 'actif'  # 'activite'

	if (answer_situation_professionnelle == 'sans-emploi'):
		# TypesActivite possible values: https://legislation.fr.openfisca.org/activite
		return 'chomeur'  # 'activite'


def format_to_openfisca_json(aides_simplifiees_test_case, period):
	# TODO autres revenus
    # bourse_criteres_sociaux
    # salaire_imposable
    # chomage_imposable
    # rpns_imposables

    # décrit la situation au format d'une requête d'API web, sans les variables à calculer
    openfisca_test_case = {
        "individus": {
            "usager": {
                "date_naissance": {
                    "ETERNITY": aides_simplifiees_test_case["answers"]["date-naissance"]
                },
                "handicap": {
                    period: aides_simplifiees_test_case["answers"]["handicap"] if aides_simplifiees_test_case["answers"]["handicap"] else False
                },
                "statut_marital": {
                    period: aides_simplifiees_test_case["answers"]["statut-marital"] if aides_simplifiees_test_case["answers"]["statut-marital"] else "celibataire"
                },
                "activite": {
                    period: dispatch_to_activite(aides_simplifiees_test_case["answers"]["statut-professionnel"], aides_simplifiees_test_case["answers"]["situation-professionnelle"])
                },
                "stagiaire": {
                    period: aides_simplifiees_test_case["answers"]["situation-professionnelle"] == "stage"
                },
                "alternant": {
                    period: aides_simplifiees_test_case["answers"]["situation-professionnelle"] == "alternance"
                },
                "sortie_academie": {
                    period: aides_simplifiees_test_case["answers"]["etudiant-mobilite"] == "parcoursup-nouvelle-region"  # false si etudiant-mobilite == 'pas-de-mobilite'
                },
                "sortie_region_academique": {
                    period: aides_simplifiees_test_case["answers"]["etudiant-mobilite"] == "master-nouvelle-zone"  # false si etudiant-mobilite == 'pas-de-mobilite'
                }
            }
        },
        "foyers_fiscaux": {
            "foyer_fiscal_1": {
                "declarants": [
                    "usager"
                ],
                "personnes_a_charge": []
            }
        },
        "menages": {
            "menage_1": {
                "conjoint": [],
                "enfants": [],
                "personne_de_reference": [
                    "usager"
                ],
                "depcom": {
                    # TODO conserver le code insee dans les inputs du front
                    # TODO en attendant, convertir ici de code postal vers code insee ?
                    period: aides_simplifiees_test_case["answers"]["code-postal-nouvelle-ville"] if aides_simplifiees_test_case["answers"]["code-postal-nouvelle-ville"] else ""
                },
                "statut_occupation_logement": {
                    # TODO adapter la valeur
                    period: dispatch_situation_logement(aides_simplifiees_test_case["answers"]["situation-logement"])
                },
                "loyer": {
                    period: aides_simplifiees_test_case["answers"]["loyer-montant-mensuel"] if aides_simplifiees_test_case["answers"]["loyer-montant-mensuel"] else 0.0
                },
                "charges_locatives": {
                    period: aides_simplifiees_test_case["answers"]["loyer-montant-charges"]
                },
                "coloc": {
                    period: aides_simplifiees_test_case["answers"]["colocation"]
                },
                "logement_conventionne": {
                    period: aides_simplifiees_test_case["answers"]["logement-conventionne"]
                }
            }
        },
        "familles": {
            "famille_1": {
                "enfants": [],
                "parents": [
                    "usager"
                ],
                "proprietaire_proche_famille": {
                    period: aides_simplifiees_test_case["answers"]["logement-parente-proprietaire"]
                }
            }
        }
    }

    return openfisca_test_case


def affiche_resultat(notion_testee: str, texte_condition: str, bilan_condition: bool, valeur_condition: float):
	symbole = "✅" if bilan_condition else "❌"

	print(f"{symbole} {texte_condition}")
	print(f"{notion_testee} : {valeur_condition}")
