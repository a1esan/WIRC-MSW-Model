from flask import Flask, request, jsonify
from flask_cors import CORS
from predict_model import predict_hhv 

app = Flask(__name__)
CORS(app)

print("--- ระบบคำนวณ HHV พร้อมใช้งาน (ไม่ต้องใช้ MATLAB Engine) ---")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        # 1. รับค่า % และคูณตัวเลขน้ำหนัก (อ้างอิงตามสเกลที่ใช้เทรน Mu/Sigma)
        fw = (float(data.get('fw', 0)) / 100) * 16603.48
        pa = (float(data.get('pa', 0)) / 100) * 15821.31
        pf = (float(data.get('pf', 0)) / 100) * 32763.28
        t  = (float(data.get('t', 0)) / 100)  * 21733.86
        w  = (float(data.get('w', 0)) / 100)  * 16920.80
        lr = (float(data.get('lr', 0)) / 100) * 29259.83
        m  = float(data.get('m', 0)) # ค่าความชื้น %
        
        # 2. ส่ง 7 ตัวแปรเข้า ANN (ตัวที่ 7 คือ m)
        input_for_ann = [fw, pa, pf, t, w, lr, m] 
        hhv_result = predict_hhv(input_for_ann)

        if isinstance(hhv_result, str):
            return jsonify({'success': False, 'error': hhv_result})

        # --- ไม่ต้องคำนวณ hhv_as แยกแล้ว ยึดตามโปรแกรมพ่นออกมาเลย ---
        print(f"✅ AI Result: {hhv_result:.2f} (Moisture included as input)")

        return jsonify({
            'success': True, 
            'hhv': hhv_result,      # ค่าที่ได้จาก AI ตรงๆ
            'hhv_dry': hhv_result,  # โชว์เหมือนกันไปก่อนเพื่อเช็กค่า
            'm_used': m
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

    @app.route('/')
def home():
    return "AI HHV Model is Running! Please go to /HHV_test.html"

@app.route('/<path:path>')
def send_report(path):
    from flask import send_from_directory
    return send_from_directory('.', path)

    # ต้องอยู่ล่างสุดของไฟล์ app10.py และห้ามเคาะเว้นวรรคข้างหน้า (ต้องชิดซ้าย)
if __name__ == '__main__':
    # host='0.0.0.0' เพื่อให้เครื่องอื่นในวงแลนมองเห็น
    app.run(host='0.0.0.0', port=5000, debug=False)