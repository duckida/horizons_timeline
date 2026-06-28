import wifi


def connect_wifi():
    wifi.connect()
    while not wifi.is_connected():
        sleep(0.2)


# def init():  # calls when the app opens
#    connect_wifi()


class ProgressBar:
    RADIUS = 4
    OUTLINE_THICKNESS = 2

    def __init__(
        self, top_left_corner_x, top_left_corner_y, width, height, initial_progress
    ):
        self.fillable_width = width
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
        self.bar_shape = shape.rounded_rectangle(
            top_left_corner_x,
            top_left_corner_y,
            self.fillable_width * initial_progress,
            height,
            self.RADIUS,
        )
        screen.shape(self.bar_shape)

    def set_progress(self, progress):
        bar_width = self.fillable_width * progress
        transformation = mat3().scale(bar_width, 1)
        self.bar_shape.transform = transformation


progress = 1
bar = ProgressBar(5, 5, 100, 10, progress)


def update():  # runs in a loop when the app is open
    global progress
    progress += 0.01
    bar.set_progress(progress)

    display.update()
