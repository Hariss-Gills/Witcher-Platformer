'''
Platformer Game
'''
import arcade
import os
import pyglet
import arcade.gui
import sys
import pickle
import supp_code.level_1
import supp_code.game_settings as st
import supp_code.game_sprites as sp
import supp_code.game_gui as gui

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):  # Used for packaging
    os.chdir(sys._MEIPASS)


class GameWindow(arcade.Window):
    '''
    Window class the resizes and goes into fullscreen
    '''
    def __init__(self):
        super().__init__(st.SCREEN_WIDTH, st.SCREEN_HEIGHT, st.SCREEN_TITLE, resizable=True)
        self.center_window()
        self.set_icon(pyglet.image.load(os.path.join(st.ASSET_PATH, 'icon.ico')))
        # Used to keep track of our scrolling
        self.view_port = 0, 0

    def adjust_port(self):
        '''
        Method to adjust viewport for all views
        '''
        arcade.set_viewport(self.view_port[0], self.view_port[0] + st.SCREEN_WIDTH, self.view_port[1], self.view_port[1] + st.SCREEN_HEIGHT)

    def on_resize(self, width, height):
        '''
        This method is automatically called when the window is resized
        '''
        super().on_resize(width, height)
        self.adjust_port()


class MenuView(arcade.View):
    '''
    Main Menu for the game
    '''

    def __init__(self, ui_manager, game):
        super().__init__()
        self.background_bottom_sprite = None
        self.gui_sprite = None
        self.menu_music = None
        self.counter = 0
        self.ui_manager = ui_manager
        self.game_view = game

    def on_show(self):
        self.setup()
        self.background_bottom_sprite = sp.Background_sprites(0, 'main_background\\background.png')
        self.gui_sprite = sp.Background_sprites(0, 'gui\gui_back.png')
        self.gui_sprite.center_x = st.SCREEN_WIDTH//2
        self.gui_sprite.center_y = st.SCREEN_HEIGHT//2
        self.background_bottom_sprite.right = st.SCREEN_WIDTH
        self.background_bottom_sprite.top = st.SCREEN_HEIGHT
        if self.menu_music is None:
            self.menu_music = arcade.Sound(os.path.join(st.ASSET_PATH, 'sounds\start_screen_music.ogg'))
            self.played_menu_music = self.menu_music.play(0.05, loop = True)   

    def setup(self):
        start_button_normal = arcade.load_texture((os.path.join(st.ASSET_PATH, 'gui\start_normal.png')))
        start_hovered_texture = arcade.load_texture((os.path.join(st.ASSET_PATH, 'gui\start_hover.png')))
        start_pressed_texture = arcade.load_texture((os.path.join(st.ASSET_PATH, 'gui\start_pressed.png')))

        options_button_normal = arcade.load_texture((os.path.join(st.ASSET_PATH, 'gui\options_normal.png')))
        options_hovered_texture = arcade.load_texture((os.path.join(st.ASSET_PATH, 'gui\options_hover.png')))
        options_pressed_texture = arcade.load_texture((os.path.join(st.ASSET_PATH, 'gui\options_pressed.png')))

        quit_button_normal = arcade.load_texture((os.path.join(st.ASSET_PATH, 'gui\quit_normal.png')))
        quit_hovered_texture = arcade.load_texture((os.path.join(st.ASSET_PATH, 'gui\quit_hover.png')))
        quit_pressed_texture = arcade.load_texture((os.path.join(st.ASSET_PATH, 'gui\quit_pressed.png')))

        self.start_button = arcade.gui.UIImageButton(center_x = st.SCREEN_WIDTH//2, center_y = st.SCREEN_HEIGHT//2 + 50,
                                                     normal_texture = start_button_normal,
                                                     hover_texture =start_hovered_texture,
                                                     press_texture = start_pressed_texture)

        self.options_button = arcade.gui.UIImageButton(center_x = st.SCREEN_WIDTH//2, center_y = st.SCREEN_HEIGHT//2,
                                                       normal_texture = options_button_normal,
                                                       hover_texture = options_hovered_texture,
                                                       press_texture = options_pressed_texture)

        self.quit_button = arcade.gui.UIImageButton(center_x = st.SCREEN_WIDTH//2, center_y = st.SCREEN_HEIGHT//2 - 50,
                                                    normal_texture = quit_button_normal,
                                                    hover_texture = quit_hovered_texture,
                                                    press_texture = quit_pressed_texture)    

        self.ui_manager.add_ui_element(self.start_button)
        self.ui_manager.add_ui_element(self.options_button)
        self.ui_manager.add_ui_element(self.quit_button)
       
    def on_draw(self):
        arcade.start_render()
        self.background_bottom_sprite.draw()
        self.gui_sprite.draw()
        arcade.draw_text('Witcher Platformer', st.SCREEN_WIDTH//2, st.SCREEN_HEIGHT//2 + 250, arcade.color.AZURE_MIST, font_size=30, anchor_x = 'center', font_name =st.FONT)
        if st.LOAD_LEVEL_1:
            arcade.draw_text('Loaded', st.SCREEN_WIDTH//2, st.SCREEN_HEIGHT//2 - 250, arcade.color.MEDIUM_SPRING_GREEN, font_size=18, anchor_x = 'center', font_name =st.FONT)
        else:
            arcade.draw_text('Loading...', st.SCREEN_WIDTH//2, st.SCREEN_HEIGHT//2 - 250, arcade.color.AZURE_MIST, font_size=18, anchor_x = 'center', font_name =st.FONT)

    def on_update(self, delta_time: float):
        self.counter += 1
        if self.start_button.pressed:
            self.ui_manager.purge_ui_elements()
            self.menu_music.stop(self.played_menu_music)
            self.game_view.load_rest_map()
            self.game_view.setup()
            self.game_view.scroll_screen()
            self.window.show_view(self.game_view)
        elif self.options_button.pressed:
            self.ui_manager.purge_ui_elements()
            options_view = OptionsView(self.ui_manager, self)
            self.window.show_view(options_view)
        elif self.quit_button.pressed:
            self.window.close()
            sys.exit()
        if self.counter == 2:
            # Load in main layer after main screen is displayed. 
            self.game_view.load_main_layer()
            st.LOAD_LEVEL_1 = True               


class OptionsView(arcade.View):
    '''
    Give user the ability to have options in the game
    '''

    def __init__(self, ui_manager, prev_view):
        super().__init__()
        self.view_left = self.window.view_port[0]
        self.view_bottom = self.window.view_port[1]
        self.background_bottom_sprite = None
        self.gui_sprite = None
        self.ui_manager = ui_manager
        self.prev_view = prev_view

    def on_show(self):
        self.setup()
        self.background_bottom_sprite = sp.Background_sprites(0, 'main_background\\background.png')
        self.gui_sprite = sp.Background_sprites(0, 'gui\gui_back.png')
        self.gui_sprite.center_x = self.view_left + st.SCREEN_WIDTH//2
        self.gui_sprite.center_y = self.view_bottom + st.SCREEN_HEIGHT//2
        self.background_bottom_sprite.right = self.view_left + st.SCREEN_WIDTH
        self.background_bottom_sprite.top = self.view_bottom + st.SCREEN_HEIGHT

    def setup(self):
        
        self.fullscreen_toggle = arcade.gui.UIToggle(center_x = self.view_left + st.SCREEN_WIDTH//2 + 70, center_y = self.view_bottom + st.SCREEN_HEIGHT//2,
                                                     height = 20, value = st.FULLSCREEN)
        self.stats_toggle = arcade.gui.UIToggle(center_x = self.view_left + st.SCREEN_WIDTH//2 + 70, center_y = self.view_bottom + st.SCREEN_HEIGHT//2 - 50,
                                                height = 20, value = st.STATS)
        
        back_button_normal = arcade.load_texture((os.path.join(st.ASSET_PATH, 'gui\\back_button_normal.png')))
        back_button_hover = arcade.load_texture((os.path.join(st.ASSET_PATH, 'gui\\back_button_hover.png')))
        back_button_pressed = arcade.load_texture((os.path.join(st.ASSET_PATH, 'gui\\back_button_pressed.png')))
        
        self.back_button =  arcade.gui.UIImageButton(center_x = self.view_left + st.SCREEN_WIDTH//2, center_y = self.view_bottom + st.SCREEN_HEIGHT//2 - 90,
                                                     normal_texture = back_button_normal,
                                                     hover_texture = back_button_hover,
                                                     pressed_texture = back_button_pressed)

        self.ui_manager.add_ui_element(self.fullscreen_toggle)
        self.ui_manager.add_ui_element(self.stats_toggle)
        self.ui_manager.add_ui_element(self.back_button)
       
    def on_draw(self):
        arcade.start_render()
        self.background_bottom_sprite.draw()
        self.gui_sprite.draw()
        arcade.draw_text('Options', self.view_left + st.SCREEN_WIDTH//2, self.view_bottom + st.SCREEN_HEIGHT//2 + 50, arcade.color.AZURE_MIST, font_size = 18, anchor_x = 'center', font_name = st.FONT)
        arcade.draw_text('Fullscreen Mode:', self.view_left + st.SCREEN_WIDTH//2 - 20, self.view_bottom + st.SCREEN_HEIGHT//2 - 10, arcade.color.AZURE_MIST, font_size = 12, anchor_x = 'center', font_name = st.FONT)
        arcade.draw_text('Display Stats:', self.view_left + st.SCREEN_WIDTH//2 - 20, self.view_bottom + st.SCREEN_HEIGHT//2 - 60, arcade.color.AZURE_MIST, font_size = 12, anchor_x = 'center', font_name = st.FONT)

    def on_update(self, delta_time: float):
        if self.fullscreen_toggle.value:
            st.FULLSCREEN = True
            self.window.set_fullscreen(st.FULLSCREEN)
        else:
            st.FULLSCREEN = False
            self.window.set_fullscreen(st.FULLSCREEN)
        if self.stats_toggle.value:
            st.STATS = True
        else:
            st.STATS = False 
        if self.back_button.pressed:
            self.ui_manager.purge_ui_elements()
            self.window.show_view(self.prev_view)


class PauseView(arcade.View):
    '''
    Pause Screen for the game
    '''

    def __init__(self, ui_manager, game):
        super().__init__()
        self.window.set_mouse_visible(True)
        self.view_left = self.window.view_port[0]
        self.view_bottom = self.window.view_port[1]
        self.gui_sprite = None
        self.ui_manager = ui_manager
        self.game_view = game  

    def on_show(self):
        self.setup()
        self.gui_sprite = sp.Background_sprites(0, 'gui\gui_back.png')
        self.gui_sprite.center_x = self.view_left + st.SCREEN_WIDTH//2
        self.gui_sprite.center_y = self.view_bottom + st.SCREEN_HEIGHT//2 
        self.game_view.background_music.set_volume(0.025, self.game_view.played_backgroud_music)

    def setup(self):
        restart_button_normal = arcade.load_texture((os.path.join(st.ASSET_PATH, 'gui\\restart_normal.png')))
        restart_hovered_texture = arcade.load_texture((os.path.join(st.ASSET_PATH, 'gui\\restart_hover.png')))
        restart_pressed_texture = arcade.load_texture((os.path.join(st.ASSET_PATH, 'gui\\restart_pressed.png')))

        options_button_normal = arcade.load_texture((os.path.join(st.ASSET_PATH, 'gui\options_normal.png')))
        options_hovered_texture = arcade.load_texture((os.path.join(st.ASSET_PATH, 'gui\options_hover.png')))
        options_pressed_texture = arcade.load_texture((os.path.join(st.ASSET_PATH, 'gui\options_pressed.png')))

        quit_button_normal = arcade.load_texture((os.path.join(st.ASSET_PATH, 'gui\quit_normal.png')))
        quit_hovered_texture = arcade.load_texture((os.path.join(st.ASSET_PATH, 'gui\quit_hover.png')))
        quit_pressed_texture = arcade.load_texture((os.path.join(st.ASSET_PATH, 'gui\quit_pressed.png')))


        self.restart_button = arcade.gui.UIImageButton(center_x = self.view_left + st.SCREEN_WIDTH//2, center_y = self.view_bottom + st.SCREEN_HEIGHT//2 + 50,
                                                       normal_texture = restart_button_normal,
                                                       hover_texture = restart_hovered_texture,
                                                       press_texture = restart_pressed_texture)

        self.options_button = arcade.gui.UIImageButton(center_x = self.view_left + st.SCREEN_WIDTH//2, center_y = self.view_bottom + st.SCREEN_HEIGHT//2,
                                                       normal_texture = options_button_normal,
                                                       hover_texture = options_hovered_texture,
                                                       press_texture = options_pressed_texture)

        self.quit_button = arcade.gui.UIImageButton(center_x =  self.view_left + st.SCREEN_WIDTH//2, center_y = self.view_bottom + st.SCREEN_HEIGHT//2 - 50,
                                                    normal_texture = quit_button_normal,
                                                    hover_texture = quit_hovered_texture,
                                                    press_texture = quit_pressed_texture)    

        self.ui_manager.add_ui_element(self.restart_button)
        self.ui_manager.add_ui_element(self.options_button)
        self.ui_manager.add_ui_element(self.quit_button)
       
    def on_draw(self):
        arcade.start_render()
        self.game_view.draw_main()
        arcade.draw_lrtb_rectangle_filled(self.view_left,  self.view_left + st.SCREEN_WIDTH,
                                          self.view_bottom + st.SCREEN_HEIGHT, self.view_bottom,
                                          color = arcade.color.AFRICAN_VIOLET + (100,))
        self.gui_sprite.draw()
        arcade.draw_text('Paused', self.view_left + st.SCREEN_WIDTH//2, self.view_bottom + st.SCREEN_HEIGHT//2 + 250, arcade.color.WHITE, font_size=30, anchor_x = 'center', font_name = st.FONT)
    
    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE: # resume game
            self.ui_manager.purge_ui_elements()
            self.window.show_view(self.game_view)

    def on_update(self, delta_time: float):
        if self.restart_button.pressed:
            self.ui_manager.purge_ui_elements()
            self.game_view.background_music.stop(self.game_view.played_backgroud_music)
            self.game_view.setup()
            self.window.show_view(self.game_view)
        elif self.options_button.pressed:
            self.ui_manager.purge_ui_elements()
            options_view = OptionsView(self.ui_manager, self)
            self.window.show_view(options_view)
        elif self.quit_button.pressed:
            self.window.close()
            sys.exit()


class GameOverView(PauseView):
    '''
    Display endgame view and calculate highscore
    '''
    def __init__(self, ui_manager, game):
        super().__init__(ui_manager, game)
        
    def on_show(self):
        self.game_view.player_sprite.update_animation(self.game_view.platforms_list)
        time = self.game_view.total_time
        points = self.game_view.points
        # Calculate minutes
        minutes = int(time) // 60
        # Calculate seconds by using a modulus (remainder)
        seconds = int(time) % 60
        # Calculate milliseconds
        seconds_100s = int(time * 100)
        # Figure out our output
        self.output = f"Time: {minutes:02d}:{seconds:02d}:{seconds_100s:02d}"
        time = seconds + minutes * 60 + seconds_100s * 1000
        self.final_score = round(1/time + points, 3)
        self.highscore = self.get_highscore()
        super().on_show()   

    def get_highscore(self):
        try:
            with open('score_data.pickle', 'r+b') as inp:
                while True:
                    try:
                        self.highscore = pickle.load(inp)                    
                    except EOFError:
                        break
                if self.final_score > self.highscore and not self.game_view.player_sprite.dead:
                    self.highscore = self.final_score
                    pickle.dump(self.highscore, inp)
                inp.close()
        except FileNotFoundError:
            with open('score_data.pickle', 'wb') as out:
                print("Create File")
                if self.game_view.player_sprite.dead:
                    self.highscore = 0.0
                else:
                    self.highscore = self.final_score    
                pickle.dump(self.highscore, out, pickle.HIGHEST_PROTOCOL)    

        return self.highscore    

    def on_draw(self):
        arcade.start_render()
        self.game_view.draw_main()
        arcade.draw_lrtb_rectangle_filled(self.view_left,  self.view_left + st.SCREEN_WIDTH,
                                          self.view_bottom + st.SCREEN_HEIGHT, self.view_bottom,
                                          color = arcade.color.BLACK + (100,))
        self.gui_sprite.draw()
        if self.game_view.player_sprite.dead:
            arcade.draw_text('Game Over', self.view_left + st.SCREEN_WIDTH//2, self.view_bottom + st.SCREEN_HEIGHT//2 + 250, arcade.color.RED, font_size= 30, anchor_x = 'center', font_name = st.FONT)
        else:
            arcade.draw_text('Game Over', self.view_left + st.SCREEN_WIDTH//2, self.view_bottom + st.SCREEN_HEIGHT//2 + 250, arcade.color.MEDIUM_SPRING_GREEN, font_size = 30, anchor_x = 'center', font_name = st.FONT)
            arcade.draw_text(f'Score: {self.final_score}', self.view_left + st.SCREEN_WIDTH//2, self.view_bottom + st.SCREEN_HEIGHT//2 - 200, arcade.color.AZURE_MIST, font_size = 20, anchor_x = 'center', font_name = st.FONT)
        arcade.draw_text(self.output,  self.view_left + st.SCREEN_WIDTH//2, self.view_bottom + st.SCREEN_HEIGHT//2 - 250, arcade.color.AZURE_MIST, font_size = 20,  anchor_x = 'center', font_name = st.FONT)
        arcade.draw_text(f'High Score: {self.highscore}',  self.view_left + st.SCREEN_WIDTH//2, self.view_bottom + st.SCREEN_HEIGHT//2 - 300, arcade.color.AZURE_MIST, font_size = 20,  anchor_x = 'center', font_name = st.FONT)
    
    def on_key_press(self, key, _modifiers):
        return 


def main():
    '''
    Main method
    '''
    window = GameWindow()
    ui_manager = gui.GUIManager()
    game_view = supp_code.level_1.MyGame(ui_manager)
    game_view.load_music()
    menu_view = MenuView(ui_manager, game_view)
    window.show_view(menu_view)
    arcade.run()

if __name__ == '__main__':
    main()
