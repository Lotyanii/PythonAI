import numpy as np
from PIL import Image

demo = np.zeros((200, 200, 3), np.uint8)
h, w, c = demo.shape
demo[:, :w // 2] = [255, 0, 0]
demo[:, w // 2:w] = [255, 255, 0]

test = Image.fromarray(demo)
test.show()



