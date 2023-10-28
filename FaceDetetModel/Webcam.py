from ultralytics import YOLO
import ultralytics

model = YOLO("best.pt")

results = model.predict(source="0",show =True)
print(results)
