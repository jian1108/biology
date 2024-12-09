import numpy as np
import pandas as pd
from skimage import io
from scipy import ndimage
import matplotlib.pyplot as plt

class STARmapAnalyzer:
    def __init__(self, image_path, coordinates_path):
        self.image_data = None
        self.coordinates = None
        self.expression_matrix = None
        self.load_data(image_path, coordinates_path)
    
    def load_data(self, image_path, coordinates_path):
        """Load imaging and coordinate data"""
        self.image_data = io.imread(image_path)
        self.coordinates = pd.read_csv(coordinates_path)
    
    def preprocess_images(self):
        """Preprocess 3D image stacks"""
        # Basic preprocessing steps
        self.image_data = ndimage.gaussian_filter(self.image_data, sigma=1)
        return self.image_data
    
    def detect_cells(self, threshold=0.5):
        """Cell segmentation using basic thresholding"""
        binary_mask = self.image_data > threshold
        labels, num_cells = ndimage.label(binary_mask)
        return labels, num_cells
    
    def calculate_expression_matrix(self, labels):
        """Generate gene expression matrix"""
        genes = self.coordinates['gene'].unique()
        cells = range(1, labels.max() + 1)
        
        expression_matrix = pd.DataFrame(0, 
                                       index=cells,
                                       columns=genes)
        
        # Count transcripts per cell
        for _, transcript in self.coordinates.iterrows():
            x, y, z = int(transcript['x']), int(transcript['y']), int(transcript['z'])
            if 0 <= x < labels.shape[0] and 0 <= y < labels.shape[1] and 0 <= z < labels.shape[2]:
                cell_id = labels[x, y, z]
                if cell_id > 0:
                    expression_matrix.loc[cell_id, transcript['gene']] += 1
        
        self.expression_matrix = expression_matrix
        return expression_matrix 