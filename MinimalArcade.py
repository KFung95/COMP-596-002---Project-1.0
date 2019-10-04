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
    def __init__(self, enemy_path: str, health: int, worth: int, game_window):
        super().__init__(enemy_path)
        self.game = game_window
        self.health = health
        self.worth = worth


class MimimalArcade(arcade.Window):
    def __init__(self, image_name: str, back_image: str, sound: str, enemy_sound: str, chef_sound: str, munch: str, victory: str, defeat: str, shot: str, enemy: str,
                 enemy2: str, enemy2_v2: str, enemy_shot: str, screen_w: int = 1024, screen_h: int = 1024):
        super().__init__(screen_w, screen_h)
        self.score = None
        self.kills = None
        self.play_once = None
        self.image_path = pathlib.Path.cwd() / 'Assets' / image_name
        self.image_enemy = pathlib.Path.cwd() / 'Assets' / enemy
        self.image_enemy_2 = pathlib.Path.cwd() / 'Assets' / enemy2
        self.image_enemy_2_low_HP = pathlib.Path.cwd() / 'Assets' / enemy2_v2
        self.image_back = pathlib.Path.cwd() / 'Assets' / back_image
        self.image_shot = pathlib.Path.cwd() / 'Assets' / shot
        self.image_enemy_shot = pathlib.Path.cwd() / 'Assets' / enemy_shot
        self.shot_sound = arcade.load_sound(str(pathlib.Path.cwd() / 'Assets' / sound))
        self.spit = arcade.load_sound(str(pathlib.Path.cwd() / 'Assets' / enemy_sound))
        self.chef_hit_sound = arcade.load_sound(str(pathlib.Path.cwd() / 'Assets' / chef_sound))
        self.munch_sound = arcade.load_sound(str(pathlib.Path.cwd() / 'Assets' / munch))
        self.victory_sound = arcade.load_sound(str(pathlib.Path.cwd() / 'Assets' / victory))
        self.defeat_sound = arcade.load_sound(str(pathlib.Path.cwd() / 'Assets' / defeat))

        self.pict = None
        self.wall = None
        self.wall_2 = None
        self.tracker = None
        self.image_move_speed = None
        self.enemy_movement_speed = None
        self.shot = None
        self.e_1 = None
        self.e_2 = None

        self.current_time = None
        self.escalation_time = None
        self.can_shoot = None
        self.can_spawn = None
        self.can_spawn_2 = None
        self.time_delay = None
        self.time_delay_2 = None
        self.random_y = None

        self.pict_list = None
        self.wall_list = None
        self.shot_list = None
        self.enemy_shot_list = None
        self.enemy_list = None
        self.enemy_list_2 = None

        self.direction = MoveEnum.NONE
        self.lose = None
        self.win = None

    def setup(self):
        self.pict = Ship(str(self.image_path), speed=8, game_window=self)
        self.wall = arcade.Sprite(str(self.image_back), 5)
        self.wall_2 = arcade.Sprite(str(self.image_back), 5)
        self.shot = Bullet(str(self.image_shot), game_window=self)

        self.current_time = time.time()
        self.escalation_time = time.time() + 20
        self.can_shoot = 0
        self.can_spawn = time.time()
        self.can_spawn_2 = time.time()
        self.time_delay = 2
        self.time_delay_2 = 2
        self.random_y = random.randint(28, 996)
        self.score = 0
        self.kills = 0

        self.pict_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.shot_list = arcade.SpriteList()
        self.enemy_shot_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.enemy_list_2 = arcade.SpriteList()

        self.pict.center_x = 500
        self.pict.center_y = 500
        self.pict_list.append(self.pict)

        self.image_move_speed = -5
        self.enemy_movement_speed = -2
        self.tracker = 0
        self.wall.center_x = 1200
        self.wall.center_y = 512
        self.wall_2.center_x = -1440
        self.wall_2.center_y = 512
        self.wall_list.append(self.wall)
        self.wall_list.append(self.wall_2)

        self.play_once = True
        self.lose = False
        self.win = False

    def on_update(self, delta_time: float):
        self.current_time = time.time()
        # Enemy type 1 spawning information
        if self.can_spawn + self.time_delay < self.current_time:
            self.e_1 = Enemy(str(self.image_enemy), 1, 1, game_window=self)
            self.e_1.center_x = 1150
            self.random_y = random.randint(28, 996)
            self.e_1.center_y = self.random_y
            self.enemy_list.append(self.e_1)
            self.can_spawn = time.time()
            self.time_delay = random.randint(1, 10)

        # Random enemy shots
        for enemy in self.enemy_list:
            if random.randrange(0, 200) == 60:
                self.shot = Bullet(str(self.image_enemy_shot), game_window=self)
                self.shot.center_x = enemy.center_x
                self.shot.center_y = enemy.center_y
                self.enemy_shot_list.append(self.shot)
                arcade.play_sound(self.spit)

        # Random enemy type 2 shots
        for enemy_2 in self.enemy_list_2:
            if random.randrange(0, 200) == 60:
                self.shot = Bullet(str(self.image_enemy_shot), game_window=self)
                self.shot.center_x = enemy_2.center_x
                self.shot.center_y = enemy_2.center_y
                self.enemy_shot_list.append(self.shot)
                arcade.play_sound(self.spit)

        # Checks for collusion between seagulls and baguettes
        seagull_collisions = [col_seagull for col_seagull in self.enemy_list if
                              arcade.check_for_collision_with_list(col_seagull, self.shot_list)]

        # Checks for collusion between baguettes and seagulls
        bullet_collusion = [col_bullet for col_bullet in self.shot_list if
                            arcade.check_for_collision_with_list(col_bullet, self.enemy_list)]

        # Checks for collusion between seagulls type 2 and baguettes
        seagull_collisions_2 = [col_seagull for col_seagull in self.enemy_list_2 if
                                arcade.check_for_collision_with_list(col_seagull, self.shot_list)]

        # Checks for collusion between baguettes and seagulls type 2
        bullet_collusion_2 = [col_bullet for col_bullet in self.shot_list if
                              arcade.check_for_collision_with_list(col_bullet, self.enemy_list_2)]

        # Checks for collusion between spit and chef
        enemy_bullet_collusion = [col_enemy_bullet for col_enemy_bullet in self.enemy_shot_list if
                                  arcade.check_for_collision_with_list(col_enemy_bullet, self.pict_list)]

        # Checks for collusion between chef and seagulls
        chef_collusion = [col_ship for col_ship in self.enemy_list if
                          arcade.check_for_collision_with_list(col_ship, self.pict_list)]

        # Checks for collusion between chef and seagulls type 2
        chef_collusion_2 = [col_ship for col_ship in self.enemy_list_2 if
                            arcade.check_for_collision_with_list(col_ship, self.pict_list)]

        if chef_collusion or chef_collusion_2:
            arcade.play_sound(self.chef_hit_sound)
            self.lose = True

        if seagull_collisions:
            go_away = filter(lambda seagull: seagull in seagull_collisions, self.enemy_list)
            for seagull in go_away:
                arcade.play_sound(self.munch_sound)
                self.enemy_list.remove(seagull)
                self.score += seagull.worth
                self.kills += 1

        if bullet_collusion:
            go_away_bullet = filter(lambda bullet: bullet in bullet_collusion, self.shot_list)
            for bullet in go_away_bullet:
                self.shot_list.remove(bullet)

        if seagull_collisions_2:
            go_away = filter(lambda seagull: seagull in seagull_collisions_2, self.enemy_list_2)
            for seagull in go_away:
                arcade.play_sound(self.munch_sound)
                seagull.health -= 1

                # Sprite changes
                if seagull.health == 1:
                    new_sprite = Enemy(str(self.image_enemy_2_low_HP), 1, 5, game_window=self)
                    new_sprite.center_x = seagull.center_x
                    new_sprite.center_y = seagull.center_y
                    self.enemy_list_2.append(new_sprite)
                    self.enemy_list_2.remove(seagull)
                elif seagull.health == 0:
                    self.enemy_list_2.remove(seagull)
                    self.score += seagull.worth
                    self.kills += 1

        if bullet_collusion_2:
            go_away_bullet = filter(lambda bullet: bullet in bullet_collusion_2, self.shot_list)
            for bullet in go_away_bullet:
                self.shot_list.remove(bullet)

        if enemy_bullet_collusion:
            dead = filter(lambda enemy_bullet: enemy_bullet in enemy_bullet_collusion, self.enemy_shot_list)
            for enemy_bullet in dead:
                self.enemy_shot_list.remove(enemy_bullet)
                arcade.play_sound(self.chef_hit_sound)
                self.lose = True

        # Removes elements that go off the screen
        for all_enemies in self.enemy_list:
            if all_enemies.center_x < 0:
                self.enemy_list.remove(all_enemies)

        for all_enemies_2 in self.enemy_list_2:
            if all_enemies_2.center_x < 0:
                self.enemy_list_2.remove(all_enemies_2)

        for all_shots in self.shot_list:
            if all_shots.center_x > 1200:
                self.shot_list.remove(all_shots)

        # 60 kill winning condition
        if self.kills >= 60:
            self.win = True

        # Escalation occurs after 20 seconds pass and increases background + enemy movement speed and spawn rates
        if self.escalation_time < self.current_time:
            self.image_move_speed = -8
            self.enemy_movement_speed = -4

            # Enemy type 2 information
            if self.can_spawn_2 + self.time_delay_2 < self.current_time:
                self.e_2 = Enemy(str(self.image_enemy_2), 2, 5, game_window=self)
                self.e_2.center_x = 1150
                self.random_y = random.randint(28, 996)
                self.e_2.center_y = self.random_y
                self.enemy_list_2.append(self.e_2)
                self.can_spawn_2 = time.time()
                self.time_delay = random.randint(1, 6)
                self.time_delay_2 = random.randint(1, 6)

        if self.lose or self.win:
            if self.lose and self.play_once:
                arcade.play_sound(self.defeat_sound)
                for chef in self.pict_list:
                    self.pict_list.remove(chef)
                self.play_once = False
            elif self.win and self.play_once:
                arcade.play_sound(self.victory_sound)
                self.play_once = False

            # Freezes screen and removes enemies/shots
            self.image_move_speed = 0
            for enemy in self.enemy_list:
                self.enemy_list.remove(enemy)
            for shots in self.enemy_shot_list:
                self.enemy_shot_list.remove(shots)
            for baguettes in self.shot_list:
                self.shot_list.remove(baguettes)
            for enemy_2 in self.enemy_list_2:
                self.enemy_list_2.remove(enemy_2)

        # Infinite scrolling
        self.wall_list.move(self.image_move_speed, 0)
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
        self.shot_list.move(20, 0)
        self.enemy_list.move(self.enemy_movement_speed, 0)
        self.enemy_list_2.move(self.enemy_movement_speed, 0)
        self.enemy_shot_list.move(-10, 0)

    def on_draw(self):
        arcade.start_render()
        self.wall_list.draw()
        self.pict_list.draw()
        self.shot_list.draw()
        self.enemy_shot_list.draw()
        self.enemy_list.draw()
        self.enemy_list_2.draw()

        # Source: http://arcade.academy/examples/sprite_collect_coins_with_stats.html?highlight=display%20text
        output = f"Seagulls Fed: {self.kills}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 30)

        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 60, arcade.color.WHITE, 30)


        if self.lose:
            arcade.draw_text("Game Over", 256, 700, arcade.color.WHITE, 100)
            arcade.draw_text('Hit \'Y\' to restart or \'N\' to close', 350, 600, arcade.color.WHITE, 24)
        elif self.win:
            arcade.draw_text("You won!", 300, 700, arcade.color.WHITE, 100)
            arcade.draw_text('Hit \'Y\' to restart or \'N\' to close', 350, 600, arcade.color.WHITE, 24)

    def on_key_press(self, key, xmodifiers):
        if self.lose or self.win:
            if key == arcade.key.Y:
                self.setup()
                arcade.run()
            elif key == arcade.key.N:
                self.close()
        else:
            if key == arcade.key.SPACE and self.current_time > self.can_shoot:
                self.can_shoot = self.current_time + 1
                self.shot = Bullet(str(self.image_shot), game_window=self)
                self.shot.center_x = self.pict.center_x
                self.shot.center_y = self.pict.center_y
                self.shot_list.append(self.shot)
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
    window = MimimalArcade("Chef.png", "Ocean.png", "bop.wav", "spit.wav", "chef_hit.wav", "munch.wav", "Victory.wav", "defeat.wav", "Baguette.png", "Seagull.png",
                           "Seagull_2.png", "Seagull_2_low_HP.png", "Shot.png", screen_w=1080)
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
