import random


class Bee:
    def __init__(self, name, hive, is_scout=False, exploration_radius=3, move_range=5):
        self.name = name
        self.hive = hive
        self.x = self.hive.get_x()
        self.y = self.hive.get_y()

        self.is_scout = is_scout

        self.exploration_goal = None
        self.exploration_radius = exploration_radius
        self.move_range = move_range

        self.found_food = False
        self.found_food_source = None

    def explore(self, food_sources):
        if self.exploration_goal and not self.is_scout:
            self.move_towards_exploration_goal()
            return
        nearby_sources = [source for source in food_sources if self.is_within_radius(source)]
        if nearby_sources:
            selected_source = random.choice(nearby_sources)
            self.found_food = True
            self.found_food_source = selected_source
        else:
            self.move()

    def is_within_radius(self, food_source):
        distance = ((self.x - food_source.x) ** 2 + (self.y - food_source.y) ** 2) ** 0.5
        return distance <= self.exploration_radius

    def return_home(self):
        if self.x == self.hive.x and self.y == self.hive.y:
            if self.found_food_source not in self.hive.found_food_sources:
                self.hive.add_found_food_source(self.found_food_source)
            self.found_food = False
            self.found_food_source = None
        else:
            if self.x != self.hive.x:
                if (self.x - self.hive.x) > 0:
                    self.x -= 1
                else:
                    self.x += 1
            if self.y != self.hive.y:
                if (self.y - self.hive.y) > 0:
                    self.y -= 1
                else:
                    self.y += 1

    def move_towards_exploration_goal(self):
        if self.x == self.exploration_goal.x and self.y == self.exploration_goal.y:
            self.exploration_goal = None
        else:
            if self.x != self.exploration_goal.x:
                if (self.x - self.exploration_goal.x) > 0:
                    self.x -= 1
                else:
                    self.x += 1
            if self.y != self.exploration_goal.y:
                if (self.y - self.exploration_goal.y) > 0:
                    self.y -= 1
                else:
                    self.y += 1

    def move(self):
        self.x += int(random.uniform(-self.move_range, self.move_range))
        self.y += int(random.uniform(-self.move_range, self.move_range))

        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x > 89:
            self.x = 89
        if self.y > 199:
            self.y = 199
