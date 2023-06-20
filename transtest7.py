import os
import openai
from flask import Flask, request, render_template

openai.api_key = "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"

app = Flask(__name__)

totallog = ""
dialogs = ""
messages = []

@app.route('/')
def index():
    return render_template('info.html')

def select_image(job, gender):
    
        return '/static/img/' + job + '_' + gender + '.jpeg'


@app.route('/gpt')
def gpt():   

    global dialogs, messages,totallog
    
    name = request.args.get("name","랜덤 판타지 이름으로 설정해줘") 
    personality = request.args.get("personality","랜덤 판타지 성격으로 설정해줘") 
    back = request.args.get("back","랜덤 판타지 배경을 설정해줘") 
    job = request.args.get("job","랜덤 판타지 직업을 설정해줘") 
    gender = request.args.get("gender","남자") 
    messages = [] 

    image_url = select_image(job, gender)
        
    setup = f"""
        너가 마스터가 되어 던전앤 드래곤즈를 함께 플레이 하자
        먼저 내가 플레이어 할 캐릭터 설정을 먼저 진행할게
        캐릭터 이름 : {name}
        캐릭터 성격 : {personality}
        캐릭터 배경  : {back}
        캐릭터 직업 : {job}
        캐릭터 성별 : {gender}
        여기까지가 내 캐릭터의 설정이야 그리고 이제 모험을 시작하기에 앞서서 내가 살고 있는 대륙과 지역의 정보를 
        던전 앤 드래곤즈 세계관에 적당한 그런 지명을 사용해서 랜덤하게 만들어주고 
        이제 자연스럽고 자세하게 세계관 배경을 5줄 정도로 자세하게 설명을 해주고 
        내가 TRPG를 하는 것 처럼 너가 마스터로써 상황 등을 부여해줬으면 좋겠고 
        매 상황마다 전략을 선택할 수 있게 선택지를 숫자를 매기면서 알려주는데
        반드시 그 명령을 수행하는 것이 아니라 언제나 마지막 항목으로 내가 직접 입력 할 수 있게 
        직접 선택지에 넣어줄 수 있어서 사용자가 직접 참여하거나 너가 선택지를 참고해서 이야기를 진행 할 수 있게 해줘
    """

    messages.append({"role": "user", "content": setup})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  messages=messages)

    res = completion.choices[0].message['content']
    

    res_html = "<br>".join(res.split("\n"))
    dialogs += f'<div style="margin:20px 0px">{res_html}</div>'   
    totallog += res_html
    # 응답을 messages에 추가
    messages.append({"role": "assistant", "content": res})
    
    return render_template('main.html', name=name,gender=gender,job=job,res_html=res_html,dialogs=dialogs, image_url=image_url)
    

@app.route('/chat')
def chat():
    global dialogs, messages,totallog
    prompt = request.args.get("prompt", "")

    if prompt != "":
        messages.append({"role": "user", "content": prompt})
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        res = completion.choices[0].message['content'].replace("\n", "<br/>").replace(" ", "&nbsp;")
        messages.append({"role": 'assistant', "content": res})

        # 질문과 답변을 따로 변수에 저장하고 이를 화면에 출력
        question = f'<div style="margin:20px 0px"><strong>👤 You:</strong> {prompt}</div>'
        answer = f'<div style="margin:20px 2px"><strong>🧙 Master:</strong> {res}</div>'

        # 이전 대화와 현재 대화를 합쳐서 dialogs에 저장
        totallog = totallog + prompt + res
        dialogs = question + answer
    html = f"""
        <style>
            *{{
                font-family: 'hero', sans-serif;
            }}
            body {{
                background-image: url('/static/배경.jpg');
                background-size: cover;
                backdrop-filter: blur(5px);
            }}
            @font-face {{
                font-family:"Hero";
                src: url('/static/HeirofLightBold.ttf');
            }}
        </style>

        <div style="background-image: url('/static/게시판.jpg');background-size: cover;background-repeat: no-repeat; padding: 200px;">
            <div style="max-width: 500px; margin: 0 auto;">
                <div style="display: flex; justify-content: center;">
                    <h2 style="margin-top: 280px;">환상의 대륙</h2>
                </div>
                {dialogs}
                <div style="display: flex; flex-wrap: wrap;justify-content: center;align-items: center;">
                    <form action="/chat" method="GET" style="width: 100px; padding: 5px;">
                        <input type="hidden" name="prompt" value="1">
                        <button type="submit" style="width: 100%; padding: 10px; background-color: transparent; border: none; cursor: pointer;">
                            <img src="/static/1.png" alt="Button 1" style="width: 100%; height: auto;">
                        </button>
                    </form>
                    <form action="/chat" method="GET" style="width: 110px; padding: 5px;">
                        <input type="hidden" name="prompt" value="2">
                        <button type="submit" style="width: 100%; padding: 10px; background-color: transparent; border: none; cursor: pointer;">
                            <img src="/static/2.png" alt="Button 2" style="width: 100%; height: auto;">
                        </button>
                    </form>
                    <form action="/chat" method="GET" style="width: 95px; padding: 5px;">
                        <input type="hidden" name="prompt" value="3">
                        <button type="submit" style="width: 100%; padding: 10px; background-color: transparent; border: none; cursor: pointer;">
                            <img src="/static/3.png" alt="Button 3" style="width: 100%; height: auto;">
                        </button>
                    </form>
                </div>
                <form action=/chat method="GET" style="margin-top: 20px;">
                    <input type="text" style="width: 100%; padding: 10px;" name="prompt" placeholder="Enter your message..." autocomplete="off" autofocus>
                    <input type="submit" value="Send" style="width: 100%; padding: 10px; margin-top: 10px; background-color: #4CAF50; color: white; font-weight: bold; cursor: pointer;">
                </form>
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <form action="/save_log" method="POST" style="margin-top: 40px; display: flex;">
                        <button type="submit" style="width: 75px; height: 75px; background-color: transparent; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center;">
                            <img src="/static/save.png" alt="Save" style="width: 100%; height: 100%;">
                        </button>
                    </form>
                </div>
            </div>
        </div>
    """

    return html

@app.route('/save_log', methods=['POST'])
def save_log():
    global totallog

    # 텍스트 파일에 대화 기록 저장
    with open('dialog_log.txt', 'w', encoding='utf-8') as f:
        f.write(totallog)

    html = '''

    <div style="max-width: 500px; margin: 0 auto;">
        <div style="display: flex; justify-content: center;">
            <h2 style="margin-top: 280px;">지금까지의 모험이 모두 기록됐습니다.</h2>
        </div>
    </div>
    '''

    return html


if __name__ == '__main__':
    app.run(debug=True)