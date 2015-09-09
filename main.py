__author__ = 'orcungumus'

import pyglet
import datetime
import urllib.request
import threading
import time


class CourseCrawler(threading.Thread):
    def __init__(self, thread_id, dept, sections, sleep_time=5):
        threading.Thread.__init__(self)
        self.url = 'https://stars.bilkent.edu.tr/homepage/ajax/plainOfferings.php?COURSE_CODE=' + dept + '&SEMESTER=20151'
        self.thread_id = thread_id
        self.dept = dept
        self.sections = []
        self.stop = False
        self.current_area = ""
        self.sleep_time = sleep_time
        self.start_time = datetime.datetime.now()
        for section in sections:
            self.sections.append(dept + ' ' + section)

    def run(self):
        while not self.stop:
            with urllib.request.urlopen(self.url) as f:
                area = False
                for line in f:
                    line = line.decode('utf-8')

                    for section in self.sections:
                        if section in line:
                            self.current_area = section
                            area = True

                    if area is True:
                        if self.is_avalible(line):
                            self.founded()

                    if 'images/icon_desc.gif' in line:
                        area = False
            time.sleep(self.sleep_time)

    def stop_t(self):
        self.stop = True

    def __str__(self):
        return "\nThread " + str(self.thread_id) + " is searching for " + str(self.sections) + " since " + str(self.start_time) + "\n"

    @staticmethod
    def is_avalible(line):
        return ("Must or Elect" in line) and (int(line.split("<td align='center'>")[7].split("</td>")[0]) != 0)

    def founded(self):
        print("Founded: {0}, {1}. Input 3 for exit".format(self.dept, self.current_area))
        song = pyglet.media.load('siren.wav')
        song.play()
        pyglet.app.run()


def main():
    count = 0
    treads = []

    while True:
        menu_input = input("What do you want. \n1 for add new course\n2 for check existing situation\n3 for exit\nEnter Number:")

        if int(menu_input) == 1:
            sections = []
            dept = input("Please enter dept name, for example HUM: ")
            course_codes = input(
                "Please enter course name with sections comma-separeted\nExample Inputs:\n*111-21,111-20\n*111-9\n*111\nEnter sections: ")
            for course_code in course_codes.split(","):
                sections.append(course_code)
            finder = CourseCrawler(count, dept, sections)
            treads.append(finder)
            finder.start()
            count += 1

        elif int(menu_input) == 2:
            for thread in treads:
                print(str(thread))

        else:
            pyglet.app.exit()
            for thread in treads:
                thread.stop_t()
                thread.join()

            break


main()
