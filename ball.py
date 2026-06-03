import pygame as pg

class Ball:
    def __init__(self, x, y, width, height, speed_x, speed_y, respawn_time, fall_time):
        self.rect = pg.Rect(x, y, width, height)    #공 위치, 크기 설정
        self.speed_x = speed_x                      #공의 x축 이동 속도 설정
        self.speed_y = speed_y                      #공의 y축 이동 속도 설정
        self.active = True                          #공이 활성화 상태인지 여부 설정
        self.ball_game_started = False              #공 게임이 시작되었는지 여부 설정
        self.respawn_time = respawn_time                       #공이 비활성화된 후 경과한 시간 설정
        self.fall_time = fall_time                          #공이 비활성화된 시간을 기록하기 위한 변수 설정

    def move(self, keys):
        if not self.ball_game_started and any(keys):   #공 게임이 시작되지 않았고, 키 입력이 있을 때
            self.ball_game_started = True              #공 게임이 시작됨

        if self.ball_game_started:                     #공 게임이 시작되었을 때    
            self.rect.x += self.speed_x                #공 이동
            self.rect.y += self.speed_y

    def check_paddle_collision(self, paddle):
        if self.rect.colliderect(paddle.rect) and self.speed_y > 0:   #공이 패들과 충돌하고, 공이 아래로 이동 중일 때
            ratio = (self.rect.centerx - paddle.rect.centerx) / (paddle.rect.width / 2)
            self.speed_x = ratio*7                                    #공의 x축 이동 각도를 패들과 닿는 위치에 따라 조절
            self.speed_y *= -1                                        #공의 y축 속도를 반전

    def check_wall_collision(self, screen_width):
        if self.rect.top < 0:                                         #공이 화면 상단에 닿았을 때
            self.speed_y *= -1                                        #공의 y축 이동 방향 반전
        if self.rect.left <0 or self.rect.right > screen_width:       #공이 화면 좌우에 닿았을 때
            self.speed_x *= -1                                        #공의 x축 이동 방향 반전

    def check_brick_collision(self, bricks):
        for brick in bricks[:]:                                       #공이 벽돌과 충돌했을 때
            if self.rect.colliderect(brick):
                bricks.remove(brick)                                  #벽돌 제거
                self.speed_y *= -1                                    #공의 y축 이동 방향 반전
                break

    def check_fall(self, screen_height):
        if self.rect.bottom > screen_height+self.rect.height:         #공이 화면 하단에서 벗어났을 때
            self.active = False                                       #공이 비활성화됨
            self.ball_game_started = False                            #공 게임이 시작되지 않은 상태로 설정
            self.fall_time = pg.time.get_ticks()                      #공이 비활성화된 시간을 기록
            return True
        return False
    
    def respawn(self, paddle):
        respawn_time = pg.time.get_ticks() - self.fall_time           #공이 비활성화된 후 경과한 시간 계산
        if respawn_time > 1000:                                       #공이 비활성화된 후 1초가 지나면
            self.active = True                                        #공이 다시 활성화됨
            self.rect.topleft = (paddle.rect.centerx - self.rect.width // 2, 500)     #공의 위치 초기화
            self.speed_x, self.speed_y = 0, 6                         #공의 이동 속도 초기화

    def draw(self, screen, color):
        pg.draw.ellipse(screen, color, self.rect)                     #공 그리기
    
    def reset(self, x, y):
        self.rect.topleft = (x, y)                                    #공 위치 초기화
        self.speed_x, self.speed_y = 0, 6                             #공 이동 속도 초기화
        self.active = True                                            #공 활성화 상태로 설정
        self.ball_game_started = False                                #공 게임이 시작되지 않은 상태로 설정
        self.fall_time = 0                                            #공이 비활성화된 시간 초기화
        self.respawn_time = 0                                         #공이 비활성화된 후 경과한 시간 초기화