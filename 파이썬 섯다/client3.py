import socket
import tkinter as tk
from tkinter import simpledialog

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#서버의 ip 주소와 서버의 포트 번호를 적어준다.
#단, 같은 네트워크 안에서 실행되어야 한다.
client.connect(('192.168.0.9', 8011))

#텍스트 창 띄워주기
application_window = tk.Tk()
text_widgiet = tk.Text(application_window)
text_widgiet.pack()


while True :
    #카드 정보 받기
    text_widgiet.insert(tk.END,"참가비 -100원\n")
    #카드를 한 장 받음
    response = client.recv(1024).decode('utf-8')
    text_widgiet.insert(tk.END,response)
    text_widgiet.insert(tk.END,"\n")
    
    #추가 진행 여부 묻기
    #ing = input("계속하실건가요? (yes/no): ")
    #답은 yes or no로 한정
    ing = simpledialog.askstring("Input", "계속하실건가요? (yes/no)",
                                    parent=application_window)

    client.send(ing.encode('utf-8'))

    if (ing == 'yes') :
        text_widgiet.insert(tk.END,"참가비 -100원\n")
        #카드를 한 장 더 받음
        response = client.recv(1024).decode('utf-8')
        text_widgiet.insert(tk.END,response)
        text_widgiet.insert(tk.END,"\n")
        #자신의 족보를 알려줌
        made = client.recv(1024).decode('utf-8')
        text_widgiet.insert(tk.END,made)
        text_widgiet.insert(tk.END,"\n")
        #추가 진행 여부 묻기
        ing2 = simpledialog.askstring("Input", "계속하실건가요? (yes/no)",
                                    parent=application_window)
        client.send(ing2.encode('utf-8'))

    #게임 결과를 받음
    result = client.recv(1024).decode('utf-8')
    text_widgiet.insert(tk.END,result)
    text_widgiet.insert(tk.END,"\n")
    #남은 잔고를 보여줌
    remainCharge = client.recv(1024).decode('utf-8')
    text_widgiet.insert(tk.END,remainCharge)
    text_widgiet.insert(tk.END,"\n")

    #게임 결과 받기
    end = simpledialog.askstring("Input", "게임을 계속하실건가요? (yes/no)",
                                    parent=application_window)
    client.send(end.encode('utf-8'))
    if end == "no" :
        break
    
    #매 판 끝날때마다 텍스트를 지워줌
    text_widgiet.delete(1.0,"end")

application_window.mainloop()
