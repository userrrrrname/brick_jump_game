import pygame as pg
pg.init()
import random as rd
from paddle import Paddle
from ball import Ball
from jumper import Jumper
from brick import create_bricks, draw_bricks

BLACK = (0, 0, 0)                       #색상 설정
WHITE = (255, 255, 255)                 
RED = (255, 0, 0)                     
GREEN = (0, 255, 0)                   
BLUE = (0, 0, 255)    
GRAY = (160, 160, 160)                

WIDTH, HEIGHT = 800, 600                #게임 화면 너비, 높이 설정

size = [WIDTH, HEIGHT]                  #pygame GUI 창 크기 설정
screen = pg.display.set_mode(size)
pg.display.set_caption("brick_jump")    #pygame GUI 창 게임 이름 설정

running = True                          #게임이 진행중인지 아닌지 설정
clock = pg.time.Clock()                 #게임 프레임 설정

state = "input"
brick_count_text = ""
font = pg.font.SysFont("malgungothic", 32)
big_font = pg.font.SysFont("malgungothic", 64)
small_font = pg.font.SysFont("malgungothic", 24)
brick_count = 0

paddle = Paddle(350, 550, 100, 15, 10)

ball = Ball(392, 450, 16, 16, 0, 6, 0, 0)
dead_count = 0

jumper = Jumper(0, 0, 16, 16, 5, 5, -8, 0.5)

LIMIT_TIME = 0
start_time = pg.time.get_ticks()

def is_on_brick(jumper, bricks):
    test_jumper = jumper.rect.copy()         #colliderect()는 객체끼리 겹쳐있어야 충돌로 판단, 그래서 테스트용 점퍼를 생성해서 아주 살짝 내려 colliderect() 판정 되게
    test_jumper.inflate_ip(6, 0)        #inflate로 테스터 점퍼 크기를 살짝 확장하여 벽돌 위에 있는 판정을 늘림
    test_jumper.y += 3                  #테스터 점퍼가 실제 점퍼보다 아래에 있도록 설정하여 벽돌과의 충돌 판정이 더 쉽게 되도록 함. 아래 벽돌에서 위로 올라올 때 판정이 좀 더 후함
                  

    for brick in bricks:
        if test_jumper.colliderect(brick):
            return True

    return False

while running:                          #게임이 진행중일 때
    keys = pg.key.get_pressed()         #키보드 입력 받기
    clock.tick(60)                      #게임 프레임 설정
    for event in pg.event.get():        #게임 이벤트 설정
        if event.type == pg.QUIT or keys[pg.K_ESCAPE]:       #게임 종료 이벤트 설정
            running = False             #게임이 종료되면 running을 False로 설정하여 게임 루프를 종료
        if state == "input":
            screen.fill(WHITE)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    if brick_count_text != "":
                        brick_count = int(brick_count_text)
                        if 1 <= brick_count <= 25:
                            bricks = create_bricks(brick_count, WIDTH)     #입력된 벽돌 개수에 따라 벽돌 생성
                            start_brick = min(bricks, key=lambda brick: (brick.y, brick.x)) #벽돌 중 가장 왼쪽 위의 벽돌 선택, key=lambda brick: (brick.y, brick.x) 
                                                                                            #-> y가 가장 작은 brick을 찾고 y가 같다면 x가 가장 작은 brick을 찾음
                            jumper.rect.centerx = start_brick.centerx
                            jumper.rect.bottom = start_brick.top
                            LIMIT_TIME = 5 + brick_count
                            state = "game"
                        else:
                            brick_count_text = ""                   #입력된 벽돌 개수가 25보다 크면 brick_count_text 초기화
                        

                elif event.key == pg.K_BACKSPACE:                   #백스페이스 입력 시 brick_count_text에서 마지막 문자 제거
                    brick_count_text = brick_count_text[:-1]

                elif event.unicode.isdigit():                       #숫자 입력 시 brick_count_text에 입력된 숫자 추가
                    brick_count_text += event.unicode

    if state == "input":
        title = font.render("벽돌 개수를 입력하세요 (1~25)", True, BLACK)
        text = font.render(brick_count_text, True, BLUE)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 220))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 380))

    elif state == "game":
        screen.fill(BLACK)                  #화면 배경색 설정

        ball.draw(screen, RED)  #공 그리기
        paddle.draw(screen, WHITE)  #패들 그리기
        draw_bricks(screen, bricks, WHITE)      #벽돌 그리기
        jumper.draw(screen, BLUE)  #점퍼 그리기

        elapsed_time = (pg.time.get_ticks() - start_time) // 1000                   #타이머, LIMIT_TIME - 게임이 시작된 후 경과한 시간 계산으로 남은 시간 계산
        remaining_time = LIMIT_TIME - elapsed_time
        timer_text = small_font.render(f"남은 시간: {remaining_time}", True, WHITE)
        timer_rect = timer_text.get_rect(topright=(WIDTH - 20, 20))
        screen.blit(timer_text, timer_rect)

        ball.move(keys)                     #공 이동 함수
        paddle.move(keys, WIDTH)            #패들 이동 함수

        if ball.active:
            ball.check_paddle_collision(paddle)     #공과 패들 충돌 체크 함수
            ball.check_wall_collision(WIDTH)        #공과 벽 충돌 체크 함수
            ball.check_brick_collision(bricks)      #공과 벽돌 충돌 체크 함수
            
            if ball.check_fall(HEIGHT):             #공이 화면 하단에서 벗어났는지 체크 함수
                dead_count += 1                     #죽은 횟수 증가
                if dead_count >= 5:                 #죽은 횟수가 5회 이상이면 게임 종료
                    state = "game_end_BW"

        if ball.active == False:
            ball.respawn(paddle)                    #공 리스폰 함수

        if not jumper.jump_game_started and any(keys):
            jumper.jump_game_started = True
        if jumper.jump_game_started:
            jumper.jumper_on_brick = is_on_brick(jumper, bricks)
            jumper.move(keys, WIDTH)         #점퍼 이동 함수
            jumper.landing_on_brick(bricks)   #점퍼가 벽돌에 착지했는지 체크 함수

            if jumper.check_fall(HEIGHT):       #점퍼가 화면 하단에서 벗어났는지 체크 함수
                state = "game_end_RW"              
            if remaining_time == 0:                    #남은 시간이 0이 되었을 때
                if jumper.active:
                    state = "game_end_BW"
    
    if state == "game_end_BW":
        end_text = big_font.render("BLUE WIN", True, BLUE)
        text_rect = end_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(end_text, text_rect)
    elif state == "game_end_RW":
        end_text = big_font.render("RED WIN", True, RED)
        text_rect = end_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(end_text, text_rect)

    if keys[pg.K_r] and state in ["game_end_BW", "game_end_RW"]:            #R 입력 시 게임 리셋
        state = "input"
        brick_count_text = ""
        brick_count = 0
        bricks = []
        paddle.reset(350, 550)
        ball.reset(392, 450)
        dead_count = 0
        jumper.reset(0, 0, 5, 0)
        LIMIT_TIME = 0
        start_time = pg.time.get_ticks()

    pg.display.update()
    