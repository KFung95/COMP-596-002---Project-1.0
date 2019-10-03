import arcade
import pathlib
import time
import random
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


class Enemy(arcade.Sprite):
    def __init__(self, enemy_path: str, health: int, game_window):
        super().__init__(enemy_path)
        self.game = game_window
        self.health = health


class MimimalArcade(arcade.Window):
    def __init__(self, image_name: str, back_image: str, sound: str, shot: str, enemy: str,
                 enemy2: str, screen_w: int = 1024, screen_h: int = 1024):
        super().__init__(screen_w, screen_h)
        self.current_time = time.time()
        self.escalation_time = time.time() + 20
        self.can_shoot = 0
        self.can_spawn = time.time()
        self.can_spawn_2 = time.time()
        self.time_delay = random.randint(1, 10)
        self.time_delay_2 = random.randint(1, 10)
        self.random_y = random.randint(28, 996)
        self.score = 0
        self.image_path = pathlib.Path.cwd() / 'Assets' / image_name
        self.image_enemy = pathlib.Path.cwd() / 'Assets' / enemy
        self.image_enemy_2 = pathlib.Path.cwd() / 'Assets' / enemy2
        self.image_back = pathlib.Path.cwd() / 'Assets' / back_image
        self.image_shot = pathlib.Path.cwd() / 'Assets' / shot
        self.shot_sound = arcade.load_sound(str(pathlib.Path.cwd() / 'Assets' / sound))

        self.pict = None
        self.wall = None
        self.wall_2 = None
        self.tracker = 0
        self.image_move_speed = -5
        self.shot = None
        self.e_1 = None
        self.e_2 = None

        self.pictlist = None
        self.walllist = None
        self.shotlist = None
        self.enemylist = None

        self.direction = MoveEnum.NONE

    def setup(self):
        self.pict = Ship(str(self.image_path), speed=8, game_window=self)
        self.wall = arcade.Sprite(str(self.image_back), 5)
        self.wall_2 = arcade.Sprite(str(self.image_back), 5)
        self.shot = Bullet(str(self.image_shot), game_window=self)

        self.pictlist = arcade.SpriteList()
        self.walllist = arcade.SpriteList()
        self.shotlist = arcade.SpriteList()
        self.enemylist = arcade.SpriteList()

        self.pict.center_x = 500
        self.pict.center_y = 500
        self.pictlist.append(self.pict)

        self.wall.center_x = 1200
        self.wall.center_y = 512
        self.wall_2.center_x = -1440
        self.wall_2.center_y = 512
        self.walllist.append(self.wall)
        self.walllist.append(self.wall_2)

    def on_update(self, delta_time: float):
        # to get really smooth movement we would use the delta time to
        # adjust the movement, but for this simple version I'll forgo that.
        self.current_time = time.time()

        if self.can_spawn + self.time_delay < self.current_time:
            self.e_1 = Enemy(str(self.image_enemy), 1, game_window=self)
            self.e_1.center_x = 1150
            self.random_y = random.randint(28, 996)
            self.e_1.center_y = self.random_y
            self.enemylist.append(self.e_1)
            self.can_spawn = time.time()
            self.time_delay = random.randint(1, 10)

        for enemy in self.enemylist:
            if random.randrange(0, 200) == 60:
                print('shoot')

        seagull_collisions = [col_seagull for col_seagull in self.enemylist if
                              arcade.check_for_collision_with_list(col_seagull, self.shotlist)]

        bullet_collusion = [col_bullet for col_bullet in self.shotlist if
                            arcade.check_for_collision_with_list(col_bullet, self.enemylist)]

        if seagull_collisions:
            go_away = filter(lambda seagull: seagull in seagull_collisions, self.enemylist)
            for seagull in go_away:
                seagull.health -= 1
                if seagull.health == 0:
                    self.enemylist.remove(seagull)
                    self.score += 1

        if bullet_collusion:
            go_away_bullet = filter(lambda bullet: bullet in bullet_collusion, self.shotlist)
            for bullet in go_away_bullet:
                self.shotlist.remove(bullet)

        if self.score >= 60:
            print('game over, score met')

        gameover = [col_ship for col_ship in self.enemylist if
                    arcade.check_for_collision_with_list(col_ship, self.pictlist)]
        if gameover:
            print('game over, chef died')

        if self.escalation_time < self.current_time:
            self.image_move_speed = -8
            if self.can_spawn_2 + self.time_delay_2 < self.current_time:
                self.e_2 = Enemy(str(self.image_enemy_2), 2, game_window=self)
                self.e_2.center_x = 1150
                self.random_y = random.randint(28, 996)
                self.e_2.center_y = self.random_y
                self.enemylist.append(self.e_2)
                self.can_spawn_2 = time.time()
                self.time_delay_2 = random.randint(1, 10)

        self.walllist.move(self.image_move_speed, 0)
        self.wall.boundary_right = -120
        self.wall_2.boundary_right = -120
        if self.wall.center_x < self.wall.boundary_right and self.tracker == 0:
            self.wall_2.center_x = 2275
            self.wall_2.center_y = 512
            self.tracker = 1
        elif self.wall_2.center_x < self.wall_2.boundary_right and self.tracker == 1:
            self.wall.center_x = 2275
            self.wall.center_y = 512
            self.tracker = 0

        self.pict.move(self.direction)
        self.shotlist.move(20, 0)
        self.enemylist.move(-2, 0)

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        # Code to draw the screen goes here
        self.walllist.draw()
        self.pictlist.draw()
        self.shotlist.draw()
        self.enemylist.draw()

        # Source: http://arcade.academy/examples/sprite_collect_coins_with_stats.html?highlight=display%20text
        output = f"Seagulls Feed: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 30)

    def on_key_press(self, key, xmodifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.SPACE and self.current_time > self.can_shoot:
            self.can_shoot = self.current_time + 1
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
    window = MimimalArcade("Chef.png", "Ocean.png", "bop.wav", "Baguette.png", "Seagull.png",
                           "Seagull_2.png", screen_w=1080)
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
