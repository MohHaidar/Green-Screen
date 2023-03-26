import cv2 
import numpy as np
from PIL import Image

def selectColor(image: np.array, color: tuple, threshold: int):
    '''
    Finds the pixels matching a given color inside the image and within a specified threshold
    
    Args:
        image: np.array containing the RGB image to look for
        color: tuple representing the color in RGB format
        threshold: int with the threshold to look within
    return:
        np.array of shape = img.shape[:2] wth values 0 and 1 representing the mask
    '''
    color_upper = (color[0]+threshold, color[1]+threshold, color[2]+threshold)
    color_lower = (color[0]-threshold, color[1]-threshold, color[2]-threshold)
    
    mask = (((image[:,:,0]<=color_upper[0]) & (image[:,:,0]>=color_lower[0])) & ((image[:,:,1]<=color_upper[1]) & (image[:,:,1]>=color_lower[1])) & ((image[:,:,2]<=color_upper[2]) & (image[:,:,2]>=color_lower[2]))).astype('uint8')
    
    return mask

##############

img = cv2.imread('GreenScreen.jpg',cv2.COLOR_BGR2RGB)

# The color is taken from a point inside the image
col = tuple(img[1000,1550]) # Or can be given expliccitly : col = (28,241,64)


# Save jpg output image iwth openCV
mask = selectColor(img, (28,241,64), 60)
mask = np.expand_dims(mask, axis=2)
mask = np.concatenate([mask, mask, mask], axis=2)
imo = mask*img
cv2.imwrite('test.jpg',imo)

# Save result image with transparent background using Pillow
mask = 255*selectColor(img, (28,241,64), 60)
mask = np.expand_dims(mask, axis=2)
imo = np.concatenate((img,mask),axis = 2)
imo = Image.fromarray(imo, 'RGBA') 
imo.save('test.png')