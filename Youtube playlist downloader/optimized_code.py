from collections import deque   #for creating queues
from fileinput import filename
from os import system, sys
import threading
from time import sleep
from tkinter import filedialog as fd
from tkinter.filedialog import  Tk # select folders
from pytube import YouTube, Playlist
import pyinputplus as pyip  # for input validation
import moviepy.editor as movie  # for converting mp4 to mp3
import multiprocessing as mp

undownloaded_vids_urls = deque()  #creating a queue of the urls of the videos that were not downloaded. first added url, first downloaded
root = Tk() #pointing root to Tk() to use it as Tk() in program.
root.withdraw() #Hides small tkinter window.
root.attributes('-topmost', True) #Opened windows will be active. above all windows despite of selection.
Qualities = ["240", "360p", "480p", "720p"]

def quality_menu(): # display the quality menu
    return pyip.inputMenu(Qualities, "Choose the quality: \n", numbered=True)

def show_info(yt, choice, quality = "720p"):    #File info. choice = 1 for videos, cboice = 3 for audios
    if choice == 1:
        print(f"""\n
            Title: {yt.title}
            Duration: {round(yt.length/60)} minutes
            Number of views: {yt.views:,} views
            Size: {round((yt.streams.get_by_resolution(quality).filesize)/1024/1024, 2)} MB
            """)
    elif choice == 3:
        print(f"""\n
            Title: {yt.title}
            Duration: {round(yt.length/60)} minutes
            Number of views: {yt.views:,} views
            Size: {round((yt.streams.get_by_itag(251).filesize)/1024/1024, 2)} MB
            """)

def progress_function(chunk, file_handling, bytes_remaining):     # function to show the progress of the download
    global filesize
    filesize=chunk.filesize
    current = ((filesize - bytes_remaining)/filesize)
    percent = ('{0:.1f}').format(current*100)
    progress = int(50*current)
    status = '█' * progress + '-' * (50 - progress)
    #change the color of the progress bar to green when the download is complete
    if bytes_remaining == 0:
        status = '\033[92m' + status + '\033[0m'
    sys.stdout.write(' ↳ |{bar}| {percent}%\r'.format(bar=status, percent=percent))
    sys.stdout.flush()

def undownloaded_videos(undownloaded_vids_urls, file_path):
    #=============================================================================
    # Videos that were not downloaded for any reason will be handeled here
    # undownloaded_vids: list of the names of the undownloaded videos
    # undownloaded_vids_urls: list of the URLs of the undownloaded videos
    #=============================================================================
    choice = pyip.inputMenu(["Re-download the videos that were not downloaded", "Return"], "\nDo you want to download them again? \n", numbered=True)
    if choice == "Re-download the videos that were not downloaded":
        i = -1
        while undownloaded_vids_urls != deque([]):  #try all the available qualities on each video until the queue is empty
            check = Video_downloader(undownloaded_vids_urls[0], Qualities[i], file_path)    # pass the first url in the queue to re-download it
            if check == 1:  # video not downloaded
                undownloaded_vids_urls.pop()
                i-=1    #try the next quality in the array
                if i == -5:
                    print(f"Could not download: {YouTube(undownloaded_vids_urls[0]).title}")    #all the qualities didn't work
                    undownloaded_vids_urls.popleft()    #remove the broken url from the queue to prevent an infinite loop
                    i = -1
            else:
                undownloaded_vids_urls.popleft()
                i = -1
    elif choice == "Return":
        undownloaded_vids_urls.clear()
        return

def Video_downloader(url, quality, file_path, i = ""):
    #============================================================
    # Download videos from youtube
    # :param url: URL of the video
    # :param quality: the quality chosen by the user
    # :param file_path: the file path to save the files
    # :param i: used to number the videos when downloading playlists, default = "" for downloading one video
    #============================================================
    yt = YouTube(url, on_progress_callback = progress_function)
    yt.streams.filter(progressive=True, file_extension="mp4").all()
    stream = yt.streams.get_by_resolution(quality)  # returns type stream if the quality is available else None
    if not stream:
        #undownloaded_vids.append(f"{i} {yt.title}")
        undownloaded_vids_urls.append(url)
        print(f"Could not download video: {yt.title}. Quality {quality} not available.")
        # skip and download next video
        return 1
    show_info(yt, 1, quality)
    stream.download(output_path=file_path, filename_prefix=f"{i} ")
    return 2

def Playlist_downlaoder(url, quality, file_path):
    #============================================================
    # Download playlists from youtube
    # :param url: URL of the playlist
    # :param quality: the quality chosen by the user
    # :param file_path: the file path to save the files
    #============================================================
    yt = Playlist(url)
    if len(yt.video_urls) == 1:
        Video_downloader(yt.video_urls[0])
        return
    print(f"""
        Number of videos: {yt.length}
        Total number of views: {yt.views:,}
        Last updated: {yt.last_updated}
    """)
    higher_range = ""   # the default option is download to the last video in the playlist
    lower_range = 1  #the default option is download starting from the first video in the playlist
    all_some = pyip.inputMenu(["All", "Some"], "Download all or some videos: \n", numbered=True)
    if all_some == "Some":
        lower_range = pyip.inputNum("Download from video number: ", min=1, max=yt.length)
        higher_range = pyip.inputNum("to video number (leave it blank to download till the last video): ",
                                                                                 min=lower_range+1, max=yt.length, blank=True)

    for i in range(lower_range, yt.length+1 if higher_range == "" else higher_range+1):
        Video_downloader(yt.video_urls[i-1], quality, file_path, i)
    #elif all_some == "All":
     #   for i in range(1, yt.length+1):
      #      Video_downloader(yt.video_urls[i-1], quality, file_path, i) 
 
def extract_audio(url):
    #=========================================
    # Download audio from youtube
    # :param url: the url of the youtube video
    #=========================================
    yt = YouTube(url, on_progress_callback=progress_function)
    yt.streams.filter(only_audio=True).first()
    stream = yt.streams.get_by_itag(251)    #get the highest audio quality
    show_info(yt, 3)
    save_file = fd.askdirectory(title = "Save")
    print(f"Downloading audio: {yt.title}")
    stream.download(output_path=save_file)

def converter(file_path, file_name):  # video to audio converter
    clip = movie.VideoFileClip(file_path)
    save_file = fd.askdirectory(title = "Save") #save to...
    clip.audio.write_audiofile(f"{save_file}/{file_name}.mp3")
    print("Conversion completed")

def main():
    while 1:
        vid_list = pyip.inputMenu(["Video downloader", "Playlist downlaoder", "Extract audio", "Video to audio converter","Exit"], numbered= True )
        system("cls")

        if vid_list == "Video downloader":
            url = pyip.inputStr("Enter the video url: ", blank=False)
            quality = quality_menu()
            file_path = fd.askdirectory(title = "Save")
            p = mp.Process(target=Video_downloader, args=(url, quality, file_path))
            p.start()
            #Video_downloader(url, quality, file_path)

        elif vid_list == "Playlist downlaoder":
            url = pyip.inputStr("Enter the playlist url: ", blank=False)
            quality = quality_menu()
            file_path = fd.askdirectory(title = "Save")
            p = mp.Process(target=Playlist_downlaoder, args=(url, quality, file_path))
            p.start()
            #Playlist_downlaoder(url, quality, file_path)

        elif vid_list == "Extract audio":
            url = input("Enter the video url: ")
            p = mp.Process(target=extract_audio, args=(url, ))
            p.start()
            #extract_audio(url)

        elif vid_list == "Video to audio converter":
            file_path = fd.askopenfilename(title = 'Select a file', filetypes = [("MP4 files", "*.mp4")])
            #list(file_path.split("/"))
            file_name = list(file_path.split("/"))[-1].removesuffix(".mp4")
            p = mp.Process(target=converter, args=(file_path, file_name))
            p.start()
            #converter(file_path, file_name)

        elif vid_list == "Exit":
            sys.exit()

        if undownloaded_vids_urls != deque([]):      # if a video was not downloaded, ask the user if he wants to download it again
            p = mp.Process(target=undownloaded_videos, args=(undownloaded_vids_urls, file_path))
            p.start()
            #undownloaded_videos(undownloaded_vids_urls, file_path)
        p.join()    # terminate any active process
        
        sleep(2)
        system("cls")


# start the execution of the program here
if __name__ == "__main__":
    main()
