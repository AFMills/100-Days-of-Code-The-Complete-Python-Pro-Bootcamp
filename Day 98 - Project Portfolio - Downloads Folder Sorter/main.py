import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import download_sorter
from threading import Thread


class OnMyWatch:
    def __init__(self, watch_directory, file_types):
        self.observer = Observer()
        self.watch_directory = watch_directory
        self.file_types = file_types
        self.create_destination_folder()

    def create_destination_folder(self):
        for ftype in self.file_types:
            dest_dir = os.path.join(self.watch_directory, ftype)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

    def move_files(self, dir_list):
        for file in dir_list:
            file_name, file_ext = os.path.splitext(file)
            for ftype, extensions in self.file_types.items():
                if file_ext.lower() in extensions:
                    dest_dir = os.path.join(self.watch_directory, ftype)
                    try:
                        shutil.move(os.path.join(self.watch_directory, file), os.path.join(dest_dir, file))
                        print(f"Moved {file} to {ftype} folder.")
                    except Exception as e:
                        print(f"Error moving {file} to {ftype} folder: {e}")
                    break

    def run(self):
        event_handler = Handler(self.watch_directory, self.file_types)
        self.observer.schedule(event_handler, self.watch_directory, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")
        self.observer.join()


class Handler(FileSystemEventHandler):
    def __init__(self, watch_directory, file_types):
        self.watch_directory = watch_directory
        self.file_types = file_types

    def on_created(self, event):
        if event.is_directory:
            return
        src_path = event.src_path
        file_name = os.path.basename(src_path)
        file_ext = os.path.splitext(file_name)[1].lower()
        for ftype, extensions in self.file_types.items():
            if file_ext in extensions:
                dest_dir = os.path.join(self.watch_directory, ftype)
                try:
                    shutil.move(src_path, os.path.join(dest_dir, file_name))
                    print(f"Moved {file_name} to {ftype} folder.")
                except Exception as e:
                    print(f"Error moving {file_name} to {ftype} folder: {e}")
                break


if __name__ == '__main__':
    downloads_dir = "downloads dir"
    file_types = {
        'videos': ['.avi', '.mpg', '.mp4', '.mov', '.wmv', '.mkv'],
        'audio': ['.mp3', '.wav', '.aac', '.ogg', '.flac'],
        'documents': ['.doc', '.docx', '.pdf', '.txt', '.rtf', '.csv', '.odt', '.xlsx', '.xls', '.pptx', '.ppt',
                      '.ods'],
        'archive': ['.zip', '.rar', '.7z', '.tar', '.gz'],
        'torrent': ['.torrent'],
        'apps': ['.exe', '.dmg', '.app', '.deb', '.rpm', '.msi'],
        'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'],
        'programming': ['.py', '.ipynb', '.r', '.rdata', '.php', '.sql', '.html', '.js']
    }
    watch = OnMyWatch(downloads_dir, file_types)
    dir_list = os.listdir(downloads_dir)

    watch.move_files(dir_list)
    watch.run()

gui.py


# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# new check-able combo box
class CheckableComboBox(QComboBox):

    # constructor
    def __init__(self, parent=None):
        super(CheckableComboBox, self).__init__(parent)
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QStandardItemModel(self))
        self.file_types = {}
        self.extensions = {
            'videos': ['.avi', '.mpg', '.mp4', '.mov', '.wmv', '.mkv'],
            'audio': ['.mp3', '.wav', '.aac', '.ogg', '.flac'],
            'documents': ['.doc', '.docx', '.pdf', '.txt', '.rtf', '.csv', '.odt', '.xlsx', '.xls', '.pptx', '.ppt',
                          '.ods'],
            'archive': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'torrent': ['.torrent'],
            'apps': ['.exe', '.dmg', '.app', '.deb', '.rpm', '.msi'],
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'],
            'programming': ['.py', '.ipynb', '.r', '.rdata', '.php', '.sql', '.html', '.js']
        }

        self.clear()
        for item, _ in self.extensions.items():
            self.addItem(item)
            self.model().item(self.count() - 1).setCheckState(Qt.Checked)
            self.file_types = {item: self.extensions[item] for item in self.extensions}
        print(self.file_types)

        # action called when item get checked

    def do_action(self):
        checked_items = []
        for index in range(self.count()):  # Loop through all items in the combo box
            item = self.itemText(index)
            if self.itemData(index, Qt.CheckStateRole) == Qt.Checked:
                checked_items.append(item)
        self.file_types = {item: self.extensions[item] for item in
                           checked_items}  # Create dictionary entry for each checked item
        print(self.file_types)

        # when any item get pressed

    def handleItemPressed(self, index):

        # getting the item
        item = self.model().itemFromIndex(index)

        # checking if item is checked
        if item.checkState() == Qt.Checked:

            # making it unchecked
            item.setCheckState(Qt.Unchecked)

            # if not checked
        else:
            # making the item checked
            item.setCheckState(Qt.Checked)

            # call the action
        self.do_action()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Sorter")
        self.setGeometry(100, 100, 400, 100)
        self.setWindowIcon(QIcon(resource_path('icon.ico')))

        layout = QGridLayout()
        self.setLayout(layout)

        choose_dir = QPushButton('Browse')
        choose_dir.clicked.connect(self.open_dir_dialog)
        self.name_edit = QLineEdit()
        self.directory = ''

        layout.addWidget(QLabel('Directory:'), 0, 0)
        layout.addWidget(self.name_edit, 0, 1)
        layout.addWidget(choose_dir, 0, 2)

        self.combo_box = CheckableComboBox()
        self.combo_box.addItems([])
        self.label = QLabel("File Types:", self)
        layout.addWidget(self.combo_box, 1, 1)
        layout.addWidget(self.label, 1, 0)

        sort_dir = QPushButton('Sort Directory')
        sort_dir.clicked.connect(self.sort_files)
        layout.addWidget(sort_dir, 2, 0)

        check_label = QLabel("Monitor:")
        monitor = QCheckBox()
        monitor.clicked.connect(self.monitor_dir)
        layout.addWidget(check_label, 2, 1)
        layout.addWidget(monitor, 2, 2)

        self.watch = None

        # Initialize system tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(resource_path("icon.ico")))

        # Create context menu
        self.tray_menu = QMenu(self)
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show_window)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.exit_application)
        sort_action = QAction("Sort", self)
        sort_action.triggered.connect(self.sort_files)
        monitor_action = QAction("Monitor", self)
        monitor_action.triggered.connect(self.monitor_dir)
        self.tray_menu.addAction(show_action)
        self.tray_menu.addAction(sort_action)
        self.tray_menu.addAction(monitor_action)
        self.tray_menu.addAction(exit_action)

        # Set context menu
        self.tray_icon.setContextMenu(self.tray_menu)

        # Connect activated signal
        self.tray_icon.activated.connect(self.tray_icon_activated)

        # Show the system tray icon
        self.tray_icon.show()

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.showNormal()

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.isMinimized():
                self.hide()
                event.ignore()  # Ignore the event to prevent the window from being minimized to the taskbar

    def show_window(self):
        self.show()

    def exit_application(self):
        self.tray_icon.hide()
        qApp.quit()

    def open_dir_dialog(self):
        dir_name = QFileDialog.getExistingDirectory(self, "Select a Directory")
        if dir_name:
            self.directory = dir_name
            self.name_edit.setText(self.directory)

    def sort_files(self):
        if self.directory:
            dir_list = os.listdir(self.directory)
            self.watch = download_sorter.OnMyWatch(self.directory, self.combo_box.file_types)
            self.watch.move_files(dir_list)
        else:
            QMessageBox.warning(self, "Warning", "Please select a directory before sorting.")

    def monitor_dir(self):
        if self.watch is not None:
            monitor_thread = Thread(target=self.watch.run)
            monitor_thread.daemon = True  # Daemonize the thread to stop it when the main program exits
            monitor_thread.start()
        else:
            QMessageBox.warning(self, "Warning", "Please sort files before starting monitoring.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())