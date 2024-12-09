from scipy import stats
from statsmodels.stats.multitest import multipletests

class NeuralStatisticalAnalyzer:
    def __init__(self, expression_matrix, cell_types, spatial_domains):
        self.expression_matrix = expression_matrix
        self.cell_types = cell_types
        self.spatial_domains = spatial_domains
        
    def differential_expression(self, group1, group2, method='t-test'):
        """
        Perform differential expression analysis between two groups
        """
        results = pd.DataFrame(index=self.expression_matrix.columns)
        
        for gene in self.expression_matrix.columns:
            g1_expr = self.expression_matrix.loc[group1, gene]
            g2_expr = self.expression_matrix.loc[group2, gene]
            
            if method == 't-test':
                stat, pval = stats.ttest_ind(g1_expr, g2_expr)
            elif method == 'wilcoxon':
                stat, pval = stats.ranksums(g1_expr, g2_expr)
                
            results.loc[gene, 'statistic'] = stat
            results.loc[gene, 'pvalue'] = pval
        
        # Multiple testing correction
        results['padj'] = multipletests(results['pvalue'], method='fdr_bh')[1]
        return results
    
    def spatial_autocorrelation(self, gene, coordinates):
        """
        Calculate Moran's I spatial autocorrelation for gene expression
        """
        from libpysal.weights import DistanceBand
        from esda.moran import Moran
        
        # Create weight matrix based on distances
        w = DistanceBand.from_array(coordinates[['x', 'y', 'z']].values)
        
        # Calculate Moran's I
        moran = Moran(self.expression_matrix[gene], w)
        return {
            'I': moran.I,
            'p_value': moran.p_sim
        } 