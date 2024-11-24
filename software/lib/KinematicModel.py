import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Définir les paramètres DH pour chaque articulation
# Chaque ligne : [a_i, alpha_i, d_i, theta_i]
dh_parameters = np.array([
    [0, 0, 20, 0],           # Articulation 1
    [54.85, np.pi/2, 0, 0],  # Articulation 2
    [0, -np.pi/2, 0, 0],     # Articulation 3
])

# Fonction pour calculer la matrice de transformation homogène à partir des paramètres DH
def dh_to_transformation(a, alpha, d, theta):
    return np.array([
        [np.cos(theta), -np.sin(theta) * np.cos(alpha), np.sin(theta) * np.sin(alpha), a * np.cos(theta)],
        [np.sin(theta), np.cos(theta) * np.cos(alpha), -np.cos(theta) * np.sin(alpha), a * np.sin(theta)],
        [0, np.sin(alpha), np.cos(alpha), d],
        [0, 0, 0, 1]
    ])

# Calcul des positions des articulations
def forward_kinematics_DH(dh_parameters):
    x = [0]  # Origine
    y = [0]
    z = [0]

    # Matrice de transformation homogène initiale
    T = np.eye(4)

    for params in dh_parameters:
        a, alpha, d, theta = params
        # Calculer la matrice de transformation pour cette articulation
        T_link = dh_to_transformation(a, alpha, d, theta)
        # Mettre à jour la matrice globale
        T = T @ T_link

        # Ajouter la position de la nouvelle articulation
        x.append(T[0, 3])
        y.append(T[1, 3])
        z.append(T[2, 3])

    return x, y, z

# Fonction pour vérifier le MGD
def verify_forward_kinematics(dh_parameters, expected_positions):
    # Calculer les positions avec la fonction de cinématique directe
    x, y, z = forward_kinematics_DH(dh_parameters)
    computed_positions = np.array([x, y, z]).T  # Positions calculées

    # Comparer avec les positions attendues
    differences = np.linalg.norm(computed_positions - expected_positions, axis=1)

    # Afficher les différences pour chaque articulation
    for i, diff in enumerate(differences):
        print(f"Articulation {i}: Différence = {diff:.6f}")
    
    # Vérifier si les différences sont acceptables
    if np.all(differences < 1e-6):  # Tolérance de 1e-6
        print("Les calculs de MGD sont corrects (différence négligeable).")
    else:
        print("Les calculs de MGD présentent des écarts significatifs.")





# Calcul des positions avec les paramètres DH
x, y, z = forward_kinematics_DH(dh_parameters)

print (x)
print (y)
print (z)

# Visualisation avec Matplotlib
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z, '-o', label="Robot 3R (DH)")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.legend()
plt.title("Configuration du robot 3R avec paramètres DH")
plt.show()


# Définir les positions attendues pour les articulations (valeurs manuelles ou connues)
# Exemple : Les coordonnées doivent être en fonction des paramètres DH pour un cas fixe.
expected_positions = np.array([
    [0, 0, 0],            # Origine
    [0, 0, 20],           # Après la première articulation
    [54.85, 0, 20],       # Après la deuxième articulation
    [54.85, 0, 20]        # Après la troisième articulation (modifiez si attendu diffère)
])

# Vérifier les résultats du MGD
verify_forward_kinematics(dh_parameters, expected_positions)
