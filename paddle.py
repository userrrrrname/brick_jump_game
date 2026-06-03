import pygame as pg

class Paddle:
    def __init__(self, x, y, width, height, speed):
        self.rect = pg.Rect(x, y, width, height)    #패들 위치, 크기 설정
        self.speed = speed                      #패들 이동 속도 설정

    def move(self, keys, screen_width):
        if keys[pg.K_LEFT]:                 #왼쪽 방향키 입력 시 패들 이동
            self.rect.x -= self.speed
        if keys[pg.K_RIGHT]:                #오른쪽 방향키 입력 시 패들 이동
            self.rect.x += self.speed
        if self.rect.left < 0:                   #패들이 화면 왼쪽을 벗어나지 않도록 설정    
            self.rect.left = 0
        elif self.rect.right > screen_width:     #패들이 화면 오른쪽을 벗어나지 않도록 설정
            self.rect.right = screen_width

    def draw(self, screen, color):          #패들 그리기
        pg.draw.rect(screen, color, self.rect)

    def reset(self, x, y):                   #패들 위치 초기화
        self.rect.topleft = (x, y)