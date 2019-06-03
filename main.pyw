import ctypes
import os
import sys
from ctypes import wintypes

import win32con
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *

import config_parser as cfgp
import image_manager as wall


def hotkey_save_error():
    error = QMessageBox()
    error.setWindowTitle("Error")
    error.setIcon(QMessageBox.Critical)
    error.setText("There was an error saving one of your selected hotkeys. Alt or Control is not a valid "
                  "hotkey.")
    error.exec_()


class Hotkeys(QDialog):
    keymap = {}

    for key, value in vars(Qt).items():
        if isinstance(value, Qt.Key):
            keymap[value] = key.partition('_')[2]

    modmap = {
        Qt.ControlModifier: keymap[Qt.Key_Control],
        Qt.AltModifier: keymap[Qt.Key_Alt],
        Qt.ShiftModifier: keymap[Qt.Key_Shift],
    }

    # Key event manipulation from github, source lost
    def keyevent_to_string(self, event):
        sequence = []
        for modifier, text in self.modmap.items():
            if event.modifiers() & modifier:
                sequence.append(text)
        key = self.keymap.get(event.key(), event.text())
        if key not in sequence:
            sequence.append(key)
        return ' + '.join(sequence)

    def __init__(self, parent_window):
        super(Hotkeys, self).__init__()
        self.parentwin = parent_window
        self.setWindowTitle("Hotkey Configuration")
        self.setGeometry(parent_window.geometry())
        self.setWindowModality(Qt.NonModal)

        self.hotkey_list = list()
        self.seq_list = list()

        swap_label = QLabel('Swap:')
        self.swap_hotkey = QLineEdit('')
        self.swap_hotkey.installEventFilter(self)
        self.swap_seq = ""
        self.hotkey_list.append(self.swap_hotkey)
        self.seq_list.append(self.swap_seq)

        shuffle_label = QLabel('Shuffle:')
        self.shuffle_hotkey = QLineEdit('')
        self.shuffle_hotkey.installEventFilter(self)
        self.shuffle_seq = ""
        self.hotkey_list.append(self.shuffle_hotkey)
        self.seq_list.append(self.shuffle_seq)

        previous_label = QLabel('Previous:')
        self.previous_hotkey = QLineEdit('')
        self.previous_hotkey.installEventFilter(self)
        self.previous_seq = ""
        self.hotkey_list.append(self.previous_hotkey)
        self.seq_list.append(self.previous_seq)

        create_main_label = QLabel('Toggle Main Window:')
        self.create_main_hotkey = QLineEdit('')
        self.create_main_hotkey.installEventFilter(self)
        self.create_main_seq = ""
        self.hotkey_list.append(self.create_main_hotkey)
        self.seq_list.append(self.create_main_seq)

        create_images_label = QLabel('Images Window:')
        self.create_images_hotkey = QLineEdit('')
        self.create_images_hotkey.installEventFilter(self)
        self.create_images_seq = ""
        self.hotkey_list.append(self.create_images_hotkey)
        self.seq_list.append(self.create_images_seq)

        create_hotkeys_label = QLabel('Hotkeys Window:')
        self.create_hotkeys_hotkey = QLineEdit('')
        self.create_hotkeys_hotkey.installEventFilter(self)
        self.create_hotkeys_seq = ""
        self.hotkey_list.append(self.create_hotkeys_hotkey)
        self.seq_list.append(self.create_hotkeys_seq)

        time_control_label = QLabel('Timer Control:')
        self.time_control_hotkey = QLineEdit('')
        self.time_control_hotkey.installEventFilter(self)
        self.time_control_seq = ""
        self.hotkey_list.append(self.time_control_hotkey)
        self.seq_list.append(self.time_control_seq)

        self.fill_text_fields()

        self.clear_button = QPushButton('Clear')
        self.clear_button.clicked.connect(self.clear)
        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save)

        form_layout = QFormLayout()
        form_layout.addRow(swap_label, self.swap_hotkey)
        form_layout.addRow(shuffle_label, self.shuffle_hotkey)
        form_layout.addRow(previous_label, self.previous_hotkey)
        form_layout.addRow(create_main_label, self.create_main_hotkey)
        form_layout.addRow(create_images_label, self.create_images_hotkey)
        form_layout.addRow(create_hotkeys_label, self.create_hotkeys_hotkey)
        form_layout.addRow(time_control_label, self.time_control_hotkey)

        form_layout.addRow(self.clear_button, self.save_button)

        self.setLayout(form_layout)
        self.swap_hotkey.setReadOnly(True)
        self.shuffle_hotkey.setReadOnly(True)
        self.previous_hotkey.setReadOnly(True)
        self.create_main_hotkey.setReadOnly(True)
        self.create_images_hotkey.setReadOnly(True)
        self.create_hotkeys_hotkey.setReadOnly(True)
        self.time_control_hotkey.setReadOnly(True)

    def eventFilter(self, src, event):
        if src == self.swap_hotkey and \
                (event.type() == QEvent.KeyPress or event.type() == QEvent.MouseButtonPress):
            if event.type() == QEvent.MouseButtonPress:
                self.clear_styles()
                self.swap_hotkey.setStyleSheet("QLineEdit { border: 2px solid green }")
            else:
                event.ignore()
                string = self.keyevent_to_string(event)
                self.swap_hotkey.setText(string)
                self.swap_seq = string
        if src == self.shuffle_hotkey and \
                (event.type() == QEvent.KeyPress or event.type() == QEvent.MouseButtonPress):
            if event.type() == QEvent.MouseButtonPress:
                self.clear_styles()
                self.shuffle_hotkey.setStyleSheet("QLineEdit { border: 2px solid green }")
            else:
                event.ignore()
                string = self.keyevent_to_string(event)
                self.shuffle_hotkey.setText(string)
                self.shuffle_seq = string
        if src == self.previous_hotkey and \
                (event.type() == QEvent.KeyPress or event.type() == QEvent.MouseButtonPress):
            if event.type() == QEvent.MouseButtonPress:
                self.clear_styles()
                self.previous_hotkey.setStyleSheet("QLineEdit { border: 2px solid green }")
            else:
                event.ignore()
                string = self.keyevent_to_string(event)
                self.previous_hotkey.setText(string)
                self.previous_seq = string
        if src == self.create_main_hotkey and \
                (event.type() == QEvent.KeyPress or event.type() == QEvent.MouseButtonPress):
            if event.type() == QEvent.MouseButtonPress:
                self.clear_styles()
                self.create_main_hotkey.setStyleSheet("QLineEdit { border: 2px solid green }")
            else:
                event.ignore()
                string = self.keyevent_to_string(event)
                self.create_main_hotkey.setText(string)
                self.create_main_seq = string
        if src == self.create_images_hotkey and \
                (event.type() == QEvent.KeyPress or event.type() == QEvent.MouseButtonPress):
            if event.type() == QEvent.MouseButtonPress:
                self.clear_styles()
                self.create_images_hotkey.setStyleSheet("QLineEdit { border: 2px solid green }")
            else:
                event.ignore()
                string = self.keyevent_to_string(event)
                self.create_images_hotkey.setText(string)
                self.create_images_seq = string
        if src == self.create_hotkeys_hotkey and \
                (event.type() == QEvent.KeyPress or event.type() == QEvent.MouseButtonPress):
            if event.type() == QEvent.MouseButtonPress:
                self.clear_styles()
                self.create_hotkeys_hotkey.setStyleSheet("QLineEdit { border: 2px solid green }")
            else:
                event.ignore()
                string = self.keyevent_to_string(event)
                self.create_hotkeys_hotkey.setText(string)
                self.create_hotkeys_seq = string
        if src == self.time_control_hotkey and \
                (event.type() == QEvent.KeyPress or event.type() == QEvent.MouseButtonPress):
            if event.type() == QEvent.MouseButtonPress:
                self.clear_styles()
                self.time_control_hotkey.setStyleSheet("QLineEdit { border: 2px solid green }")
            else:
                event.ignore()
                string = self.keyevent_to_string(event)
                self.time_control_hotkey.setText(string)
                self.time_control_seq = string
        return False

    def clear_styles(self):
        for style in self.hotkey_list:
            style.setStyleSheet("")

    def fill_text_fields(self):
        res = cfgp.get_hotkey_text()
        try:
            self.swap_hotkey.setText(res['1'])
            self.swap_seq = res['1']
            self.shuffle_hotkey.setText(res['2'])
            self.shuffle_seq = res['2']
            self.previous_hotkey.setText(res['3'])
            self.previous_seq = res['3']
            self.create_images_hotkey.setText(res['4'])
            self.create_images_seq = res['4']
            self.create_hotkeys_hotkey.setText(res['5'])
            self.create_hotkeys_seq = res['5']
            self.time_control_hotkey.setText(res['6'])
            self.time_control_seq = res['6']
            self.create_main_hotkey.setText(res['7'])
            self.create_main_seq = res['7']
        except KeyError:
            print("No hotkey information found in hotkey_config.ini")

    def save(self):
        settings = {"1": self.swap_seq, "2": self.shuffle_seq, "3": self.previous_seq, "4": self.create_images_seq,
                    "5": self.create_hotkeys_seq, "6": self.time_control_seq, "7": self.create_main_seq}
        for seq in settings.values():
            if seq == "Alt" or seq == "Control":
                hotkey_save_error()
                self.fill_text_fields()
                for temp in self.hotkey_list:
                    temp.setStyleSheet("")
                return
        cfgp.create_hotkey_config(settings)
        for temp in self.hotkey_list:
            temp.setStyleSheet("")
        App.unregister_hotkeys(self.parentwin)
        App.hotkeys = cfgp.get_hotkeys()
        App.register_hotkeys(self.parentwin)
        App.register_hotkey_actions(self.parentwin)
        self.fill_text_fields()

    def clear(self):
        for hotkey in self.hotkey_list:
            hotkey.setText("")
        settings = {"1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": ""}
        cfgp.create_hotkey_config(settings)


class Images(QDialog):
    def __init__(self, parent_window):
        super(Images, self).__init__()
        self.setWindowTitle("Images")
        self.setGeometry(parent_window.geometry())
        self.setWindowModality(Qt.NonModal)

        self.open_left_button = QPushButton('Open in folder', self)
        self.open_left_button.clicked.connect(lambda: wall.open_left_image())

        self.open_right_button = QPushButton('Open in folder', self)
        self.open_right_button.clicked.connect(lambda: wall.open_right_image())

        self.left_picture = os.path.join(wall.home_dir, wall.image_left)
        if not os.path.exists(self.left_picture):
            self.left_picture = wall.image_left
        self.left_picture_label = QLabel(self)
        self.left_picture_label.setPixmap(QPixmap(self.left_picture).scaled(300, 170))
        self.left_picture_label.installEventFilter(self)

        self.right_picture = os.path.join(wall.home_dir, wall.image_right)
        if not os.path.exists(self.right_picture):
            self.right_picture = wall.image_right
        self.right_picture_label = QLabel(self)
        self.right_picture_label.setPixmap(QPixmap(self.right_picture).scaled(300, 170))
        self.right_picture_label.installEventFilter(self)

        main_layout = QVBoxLayout()
        layout = QHBoxLayout()
        layout.addWidget(self.open_left_button)
        layout.addWidget(self.open_right_button)
        self.layout2 = QHBoxLayout()
        self.layout2.addWidget(self.left_picture_label)
        self.layout2.addWidget(self.right_picture_label)
        main_layout.addLayout(layout)
        main_layout.addLayout(self.layout2)

        self.setLayout(main_layout)

    def change_pix(self):
        self.layout2.removeWidget(self.left_picture_label)
        self.left_picture_label.deleteLater()
        self.left_picture_label = None
        self.layout2.removeWidget(self.right_picture_label)
        self.right_picture_label.deleteLater()
        self.right_picture_label = None

        self.left_picture = os.path.join(wall.home_dir, wall.image_left)
        if not os.path.exists(self.left_picture):
            self.left_picture = wall.image_left
        self.left_picture_label = QLabel(self)
        self.left_picture_label.setPixmap(QPixmap(self.left_picture).scaled(300, 170))
        self.left_picture_label.installEventFilter(self)

        self.right_picture = os.path.join(wall.home_dir, wall.image_right)
        if not os.path.exists(self.right_picture):
            self.right_picture = wall.image_right
        self.right_picture_label = QLabel(self)
        self.right_picture_label.setPixmap(QPixmap(self.right_picture).scaled(300, 170))
        self.right_picture_label.installEventFilter(self)

        self.layout2.addWidget(self.left_picture_label)
        self.layout2.addWidget(self.right_picture_label)

    def eventFilter(self, obj, event):
        from PyQt5.Qt import QMouseEvent
        if obj == self.left_picture_label:
            if event.type() == QMouseEvent.MouseButtonPress or event.type() == QMouseEvent.MouseButtonDblClick:
                os.startfile(os.path.join(wall.home_dir, wall.image_left))
        if obj == self.right_picture_label:
            if event.type() == QMouseEvent.MouseButtonPress or event.type() == QMouseEvent.MouseButtonDblClick:
                os.startfile(os.path.join(wall.home_dir, wall.image_right))
        return False


class App(QWidget):
    timer_mode = str()
    bar_only = False
    image_window: Images
    hotkeys_window: Hotkeys
    hotkeys = cfgp.get_hotkeys()

    def __init__(self):
        super(App, self).__init__()
        myappid = u'nick.wallpaper.changer.0.0.5'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.setWindowTitle("Wallpaper Changer")
        self.setWindowIcon(QIcon('icon.png'))

        self.swap_button = QPushButton('Swap', self)
        self.swap_button.clicked.connect(self.get_wall)

        self.shuffle_button = QPushButton('Shuffle', self)
        self.shuffle_button.clicked.connect(self.shuffle_wall)

        self.shuffle_before_swap_checkbox = QCheckBox()
        self.shuffle_before_swap_checkbox.clicked.connect(lambda: self.set_wall_shuffler_status())

        self.shuffle_before_swap_label = QLabel('Shuffle before swapping')
        self.shuffle_before_swap_label.installEventFilter(self)

        self.exec_hack_button = QPushButton("Exec fade force")
        self.exec_hack_button.clicked.connect(self.exec_fade_hack)

        self.images_button = QPushButton('Images', self)
        self.images_button.clicked.connect(self.create_images_window)

        self.set_manually_button = QPushButton('Manually Set', self)
        self.set_manually_button.clicked.connect(self.set_manual)

        self.previous_button = QPushButton('Previous', self)
        self.previous_button.clicked.connect(self.previous)

        self.randomize_list_button = QPushButton('Randomize Order', self)
        self.randomize_list_button.clicked.connect(lambda: wall.randomize_image_list())

        self.set_dir_button = QPushButton('Set Directory', self)
        self.set_dir_button.clicked.connect(self.set_dir)

        self.timer = QTimer()
        self.one_percent_of_interval = 0

        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self.update_progress)

        self.timer_entry_label = QLabel('Set timer duration: ')

        self.timer_entry = QLineEdit('', self)
        self.timer_entry.returnPressed.connect(self.set_timer_handler)

        self.timer_dropdown = QComboBox()
        self.timer_dropdown.addItems(['Seconds', 'Minutes', 'Hours'])
        self.timer_dropdown.currentIndexChanged.connect(self.dropdown_handler)

        self.timer_button = QPushButton('', self)
        self.timer_button.clicked.connect(self.start_or_pause_timer)

        self.timer_interval_label = QLabel('')

        self.timer_progress_bar = QProgressBar(self)
        self.step = 0
        self.timer_progress_bar.setStyleSheet(
            "QProgressBar { border: 1px solid grey; border-radius: 0px; text-align: center; height: 5px} "
            "QProgressBar::chunk { ""background-color: #3add36; width: 1px;}")

        self.hotkeys_button = QPushButton('Hotkeys')
        self.hotkeys_button.clicked.connect(self.create_hotkeys_window)

        main_layout = QVBoxLayout()
        main_functionality_layout = QHBoxLayout()
        shuffler_option_layout = QHBoxLayout()
        utility_layout = QHBoxLayout()
        timer_layout = QHBoxLayout()
        timer_progress_layout = QHBoxLayout()

        main_functionality_layout.addWidget(self.swap_button)
        main_functionality_layout.addWidget(self.shuffle_button)
        main_functionality_layout.addWidget(self.images_button)
        main_functionality_layout.addWidget(self.set_manually_button)

        shuffler_option_layout.setAlignment(Qt.AlignLeft)
        shuffler_option_layout.addWidget(self.shuffle_before_swap_checkbox)
        shuffler_option_layout.addWidget(self.shuffle_before_swap_label)
        shuffler_option_layout.addWidget(self.exec_hack_button)

        utility_layout.addWidget(self.previous_button)
        utility_layout.addWidget(self.randomize_list_button)
        utility_layout.addWidget(self.set_dir_button)
        utility_layout.addWidget(self.hotkeys_button)

        timer_layout.addWidget(self.timer_entry_label)
        timer_layout.addWidget(self.timer_entry)
        timer_layout.addWidget(self.timer_dropdown)
        timer_layout.addWidget(self.timer_button)

        timer_progress_layout.addWidget(self.timer_interval_label)
        timer_progress_layout.addWidget(self.timer_progress_bar)

        main_layout.addLayout(main_functionality_layout)
        main_layout.addLayout(shuffler_option_layout)
        main_layout.addLayout(utility_layout)
        main_layout.addLayout(timer_layout)
        main_layout.addLayout(timer_progress_layout)

        self.setLayout(main_layout)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))

        show_action = QAction('Show', self)
        quit_action = QAction('Exit', self)
        hide_action = QAction('Hide', self)
        show_action.triggered.connect(lambda: (
            self.show(),
            self.showNormal()
        ))
        hide_action.triggered.connect(lambda: self.hide())
        quit_action.triggered.connect(lambda: (
            self.save_settings(),
            wall.save_settings(self, False),
            self.close()
        ))

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.double_click_get_wall)
        self.tray_icon.show()

        self.load_settings()

        self.image_window = Images(self)
        self.hotkeys_window = Hotkeys(self)

        self.hotkey_actions = self.register_hotkey_actions()
        self.register_hotkeys()

        self.show()
        self.testing()

    def toggle_window_visibility(self):
        if self.isVisible():
            self.hide()
        elif not self.isVisible():
            self.show()
            self.showNormal()

    @staticmethod
    def exec_fade_hack():
        os.startfile("fade.exe")

    def update_progress(self):
        if self.step >= self.one_percent_of_interval * 100:
            self.timer.stop()
            self.progress_timer.stop()
            self.get_wall()
            self.step = 0
            self.timer_progress_bar.setValue(0)
            self.timer.start()
            self.progress_timer.start()
            return
        self.step += self.one_percent_of_interval
        self.timer_progress_bar.setValue(self.step)

    def start_or_pause_timer(self):
        if self.timer.isActive():
            self.timer_button.setText('Start')
            self.timer.stop()
            self.progress_timer.stop()
        elif not self.timer.isActive():
            self.timer_button.setText('Stop')
            self.timer.start()
            self.progress_timer.start()

    def dropdown_handler(self):
        self.timer_mode = str(self.timer_dropdown.currentText())

    def set_timer_handler(self):
        converted_interval = self.convert_interval(self.timer_entry.text())
        if self.timer.isActive():
            self.one_percent_of_interval = converted_interval / 100000
            self.step = 0
            self.timer_progress_bar.setValue(0)
            self.timer_progress_bar.setMaximum(converted_interval / 1000)
            self.timer.start(converted_interval)
            self.progress_timer.start(converted_interval / 100)
        else:
            self.one_percent_of_interval = converted_interval / 100000
            self.timer_progress_bar.setMaximum(converted_interval / 1000)
            self.timer.setInterval(converted_interval)
            self.progress_timer.setInterval(converted_interval / 100)
        self.timer_entry.setText('')
        self.update_interval_label()

    def convert_interval(self, user_input):
        try:
            user_input = int(user_input)
        except ValueError:
            user_input = int(float(user_input))
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            error.setText('Your number is being converted to: ' + str(user_input))
            error.setWindowTitle('Input Error')
            error.setStandardButtons(QMessageBox.Ok)
            error.setEscapeButton(QMessageBox.Ok)
            error.show()
            error.exec_()

        result = int()
        if self.timer_mode == "Seconds":
            result = user_input * 1000
        if self.timer_mode == "Minutes":
            result = user_input * 60 * 1000
        if self.timer_mode == "Hours":
            result = user_input * 60 * 60 * 1000
        return result

    def get_wall(self):
        wall.get_wallpaper(self.swap_button)
        self.image_window.change_pix()

    def shuffle_wall(self):
        wall.shuffle(self.shuffle_button)
        self.image_window.change_pix()

    def previous(self):
        wall.previous(self.previous_button)
        self.image_window.change_pix()

    def set_dir(self):
        if self.timer.isActive():
            self.timer.stop()
            self.progress_timer.stop()
            wall.get_dir(self)
            self.timer.start()
            self.progress_timer.start()
            self.set_dir_button.setToolTip(wall.home_dir)
        else:
            wall.get_dir(self)
            self.set_dir_button.setToolTip(wall.home_dir)

    def set_wall_shuffler_status(self):
        if self.shuffle_before_swap_checkbox.isChecked():
            wall.shuffler_on = True
        else:
            wall.shuffler_on = False

    def create_images_window(self):
        self.image_window.show()

    def create_hotkeys_window(self):
        self.hotkeys_window.show()

    def double_click_get_wall(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.get_wall()

    def eventFilter(self, obj, event):
        from PyQt5.Qt import QMouseEvent
        if obj == self.shuffle_before_swap_label:
            if event.type() == QMouseEvent.MouseButtonPress or event.type() == QMouseEvent.MouseButtonDblClick:
                self.shuffle_before_swap_checkbox.click()
        return False

    def closeEvent(self, event):
        self.removeEventFilter(self)
        self.save_settings()
        wall.save_settings(self, True)

    def changeEvent(self, event):
        if event.type() == QGraphicsSceneEvent.WindowStateChange:
            if self.windowState() & QWidget.isMinimized(self):
                event.ignore()
                self.hide()

    def set_manual(self):
        from PIL import Image
        import iad_handler
        files = QFileDialog.getOpenFileNames(None, "Select image(s)", wall.home_dir)
        if len(files[0]) > wall.num_monitors:
            error = QMessageBox()
            error.setWindowTitle("Error")
            error.setText("Too many files provided")
            error.setIcon(QMessageBox.Critical)
            error.exec_()
            return
        if len(files[0]) == 0:
            return
        if len(files[0]) < wall.num_monitors:
            while len(files[0]) < wall.num_monitors:
                files[0].append(files[0][0])
        image_left = str(files[0][0])
        image_left = image_left.replace('/', '\\')
        if len(files[0]) > 1:
            image_right = str(files[0][1])
            image_right = image_right.replace('/', '\\')
            wall.image_right = image_right
        wall.image_left = image_left
        image_map = map(Image.open, files[0])
        combined_image = Image.new('RGB', wall.virtual_screensize)
        combined_image = wall.resize_images(image_map, combined_image)
        combined_image.save('test.png', quality=95)
        image_path = os.path.join(wall.working_dir, 'test.png')
        iad_handler.invoke(image_path)
        self.image_window.change_pix()

    def update_interval_label(self):
        inter = self.timer.interval() / 1000
        mode = self.timer_mode
        if mode == "Seconds":
            inter = int(inter)
        elif mode == "Minutes":
            inter = int(inter / 60)
        elif mode == "Hours":
            inter = int(inter / 60 / 60)
        if inter == 1:
            self.timer_interval_label.setText(str(int(inter)) + " " + mode[0:len(mode) - 1] + ":")
        else:
            self.timer_interval_label.setText(str(int(inter)) + " " + mode + ":")

    def save_settings(self):
        temp = {"shuffler_on": self.shuffle_before_swap_checkbox.isChecked(),
                "timer_interval": self.timer.interval(), "window_geometry": self.geometry(),
                "timer_mode": self.timer_mode, "timer_running": self.timer.isActive()}
        cfgp.create_gui_config(temp)

    def load_settings(self):
        try:
            cords = cfgp.get_geometry()
            self.setGeometry(int(cords[0]), int(cords[1]), int(cords[2]), int(cords[3]))
        except KeyError:
            self.setGeometry(300, 300, 300, 150)
        if cfgp.get_shuffler_status() == "True":
            self.shuffle_before_swap_checkbox.click()

        inter = cfgp.get_timer_interval()
        was_running = cfgp.get_timer_status()
        if was_running and inter > 0:
            self.timer.start(inter)
            self.progress_timer.start(inter / 100)
            self.one_percent_of_interval = inter / 100000
            self.timer_progress_bar.setMaximum(inter / 1000)
            self.timer_button.setText("Stop")
        elif not was_running and inter > 0:
            self.timer.setInterval(inter)
            self.progress_timer.setInterval(inter / 100)
            self.one_percent_of_interval = inter / 100000
            self.timer_progress_bar.setMaximum(inter / 1000)
            self.timer_button.setText("Start")
        timer_mode_result = cfgp.get_timer_mode_index()
        self.timer_dropdown.setCurrentIndex(timer_mode_result)
        if timer_mode_result == 0:
            self.timer_mode = "Seconds"
        if timer_mode_result == 1:
            self.timer_mode = "Minutes"
        if timer_mode_result == 2:
            self.timer_mode = "Hours"
        self.update_interval_label()
        try:
            home_dir = cfgp.get_home_dir()
            self.set_dir_button.setToolTip(home_dir)
        except KeyError:
            home_dir = os.getcwd()
            self.set_dir_button.setToolTip(home_dir)

    '''
    Ctypes hotkey code from: http://timgolden.me.uk/python/win32_how_do_i/catch_system_wide_hotkeys.html
    '''
    byref = ctypes.byref
    user32 = ctypes.windll.user32

    def register_hotkey_actions(self):
        return {
            1: self.get_wall,
            2: self.shuffle_wall,
            3: self.previous,
            4: self.create_images_window,
            5: self.create_hotkeys_window,
            6: self.start_or_pause_timer,
            7: self.toggle_window_visibility
        }

    def register_hotkeys(self):
        for h_id, (vk, modifiers) in self.hotkeys.items():
            self.user32.RegisterHotKey(None, h_id, modifiers, vk)

    def unregister_hotkeys(self):
        for hotkey in self.hotkeys.keys():
            self.user32.UnregisterHotKey(None, hotkey)

    def testing(self):
        try:
            msg = wintypes.MSG()
            while self.user32.GetMessageA(self.byref(msg), None, 0, 0) != 0:
                if msg.message == win32con.WM_HOTKEY:
                    action = self.hotkey_actions.get(msg.wParam)
                    if action:
                        self.user32.UnregisterHotKey(None, msg.wParam)
                        action()
                        self.register_hotkeys()
                self.user32.TranslateMessage(self.byref(msg))
                self.user32.DispatchMessageA(self.byref(msg))
        finally:
            self.unregister_hotkeys()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
