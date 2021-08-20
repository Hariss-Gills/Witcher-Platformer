"""
Gui elements for the game
"""
import arcade.gui


class GUIManager(arcade.gui.UIManager):

    def adjust_mouse_coordinates(self, x, y):
        """
        This method is used, to translate mouse coordinates to coordinates
        respecting the viewport and window size.
        The implementation should work in most common cases.
        """    
        vx, vy, vw, vh = self.window.ctx.viewport
        vx, vy = self.window.view_port
        pl, pr, pb, pt = self.window.ctx.projection_2d
        proj_width, proj_height = pr - pl, pt - pb
        cords_x = x - (abs(proj_width - vw) / 2) + vx
        cords_y = y - (abs(proj_height - vh) / 2) + vy
        return cords_x, cords_y
