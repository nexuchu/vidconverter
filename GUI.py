import customtkinter
from tkinter import filedialog    


class App(customtkinter.CTk):
    def __init__(self, on_convert_callback, download_youtube):
        super().__init__()
        self.on_convert_callback = on_convert_callback
        self.download_youtube = download_youtube

        self.title("Media Converter")
        self.geometry("700x450")

        # set default values
        self.format = '.mp4'
        self.res = '144p'
        self.showprogress = False

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)


        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="Media Converter",
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Video converter",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Youtube to MP4/MP3",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Cut video",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")




        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_label = customtkinter.CTkLabel(self.home_frame, text="Convert any video to different video/audio formats!")
        self.home_frame_large_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_frame_button_1 = customtkinter.CTkButton(self.home_frame, text="Choose videos", command=self.select_file)
        self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.home_frame_button_2 = customtkinter.CTkButton(self.home_frame, text="Output folder", command=self.select_output)
        self.home_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.home_frame_optionframe = customtkinter.CTkOptionMenu(self.home_frame, values=['.mp4', '.mpg', '.mov', '.mp3'], command=self.optionmenu_callback, width=50)
        self.home_frame_optionframe.grid(row=3, column=0, padx=20, pady=10)
        self.home_frame_entry = customtkinter.CTkEntry(self.home_frame, placeholder_text="Title (no spaces)")
        self.home_frame_entry.grid(row=4, column=0, padx=20, pady=10)
        self.home_frame_button_4 = customtkinter.CTkButton(self.home_frame, text="Convert", command=self.Convert)
        self.home_frame_button_4.grid(row=5, column=0, padx=20, pady=10)

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0, weight=1)

        self.second_frame_label = customtkinter.CTkLabel(self.second_frame, text="Paste your youtube link below:")
        self.second_frame_label.grid(row=0, column=0, padx=20, pady=20)
        self.second_frame_entry = customtkinter.CTkEntry(self.second_frame, placeholder_text="URL")
        self.second_frame_entry.grid(row=1, column=0, padx=20, pady=10)
        self.second_frame_optionframe = customtkinter.CTkOptionMenu(self.second_frame, values=['144p', '360p', '720p', '1080p'], command=self.optionmenu_yt_callback, width=50)
        self.second_frame_optionframe.grid(row=2, column=0, padx=20, pady=10)  
        self.second_frame_button_1 = customtkinter.CTkButton(self.second_frame, text="Output folder", command=self.select_output)
        self.second_frame_button_1.grid(row=3, column=0, padx=20, pady=10)      
        self.second_frame_button_2 = customtkinter.CTkButton(self.second_frame, text="Download", command=self.Download)
        self.second_frame_button_2.grid(row=4, column=0, padx=20, pady=10)
        self.second_frame_progress_label = customtkinter.CTkLabel(self.second_frame, text="0%")
        self.second_frame_progress_bar = customtkinter.CTkProgressBar(self.second_frame)

        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")



    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def optionmenu_callback(self, choice):
        self.format = choice
    
    def optionmenu_yt_callback(self, choice):
        self.res = choice
    
    def progress_visibility(self):
        if self.showprogress == True:
            self.second_frame_progress_label.grid(row=5, column=0, padx=20, pady=0)
            self.second_frame_progress_bar.grid(row=6, column=0, padx=20, pady=10)
        else:
            self.second_frame_progress_label.grid_forget()
            self.second_frame_progress_bar.grid_forget()

    def select_file(self): #for the file chooser popup, chooses the file and changes the button
        self.files = [x.replace("/", "\\") for x in list(filedialog.askopenfilenames())]
        self.home_frame_button_1.configure(text=f"Videos chosen ({len(self.files)})", fg_color="green")

    
    def select_output(self): #for the file chooser popup to choose the output path, chooses the path(folder)and changes the button
        self.outputpath = filedialog.askdirectory().replace('/', f'\\')
        self.home_frame_button_2.configure(text=f"Output folder chosen ({self.outputpath})", fg_color="green")
        self.second_frame_button_1.configure(text=f"Output folder chosen ({self.outputpath})", fg_color="green")

    def Percentage(self, percentage):
        self.second_frame_progress_label.configure(text=f"{int(percentage)}%")
        self.second_frame_progress_label.update()
        self.second_frame_progress_bar.set(float(percentage/100))

    def Convert(self): #checks if the data provided is enough, if yes, gives data to main py file
        self.name = self.home_frame_entry.get()
        self.home_frame_entry.delete(first_index=0, last_index=len(self.name))
        if self.files and self.name and self.outputpath != "":
            print(self.name)
            print(self.files)
            print(self.outputpath)
            self.home_frame_button_1.configure(text="Choose videos", fg_color='#1F6AA5')
            self.home_frame_button_2.configure(text="Output folder", fg_color="#1F6AA5")
            self.home_frame_button_4.configure(text="Converting...")
            self.on_convert_callback(self.name, self.files, self.outputpath, self.format)
        else:
            self.home_frame_button_4.configure(text="Missing required parameters! Retry!")
        
    def Download(self):
        self.link = self.second_frame_entry.get()
        self.second_frame_entry.delete(first_index=0, last_index=len(self.link))
        if self.link and self.outputpath != '':
            print(self.link)
            print(self.res)
            print(self.outputpath)
            self.download_youtube(self.link, self.res, self.outputpath)
            self.second_frame_button_1.configure(text="Output folder", fg_color="#1F6AA5")
        else:
            self.home_frame_button_2.configure(text="Missing required parameters! Retry!")

if __name__ == "__main__":
    app = App()
    app.mainloop()