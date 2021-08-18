import arcade, os, timeit
import game_settings as st, game_sprites as sp, game as gm

class MyGame(arcade.View):
    '''
    View to Run the game
    '''

    def __init__(self, ui_manager):
        super().__init__()

        self.ui_manager = ui_manager   

        # --- Variables for our statistics

        # Time for on_update
        self.processing_time = 0

        # Time for on_draw
        self.draw_time = 0

        # Variables used to calculate frames per second
        self.frame_count = 0
        self.fps_start_timer = None
        self.fps = None

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list

        self.coin_list = None
        self.wall_list = None
        self.player_list = None
        self.empty_list = None
        self.background_list = None
        self.platforms_list = None
        self.water_list = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False

        # Our TileMap Object
        self.tile_map = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None
        self.physics_engine_background_0 = None
        self.physics_engine_background_1 = None
        self.physics_engine_background_2 = None

        # Used to keep track of our scrolling
        self.view_left = self.window.view_port[0]
        self.view_bottom = self.window.view_port[1]

        # Load sounds
        self.background_music = None
        self.collect_coin_sound = None
        self.jump_sound = None
        self.death_sound = None

        # Keep track of the score
        self.points = 0

        # Speedrun Timer
        self.total_time = 0.0


    def load_music(self):
        '''
        Load in the music separately 
        '''
        # load Music to shave off 2 second when restarting
        self.background_music = arcade.Sound(os.path.join(st.current_path, 'game_assets\sounds\\background_music.ogg'))
        self.jump_sound = arcade.Sound(os.path.join(st.current_path, 'game_assets\sounds\jump_sound.ogg'))
        self.collect_coin_sound = arcade.Sound(os.path.join(st.current_path, 'game_assets\sounds\coin_sound.ogg'))
        self.death_sound = arcade.Sound(os.path.join(st.current_path, 'game_assets\sounds\death_sound.ogg'))


    def load_main_layer(self):
        '''
        Load in the first layer separately 
        '''
        #load Main Layer to shave off 4 seconds when restarting
        # What are the names of the layers?
        platform_layer = 'main_platforms'
        # Read in the tiled map
        level1_map = arcade.tilemap.read_tmx(os.path.join(st.current_path, 'game_assets\maps\imporved_map.tmx'))
        self.platforms_list = arcade.tilemap.process_layer(
            map_object=level1_map,layer_name=platform_layer,scaling=st.MAP_SCALING,use_spatial_hash=True) 

    def load_rest_map(self):
        '''
        Load in the other layers separately 
        '''
        #load Other Layers to shave off 1 second when restarting

        # What are the names of the layers?
        platform_damage = 'damage_platforms'
        platform_decor = 'uninteractable_platform_decor'
        back_decor = 'decor_behind_player'
        front_decor = 'decor_infront_player'


        # Read in the tiled map
        level1_map = arcade.tilemap.read_tmx(os.path.join(st.current_path, 'game_assets\maps\imporved_map.tmx'))

        self.platforms_damage_list = arcade.tilemap.process_layer(
            map_object=level1_map,layer_name=platform_damage,scaling=st.MAP_SCALING,use_spatial_hash=True)                 
        self.uninteractable_decor_list = arcade.tilemap.process_layer(
            map_object=level1_map,layer_name= platform_decor,scaling=st.MAP_SCALING,use_spatial_hash=False)        
        self.back_decor_list = arcade.tilemap.process_layer(
            map_object=level1_map,layer_name= back_decor,scaling=st.MAP_SCALING,use_spatial_hash=False)                   
        self.front_decor_list = arcade.tilemap.process_layer(
            map_object=level1_map,layer_name= front_decor,scaling=st.MAP_SCALING,use_spatial_hash=False)     

    def setup(self):
        '''
        Set up the game here. Call this function to restart the game.
        '''
    
        # Used to keep track of our scrolling
        self.view_bottom = st.PLAYER_START_Y - 50
        self.view_left = st.PLAYER_START_X  - 300

        # Keep track of the score
        self.points = 0

        # Speedrun Timer
        self.total_time = 0.0
                 
        # Create the Sprite lists
        self.empty_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        # Read in the tiled map to Reload Coins
        level1_map = arcade.tilemap.read_tmx(os.path.join(st.current_path, 'game_assets\maps\imporved_map.tmx'))
        coins = 'animated_coins'
        self.coins_list = arcade.tilemap.process_layer(
            map_object=level1_map,layer_name=coins,scaling=st.MAP_SCALING,use_spatial_hash=True)
        # Experiment with adding a background over player sprite
        self.background_bottom_sprite = sp.Background_sprites(0 ,'game_assets\\tilesets\pack-1\\background_0(1).png')
        self.background_mid_sprite =  sp.Background_sprites(-0.375, 'game_assets\\tilesets\pack-1\\background_1(2).png')
        self.background_top_sprite = sp.Background_sprites(0.675, 'game_assets\\tilesets\pack-1\\background_2(4).png')
        self.background_list.append(self.background_bottom_sprite)
        self.background_list.append(self.background_mid_sprite)
        self.background_list.append(self.background_top_sprite)
        
        # Set up the player, specifically placing it at these coordinates.
        self.player_sprite = sp.Main_character()
        self.player_sprite.center_x = st.PLAYER_START_X
        self.player_sprite.center_y = st.PLAYER_START_Y
        self.player_list.append(self.player_sprite)
    

        # Load the physics engine for this map
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,self.platforms_list, st.GRAVITY)
        self.physics_engine_background_0 = arcade.PhysicsEngineSimple(self.background_bottom_sprite, self.empty_list)
        self.physics_engine_background_1 = arcade.PhysicsEngineSimple(self.background_mid_sprite, self.empty_list)
        self.physics_engine_background_2 = arcade.PhysicsEngineSimple(self.background_top_sprite, self.empty_list)
        self.played_backgroud_music = None  
                 

    def on_show(self):
        self.window.set_mouse_visible(False)
        if self.played_backgroud_music is None:
            self.played_backgroud_music =  self.background_music.play(0.05,loop = True)
        self.background_music.set_volume(0.05, self.played_backgroud_music) 

    def process_keychange(self):
        '''
        Called when we change a key up/down or we move on/off a ladder.
        '''
        # Process up/down
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.can_jump(y_distance=10) and not self.jump_needs_reset:
                self.player_sprite.change_y = st.PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
                self.jump_sound.play(0.5)
        elif self.down_pressed and not self.up_pressed:
                self.player_sprite.change_y = -st.PLAYER_MOVEMENT_SPEED

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = st.PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -st.PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0            

    def on_key_press(self, key, modifiers):
        '''
        Called whenever a key is pressed.
        '''

        if self.player_sprite.dead:
            return
       
        if key == arcade.key.ESCAPE:
            self.up_pressed = False
            self.down_pressed = False
            self.left_pressed = False
            self.right_pressed = False
            pause_view = gm.PauseView(self.ui_manager, self)
            self.window.show_view(pause_view)
        elif key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
            self.player_sprite.character_face_direction = st.LEFT_FACING
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.character_face_direction = st.RIGHT_FACING
            self.right_pressed = True
        
        self.process_keychange()    
            
    def on_key_release(self, key, modifiers):
        '''
        Called when the user releases a key.
        '''
        if self.player_sprite.dead:
            return

        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
        
        self.process_keychange()    

    def draw_main(self):
        # Draw our sprites
        self.background_list.draw()
        self.platforms_list.draw()
        self.platforms_damage_list.draw()
        self.back_decor_list.draw()
        self.uninteractable_decor_list.draw()
        self.coins_list.draw()
        self.player_sprite.draw()
        self.front_decor_list.draw()

    def on_draw(self):
        '''
        Render the screen.
        '''

        # Start timing how long this takes
        start_time = timeit.default_timer()

        # --- Calculate FPS

        fps_calculation_freq = 60
        # Once every 60 frames, calculate our FPS
        if self.frame_count % fps_calculation_freq == 0:
            # Do we have a start time?
            if self.fps_start_timer is not None:
                # Calculate FPS
                total_time = timeit.default_timer() - self.fps_start_timer
                self.fps = fps_calculation_freq / total_time
            # Reset the timer
            self.fps_start_timer = timeit.default_timer()
        # Add one to our frame count
        self.frame_count += 1

        arcade.start_render()
        # Code to draw the screen goes here
        self.draw_main()
        
        score_text = f'Points: {self.points}'
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom, arcade.csscolor.WHITE, 18, font_name = st.FONT)

        if st.STATS:
         # Display timings
            output = f'Processing time: {self.processing_time:.3f}'
            arcade.draw_text(output, 10 + self.view_left, 650 + self.view_bottom, arcade.color.MEDIUM_SPRING_GREEN, 15, font_name = st.FONT)

            output = f'Drawing time: {self.draw_time:.3f}'
            arcade.draw_text(output, 10 + self.view_left, 670 + self.view_bottom, arcade.color.MEDIUM_SPRING_GREEN, 15, font_name = st.FONT)

            if self.fps is not None:
                output = f'FPS: {self.fps:.0f}'
                arcade.draw_text(output, 10 + self.view_left, 690 + self.view_bottom, arcade.color.MEDIUM_SPRING_GREEN, 15, font_name = st.FONT)

        # Stop the draw timer, and calculate total on_draw time.
        self.draw_time = timeit.default_timer() - start_time    


    def scroll_screen(self):
        '''
        Scroll Screen to player movement
        '''
        # Track if we need to change the viewport        
        changed = False

        # Scroll left
        left_boundary = self.view_left + st.LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + st.SCREEN_WIDTH - st.RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + st.SCREEN_HEIGHT - st.TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + st.BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)
            self.window.view_port = self.view_left, self.view_bottom

            # Do the scrolling
            self.window.adjust_port()

            self.background_bottom_sprite.left = self.view_left
            self.background_bottom_sprite.bottom = self.view_bottom
            self.background_mid_sprite.bottom = self.view_bottom
            self.background_top_sprite.bottom = self.view_bottom
           
    def on_update(self, delta_time):
        '''
        Movement and game logic 
        '''
        # Start timing how long this takes
        start_time = timeit.default_timer()

        # Move the player with the physics engine
        self.physics_engine.update()
        self.physics_engine_background_0.update()
        self.physics_engine_background_1.update()
        self.physics_engine_background_2.update()
    

        # Play the animations
        self.background_mid_sprite.update_animation(self.view_left, delta_time)
        self.background_top_sprite.update_animation(self.view_left, delta_time)
        self.player_sprite.update_animation(self.platforms_list, delta_time)

        # Add to timer
        self.total_time += delta_time
        
        # --- Manage Scrolling ---
        self.scroll_screen()
        # --- Manage Game Mechanics ---
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coins_list)
        platforms_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.platforms_damage_list)

        for coin in coin_hit_list:            
            points = int(coin.properties['Points'])
            self.points += points
            # Remove the coin
            coin.remove_from_sprite_lists()
            # Play a sound
            self.collect_coin_sound.play(0.05)

        if len(platforms_hit_list) > 0:
            self.player_sprite.stop()
            self.player_sprite.dead = True

        if(self.player_sprite.center_y < 300):
            self.view_bottom = st.PLAYER_START_Y - 50
            self.view_left = st.PLAYER_START_X  - 300 
            self.player_sprite.center_y = st.PLAYER_START_Y
            self.player_sprite.center_x = st.PLAYER_START_X
        
        if(self.player_sprite.bottom == st.PLAYER_END_X and st.PLAYER_END_Y[0] <= self.player_sprite.center_x <= st.PLAYER_END_Y[1]) or self.player_sprite.dead:
            game_over_view = gm.GameOverView(self.ui_manager, self)
            self.window.show_view(game_over_view)       

        # Stop the draw timer, and calculate total on_draw time.
        self.processing_time = timeit.default_timer() - start_time