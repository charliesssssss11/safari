import os 
import random
from animal import Empty, Zebra, Lion


class CircleOfLife:
    def __init__(self, world_size, num_zebras, num_lions):
        self.world_size = world_size
        self.grid = [[Empty(y, x) for y in range(self.world_size)]
                                  for x in range(self.world_size)]
        zebra_coords, lion_coords = self.get_random_coords(num_zebras, num_lions)
        for y, x in zebra_coords:
            self.grid[y][x] = Zebra(y, x) 
        for y, x in lion_coords:
            self.grid[y][x] = Lion(y, x)
        self.timestep = 0
        print('Welcome to AIE Safari!')
        print(f'\tworld size = {world_size}')
        print(f'\tnumber of zebras = {num_zebras}')
        print(f'\tnumber of lions = {num_lions}')

    def get_random_coords(self, num_zebras, num_lions):
        all_coords = [(y, x) for y in range(self.world_size)
                       for x in range(self.world_size)]
        zebra_coords = random.sample(all_coords, num_zebras)
        all_coords = list(set(all_coords) - set(zebra_coords))
        lion_coords = random.sample(all_coords, num_lions)
        return zebra_coords, lion_coords

    def display(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        print(f'Clock: {self.timestep}')
        top_coord_str = ' '.join([f'{coord}' for coord in range(len(self.grid))])
        print('   ' + top_coord_str)
        for row, line in enumerate(self.grid):
            buffer = [str(animal) for animal in line]
            print(f'{row:2} ' + ' '.join(buffer))
        key = input('enter [q] to quit:')
        if key == 'q':
            exit()

    def step_move(self):
        animals = [animal for line in self.grid for animal in line
                   if not isinstance(animal, Empty)]
        for animal in animals:
            if animal.hp != 0:
                if isinstance(animal, Lion):
                    lion = animal
                    zebra_neighbors = lion.get_neighbors(self.grid, target='Z')
                    if len(zebra_neighbors) > 0:
                        chosen_neighbor = random.choice(zebra_neighbors)
                        self.grid[lion.y][lion.x] = Empty(lion.y, lion.x)
                        lion.y, lion.x = chosen_neighbor
                        self.grid[lion.y][lion.x].hp = 0  # kill
                        self.grid[lion.y][lion.x] = lion
                    else:
                        lion.move_to(self.grid, target='.')
                else:
                    animal.move_to(self.grid, target='.')

    def step_breed(self):
        animals = [animal for line in self.grid for animal in line
                   if not isinstance(animal, Empty)
                   and animal.is_ready_to_breed()]
        for animal in animals.copy(): 
            animal.breed(self.grid)


    def housekeeping(self):
        for y, line in enumerate(self.grid):
            for x, animal in enumerate(line):
                if isinstance(animal, Lion):
                    animal.age += 1
                    if animal.hp <= 0:  
                        self.grid[y][x] = Empty(y, x)
                    elif animal.age % 3 == 0: 
                        animal.hp -= 1  
                        if animal.hp <= 0:  
                            self.grid[y][x] = Empty(y, x)






    def run(self, num_timesteps=100):
        self.display()
        for _ in range(num_timesteps):
            self.timestep += 1
            self.step_move()
            self.display()
            self.step_breed()
            self.display()
            self.housekeeping()


if __name__ == '__main__':
    world_size = 20
    num_zebras = 100
    num_lions = 5

    safari = CircleOfLife(world_size, num_zebras, num_lions)
    safari.run(10)
