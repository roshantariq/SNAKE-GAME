import pygame,sys,random,asyncio
from pygame.math import Vector2 as v2

class SNAKE:
    def __init__(self):
        self.body = [v2(7,10),v2(6,10),v2(5,10)]
        self.direction = v2(1,0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            snake_rect = pygame.Rect(int(block.x * cell_size), int(block.y * cell_size), cell_size, cell_size)
            pygame.draw.rect(screen,(90,115,200),snake_rect)

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
        
    def add_block(self):
        self.new_block = True

class FRUIT:
    def __init__(self):
        self.randomize()
    
    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
        pygame.draw.rect(screen,(126,166,114),fruit_rect)
        #screen.blit(apple,fruit_rect)


    def randomize(self):
        self.x = random.randint(0,cell_number - 1)
        self.y = random.randint(0,cell_number - 1)
        self.pos = v2(self.x,self.y)

class GAME : 
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.game_over_flag = False

    def update(self) :
        if not self.game_over_flag:
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            
    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
            

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
                
    
    def game_over(self):

        self.game_over_flag = True

        game_over_text = "GAME OVER"
        game_over_surface = game_font.render(game_over_text,True,(255,255,255)) #text,antialiasing,color
        game_over_x = int(cell_size * cell_number / 2)
        game_over_y = int(cell_size * cell_number / 2)
        game_over_rect = game_over_surface.get_rect(center = (game_over_x,game_over_y))
        screen.fill((0,0,0))
        screen.blit(game_over_surface,game_over_rect)
           
       
        restart_text = "PRESS SPACE TO RESTART"
        restart_surface = game_font.render(restart_text,False,(255,255,255)) 
        restart_x = int(cell_size * cell_number / 2)
        restart_y = int(cell_size * cell_number / 2 + 50)
        restart_rect = restart_surface.get_rect(center = (restart_x,restart_y))
        screen.blit(restart_surface,restart_rect)

        pygame.display.update()
        pygame.time.delay(5000)

    def draw_score(self):

        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text,False,(100,74,12)) 
        score_x = int(cell_size * cell_number - 550)
        score_y = int(cell_size * cell_number - 550)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        screen.blit(score_surface,score_rect)

        score_text = "Score"
        score_surface = game_font.render(score_text,False,(100,74,12))
        score_x = int(cell_size * cell_number - 550)
        score_y = int(cell_size * cell_number - 570)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        screen.blit(score_surface,score_rect)        


pygame.init()
cell_size = 30
cell_number = 20
screen = pygame.display.set_mode((cell_number*cell_size,cell_number*cell_size))
clock  = pygame.time.Clock()
game_font = pygame.font.Font(None,25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

game = GAME()

async def main():
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() #Quits pygame
                sys.exit() #Quits the game
            if event.type == SCREEN_UPDATE:
                game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if game.snake.direction.y != 1:
                        game.snake.direction = v2(0,-1)
                if event.key == pygame.K_DOWN:
                    if game.snake.direction.y != -1:
                        game.snake.direction = v2(0,1)
                if event.key == pygame.K_LEFT:
                    if game.snake.direction.x != 1:
                        game.snake.direction = v2(-1,0)
                if event.key == pygame.K_RIGHT:
                    if game.snake.direction.x != -1:
                        game.snake.direction = v2(1,0)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and game.game_over:
                    game.__init__()
                    game.game_over_flag = False
                    

        screen.fill((175,215,70)) #Fills the screen with a color
        game.draw_elements()    
        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())