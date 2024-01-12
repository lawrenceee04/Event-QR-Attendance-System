import cv2 as cv
from qreader import QReader
import pandas as pd
import customtkinter as ctk
from PIL import Image
import vtk

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
        frame = frame[0:480, 80:560]
        frame = Image.fromarray(frame)
        # Convert PIL Image to ctkImage
        frame_preview = vtk.vtkImageData()
        frame_preview.SetDimensions(frame.size[0], frame.size[1], 1)
        frame_preview.AllocateScalars(vtk.VTK_UNSIGNED_CHAR, 3)
        for y in range(frame.size[1]):
            for x in range(frame.size[0]):
                r, g, b = frame.getpixel((x, y))
                frame_preview.SetScalarComponentFromFloat(x, y, 0, 0, r / 255.0)
                frame_preview.SetScalarComponentFromFloat(x, y, 0, 1, g / 255.0)
                frame_preview.SetScalarComponentFromFloat(x, y, 0, 2, b / 255.0)
        camera_preview.configure(image=frame_preview)
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
                    print(code_text_.format(qrData))
                    cv.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 10)
                    # frame_preview = ImageTk.PhotoImage(Image.fromarray(frame))
                    camera_preview.configure(image=frame_preview)
                    # camera_preview.image=frame_preview
                    camera_preview.update()
                    code_text_view.configure(text=code_text_.format(qrData))
                    code_text_view.update()
                    name_text_view.configure(text=name_text_.format(col_firstName[i]))
                    name_text_view.update()
                    cv.waitKey(1500)
                    break
                else:
                    code_text_view.configure(text=" ")
                    code_text_view.update()
                    name_text_view.configure(text=" ")
                    name_text_view.update()
                    print("Not found")
    except:
        code_label.configure(text="Code:")
        code_label.update()
        print("Not found")


# Camera for Scanning
camera_list = {"Main Camera": 0,
               "OBS Virtual Camera": 1}
cameraIndex = camera_list.get("Main Camera")

code_text_ = "{}"
name_text_ = "{}"

# Initialize QReader and QR OpenCV Camera
qrScanner = QReader()
videoCaptureQR = cv.VideoCapture(cameraIndex)
qrCamera = Camera(videoCaptureQR) 

# Assign dataframes to the information of the guests
df = pd.read_csv("config_files/guestList.csv", index_col = False)
col_qrData = df["qrValues"]
col_firstName = df["firstName"]


# User Interface
window_width = 1000
window_height = 800
root = ctk.CTk()
root.title('Event QR Attendance System')
root.maxsize(window_width, window_height)

# Camera Frame
camera_frame = ctk.CTkFrame(master=root, width=window_width*0.482, height=window_height*0.6025)
# camera_frame.pack(side="left", fill="both", expand=True)
camera_frame.grid(row=0, column=0)
camera_frame.grid_propagate(False)
# Camera Frame Elements
camera_preview = ctk.CTkLabel(master=camera_frame, text="")
camera_preview.grid(row=0, column=0)


scan_frame = ctk.CTkFrame(master=root, width=window_width*0.482, height=window_height*0.3975)
# scan_frame.pack(side="left", fill="both", expand=True)
scan_frame.grid(row=1, column=0)
scan_frame.grid_propagate(False)
scan_button = ctk.CTkButton(scan_frame, text="Scan", font=("Open Sans", 40), width=100, height=10, command=scanButton)
scan_button.grid(row=0, column=0)


# Information Frame
info_frame = ctk.CTkFrame(master=root, width=window_width*0.518, height=window_height*1.0)
# info_frame.pack(side="left", fill="both", expand=True)
info_frame.grid(rowspan=2, row=0, column=1)
info_frame.grid_propagate(False)
# Information Frame Elements
name_label = ctk.CTkLabel(master=info_frame, text="Name")
name_label.grid(row=0, columnspan=1, column=0)
name_text_view = ctk.CTkLabel(master=info_frame, text=name_text_)
name_text_view.grid(row=1, columnspan=4, column=0)
code_label = ctk.CTkLabel(master=info_frame, text="Code")
code_label.grid(row=2, columnspan=1, column=0)
code_text_view = ctk.CTkLabel(master=info_frame, text=name_text_)
code_text_view.grid(row=3, columnspan=4, column=0)

startEvent()
root.mainloop()