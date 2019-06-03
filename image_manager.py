from __future__ import print_function

import ctypes
import os
import random
import subprocess
import sys
import threading
import time

import wmi
from PIL import Image

import config_parser as cfgp


def get_images():
    files = os.listdir(home_dir)
    random.shuffle(files)
    return files


try:
    home_dir = str(cfgp.get_home_dir()).replace('/', '\\')
    image_index = cfgp.get_image_index()
    images = cfgp.get_images()
    image_left = images[image_index - 2]
    image_right = images[image_index - 1]
    if int(cfgp.get_shuffle_counter()) == 1:
        image_left = images[image_index - 1]
        image_right = images[image_index - 2]
    virtual_screensize = cfgp.get_virtual_size()
    num_monitors = cfgp.get_num_monitors()
    mon_info = cfgp.get_mon_info()
except KeyError:
    home_dir = str(os.getcwd()).replace('/', '\\')
    image_index = 0
    images = get_images()
    image_left = str()
    image_right = str()
    obj = wmi.WMI().Win32_PnPEntity(ConfigManagerErrorCode=0)
    displays = [x for x in obj if 'MONITOR' in str(x)]
    virtual_screensize = ctypes.windll.user32.GetSystemMetrics(78), ctypes.windll.user32.GetSystemMetrics(79)
    num_monitors = len(displays)
    from screeninfo import get_monitors
    mon_info = list()
    count = 0
    for m in get_monitors():
        mon_info.append((count, m.width, m.height))
        count += 1

shuffler_on = bool()
shuffle_counter = 0
working_dir = os.getcwd()
thread_active = bool()


def randomize_image_list():
    global image_index
    random.shuffle(images)
    image_index = 0


def compute_average_image_color(img):
    img = img.resize((100, 100))
    width, height = img.size
    r_total = 0
    g_total = 0
    b_total = 0
    counter = 0
    for x in range(0, width):
        for y in range(0, height):
            try:
                if img.mode == 'RGBA':
                    r, g, b, a = img.getpixel((x, y))
                else:
                    r, g, b = img.getpixel((x, y))
            # Possibly happening on only black and white images...
            except TypeError:
                return 0, 0, 0
            r_total += r
            g_total += g
            b_total += b
            counter += 1
    return int(r_total / counter), int(g_total / counter), int(b_total / counter)


def open_left_image():
    global image_left, home_dir
    subprocess.Popen(r'explorer /select,"' + os.path.join(home_dir, image_left) + '"')


def open_right_image():
    global image_right, home_dir
    subprocess.Popen(r'explorer /select,"' + os.path.join(home_dir, image_right) + '"')


def get_dir(app):
    from PyQt5.QtWidgets import QFileDialog as fd
    global home_dir, image_index, image_left, image_right, images, shuffle_counter
    potential_home_dir = str(fd.getExistingDirectory(None, "Select Directory", home_dir)).replace('/', '\\')
    if len(potential_home_dir) != 0:
        home_dir = potential_home_dir
        image_index = 0
        image_left = ""
        image_right = ""
        images = list()
        images = get_images()
        shuffle_counter = 1
        save_settings(app, False)


def previous(button=None):
    global image_index, images, shuffle_counter, shuffler_on
    if image_index < 4:
        return
    image_index -= 4
    shuffle_counter = 0
    shuffler_status_backup = shuffler_on
    shuffler_on = False
    get_wallpaper(button)
    shuffler_on = shuffler_status_backup


def resize_images(image_map_input, combined_image_input):
    x_offset = 0
    iteration = 0
    for im in image_map_input:
        monitor = mon_info[num_monitors - 1 - iteration]
        mon_width = monitor[1]
        mon_height = monitor[2]
        if im.height > im.width:
            im.thumbnail((mon_width, mon_height), Image.BILINEAR)
            most_common_color = compute_average_image_color(im)
            temp_offset = int((mon_width - im.width) / 2)
            combined_image_input.paste(most_common_color, (x_offset, 0, x_offset + mon_width, mon_height))
            combined_image_input.paste(im, (x_offset + temp_offset, 0))
        else:
            base_width = mon_width
            width_percent = (base_width / float(im.size[0]))
            height_size = int((float(im.size[1]) * float(width_percent)))
            im = im.resize((base_width, height_size), Image.BILINEAR)
            half_of_extra_height_pixels = (im.size[1] - mon_height) / 2
            im = im.crop((0, half_of_extra_height_pixels, im.size[0], im.size[1] - half_of_extra_height_pixels))
            combined_image_input.paste(im, (x_offset, 0))
        iteration += 1
        x_offset += mon_width
    return combined_image_input


def get_wallpaper(button=None):
    import iad_handler as iad_handler

    def thread_work():
        global image_index, image_left, image_right, images, thread_active, images, shuffle_counter, shuffler_on, \
            virtual_screensize
        if button:
            button.setDisabled(True)
        if shuffler_on:
            if shuffle_counter < 1:
                shuffle(button)
                shuffle_counter += 1
                return
            if shuffle_counter == 1:
                shuffle_counter = 0

        thread_active = True
        if image_index + 1 >= len(images):
            image_index = 0
            random.shuffle(images)
        image_map = map(Image.open,
                        [os.path.join(home_dir, images[image_index]),
                         os.path.join(home_dir, images[image_index + 1])])
        image_left = images[image_index]
        image_right = images[image_index + 1]
        image_index += 2

        try:
            combined_image = Image.new('RGB', virtual_screensize)
            combined_image = resize_images(image_map, combined_image)
            combined_image.save('test.png', quality=95)
        except OSError:
            eprint("OS error occurred")
            eprint("Please use a higher timer interval")
            time.sleep(2.5)
            combined_image = Image.new('RGB', virtual_screensize)
            combined_image = resize_images(image_map, combined_image)
            combined_image.save('test.png', quality=95)
        thread_active = False

        if button:
            button.setDisabled(False)

        image_path = os.path.join(working_dir, 'test.png')
        iad_handler.invoke(image_path)

    if not thread_active:
        threading.Thread(target=thread_work, name="Changing_Thread").start()


def shuffle(button=None):
    import iad_handler as iad_handler

    def thread_work():
        global image_index, image_left, image_right, home_dir, thread_active, working_dir
        if button:
            button.setDisabled(True)

        thread_active = True
        image_map = map(Image.open, [os.path.join(home_dir, image_left), os.path.join(home_dir, image_right)])

        try:
            combined_image = Image.new('RGB', virtual_screensize)
            combined_image = resize_images(image_map, combined_image)
            combined_image.save('test.png')
        except OSError:
            eprint("OS error occurred")
            eprint("Please use a higher timer interval")
            time.sleep(2.5)
            combined_image = Image.new('RGB', virtual_screensize)
            combined_image = resize_images(image_map, combined_image)
            combined_image.save('test.png', quality=95)

        if button:
            button.setDisabled(False)

        thread_active = False
        image_path = os.path.join(working_dir, 'test.png')
        iad_handler.invoke(image_path)

    if not thread_active:
        global image_left, image_right
        temp = image_left
        image_left = image_right
        image_right = temp
        threading.Thread(target=thread_work).start()


def save_settings(application, exiting):
    temp = {"home_dir": home_dir, "images": images, "image_index": image_index, "shuffle_counter": shuffle_counter,
            "num_monitors": num_monitors, "virtual_screensize": virtual_screensize, "mon_info": mon_info}
    cfgp.create_config(temp)
    if exiting:
        application.destroy()
        sys.exit(0)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
