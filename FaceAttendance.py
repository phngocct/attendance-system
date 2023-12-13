import os.path
from datetime import datetime
import time
import tkinter
from tkinter import ttk
import tkinter.messagebox
from tkinter import filedialog

import customtkinter
import cv2
from PIL import Image, ImageTk, ImageDraw

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
        self.frame_visible = False
        self.ref = connect_database()
        filename = "EncodeFile_hog.pkl"
        self.stdList, self.encodefaceList = load_encode_file(filename)

        # configure window
        self.title("Face Attendance System")
        self.iconbitmap("assets/ico/facial-recognition.ico")
        self.geometry(f"{1400}x{720}+{50}+{40}")

        # configure grid layout 1x3
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        self.toplevel_window = None

        # load images with light and dark mode image
        image_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "assets/images"
        )
        self.webcam_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "webcam.png")),
            dark_image=Image.open(os.path.join(image_path, "webcam.png")),
            size=(25, 25),
        )
        self.history_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "history.png")),
            dark_image=Image.open(os.path.join(image_path, "history.png")),
            size=(25, 25),
        )

        self.not_found = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "notfound.png")),
            dark_image=Image.open(os.path.join(image_path, "notfound.png")),
            size=(380, 300),
        )
        self.no_student = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "nostudent.png")),
            dark_image=Image.open(os.path.join(image_path, "nostudent.png")),
            size=(380, 300),
        )

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(
            self.navigation_frame,
            text="Face Attendance",
            font=customtkinter.CTkFont(size=25, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, columnspan=2, padx=20, pady=30)

        self.attendance_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=50,
            border_spacing=20,
            text="Attendances",
            font=customtkinter.CTkFont(size=18, weight="bold", slant="italic"),
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.webcam_image,
            anchor="w",
            command=self.attendance_button_event,
        )
        self.attendance_button.grid(row=1, column=0, columnspan=2, sticky="ew")

        self.history_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=50,
            border_spacing=20,
            text="History",
            font=customtkinter.CTkFont(size=18, weight="bold", slant="italic"),
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.history_image,
            anchor="w",
            command=self.history_button_event,
        )
        self.history_button.grid(row=2, column=0, columnspan=2, sticky="ew")

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

        # ================================== Create attendance frame with widgets ==================================
        self.attendance_frame = customtkinter.CTkFrame(
            self, fg_color="transparent", corner_radius=0
        )

        # create webcam frame
        self.webcam_frame = customtkinter.CTkFrame(self.attendance_frame)
        self.webcam_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.webcam_label = customtkinter.CTkLabel(
            self.webcam_frame,
            text="",
        )
        self.webcam_label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.add_webcam(self.webcam_label)

        self.btn_register = customtkinter.CTkButton(
            master=self.webcam_frame, text="Verify", height=40, command=self.verify
        )
        self.btn_register.grid(row=1, column=0, pady=50)

        # create result frame
        self.result_frame = customtkinter.CTkFrame(self.attendance_frame)
        self.result_frame.grid(row=0, column=1, pady=20, sticky="nsew")
        self.result_frame.grid_rowconfigure(0, weight=1)
        self.result_frame.grid_rowconfigure(1, weight=0)
        self.result_frame.grid_columnconfigure(0, weight=1)

        # Show result image
        self.result_image = customtkinter.CTkLabel(self.result_frame, text="")

        # Show info student
        # create form info frame
        self.info_frame = customtkinter.CTkFrame(self.result_frame)
        # create no_std_frame
        self.no_std_frame = customtkinter.CTkFrame(self.result_frame)

        # ================================== Create history frame with widgets ==================================
        self.history_frame = customtkinter.CTkFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
        )
        self.log_frame = customtkinter.CTkFrame(self.history_frame)
        self.log_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.cols, self.value_tuples = self.load_history()
        self.treeScroll = ttk.Scrollbar(self.log_frame)
        self.treeScroll.pack(side="right", fill="y")
        self.treeview = ttk.Treeview(
            self.log_frame,
            show="headings",
            yscrollcommand=self.treeScroll.set,
            columns=self.cols,
            padding=20,
        )
        self.treeScroll.config(command=self.treeview.yview)
        self.treeview.pack(expand=True, fill="both")
        # Thêm dữ liệu vào TreeView
        for col_name in self.cols:
            self.treeview.heading(col_name, text=col_name)

        for value_tuple in self.value_tuples:
            self.treeview.insert("", tkinter.END, values=value_tuple)

        # ============================================ Set default values ============================================
        self.appearance_mode_optionemenu.set("System")
        self.select_frame_by_name("attendance_frame")

    # ======================================== Define functions ========================================

    def add_webcam(self, label):
        if "cap" not in self.__dict__:
            self.cap = cv2.VideoCapture(0)
        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()
        self.imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        self.imgS = cv2.cvtColor(self.imgS, cv2.COLOR_BGR2RGB)

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = customtkinter.CTkImage(
            light_image=self.most_recent_capture_pil,
            dark_image=self.most_recent_capture_pil,
            size=(640, 480),
            # size=(320, 240),
        )
        self._label.configure(image=imgtk)
        self._label.image = imgtk
        self._label.after(10, self.process_webcam)

    def verify(self):
        self.result_image.grid(row=0, column=0, sticky="nsew")

        self.current_frame = self.imgS.copy()
        frame_draw = self.most_recent_capture_arr.copy()
        self.current_frame_draw = cv2.cvtColor(frame_draw, cv2.COLOR_BGR2RGB)

        self.face_locations = get_face_locations(self.current_frame)
        if self.face_locations is not None:
            self.unknown_face_encoding = face_recognition.face_encodings(
                self.current_frame
            )
            print(
                "------------------------------------------------------------------------------------------------"
            )
            print("face_encodings from webcam:\n", self.unknown_face_encoding)

            self.stdId, self.faceDis, self.iou = recognize_result(
                self.unknown_face_encoding,
                self.encodefaceList,
                self.stdList,
            )
            if self.stdId is not None:
                if self.no_std_frame.winfo_exists():
                    self.no_std_frame.grid_remove()
                (
                    self.name_res_from_db,
                    self.major_res_from_db,
                    self.total_attendance_res_from_db,
                    self.last_attendance_time_res_from_db,
                ) = get_data_to_database(self.stdId)
                self.img_res_from_db = get_image_from_db(self.stdId)

                self.info_frame = customtkinter.CTkFrame(self.result_frame)
                self.info_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
                self.info_frame.grid_columnconfigure(0, weight=0)
                self.info_frame.grid_columnconfigure(1, weight=1)
                self.form_info()

            else:
                if self.info_frame.winfo_exists():
                    self.info_frame.grid_remove()

                self.no_std_frame = customtkinter.CTkFrame(self.result_frame)
                self.no_std_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
                self.no_std_frame.grid_columnconfigure(0, weight=1)

                self.no_std_label = customtkinter.CTkLabel(
                    self.no_std_frame,
                    text="",
                )
                self.no_std_label.grid(row=0, column=0, pady=20, sticky="nsew")
                self.no_std_label.configure(image=self.no_student)
                print("Không tìm thấy sinh viên.")

            # draw_bounding_box
            img = draw_bounding_box(
                self.current_frame_draw, self.face_locations, self.stdId, self.iou
            )
            self.current_frame_draw_pil = Image.fromarray(img)
            imgtk = customtkinter.CTkImage(
                light_image=self.current_frame_draw_pil,
                dark_image=self.current_frame_draw_pil,
                size=(380, 300),
            )
            self.result_image.configure(image=imgtk)

        else:
            self.no_std_frame.grid_remove()
            self.info_frame.grid_remove()
            self.result_image.configure(image=self.not_found)

    def form_info(self):
        self.form_label = customtkinter.CTkLabel(
            self.info_frame,
            text="Student Infomation",
            font=customtkinter.CTkFont(size=18, weight="bold"),
        )
        self.form_label.grid(row=0, column=0, columnspan=3)

        self.stdID_label = customtkinter.CTkLabel(self.info_frame, text="Student code:")
        self.stdID_label.grid(row=1, column=0, sticky="w")
        # self.stdID_res = customtkinter.CTkLabel(self.info_frame, text="FP22016")
        self.stdID_res = customtkinter.CTkLabel(self.info_frame, text=self.stdId)
        self.stdID_res.grid(row=1, column=1, columnspan=2, sticky="w")

        self.name_label = customtkinter.CTkLabel(self.info_frame, text="Full name:")
        self.name_label.grid(row=2, column=0, sticky="w")
        # self.name_res = customtkinter.CTkLabel(
        #     self.info_frame, text="Huỳnh Dương Tấn Khanh"
        # )
        self.name_res = customtkinter.CTkLabel(
            self.info_frame, text=self.name_res_from_db
        )
        self.name_res.grid(row=2, column=1, columnspan=2, sticky="w")

        self.major_label = customtkinter.CTkLabel(self.info_frame, text="Major:")
        self.major_label.grid(row=3, column=0, sticky="w")
        # self.major_res = customtkinter.CTkLabel(
        #     self.info_frame, text="Công nghệ Kỹ thuật điều khiển & Tự động hóa"
        # )
        self.major_res = customtkinter.CTkLabel(
            self.info_frame, text=self.major_res_from_db
        )
        self.major_res.grid(row=3, column=1, columnspan=2, sticky="w")

        for widget in self.info_frame.winfo_children():
            widget.grid_configure(padx=20, pady=15)

        self.btn_accept = customtkinter.CTkButton(
            master=self.info_frame,
            text="Accept",
            height=40,
            command=self.accept_attendance,
        )
        self.btn_accept.grid(row=6, column=0, padx=20, pady=30)

    def accept_attendance(self):
        self.info_frame.destroy()
        self.no_std_frame.destroy()

        self.accept_frame = tkinter.Toplevel()
        self.accept_frame.title("Student Infomation")
        self.accept_frame.iconbitmap("assets/ico/facial-recognition.ico")
        self.accept_frame.geometry(f"{1200}x{720}+{370}+{80}")
        # self.accept_frame = customtkinter.CTkFrame(self.new_window)
        # self.accept_frame.grid(row=0, column=0, sticky="nsew")
        self.accept_frame.grid_rowconfigure(0, weight=1)
        self.accept_frame.grid_columnconfigure(0, weight=1)
        self.accept_frame.grid_columnconfigure(1, weight=1)
        # Update database
        update_data_to_database(self.stdId)
        (
            self.name_res_from_db,
            self.major_res_from_db,
            self.total_attendance_res_from_db,
            self.last_attendance_time_res_from_db,
        ) = get_data_to_database(self.stdId)

        # Add data to excel
        now = datetime.now()
        file_path = f"log_{now.strftime('%d-%m-%Y')}.xlsx"
        add_data_to_excel(
            file_path,
            self.last_attendance_time_res_from_db,
            self.stdId,
            self.name_res_from_db,
            self.major_res_from_db,
        )
        # Reload data from excel file
        self.reload_history()

        # create form info frame
        self.info_frame = customtkinter.CTkFrame(self.accept_frame)
        self.info_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.info_frame.grid_columnconfigure(0, weight=0)
        self.info_frame.grid_columnconfigure(1, weight=1)

        self.form_label = customtkinter.CTkLabel(
            self.info_frame,
            text="Student Infomation",
            font=customtkinter.CTkFont(size=18, weight="bold"),
        )
        self.form_label.grid(row=0, column=0, columnspan=3)

        self.stdID_label = customtkinter.CTkLabel(self.info_frame, text="Student code:")
        self.stdID_label.grid(row=1, column=0, sticky="w")
        self.stdID_res = customtkinter.CTkLabel(self.info_frame, text=self.stdId)
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
        self.last_attendance_time_res.grid(row=4, column=1, columnspan=2, sticky="w")

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
        self.image_res = customtkinter.CTkLabel(self.accept_frame, text="")
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

    def load_history(self):
        now = datetime.now()
        file_path = f"log_{now.strftime('%d-%m-%Y')}.xlsx"
        cols, value_tuples = load_excel(file_path)
        return cols, value_tuples

    def reload_history(self):
        # Reload data from excel file
        self.treeview.delete(*self.treeview.get_children())
        self.cols, self.value_tuples = self.load_history()
        for value_tuple in self.value_tuples:
            self.treeview.insert("", tkinter.END, values=value_tuple)

    def attendance_button_event(self):
        self.select_frame_by_name("attendance_frame")

    def history_button_event(self):
        self.select_frame_by_name("history_frame")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.attendance_button.configure(
            fg_color=("gray75", "gray25")
            if name == "attendance_frame"
            else "transparent"
        )
        self.history_button.configure(
            fg_color=("gray75", "gray25") if name == "history_frame" else "transparent"
        )

        # show selected frame
        if name == "attendance_frame":
            self.attendance_frame.grid(row=0, column=1, sticky="nsew")
            self.attendance_frame.grid_rowconfigure(0, weight=1)
            self.attendance_frame.grid_columnconfigure(1, weight=1)

        else:
            self.attendance_frame.grid_forget()
        if name == "history_frame":
            self.history_frame.grid(row=0, column=1, sticky="nsew")
            self.history_frame.grid_rowconfigure(0, weight=1)
            self.history_frame.grid_columnconfigure(0, weight=1)
            cols, value_tuples = self.load_history()

        else:
            self.history_frame.grid_forget()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
