from IPython.display import display
import ipywidgets as widgets


def add_input(label, placeholder):
    # Créer un champ de texte pour l'input
    text_input = widgets.Text(
        value='',
        placeholder=placeholder if type(placeholder) == str else str(placeholder),
        description=label,
        disabled=False,
        layout=widgets.Layout(
            width="300px",
            description_width="500px"
        )
    )

    return text_input
    

def display_inputs(entity_roles, entity_data):
    entity_inputs = []
    for variable, period_value in entity_data.items():
        if variable not in entity_roles:
            period, value = next(iter(period_value.items()))
            input = add_input(variable + " " + period, value)
            entity_inputs.append(input)
            display(input)

    return entity_inputs


def add_output():
    # Créer une zone de sortie pour afficher le message
    output = widgets.Output()

    return output


def add_calculate_button(inputs, output):
    # Créer un bouton
    button = widgets.Button(
        description='Calculer',
        disabled=False,
        button_style='', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Cliquez pour calculer',
        icon='check'
    )

    def on_button_click(b):
        with output:
            # Effacer la sortie précédente
            output.clear_output()

            for input in inputs:
                input_value = input.value
                print(f"Bonjour, {input_value} !")
                # input.value = ""

    # Attacher la fonction de rappel au bouton
    button.on_click(on_button_click)

    return button
