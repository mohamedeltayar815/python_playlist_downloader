import sys
import PySide6 as PySide6
from PySide6.QtCore import *
from PySide6.QtWidgets import *
import pytube as pt
from pytube import *


class DownloadThread(QThread):
    # Signals to communicate with the main thread
    video_downloaded = Signal(str)
    error_occurred = Signal(str)

    def __init__(self, playlist_url, output_path):
        super().__init__()
        self.playlist_url = playlist_url
        self.output_path = output_path

    def run(self):
        try:
            # Create a Playlist object
            playlist = Playlist(self.playlist_url)

            # Iterate over each video in the playlist
            for video_url in playlist.video_urls:
                try:
                    # Create a YouTube object for the video
                    video = pt.YouTube(video_url)

                    # Download the highest resolution video available
                    stream = video.streams.get_highest_resolution()
                    video_title = video.title

                    # Emit signal to notify the video download
                    self.video_downloaded.emit(video_title)

                    stream.download(output_path=self.output_path)

                except Exception as e:
                    # Emit signal to notify the error
                    self.error_occurred.emit(f"استنى بحاول تانى  {video_url}: {str(e)}")

        except Exception as e:
            # Emit signal to notify the error
            self.error_occurred.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("mohamed eltayar   ")
        
        
       
        self.playlist_input = QLineEdit()
        self.playlist_label = QLabel(" pl url")
        self.output_input = QLineEdit()
        self.output_label = QLabel("location url")
        self.download_button = QPushButton("حمل")
        self.log_output = QTextEdit()

        layout = QVBoxLayout()
        form_layout = QHBoxLayout()
        form_layout.addWidget(self.playlist_label)
        form_layout.addWidget(self.playlist_input)
        form_layout.addWidget(self.output_label)
        form_layout.addWidget(self.output_input)
        layout.addLayout(form_layout)
        layout.addWidget(self.download_button)
        layout.addWidget(self.log_output)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.download_button.clicked.connect(self.start_download)

    def start_download(self):
        playlist_url = self.playlist_input.text()
        output_path = self.output_input.text()

        # Create and start the download thread
        self.thread = DownloadThread(playlist_url, output_path)
        self.thread.video_downloaded.connect(self.log_output.append)
        self.thread.error_occurred.connect(self.log_output.append)
        self.thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


    