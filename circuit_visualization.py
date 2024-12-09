import plotly.graph_objects as go
import networkx as nx
import seaborn as sns
import matplotlib.pyplot as plt

def plot_circuit_modules(circuit_analyzer, behavior_data=None):
    """
    Visualize circuit modules and their relationships
    """
    # Create network graph
    G = nx.from_pandas_adjacency(circuit_analyzer.connectivity_matrix)
    
    # Get layout
    pos = nx.spring_layout(G, dim=3)
    
    # Create figure
    fig = go.Figure()
    
    # Add edges
    edge_x = []
    edge_y = []
    edge_z = []
    
    for edge in G.edges():
        x0, y0, z0 = pos[edge[0]]
        x1, y1, z1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_z.extend([z0, z1, None])
    
    fig.add_trace(go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    ))
    
    # Add nodes
    node_x = []
    node_y = []
    node_z = []
    node_color = []
    
    for node in G.nodes():
        x, y, z = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_z.append(z)
        node_color.append(circuit_analyzer.circuit_modules[node])
    
    fig.add_trace(go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers',
        marker=dict(
            size=6,
            color=node_color,
            colorscale='Viridis',
        ),
        text=circuit_analyzer.circuit_modules,
        hoverinfo='text'
    ))
    
    fig.update_layout(
        title='Neural Circuit Modules',
        showlegend=False
    )
    
    return fig

def plot_behavior_correlations(behavior_analyzer):
    """
    Visualize correlations between circuits and behavior
    """
    plt.figure(figsize=(10, 6))
    sns.heatmap(behavior_analyzer.behavior_correlations,
                cmap='RdBu_r',
                center=0,
                annot=True)
    plt.title('Circuit-Behavior Correlations')
    return plt 