import cv2 as cv
from qreader import QReader
import pandas as pd
import tkinter as tk
from PIL import Image, ImageTk
import winsound

class Camera:

    def __init__(self, cameraInstance):
        self.cameraInstance = cameraInstance

    def frame(self):
        running, frame = self.cameraInstance.read()
        return frame
    
    def running(self):
        running, frame = self.cameraInstance.read()
        return running
    
    def release(self):
        self.cameraInstance.release()

def startEvent():
    global frame, frame_preview
    print("Started")
    # OpenCV running
    while qrCamera.running():
        frame = cv.cvtColor(qrCamera.frame(),cv.COLOR_BGR2RGB)
        # frame = cv.resize(frame, (left_frame_width, left_frame_height))
        frame = frame[0:480, 80:560]
        frame_preview = ImageTk.PhotoImage(Image.fromarray(frame))
        camera_preview.configure(image=frame_preview)
        camera_preview.image=frame_preview
        camera_preview.update()

def scanButton():
    global qrData
    try:
        qrScanned = qrScanner.detect_and_decode(frame, return_detections=True)
        if qrScanned[0] != None:
            qrData = qrScanned[0][0]
            x1, y1, x2, y2 = qrScanned[1][0]['bbox_xyxy']
            for i in range(len(col_qrData)):
                if col_qrData[i] == qrData:
                    winsound.Beep(2740, 220)
                    print(course_text_.format(qrData))
                    x1 = int(x1) - coded_qr_padding
                    y1 = int(y1) - coded_qr_padding
                    x2 = int(x2) + coded_qr_padding
                    y2 = int(y2) + coded_qr_padding
                    cropped_qr = frame[y1:y2, x1:x2]
                    cropped_qr = cv.resize(cropped_qr, (int(window_width*0.186), int(window_width*0.186)))
                    cv.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 10)
                    frame_preview = ImageTk.PhotoImage(Image.fromarray(frame))
                    camera_preview.configure(image=frame_preview)
                    camera_preview.image=frame_preview
                    camera_preview.update()

                    
                    name_text_view.configure(text=name_text_.format(col_lastName[i],
                                                                    col_firstName[i],
                                                                    col_middleName[i]),
                                             bg="#C93535",
                                             fg="#ffffff")
                    name_text_view.update()

                    year_text_view.configure(text=year_text_.format(col_year[i]),
                                            bg="#C93535",
                                            fg="#ffffff")
                    year_text_view.update()

                    course_text_view.configure(text=course_text_.format(col_course[i]),
                                               bg="#C93535",
                                               fg="#ffffff")
                    course_text_view.update()
                    
                    ticket_valid_label.configure(text="TICKET VALID",
                                              fg="#000000",
                                              bg="#39ff53")
                    ticket_valid_label.update()

                    cropped_qr = ImageTk.PhotoImage(Image.fromarray(cropped_qr))
                    captured_qr_view.configure(image=cropped_qr)
                    captured_qr_view.update()

                    cv.waitKey(1500)
                    break
                elif i == len(col_qrData)-1:
                    winsound.Beep(320, 250)
                    name_text_view.configure(text="INVALID",
                                             fg="#ff1414",
                                             bg="#000000")
                    name_text_view.update()

                    year_text_view.configure(text="INVALID",
                                             fg="#ff1414",
                                             bg="#000000")
                    year_text_view.update()

                    course_text_view.configure(text="INVALID",
                                               fg="#ff1414",
                                               bg="#000000")
                    course_text_view.update()

                    ticket_valid_label.configure(text="TICKET INVALID",
                                               fg="#000000",
                                               bg="#ff1414")
                    ticket_valid_label.update()
    except:
        winsound.Beep(320, 250)
        name_text_view.configure(text="INVALID",
                                 fg="#ff1414",
                                 bg="#000000")
        name_text_view.update()

        year_text_view.configure(text="INVALID",
                                 fg="#ff1414",
                                 bg="#000000")
        year_text_view.update()

        course_text_view.configure(text="INVALID",
                                   fg="#ff1414",
                                   bg="#000000")
        course_text_view.update()

        ticket_valid_label.configure(text="TICKET INVALID",
                                  fg="#000000",
                                  bg="#ff1414")
        ticket_valid_label.update()
        print("Not found")

camera_list = {"Main Camera": 0,
               "OBS Virtual Camera": 1}
cameraIndex = camera_list.get("Main Camera")
def_font = "Consolas"
def_size = 30
coded_qr_padding = 40

name_text_ = "{}, {} {}"
year_text_ = "{}"
course_text_ = "{}"
is_ticket_valid = "{}"

qrScanner = QReader()
videoCaptureQR = cv.VideoCapture(cameraIndex)
qrCamera = Camera(videoCaptureQR) 

df = pd.read_csv("config_files/guestList.csv", index_col = False)
col_qrData = df["qrValues"]
col_firstName = df["firstName"]
col_middleName = df["middleName"]
col_lastName = df["lastName"]
col_year = df["year"]
col_course = df["course"]
col_contactNumber = df["contactNumber"]

# User Interface
window_width = 1920
window_height = 1080
root = tk.Tk()
root.title('Event QR Attendance System')
root.maxsize(window_width, window_height)
root.attributes("-fullscreen", True)
root.config(bg="#212121")
button_sizeimg = tk.PhotoImage(width=1, height=1) 

# Camera Frame
camera_frame = tk.Frame(master=root, 
                        width=window_width*0.482, 
                        height=window_height*0.6025, 
                        bg="#2d2e2e")
# camera_frame.pack(side="left", fill="both", expand=True)
camera_frame.grid(row=0, column=0)
camera_frame.grid_propagate(False)
# Camera Frame Elements
camera_preview = tk.Label(master=camera_frame, 
                          text="")
camera_preview.place(relx=0.5, 
                     rely=0.5, 
                     anchor="center")


scan_frame = tk.Frame(master=root, 
                      width=window_width*0.482, 
                      height=window_height*0.3975, 
                      bg="#2d2e2e")
# scan_frame.pack(side="left", fill="both", expand=True)
scan_frame.grid(row=1, column=0)
scan_frame.grid_propagate(False)
scan_button = tk.Button(scan_frame,
                        bg="#0e0e0f",
                        fg="#d9d9d9",
                        font=(def_font, def_size), 
                        text="Scan", 
                        image=button_sizeimg,
                        compound="left",
                        width=window_width*.216, 
                        height=window_height*.0975, 
                        command=scanButton)
scan_button.place(relheight=0.245,
                  relwidth=0.448,
                  relx=0.5,
                  rely=0.3,
                  anchor="center")
# scan_button.grid(row=0, column=0)


# Information Frame
info_frame = tk.Frame(master=root, 
                      width=window_width*0.518,
                      height=window_height*1.0,
                      bg="#212121")
# info_frame.pack(side="left", fill="both", expand=True)
info_frame.grid(rowspan=2, row=0, column=1)
info_frame.grid_propagate(False)
# Information Frame Elements

name_frame = tk.Frame(master=info_frame,
                      bg="#212121")
name_frame.grid(row=0,
                column=0,
                columnspan=2,
                sticky="w",
                padx=window_width*0.026,
                pady=window_height*0.0185)
name_label = tk.Label(master=name_frame,
                      bg="#212121",
                      fg="#ffffff",                     
                      text="Name",
                      font=(def_font, def_size))
name_label.grid(row=0,
                column=0,
                sticky="w")
name_text_view = tk.Label(master=name_frame,
                          bg="#C93535",
                          fg="#ffffff",
                          text="name",
                          font=(def_font, def_size))
name_text_view.grid(row=1,
                    column=0,
                    columnspan=2,
                    sticky="w")

year_frame = tk.Frame(master=info_frame,
                      bg="#212121")
year_frame.grid(row=1,
                column=0,
                sticky="w",
                padx=window_width*0.026,
                pady=window_height*0.0185)
year_label = tk.Label(master=year_frame,
                      bg="#212121",
                      fg="#ffffff",
                      text="Year",
                      font=(def_font, def_size))
year_label.grid(row=0,
                column=0,
                sticky="w")
year_text_view = tk.Label(master=year_frame,
                          bg="#C93535",
                          fg="#ffffff",
                          text="year",
                          font=(def_font, def_size))
year_text_view.grid(row=1,
                    column=0,
                    sticky="w")

course_frame = tk.Frame(master=info_frame,
                      bg="#212121")
course_frame.grid(row=1,
                column=1,
                sticky="w",
                padx=window_width*0.026,
                pady=window_height*0.0185)
course_label = tk.Label(master=course_frame,
                      bg="#212121",
                      fg="#ffffff",
                      text="Course",
                      font=(def_font, def_size))
course_label.grid(row=0,
                column=0,
                sticky="w")
course_text_view = tk.Label(master=course_frame,
                          bg="#C93535",
                          fg="#ffffff",
                          text="course",
                          font=(def_font, def_size))
course_text_view.grid(row=1,
                    column=0,
                    sticky="w")

captured_qr_frame = tk.Frame(master=info_frame,
                             width=window_width*0.186,
                             height=window_width*.186,
                             bg="#212121")
captured_qr_frame.grid(row=2,
                       column=0,
                       columnspan=2,
                       padx=window_width*0.098,
                       pady=window_height*0.0725,
                       sticky="nsew")
captured_qr_frame.grid_propagate(False)
captured_qr_view = tk.Label(master=captured_qr_frame,
                            bg="#212121")
captured_qr_view.grid(row=0,
                      column=0,
                      sticky="nsew")


ticket_valid_frame = tk.Frame(master=info_frame,
                      bg="#212121")
ticket_valid_frame.grid(row=3,
                        column=0,
                        columnspan=2,
                        sticky="n",
                        padx=window_width*0.026,
                        pady=window_height*0.0185)
ticket_valid_label = tk.Label(master=ticket_valid_frame,
                              text=is_ticket_valid.format("TICKET STATUS"),
                              bg="#C93535",
                              fg="#ffffff",
                              font=(def_font, def_size),
                              padx=10,
                              pady=10)
ticket_valid_label.grid(row=0,
                        column=0,
                        sticky="n")
ticket_valid_label.grid_propagate(False)

startEvent()
root.mainloop()