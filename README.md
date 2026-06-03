# Brick Jump Game

Python과 Pygame으로 만든 2인용 벽돌깨기 + 플랫포머 게임입니다.

## 게임 소개

Brick Jump Game은 벽돌깨기와 플랫포머 요소를 합친 2인용 게임입니다.

- 1P는 벽돌 위에서 움직이고 점프하며 제한 시간 동안 살아남아야 합니다.
- 2P는 패들을 움직여 공을 튕기고 벽돌을 부숴 2P를 떨어뜨려야 합니다.
- 시간이 끝날 때까지 1P가 살아남으면 1P가 승리합니다.
- 제한 시간 안에 1P가 떨어지면 2P가 승리합니다.
-게임을 시작하기 전 입력 화면에서는 25이내의 숫자를 입력해야 합니다.
-1P는 WAD, 2P는 방향키로 조작합니다.

## 실행 방법

### 1. 저장소 다운로드

Python 3.12 환경을 권장합니다.

```bash
git clone https://github.com/userrrrrname/brick_jump_game.git
cd brick_jump_game
pip install pygame
python main.py
