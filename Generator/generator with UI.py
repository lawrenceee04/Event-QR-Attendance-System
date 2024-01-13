import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

root_width = 1000
root_height = 900
root_geometry = "{}x{}"
def_font = "Consolas"
def_size = 20

root = tk.Tk()
root.geometry(root_geometry.format(root_width, root_height))
root.maxsize(root_width, root_height)
root.title("Ticket Generator")

# tk.StringVar
event_name = tk.StringVar()


ticket_preview_frame = tk.Frame(master=root,
                                bg="#c7c7c7",
                                width=root_width*0.888,
                                height=root_height*0.505)
ticket_preview_frame.grid(row=0,
                          column=0,
                          padx=root_width*0.056,
                          pady=root_height*0.075)
ticket_preview_frame.grid_propagate(False)

ticket_preview_canvas = tk.Canvas(master=ticket_preview_frame,
                                  bg="#c7c7c7",
                                  width=root_width*0.888,
                                  height=root_height*0.505)
ticket_preview_canvas.grid(row=0,
                          column=0)

ticket_settings_frame = tk.Frame(master=root,
                                     width=root_width*0.888,
                                     height=root_height*0.29,
                                     bg="#c7c7c7")
ticket_settings_frame.grid(row=1,
                           columnspan=1,
                           column=0,
                           padx=10,
                           pady=10)
ticket_settings_frame.grid_propagate(False)

event_name_label = tk.Label(master=ticket_settings_frame,
                            text="Event Name",
                            fg="#000000",
                            bg="#c7c7c7",
                            font=(def_font, def_size))
event_name_label.grid(row=0,
                      column=0,
                      sticky="w",
                      padx=10,
                      pady=10)

event_name_text_view = tk.Entry(master=ticket_settings_frame,
                                textvariable = event_name,
                                fg="#000000",
                                bg="#c7c7c7",
                                font=(def_font, def_size,),
                                borderwidth=4,
                                relief="solid")

event_name_text_view.grid(row=1,
                      column=0,
                      sticky="w",
                      padx=10,
                      pady=10)
root.mainloop()