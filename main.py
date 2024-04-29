import os
from GUI import App
from ffmpeg import FFmpeg
from pytube import YouTube
from threading import Thread

def on_convert(name, files, path, format): # converts the video(s) to the provided format
    print(rf"{path}\\{name}.mp4")
    filecount = len(files)
    for num, file_path in enumerate(files):
        print(file_path)
        ffmpeg = (
            FFmpeg()
            .option("y")
            .input(file_path)
            .output(
                f"{path}\\{name}-{num+1}{format}"
            )
        )

        @ffmpeg.on("completed")
        def on_completion():
            app.home_frame_button_4.configure(text=f"Converted! {num+1}/{filecount}")
            if num+1 == filecount:
                os.system(f'start {os.path.realpath(path)}')

        ffmpeg.execute()

def download_worker(yt, path): # downloads the video and updates GUI
    app.showprogress = True
    app.progress_visibility()
    app.second_frame_button_2.configure(text="Downloading...")
    yt.download(path)
    app.showprogress = False
    app.progress_visibility()
    app.second_frame_button_2.configure(text="Downloaded video!")
    os.system(f'start {os.path.realpath(path)}')

def on_progress(stream, chunk, bytes_remaining): # updates progress bar info
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_completed = bytes_downloaded / total_size * 100
    app.Percentage(percentage_completed)

def download_youtube(link, res, path): # checks if the info provided is correct, if so, downloads the video threaded
    try:
        yt = YouTube(link, on_progress_callback=on_progress)
        if res != '1080p':
            yt = yt.streams.get_by_resolution(res)
        else:
            yt = yt.streams.get_highest_resolution()
        if yt:
            th = Thread(target=download_worker, daemon=True, args=(yt, path))
            th.start()
        else:
            raise ValueError("No video streams found for set resolution")
    except Exception as e: 
        app.second_frame_button_2.configure(text=f"An error has occurred: {e}")
        print(e)


if __name__ == "__main__":
    app = App(on_convert, download_youtube)
    app.mainloop()