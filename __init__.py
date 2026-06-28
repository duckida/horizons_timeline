import time

import wifi


def connect_wifi():
    wifi.connect()
    while not wifi.is_connected():
        time.sleep(0.2)


class ProgressBar:
    RADIUS = 4
    OUTLINE_THICKNESS = 2
    PADDING = 4

    def __init__(self, top_left_corner_x, top_left_corner_y, width, height):
        self.fillable_width = width
        self.top_left_x = top_left_corner_x
        self.top_left_y = top_left_corner_y
        self.bar_height = height

        # Draw the filled white inside
        outline_fill = shape.rounded_rectangle(
            top_left_corner_x,
            top_left_corner_y,
            width,
            height,
            self.RADIUS,
        )
        # Draw the outline
        outline = outline_fill.stroke(self.OUTLINE_THICKNESS)

        screen.pen = color.white
        screen.shape(outline_fill)
        screen.pen = color.black
        screen.shape(outline)

        # The actual progress bar
        self.bar_shape = shape.rectangle(
            top_left_corner_x,
            top_left_corner_y,
            0,
            self.bar_height,
        )
        screen.shape(self.bar_shape)

    def set_progress(self, progress):
        bar_width = self.fillable_width * progress
        self.bar_shape = shape.rounded_rectangle(
            self.top_left_x,
            self.top_left_y,
            bar_width,
            self.bar_height,
            self.RADIUS,
        )

        screen.pen = color.black
        screen.shape(self.bar_shape)


progress = 0.1
bar = ProgressBar(15, 15, 200, 20)


def update():  # runs in a loop when the app is open
    global progress
    progress += 0.1
    bar.set_progress(progress)

    display.update()


run(update)
