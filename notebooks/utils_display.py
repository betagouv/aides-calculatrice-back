def colorie_reference(valeur, reference):
    """
    Colorie la valeur en jaune si elle est égale à la référence.
    """
    if str(valeur) == str(reference):
        return 'background-color: yellow'
    else:
        return ''
