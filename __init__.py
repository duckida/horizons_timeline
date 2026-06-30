import math
import time
from random import choice

import requests
import wifi


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

    # color choices for projects
    grays = [
        color.rgb(85, 85, 85),
        color.rgb(192, 192, 192),
        color.rgb(0, 0, 0),
        color.rgb(128, 128, 128),
    ]

    # reset
    time_worked_on = 0
    project_data = []

    rq = requests.get(
        f"http://hackatime.hackclub.com/api/v1/users/{HACKATIME_USERNAME}/projects/details?projects={HACKATIME_PROJECTS}",
    )

    for project in rq.json()["projects"]:
        # pick a color to represent the project
        color_choice = choice(grays)
        grays.remove(color_choice)

        project_data.append(
            [project["name"], project["total_seconds"], color_choice]
        )  # a list [name, seconds, color]
        time_worked_on += int(project["total_seconds"])

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
        self.project_bars = []

    def set_projects(self, project_data):
        self.project_bars = []  # reset
        projects_to_plot = []
        start_x = 0

        for project in project_data:
            percentage = project[1] / TIME_REQUIRED

            bar_width = self.fillable_width * percentage

            self.project_bars.append(
                [
                    shape.rectangle(
                        self.top_left_x + start_x,
                        self.top_left_y,
                        bar_width,
                        self.bar_height,
                        # self.RADIUS,
                    ),
                    project[2],
                ]
            )  # a list [shape, color]

            start_x += bar_width

    def draw(self):
        screen.pen = color.white
        screen.shape(self.outline_fill)

        for project in self.project_bars:
            screen.pen = project[1]
            screen.shape(project[0])
            screen.dither()

        screen.pen = color.black
        screen.shape(self.outline)


def draw_gallery(x, y, projects):
    BOX_SIZE = 9
    OUTLINE_THICKNESS = 1
    PADDING = 3
    Y_GAP = 18
    start_x = x
    start_y = y

    for project in projects:
        screen.pen = project[2]
        color_box = shape.rectangle(start_x, start_y, BOX_SIZE, BOX_SIZE)
        screen.shape(color_box)

        outline = color_box.stroke(OUTLINE_THICKNESS)
        screen.pen = color.black
        screen.shape(outline)

        project_hours = round(project[1] / 3600, 2)
        text = f"{project[0]} {project_hours}h"

        screen.pen = color.black
        screen.font = rom_font.kobold
        screen.text(text, start_x + BOX_SIZE + PADDING, start_y)

        text_width, _ = screen.measure_text(text)

        start_x += BOX_SIZE + PADDING + text_width + PADDING
        if start_x > 160:  # go to the next line
            start_x = x
            start_y += Y_GAP


time_bar = ProgressBar((screen.width - 200) / 2, 70, 200, 20)
hackatime_bar = HackatimeProgressBar((screen.width - 200) / 2, 115, 200, 20)

try:
    logo = image.load("/system/apps/horizons_timeline/assets/logo.png")
except:
    logo = image.rectangle(5, 5, 5, 5)


wifi.connect()
while not wifi.is_connected():
    time.sleep(0.2)


def update():  # runs in a loop when the app is open
    badge.mode(FAST_UPDATE | NON_BLOCKING)

    screen.pen = color.white
    screen.clear()

    # Horizons logo
    screen.blit(logo, vec2(10, 5))

    # Time text
    days, hours = calculate_time_to_event()
    screen.font = rom_font.nope
    screen.pen = color.black
    screen.text(f"{days} days, {hours} hours left!", 30, 55)

    # Time bar
    time_bar.set_progress(get_percentage_to_event())
    time_bar.draw()

    # Hackatime stuff
    wifi.connect()
    projects_data = fetch_hackatime()  # fetch the projects

    # Hackatime text
    hours_worked = round(time_worked_on / 3600, 2)
    time_required_hours = TIME_REQUIRED / 3600
    screen.pen = color.black
    screen.text(f"{hours_worked} / {time_required_hours} hours", 30, 100)

    # Hackatime bar
    hackatime_bar.set_projects(projects_data)
    hackatime_bar.draw()

    # Key
    draw_gallery(5, 140, projects_data)

    badge.update()
    wait_for_button_or_alarm(timeout=600 * 1000)  # 600 seconds


run(update)
