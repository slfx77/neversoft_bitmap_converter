import traceback
import os
import sys
import png

from PyQt5.QtWidgets import (QTableWidgetItem, QApplication, QMainWindow, QFileDialog)
from main_window_ui import Ui_MainWindow
from printer import Printer
from rle_helper import convert
from math import ceil

printer = Printer()
printer.on = False
print_traceback = False


class Window(QMainWindow, Ui_MainWindow):
    input_dir = ""
    output_dir = ""
    current_files = []
    files_extracted = 0

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def inputBrowseClicked(self):
        options = QFileDialog.Options()
        dir_name = QFileDialog.getExistingDirectory(self, "Choose Directory", "", options=options)
        if dir_name:
            self.input_dir = dir_name
            self.current_files = []
            self.fileTable.setRowCount(0)
            self.getRleFiles(dir_name)

    def filter_rle_files(self, file_list):
        return filter(lambda file: file.split('.')[-1].upper() == 'RLE' or file.split('.')[-1].upper() == 'BMR', file_list)

    def getRleFiles(self, dir_name):
        self.inputPath.setText(dir_name)
        dir_files = [f for f in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, f))]
        rle_files = list(self.filter_rle_files(dir_files))
        if len(rle_files) > 0:
            self.fileTable.setRowCount(len(rle_files))
            for row, file in enumerate(rle_files):
                self.current_files.append(file)
                self.fileTable.setItem(row, 0, QTableWidgetItem(file))
            if self.output_dir != "":
                self.convertButton.setEnabled(True)
        else:
            self.convertButton.setEnabled(False)

    def outputBrowseClicked(self):
        options = QFileDialog.Options()
        dir_name = QFileDialog.getExistingDirectory(self, "Choose Directory", "", options=options)
        if dir_name:
            self.output_dir = dir_name
            self.outputPath.setText(dir_name)
            if len(self.current_files) > 0:
                self.convertButton.setEnabled(True)
            else:
                self.convertButton.setEnabled(False)

    def write_to_png(self, filename, img_width, img_height, pixels):
        self.files_extracted += 1
        filename_without_extension = "".join(filename.split(".")[0:-1])
        output_path = os.path.join(self.output_dir, f"{filename_without_extension}.png")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        file = open(output_path, 'wb')
        writer = png.Writer(img_width, img_height, greyscale=False, alpha=False)
        writer.write(file, pixels)
        file.close()

    def convertClicked(self):
        self.progressBar.setValue(0)
        for index, filename in enumerate(self.current_files):
            try:
                input_file = os.path.join(self.input_dir, filename)
                width = self.widthSelector.value()
                pixels = convert(input_file, width)

                self.write_to_png(filename, width, len(pixels), pixels)
                self.fileTable.setItem(index, 1, QTableWidgetItem("OK"))
            except Exception as e:
                printer("An error ocurred while trying to convert {}. The error was: {}", filename, e)
                if print_traceback:
                    traceback.print_exc()
                self.fileTable.setItem(index, 1, QTableWidgetItem("ERROR"))
            self.progressBar.setValue(round(index/len(self.current_files)*100))
        self.progressBar.setValue(100)

    def createSubDirsClicked(self):
        self.create_sub_dirs = not self.create_sub_dirs


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
