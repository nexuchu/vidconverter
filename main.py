import ffmpeg
import customtkinter
import tkinter as tk
import os
from GUI import App
from ffmpeg import FFmpeg, Progress

def on_convert(name, files, path, format): #converts the provided video to mp4 format
    print(rf"{path}\\{name}.mp4")
    filecount = len(files)
    for num, file_path in enumerate(files):
        print(file_path)
        ffmpeg = (
            FFmpeg()
            .option("y")
            .input(file_path)
            .output(
                f"{path}\\{name}-{num+1}{format}",
                codec="copy"
            )
        )

        @ffmpeg.on("completed")
        def on_completion():
            app.home_frame_button_4.configure(text=f"Converted! {num+1}/{filecount}")
            if num+1 == filecount:
                os.system(f'start {os.path.realpath(path)}')

        ffmpeg.execute()


if __name__ == "__main__":
    app = App(on_convert)
    app.mainloop()