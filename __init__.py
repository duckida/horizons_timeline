import math
import time
from random import choice

import requests
import wifi


def connect_wifi():
    wifi.connect()
    while not wifi.is_connected():
        time.sleep(0.2)


# Event time functions
def calculate_time_to_event():
    rtc_list = list(rtc.datetime())
    rtc_list.append(0)
    time_tuple = rtc_list

    current_epoch = time.mktime(time_tuple)
    event_epoch = 1784879400  # July 24, 2026 at 8:50:00 AM BST

    difference = event_epoch - current_epoch  # this is in seconds
    difference_days = math.floor(difference / 60 / 60 / 24)
    difference_hours = math.floor(difference / 60 / 60) - (difference_days * 24)

    return difference_days, difference_hours


def get_percentage_to_event():
    rtc_list = list(rtc.datetime())
    rtc_list.append(0)
    time_tuple = rtc_list

    booking_epoch = 1782466200  # June 26, 2026 at 10:30:00 AM BST
    current_epoch = time.mktime(time_tuple)
    event_epoch = 1784879400  # July 24, 2026 at 8:50:00 AM BST

    percentage = (current_epoch - booking_epoch) / (event_epoch - booking_epoch)
    return percentage


# Hackatime stuff
HACKATIME_PROJECTS = "chessboard,horizons_timeline,ha-todo-badger"
HACKATIME_USERNAME = "nirvaannn"

time_worked_on = 0  # in seconds
TIME_REQUIRED = 20 * 60 * 60  # 20 hours in seconds


def fetch_hackatime():
    global time_worked_on
    time_worked_on = 0
    project_data = []

    rq = requests.get(
        f"https://hackatime.hackclub.com/api/v1/users/{HACKATIME_USERNAME}/projects/details?projects={HACKATIME_PROJECTS}",
    )

    for project in rq.json()["projects"]:
        project_data.append(
            [project["name"], project["total_seconds"]]
        )  # a list [name, seconds]
        time_worked_on += project["total_seconds"]

    return project_data


class ProgressBar:
    RADIUS = 4
    OUTLINE_THICKNESS = 2

    def __init__(self, top_left_corner_x, top_left_corner_y, width, height):
        self.fillable_width = width
        self.top_left_x = top_left_corner_x
        self.top_left_y = top_left_corner_y
        self.bar_height = height

        # Draw the filled white inside
        self.outline_fill = shape.rounded_rectangle(
            top_left_corner_x,
            top_left_corner_y,
            width,
            height,
            self.RADIUS,
        )
        # Draw the outline
        self.outline = self.outline_fill.stroke(self.OUTLINE_THICKNESS)

        # The actual progress bar
        self.bar_shape = shape.rectangle(
            top_left_corner_x,
            top_left_corner_y,
            0,
            self.bar_height,
        )

        # self.draw()

    def set_progress(self, progress):
        bar_width = self.fillable_width * progress
        self.bar_shape = shape.rounded_rectangle(
            self.top_left_x,
            self.top_left_y,
            bar_width,
            self.bar_height,
            self.RADIUS,
        )

    def draw(self):
        screen.pen = color.white
        screen.shape(self.outline_fill)

        screen.pen = color.black
        screen.shape(self.outline)

        screen.pen = color.black
        screen.shape(self.bar_shape)


class HackatimeProgressBar(ProgressBar):
    def __init__(self, top_left_corner_x, top_left_corner_y, width, height):
        super().__init__(top_left_corner_x, top_left_corner_y, width, height)
        self.bar_shapes = []

    def set_projects(self, project_data):
        self.bar_shapes = []  # reset
        projects_to_plot = []
        start_x = 0

        for project in project_data:
            percentage = project[1] / TIME_REQUIRED

            bar_width = self.fillable_width * percentage

            self.bar_shapes.append(
                shape.rounded_rectangle(
                    self.top_left_x + start_x,
                    self.top_left_y,
                    bar_width,
                    self.bar_height,
                    self.RADIUS,
                )
            )

            start_x += bar_width

    def draw(self):
        screen.pen = color.white
        screen.shape(self.outline_fill)

        screen.pen = color.black
        screen.shape(self.outline)

        grays = [
            color.rgb(85, 85, 85),
            color.rgb(192, 192, 192),
            color.rgb(220, 220, 220),
            color.rgb(128, 128, 128),
            color.rgb(229, 228, 226),
        ]

        for shape in self.bar_shapes:
            # Choose a random color
            color_choice = choice(grays)
            grays.remove(color_choice)

            screen.pen = color_choice

            screen.shape(shape)
            screen.dither()


time_bar = ProgressBar((screen.width - 200) / 2, 80, 200, 20)
hackatime_bar = HackatimeProgressBar((screen.width - 200) / 2, 130, 200, 20)

badge.mode(FAST_UPDATE | NON_BLOCKING)

try:
    logo = image.load("/system/apps/horizons_timeline/assets/logo.png")
except:
    logo = image.rectangle(5, 5, 5, 5)


def init():
    connect_wifi()


def update():  # runs in a loop when the app is open
    screen.pen = color.white
    screen.clear()

    # Horizons logo
    screen.blit(logo, vec2(10, 10))

    # Time text
    days, hours = calculate_time_to_event()
    screen.font = rom_font.nope
    screen.pen = color.black
    screen.text(f"{days} days, {hours} hours left!", 30, 64)

    # Time bar
    time_bar.set_progress(get_percentage_to_event())
    time_bar.draw()

    # Hackatime text
    hours_worked = time_worked_on / 3600
    time_required_hours = TIME_REQUIRED / 3600

    screen.pen = color.black
    screen.text(f"{hours_worked} / {time_required_hours} hours", 30, 114)

    # Hackatime bar
    connect_wifi()  # connect to WiFi
    projects_data = fetch_hackatime()  # fetch the projects
    hackatime_bar.set_projects(projects_data)
    hackatime_bar.draw()

    badge.update()
    wait_for_button_or_alarm(timeout=600 * 1000)  # 600 seconds


run(update)
