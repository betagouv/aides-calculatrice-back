
import streamlit as st
from notebooks.situation import situation_18yo_moving_away


st.title("Comprendre le montant d'APL")

st.markdown("L'APL s'applique à un parc de logement déterminé. \
			L'évaluation du montant alloué sera différente \
			selon que vous soyez en secteur locatif ordinaire, \
			en secteur foyer ou en accession.")
st.markdown("Vous avez indiqué demander l'APL pour un **logement en secteur locatif ordinaire**.")


# récupération des réponses au questionnaire aides-simplifiées
answers = situation_18yo_moving_away["answers"]

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


