import customtkinter as ctk
code_text_ = "{}"
name_text_ = "{}"

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
camera_preview = ctk.CTkLabel(master=camera_frame)
camera_preview.grid(row=0, column=0)


scan_frame = ctk.CTkFrame(master=root, width=window_width*0.482, height=window_height*0.3975)
# scan_frame.pack(side="left", fill="both", expand=True)
scan_frame.grid(row=1, column=0)
scan_frame.grid_propagate(False)
scan_button = ctk.CTkButton(scan_frame, text="Scan", font=("Open Sans", 40), width=100, height=10)
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

root.mainloop()