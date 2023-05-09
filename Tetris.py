import pygame
import time
import random
from dataclasses import dataclass

#khởi tạo mudule của game
pygame.init()
#Set kích thước (Ngang - 400, Cột - 15, Dòng - 30)
width, columns, rows, temp = 400, 15, 30, 0
#khoản cách 
distance = width // columns #400 / 15 = 26
#chiều cao
height = distance * rows 
#lưới 
grid = [0] * columns * rows
#tốc độ
speed, score, level = 1000, 0, 1 
#load hình
picture = []
for i in range(8):
    picture.append(pygame.transform.scale(pygame.image.load(f'T_{i}.jpg'),(distance,distance )))

screen = pygame.display.set_mode([width, height])
#tiêu đề game
pygame.display.set_caption('Game Xếp Gạch')
#tạo sự kiện 
tetroromino_down = pygame.USEREVENT + 1

pygame.time.set_timer(tetroromino_down, speed)

pygame.key.set_repeat(1,100)
#Block gạch cho các chữ cái O, I, J, L, S, Z, T
tetrorominos = [
                #0
                [0,1,1,0,
                 0,1,1,0,
                 0,0,0,0],
                #I
                [0,0,0,0,
                 2,2,2,2,
                 0,0,0,0],
                #J
                [0,0,0,0,
                 3,3,3,0,
                 0,0,3,0,
                 0,0,0,0],
                #L  
                [0,0,4,0,
                 4,4,4,0,
                 0,0,0,0,
                 0,0,0,0],
                #S
                [0,5,5,0,
                 5,5,0,0,
                 0,0,0,0,
                 0,0,0,0],
                #Z
                [0,6,6,0,
                 0,0,6,6,
                 0,0,0,0,
                 0,0,0,0],
                #Tcl
                [0,0,0,0,
                 7,7,7,0,
                 0,7,0,0,
                 0,0,0,0],
                ]

#tạo lớp và định nghĩa
@dataclass
class tetroromino():
    tetro: list
    row: int = 0 # Vị trí xuất hiện lần đầu
    column: int = 5 
    
    def show(self):
        #i là chỉ số 
        #color từ 1-7
        for i, color in enumerate(self.tetro):
            #Nếu ô nào được đánh số từ 1-7 -> Tính toán lại tọa độ x, y
            if color > 0:
                x = (self.column + i % 4) * distance
                y = (self.row + i //4) * distance
                #Cập nhập lên màn hình
                screen.blit(picture[color],(x,y))
    #kiểm tra biên 2 bên
    def check(self, r, c):
        for i, color in enumerate(self.tetro):
            if color > 0:
                rs = r + i // 4
                cs = c + i % 4
                if rs >= rows or cs < 0 or cs >= columns or grid[rs * columns + cs] > 0:
                    return False
        return True  
    #gạch rơi xuống từng ô 
    def update(self, r, c):
        if self.check(self.row + r, self.column + c):
            self.row += r
            self.column += c
            return True
        return False
    #hàm xoay
    def rotate(self):
        savetetro = self.tetro.copy()
        for i, color in enumerate(savetetro):
            self.tetro[(2-(i % 4)) * 4 + (i // 4)] = color
        if not self.check(self.row, self.column):
            self.tetro = savetetro.copy()
             
#hàm gọi lại
def ObjectOnGridline():
    for i, color in enumerate(character.tetro):
        if color > 0:
            grid[(character.row + i//4) * columns + (character.column + i%4)] = color

# hàm xóa dòng
def DeleteAllRows():
    fullrows = 0
    for row in range(rows):
        for column in range(columns):
            if grid [row * columns + column] == 0: #in ra một cột có 30 số 0 #kiểm tra nếu dòng nào có ô rỗng thì bỏ qua
                break
        else:
            del grid[row * columns : row + columns + columns]
            grid[0:0] = [0] * columns #trả về []
            fullrows += 1
    return fullrows**2*100 # điểm nhân đôi khi xóa càng nhiều dòng
        
character = tetroromino(random.choice(tetrorominos))
status = True
while status:
    pygame.time.delay(100)
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:
            status = False
        if event.type ==  tetroromino_down:
            if not character.update(1,0):
                ObjectOnGridline()
                score += DeleteAllRows()
                if score > 0 and score // 500 >= level and temp != score:
                    speed = int(speed * 0.8)
                    pygame.time.set_timer(tetroromino_down, speed)
                    level = score // 500 + 1 # tăng level khi 500 điểm
                character = tetroromino(random.choice(tetrorominos))
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character.update(0, -1)
            if event.key == pygame.K_RIGHT:
                character.update(0, 1)
            if event.key == pygame.K_DOWN:
                character.update(1, 0)
            if event.key == pygame.K_SPACE:
                character.rotate() 
    screen.fill((128,128,128))
    character.show()
    textsurface = pygame.font.SysFont('conslas', 40).render(f'{score:,}', False,(255,255,255))
    screen.blit(textsurface,(width//2 - textsurface.get_width()//2,5))
    textsurface = pygame.font.SysFont('conslas', 20).render(f'Level: {level}', False,(255,255,255))
    screen.blit(textsurface,(width//2 - textsurface.get_width()//2,55))
    for i, color in enumerate(grid):
        if color > 0:
            x = i % columns * distance 
            y = i // columns * distance 
            screen.blit(picture[color], (x,y)) 
    pygame.display.flip()
pygame.quit()
