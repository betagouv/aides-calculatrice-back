
import streamlit as st
from numpy import round

from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_france import FranceTaxBenefitSystem

from notebooks.situation import situation_18yo_moving_away as situation_to_explain
from notebooks.utils_mapping_simulateur import format_to_openfisca_json


# initialisation d'une simulation sur la base de la situation déjà calculée

# TODO ajouter la période au json aides-simplifiées
SIMULATION_MONTH = "2025-01"
situation_apl = format_to_openfisca_json(situation_to_explain, SIMULATION_MONTH)
tax_benefit_system = FranceTaxBenefitSystem()
sb = SimulationBuilder()
simulation = sb.build_from_entities(tax_benefit_system, situation_apl)


st.title("Comprendre le montant d'APL")

st.markdown("L'APL s'applique à un parc de logement déterminé. \
			L'évaluation du montant alloué sera différente \
			selon que vous soyez en secteur locatif ordinaire, \
			en secteur foyer ou en accession.")
st.markdown("Vous avez indiqué demander l'APL pour un **logement en secteur locatif ordinaire**.")


# récupération des réponses au questionnaire aides-simplifiées
answers = situation_to_explain["answers"]

# transcription des réponses d'après le type détecté
with st.expander("Consulter toutes les réponses fournies au simulateur..."):
	for key, value in answers.items():
		if isinstance(value, bool):
			st.checkbox(key, value=value, key=key)
		elif isinstance(value, int) or isinstance(value, float):
			st.number_input(key, value=value, key=key)
		elif isinstance(value, str):
			st.text_input(key, value=value, key=key)
		elif isinstance(value, list):
			st.multiselect(key, options=value, default=value, key=key)
		else:
			st.write(f"Champ '{key}': {type(value)} non transcrit.")

# L
aide_logement_loyer_retenu = round(simulation.calculate('aide_logement_loyer_retenu', SIMULATION_MONTH)[0])
# C
aide_logement_charges = round(simulation.calculate('aide_logement_charges', SIMULATION_MONTH)[0])
# Pp
aide_logement_participation_personnelle = round(simulation.calculate('aide_logement_participation_personnelle', SIMULATION_MONTH)[0])


st.markdown("En secteur locatif ordinaire, l'APL est calculée comme :")
st.markdown("* un `loyer pris en compte` (`L`) éventuellement plafonné,")
st.markdown("* additionné d'un `forfait de charges` (`C`),")
st.markdown("* auquel est retirée une `participation personnelle` (`Pp`) \
			qui est déterminée en fonction des ressources du ménage et de sa composition familiale.")
st.markdown("Ainsi le montant d'APL alloué est égal à `L + C - Pp`")

st.markdown("## Votre loyer pris en compte")
st.markdown("L est le loyer mensuel réel pris en compte dans la limite \
			d’un plafond variable en fonction de trois zones géographiques \
			et du nombre de personnes à charge.")
st.markdown(f"L = {aide_logement_loyer_retenu}")


st.markdown("## Votre forfait charges pris en compte")
st.markdown(f"C = {aide_logement_charges}")

st.markdown("## Votre participation personnelle")
st.markdown(f"Pp = {aide_logement_participation_personnelle}")
