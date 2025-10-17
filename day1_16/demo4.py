import numpy as np
from PIL import Image

img = Image.open('test.png')

# img.show()

# print(img.mode)
# print(img.size)

imgData = np.array(img)
print(imgData.shape)

