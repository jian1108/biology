import plotly.express as px
import seaborn as sns

def visualize_3d_expression(coordinates, gene):
    """
    Create 3D visualization of gene expression
    """
    gene_coords = coordinates[coordinates['gene'] == gene]
    
    fig = px.scatter_3d(gene_coords, 
                        x='x', y='y', z='z',
                        color='intensity',
                        title=f'Spatial distribution of {gene}')
    return fig

def plot_expression_heatmap(expression_matrix):
    """
    Create heatmap of gene expression
    """
    plt.figure(figsize=(12, 8))
    sns.heatmap(expression_matrix, 
                cmap='viridis',
                xticklabels=True,
                yticklabels=True)
    plt.title('Gene Expression Heatmap')
    plt.show() 