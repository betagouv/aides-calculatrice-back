
import streamlit as st
from notebooks.situation import situation_18yo_moving_away as situation_to_explain
# TODO ajouter la période au json aides-simplifiées

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


st.markdown("En secteur locatif ordinaire, l'APL est calculée comme :")
st.markdown("* un `loyer pris en compte` (`L`) éventuellement plafonné,")
st.markdown("* additionné d'un `forfait de charges` (`C`),")
st.markdown("* auquel est retirée une `participation personnelle` (`Pp`) \
			qui est déterminée en fonction des ressources du ménage et de sa composition familiale.")
st.markdown("Ainsi le montant d'APL alloué est égal à `L + C - Pp`")

# L est le loyer mensuel réel pris en compte dans la limite d’un plafond variable en fonction de trois zones géographiques et du nombre de personnes à charge.
