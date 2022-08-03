from os import system
from pytube import YouTube, Playlist
import pyinputplus as pyip  # for input validation
from langdetect import detect

def Video_downloader(url):
    system("cls")
    yt = YouTube(url)
    print(f"Title: {yt.title}\nDuration: {round(yt.length/60)} minutes\nNumber of views: {yt.views} views")
    yt.streams.filter(adaptive=True, file_extension='mp4')
    while 1:
        quality = pyip.inputMenu(["240p", "360p", "480p", "720p", "1080p"], "Choose the quality: \n", numbered=True)
        stream = yt.streams.get_by_resolution(quality)  # returns type stream if the quality is available else None
        if(stream): # if the quality is available
            file_path = pyip.inputFilepath("Enter the file path: ")
            print("Downloading...")
            stream.download(output_path=file_path)
            break
        else:
            print("Quality not available")
    print("Download completed")

def Playlist_downlaoder(url):
    system("cls")
    yt = Playlist(url)
    if(len(yt.video_urls) == 1):
        Video_downloader(yt.video_urls[0])
        return
    print(f"Number of videos: {yt.length}\nTtal number of views: {yt.views:,}\nLast updated: {yt.last_updated}")
    quality = pyip.inputMenu(["240p", "360p", "480p", "720p", "1080p"], "Choose the quality: \n", numbered=True)
    file_path = pyip.inputFilepath("Enter the file path: ")
    i=1
    for urls in yt.video_urls:
        p = YouTube(urls)
        p.streams.filter(adaptive=True, file_extension='mp4')
        stream = p.streams.get_by_resolution(quality)
        print(f"Downloading: {p.title}")
        if not stream:
            #downlaod the video in 720p 
            stream = p.streams.get_by_resolution("720p")
            stream.download(output_path=file_path, filename=f"{i}- {p.title}")
            print(f"Downloaded: {p.title}") 
        else:
            stream.download(output_path=file_path, filename= f"{i}- {p.title}")
        i+=1


# start the execution of the program here
if __name__ == "__main__":
    while 1:
        vid_list = pyip.inputMenu(["Video downloader", "Playlist downlaoder", "Extract audio", "Exit"], numbered= True )
        if vid_list == "Video downloader":
            url = input("Enter the video url: ")
            Video_downloader(url)
        elif vid_list == "Playlist downlaoder":
            url = input("Enter the palylist url: ")
            Playlist_downlaoder(url)


        elif vid_list == "Exit":
            exit()



    #call main function to start the program execution again
