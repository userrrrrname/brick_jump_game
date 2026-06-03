import pygame as pg

class Jumper:
    def __init__(self, x, y, width, height, speed_x, speed_y, jump_power, gravity):
        self.rect = pg.Rect(x, y, width, height)    #점퍼 위치, 크기 설정
        self.active = True                          #점퍼가 활성화 상태인지 여부 설정
        self.speed_x = speed_x                      #점퍼 수평 이동 속도 설정
        self.speed_y = speed_y                      #점퍼 수직 이동 속도 설정
        self.jump_power = jump_power                #점퍼 점프 힘 설정
        self.gravity = gravity                      #중력 가속도 설정
        self.jumper_on_brick = False                #점퍼가 벽돌 위에 있는지 여부 설정
        self.jump_game_started = False            #점퍼 게임이 시작되었는지 여부 설정
        self.prev_bottom = self.rect.bottom

    def move(self, keys, screen_width):
        if keys[pg.K_a]:                            #왼쪽 방향키 입력 시 점퍼 이동
            self.rect.x -= self.speed_x
        if keys[pg.K_d]:                            #오른쪽 방향키 입력 시 점퍼 이동
            self.rect.x += self.speed_x
        if keys[pg.K_w] and self.jumper_on_brick:   #W 입력 시 점퍼 점프
            self.speed_y = self.jump_power
        self.prev_bottom = self.rect.bottom             #이전 프레임에서 점퍼의 바닥이 벽돌 윗면보다 위에 있었다
        self.speed_y += self.gravity
        self.rect.y += self.speed_y
    
    def landing_on_brick(self, bricks):
        for brick in bricks:
            if self.rect.colliderect(brick) and self.speed_y > 0 and self.prev_bottom <= brick.top:   #점퍼가 벽돌과 충돌했을 때
                self.rect.bottom = brick.top
                self.speed_y = 0
                break

    def check_fall(self, screen_height):
        if self.rect.top > screen_height+self.rect.height:       #점퍼가 화면 하단에서 벗어났을 때
            self.active = False             #점퍼가 비활성화됨
            return True
        return False

    def draw(self, screen, color):          #점퍼 그리기
        pg.draw.ellipse(screen, color, self.rect)

    def reset(self, x, y, speed_x, speed_y):                   #점퍼 위치 초기화
        self.rect.topleft = (x, y)
        self.speed_x, self.speed_y = speed_x, speed_y
        self.active = True
        self.jump_game_started = False
        self.jumper_on_brick = False