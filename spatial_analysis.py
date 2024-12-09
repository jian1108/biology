from scipy.spatial import distance
from sklearn.neighbors import NearestNeighbors

def analyze_spatial_patterns(coordinates, gene_names):
    """
    Analyze spatial patterns of gene expression
    """
    def calculate_spatial_correlation(gene1, gene2):
        coords1 = coordinates[coordinates['gene'] == gene1][['x', 'y', 'z']]
        coords2 = coordinates[coordinates['gene'] == gene2][['x', 'y', 'z']]
        
        # Calculate nearest neighbor distances
        nbrs = NearestNeighbors(n_neighbors=1).fit(coords2)
        distances, _ = nbrs.kneighbors(coords1)
        
        return np.mean(distances)
    
    # Calculate spatial correlation matrix
    correlation_matrix = pd.DataFrame(index=gene_names, columns=gene_names)
    
    for gene1 in gene_names:
        for gene2 in gene_names:
            if gene1 != gene2:
                correlation = calculate_spatial_correlation(gene1, gene2)
                correlation_matrix.loc[gene1, gene2] = correlation
    
    return correlation_matrix 