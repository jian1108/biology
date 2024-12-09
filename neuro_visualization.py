import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

def plot_cell_type_distribution(coordinates, cell_types):
    """
    Visualize spatial distribution of cell types in 3D
    """
    fig = go.Figure()
    
    for cell_type in cell_types.unique():
        mask = cell_types == cell_type
        cell_coords = coordinates[mask]
        
        fig.add_trace(go.Scatter3d(
            x=cell_coords['x'],
            y=cell_coords['y'],
            z=cell_coords['z'],
            mode='markers',
            name=cell_type,
            marker=dict(size=3)
        ))
    
    fig.update_layout(title='Spatial Distribution of Cell Types')
    return fig

def plot_domain_interactions(spatial_domains, expression_matrix):
    """
    Visualize interactions between spatial domains
    """
    domain_means = pd.DataFrame()
    for domain in spatial_domains.unique():
        domain_means[domain] = expression_matrix[spatial_domains == domain].mean()
    
    plt.figure(figsize=(10, 8))
    sns.clustermap(domain_means.corr(), 
                   cmap='RdBu_r',
                   center=0,
                   annot=True)
    plt.title('Domain Interaction Map')
    return plt 