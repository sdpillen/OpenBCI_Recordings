# -*- coding: utf-8 -*-

"""

Displays a crosshair using pygame.

#############################
Running with queue          #
#############################
This module can be run with a multithread (or multiprocess) Queue.  To run it with a queue, create the object, then run the run_with_queue function, passing in the necessary queue.
An example of this call would be:
        import Queue
        queue = Queue.queue()
        PyCrosshair.PyCrosshair().run_with_queue(queue)

To control the graphics, place items in the queue in the format (command, args).  For example:
        queue.put((CursorTask.crosshair_cross_color_red, None))  # This will call the collide left operation with No arguments.

#############################
Crosshairs and blank screen #
#############################
To show the crosshair, call:
    queue.put((CursorTask.SHOW_CROSSHAIR, None))

To show a blank screen, call:
    queue.put((CursorTask.SHOW_BLANK, None))

"""

import pygame
import sys
import os
import Queue


class PyCrosshair(object):
    # Global settings
    SHOW_BLANK = 'show_blank'  # Shows only the blank screen (with no crosshair)
    SHOW_CROSSHAIR = 'show_crosshair'  # Shows the crosshair
    HIDE_CROSSHAIR = 'hide_crosshair'
    RESET_CROSSHAIR = 'reset_crosshair' # Shows the crosshair and hides all onscreen text



    CROSSHAIR_CROSS_COLOR_FLASH = 'crosshair_cross_color_flash'  # Sets the crosshair to the flash color
    CROSSHAIR_CROSS_COLOR_DEFAULT = 'crosshair_cross_color_reset'  # Sets the crosshair to the default color

    # Text Commands
    SET_TEXT_DICTIONARY_LIST = 'dictionary_text_list'


    def __init__(self, screen_size_width=1920, screen_size_height=1080,
                 background_color=(128, 128, 128), window_x_pos=0, window_y_pos=0, cursor_radius=60, font_size=60, font_type="Verdana",
                 rest_crosshair_cross_color=(255, 255, 255), flash_crosshair_cross_color=(255, 0, 0),
                 show_mouse=False, tick_time=10, crosshair_height=60, crosshair_width=60, crosshair_thickness=8, text_dictionary_list=None):
        """
        Defaults to drawing the crosshair first.

        :param screen_size_width:  Width of screen in pixels, defaults to 1920.
        :param screen_size_height: Height of screen in pixels, defaults to 1920.
        :param background_color: Background of crosshair. Defaults to grey.
        :param window_x_pos: Position of the window.  Defaults to -1920 (left of primary screen)
        :param window_y_pos: Position of the window.  Defaults to 0 (top of primary screen)
        :param cursor_radius: Radius of the cursor. Defaults to 60 pixels.
        :param font_size: Size of the font. Defaults to 40.
        :param font_type: Type of the font. Defaults to Calibri (Body)
        :param show_mouse: bool - False hides the mouse, True shows it.  Defaults to false.
        :param tick_time: tick setting for pygame.
        :param crosshair_height: height of crosshair in pixels
        :param crosshair_width: width of crosshair in pixels
        :param crosshair_thickness: thickness of the crosshair in pixels
        """
        self.screen_width, self.screen_height = screen_size_width, screen_size_height


        # We'll keep track of our text locally.  If using a manager, send set the desired text in the manager and update.
        # This variable will update to display the text.
        self.dictionary_text_list = [] if text_dictionary_list is None else text_dictionary_list

        # Set our window position  (not sure if this commands works on non-windows computers...)
        os.environ['SDL_VIDEO_WINDOW_POS'] = str(window_x_pos) + "," + str(window_y_pos)

        self.tick_time = tick_time

        self.crosshair_height = crosshair_height
        self.crosshair_width = crosshair_width
        self.crosshair_thickness = crosshair_thickness
        self.crosshair_cross_color_default = rest_crosshair_cross_color
        self.crosshair_cross_color_flash = flash_crosshair_cross_color

        self.current_crosshair_cross_color = self.crosshair_cross_color_default  # Keep track of the current crosshair color

        self.cursor_x, self.cursor_y, self.cursor_radius = self.screen_width // 2, self.screen_height // 2, cursor_radius

        self.q_action_dictionary = self.gen_action_dictionary()
        self.ch_background_color = background_color
        # Default of object is to draw the crosshair first.
        self.draw_crosshair_flag = True

        # Init Pygame
        pygame.init()
        pygame.mouse.set_visible(show_mouse)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.NOFRAME)

        self.font = pygame.font.SysFont(font_type, font_size)
        pygame.event.set_blocked(pygame.MOUSEMOTION)


    def gen_action_dictionary(self):
        """
        This is a function that initializes our action dictionary.

        This is a simple way of encapsulating our function calls.  To use, call:
            action_dictionary[key](args)
        """
        action_dictionary = {
                             self.RESET_CROSSHAIR: lambda: self.reset_crosshair(),
                             self.SHOW_BLANK: lambda: self.show_crosshair(False),
                             self.SHOW_CROSSHAIR: lambda: self.show_crosshair(True),
                             self.HIDE_CROSSHAIR: lambda: self.show_crosshair(False),
                             self.CROSSHAIR_CROSS_COLOR_FLASH: lambda ch_red=self.crosshair_cross_color_flash: self.set_crosshairs_color(color=ch_red),
                             self.CROSSHAIR_CROSS_COLOR_DEFAULT: lambda ch_white=self.crosshair_cross_color_default: self.set_crosshairs_color(color=ch_white),
                             self.SET_TEXT_DICTIONARY_LIST: lambda new_text_dictionary_list_l: self.set_text_dictionary_list(new_text_dictionary_list=new_text_dictionary_list_l)}
        return action_dictionary

    def set_text_dictionary_list(self, new_text_dictionary_list):
        if type(new_text_dictionary_list) is dict():
            new_text_dictionary_list = [new_text_dictionary_list]
        self.dictionary_text_list = new_text_dictionary_list

    def reset_crosshair(self):
        """
        Resets our crosshair -- shows crosshair, changes crosshair to default color and hides all texts,
        """
        self.dictionary_text_list = []
        self.current_crosshair_cross_color = self.crosshair_cross_color_default
        self.show_crosshair(True)

    def quit(self):
        """
        Quits pygame and exits (via sys.exit)
        """
        pygame.quit()
        sys.exit(0)

    def run_with_queue(self, q):
        """
        Runs our game by reading off events off the passed queue. Events should be passed in the form:
            (event, args).
        If no args, pass None instead.
        :param q: Multithread (or multiprocess) object queue to read from.
        :return: None - runs infinitely
        """
        timer = pygame.time.Clock()
        while True:
            self.clear_events()
            try:
                key, args = q.get(False)
                if args is None:
                    self.q_action_dictionary[key]()
                elif key == self.SET_TEXT_DICTIONARY_LIST:
                    self.q_action_dictionary[key](args)
                elif type(args) is not tuple:
                    self.q_action_dictionary[key](args)
                else:
                    self.q_action_dictionary[key](*args)
            except Queue.Empty:
                pass
            self.clear_events()
            timer.tick(self.tick_time)
            self.draw_shapes()
            pygame.display.update()

    def show_crosshair(self, b):
        """
        Shows the crosshair
        :return:
        """
        self.draw_crosshair_flag = b

    def clear_events(self):
        """
        Clear all events from our pygame event queue.  Needs to be called to prevent freezing.
        """
        pygame.event.clear()


    def draw_shapes(self):
        """
        Draws our boards according to how the flags of this class are set.

        This method should not be called externally.

        """

        # Fill the screen with our current background
        self.screen.fill(self.ch_background_color)

        if self.draw_crosshair_flag:
            height_half = self.crosshair_height // 2
            width_half = self.crosshair_width // 2
            screenheight_half = self.screen_height // 2
            screenwidth_half = self.screen_width // 2

            # The Horizontal Bar of the crosshari
            pygame.draw.rect(self.screen, self.current_crosshair_cross_color,
                             pygame.Rect((screenwidth_half - width_half, screenheight_half - self.crosshair_thickness // 2),
                                         (self.crosshair_width, self.crosshair_thickness)))
            # The Vertical Bar
            pygame.draw.rect(self.screen, self.current_crosshair_cross_color,
                             pygame.Rect((screenwidth_half - self.crosshair_thickness // 2, screenheight_half - height_half),
                                         (self.crosshair_thickness, self.crosshair_height)))

        self.clear_events()
        self.draw_text()
        self.clear_events()

    def set_crosshairs_color(self, color):
        """
        Sets the crosshair color to color.
        :param color: RGB (tuple) color.  Defaults to white.
        """
        self.current_crosshair_cross_color = color

    def draw_text(self):
        """
        Draws our text contained in dictionary_text_list onscreen.
        :return:
        """
        if type(self.dictionary_text_list) is not list:
            self.dictionary_text_list = [self.dictionary_text_list]
        for text_dict in self.dictionary_text_list:
            assert type(text_dict) is dict
            color = text_dict['color']
            x, y = text_dict['pos']
            text = text_dict['text']
            if x is None or y is None:
                center_x, center_y = self.get_coords_for_message_center(text)
                x = center_x if x is None else x
                y = center_y if y is None else y
            answer_txt = self.font.render(text, False, color)
            self.screen.blit(answer_txt, (x, y))

    def blt_text(self, text, x, y, color=(255, 255, 255)):
        """
        Shows text on screen at the passed x and y coords.

        If x is None or Y is none, text will be displayed in the middle of the screen
        :param text: str - text to show
        :param x: x coord. If none, we'll show in center
        :param y: x coord. If none, we'll show in center
        :param color: rgb, defaults to white.
        :return:
        """
        center_x, center_y = self.get_coords_for_message_center(text)
        x = center_x if x is None else x
        y = center_y if y is None else y
        text = self.font.render(text, False, color)
        self.screen.blit(text, (x, y))

    def get_coords_for_message_center(self, msg):
        """
        Gets the coordinates for centering the message on screen.
        :param msg: The message to center onscreen
        :return: The x y coords to blit the message to have it be at the center of the screen.
        """
        size_x, size_y = self.get_message_size(msg)
        center_x = (self.screen_width // 2) - (size_x // 2)
        center_y = (self.screen_height // 2) - (size_y // 2)
        return center_x, center_y

    def get_message_size(self, msg):
        """
        Gets the width and height of our message.
        """
        msg_image = self.font.render(msg, False, (255, 255, 255), (0, 0, 0))
        size_x, size_y = msg_image.get_size()
        return size_x, size_y

    def center_multiline_msg(self, msg):
        """
        Displays a multiline message (msg) to screen at the very center of the screen.
        :param msg: The string message
        :return: None - displays to screen
        """
        for i, line in enumerate(msg.splitlines()):
            msg_image = self.font.render(line, False,
                                         (255, 255, 255), (0, 0, 0))

            msgim_center_x, msgim_center_y = msg_image.get_size()
            msgim_center_x //= 2
            msgim_center_y //= 2

            self.screen.blit(msg_image, (
                self.background_width // 2 - msgim_center_x,
                self.background_height // 2 - msgim_center_y + i * 22))

if __name__ == '__main__':
    PyCrosshair().run_with_queue(Queue.Queue())
