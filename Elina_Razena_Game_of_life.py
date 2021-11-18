import pygame
import sys
import random
import time


screen_width = 600
screen_height = 600
cell_size = 6
dead_color = (40, 40, 40)
alive_color = (52, 168, 83)

pygame.display.set_caption("Game of life | Elīna Ražena")

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clear_screen()
        # flip atjauno ekrānu
        pygame.display.flip()
        # spēlē ir divi saraksti. Pirmais = active grid, kurā tiek parādīta esošā šūnu paaudze, otrs = inactive grd, kurā tiek radīta nākamā šūnu paaudze. Pēc tam, inactive grid kļūst par active grid un uz ekrāna parādās nākamā paaudze
        self.active_grid = 0
        # nosaka rindu un kolonnu skaitu spēles laukumā
        self.num_columns = int(screen_width / cell_size)
        self.num_rows = int(screen_height / cell_size)
        self.grids = []
        self.create_grids()
        self.set_grid()
        self.paused = False


    # funkcija izveido divus sarakstus - viens active grid, otrs - inactive grid
    def create_grids(self):

        def create_grid():
            row = []
            # izveido sarakstu sarakstā, kurā visi ieraksti ir 0 - visas šūnas ir mirušas
            for r in range(self.num_rows):
                list_of_columns = [0] * self.num_columns
                row.append(list_of_columns)
            return row
                
        self.grids.append(create_grid())
        self.grids.append(create_grid())


    # ja value = 1 - šūna ir dzīva
    # ja value = 0 - šūna ir mirusi
    # ja value = None - random šūnas

    # funkcija aizpilda izveidotos sarakstus ar random šunām - dzīvām un mirušām (skaitļi no 0 - 1)
    def set_grid(self, value=None, grid = 0):
        for r in range(self.num_rows):
            for c in range(self.num_columns):
                if value is None:
                    cell_value = random.randint(0,1)
                else:
                    cell_value = value
                # šādi piekļūst konkrētai šūnau
                self.grids[grid][c][r] = cell_value

    # funkcija uzzīmē dzīvās un mirušās šūnas uz ekrāna atbilstoši active grid sarakstam
    def draw_grid(self):
        for r in range(self.num_rows):
            for c in range(self.num_columns):
                if self.grids[self.active_grid][r][c] == 1:
                    color = alive_color
                else:
                    color = dead_color
                pygame.draw.rect(self.screen, color, (r * cell_size, c * cell_size, cell_size, cell_size))
        pygame.display.flip()

    # nodzēš visu ekrānu
    def clear_screen(self):
        self.screen.fill(dead_color)

    # funkcija pārbauda katras šūnas 8 kaimiņus un sakaita, cik dzīvo šūnu tai ir apkārt un pieņem lēmumu - vai šūna nākamajā paaudzē  turpinās dzīvot, nomirs vai piedzims
    def check_neighbours(self, row_index, column_index):
        def get_cell(r, c):
            try:
                cell_value = self.grids[self.active_grid][r][c]
            except:
                cell_value = 0
            return cell_value

        number_alive_neighbours = 0
        number_alive_neighbours += get_cell(row_index - 1, column_index -1)
        number_alive_neighbours += get_cell(row_index - 1, column_index)
        number_alive_neighbours += get_cell(row_index - 1, column_index + 1)
        number_alive_neighbours += get_cell(row_index, column_index - 1)
        number_alive_neighbours += get_cell(row_index, column_index + 1)
        number_alive_neighbours += get_cell(row_index + 1, column_index - 1)
        number_alive_neighbours += get_cell(row_index + 1, column_index)
        number_alive_neighbours += get_cell(row_index + 1, column_index + 1)
        
        # ja šūna ir dzīva un tai kaimiņos ir 2 vai 3 citas dzīvas šūnas, tā turpina dzīvot
        if self.grids[self.active_grid][row_index][column_index] == 1 and (number_alive_neighbours == 2 or number_alive_neighbours == 3):
            return 1
        # ja šūna ir mirusi, bet tai apkārt ir 3 dzīvi kaimiņi, tā atdzīvojas
        elif self.grids[self.active_grid][row_index][column_index] == 0 and number_alive_neighbours == 3:
            return 1
        else:
        # pārējos gadījumos dzīvās šūnas nomirst vai mirušās šūnas paliek mirušas
            return 0


    # funkcija iestata inactve grid uz nākamo paaudzi un pēc tam active grid samaina uz inactie grid, lai uz ekrāna parādītos nākamā paaudze
    def new_generation(self):
        for r in range(self.num_rows):
            for c in range(self.num_columns):
                # pārbauda konkrētās šūnas kaimiņus
                next_generation = self.check_neighbours(r, c)
                self.grids[self.inactive_grid()][r][c]= next_generation


        # Samaina game_grid_inactive info ar game_grid_active (līdzīgi kā Fbonači skaitļu virknē)
        self.active_grid = self.inactive_grid()

    # iestata inactive grid uz nākamo paaudzi, jo ja active grid šūna ir dzīva check_neigbours funkcija atgriež 0, (0 + 1) % 2 = 1 --> inactive_grid 
    def inactive_grid(self):
        return((self.active_grid + 1) %2)



    # nosaka konkrētus notikumus pie tasutiņiem
    def player_events(self):
        # pygame.event.get ir saraksts ar visiem notikumiem, kas notiek spēlē
        for event in pygame.event.get():
            # ja nospiež krustiņu, spēles logs aizveras
            if event.type == pygame.QUIT:
                sys.exit()
            # ja nospiež "s", spēle tiek iepauzēta
            elif event.type == pygame.KEYDOWN:
                if event.unicode == "s":
                    if self.paused:
                        self.paused = False
                    else:
                        self.paused = True
                # ja nopiež "r", spēles laukums tiek iestatīts uz jaunu nejaušu laukumu
                if event.unicode == "r":
                    self.active_grid = 0
                    self.set_grid(None, self.active_grid)
                    self.set_grid(0, self.inactive_grid())
                    self.draw_grid()




    def run(self):
        while True:
            # pārbauda, vai spēlētājs nenospiež kādu taustiņu, vai neizslēdz spēli
            self.player_events()
            # ja spēlē nospiesta pauze, tad spēle tiek apturēta, bet joprojām spēles laukumu var randomizēt
            if self.paused:
                continue
            # tiek izveidota un parādīta jaunā paaudze
            self.new_generation()
            # tiek uzzīmēts jauns spēles laukums
            self.draw_grid()
            # pauzīte, cik ilgi cikls tiek iepauzēts ()
            time.sleep(0.05)
        




# tests
if __name__ == "__main__":
    game = Game()
    game.draw_grid()
    game.run()


    

    

