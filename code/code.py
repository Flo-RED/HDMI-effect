from PIL import Image, ImageTk
import PySimpleGUI as sg
import time, os, numpy, math, webbrowser


# ...................................................................... layouts
# adjustments layaut
sg.theme('darkbrown1')
l_1 = [
[sg.Slider((1, 50), key="-SLIDER_s-", orientation='horizontal', default_value=3, disabled=False),
sg.Text("Division input scale", key="-SCALE_TEXT-")],
[sg.Slider((1, 50), key="-SLIDER_p_x-", orientation='horizontal', default_value=1),
sg.Text("HDMI pixel width")],
[sg.Slider((1, 50), key="-SLIDER_p_y-", orientation='horizontal', default_value=1),
sg.Text("HDMI pixel height", key="-P_X_TEXT-")],
[sg.Slider((0, 50), key="-SLIDER_b_x-", orientation='horizontal', default_value=0),
sg.Text("Black spacing width")],
[sg.Slider((0, 50), key="-SLIDER_b_y-", orientation='horizontal', default_value=0),
sg.Text("Black spacing height", key="-B_X_TEXT-")],
[sg.Checkbox("Auto division input scale", key="-BOX-")],
[sg.Checkbox("Fixed: HDMI pixels & black spacing", key="-BOX_F-", default=True)],
]

# multiline + progress bar
l_3 = [[sg.Multiline(key="-TEXT-", disabled=True, size=(31, 18), no_scrollbar=True, font=("Courier New", 10, "bold"))],
[sg.ProgressBar(100, size=(22.9, 20), key="-BAR-")]]

# browse
l_4 = [[sg.FileBrowse(key="-BROWSE-")]]


# ................................................. function : import file popup
def update_text(text, window):
    window["-TEXT-"].update(text)
    window.read(1/1000)


# ........................................................ function : get incode
def get_code(path):
    for file in os.listdir("Images Codes"):
        with open(f"Images Codes\\{file}", "r") as txt:
            if path == file[:len(file)-4]:
                return txt.readline()


# .............................................................. function : info
def info(text):
    sg.theme('darkbrown1')
    # layout
    layout = [[sg.Multiline(text, key="-INFO_TEXT-", disabled=True, no_scrollbar=True, font=("Courier New", 10, "bold"), size=(50, 10))],
    [sg.Button("", image_data=get_code("instagram"), key="-INSTA-", button_color="#ffffff"),
    sg.Button("", image_data=get_code("youtube"), key="-YOU-", button_color="#ffffff"),
    sg.Button("", image_data=get_code("tiktok"), key="-TIK-", button_color="#ffffff"),
    sg.Button("", image_data=get_code("itchio"), key="-ITCH-", button_color="#ffffff"), sg.Text("<< Visit me!! 😉", font=("default", 15, "bold"))]]
    window = sg.Window("Info", layout)
    # run window
    while True:
        event, value = window.read(1)
        # instagram event
        if event == "-INSTA-":
            webbrowser.open("https://www.instagram.com/__ahmed_alhasan__/")
        elif event == "-YOU-":
            webbrowser.open("https://www.youtube.com/channel/UCdduXKWnZYnWBu3NNW7_KBQ")
        elif event == "-TIK-":
            webbrowser.open("https://www.tiktok.com/@__flored__?is_from_webapp=1&sender_device=pc")
        elif event == "-ITCH-":
            webbrowser.open("https://flored.itch.io/")
        # close event
        elif event == sg.WIN_CLOSED:
            window.close()
            break


# ................................................... function : save note popup
def note_popup():
    # layout
    layout = [[sg.Text("Name exists!")], [sg.Button("Replace"), sg.Button("Cancel")]]
    window = sg.Window(":: NOTE", layout)
    event, value = window.read()
    if event == "Replace":
        # all done
        window.close()
        return True
    elif event == "Cancel":
        window.close()


# ........................................................ function : save popup
def save_popup(save_path, file_name):
    sg.theme('darkbrown1')
    # layout
    layout = [
    [sg.Input(save_path, key="-INPUT-", size=(36,0)), sg.FolderBrowse(key="-BROWSE-"), sg.Text(":Select location")],
    [sg.Input(file_name, key="-INPUT_NAME-"), sg.Text(":Selcet name")],
    [sg.Button("Save"), sg.Button("Cancel")]]
    window = sg.Window("Save file", layout)
    # window run
    while True:
        event, value = window.read()
        # save event
        if event == "Save":
            if value["-INPUT-"]:
                # loop thro the chosen path
                for file in os.listdir(value["-INPUT-"]):
                    # check if name exists
                    if file == f"{value['-INPUT_NAME-']}.png":
                        # note popup
                        if note_popup():
                            window.close()
                            return value["-INPUT-"], value["-INPUT_NAME-"]
                        break
                else:
                    # all done
                    window.close()
                    return value["-INPUT-"], value["-INPUT_NAME-"]
        # close event or cancel
        if event in (sg.WIN_CLOSED, "Cancel"):
            window.close()
            return None, None
