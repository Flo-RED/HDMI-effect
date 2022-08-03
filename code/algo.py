from PIL import Image
import PySimpleGUI as sg
import code, time, os, numpy, math
old_path = ""
file_name = ""
def main(window, text, path):
    global old_path, file_name
    if path:
        if path[len(path)-3:] in ("png", "jpg"):
            event, value = window.read(1)
            final_image = []

            # ...................................................... adjustments
            # adjust the scaling variables
            scale = int(value["-SLIDER_s-"])
            p_scale_x = int(value["-SLIDER_p_x-"])
            p_scale_y = int(value["-SLIDER_p_y-"])
            b_scale_x = int(value["-SLIDER_b_x-"])
            b_scale_y = int(value["-SLIDER_b_y-"])
            default_values = (scale, p_scale_x, p_scale_y, b_scale_x, b_scale_y)
            # choose the save path
            old_path, file_name = code.save_popup(old_path, file_name)
            save_path = f"{old_path}/{file_name}"
            try:
                if old_path:

                    # ......................... import image and convert to list
                    # open the image
                    start_image = Image.open(path)
                    # define the new size for the image
                    new_size = (round(start_image.size[0] / scale), round(start_image.size[1] / scale))
                    # resize the image to the new size
                    image = start_image.resize(new_size)
                    # convert the image to an array
                    image_array = numpy.array(image)
                    # convert the array to python array
                    list = image_array.tolist()

                    # ..................... loop for every row in the image list
                    try:
                        for y in range(len(list)):
                            column = []
                            # convert every pixel to HDMI pixel
                            for x in list[y]:
                                column += [[0, 0, 0]] * b_scale_x + [[x[0], 0, 0]] * p_scale_x + [[0, x[1], 0]] * p_scale_x + [[0, 0, x[2]]] * p_scale_x
                            column += [[0, 0, 0]] * b_scale_x
                            # add black line every row
                            for x in range(b_scale_y):
                                final_image += [[[0, 0, 0]] * len(list[0]) * 3 * p_scale_x + [[0, 0, 0]] * len(list[0]) * b_scale_x + [[0, 0, 0]] * b_scale_x]
                            # add the colored pixels rows
                            for x in range(p_scale_y * 3):
                                final_image += [column]
                            # update progress bar
                            window.read(1/1000)
                            window["-BAR-"].update(f"{math.floor(y / len(list) * 100)}")
                        # add the final black line
                        for x in range(b_scale_y):
                            final_image += [[[0, 0, 0]] * len(list[0]) * 3 * p_scale_x + [[0, 0, 0]] * len(list[0]) * b_scale_x + [[0, 0, 0]] * b_scale_x]

                        window["-BAR-"].update(0) # reset progress bar

                        # .......................................... final steps
                        # convert the python list to numpy array
                        code.update_text("Converting to array...\n", window)
                        final_image = numpy.array(final_image)
                        # adjust the new image size
                        size = (final_image.shape[1], final_image.shape[0])
                        # create the image by numpy array
                        code.update_text("Creating image...\n", window)
                        image = Image.fromarray(final_image.astype(numpy.uint8))
                        # save the image to the chosen path
                        code.update_text("Saving image...\n", window)
                        image.save(f"{save_path}.png")
                        # set the results
                        text = "DONE!!!\n"
                        text += f"Origin size: {start_image.size[0]} x {start_image.size[1]} px\n"
                        text += f"...............................\n"
                        text += f"New size   : {size[0]} x {size[0]} px\n"
                        text += f"Resolution : {new_size[0]} x {new_size[1]}"
                        return text

                    except:
                        text = ""
                        text += ":: ERROR ❌\n\n"
                        text += "Something went wrong, this image doesnt work for some reason... sorry"
                        return text
                else:
                    text = ""
                    text += ":: Saving canceled 🙃"
                    return text
            except ValueError:
                text = ""
                text += ":: ERROR ❌\n\n"
                text += "The image is too small for those conditions"
                return text
        else:
            text = ""
            text += ":: ERROR ❌\n\n"
            text += "Note that the file must be png or jpg"
            return text
    else:
        text = ""
        text += ":: ERROR ❌\n\n"
        text += "Please choose a file"
        return text
