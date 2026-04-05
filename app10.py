from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from predict_model import predict_hhv 

app = Flask(__name__)
CORS(app)

# ระบุชื่อโฟลเดอร์ที่เก็บไฟล์ทั้งหมด
BASE_DIR = 'MSW UI'

# 1. หน้าแรกสุด: ใครเข้าลิงก์หลัก ให้ไปเปิด index.html ในโฟลเดอร์ MSW UI
@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

# 2. ทางลัดดึงไฟล์อื่นๆ: ใครพิมพ์ชื่อไฟล์อะไรมา (เช่น /HHV_test.html) ให้ไปหยิบจาก MSW UI มาให้
@app.route('/<path:path>')
def send_static(path):
    return send_from_directory(BASE_DIR, path)

# 3. ระบบคำนวณ (เหมือนเดิม)
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        fw = (float(data.get('fw', 0)) / 100) * 16603.48
        pa = (float(data.get('pa', 0)) / 100) * 15821.31
        pf = (float(data.get('pf', 0)) / 100) * 32763.28
        t  = (float(data.get('t', 0)) / 100)  * 21733.86
        w  = (float(data.get('w', 0)) / 100)  * 16920.80
        lr = (float(data.get('lr', 0)) / 100) * 29259.83
        m  = float(data.get('m', 0))
        
        input_for_ann = [fw, pa, pf, t, w, lr, m] 
        hhv_result = predict_hhv(input_for_ann)

        if isinstance(hhv_result, str):
            return jsonify({'success': False, 'error': hhv_result})

        return jsonify({
            'success': True, 
            'hhv': hhv_result,
            'm_used': m
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    # Render จะใช้ Port จากระบบ ถ้าหาไม่เจอจะใช้ 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)