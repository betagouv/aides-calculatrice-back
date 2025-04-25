from datetime import datetime
from dateutil.relativedelta import relativedelta
from numpy import timedelta64

from openfisca_core.parameters import Parameter
from openfisca_core.simulation_builder import SimulationBuilder, Simulation
from openfisca_core.taxbenefitsystems import TaxBenefitSystem

from openfisca_france import FranceTaxBenefitSystem


today = datetime.now()
today_year_month = today.strftime("%Y-%m")
period = today_year_month  # par exemple : '2025-04'

last_month = today - relativedelta(months=1)
period_last_month  = last_month.strftime("%Y-%m")

france_tax_benefit_system = FranceTaxBenefitSystem()


def new_simulation(tax_benefit_system, situation_json_openfisca):
    sb = SimulationBuilder()
    simulation = sb.build_from_entities(tax_benefit_system, situation_json_openfisca)
    return simulation


def est_dans_intervalle(
        simulation: Simulation, nom_openfisca: str, 
        valeur_min: float, valeur_max: float, 
        description: str, index_entite = 0) -> bool:

    truc = simulation.calculate(nom_openfisca, period)
    condition_truc = truc[index_entite] >= valeur_min and truc[index_entite] <= valeur_max 
    affiche_resultat(nom_openfisca, description, condition_truc, truc[index_entite])

    return condition_truc


def est_strictement_superieur_seuil(
        simulation: Simulation, nom_openfisca: str, 
        seuil: float,
        description: str, index_entite = 0) -> bool:

    truc = simulation.calculate(nom_openfisca, period)
    condition_truc = truc[index_entite] > seuil
    affiche_resultat(nom_openfisca, description, condition_truc, truc[index_entite])

    return condition_truc


def est_inferieur_ou_egal_plafond(
        simulation: Simulation, nom_openfisca: str, period: int | str,
        plafond: float,
        description: str, index_entite = 0) -> bool:
     
    truc = simulation.calculate(nom_openfisca, period)
    condition_truc = truc[index_entite] <= plafond
    affiche_resultat(nom_openfisca, f"[{period}] {description}", condition_truc, truc[index_entite])

    return condition_truc


def est_pas_enum_dans_liste(
        simulation: Simulation, nom_openfisca: str, 
        valeurs_enum: list, enum_names,
        description: str, index_entite = 0) -> bool:
     
    truc_enum = simulation.calculate(nom_openfisca, period)
    condition_truc = enum_names[truc_enum[index_entite]] not in valeurs_enum
    affiche_resultat(nom_openfisca, description, condition_truc, enum_names[truc_enum[index_entite]])

    return condition_truc


def est_enum_dans_liste(
        simulation: Simulation, nom_openfisca: str, 
        valeurs_enum: list, enum_names,
        description: str, index_entite = 0) -> bool:
     
    truc_enum = simulation.calculate(nom_openfisca, period)
    condition_truc = enum_names[truc_enum[index_entite]] in valeurs_enum
    affiche_resultat(nom_openfisca, description, condition_truc, enum_names[truc_enum[index_entite]])

    return condition_truc


def date_de_moins_de_nb_mois(
        simulation: Simulation, nom_openfisca: str,
        duree_mois_max: int,
        description: str, index_entite = 0) -> bool:

    truc_date = simulation.calculate(nom_openfisca, period)
    duree_mois_depuis_truc_date = truc_date.astype('timedelta64[M]')

    truc_date_par_defaut = france_tax_benefit_system.get_variable(nom_openfisca).default_value
    condition_truc = (
        truc_date != truc_date_par_defaut  # date renseignée
        ) * ( duree_mois_depuis_truc_date <= timedelta64(duree_mois_max, 'M')  # depuis moins de 'duree_mois_max' mois
        )
    
    affiche_resultat(nom_openfisca, description, condition_truc, truc_date[index_entite])
    return condition_truc    


def non_renseignee_ou_egale_valeur_par_defaut(
        tax_benefit_system: TaxBenefitSystem, simulation: Simulation, nom_openfisca: str,
        description: str, index_entite = 0) -> bool:
        
    truc = simulation.calculate(nom_openfisca, period)
    truc_default_value = tax_benefit_system.get_variable(nom_openfisca).default_value
    condition_truc = truc[index_entite] == truc_default_value

    affiche_resultat(nom_openfisca, description, condition_truc, truc[index_entite])
    return condition_truc


def get_yearly_parameter_references(p: Parameter, year: str):
    p_references: dict = p.metadata['reference']
    year_references = {cle: valeur for cle, valeur in p_references.items() if cle.startswith(year)}
    return year_references


def get_latest_parameter_references(p: Parameter):
    p_references: dict = p.metadata['reference']

    dates = [datetime.strptime(key, '%Y-%m-%d') for key in p_references.keys()]
    latest_date = max(dates)
    latest_key = latest_date.strftime('%Y-%m-%d')

    return p_references[latest_key]
