import numpy as np
import pandas as pd
from scipy import stats
from sklearn.decomposition import PCA

class BehavioralCircuitAnalyzer:
    def __init__(self, circuit_analyzer):
        self.circuit_analyzer = circuit_analyzer
        self.behavior_correlations = None
        self.activity_behavior_mapping = None
    
    def correlate_with_behavior(self, behavioral_data, behavior_metrics):
        """
        Correlate circuit activity patterns with behavioral metrics
        
        Parameters:
        behavioral_data: pd.DataFrame
            Behavioral measurements for each sample
        behavior_metrics: list
            List of behavioral metrics to analyze
        """
        circuit_activity = self.circuit_analyzer.connectivity_matrix
        
        correlations = pd.DataFrame(index=behavior_metrics,
                                  columns=['correlation', 'p_value'])
        
        for metric in behavior_metrics:
            # Calculate correlation between circuit activity and behavior
            corr_matrix = []
            p_matrix = []
            
            for i in range(len(circuit_activity)):
                corr, p = stats.pearsonr(circuit_activity.iloc[i],
                                       behavioral_data[metric])
                corr_matrix.append(corr)
                p_matrix.append(p)
            
            correlations.loc[metric] = [np.mean(corr_matrix), np.mean(p_matrix)]
        
        self.behavior_correlations = correlations
        return correlations
    
    def identify_behavior_circuits(self, behavioral_data, behavior,
                                 significance_threshold=0.05):
        """
        Identify circuits specifically associated with a behavior
        
        Parameters:
        behavioral_data: pd.DataFrame
            Behavioral measurements
        behavior: str
            Specific behavior to analyze
        """
        # Get circuit modules
        modules = self.circuit_analyzer.circuit_modules
        
        behavior_circuits = {}
        
        for module in modules.unique():
            module_mask = modules == module
            
            # Calculate correlation between module activity and behavior
            module_activity = self.circuit_analyzer.connectivity_matrix.loc[module_mask].mean()
            
            corr, p_val = stats.pearsonr(module_activity,
                                        behavioral_data[behavior])
            
            if p_val < significance_threshold:
                behavior_circuits[module] = {
                    'correlation': corr,
                    'p_value': p_val
                }
        
        return behavior_circuits 