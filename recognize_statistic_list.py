from util import *
import pandas as pd
from datetime import datetime

face_detection_model = "hog"
# face_detection_model = "cnn"

image_path = "TranQuocThinh-22.png"
result_folder = f'result_face_to_check_{face_detection_model}'
xlsxs_path = f'result_threshold_{face_detection_model}.xlsx'

# image_path = "unknown.png"
# result_folder = f'result_face_to_check_{face_detection_model}_unknown'
# xlsxs_path = f'result_threshold_{face_detection_model}_unknown.xlsx'

threshold_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
result_threshold_folder = "result_threshold"

filename = f"EncodeFile_{face_detection_model}.pkl"
studentIds, known_face_encoding  = load_encode_file(filename)
known_face_encoding = np.array(known_face_encoding)
known_face_encoding = np.squeeze(known_face_encoding)

image_resize_path = resize_25(image_path)

image_array = face_recognition.load_image_file(image_resize_path)
face_locations = face_recognition.face_locations(image_array, model=face_detection_model)
face_encoding_to_check = face_recognition.face_encodings(image_array,face_locations)[0]
print('face_encoding_to_check \n',face_encoding_to_check)

if not os.path.exists(result_folder):
    os.makedirs(result_folder)

list_matches = []
# recognize_result(face_encoding_to_check, known_face_encoding, studentIds, tolerance=0.4):
for i in range(len(threshold_list)):
    threshold = threshold_list[i]
    start = datetime.now()
    print('---------------------------------- start -------------------------------------------')
    print("threshold: ", threshold)

    matches = face_recognition.compare_faces(
        known_face_encoding, face_encoding_to_check, tolerance=threshold
    )
    faceDis = face_recognition.face_distance(
        known_face_encoding, face_encoding_to_check
    )
    match = any(matches)  # True/False
    count = matches.count(True)
    matchIndex = np.argmin(faceDis)     
    distance = faceDis[matchIndex]
    distance = round(distance, 5)

    duration = datetime.now() - start
    time_completed = str(duration)

    ious = []
    for i in faceDis:
        iou_score = (1 / (1 + i))*100
        iou_score = round(iou_score, 5)
        ious.append(iou_score)

    # print("----------------------------------------------------------------------")
    # print("Matches: \n", matches)
    # print("Match: ", match)
    # print('Count True: ', count)
    # print("Face distance: \n", faceDis)
    # print("Min match Index: ", matchIndex)
    # print("Face distance[ minmatchIndex] ", distance)
    # print("----------------------------------------------------------------------")
    if match & (distance <= threshold):
        stdId = studentIds[matchIndex]
        iou_score = (1 / (1 + distance))* 100
        iou_score = round(iou_score, 5)
        print("Student ID: ", stdId)
        print ('Distance: ', distance)
        print ('Iou score: ', iou_score)
    else:
        stdId = None
        iou_score = None
        print("Student ID: ", stdId)
        print ('Không tìm thấy khuôn mặt khớp')

    data_eval = 'Students List: ' + str(studentIds) \
                + '\n' + 'Matches: ' + str(matches) \
                + '\n' + 'Face distance: \n' + str(faceDis) \
                + '\n' + 'IOU: \n' + str(ious) \
                + '\n' + 'Match: ' + str(match) \
                + '\n' + 'Count True: ' + str(count) \
                + '\n' + 'Min match Index: ' + str(matchIndex) \
                + '\n' + 'Face distance[ minmatchIndex]: ' + str(distance) \
                + '\n' + 'Student ID: ' + str(stdId) \
                + '\n' + 'Iou_score: ' + str(iou_score) \
                + '\n' + 'TIME COMPLETED: ' + time_completed

    print(data_eval)

    eval_path = f'evaluate_{face_detection_model}_{threshold}.txt'
    path_s = os.path.join(result_folder , eval_path)
    with open(path_s, mode='w') as f:
        f.writelines(data_eval)
    f.close()

    # Tạo DataFrame từ các danh sách
    data = {'Student ID': studentIds, 'Matches': matches, 'Face distance': faceDis, 'IOU': ious}
    df = pd.DataFrame(data)
    # Lưu DataFrame vào file Excel
    xlsx_path = f'evaluate_{face_detection_model}_{threshold}.xlsx'
    xlsx_path_s = os.path.join(result_folder , xlsx_path)
    df.to_excel(xlsx_path_s, index=False)
    list_matches.append(matches)

# list_1 = []
# list_2 = []
# list_3 = []
# list_4 = []
# list_5 = []
# list_6 = []
# list_7 = []
# list_8 = []
# list_9 = []
list_1, list_2, list_3, list_4, list_5, list_6, list_7, list_8, list_9 = list_matches
# Tạo DataFrame từ các danh sách
data = {'Student ID': studentIds, '0.1': list_1, '0.2': list_2, '0.3': list_3, '0.4': list_4, '0.5': list_5, '0.6': list_6, '0.7': list_7, '0.8': list_8, '0.9': list_9, 'Face distance': faceDis,'IOU': ious }
df = pd.DataFrame(data)
# Lưu DataFrame vào file Excel
if not os.path.exists(result_threshold_folder):
    os.makedirs(result_threshold_folder)
xlsxs_path_s = os.path.join(result_threshold_folder , xlsxs_path)
df.to_excel(xlsxs_path_s, index=False)
print("-----------------------------------------------------------------------")
print("Evaluation saved successfully!")