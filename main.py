from pulp import LpMinimize, LpProblem, lpSum, LpVariable

# Définir les ingrédients et leurs compositions
ingredients = {
    "Maïs": {"protéines": 8.5, "énergie": 13.5, "calcium": 0.02, "phosphore": 0.28, "coût": 0.2},
    "Tourteau de soja": {"protéines": 44.0, "énergie": 12.0, "calcium": 0.25, "phosphore": 0.65, "coût": 0.4},
    "Farine de poisson": {"protéines": 65.0, "énergie": 13.0, "calcium": 5.0, "phosphore": 3.0, "coût": 1.2},
    "Phosphate bicalcique": {"protéines": 0.0, "énergie": 0.0, "calcium": 24.0, "phosphore": 18.0, "coût": 0.8},
    "Sel": {"protéines": 0.0, "énergie": 0.0, "calcium": 0.0, "phosphore": 0.0, "coût": 0.1}
}

# Définir les besoins nutritionnels
besoins = {
    "protéines": 21.0,  # % minimum
    "énergie": 12.8,    # MJ/kg minimum
    "calcium": 0.95,    # % minimum
    "phosphore": 0.45   # % minimum
}

# Créer le modèle
model = LpProblem(name="formulation_aliment_poulet", sense=LpMinimize)

# Définir les variables
vars = LpVariable.dicts("proportion", ingredients.keys(), lowBound=0, upBound=1)

# Objectif : minimiser le coût
model += lpSum([ingredients[ingr]["coût"] * vars[ingr] for ingr in ingredients]), "Coût total"

# Contraintes
model += lpSum([vars[ingr] for ingr in ingredients]) == 1, "Somme des proportions"
model += lpSum([ingredients[ingr]["protéines"] * vars[ingr] for ingr in ingredients]) >= besoins["protéines"] / 100, "Protéines"
model += lpSum([ingredients[ingr]["énergie"] * vars[ingr] for ingr in ingredients]) >= besoins["énergie"], "Énergie"
model += lpSum([ingredients[ingr]["calcium"] * vars[ingr] for ingr in ingredients]) >= besoins["calcium"] / 100, "Calcium"
model += lpSum([ingredients[ingr]["phosphore"] * vars[ingr] for ingr in ingredients]) >= besoins["phosphore"] / 100, "Phosphore"

# Résoudre
status = model.solve()

# Afficher les résultats
if status == 1:
    print("Formulation optimale pour poulets de chair :")
    for var in model.variables():
        print(f"{var.name.replace('proportion_', '')}: {var.varValue * 100:.2f}%")
    print(f"Coût total : {model.objective.value():.2f} $/kg")
else:
    print("Erreur : Impossible de trouver une formulation optimale.")