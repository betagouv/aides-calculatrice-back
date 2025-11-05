def affiche_resultat(notion_testee: str, texte_condition: str, bilan_condition: bool, valeur_condition: float):
	# valeur_condition = la valeur initiale (typiquement fournie par l'usager)
    # bilan_condition = la valeur_condition mise au regard de critères d'évaluation
    symbole = "✅" if bilan_condition else "❌"

    print(f"{symbole} {texte_condition}")
    print(notion_testee, " : ", valeur_condition)  # 2 décimales


def colorie_reference(valeur, reference):
    """
    Colorie la valeur en jaune si elle est égale à la référence.
    """
    if str(valeur) == str(reference):
        return 'background-color: yellow'
    else:
        return ''
