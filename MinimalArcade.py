import arcade
import pathlib
from enum import auto, Enum


class MoveEnum(Enum):
    NONE = auto()
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class MinimalSprite(arcade.Sprite):
    def __init__(self, ship_path: str, speed: int, game_window):
        super().__init__(ship_path)
        self.speed = speed
        self.game = game_window

    def move(self, direction: MoveEnum):
        # as a class exercise, lets fix this so it doesn't go off the window
        if direction == MoveEnum.UP:
            self.center_y += self.speed
        elif direction == MoveEnum.DOWN:
            self.center_y -= self.speed
        elif direction == MoveEnum.LEFT:
            self.center_x -= self.speed
        elif direction == MoveEnum.RIGHT:
            self.center_x += self.speed
        else:  # should be MoveEnum.NONE
            pass


class MimimalArcade(arcade.Window):

    def __init__(self, image_name: str, screen_w: int = 1024, screen_h: int = 1024):
        super().__init__(screen_w, screen_h)
        self.image_path = pathlib.Path.cwd() / 'Assets' / image_name
        self.pict = None
        self.direction = MoveEnum.NONE
        self.pictlist = None

    def setup(self):
        self.pict = MinimalSprite(str(self.image_path), speed=3, game_window=self)
        self.pict.center_x = 500
        self.pict.center_y = 500
        self.pictlist = arcade.SpriteList()
        self.pictlist.append(self.pict)

    def on_update(self, delta_time: float):
        # to get really smooth movement we would use the delta time to
        # adjust the movement, but for this simple version I'll forgo that.
        self.pict.move(self.direction)

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        # Code to draw the screen goes here
        self.pictlist.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
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
    window = MimimalArcade("PlayerShip.png", screen_w=1080)
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
