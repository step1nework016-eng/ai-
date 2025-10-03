import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# --- 初始設定 ---
app = Flask(__name__, template_folder='.')
CORS(app) # 允許來自不同來源的前端請求

# --- API 金鑰與模型設定 ---
model = None
try:
    # 【您的最新 API 金鑰】
    GEMINI_API_KEY = 'AIzaSyCNmsgpPxo6acx3TVlVrvMLWOvqqj38TR4'

    # 設定金鑰
    genai.configure(api_key=GEMINI_API_KEY)

    # 【重要】這次我們使用最穩定、最通用的 'gemini-pro' 模型
    model = genai.GenerativeModel('gemini-pro')
    
    print("✅ Gemini 模型 (gemini-pro) 成功初始化！")

except Exception as e:
    print(f"❌ Gemini 初始化失敗，請檢查您的 API 金鑰權限或網路連線: {e}")
    model = None # 確保如果初始化失敗，模型變數是 None


# --- AI 提示 (Prompt) 定義 ---
COPYWRITING_PROMPT_TEMPLATE = """
你是一位頂尖的短影音文案專家。請根據使用者提供的主題，生成一份包含「文案架構」、「完整文案」和「A/B測試素材」的內容。
主題：{topic}
請嚴格按照以下格式輸出，不要添加任何額外說明：
### 文案架構 (條列式)
- **開頭**：[簡述開頭的核心策略]
- **中間**：[簡述中間的論述方式]
- **結尾**：[簡述結尾的行動呼籲]
### 完整文案
[這裡生成一段約200-300字的完整文案，包含鉤子、主體和結尾]
### A/B 測試素材
***吸睛開頭：***
- [創意的開頭句 1]
- [創意的開頭句 2]
- [創意的開頭句 3]
***行動呼籲 (CTA)：***
- [具體的行動呼籲 1]
- [具體的行動呼籲 2]
- [具體的行動呼籲 3]
"""

SCRIPTWRITING_PROMPT_TEMPLATE = """
你是一位經驗豐富的短影音導演。請根據使用者提供的主題，設計一份約60秒的短影音腳本。
主題：{topic}
請嚴格按照以下格式輸出，不要添加任何額外說明：
### 拍攝建議
- [建議1：關於鏡頭]
- [建議2：關於燈光或場景]
- [建議3：關於演員或情緒]
### 分鏡腳本
- **0-5秒**：[畫面描述]，旁白：[旁白內容]，字幕：[螢幕上的簡短文字]
- **5-15秒**：[畫面描述]，旁白：[旁白內容]，字幕：[螢幕上的簡短文字]
- **15-30秒**：[畫面描述]，旁白：[旁白內容]，字幕：[螢幕上的簡短文字]
- **30-45秒**：[畫面描述]，旁白：[旁白內容]，字幕：[螢幕上的簡短文字]
- **45-60秒**：[畫面描述]，旁白：[旁白內容]，字幕：[螢幕上的簡短文字]
"""

# --- API 路由 (Endpoint) ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if not model:
        return jsonify({"error": "AI 模型未成功初始化，請檢查伺服器日誌中的 API 金鑰或模型設定。"}), 500
    data = request.get_json()
    if not data:
        return jsonify({"error": "無效的請求，沒有收到 JSON 數據。"}), 400
    topic = data.get('topic')
    action = data.get('action')
    if not topic or not action:
        return jsonify({"error": "請求中缺少 'topic' 或 'action' 參數。"}), 400
    if action == 'copywriting':
        prompt = COPYWRITING_PROMPT_TEMPLATE.format(topic=topic)
    elif action == 'scriptwriting':
        prompt = SCRIPTWRITING_PROMPT_TEMPLATE.format(topic=topic)
    else:
        return jsonify({"error": f"未知的 action: {action}"}), 400
    try:
        print(f"正在為主題 '{topic}' 執行 '{action}'...")
        response = model.generate_content(prompt)
        print("✅ AI 已成功生成內容！")
        return jsonify({"result": response.text})
    except Exception as e:
        print(f"❌ AI 生成時發生錯誤: {e}")
        return jsonify({"error": f"AI 生成時發生錯誤: {e}"}), 500

# --- 主程式入口 ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
