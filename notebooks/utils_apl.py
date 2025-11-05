from numpy import round
from pandas import DataFrame, Index

from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_france import FranceTaxBenefitSystem
from openfisca_france.model.prestations.aides_logement import TypesZoneApl, TypesStatutOccupationLogement

from notebooks.utils_mapping_simulateur import format_to_openfisca_json

from situation import to_test


NB_DECIMALES = 2


# DÉFINITION DES PÉRIODES DES DONNÉES ET DES CALCULS 

from datetime import datetime
from dateutil.relativedelta import relativedelta

from openfisca_core.periods import Instant, Period

today = datetime.now()

today_year_month = today.strftime("%Y-%m")
period = today_year_month  # par exemple : '2025-04'
last_month = today - relativedelta(months=1)
period_last_month  = last_month.strftime("%Y-%m")

year = today.strftime("%Y")
last_year = (today - relativedelta(years=1)).strftime("%Y")
two_years_ago = (today - relativedelta(years=2)).strftime("%Y")
last_twelve_months = Period(('year', Instant((int(year), int(today.strftime("%m")), 1)), 1)).offset(-1).offset(-1, 'month')  # année glissante


# SITUATION ANALYSÉE

situation_apl = format_to_openfisca_json(to_test, period)

# CALCUL DE L'APL

tax_benefit_system = FranceTaxBenefitSystem()

sb = SimulationBuilder()
simulation = sb.build_from_entities(tax_benefit_system, situation_apl)

apl_variables = ['apl', 'logement_conventionne', 'aide_logement_montant', 'aide_logement_montant_brut', 'zone_apl']
# apl_variables_entities = ['familles', 'menages', 'familles', 'familles', 'menages']
# apl_variables_groupes = ['famille_1', 'menage_1', 'famille_1', 'famille_1', 'menage_1']

parametres_secteur_locatif_period = tax_benefit_system.parameters(period).prestations_sociales.aides_logement.allocations_logement.locatif

# Pour mémoire, à partir d'ici, tous les simulation.calculate d'une variable impliquée dans le calcul 'apl'
# fera appel au cache des valeurs de la simulation (n'impliquera pas de re-calcul)


# ANALYSE DE LA SITUATION FAMILIALE

en_couple = simulation.calculate('en_couple', period)[0]
celibataire = ~en_couple
label_situation_maritale = 'en couple' if en_couple else 'célibataire'

al_nb_personnes_a_charge = simulation.calculate('al_nb_personnes_a_charge', period)[0]
au_moins_une_personne_a_charge = al_nb_personnes_a_charge > 0

# SITUATION DU LOGEMENT

zone_apl = simulation.calculate('zone_apl', period)[0]
id_zone_apl_applicable = TypesZoneApl.names[zone_apl]

logement_chambre = simulation.calculate('logement_chambre', period)[0]

statut_occupation_logement = simulation.calculate('statut_occupation_logement', period)[0]
location_meuble = statut_occupation_logement == TypesStatutOccupationLogement.locataire_meuble

coloc = simulation.calculate('coloc', period)[0]

loyer = simulation.calculate('loyer', period)[0]

# CALCUL DE L - LOYER PRIS EN COMPTE

# aide_logement_loyer_plafond (intégrant la zone_apl, la situation familiale, la colocation et le logement chambre)
# aide_logement_loyer_reel (intégrant les coefficients  de chambre et logement meublé)
aide_logement_loyer_retenu = simulation.calculate('aide_logement_loyer_retenu', period)[0]
L_calcule = round(aide_logement_loyer_retenu, NB_DECIMALES)


loyer_plafond_toute_situation = None

# RECUPERATION DES PARAMETRES DE PLAFOND DE LOYER PAR ZONE APL

id_zone_1 = TypesZoneApl.names[1]
id_zone_2 = TypesZoneApl.names[2]
id_zone_3 = TypesZoneApl.names[3]

parametres_locatif_zone_1 = parametres_secteur_locatif_period.formule.l_plafonds_loyers.par_zone[id_zone_1]
parametres_locatif_zone_2 = parametres_secteur_locatif_period.formule.l_plafonds_loyers.par_zone[id_zone_2]
parametres_locatif_zone_3 = parametres_secteur_locatif_period.formule.l_plafonds_loyers.par_zone[id_zone_3]

plafond_loyer_period_zone = parametres_secteur_locatif_period.formule.l_plafonds_loyers.par_zone[id_zone_apl_applicable]


# TABLEAU LOGEMENT CHAMBRE

# TODO tableau complémentaire personne âgée ou handicapée adulte hébergée à titre onéreux chez des particuliers

# if logement_chambre:
coef_chambre = parametres_secteur_locatif_period.formule.l_plafonds_loyers.coef_chambre_et_colocation.coef_chambre
plafond_loyer_applicable_chambre = coef_chambre * plafond_loyer_period_zone.personnes_seules
loyer_plafond_toute_situation = plafond_loyer_applicable_chambre

data_parametres_chambre = {
    ('Logement chambre (cas général)', 'Montant'): [
        coef_chambre * parametres_locatif_zone_1.personnes_seules,
        coef_chambre * parametres_locatif_zone_2.personnes_seules,
        coef_chambre * parametres_locatif_zone_3.personnes_seules
        ]
}

index = Index([id_zone_1, id_zone_2, id_zone_3], name='Zone')
df_parametres_chambre = DataFrame(data_parametres_chambre, index=index)


# TABLEAU SANS PERSONNE À CHARGE

data_parametres_sans_personne_a_charge = {
    'Zone': [id_zone_1, id_zone_2, id_zone_3],
    'Personne seule': [parametres_locatif_zone_1.personnes_seules, parametres_locatif_zone_2.personnes_seules, parametres_locatif_zone_3.personnes_seules],
    'Couple': [parametres_locatif_zone_1.couples, parametres_locatif_zone_2.couples, parametres_locatif_zone_3.couples]
}

df_parametres_sans_personne_a_charge = DataFrame(data_parametres_sans_personne_a_charge)

# Définir la colonne 'Zone' comme index (optionnel, pour correspondre à l'exemple de la brochure APL)
df_parametres_sans_personne_a_charge = df_parametres_sans_personne_a_charge.set_index('Zone')

# TABLEAU AVEC PERSONNE À CHARGE

def get_plafond_loyer(zone_parameters, nb_personnes_a_charge):
    premier_enfant = zone_parameters.un_enfant if nb_personnes_a_charge > 0 else 0
    return premier_enfant + (zone_parameters.majoration_par_enf_supp * max(0, nb_personnes_a_charge - 1))

data_parametres_avec_personne_a_charge = {
    ('Personne seule ou couple', '1'): [parametres_locatif_zone_1.un_enfant, parametres_locatif_zone_2.un_enfant, parametres_locatif_zone_3.un_enfant],
    ('Personne seule ou couple', '2'): [get_plafond_loyer(parametres_locatif_zone_1, 2), get_plafond_loyer(parametres_locatif_zone_2, 2), get_plafond_loyer(parametres_locatif_zone_3, 2)],
    ('Personne seule ou couple', '3'): [get_plafond_loyer(parametres_locatif_zone_1, 3), get_plafond_loyer(parametres_locatif_zone_2, 3), get_plafond_loyer(parametres_locatif_zone_3, 3)],
    ('Personne seule ou couple', '4'): [get_plafond_loyer(parametres_locatif_zone_1, 4), get_plafond_loyer(parametres_locatif_zone_2, 4), get_plafond_loyer(parametres_locatif_zone_3, 4)],
    ('Personne seule ou couple', '5'): [get_plafond_loyer(parametres_locatif_zone_1, 5), get_plafond_loyer(parametres_locatif_zone_2, 5), get_plafond_loyer(parametres_locatif_zone_3, 5)],
    ('', 'Par pàc sup.'): [parametres_locatif_zone_1.majoration_par_enf_supp, parametres_locatif_zone_2.majoration_par_enf_supp, parametres_locatif_zone_3.majoration_par_enf_supp]
}

index = Index([id_zone_1, id_zone_2, id_zone_3], name='Zone')
df_parametres_avec_personne_a_charge = DataFrame(data_parametres_avec_personne_a_charge, index=index)

# Réorganiser les colonnes pour correspondre à l'ordre souhaité
df_parametres_avec_personne_a_charge = df_parametres_avec_personne_a_charge[[('Personne seule ou couple', '1'), ('Personne seule ou couple', '2'),
         ('Personne seule ou couple', '3'), ('Personne seule ou couple', '4'),
         ('Personne seule ou couple', '5'), ('', 'Par pàc sup.')]]

df_parametres_avec_personne_a_charge.columns.names = [None, 'Nombre de personnes à charge (pàc)']


# IDENTIFICATION DU PLAFOND DE LOYER APPLICABLE

from utils_calculate import get_latest_parameter_references
from utils_apl import al_nb_personnes_a_charge, au_moins_une_personne_a_charge, celibataire, get_plafond_loyer, plafond_loyer_period_zone

plafond_loyer_applicable = None
if (~logement_chambre and ~coloc):  # TODO ajouter hors sous-location
    if au_moins_une_personne_a_charge:
        plafond_loyer_applicable = get_plafond_loyer(plafond_loyer_period_zone, al_nb_personnes_a_charge)
        loyer_plafond_toute_situation = plafond_loyer_applicable

    else:
        plafond_loyer_applicable = plafond_loyer_period_zone['personnes_seules' if celibataire else 'couples']
        loyer_plafond_toute_situation = plafond_loyer_applicable


L_analyse = min(loyer, loyer_plafond_toute_situation)
condition_verification_L = (round(L_calcule, NB_DECIMALES) - L_analyse) <= 0.001  # marge d'erreur pour écarts numpy.float32 et float (ici largement supérieure)


# C - Forfait charges pris en compte

aide_logement_charges = simulation.calculate('aide_logement_charges', period)[0]
C_calcule = aide_logement_charges

forfait_charges_toute_situation = None

# paramètres forfait charges - cas général
montant_forfaitaire_charges_seul_ou_couple = parametres_secteur_locatif_period.formule.c_forfait_charges.cas_general.cas_general
montant_majoration_charges_par_enfant = parametres_secteur_locatif_period.formule.c_forfait_charges.cas_general.majoration_par_enfant


# TABLEAU SANS PERSONNE À CHARGE - CAS GÉNÉRAL
# TODO cas des colocataires

# if (~au_moins_une_personne_a_charge):
forfait_charges_applicable = montant_forfaitaire_charges_seul_ou_couple
forfait_charges_toute_situation = forfait_charges_applicable

data_parametres_charges_sans_personne_a_charge = {
    'Personne seule ou en couple': [montant_forfaitaire_charges_seul_ou_couple]
}

index = Index(['Cas général'], name='Cas')
df_parametres_charges_sans_personne_a_charge = DataFrame(data_parametres_charges_sans_personne_a_charge, index=index)


# if au_moins_une_personne_a_charge:
forfait_charges_applicable = montant_forfaitaire_charges_seul_ou_couple + al_nb_personnes_a_charge * montant_majoration_charges_par_enfant
forfait_charges_toute_situation = forfait_charges_applicable

data_parametres_charges_avec_personne_a_charge = {
    ('Personne seule ou couple', '1'): [montant_forfaitaire_charges_seul_ou_couple + montant_majoration_charges_par_enfant],
    ('Personne seule ou couple', '2'): [montant_forfaitaire_charges_seul_ou_couple + 2 * montant_majoration_charges_par_enfant],
    ('Personne seule ou couple', '3'): [montant_forfaitaire_charges_seul_ou_couple + 3 * montant_majoration_charges_par_enfant],
    ('', 'Par pàc sup.'): [montant_majoration_charges_par_enfant]
}

index = Index(['Cas général'], name='Cas')
df_parametres_charges_avec_personne_a_charge = DataFrame(data_parametres_charges_avec_personne_a_charge, index=index)

# Réorganiser les colonnes pour correspondre à l'ordre souhaité
df_parametres_charges_avec_personne_a_charge = df_parametres_charges_avec_personne_a_charge[[
    ('Personne seule ou couple', '1'),
    ('Personne seule ou couple', '2'),
    ('Personne seule ou couple', '3'),
    ('', 'Par pàc sup.')]]

df_parametres_charges_avec_personne_a_charge.columns.names = [None, 'Nombre de personnes à charge (pàc)']

