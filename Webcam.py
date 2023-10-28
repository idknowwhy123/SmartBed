#from IPython import display

#import ultralytics

from ultralytics import YOLO
import ultralytics

#from IPython.display import display, Image

#from ultralytics import YOLO
ultralytics.checks()

model = YOLO("best.pt")

results = model.predict(source="0",show =True)
print(results)
