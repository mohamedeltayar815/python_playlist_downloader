import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock ,Mock
from PySide6.QtWidgets import QApplication  # Import QApplication
from Playlist import MainWindow ,DownloadThread


class TestDownloadThread(unittest.TestCase):
    def test_run_downloads_videos(self):
        # Mock Playlist object and its methods
        playlist_mock = Mock()
        playlist_mock.video_urls = ["video_url_1", "video_url_2"]

        # Mock YouTube object and its methods
        youtube_mock = Mock()
        youtube_mock.title = "Video Title"
        stream_mock = Mock()
        stream_mock.download.return_value = None
        youtube_mock.streams.get_highest_resolution.return_value = stream_mock

        # Patching external dependencies
        with patch('Playlist.Playlist', return_value=playlist_mock), \
             patch('pytube.YouTube', return_value=youtube_mock):

            # Initialize DownloadThread
            playlist_url = "https://www.example.com/playlist"
            output_path = "/path/to/save/videos"
            download_thread = DownloadThread(playlist_url, output_path)

            # Mock signal emitters
            video_downloaded_signal = Mock()
            error_occurred_signal = Mock()
            download_thread.video_downloaded.connect(video_downloaded_signal)
            download_thread.error_occurred.connect(error_occurred_signal)

            # Call run method
            download_thread.run()

            # Assertions
            self.assertEqual(video_downloaded_signal.call_count, 2)  # Two videos in playlist
            self.assertEqual(error_occurred_signal.call_count, 0)    # No errors occurred

            # Assert that signals were emitted with correct arguments
            video_downloaded_signal.assert_any_call("Video Title")
            self.assertFalse(error_occurred_signal.called)  # No errors emitted



class TestMainWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize QApplication instance
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication([])

    @classmethod
    def tearDownClass(cls):
        # Clean up QApplication instance
        del cls.app

    def test_widgets_initialized_correctly(self):
        # Initialize MainWindow
        window = MainWindow()

        # ... (rest of your existing test)

    @patch('Playlist.DownloadThread')  # Adjust the module name here
    def test_start_download(self, mock_download_thread):
        # Initialize MainWindow
        window = MainWindow()

        # Set up mock objects
        mock_thread_instance = MagicMock()
        mock_download_thread.return_value = mock_thread_instance

        # Set up input values
        playlist_url = "https://www.example.com/playlist"
        output_path = "/path/to/save/videos"

        # Set input values in QLineEdit widgets
        window.playlist_input.setText(playlist_url)
        window.output_input.setText(output_path)

        # Click the download button
        window.start_download()

        # Assert that DownloadThread was created with correct arguments
        mock_download_thread.assert_called_once_with(playlist_url, output_path)

        # Assert that signals are connected and start method is called
        mock_thread_instance.video_downloaded.connect.assert_called_once_with(window.log_output.append)
        mock_thread_instance.error_occurred.connect.assert_called_once_with(window.log_output.append)
        mock_thread_instance.start.assert_called_once()

if __name__ == '__main__':
    unittest.main()
