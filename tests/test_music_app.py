import os
import unittest
from music_app import MusicApp
from PyQt5.QtWidgets import QApplication

class TestMusicApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])
        cls.music_app = MusicApp()

    def test_model_loading(self):
        self.assertIsNotNone(self.music_app.model, "Model failed to load")

    def test_midi_generation(self):
        self.music_app.music_type_dropdown.setCurrentText("Melody")
        self.music_app.generate_music()
        self.assertIsNotNone(self.music_app.generated_sequence, "MIDI generation failed")

    def test_file_saving(self):
        self.music_app.music_type_dropdown.setCurrentText("Melody")
        self.music_app.generate_music()
        test_file_path = "test_output.mid"
        self.music_app.generated_sequence.to_midi_file(test_file_path)
        self.assertTrue(os.path.exists(test_file_path), "MIDI file was not saved")
        os.remove(test_file_path)

if __name__ == '__main__':
    unittest.main()
