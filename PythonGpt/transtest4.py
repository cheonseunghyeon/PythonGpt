import os
import openai
from flask import Flask, request
from flask import render_template

openai.api_key = "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"

app = Flask(__name__)

dialogs = ""
messages = []

@app.route('/')
def index():
    return render_template('info.html')


@app.route('/gpt')
def gpt():   
    # index가 아닌 바깥에서 사용한 전역 변수를 사용하겠다
    global dialogs, messages
    
    name = request.args.get("name","랜덤 판타지 이름으로 설정해줘") 
    personality = request.args.get("personality","랜덤 판타지 성격으로 설정해줘") 
    back = request.args.get("back","랜덤 판타지 배경을 설정해줘") 
    job = request.args.get("job","랜덤 판타지 직업을 설정해줘") 
    gender = request.args.get("gender","남자") 
    messages = []  # messages 초기화
        
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
    
    # 각 줄을 구분하기 위해 <br> 태그 사용
    res_html = "<br>".join(res.split("\n"))
    dialogs += f'<div style="margin:20px 0px">{res_html}</div>'   
    
    # 응답을 messages에 추가
    messages.append({"role": "assistant", "content": res})
    
    return render_template('main.html', name=name,gender=gender,job=job,res_html=res_html, dialogs=dialogs)

@app.route('/chat')  # 새로운 route 추가
def chat():
    global dialogs, messages
    
    prompt = request.args.get("prompt", "")

    if prompt != "" :
        messages.append({"role": "user", "content": prompt})
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        res = completion.choices[0].message['content'].replace("\n", "<br/>").replace(" "," &nbsp;" )
        messages.append({"role": 'assistant', "content": res}  )

        dialogs += f'<div style="margin:20px 0px">🍳{prompt}</div>' 
        dialogs += f'<div style="background-color:#ddd;margin:20px 2px">😊{res}</div>' 
        
    html= f"""
        <div style="background-color:gray">{dialogs}</div>
        <form action=/chat> 
            <textarea style="width:100%"  rows=4 name=prompt></textarea>
            <input type=submit value=Chat>
        </form>
    """    
    return html

if __name__ == '__main__':
	app.run(debug=True)