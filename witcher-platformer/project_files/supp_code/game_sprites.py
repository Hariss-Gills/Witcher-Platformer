'''
Sprites used within the game
'''

from . import game_settings as st
import os, arcade

   #- - - Animation Helpers - - -#

def load_animation(type, frames_start, frames_end):
    '''
    Load the all the frames for the animation in a loop
    '''
    path = os.path.join(st.ASSET_PATH, f'sprites\main_character\{type}\\')
    textures = []
    for i in range(frames_start, frames_end):
        texture = load_texture_pair(f'{path}Fullmain_{type}_{i}.png')
        textures.append(texture)
    return textures    
            
def load_texture_pair(filename):
    '''
    Load a texture pair, with the second being a mirror image
    '''
    return [
         arcade.load_texture(filename),
         arcade.load_texture(filename, flipped_horizontally=True)
     ]


        #- - - Sprites - - -#
class Main_character(arcade.Sprite):
    '''
    Sprite Class to animate background clouds
    '''
    def __init__(self):
         super().__init__()

         # Default to face-right
         self.character_face_direction = st.RIGHT_FACING

         # Used for flipping between image sequences
         self.cur_texture = 0
         self.scale = st.CHARACTER_SCALING
        
         # Track our state
         self.dead = False

         # Timer to track time
         self.time_counter = 0.0

        # --- Load Textures ---

         # Load textures for idling
         self.idle_textures = load_animation('idle', 0, 4)

        # Load textures for running
         self.run_textures = load_animation('run', 0, 6)
         
        # Load textures for jumping
         self.jump_textures = load_animation('jump+fall', 0, 5)

        # Load textures for falling
         self.fall_textures = load_animation('jump+fall', 5, 8)
         
        # Load textures for landing
         self.land_textures = load_animation('jump+fall', 8, 10)
         
        # Load textures for death
         self.death_textures = load_animation('death', 0, 5)
                                   
        # Set the initial texture
         self.texture = self.idle_textures[0][0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # self.set_hit_box([[-22, -64], [22, -64], [22, 28], [-22, 28]])
         self.set_hit_box(self.texture.hit_box_points)
    
    def cycle_animation(self, delta_time, animation_textures, frame_speed):
        '''
        Cycle through images to animate sprite with delta_time
        '''
        self.time_counter += delta_time
        while self.time_counter > frame_speed / 1000.0:
            self.time_counter -= frame_speed / 1000.0
            self.cur_texture += 1
            if self.cur_texture >= len(animation_textures):
                self.cur_texture = 0  
            self.texture = animation_textures[self.cur_texture][self.character_face_direction]     

    def update_animation(self, platforms, delta_time: float = 1/60):
        '''
        Run animations conditionally
        '''
        # Death animation
        if self.dead:
            self.cycle_animation(delta_time, self.death_textures, 200)
            self.texture = self.death_textures[4][self.character_face_direction]
            return           
        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.cycle_animation(delta_time, self.idle_textures, 125)
            return
        # Run animation    
        elif self.change_x != 0 and self.change_y == 0:
            self.cycle_animation(delta_time, self.run_textures, 100)
            return         
        # Jump animation
        if self.change_y > 0:
            self.cycle_animation(delta_time, self.jump_textures, 175)
            return
        # Fall animation    
        elif self.change_y < 0:
            self.cycle_animation(delta_time, self.fall_textures, 100)
            # Land Animation            
            if len(arcade.get_sprites_at_point([self.center_x, self.bottom - 30], platforms)) > 0:
                self.cycle_animation(delta_time, self.land_textures, 175)
                return            
class Background_sprites(arcade.Sprite):
    '''
    Sprite Class to animate background clouds
    '''
    def __init__(self, change_x, texture):
        # Set up parent class
        super().__init__()
    
        self.texture = arcade.load_texture(os.path.join(st.ASSET_PATH, texture))
        self.change_x = change_x  
        
    def update_animation(self, view_left, delta_time: float = 1/60):
        '''
        Run animations unconditionally
        '''
        view_left = view_left

        if self.left > view_left + st.SCREEN_WIDTH + st.RIGHT_VIEWPORT_MARGIN:
            self.right = view_left

        if self.right < view_left:
            self.left = view_left + st.SCREEN_WIDTH + st.RIGHT_VIEWPORT_MARGIN