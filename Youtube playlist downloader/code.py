from os import system
from pytube import YouTube, Playlist
import pyinputplus as pyip  # for input validation
from hurry.filesize import size #To covert bytes to MB, GB, etc


def quality_menu():
    return pyip.inputMenu(["360p", "480p", "720p", "1080p"], "Choose the quality: \n", numbered=True)

def show_info(yt):
    print(f"""
        Title: {yt.title}
        Duration: {round(yt.length/60)} minutes
        Number of views: {yt.views:,} views
        Size: {size(yt.streams.first().filesize)}
        """)

def Video_downloader(url):
    yt = YouTube(url)
    yt.streams.filter(adaptive=True, file_extension='mp4')
    while 1:
        quality = quality_menu()
        stream = yt.streams.get_by_resolution(quality)  # returns type stream if the quality is available else None
        if(stream): # if the quality is available
            show_info(yt)
            file_path = pyip.inputFilepath("Save file to: ")
            print("Downloading...")
            stream.download(output_path=file_path)
            break
        else:
            print("Quality not available")
    print("Download completed")

def Download_range(url, quality, file_path, i):
    p = YouTube(url)
    p.streams.filter(adaptive=True, file_extension='mp4')
    stream = p.streams.get_by_resolution(quality)
    print(f"Downloading: ")
    show_info(p)    # show info of the video
    if not stream:
        #downlaod the video in 720p 
        stream = p.streams.get_by_resolution("720p")
        stream.download(output_path=file_path, filename=f"{i}- {p.title}")
        print(f"File downloaded") 
    else:
        stream.download(output_path=file_path, filename=f"{i}- {p.title}")
        print(f"File downloaded")

def Playlist_downlaoder(url):
    yt = Playlist(url)
    if(len(yt.video_urls) == 1):
        Video_downloader(yt.video_urls[0])
        return

    print(f"Number of videos: {yt.length}\nTotal number of views: {yt.views:,}\nLast updated: {yt.last_updated}")
    quality = quality_menu()

    file_path = pyip.inputFilepath("Save the file to: ")
    all_some = pyip.inputMenu(["All", "Some"], "Download all or some videos: \n", numbered=True)
    
    if all_some == "Some":
        lower_range = pyip.inputNum("Download from video number: ", min=1, max=yt.length)
        higher_range = pyip.inputNum("to video number: ", min=lower_range, max=yt.length)
        for i in range(lower_range, higher_range+1):
            Download_range(yt.video_urls[i-1], quality, file_path, i)
        return 

    for urls in yt.video_urls:
        p = YouTube(urls)
        p.streams.filter(adaptive=True, file_extension='mp4')
        stream = p.streams.get_by_resolution(quality)
        print("Downloading: ")
        show_info(p)
        if not stream:
            #downlaod the video in 720p 
            stream = p.streams.get_by_resolution("720p")
            stream.download(output_path=file_path, filename=f"{i}- {p.title}")
            print(f"Downloaded: {p.title}") 
        else:
            stream.download(output_path=file_path, filename= f"{i}- {p.title}")
        i+=1

def extract_audio(url):
    yt = YouTube(url)
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
            Video_downloader(url)
        elif vid_list == "Playlist downlaoder":
            url = input("Enter the palylist url: ")
            Playlist_downlaoder(url)
        elif vid_list == "Extract audio":
            url = input("Enter the video url: ")
            extract_audio(url)
        elif vid_list == "Exit":
            exit()
