from flask import Flask, request, jsonify
from flask_cors import CORS
# เรียกใช้ไฟล์คำนวณที่เราสร้างใหม่
from predict_model import predict_hhv 

app = Flask(__name__)
CORS(app)

print("--- ระบบคำนวณ HHV (เวอร์ชันไม่ต้องเปิด MATLAB) พร้อมใช้งาน ---")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        # รับค่าจากหน้าเว็บ (FW, PA, PF, T, W, LR, M)
        fw = (float(data.get('fw', 0)) / 100) * 16603.48
        pa = (float(data.get('pa', 0)) / 100) * 15821.31
        pf = (float(data.get('pf', 0)) / 100) * 32763.28
        t  = (float(data.get('t', 0)) / 100)  * 21733.86
        w  = (float(data.get('w', 0)) / 100)  * 16920.80
        lr = (float(data.get('lr', 0)) / 100) * 29259.83
        m  = (float(data.get('m', 0)) / 1)
        
        # ส่งค่าไปคำนวณในไฟล์ predict_model.py
        input_list = [fw, pa, pf, t, w, lr, m] 
        hhv_result = predict_hhv(input_list)

        print(f"คำนวณสำเร็จ! ค่า HHV คือ: {hhv_result:.2f}")
        
        return jsonify({
            'success': True, 
            'hhv': hhv_result,
            'm_used': m
        })

    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    # รันที่พอร์ต 5000 เหมือนเดิมที่หน้าเว็บอายเรียกใช้
    app.run(port=5000, debug=False)