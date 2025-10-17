from PIL import Image as Img
import numpy as np

# Img.new("RGB", size=(100, 100), color="#66CCFF").show()

# imgData = np.array([[[255, 0, 0]]], dtype=np.uint8)

# pilImg = Img.fromarray(imgData)

# pilImg.show()

# pilImg.convert("RGB").show()

pilImg = Img.open("test.png")

pilImg.transpose(3).show()
