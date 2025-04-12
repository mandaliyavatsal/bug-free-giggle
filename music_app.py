import sys
import os
import gc
import tensorflow as tf
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QComboBox, QFileDialog, QMessageBox
from magenta.models.music_vae import TrainedModel
from magenta.models.music_vae.configs import configs
import pretty_midi

class MusicApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.model = None
        self.load_model()

    def initUI(self):
        self.setWindowTitle('Music Generator')
        self.setGeometry(100, 100, 300, 200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.music_type_dropdown = QComboBox()
        self.music_type_dropdown.addItem("Melody")
        self.music_type_dropdown.addItem("Drums")
        layout.addWidget(self.music_type_dropdown)

        self.generate_button = QPushButton('Generate Music')
        self.generate_button.clicked.connect(self.generate_music)
        layout.addWidget(self.generate_button)

        self.save_button = QPushButton('Save Music')
        self.save_button.clicked.connect(self.save_music)
        layout.addWidget(self.save_button)

        central_widget.setLayout(layout)

    def load_model(self):
        try:
            tf.config.experimental.set_memory_growth(tf.config.experimental.list_physical_devices('GPU')[0], True)
            self.model = TrainedModel(
                configs['cat-mel_2bar_small'],
                batch_size=1,
                checkpoint_dir_or_path='models/cat-mel_2bar_small'
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load model: {e}")

    def generate_music(self):
        try:
            music_type = self.music_type_dropdown.currentText()
            if music_type == "Melody":
                z = self.model.sample(n=1, length=32, temperature=0.9)
            elif music_type == "Drums":
                z = self.model.sample(n=1, length=32, temperature=0.9)
            self.generated_sequence = z[0]
            QMessageBox.information(self, "Success", "Music generated successfully!")
            gc.collect()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate music: {e}")

    def save_music(self):
        try:
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Music", "", "MIDI Files (*.mid);;All Files (*)", options=options)
            if file_name:
                self.generated_sequence.to_midi_file(file_name)
                QMessageBox.information(self, "Success", "Music saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save music: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MusicApp()
    ex.show()
    sys.exit(app.exec_())
