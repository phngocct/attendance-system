from util import *
face_detection_model = "hog"
# face_detection_model = "cnn"

filename = f"EncodeFile_{face_detection_model}.pkl"
stdList, encodefaceList = load_encode_file(filename)