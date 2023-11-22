import socket
import threading
import random

Made_dict = {#족보의 딕셔너리
        #광땡포함 떙
        '00': ('lose', -999),
        '1010': ('장땡',16),
        '1G3G': ('13광땡',17),
        '1G8G': ('18광땡',18),
        '3G8G': ('38광땡',19),
        '1G1': ('1땡',7), '3G3': ('3땡',9), '8G8': ('8땡',14),##G들어가는 거 조심
        '22': ('2땡',8), '44': ('4땡',10), '55': ('5땡',11), '66': ('6땡',12), '77': ('7땡',13), '99': ('9땡',15),
        ##여기부터 족보
        '12' : ('알리',6), '1G2' : ('알리',6),
        '14' : ('독사',5), '1G4' : ('독사',5),
        '19' : ('구삥',4), '1G9' : ('구삥',4),
        '110' : ('장삥',3), '1G10' : ('장삥',3),
        '104' : ('장사',2), '46' : ('세륙',1)
    }

def check_Made(player):#족보인지 끗인지 구분하는 definition
    card1 = player[0]
    card2 = player[1]
    if card1 + card2 in Made_dict:
        print(Made_dict[card1 + card2][0])
        return Made_dict[card1 + card2][0]
    elif card2 + card1 in Made_dict:
        print(Made_dict[card2 + card1][0])
        return Made_dict[card2 + card1][0]
    else:
        gguet = calculate_gguet(card1, card2)
        return gguet

def calculate_gguet(card1, card2):#몇 끗인지 계산하는 것
    if 'G' in card1:
        card1 = card1.replace('G', '')  # G는 삭제하고 int형으로 바꿔서 나머지 계산하기
    if 'G' in card2:
        card2 = card2.replace('G', '')
    return (int(card1) + int(card2)) % 10


def check_score(player):#승자를 정하기 위해 사용하는 definition이며, Made_dict의 경우 계산하기 쉽게 int형의 value도 함께 저장
    card1 = player[0]
    card2 = player[1]
    if card1 + card2 in Made_dict:
        return Made_dict[card1 + card2][1]
    elif card2 + card1 in Made_dict:
        return Made_dict[card2 + card1][1]
    else:
        gguet = calculate_gguet(card1, card2) - 9 ##이렇게하면 끗도 순서대로 할 수 있음
        return gguet

def check_winner(A, B, C):
    global totalCharge, playerCharge
    if A > B and A > C:
        playerCharge[0] += totalCharge#승리한 플레이어의 통장에 돈 넣어준다.
        totalCharge = 0
        return "Player A WIN"
    elif B > A and B > C:
        playerCharge[1] += totalCharge
        totalCharge = 0
        return "Player B WIN"
    elif C > A and C > B:
        playerCharge[2] += totalCharge
        totalCharge = 0
        return "Player C WIN"
    else:
        return "DRAW"#비긴 경우 배팅 금액 저장소의 금액을 그대로 가지고 간다.(묻고 더블)
    
def start_server():
    global cards, playerA, playerB, playerC, playerCharge, totalCharge
    players = [playerA, playerB, playerC]
    clients = []

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('192.168.0.9', 8011))#같은 wifi, 서버의 IPv4주소 기입, 포트 번호 임의로 정한 후 클라이언트도 알아야 함.
    server.listen(3)  # 최대 3명의 클라이언트까지 허용

    print("서버 대기 중...")

    # 클라이언트가 3명 모두 접속할 때까지 대기
    while len(clients) < 3:
        client, addr = server.accept()
        print(f"연결 수락: {addr}")
        clients.append(client) 

    while(True):
        # 각 클라이언트에게 카드 1장씩 나눠주기
        for client_index, client in enumerate(clients):#리스트를 인덱스별로 for 문 돌릴 때 사용
            playerCharge[client_index] = playerCharge[client_index] - 100
            totalCharge = totalCharge + 100
            dealt_cards = random.choice(cards[1:20])
            print(dealt_cards)
            players[client_index].append(dealt_cards)#extend 사용시 10같은 카드가 '1', '0' 으로 나눠지기 때문에 append 사용해야함
            cards.remove(dealt_cards)

        for client_index, client in enumerate(clients):
            response = f"Player {chr(ord('A') + client_index)}: {players[client_index]}"
            client.send(response.encode('utf-8'))

        for client_index, client in enumerate(clients):
            # 플레이어가 'yes'를 선택하면 추가 카드를 받을 수 있음
            ing = client.recv(1024).decode('utf-8')
            if ing == 'yes' and cards:
                playerCharge[client_index] = playerCharge[client_index] - 100
                totalCharge = totalCharge + 100
                dealt_card = random.choice(cards[1:20])
                players[client_index].append(dealt_card)
                cards.remove(dealt_card)
                client.send((f"Player {chr(ord('A') + client_index)}: {players[client_index]}").encode('utf-8'))
                #각 플레이어들에게 어떤 카드를 받았는지 정보를 보내줌            
                made = check_Made(players[client_index])
                client.send((f"Player {chr(ord('A') + client_index)}'s made: {made}").encode('utf-8'))
                #각 플레이어들에게 어떤 족보인지 정보를 보내줌.(다만 카드 2장이어야 족보이기 때문에 두 번째 yes에서 보냄)

            elif ing == 'no':
                players[client_index] = ['0','0']#'no'이면 플레이어의 카드를 00으로 바꾼다. 이는 -999점으로 무조건 지게 되어있다.

        for client_index, client in enumerate(clients):
                if ing == 'no' :
                    break
                else :
                    ing2 = client.recv(1024).decode('utf-8')
                    if ing2 == 'no' :
                        players[client_index] = ['0','0']
                        #서버에서 오류 확인용
                        print(players[0],players[1], players[2])
                        print(check_score(players[0]),check_score(players[1]),check_score(players[2]))
                        print(check_winner(int(check_score(players[0])), int(check_score(players[1])),int(check_score(players[2]))))
            

        # 게임 결과 확인 및 전송
        # 계속하실건가요?이때
        result = check_winner(int(check_score(players[0])), int(check_score(players[1])),int(check_score(players[2])))
        print(int(check_score(playerA)),"    그리고    ",int(check_score(playerB)), int(check_score(players[2])))
        
        for client_index, client in enumerate(clients):
            client.send(result.encode('utf-8'))
            client.send((f"Player {chr(ord('A') + client_index)}의 남은 잔고는 {playerCharge[client_index]}원입니다.").encode('utf-8'))
        for client in clients:
            end = client.recv(1024).decode('utf-8')
            if (end == 'no'):
                client.close()
        cards = ['00','1', '1G', '2', '2', '3', '3G', '4', '4', '5', '5', '6', '6', '7', '7', '8', '8G', '9', '9', '10', '10']
        players[0].clear()
        players[1].clear()
        players[2].clear()
        


if __name__ == "__main__":
    cards = ['00','1', '1G', '2', '2', '3', '3G', '4', '4', '5', '5', '6', '6', '7', '7', '8', '8G', '9', '9', '10', '10']
    playerA = []
    playerB = []
    playerC = []
    result = []
    playerCharge = [1500, 1500, 1500]#각 플레이어의 통장 개념
    totalCharge = 0#참가비, 배팅 금액이 모여 있는 곳
    start_server()