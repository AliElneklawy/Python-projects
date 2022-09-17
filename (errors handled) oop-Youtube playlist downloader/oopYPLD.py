from tkinter import filedialog as fd
from tkinter.filedialog import Tk
from os import system, sys, rename
from string import punctuation
from pytube import YouTube, Playlist
import pyinputplus as pyip
import moviepy.editor as movie
from constants import *

class DowloadErr(Exception):
    pass

class Downloader:
    """
    This class is used to download videos, playlists, audios and captions from Youtube
    and covert some video formats (mkv and mp4) to mp3.

    methods:-
        _undownloaded_videos(self, undownloaded_vids_urls, file_path)

        available_captions(self, url)

        Video_downloader(self, url, quality, file_path, i="")

        Playlist_downlaoder(self, url, quality, file_path)

        download_captions(self, url, file_path, lang_code)

        extract_audio(self, url)

        converter(self, file_path, file_name)
    """
    def __init__(self) -> None:
        root = Tk()
        root.withdraw()
        root.attributes("-topmost", True)

    def __show_info(self, yt, choice, quality="720p"):
        if choice == 1:
            print(
                f"""\n
                Title: {yt.title}
                Duration: {round(yt.length/60)} minutes
                Number of views: {yt.views:,} views
                Size: {round((yt.streams.get_by_resolution(quality).filesize)/1024/1024, 2)} MB
                """
            )
        elif choice == 3:
            print(
                f"""\n
                Title: {yt.title}
                Duration: {round(yt.length/60)} minutes
                Number of views: {yt.views:,} views
                Size: {round((yt.streams.get_by_itag(251).filesize)/1024/1024, 2)} MB
                """
            )

    def __progress_function(self, chunk, file_handling, bytes_remaining):
        """
        method to show the progress of the download
        """
        global filesize
        filesize = chunk.filesize
        current = (filesize - bytes_remaining) / filesize
        percent = ("{0:.1f}").format(current * 100)
        progress = int(50 * current)
        status = "█" * progress + "-" * (50 - progress)
        if bytes_remaining == 0:
            status = "\033[92m" + status + "\033[0m"
        sys.stdout.write(" ↳ |{bar}| {percent}%\r".format(bar=status, percent=percent))
        sys.stdout.flush()


    def _undownloaded_videos(self, undownloaded_vids_urls, file_path):
        """
        Videos that were not downloaded for any reason will be handeled here
        undownloaded_vids: list of the names of the undownloaded videos
        undownloaded_vids_urls: list of the URLs of the undownloaded videos
        """
        choice = pyip.inputMenu(
            ["Re-download the videos that were not downloaded", "Return"],
            "\nDo you want to download them again? \n",
            numbered=True,
        )
        if choice == "Re-download the videos that were not downloaded":
            i = -1
            while undownloaded_vids_urls != deque([]):
                check = self.Video_downloader(
                    undownloaded_vids_urls[0][0],
                    Qualities[i],
                    file_path,
                    undownloaded_vids_urls[0][1],
                )
                if check == 1:
                    undownloaded_vids_urls.pop()
                    i -= 1
                    if i == -5:
                        print(
                            f"Could not download: {YouTube(undownloaded_vids_urls[0][0]).title}"
                        )
                        undownloaded_vids_urls.popleft()
                        i = -1
                else:
                    undownloaded_vids_urls.popleft()
                    i = -1
        elif choice == "Return":
            undownloaded_vids_urls.clear()
            return

    def available_captions(self, url):
        """
        Check if there are captions available for the video
        :param url: url of the youtube video
        """
        yt = YouTube(url)
        cap = yt.captions
        langs = {}
        for capt in cap:
            if "(auto-generated)" in capt.name:
                continue
            langs.update({capt.name: capt.code})
        if len(langs) > 0:
            lang = pyip.inputMenu(
                list(langs.keys()), "Choose a language: \n", numbered=True
            )
            return langs[lang]
        return False

    def Video_downloader(self, url, quality, save_path, i=""):
        """
        Download videos from youtube
        :param url: URL of the video
        :param quality: the quality chosen by the user
        :param save_path: the file path to save the files
        :param i: used to number the videos when downloading playlists,
            default = "" for downloading one video
        """
        yt = YouTube(url, on_progress_callback=self.__progress_function)
        yt.streams.filter(progressive=True, file_extension="mp4").all()
        stream = yt.streams.get_by_resolution(quality)
        if not stream:
            undownloaded_vids_urls.append([url, i])
            print(
                f"Could not download video: {yt.title}. Quality {quality} not available."
            )
            return 1

        self.__show_info(yt, 1, quality)
        stream.download(
            output_path=save_path, filename_prefix="" if i == "" else f"{i} "
        )
        return 2

    def Playlist_downlaoder(self, url, quality, save_path):
        """
        Download playlists from youtube
        :param url: URL of the playlist
        :param quality: the quality chosen by the user
        :param save_path: the file path to save the files
        """
        yt = Playlist(url)

        if len(yt.video_urls) == 1:
            self.Video_downloader(yt.video_urls[0], quality, save_path, i=1)
            return

        print(
            f"""
            Number of videos: {yt.length}
            Total number of views: {yt.views}
            Last updated: {yt.last_updated}
        """
        )

        higher_range = ""
        lower_range = 1
        all_some = pyip.inputMenu(
            ["All", "Some"], "Download all or some videos: \n", numbered=True
        )
        if all_some == "Some":
            lower_range = pyip.inputNum(
                "Download from video number: ", min=1, max=yt.length
            )
            higher_range = pyip.inputNum(
                "to video number (leave it blank to download till the last video): ",
                min=lower_range + 1,
                max=yt.length,
                blank=True,
            )

        for i in range(
            lower_range, yt.length + 1 if higher_range == "" else higher_range + 1
        ):
            self.Video_downloader(yt.video_urls[i - 1], quality, save_path, i)

    def download_captions(self, url, save_path, lang_code):
        """
        Download captions from youtube
        :param url: URL of the video
        :param save_path: the file path to save the file
        """
        yt = YouTube(url)
        try:
            caption = yt.captions[lang_code]
        except KeyError:
            raise DowloadErr("Couldn't download subtitle. Maybe it's auto-generated")
        caption.generate_srt_captions()
        caption.download(title=yt.title, output_path=save_path)
        oldname = save_path + "/" + yt.title + " (" + lang_code + ")" + ".srt"
        newname = save_path + "/" + yt.title + ".srt"

        try:
            rename(oldname, newname)
        except:
            invalid_chars = punctuation
            if any(char in invalid_chars for char in yt.title):
                newname = (
                    save_path
                    + "/"
                    + yt.title.translate(str.maketrans("", "", invalid_chars))
                    + ".srt"
                )
                oldname = (
                    save_path
                    + "/"
                    + yt.title.translate(str.maketrans("", "", invalid_chars))
                    + " ("
                    + lang_code
                    + ")"
                    + ".srt"
                )
                try:
                    rename(oldname, newname)
                except (WindowsError, OSError, IOError):
                    raise DowloadErr("Could not rename the file. Maybe, the file already exists. Rename it manually.")

    def extract_audio(self, url, save_path):
        """
        Download audio from youtube
        :param url: the url of the youtube video
        """
        yt = YouTube(url, on_progress_callback=self.__progress_function)
        yt.streams.filter(only_audio=True).first()
        stream = yt.streams.get_by_itag(251)
        self.__show_info(yt, 3)
        print(f"Downloading audio: {yt.title}")
        stream.download(output_path=save_path)

    def converter(self, file_path, file_name):
        """ convert mp4 or mkv to mp3 """
        clip = movie.VideoFileClip(file_path)
        save_file = fd.askdirectory(title="Save")
        clip.audio.write_audiofile(f"{save_file}/{file_name}.mp3")
        clip.close()
        print("Conversion completed")
