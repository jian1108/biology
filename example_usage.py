# Initialize analyzer
analyzer = STARmapAnalyzer('path/to/images.tiff', 'path/to/coordinates.csv')

# Process images
processed_images = analyzer.preprocess_images()

# Detect cells
labels, num_cells = analyzer.detect_cells()

# Calculate expression matrix
expression_matrix = analyzer.calculate_expression_matrix(labels)

# Visualize results
visualize_3d_expression(analyzer.coordinates, 'GeneA')
plot_expression_heatmap(expression_matrix) 