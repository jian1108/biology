import cv2
from scipy import ndimage

def process_image_stack(image_stack):
    """
    Process 3D image stack
    """
    processed_stack = np.zeros_like(image_stack, dtype=np.float32)
    
    for z in range(image_stack.shape[0]):
        # Background subtraction
        processed_stack[z] = cv2.subtract(image_stack[z], 
                                        cv2.medianBlur(image_stack[z], 101))
        
        # Denoise
        processed_stack[z] = cv2.fastNlMeansDenoising(processed_stack[z].astype(np.uint8))
        
        # Enhance contrast
        processed_stack[z] = cv2.equalizeHist(processed_stack[z].astype(np.uint8))
    
    return processed_stack 