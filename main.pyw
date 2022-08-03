from PIL import Image
import PySimpleGUI as sg
import code, algo, time, os, numpy, math, webbrowser

# ........................................................... Constant variables
time_out = 0
timer = 0
text = "Welcome!!👋👋"
info_text = """Creator: Ahmed Al-Hasan "aka FloRED" ⚒️

This program makes your chosen image to look like a realistic HDMI screen effect with so much optimization.

This program was developed using Python and its module PySimpleGUI."""

# .................................................................. main layout
sg.theme('darkbrown1')
layout = [
[sg.Frame("Adjustments", code.l_1),
sg.Column(code.l_3)],
[sg.Button("Create"), sg.VSeperator(), sg.Column(code.l_4), sg.Text("Import a file...", key="-FILE_TEXT-", size=(50, 1)), sg.Button("Info", key="-INFO-")]]
window = sg.Window("HDMI Pixel filter", layout, grab_anywhere=True)

# ................................................................... window run
while True:
    event, value = window.read(1)
    window["-TEXT-"].update(text)
    # timer goes down
    if time_out > 0:
        time_out -= 1
    if timer > 0:
        timer -= 1
    else:
        timer = 100

    if timer == 0:
    	window["-INFO-"].update(button_color="#ffffff")
    elif timer == 50:
        window["-INFO-"].update(button_color="#FDCB52")

    # .............................................................. browse path
    path = value["-BROWSE-"]
    if path:
        window["-FILE_TEXT-"].update(path)
        image = Image.open(path)
        if time_out == 0:
            new_size = (round(image.size[0] / value["-SLIDER_s-"]), round(image.size[1] / value["-SLIDER_s-"]))
            size = (
            int(new_size[0] * 3 * value["-SLIDER_p_x-"] + new_size[0] * value["-SLIDER_b_x-"]),
            int(new_size[1] * 3 * value["-SLIDER_p_y-"] + new_size[1] * value["-SLIDER_b_y-"]))
            text = ""
            text += f"Origin size: {image.size[0]} x {image.size[1]} px\n"
            text += f"...............................\n"
            text += f"New size   : {size[0]} x {size[0]} px\n"
            text += f"Resolution : {new_size[0]} x {new_size[1]}"

    # ...................................................... auto scale checkbox
    if value["-BOX-"]:
        window["-SCALE_TEXT-"].update(text_color="#705E52")
        s_value = 3 * value["-SLIDER_p_x-"] + value["-SLIDER_b_x-"]
        window["-SLIDER_s-"].update(disabled=True, value=s_value)
    else:
        window["-SCALE_TEXT-"].update(text_color="#FDCB52")
        window["-SLIDER_s-"].update(disabled=False)

    # ................................................... fixed sliders checkbox
    if value["-BOX_F-"]:
        window["-P_X_TEXT-"].update(text_color="#705E52")
        window["-B_X_TEXT-"].update(text_color="#705E52")
        window["-SLIDER_p_y-"].update(disabled=True,value=value["-SLIDER_p_x-"])
        window["-SLIDER_b_y-"].update(disabled=True,value=value["-SLIDER_b_x-"])
    else:
        window["-P_X_TEXT-"].update(text_color="#FDCB52")
        window["-B_X_TEXT-"].update(text_color="#FDCB52")
        window["-SLIDER_p_y-"].update(disabled=False)
        window["-SLIDER_b_y-"].update(disabled=False)

    # ............................................................... info event
    if event == "-INFO-":
        code.info(info_text)

    # ............................................................. Create event
    elif event == "Create":
        text = algo.main(window, text, path)
        window["-TEXT-"].update(text)
        time_out = 400

    # ....................................................... close window event
    elif event == sg.WIN_CLOSED:
        window.close()
        break
