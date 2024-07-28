'''
GUI Project

작성자: 김민지
게임: 도형 맞추기 게임
게임설명: 1초 미만의 랜덤하게 주어진 시간 내에 화면에 주어진 두 도형과 같은 모양, 같은 색깔의 도형을 보기 중에서 클릭한다
         두 도형 중 일치하는 도형을 마우스로 아래에 주어지는 보기에서 하나만 선택하면 된다
         총 5개의 레벨로 이루어져 있으며, 네 레벨 이상 통과시 이긴다
         치트를 사용하려면 c키를 누르면 되는데, c키를 누르는 시점부터 100초가 주어지며 이는 5개의 레벨을 모두 통과하는 데에 충분한 시간이다
         치트 키는 게임 시작 전(F5를 눌러 프로그램을 시작한 직후)과 다음 레벨을 시작하기 전에 누르면 발동된다

'''

import time
import random
import gui_core as gui

w = gui.Window('시작하려면 엔터 키를 누르세요')


def initialize(timestamp):
    w.newText(10, 10, 1000, '''게임설명: 시간 내에 화면에 주어진 두 도형과 같은 모양, 같은 색깔의 도형을 보기 중에서 클릭한다
              총 5개의 레벨로 이루어져 있으며, 네 레벨 이상 통과시 이긴다

c 키를 누르면 치트가 발동됩니다 (단, 레벨이 시작되기 전에 눌러주세요. 어느 레벨이든 상관없습니다)
''', anchor='nw')
                
    w.data.maxPlay=5
    w.data.maxColors=4
    w.data.wrongCount=0
    w.data.correctCount=0

    w.data.colors=['red', 'orange', 'yellow', 'green', 'blue', 'navy', 'purple', 'pink', 'gray', 'black']
    random.shuffle(w.data.colors)
    
    w.data.s2 = []
    w.data.selectedColors = []
    count=0

    while count<w.data.maxColors:
        w.data.s2.append(w.newRectangle(count*2*100,400,100,100,w.data.colors[count], isVisible=False))
        w.data.s2.append(w.newOval((count*2+1)*100,400,100,100,w.data.colors[count], isVisible=False))

        w.data.selectedColors.append(count)
        count=count+1

    w.data.answerShapes=[
        w.newRectangle(500, 100, 100, 100, w.data.colors[0]),
        w.newOval(150, 100, 100, 100, w.data.colors[1])
        ]
    
    w.data.time_start = 0
    w.data.time_end = 0
    w.data.min_duration_wait = 0.5
    w.data.max_duration_wait = 1.0
    w.data.duration_game = 1.0
    w.data.duration_result = 3.0
    w.data.state = 0
    w.data.previous_state = 0
    

def update(timestamp):
    
    if w.data.state==0:
        if w.keys['c']:
            w.data.duration_game = 100.0
            w.newText(10, 70, 1000, '''치트 발동 중:) !!!
''', anchor='nw')
                
        if w.keys['Return']:
            w.setTitle('두 도형을 잘 봐주세요')

            w.data.time_start = timestamp
            w.data.time_end = timestamp + random.random() * (w.data.max_duration_wait - w.data.min_duration_wait) + w.data.min_duration_wait

            w.data.state = 1
    
    elif w.data.state == 1:
        if timestamp >= w.data.time_end:
            w.setTitle('다음 도형과 같은 모양, 같은 색깔의 도형을 아래 보기 중에서 클릭해주세요!')
            w.data.time_start = timestamp
            w.data.time_end = timestamp + w.data.duration_game

            idxs = list(range(8))
            random.shuffle(idxs)

            new_x = 0

            for idx in idxs:
                s = w.data.s2[idx]
                w.showObject(s)
                w.moveObject(s, new_x, None)
                new_x += 100                    

            w.data.state = 2
            w.data.time_start = timestamp
            w.data.time_end = timestamp + w.data.duration_game
    
    elif w.data.state == 2:
        if w.mouse_buttons[1]:
            number = w.getTopObjectAt(w.mouse_position_x, w.mouse_position_y)

            for idx in range(8):
                if number == w.data.s2[idx]:
                    if idx == 0 or idx == 3:
                        w.setTitle('잘하셨습니다!')
                        w.data.correctCount+=1
                        break
            else:
                w.setTitle('틀렸습니다')
                w.data.wrongCount+=1

            w.data.time_start = timestamp
            w.data.time_end = timestamp + w.data.duration_result
            
            w.data.state = 3
        
        elif timestamp >= w.data.time_end:
                w.setTitle('시간이 초과되었습니다.')
                w.data.wrongCount+=1
                w.data.state = 3
                w.data.time_end = timestamp + w.data.duration_result

    elif w.data.state == 3:
        if timestamp >= w.data.time_end:
            w.setTitle('기회가 남았습니다. 계속 진행하려면 엔터 키를 누르세요')
            
            w.data.state = 0

    if w.data.correctCount + w.data.wrongCount == w.data.maxPlay:
        if w.data.correctCount>w.data.maxPlay-2:
            w.setTitle('게임에서 이겼습니다. 엔터 키를 누르면 게임을 종료합니다.')
            if w.keys['Return']:
                w.stop()
                return
        else:
            w.setTitle('게임에서 졌습니다. 엔터 키를 누르면 게임을 종료합니다.')
            if w.keys['Return']:
                w.stop()
                return
            

    w.data.previous_state = w.data.state

    
w.initialize = initialize
w.update = update

w.start()
