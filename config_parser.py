import configparser

import win32con


def create_config(settings):
    configfile = open("config.ini", "w")
    cfg = configparser.ConfigParser()
    cfg["Settings"] = {"home_dir": settings['home_dir'], "images": ",".join(settings["images"]),
                       "image_index": settings["image_index"], "shuffle_counter": settings["shuffle_counter"],
                       "num_monitors": settings["num_monitors"], "virtual_screensize": settings["virtual_screensize"],
                       "mon_info": settings["mon_info"]}
    cfg.write(configfile)
    configfile.close()


def create_gui_config(settings):
    configfile2 = open("gui_config.ini", "w")
    cfg_gui = configparser.ConfigParser()
    cfg_gui["Settings"] = {"shuffler_on": settings["shuffler_on"], "timer_interval": settings["timer_interval"],
                           "window_geometry": settings["window_geometry"], "timer_mode": settings["timer_mode"],
                           "timer_running": settings["timer_running"]}
    cfg_gui.write(configfile2)
    configfile2.close()


def create_hotkey_config(settings):
    configfile3 = open("hotkey_config.ini", "w")
    cfg_hotkey = configparser.ConfigParser()
    cfg_hotkey["Hotkeys"] = {"1": settings["1"], "2": settings["2"], "3": settings["3"], "4": settings["4"],
                             "5": settings["5"], "6": settings["6"], "7": settings["7"]}
    cfg_hotkey.write(configfile3)
    configfile3.close()


def get_home_dir():
    cfg = configparser.ConfigParser()
    cfg.read("config.ini")
    return cfg["Settings"]["home_dir"]


def get_mon_info():
    cfg = configparser.ConfigParser()
    cfg.read("config.ini")
    from ast import literal_eval as make_list
    return make_list(cfg["Settings"]["mon_info"])


def get_image_index():
    cfg = configparser.ConfigParser()
    cfg.read("config.ini")
    return int(cfg["Settings"]["image_index"])


def get_images():
    cfg = configparser.ConfigParser()
    cfg.read("config.ini")
    return cfg["Settings"]["images"].split(",")


def get_virtual_size():
    cfg = configparser.ConfigParser()
    cfg.read("config.ini")
    from ast import literal_eval as make_tuple
    return make_tuple(cfg["Settings"]["virtual_screensize"])


def get_num_monitors():
    cfg = configparser.ConfigParser()
    cfg.read("config.ini")
    return int(cfg["Settings"]["num_monitors"])


def get_shuffler_status():
    cfg = configparser.ConfigParser()
    cfg.read("gui_config.ini")
    return cfg["Settings"]["shuffler_on"]


def get_shuffle_counter():
    cfg = configparser.ConfigParser()
    cfg.read("config.ini")
    return cfg["Settings"]["shuffle_counter"]


def get_timer_interval():
    cfg = configparser.ConfigParser()
    cfg.read("gui_config.ini")
    return int(cfg["Settings"]["timer_interval"])


def get_timer_mode_index():
    cfg = configparser.ConfigParser()
    cfg.read("gui_config.ini")
    temp = cfg["Settings"]["timer_mode"]
    if temp == "Seconds":
        return 0
    if temp == "Minutes":
        return 1
    if temp == "Hours":
        return 2


def get_timer_status():
    cfg = configparser.ConfigParser()
    cfg.read("gui_config.ini")
    temp = cfg["Settings"]["timer_running"]
    if temp == "True":
        return True
    else:
        return False


def get_geometry():
    cfg = configparser.ConfigParser()
    cfg.read("gui_config.ini")
    temp = str(cfg["Settings"]["window_geometry"])
    temp = temp[temp.find('(') + 1:len(temp) - 1].replace(' ', '')
    cords = temp.split(',')
    return cords


def get_hotkey_text():
    cfg = configparser.ConfigParser()
    cfg.read("hotkey_config.ini")
    temp = dict(cfg["Hotkeys"])
    return temp


def get_hotkeys():
    cfg = configparser.ConfigParser()
    cfg.read("hotkey_config.ini")
    num_items = dict(cfg.items("Hotkeys"))
    builder = {}
    ctrl = win32con.MOD_CONTROL
    alt = win32con.MOD_ALT
    shift = win32con.MOD_SHIFT
    for i in range(1, len(num_items) + 1):
        hotkey = str(cfg["Hotkeys"][str(i)])
        hotkey_arr = hotkey.replace(' ', '').split("+")
        try:
            hotkey_code = ord(hotkey_arr[len(hotkey_arr) - 1])
        except TypeError:
            check = hotkey_arr[len(hotkey_arr) - 1]
            hotkey_code = check_for_special(check)
        hotkey_arr = hotkey_arr[0:len(hotkey_arr) - 1]
        if len(hotkey_arr) == 2:
            if hotkey_arr[0] == "Control" and hotkey_arr[1] == "Alt":
                builder[i] = hotkey_code, ctrl | alt
            if hotkey_arr[0] == "Control" and hotkey_arr[1] == "Shift":
                builder[i] = hotkey_code, ctrl | shift
            if hotkey_arr[0] == "Alt" and hotkey_arr[1] == "Shift":
                builder[i] = hotkey_code, ctrl | alt
        if len(hotkey_arr) == 1:
            if hotkey_arr[0] == "Control":
                builder[i] = hotkey_code, ctrl
            if hotkey_arr[0] == "Shift":
                builder[i] = hotkey_code, shift
            if hotkey_arr[0] == "Alt":
                builder[i] = hotkey_code, alt
        if len(hotkey_arr) == 0:
            builder[i] = hotkey_code, None
    return builder


def check_for_special(inp):
    mappings = {"F1": 0x70, "F2": 0x71, "F3": 0x72, "F4": 0x73, "F5": 0x74, "F6": 0x75, "F7": 0x76, "F8": 0x77,
                "F9": 0x78, "F10": 0x79, "F11": 0x7A, "F12": 0x7B, "Tab": 0x09, "Backspace": 0x08, "Pause": 0x13,
                "Space": 0x20, "PageUp": 0x21, "PageDown": 0x22, "End": 0x23, "Home": 0x24, "Left": 0x25, "Right": 0x27,
                "Up": 0x26, "Down": 0x28, "Insert": 0x2D, "Delete": 0x2E, "Asterisk": 0x6A, "Plus": 0x6B, "Minus": 0x6D,
                "Period": 0xBE, "Slash": 0x6F, "Semicolon": 0xBA, "QuoteLeft": 0xC0, "Comma": 0xBC, "Apostrophe": 0xDE,
                "BracketLeft": 0xDB, "BracketRight": 0xDD, "Backslash": 0xDC}
    for i in mappings:
        if inp == i:
            return mappings.get(i)
