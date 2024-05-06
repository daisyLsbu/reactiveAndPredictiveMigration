from PyMCDA import AHPModel

# Define the attributes and their hierarchy
attributes = {
    'CPU': {},
    'NW': {},
    'STG': {},
    'MEM': {},
}

# Define the pairwise comparison matrix for attribute comparisons
comparison_matrix = {
    ('CPU', 'NW'): 3,    # Adjust the values based on pairwise comparisons
    ('CPU', 'STG'): 2,
    ('CPU', 'MEM'): 4,
    ('NW', 'STG'): 1/2,
    ('NW', 'MEM'): 2/3,
    ('STG', 'MEM'): 1,
}

# Create an AHP model
ahp_model = AHPModel(attributes, comparison_matrix)

# Calculate the weights
weights = ahp_model.calculate_weights()

# Define the performance values for each attribute (between 0 and 1)
performance_values = {
    'CPU': 0.8,
    'NW': 0.6,
    'STG': 0.7,
    'MEM': 0.9,
}

# Calculate the overall utilization
utilization = sum(weights[attr] * performance_values[attr] for attr in attributes)

# Print the weights and utilization
print("Weights:")
for attr, weight in weights.items():
    print(f"{attr}: {weight}")

print(f"Utilization: {utilization}")
