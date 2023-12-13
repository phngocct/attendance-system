from util import *
import pandas as pd

face_detection_model = "hog"
# face_detection_model = "cnn"

result_folder = "evaluation"
excel_file_path = "Info.xlsx"

ref = connect_database()
# Đọc dữ liệu từ tệp Excel và lưu vào DataFrame
data_frame = pd.read_excel(excel_file_path)
# Truy cập các cột dữ liệu trong DataFrame và lưu vào danh sách
student_ids = data_frame["Student ID"].tolist()
names = data_frame["Name"].tolist()
majors = data_frame["Major"].tolist()

image_folder_path = "data"
image_filenames = []
for filename in os.listdir(image_folder_path):
    # Kiểm tra nếu là tệp hình ảnh
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_filenames.append(filename)  # Thêm tên tệp vào danh sách
# print(image_filenames)

student_id_list = []
name_list = []
major_list = []
time_list = []

for i in range(len(student_ids)):
    stdID = student_ids[i]
    name = names[i]
    major = majors[i]
    image_path = os.path.join(image_folder_path, "{}".format(image_filenames[i]))
    time_completed = add_data_to_database(
        student_id=stdID,
        name=name,
        major=major,
        image_path_100=image_path,
        ref=ref,
    )
    student_id_list.append(stdID)
    name_list.append(name)
    major_list.append(major)
    time_list.append(time_completed)
    print("-----------------------------------------------------------------------")
    print("Student ID: ", stdID)
    print("Name: ", name)
    print("Major: ", major)
    print("Image_path: ", image_path)
    print("-----------------------------------------------------------------------")

print("Finished adding data to the database!")

if not os.path.exists(result_folder):
    os.makedirs(result_folder)
# Tạo DataFrame từ các danh sách
data = {'Student ID': student_id_list, 'Names': name_list, 'Majors': major_list, 'Time Completed': time_list}
df = pd.DataFrame(data)
# Lưu DataFrame vào file Excel
xlsx_path = f'time_use_{face_detection_model}.xlsx'
xlsx_path_s = os.path.join(result_folder , xlsx_path)
df.to_excel(xlsx_path_s, index=False)
print("-----------------------------------------------------------------------")
print("Evaluation saved successfully!")
