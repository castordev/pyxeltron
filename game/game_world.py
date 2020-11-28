from enum import Enum

from engine.physics.movement import UP, DOWN, RIGHT, LEFT
from engine.game_world import GameWorld
from engine.physics.collisions.rectangle import Rectangle, check_collision
from game.entities.bullet import Bullet
from game.entities.enemy import Enemy
from game.entities.ship import Ship


class Action(Enum):
    MOVE_LEFT = 1
    MOVE_RIGHT = 2
    MOVE_UP = 3
    MOVE_DOWN = 4
    SHOOT = 5


class PyxelTronGameWorld(GameWorld):

    def initialize(self):
        self.add_entity(Ship(0, 0), 'ship')
        self.add_entity_to_category(Enemy(0, 8), 'enemies')

    def _handle_action(self, actions):
        ship = self.get_entity('ship')
        if not actions:
            ship.direction = None

        for action in actions:
            if action == Action.MOVE_LEFT:
                ship.orientation = LEFT
                ship.direction = LEFT
            elif action == Action.MOVE_RIGHT:
                ship.orientation = RIGHT
                ship.direction = RIGHT
            elif action == Action.MOVE_UP:
                ship.orientation = UP
                ship.direction = UP
            elif action == Action.MOVE_DOWN:
                ship.orientation = DOWN
                ship.direction = DOWN
            else:
                ship.direction = None

            if action == Action.SHOOT:
                bullet = Bullet(ship.x, ship.y, direction=ship.orientation)
                self.add_entity_to_category(bullet, 'bullets')

    def _calculate_direction_from_enemy_to_ship(self, enemy, ship):
        # the enemy chase the ship shortening the longest component distance
        x_distance = abs(enemy.x - ship.x)
        y_distance = abs(enemy.y - ship.y)
        if x_distance > y_distance:
            if enemy.x < ship.x:
                enemy.orientation = RIGHT
                enemy.direction = RIGHT
            else:
                enemy.orientation = LEFT
                enemy.direction = LEFT
        else:
            if enemy.y < ship.y:
                enemy.orientation = DOWN
                enemy.direction = DOWN
            else:
                enemy.direction = UP
                enemy.orientation = UP

    def _update_enemies(self):
        enemies = self.get_entities_by_category('enemies')
        ship = self.get_entity('ship')
        for enemy in enemies:
            self._calculate_direction_from_enemy_to_ship(enemy, ship)

    def update_scenario(self, actions):
        self._handle_action(actions)
        self._update_enemies()
        self._update_positions()
        # TODO: remove entities outside world zone render. should be configured by entity class

    def _update_collision_bullets_enemies(self):
        enemies = self.get_entities_by_category('enemies')
        bullets = self.get_entities_by_category('bullets')
        collisions = []
        if bullets and enemies:
            for idx_enemy, enemy in enumerate(enemies):
                for idx_bullet, bullet in enumerate(bullets):
                    rect_enemy = Rectangle(enemy.x, enemy.y, enemy.width, enemy.height)
                    rect_bullet = Rectangle(bullet.x, bullet.y, bullet.width, bullet.height)
                    collision = check_collision(rect_enemy, rect_bullet)
                    if collision:
                        collisions.append((idx_bullet, idx_enemy,))
        return collisions

    def _update_collision_ship_enemies(self):
        ship = self.get_entity('ship')
        enemies = self.get_entities_by_category('enemies')
        collisions = []
        rect_ship = Rectangle(ship.x, ship.y, ship.width, ship.height)
        for idx_enemy, enemy in enumerate(enemies):
            rect_enemy = Rectangle(enemy.x, enemy.y, enemy.width, enemy.height)
            collision = check_collision(rect_enemy, rect_ship)
            if collision:
                collisions.append(idx_enemy)
        return collisions

    def update_collisions(self):
        ship_enemies = self._update_collision_ship_enemies()
        bullet_enemies = self._update_collision_bullets_enemies()
        return dict(ship_enemies=ship_enemies, bullet_enemies=bullet_enemies)
