from os import system
from pytube import YouTube, Playlist
import pyinputplus as pyip  # for input validation

undownloaded_vids = []
undownloaded_vids_urls = []

def quality_menu():
    return pyip.inputMenu(["360p", "480p", "720p", "1080p"], "Choose the quality: \n", numbered=True)

def show_info(yt, quality, choice):
    if choice == 1:
        print(f"""
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

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    percentage_of_completion = round(percentage_of_completion, 2)
    print(percentage_of_completion)

def undownloaded_videos(undownloaded_vids, undownloaded_vids_urls, quality, file_path):
    print(f"\nThe following videos were not downloaded because they are not available in {quality}: ")
    # print the name and url of the videos that were not downloaded
    for i in range(len(undownloaded_vids)):
        print(f"{undownloaded_vids[i]} - {undownloaded_vids_urls[i]}")
    choice = pyip.inputMenu(["Download again", "Return"], "\nDo you want to download them again? \n", numbered=True)
    if choice == "Download again":
        for i in range(len(undownloaded_vids)):
            quality = quality_menu()
            Video_downloader(undownloaded_vids_urls[i], quality, file_path)
            undownloaded_vids.remove(undownloaded_vids[i])
            undownloaded_vids_urls.remove(undownloaded_vids_urls[i])
    elif choice == "Return":
        undownloaded_vids.clear()
        undownloaded_vids_urls.clear()
        return

def Video_downloader(url, quality, file_path, i = ""):
    yt = YouTube(url)
    yt.streams.filter(file_extension='mp4')
    stream = yt.streams.get_by_resolution(quality)  # returns type stream if the quality is available else None 
    
    if not stream:
        undownloaded_vids.append(f"{i} {yt.title}")
        undownloaded_vids_urls.append(url)
        # skip and download next video
        return

    print("Downloading...")
    show_info(yt, quality, 1)
    stream.download(output_path=file_path, filename_prefix=f"{i} ")
    print("Download completed")

    

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
        higher_range = pyip.inputNum("to video number: ", min=lower_range, max=yt.length)
        for i in range(lower_range, higher_range+1):
            Video_downloader(yt.video_urls[i-1], quality, file_path, i)
    elif all_some == "All":
        for i in range(1, yt.length+1):
            Video_downloader(yt.video_urls[i-1], quality, file_path, i) 
    

def extract_audio(url):
    yt = YouTube(url, on_progress_callback=on_progress)
    yt.streams.filter(only_audio=True).first()
    stream = yt.streams.get_by_itag(251)
    show_info(yt, 3)
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
            url = pyip.inputStr("Enter the video url: ", blank=False)
            quality = quality_menu()
            file_path = pyip.inputFilepath("Save file to: ")
            Video_downloader(url, quality, file_path)

        elif vid_list == "Playlist downlaoder":
            url = pyip.inputStr("Enter the video url: ", blank=False)
            quality = quality_menu()
            file_path = pyip.inputFilepath("Save file to: ")
            Playlist_downlaoder(url, quality, file_path)

        elif vid_list == "Extract audio":
            url = input("Enter the video url: ")
            extract_audio(url)
        elif vid_list == "Exit":
            exit()
        
        while undownloaded_vids != []:      # if a video was not downloaded, ask the user if he wants to download it again
            undownloaded_videos(undownloaded_vids, undownloaded_vids_urls, quality, file_path)
        system("cls")