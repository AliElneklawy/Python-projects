from collections import deque
from fileinput import filename
from os import system, sys
from time import sleep
from pytube import YouTube, Playlist
import pyinputplus as pyip  # for input validation
import moviepy.editor as movie
from tkinter.filedialog import askdirectory, Tk # select folders
from tkinter import filedialog as fd 

undownloaded_vids = deque() # creating a queue of the urls of the videos that were not downloaded. first added url, first downloaded
undownloaded_vids_urls = deque()
root = Tk() # pointing root to Tk() to use it as Tk() in program.
root.withdraw() # Hides small tkinter window.
root.attributes('-topmost', True) # Opened windows will be active. above all windows despite of selection.
Qualities = ["240", "360p", "480p", "720p"]

def quality_menu():
    return pyip.inputMenu(Qualities, "Choose the quality: \n", numbered=True)

def show_info(yt, choice, quality = "720p"):
    if choice == 1:
        print(f"""\n
            Title: {yt.title}
            Duration: {round(yt.length/60)} minutes
            Number of views: {yt.views:,} views
            Size: {round((yt.streams.get_by_resolution(quality).filesize)/1024/1024, 2)} MB
            """)
    elif choice == 3:
        print(f"""
            Title: {yt.title}
            Duration: {round(yt.length/60)} minutes
            Number of views: {yt.views:,} views
            Size: {round((yt.streams.get_by_itag(251).filesize)/1024/1024, 2)} MB
            """)

def progress_function(chunk, file_handle, bytes_remaining):     # function to show the progress of the download
    global filesize
    filesize=chunk.filesize
    current = ((filesize - bytes_remaining)/filesize)
    percent = ('{0:.1f}').format(current*100)
    progress = int(50*current)
    status = '█' * progress + '-' * (50 - progress)
    #change the color of the progress bar to green when the download is complete
    if(bytes_remaining == 0):
        status = '\033[92m' + status + '\033[0m'
    sys.stdout.write(' ↳ |{bar}| {percent}%\r'.format(bar=status, percent=percent))
    sys.stdout.flush()

def undownloaded_videos(undownloaded_vids, undownloaded_vids_urls, quality, file_path):
    #print(f"\nThe following videos were not downloaded because they are not available in {quality}: ")
    # print the names of the videos that were not downloaded
    #for i in undownloaded_vids:
    #    print(f"{i}")
    choice = pyip.inputMenu(["Re-download the videos that were not downloaded", "Return"], "\nDo you want to download them again? \n", numbered=True)
    if choice == "Re-download the videos that were not downloaded":
        i = -1
        #quality = quality_menu()
        while undownloaded_vids_urls != deque([]):
            check = Video_downloader(undownloaded_vids_urls[0], Qualities[i], file_path)
            #undownloaded_vids.popleft()
            if check == 1:
                undownloaded_vids_urls.pop()
                i-=1
                if i == -5:
                    print(f"Could not download: {YouTube(undownloaded_vids_urls[0]).title}")
                    undownloaded_vids_urls.popleft()
                    i = -1
            else:
                undownloaded_vids_urls.popleft()
                i = -1
    elif choice == "Return":
        #undownloaded_vids.clear()
        undownloaded_vids_urls.clear()
        return

def Video_downloader(url, quality, file_path, i = ""):
    yt = YouTube(url, on_progress_callback = progress_function)
    yt.streams.filter(progressive=True, file_extension="mp4").all()
    stream = yt.streams.get_by_resolution(quality)  # returns type stream if the quality is available else None
    if not stream:
        #undownloaded_vids.append(f"{i} {yt.title}")
        undownloaded_vids_urls.append(url)
        print(f"Could not download video: {yt.title}. Quality {quality}p not available.")
        # skip and download next video
        return 1
    show_info(yt, 1, quality)
    stream.download(output_path=file_path, filename_prefix=f"{i} ")
    return 2

def Playlist_downlaoder(url, quality, file_path):
    yt = Playlist(url)
    if(len(yt.video_urls) == 1):
        Video_downloader(yt.video_urls[0])
        return
    print(f"""
        Number of videos: {yt.length}
        Total number of views: {yt.views:,}
        Last updated: {yt.last_updated}
    """)
    all_some = pyip.inputMenu(["All", "Some"], "Download all or some videos: \n", numbered=True)
    if all_some == "Some":
        lower_range = pyip.inputNum("Download from video number: ", min=1, max=yt.length)
        higher_range = pyip.inputNum("to video number (Leave it blank to download till the las video): ", 
                                                                                 min=lower_range, max=yt.length, blank=True)                                                                                                    
        for i in range(lower_range, yt.length if higher_range == "" else higher_range+1):
            Video_downloader(yt.video_urls[i-1], quality, file_path, i)
    elif all_some == "All":
        for i in range(1, yt.length+1):
            Video_downloader(yt.video_urls[i-1], quality, file_path, i) 
    
def extract_audio(url):
    yt = YouTube(url, on_progress_callback=progress_function)
    yt.streams.filter(only_audio=True).first()
    stream = yt.streams.get_by_itag(251)
    show_info(yt, 3)
    save_file = fd.askdirectory(title = "Save")
    print(f"Downloading audio: {yt.title}")
    stream.download(output_path=save_file)

def converter(file_path, file_name):  # video to audio converter
    clip = movie.VideoFileClip(file_path)
    save_file = fd.askdirectory(title = "Save")
    clip.audio.write_audiofile(f"{save_file}/{file_name}.mp3")
    print("Conversion completed")

# start the execution of the program here
if __name__ == "__main__":
    while 1:
        vid_list = pyip.inputMenu(["Video downloader", "Playlist downlaoder", "Extract audio", "Video to audio converter","Exit"], numbered= True )
        system("cls")

        if vid_list == "Video downloader":
            url = pyip.inputStr("Enter the video url: ", blank=False)
            quality = quality_menu()
            file_path = fd.askdirectory(title = "Save")
            Video_downloader(url, quality, file_path)

        elif vid_list == "Playlist downlaoder":
            url = pyip.inputStr("Enter the playlist url: ", blank=False)
            quality = quality_menu()
            file_path = fd.askdirectory(title = "Save")
            Playlist_downlaoder(url, quality, file_path)

        elif vid_list == "Extract audio":
            url = input("Enter the video url: ")
            extract_audio(url)

        elif vid_list == "Exit":
            exit()

        elif vid_list == "Video to audio converter":
            file_path = fd.askopenfilename(title = 'Select a file', filetypes = [("MP4 files", "*.mp4")])
            list(file_path.split("/"))
            file_name = list(file_path.split("/"))[-1].removesuffix(".mp4")
            converter(file_path, file_name)
        
        if undownloaded_vids_urls != deque([]):      # if a video was not downloaded, ask the user if he wants to download it again
            undownloaded_videos(undownloaded_vids, undownloaded_vids_urls, quality, file_path)
        
        sleep(3)
        system("cls")
