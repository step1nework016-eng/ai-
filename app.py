# app.py (安全版本)
import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, template_folder='.')
CORS(app)

model = None
try:
    # 【安全措施】從環境變數中讀取 API 金鑰，而不是直接寫在程式碼裡
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

    if not GEMINI_API_KEY:
        print("❌ 錯誤：找不到環境變數 GEMINI_API_KEY。")
        # 在這種情況下，我們不讓程式崩潰，但模型會是 None
    else:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        print("✅ Gemini 模型 (gemini-pro) 成功初始化！")

except Exception as e:
    print(f"❌ Gemini 初始化失敗: {e}")
    model = None

# --- (後面的程式碼保持不變) ---
# ... (此處省略與之前版本相同的 Prompt 和路由程式碼) ...
COPYWRITING_PROMPT_TEMPLATE = """..."""
SCRIPTWRITING_PROMPT_TEMPLATE = """..."""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if not model:
        return jsonify({"error": "AI 模型未在伺服器端成功初始化。請檢查伺服器的環境變數設定。"}), 500
    # ... (後面的邏輯不變) ...
    data = request.get_json()
    topic = data.get('topic')
    action = data.get('action')
    if not topic or not action: return jsonify({"error": "缺少參數"}), 400
    
    if action == 'copywriting': prompt = COPYWRITING_PROMPT_TEMPLATE.format(topic=topic)
    elif action == 'scriptwriting': prompt = SCRIPTWRITING_PROMPT_TEMPLATE.format(topic=topic)
    else: return jsonify({"error": f"未知的 action: {action}"}), 400
    
    try:
        response = model.generate_content(prompt)
        return jsonify({"result": response.text})
    except Exception as e:
        return jsonify({"error": f"AI 生成時發生錯誤: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
