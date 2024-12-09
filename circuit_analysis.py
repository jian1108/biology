import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from sklearn.metrics import pairwise_distances
import networkx as nx

class NeuralCircuitAnalyzer:
    def __init__(self, neuro_analyzer):
        self.neuro_analyzer = neuro_analyzer
        self.connectivity_matrix = None
        self.circuit_modules = None
        self.activity_patterns = None
    
    def construct_connectivity_matrix(self, max_distance=50, synaptic_markers=['SYN1', 'SYP']):
        """
        Construct potential connectivity matrix based on spatial proximity 
        and synaptic marker expression
        """
        coords = self.neuro_analyzer.starmap.coordinates
        expr_matrix = self.neuro_analyzer.starmap.expression_matrix
        
        # Calculate spatial distances
        distances = squareform(pdist(coords[['x', 'y', 'z']]))
        
        # Calculate synaptic strength based on marker expression
        synaptic_strength = expr_matrix[synaptic_markers].mean(axis=1).values
        synaptic_matrix = np.outer(synaptic_strength, synaptic_strength)
        
        # Combine distance and synaptic information
        connectivity = np.where(distances < max_distance, synaptic_matrix, 0)
        self.connectivity_matrix = pd.DataFrame(connectivity,
                                              index=expr_matrix.index,
                                              columns=expr_matrix.index)
        return self.connectivity_matrix
    
    def identify_circuit_modules(self, min_module_size=5):
        """
        Identify functional circuit modules using community detection
        """
        if self.connectivity_matrix is None:
            raise ValueError("Construct connectivity matrix first")
            
        # Create network graph
        G = nx.from_pandas_adjacency(self.connectivity_matrix)
        
        # Detect communities
        communities = nx.community.louvain_communities(G)
        
        # Filter by size and assign modules
        valid_modules = [comm for comm in communities if len(comm) >= min_module_size]
        
        self.circuit_modules = pd.Series(index=self.connectivity_matrix.index)
        for i, module in enumerate(valid_modules):
            self.circuit_modules[list(module)] = f"Module_{i}"
            
        return self.circuit_modules
    
    def analyze_disease_alterations(self, condition_labels, control_label='control'):
        """
        Analyze circuit alterations in disease conditions
        
        Parameters:
        condition_labels: pd.Series
            Labels indicating disease/control status for each sample
        """
        results = {}
        
        # Compare connectivity patterns
        for condition in condition_labels.unique():
            if condition == control_label:
                continue
                
            condition_mask = condition_labels == condition
            control_mask = condition_labels == control_label
            
            # Compare connectivity matrices
            conn_diff = (self.connectivity_matrix.loc[condition_mask].mean() - 
                        self.connectivity_matrix.loc[control_mask].mean())
            
            # Compare module preservation
            condition_modules = self.identify_circuit_modules()
            module_overlap = self._calculate_module_preservation(
                condition_modules[condition_mask],
                condition_modules[control_mask]
            )
            
            results[condition] = {
                'connectivity_changes': conn_diff,
                'module_preservation': module_overlap
            }
            
        return results
    
    def _calculate_module_preservation(self, modules1, modules2):
        """Helper function to calculate module preservation between conditions"""
        from sklearn.metrics import adjusted_rand_score
        return adjusted_rand_score(modules1, modules2) 