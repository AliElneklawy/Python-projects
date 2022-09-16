from collections import deque   #for creating queues
#from fileinput import filename
from os import system, sys
from os import rename
from time import sleep
from tkinter import filedialog as fd
from tkinter.filedialog import  Tk # select folders
#import multiprocessing as mp
from pytube import YouTube, Playlist
import pyinputplus as pyip  # for input validation
import moviepy.editor as movie  # for converting mp4 to mp3
from string import punctuation
#import pyautogui

undownloaded_vids_urls = deque()  #creating a queue of the urls of the videos that were not downloaded. first added url, first downloaded
root = Tk() #pointing root to Tk() to use it as Tk() in program.
root.withdraw() #Hides small tkinter window.
root.attributes('-topmost', True) #Opened windows will be active. above all windows despite of selection.
Qualities = ["144", "240", "360p", "480p", "720p"]

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

def progress_function(chunk, file_handling, bytes_remaining):
    '''
    function to show the progress of the download
    '''
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
    '''
     Videos that were not downloaded for any reason will be handeled here
     undownloaded_vids: list of the names of the undownloaded videos
     undownloaded_vids_urls: list of the URLs of the undownloaded videos
    '''
    choice = pyip.inputMenu(["Re-download the videos that were not downloaded", "Return"],
                             "\nDo you want to download them again? \n", numbered=True)
    if choice == "Re-download the videos that were not downloaded":
        i = -1
        while undownloaded_vids_urls != deque([]):  #try all the available qualities on each video until the queue is empty
            check = Video_downloader(undownloaded_vids_urls[0][0], Qualities[i], file_path, undownloaded_vids_urls[0][1])    # pass the first url in the queue to re-download it
            if check == 1:  # video not downloaded
                undownloaded_vids_urls.pop()
                i-=1    #try the next quality in the array
                if i == -5: #reached the end of the array of qualities
                    print(f"Could not download: {YouTube(undownloaded_vids_urls[0][0]).title}")    #all the qualities didn't work
                    undownloaded_vids_urls.popleft()    #remove the broken url from the queue to prevent an infinite loop
                    i = -1
            else:
                undownloaded_vids_urls.popleft()
                i = -1
    elif choice == "Return":
        undownloaded_vids_urls.clear()
        return

def available_captions(yt, file_path):
    '''
     Check if there are captions available for the video
     :param yt: YouTube object of the video
    '''
    cap = yt.captions
    langs = {} # dictionary to store the languages and their codes. Since we have mapping between the codes and the languages, dicts are suitable.
    for capt in cap:
        if '(auto-generated)' in capt.name: #skip auto-generated captions
                continue
        langs.update({capt.name: capt.code})
    if len(langs) > 0:
        lang = pyip.inputMenu(list(langs.keys()), "Choose a language: \n", numbered=True)   # choose a language
        return langs[lang]  #return language code
        #Download_captions(yt, file_path, langs[lang])
    return False

def Download_captions(yt, file_path, lang_code):
    '''
     Download captions from youtube
     :param url: URL of the video
     :param file_path: the file path to save the file
    '''
    caption = yt.captions[lang_code]
    caption.generate_srt_captions()
    caption.download(title=yt.title, output_path=file_path)
    oldname = file_path + '/' + yt.title + ' ('+ lang_code +')'+'.srt'
    newname = file_path + '/' + yt.title+'.srt'

    try:
        rename(oldname, newname)
    except:
        invalid_chars = punctuation  # list of invalid characters
        if any(char in invalid_chars for char in yt.title): #if the title contains invalid characters, replace them with ''
        # replace the invalid characters in the filename with nothing
            newname = file_path + '/' + yt.title.translate(str.maketrans('', '', invalid_chars)) + '.srt'
            oldname = file_path + '/' + yt.title.translate(str.maketrans('', '', invalid_chars)) + ' ('+ lang_code +')' + '.srt'
            try:
                 rename(oldname, newname)
            except:
                print("Could not rename the file. Maybe, the file already exists. Rename it manually.")


def Video_downloader(url, quality, file_path, i = ""):
    '''
     Download videos from youtube
     :param url: URL of the video
     :param quality: the quality chosen by the user
     :param file_path: the file path to save the files
     :param i: used to number the videos when downloading playlists, default = "" for downloading one video
    '''
    yt = YouTube(url, on_progress_callback = progress_function)
    yt.streams.filter(progressive=True, file_extension="mp4").all()
    stream = yt.streams.get_by_resolution(quality)  # returns type stream if the quality is available else None
    if not stream:
        undownloaded_vids_urls.append([url, i])
        print(f"Could not download video: {yt.title}. Quality {quality} not available.")
        # skip and download next video
        return 1
    show_info(yt, 1, quality)
    stream.download(output_path=file_path, filename_prefix='' if i == "" else f"{i} ")
    return 2

def Playlist_downlaoder(url, quality, file_path):
    '''
    Download playlists from youtube
    :param url: URL of the playlist
    :param quality: the quality chosen by the user
    :param file_path: the file path to save the files
    '''
    yt = Playlist(url)
    if len(yt.video_urls) == 1:
        Video_downloader(yt.video_urls[0], quality, file_path, i = 1)
        return

    print(f"""
        Number of videos: {yt.length}
        Total number of views: {yt.views}
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

def extract_audio(url):
    """ Download audio from youtube
    :param url: the url of the youtube video """
    yt = YouTube(url, on_progress_callback=progress_function)
    yt.streams.filter(only_audio=True).first()
    stream = yt.streams.get_by_itag(251)    #get the highest audio quality
    save_file = fd.askdirectory(title = "Save")
    show_info(yt, 3)
    print(f"Downloading audio: {yt.title}")
    stream.download(output_path=save_file)

def converter(file_path, file_name):  # video to audio converter
    clip = movie.VideoFileClip(file_path)
    save_file = fd.askdirectory(title = "Save") #save to...
    clip.audio.write_audiofile(f"{save_file}/{file_name}.mp3")
    clip.close()
    print("Conversion completed")

def main():
    vid_list = pyip.inputMenu(["Video downloader",
                              "Playlist downlaoder",
                               "Download captions",
                               "Extract audio",
                               "Video to audio converter",
                               "Exit"], numbered= True)
    system("cls")
    # lang='' # do not download captions by default
    # if vid_list == "Video downloader" or vid_list == "Playlist downlaoder":
    #     url = pyip.inputStr("Enter the url: ", blank=False)
    #     down_cap = pyip.inputMenu(["Download captions", "Don't download captions"], "Download captions? \n", numbered=True)
    #     if down_cap == "Download captions":
    #        lang = available_captions(YouTube(url))    #get the available languages
    #        #lang = pyip.inputMenu(list(langs.keys()), "Choose a language: \n", numbered=True)   # choose a language


    if vid_list == "Video downloader":
        url = pyip.inputStr("Enter the url: ", blank=False)
        quality = quality_menu()
        file_path = fd.askdirectory(title = "Save")
        Video_downloader(url, quality, file_path)

    elif vid_list == "Playlist downlaoder":
        url = pyip.inputStr("Enter the url: ", blank=False)
        quality = quality_menu()
        file_path = fd.askdirectory(title = "Save")
        Playlist_downlaoder(url, quality, file_path)

    elif vid_list == "Download captions":
        url = pyip.inputStr("Enter the video url: ", blank=False)
        file_path = fd.askdirectory(title = "Save")
        lang = available_captions(YouTube(url))    #get the available languages
        Download_captions(url, file_path, lang)

    elif vid_list == "Extract audio":
        url = input("Enter the video url: ")
        extract_audio(url)

    elif vid_list == "Video to audio converter":
        file_path = fd.askopenfilename(title = 'Select a file', filetypes = [("mkv files", "*.mkv"), ("MP4 files", "*.mp4")])
        file_name = tuple(file_path.split("/"))[-1]
        file_name = file_name.removesuffix(".mp4") if file_name.endswith(".mp4") else file_name.removesuffix(".mkv")
        converter(file_path, file_name)

    elif vid_list == "Exit":
        sys.exit()

    if undownloaded_vids_urls != deque([]):      # if a video was not downloaded, ask the user if he wants to download it again
        undownloaded_videos(undownloaded_vids_urls, file_path)

    sleep(2)
    system("cls")

if __name__ == "__main__":
    while 1:
        main()
