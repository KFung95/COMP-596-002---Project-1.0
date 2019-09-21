import arcade
import pathlib
from enum import auto, Enum


class MoveEnum(Enum):
    NONE = auto()
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Ship(arcade.Sprite):
    def __init__(self, ship_path: str, speed: int, game_window):
        super().__init__(ship_path)
        self.speed = speed
        self.game = game_window

    def move(self, direction: MoveEnum):
        # as a class exercise, lets fix this so it doesn't go off the window
        if direction == MoveEnum.UP and self.center_y < 990:
            self.center_y += self.speed
        elif direction == MoveEnum.DOWN and self.center_y > 30:
            self.center_y -= self.speed
        elif direction == MoveEnum.LEFT and self.center_x > 35:
            self.center_x -= self.speed
        elif direction == MoveEnum.RIGHT and self.center_x < 1048:
            self.center_x += self.speed
        else:  # should be MoveEnum.NONE
            pass


class Bullet(arcade.Sprite):
    def __init__(self, bullet_path: str, game_window):
        super().__init__(bullet_path)
        self.game = game_window


class MimimalArcade(arcade.Window):
    def __init__(self, image_name: str, back_image: str, sound: str, shot: str, screen_w: int = 1024,
                 screen_h: int = 1024):
        super().__init__(screen_w, screen_h)
        self.will_shoot = False
        self.image_path = pathlib.Path.cwd() / 'Assets' / image_name
        self.image_back = pathlib.Path.cwd() / 'Assets' / back_image
        self.image_shot = pathlib.Path.cwd() / 'Assets' / shot
        self.shot_sound = arcade.load_sound(str(pathlib.Path.cwd() / 'Assets' / sound))

        self.pict = None
        self.wall = None
        self.shot = None

        self.pictlist = None
        self.walllist = None
        self.shotlist = None

        self.direction = MoveEnum.NONE

    def setup(self):
        self.pict = Ship(str(self.image_path), speed=8, game_window=self)
        self.wall = arcade.Sprite(str(self.image_back), 5)
        self.shot = Bullet(str(self.image_shot), game_window=self)

        self.pictlist = arcade.SpriteList()
        self.walllist = arcade.SpriteList()
        self.shotlist = arcade.SpriteList()

        self.pict.center_x = 500
        self.pict.center_y = 500
        self.pictlist.append(self.pict)

        self.wall.center_x = 240
        self.wall.center_y = 490
        self.walllist.append(self.wall)

    def on_update(self, delta_time: float):
        # to get really smooth movement we would use the delta time to
        # adjust the movement, but for this simple version I'll forgo that.
        self.walllist.move(-5, 0)
        self.pict.move(self.direction)
        self.shotlist.move(20, 0)

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        # Code to draw the screen goes here
        self.walllist.draw()
        self.pictlist.draw()
        self.shotlist.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.SPACE:
            self.shot = Bullet(str(self.image_shot), game_window=self)
            self.shot.center_x = self.pict.center_x
            self.shot.center_y = self.pict.center_y
            self.shotlist.append(self.shot)
            arcade.play_sound(self.shot_sound)

        if key == arcade.key.UP or key == arcade.key.W:
            self.direction = MoveEnum.UP
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.direction = MoveEnum.DOWN
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.direction = MoveEnum.LEFT
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.direction = MoveEnum.RIGHT

    def on_key_release(self, key: int, modifiers: int):
        """called by arcade for keyup events"""
        if (key == arcade.key.UP or key == arcade.key.W) and \
                self.direction == MoveEnum.UP:
            self.direction = MoveEnum.NONE
        if (key == arcade.key.DOWN or key == arcade.key.S) and \
                self.direction == MoveEnum.DOWN:
            self.direction = MoveEnum.NONE
        if (key == arcade.key.LEFT or key == arcade.key.A) and \
                self.direction == MoveEnum.LEFT:
            self.direction = MoveEnum.NONE
        if (key == arcade.key.RIGHT or key == arcade.key.D) and \
                self.direction == MoveEnum.RIGHT:
            self.direction = MoveEnum.NONE


def main():
    """ Main method """
    window = MimimalArcade("Ship2.png", "Ocean.png", "laser4_0.wav", "Shot.png", screen_w=1080)
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
