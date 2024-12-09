# Initialize analyzers
circuit_analyzer = NeuralCircuitAnalyzer(neuro_analyzer)
behavior_analyzer = BehavioralCircuitAnalyzer(circuit_analyzer)

# Construct connectivity matrix
connectivity = circuit_analyzer.construct_connectivity_matrix(max_distance=50)

# Identify circuit modules
modules = circuit_analyzer.identify_circuit_modules()

# Example behavioral data
behavioral_data = pd.DataFrame({
    'sample_id': range(len(starmap.coordinates)),
    'locomotion': np.random.rand(len(starmap.coordinates)),
    'anxiety': np.random.rand(len(starmap.coordinates)),
    'memory': np.random.rand(len(starmap.coordinates))
})

# Analyze behavior correlations
behavior_metrics = ['locomotion', 'anxiety', 'memory']
correlations = behavior_analyzer.correlate_with_behavior(
    behavioral_data,
    behavior_metrics
)

# Identify circuits related to specific behavior
memory_circuits = behavior_analyzer.identify_behavior_circuits(
    behavioral_data,
    'memory'
)

# Disease analysis
condition_labels = pd.Series(['control', 'disease'] * (len(starmap.coordinates)//2))
disease_alterations = circuit_analyzer.analyze_disease_alterations(condition_labels)

# Visualize results
plot_circuit_modules(circuit_analyzer)
plot_behavior_correlations(behavior_analyzer) 