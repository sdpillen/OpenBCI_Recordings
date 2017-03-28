"""
Crosshair via wxpython.  See __main__ for an example use.
"""
import wx
import time


class Crosshair(wx.Frame):

    def __init__(self, x_pos, y_pos, screen_width=1920, screen_height=1080, title="Crosshair", background_color="#686868",
                 crosshair_height=60, crosshair_width=60, thickness=7, hide_cursor=True):
        """
        A wxpython Crosshair that can flash red.

        :param x_pos: x position
        :param y_pos: y position
        :param screen_width: size of screen in pixels
        :param screen_height: height of screen in pixels
        :param title: Not displayed externally.  Defaults to "Crosshair"
        :param background_color: Hex color. Defaults to grey.
        :param crosshair_height: Height of crosshair
        :param crosshair_width: Width of crosshair
        :param thickness: Thickness of crosshair
        :param hide_cursor: Hides the cursor when cursor is displayed over crosshair if True.
        """

        wx.Frame.__init__(self, None, title, style=wx.NO_BORDER)
        self.height_half = crosshair_height // 2
        self.width_half = crosshair_width // 2
        self.screenheight_half = screen_height // 2
        self.screenwidth_half = screen_width // 2
        self.thickness = thickness
        self.SetBackgroundColour(background_color)
        self.pen_color = wx.WHITE
        self.SetSize((screen_width, screen_height))
        self.SetPosition((x_pos, y_pos))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        if hide_cursor:
            self.SetCursor(wx.StockCursor(wx.CURSOR_BLANK))

    def OnPaint(self, event=None):
        """
        Redraws the crosshair with the current pen color
        """
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.SetPen(wx.Pen(self.pen_color, self.thickness))
        # Draw Horizontal Crosshair
        dc.DrawLine(self.screenwidth_half - self.width_half, self.screenheight_half,
                    self.screenwidth_half + self.width_half, self.screenheight_half)
        # Draw Horizontal Crosshair
        dc.DrawLine(self.screenwidth_half, self.screenheight_half - self.height_half,
                    self.screenwidth_half, self.screenheight_half + self.height_half)

    def flash_red(self, duration=0.2):
        """
        Causes the crosshair to flash red for duration seconds.
        :param duration: duration in seconds. defaults to 0.2
        """
        self.pen_color = wx.RED
        self.Refresh(True)
        t = time.time()
        while time.time() - t < duration:
            time.sleep(0.001)
        self.pen_color = wx.WHITE
        self.Refresh(True)

if __name__ == '__main__':
    """
    Example use case.
    """
    app = wx.App(False)

    # Show it on screen to the left of primary screen
    ch = Crosshair(-1920, 0)
    # Set size (or can be passed as parameter)
    ch.SetSize((1920, 1080))
    ch.SetPosition((-1920, 0))
    ch.Show()
    app.MainLoop()
