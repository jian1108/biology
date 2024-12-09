# Initialize analyzers
starmap = STARmapAnalyzer('brain_section.tiff', 'coordinates.csv')
neuro_analyzer = NeuroscienceSTARmapAnalyzer(starmap)

# Define neural cell type markers
neural_markers = {
    'excitatory_neurons': ['SLC17A7', 'CAMK2A'],
    'inhibitory_neurons': ['GAD1', 'GAD2'],
    'astrocytes': ['GFAP', 'S100B'],
    'oligodendrocytes': ['MBP', 'MOG'],
    'microglia': ['CX3CR1', 'IBA1']
}

# Identify cell types
cell_types = neuro_analyzer.identify_cell_types(neural_markers)

# Analyze spatial domains
spatial_domains = neuro_analyzer.analyze_spatial_domains()

# Analyze neural connectivity
synaptic_markers = ['SYN1', 'SYP', 'DLG4']
connectivity = neuro_analyzer.analyze_neural_connectivity(synaptic_markers)

# Statistical analysis
stat_analyzer = NeuralStatisticalAnalyzer(
    starmap.expression_matrix,
    cell_types,
    spatial_domains
)

# Perform differential expression analysis
de_results = stat_analyzer.differential_expression(
    cell_types == 'excitatory_neurons',
    cell_types == 'inhibitory_neurons'
)

# Visualize results
plot_cell_type_distribution(starmap.coordinates, cell_types)
plot_domain_interactions(spatial_domains, starmap.expression_matrix) 