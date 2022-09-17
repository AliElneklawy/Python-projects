from time import sleep
from oopYPLD import *

oDownloader = Downloader()


def quality_menu():
    """ Display a menu of available qualities """
    return pyip.inputMenu(Qualities, "Choose the quality: \n", numbered=True)


while True:
    vid_list = pyip.inputMenu(
        [
            "Video downloader",
            "Playlist downlaoder",
            "Download captions",
            "Extract audio",
            "Video to audio converter",
            "Exit",
        ],
        numbered=True,
    )
    system("cls")

    if vid_list == "Video downloader":
        url = pyip.inputStr("Enter the url: ", blank=False)
        quality = quality_menu()
        file_path = fd.askdirectory(title="Save")
        oDownloader.Video_downloader(url, quality, file_path)

    elif vid_list == "Playlist downlaoder":
        url = pyip.inputStr("Enter the url: ", blank=False)
        quality = quality_menu()
        file_path = fd.askdirectory(title="Save")
        oDownloader.Playlist_downlaoder(url, quality, file_path)

    elif vid_list == "Download captions":
        url = pyip.inputStr("Enter the video url: ", blank=False)
        file_path = fd.askdirectory(title="Save")
        lang = oDownloader.available_captions(url)
        oDownloader.download_captions(url, file_path, lang)

    elif vid_list == "Extract audio":
        url = input("Enter the video url: ")
        oDownloader.extract_audio(url)

    elif vid_list == "Video to audio converter":
        file_path = fd.askopenfilename(
            title="Select a file",
            filetypes=[("mkv files", "*.mkv"), ("MP4 files", "*.mp4")],
        )
        file_name = tuple(file_path.split("/"))[-1]
        file_name = (
            file_name.removesuffix(".mp4")
            if file_name.endswith(".mp4")
            else file_name.removesuffix(".mkv")
        )
        oDownloader.converter(file_path, file_name)

    elif vid_list == "Exit":
        sys.exit()

    if undownloaded_vids_urls != deque([]):
        oDownloader._undownloaded_videos(undownloaded_vids_urls, file_path)

    sleep(2)
    system("cls")
