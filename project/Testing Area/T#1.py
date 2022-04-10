import cv2.cv2 as cv
from matplotlib import pyplot as plt
from PIL import Image as PILmage
imge0 = cv.imread(filename='marin.jpg',flags=cv.IMREAD_UNCHANGED)

imge = cv.cvtColor(imge0, cv.COLOR_BGR2RGB)
imge1 = PILmage.fromarray(imge, 'RGB')

imge1.show()

# plt.imshow(imge, interpolation='nearest')
# plt.show()
cv.waitKey(0)