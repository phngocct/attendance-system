import os.path
import datetime
import pickle
import tkinter
from tkinter import ttk
import tkinter.messagebox
from tkinter import filedialog
import threading

import customtkinter
import cv2
from PIL import Image, ImageTk

from util import *

customtkinter.set_appearance_mode(
    "System"
)  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "assets/themes/orange.json"
)  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.image_path = None
        self.webcam_active = False

        self.ref = connect_database()

        # configure window
        self.title("Face Attendance System")
        self.iconbitmap("assets/ico/facial-recognition.ico")
        self.geometry(f"{1280}x{720}+{50}+{40}")

        # configure grid layout 1x3
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        # load images with light and dark mode image
        image_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "assets/images"
        )
        self.webcam_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "webcam.png")),
            dark_image=Image.open(os.path.join(image_path, "webcam.png")),
            size=(25, 25),
        )
        self.add_image_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "add_image.png")),
            dark_image=Image.open(os.path.join(image_path, "add_image.png")),
            size=(25, 25),
        )
        self.management_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "students.png")),
            dark_image=Image.open(os.path.join(image_path, "students.png")),
            size=(25, 25),
        )

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        # self.navigation_frame.grid_columnconfigure(0, weight=1)
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(
            self.navigation_frame,
            text="Face Attendance",
            font=customtkinter.CTkFont(size=25, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, columnspan=2, padx=20, pady=30)

        self.webcam_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=50,
            border_spacing=20,
            text="Webcam",
            font=customtkinter.CTkFont(size=18, weight="bold", slant="italic"),
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.webcam_image,
            anchor="w",
            command=self.webcam_button_event,
        )
        self.webcam_button.grid(row=1, column=0, columnspan=2, sticky="ew")

        self.image_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=50,
            border_spacing=20,
            text="Image",
            font=customtkinter.CTkFont(size=18, weight="bold", slant="italic"),
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.add_image_image,
            anchor="w",
            command=self.image_button_event,
        )
        self.image_button.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.std_management_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=50,
            border_spacing=20,
            text="Students",
            font=customtkinter.CTkFont(size=18, weight="bold", slant="italic"),
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.management_image,
            anchor="w",
            command=self.std_management_button_event,
        )
        self.std_management_button.grid(row=3, column=0, columnspan=2, sticky="ew")

        self.appearance_mode_label = customtkinter.CTkLabel(
            self.navigation_frame, text="Mode:", anchor="w"
        )
        self.appearance_mode_label.grid(row=5, column=0, padx=(30, 0), pady=10)
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.navigation_frame,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_optionemenu.grid(row=5, column=1, padx=20, pady=10)

        # ================================== Create webcam frame with widgets ==================================
        self.webcam_frame = customtkinter.CTkFrame(
            self, fg_color="transparent", corner_radius=0
        )
        # create webcam frame
        self.cam_frame = customtkinter.CTkFrame(self.webcam_frame)
        self.cam_frame.grid(row=0, column=0, pady=20, sticky="nsew")
        self.cam_frame.grid_columnconfigure(0, weight=0)
        self.cam_frame.grid_columnconfigure(1, weight=1)
        self.cam_frame.grid_rowconfigure(0, weight=1)
        # Show webcam
        self.webcam_label = customtkinter.CTkLabel(
            self.cam_frame,
            text="",
        )
        self.webcam_label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        # Button Register
        self.btn_register = customtkinter.CTkButton(
            master=self.cam_frame, text="Register", height=40, command=self.register_w
        )
        self.btn_register.grid(row=0, column=1, padx=20, pady=20)

        # ================================== Create image frame with widgets ==================================
        self.image_frame = customtkinter.CTkFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
        )
        # create form register frame
        self.register_frame = customtkinter.CTkFrame(self.image_frame)
        self.register_frame.grid(row=0, column=0, pady=20, sticky="n")
        self.form_register()

        # =============================== Create student management frame with widgets ===============================
        self.std_management_frame = customtkinter.CTkFrame(
            self, fg_color="transparent", corner_radius=0
        )
        self.std_frame = customtkinter.CTkFrame(self.std_management_frame)
        self.std_frame.grid(row=0, column=0, pady=20, sticky="nsew")
        self.std_frame.grid_columnconfigure(0, weight=1)
        # self.std_frame.grid_rowconfigure(0, weight=1)
        self.std_frame.grid_rowconfigure(1, weight=1)
        self.btn_detail_std = customtkinter.CTkButton(
            master=self.std_frame,
            text="Detail",
            command=self.detail_std,
            fg_color=("#415C7B", "#415C7B"),
            hover_color=("#4F709C", "#4F709C"),
        )
        self.btn_detail_std.grid(row=0, column=0, padx=200, pady=20, sticky="e")

        self.btn_delete_std = customtkinter.CTkButton(
            master=self.std_frame,
            text="Delete",
            command=self.delete_std,
            fg_color=("#D21312", "#D21312"),
            hover_color=("#F24C3D", "#F24C3D"),
        )
        self.btn_delete_std.grid(row=0, column=0, padx=20, pady=20, sticky="e")
        # Load list data from database
        (
            self.std_ids,
            self.names,
            self.majors,
            self.total_attendances,
            self.last_attendance_times,
        ) = self.load_management()
        self.cols = (
            "STT",
            "Student ID",
            "Full Name",
            "Major",
            "Total Attendance",
            "Last Attendance Time",
        )
        self.treeScroll = ttk.Scrollbar(self.std_frame)
        self.treeScroll.grid(row=1, column=1, sticky="ns")
        self.treeview = ttk.Treeview(
            self.std_frame,
            show="headings",
            yscrollcommand=self.treeScroll.set,
            columns=self.cols,
            padding=20,
        )
        self.treeScroll.config(command=self.treeview.yview)
        self.treeview.grid(row=1, column=0, sticky="nsew")
        column_widths = [20, 50, 150, 220, 50, 150, 100]
        for col, width in zip(self.treeview["columns"], column_widths):
            self.treeview.column(col, width=width)
        for col_name in self.cols:
            self.treeview.heading(col_name, text=col_name)

        for index, (
            std_id,
            name,
            major,
            total_attendance,
            last_attendance_time,
        ) in enumerate(
            zip(
                self.std_ids,
                self.names,
                self.majors,
                self.total_attendances,
                self.last_attendance_times,
            ),
            start=1,
        ):
            self.treeview.insert(
                "",
                tkinter.END,
                text=str(index),
                values=(
                    str(index),
                    std_id,
                    name,
                    major,
                    total_attendance,
                    last_attendance_time,
                ),
            )

        # ============================================ Set default values ============================================
        self.appearance_mode_optionemenu.set("System")
        # self.select_frame_by_name("webcam_frame")
        # self.select_frame_by_name("upload_img_frame")
        self.select_frame_by_name("std_management_frame")

    # ======================================== Define functions ========================================
    def destroy_webcam(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self.webcam_active = False

    def add_webcam(self, label):
        self.webcam_active = True
        # if "cap" not in self.__dict__:

        self.cap = cv2.VideoCapture(0)
        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()
        # Lấy chiều rộng và chiều cao của ảnh
        # height, width, _ = frame.shape
        # Tính toán kích thước mới sau khi cắt 2 bên
        # new_width = width - 2 * 185
        # Cắt 2 bên của ảnh
        # cropped_image = frame[:, 185:new_width+185]

        self.imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        self.imgS = cv2.cvtColor(self.imgS, cv2.COLOR_BGR2RGB)

        self.most_recent_capture_arr = frame

        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = customtkinter.CTkImage(
            light_image=self.most_recent_capture_pil,
            dark_image=self.most_recent_capture_pil,
            # size=(480, 854),
            size=(640, 480),
            # size=(480, 640),
            # size=(240, 320),
            # size=(320, 240),
        )
        self._label.configure(image=imgtk)
        self._label.image = imgtk
        self._label.after(10, self.process_webcam)

    def form_register(self):
        self.register_label = customtkinter.CTkLabel(
            self.register_frame,
            text="Student Infomation",
            font=customtkinter.CTkFont(size=18, weight="bold"),
        )
        self.register_label.grid(row=0, column=0, columnspan=3)

        self.stdID_label = customtkinter.CTkLabel(
            self.register_frame, text="Student code:"
        )
        self.stdID_label.grid(row=1, column=0, sticky="e")
        self.stdID_entry = customtkinter.CTkEntry(
            self.register_frame, placeholder_text="Enter student code"
        )
        self.stdID_entry.grid(row=1, column=1, columnspan=2, sticky="nsew")

        self.name_label = customtkinter.CTkLabel(self.register_frame, text="Full name:")
        self.name_label.grid(row=2, column=0, sticky="e")
        self.name_entry = customtkinter.CTkEntry(
            self.register_frame, placeholder_text="Enter student's name"
        )
        self.name_entry.grid(row=2, column=1, columnspan=2, sticky="nsew")

        self.major_label = customtkinter.CTkLabel(self.register_frame, text="Major:")
        self.major_label.grid(row=3, column=0, sticky="e")
        majorList = [
            "Phát triển phần mềm",
            "Lập trình Web",
            "Lập trình Mobile",
            "Lập trình Game",
            "Ứng dụng phần mềm",
            "Xử lý dữ liệu",
            "Quản trị kinh doanh",
            "Công nghệ Kỹ thuật điều khiển & Tự động hóa",
            "Thiết kế đồ họa",
            "Hướng dẫn du lịch",
            "Công nghệ kỹ thuật cơ khí",
            "Chăm sóc Sức khỏe và Làm đẹp",
            "Tiếng Anh - Top Notch",
        ]
        self.major_combobox = customtkinter.CTkComboBox(
            self.register_frame, values=majorList
        )
        self.major_combobox.grid(row=3, column=1, columnspan=2, sticky="nsew")

        self.image_label = customtkinter.CTkLabel(self.register_frame, text="Image:")
        self.image_label.grid(row=4, column=0, sticky="e")

        self.btn_choose_image = customtkinter.CTkButton(
            self.register_frame,
            text="Choose image",
            anchor="w",
            fg_color=("#F9F9FA", "#343638"),
            border_color=("#979DA2", "#565B5E"),
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=self.choose_image,
        )
        self.btn_choose_image.grid(row=4, column=1, columnspan=2, sticky="nsew")

        # Show uploaded image
        self.selected_image = customtkinter.CTkLabel(self.image_frame, text="")
        self.selected_image.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        for widget in self.register_frame.winfo_children():
            widget.grid_configure(padx=20, pady=15)

        # Button Clear
        self.btn_cancel = customtkinter.CTkButton(
            self.register_frame,
            text="Clear",
            fg_color=("#545B77", "#374259"),
            hover_color=("#9BABB8", "#526D82"),
            command=self.clear_form,
        )
        self.btn_cancel.grid(row=6, column=1, padx=20, pady=(30, 20), sticky="w")
        # Button submit
        self.btn_submit = customtkinter.CTkButton(
            self.register_frame,
            text="Submit",
            command=self.submit_form,
        )
        self.btn_submit.grid(row=6, column=2, padx=20, pady=(30, 20), sticky="e")

    def register_w(self):
        self.webcam_register_frame = tkinter.Toplevel()
        self.webcam_register_frame.title("Register Student")
        self.webcam_register_frame.iconbitmap("assets/ico/facial-recognition.ico")
        self.webcam_register_frame.geometry(f"{1280}x{720}+{370}+{80}")
        self.webcam_register_frame.grid_rowconfigure(0, weight=1)
        self.webcam_register_frame.grid_columnconfigure(0, weight=1)
        self.webcam_register_frame.grid_columnconfigure(1, weight=1)

        # create image from webcam frame
        self.image_from_cam_frame = customtkinter.CTkFrame(self.webcam_register_frame)
        self.image_from_cam_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.image_from_cam_frame.grid_rowconfigure(0, weight=1)
        self.image_from_cam_frame.grid_rowconfigure(1, weight=1)
        self.image_from_cam_frame.grid_columnconfigure(0, weight=1)
        # Image from webcam
        self.image_register_label = customtkinter.CTkLabel(
            self.image_from_cam_frame,
            text="",
        )
        self.image_register_label.grid(row=0, column=0, pady=20, sticky="nsew")
        image_arr = self.most_recent_capture_arr.copy()
        # Kích thước mới
        width = image_arr.shape[1] * 2
        height = image_arr.shape[0] * 2
        # Tăng kích thước ảnh
        self.image_arr = cv2.resize(image_arr, (width, height))

        self.current_frame_pil = self.most_recent_capture_pil.copy()
        imgtk = customtkinter.CTkImage(
            light_image=self.current_frame_pil,
            dark_image=self.current_frame_pil,
            # size=(640, 480),
            size=(320, 240),
            # size=(240, 320),
            # size=(380, 300),
        )
        self.image_register_label.configure(image=imgtk)
        # Button Try again
        self.btn_w_try_again = customtkinter.CTkButton(
            self.image_from_cam_frame,
            text="Try again",
            height=40,
            fg_color=("#545B77", "#374259"),
            hover_color=("#9BABB8", "#526D82"),
            command=self.try_again_register,
        )
        self.btn_w_try_again.grid(row=1, column=0, padx=20, pady=(20, 40))

        # create form register frame
        self.register_w_frame = customtkinter.CTkFrame(self.webcam_register_frame)
        self.register_w_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        # self.register_w_frame.grid_rowconfigure(0, weight=1)
        self.form_register_w()

    def form_register_w(self):
        self.register_w_label = customtkinter.CTkLabel(
            self.register_w_frame,
            text="Student Infomation",
            font=customtkinter.CTkFont(size=18, weight="bold"),
        )
        self.register_w_label.grid(row=0, column=0, columnspan=3)

        self.stdID_w_label = customtkinter.CTkLabel(
            self.register_w_frame, text="Student code:"
        )
        self.stdID_w_label.grid(row=1, column=0, sticky="e")
        self.stdID_w_entry = customtkinter.CTkEntry(
            self.register_w_frame, placeholder_text="Enter student code"
        )
        self.stdID_w_entry.grid(row=1, column=1, columnspan=2, sticky="nsew")

        self.name_w_label = customtkinter.CTkLabel(
            self.register_w_frame, text="Full name:"
        )
        self.name_w_label.grid(row=2, column=0, sticky="e")
        self.name_w_entry = customtkinter.CTkEntry(
            self.register_w_frame, placeholder_text="Enter student's name"
        )
        self.name_w_entry.grid(row=2, column=1, columnspan=2, sticky="nsew")

        self.major_w_label = customtkinter.CTkLabel(
            self.register_w_frame, text="Major:"
        )
        self.major_w_label.grid(row=3, column=0, sticky="e")
        majorList = [
            "Phát triển phần mềm",
            "Lập trình Web",
            "Lập trình Mobile",
            "Lập trình Game",
            "Ứng dụng phần mềm",
            "Xử lý dữ liệu",
            "Quản trị kinh doanh",
            "Công nghệ Kỹ thuật điều khiển & Tự động hóa",
            "Thiết kế đồ họa",
            "Hướng dẫn du lịch",
            "Công nghệ kỹ thuật cơ khí",
            "Chăm sóc Sức khỏe và Làm đẹp",
            "Tiếng Anh - Top Notch",
        ]
        self.major_w_combobox = customtkinter.CTkComboBox(
            self.register_w_frame, values=majorList
        )
        self.major_w_combobox.grid(row=3, column=1, columnspan=2, sticky="nsew")

        for widget in self.register_w_frame.winfo_children():
            widget.grid_configure(padx=20, pady=15)

        # Button Clear
        self.btn_w_cancel = customtkinter.CTkButton(
            self.register_w_frame,
            text="Clear",
            fg_color=("#545B77", "#374259"),
            hover_color=("#9BABB8", "#526D82"),
            command=self.clear_form_w,
        )
        self.btn_w_cancel.grid(row=5, column=1, padx=20, pady=(30, 20), sticky="w")

        # Button submit
        self.btn_w_submit = customtkinter.CTkButton(
            self.register_w_frame,
            text="Submit",
            command=self.submit_form_w,
        )
        self.btn_w_submit.grid(row=5, column=2, padx=20, pady=(30, 20), sticky="e")

    def choose_image(self):
        self.image_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png")]
        )
        if self.image_path:
            print("Đã chọn tệp tin:", self.image_path)
            image = Image.open(self.image_path)
            resized_image = resize_image(image, 600, 1000)
            width = resized_image.size[0]
            height = resized_image.size[1]
            ctk_image = customtkinter.CTkImage(
                light_image=resized_image,
                dark_image=resized_image,
                size=(width, height),
            )
            self.selected_image.configure(image=ctk_image)
            self.selected_image.image = ctk_image
            self.btn_choose_image.configure(text=self.image_path)

    def try_again_register(self):
        self.webcam_register_frame.destroy()

    def clear_form(self):
        self.stdID_entry.delete(0, "end")
        self.name_entry.delete(0, "end")
        self.btn_choose_image.configure(text="Choose image", anchor="w")
        self.selected_image.configure(image="")

    def clear_form_w(self):
        self.stdID_w_entry.delete(0, "end")
        self.name_w_entry.delete(0, "end")

    def submit_form(self):
        stdID = self.stdID_entry.get()
        name = self.name_entry.get()
        if stdID and name:
            major = self.major_combobox.get()
            image_path = self.image_path
            if image_path:
                print(
                    "------------------------------------------------------------------------------------------------"
                )
                print("Student id: ", stdID)
                print("Full name: ", name)
                print("Major: ", major)
                print("Image_path: ", image_path)
                print(
                    "------------------------------------------------------------------------------------------------"
                )
                # Add data to database
                add_data_to_database(
                    student_id=stdID,
                    name=name,
                    major=major,
                    image_path_100=image_path,
                    ref=self.ref,
                )
                self.reload_management()
                # Clear form
                self.clear_form()

            else:
                tkinter.messagebox.showwarning("Error", "Image is required.")
        else:
            tkinter.messagebox.showwarning(
                "Error", "Student code and name are required."
            )

    def submit_form_w(self):
        stdID = self.stdID_w_entry.get()
        name = self.name_w_entry.get()
        if stdID and name:
            major = self.major_w_combobox.get()
            output_folder = "temp_webcam"
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            cv2.imwrite(f"temp_webcam/{stdID}.png", self.image_arr)

            image_path = f"temp_webcam/{stdID}.png"
            print(
                "------------------------------------------------------------------------------------------------"
            )
            print("Student id: ", stdID)
            print("Full name: ", name)
            print("Major: ", major)
            print("image_path: ", image_path)
            print(
                "------------------------------------------------------------------------------------------------"
            )
            # Add data to database

            add_data_to_database(
                student_id=stdID,
                name=name,
                major=major,
                image_path_100=image_path,
                ref=self.ref,
            )
            self.reload_management()
            self.webcam_register_frame.destroy()

        else:
            tkinter.messagebox.showwarning(
                "Error", "Student code and name are required."
            )

    def detail_std(self):
        selected_item = self.treeview.focus()
        if selected_item:
            item_values = self.treeview.item(selected_item)["values"]
            std_id = item_values[1]
            print("item_values", item_values)
            print("std_id: ", std_id)
            self.detail_frame = tkinter.Toplevel()
            self.detail_frame.title("Detail Student")
            self.detail_frame.iconbitmap("assets/ico/facial-recognition.ico")
            self.detail_frame.geometry(f"{1280}x{720}+{370}+{80}")
            self.detail_frame.grid_rowconfigure(0, weight=1)
            self.detail_frame.grid_columnconfigure(0, weight=0)
            self.detail_frame.grid_columnconfigure(1, weight=1)
            # get data to database
            (
                self.name_res_from_db,
                self.major_res_from_db,
                self.total_attendance_res_from_db,
                self.last_attendance_time_res_from_db,
            ) = get_data_to_database(std_id)
            self.img_res_from_db = get_image_from_db(std_id)

            # create form info frame
            self.info_frame = customtkinter.CTkFrame(self.detail_frame)
            self.info_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
            self.info_frame.grid_columnconfigure(0, weight=0)
            self.info_frame.grid_columnconfigure(1, weight=1)
            self.form_label = customtkinter.CTkLabel(
                self.info_frame,
                text="Student Infomation",
                font=customtkinter.CTkFont(size=18, weight="bold"),
            )
            self.form_label.grid(row=0, column=0, columnspan=3)
            self.stdID_label = customtkinter.CTkLabel(
                self.info_frame, text="Student code:"
            )
            self.stdID_label.grid(row=1, column=0, sticky="w")
            self.stdID_res = customtkinter.CTkLabel(self.info_frame, text=std_id)
            self.stdID_res.grid(row=1, column=1, columnspan=2, sticky="w")

            self.name_label = customtkinter.CTkLabel(self.info_frame, text="Full name:")
            self.name_label.grid(row=2, column=0, sticky="w")
            self.name_res = customtkinter.CTkLabel(
                self.info_frame, text=self.name_res_from_db
            )
            self.name_res.grid(row=2, column=1, columnspan=2, sticky="w")

            self.major_label = customtkinter.CTkLabel(self.info_frame, text="Major:")
            self.major_label.grid(row=3, column=0, sticky="w")
            self.major_res = customtkinter.CTkLabel(
                self.info_frame, text=self.major_res_from_db
            )
            self.major_res.grid(row=3, column=1, columnspan=2, sticky="w")

            self.last_attendance_time_label = customtkinter.CTkLabel(
                self.info_frame, text="Attendance time:"
            )
            self.last_attendance_time_label.grid(row=4, column=0, sticky="w")
            self.last_attendance_time_res = customtkinter.CTkLabel(
                self.info_frame, text=self.last_attendance_time_res_from_db
            )
            self.last_attendance_time_res.grid(
                row=4, column=1, columnspan=2, sticky="w"
            )

            self.total_attendance_label = customtkinter.CTkLabel(
                self.info_frame, text="Total attendance:"
            )
            self.total_attendance_label.grid(row=5, column=0, sticky="w")
            self.total_attendance_res = customtkinter.CTkLabel(
                self.info_frame, text=self.total_attendance_res_from_db
            )
            self.total_attendance_res.grid(row=5, column=1, columnspan=2, sticky="w")

            for widget in self.info_frame.winfo_children():
                widget.grid_configure(padx=20, pady=15)

            # Show image from db
            self.image_res = customtkinter.CTkLabel(self.detail_frame, text="")
            self.image_res.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
            resized_image = resize_image(self.img_res_from_db, 600, 1000)
            width = resized_image.size[0]
            height = resized_image.size[1]
            img = customtkinter.CTkImage(
                light_image=resized_image,
                dark_image=resized_image,
                size=(width, height),
            )
            self.image_res.configure(image=img)

    def delete_std(self):
        selected_item = self.treeview.focus()
        if selected_item:
            item_values = self.treeview.item(selected_item)["values"]
            std_id = item_values[1]
            print("item_values", item_values)
            print("std_id: ", std_id)
            delete_data_from_firebase(std_id)
            filename = "EncodeFile_hog.pkl"
            delete_std_from_encode(std_id, filename)

            # Xóa hàng trong TreeView
            self.treeview.delete(selected_item)
            self.update_stt_column()
            print("Deleted")

    def load_management(self):
        (
            std_ids,
            names,
            majors,
            total_attendances,
            last_attendance_times,
        ) = load_data_from_firebase()

        return std_ids, names, majors, total_attendances, last_attendance_times

    def reload_management(self):
        self.treeview.delete(*self.treeview.get_children())
        (
            self.std_ids,
            self.names,
            self.majors,
            self.total_attendances,
            self.last_attendance_times,
        ) = self.load_management()
        for index, (
            std_id,
            name,
            major,
            total_attendance,
            last_attendance_time,
        ) in enumerate(
            zip(
                self.std_ids,
                self.names,
                self.majors,
                self.total_attendances,
                self.last_attendance_times,
            ),
            start=1,
        ):
            self.treeview.insert(
                "",
                tkinter.END,
                text=str(index),
                values=(
                    str(index),
                    std_id,
                    name,
                    major,
                    total_attendance,
                    last_attendance_time,
                ),
            )

    def update_stt_column(self):
        items = self.treeview.get_children()
        for index, item in enumerate(items, start=1):
            self.treeview.set(item, "#1", str(index))

    def webcam_button_event(self):
        if not self.webcam_active:
            self.add_webcam(self.webcam_label)

        self.select_frame_by_name("webcam_frame")

    def image_button_event(self):
        if self.webcam_active:
            self.destroy_webcam()
        self.select_frame_by_name("upload_img_frame")

    def std_management_button_event(self):
        if self.webcam_active:
            self.destroy_webcam()
        self.select_frame_by_name("std_management_frame")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.webcam_button.configure(
            fg_color=("gray75", "gray25") if name == "webcam_frame" else "transparent"
        )
        self.image_button.configure(
            fg_color=("gray75", "gray25")
            if name == "upload_img_frame"
            else "transparent"
        )
        self.std_management_button.configure(
            fg_color=("gray75", "gray25")
            if name == "std_management_frame"
            else "transparent"
        )

        # show selected frame
        if name == "webcam_frame":
            self.webcam_frame.grid(row=0, column=1, padx=20, sticky="nsew")
            self.webcam_frame.grid_rowconfigure(0, weight=1)
            self.webcam_frame.grid_columnconfigure(0, weight=1)
        else:
            self.webcam_frame.grid_forget()
        if name == "upload_img_frame":
            self.image_frame.grid(row=0, column=1, padx=20, sticky="nsew")
        else:
            self.image_frame.grid_forget()

        if name == "std_management_frame":
            self.std_management_frame.grid(row=0, column=1, padx=20, sticky="nsew")
            self.std_management_frame.grid(row=0, column=1, padx=20, sticky="nsew")
            self.std_management_frame.grid_columnconfigure(0, weight=1)
            self.std_management_frame.grid_rowconfigure(0, weight=1)

        else:
            self.std_management_frame.grid_forget()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
