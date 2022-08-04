from os import system
from pytube import YouTube, Playlist
import pyinputplus as pyip  # for input validation


def quality_menu():
    return pyip.inputMenu(["360p", "480p", "720p", "1080p"], "Choose the quality: \n", numbered=True)

def show_info(yt):
    print(f"""
        Title: {yt.title}
        Duration: {round(yt.length/60)} minutes
        Number of views: {yt.views:,} views
        Video size: {round((yt.streams.get_by_resolution("720p").filesize)/1024/1024, 2)} MB
        Audio size: {round((yt.streams.get_by_itag(251).filesize)/1024/1024, 2)} MB
        """)

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    percentage_of_completion = round(percentage_of_completion, 2)
    print(percentage_of_completion)


def Video_downloader(url, quality, file_path, i = ""):
    yt = YouTube(url)
    yt.streams.filter(file_extension='mp4')
    stream = yt.streams.get_by_resolution(quality)  # returns type stream if the quality is available else None 
    print("Downloading...")
    if(not stream): # if the quality is available
        stream = yt.streams.get_by_resolution("720p")
        stream.download(output_path=file_path, filename_prefix=f"{i} ")
        print("Download completed")
        return
    stream.download(output_path=file_path, filename_prefix=f"{i} ")
    print("Download completed")

def Playlist_downlaoder(url, quality, file_path):
    yt = Playlist(url)
    if(len(yt.video_urls) == 1):
        Video_downloader(yt.video_urls[0])
        return
    print(f"Number of videos: {yt.length}\nTotal number of views: {yt.views:,}\nLast updated: {yt.last_updated}")

    all_some = pyip.inputMenu(["All", "Some"], "Download all or some videos: \n", numbered=True)
    if all_some == "Some":
        lower_range = pyip.inputNum("Download from video number: ", min=1, max=yt.length)
        higher_range = pyip.inputNum("to video number: ", min=lower_range, max=yt.length)
        for i in range(lower_range, higher_range+1):
            show_info(YouTube(yt.video_urls[i-1]))
            Video_downloader(yt.video_urls[i-1], quality, file_path, i)
        return 
    i = 1
    for urls in yt.video_urls:
        show_info(yt.video(i))
        Video_downloader(yt.video_urls[i-1], quality, file_path, i)
        i+=1

def extract_audio(url):
    yt = YouTube(url, on_progress_callback=on_progress)
    yt.streams.filter(only_audio=True).first()
    stream = yt.streams.get_by_itag(251)
    show_info(yt)
    file_path = pyip.inputFilepath("Save file to: ")
    print(f"Downloading audio: {yt.title}")
    stream.download(output_path=file_path)
    print("Download completed")

# start the execution of the program here
if __name__ == "__main__":
    while 1:
        vid_list = pyip.inputMenu(["Video downloader", "Playlist downlaoder", "Extract audio", "Exit"], numbered= True )
        system("cls")

        if vid_list == "Video downloader":
            url = input("Enter the video url: ")
            quality = quality_menu()
            show_info(YouTube(url))
            file_path = pyip.inputFilepath("Save file to: ")
            Video_downloader(url, quality, file_path)

        elif vid_list == "Playlist downlaoder":
            url = input("Enter the palylist url: ")
            #show_info(Playlist(url))
            quality = quality_menu()
            file_path = pyip.inputFilepath("Save file to: ")
            Playlist_downlaoder(url, quality, file_path)

        elif vid_list == "Extract audio":
            url = input("Enter the video url: ")
            extract_audio(url)
        elif vid_list == "Exit":
            exit()
        system("cls")
