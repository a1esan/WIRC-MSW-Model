import numpy as np
import pandas as pd

def relu(x):
    return np.maximum(0, x)

def predict_hhv(input_data):
    # โหลดค่าจาก CSV 4 ไฟล์ (ต้องวางไฟล์ CSV ไว้ข้างๆ ไฟล์นี้ด้วยนะ)
    try:
        w1 = pd.read_csv('weights1.csv', header=None).values
        w2 = pd.read_csv('weights2.csv', header=None).values
        b1 = pd.read_csv('biases1.csv', header=None).values.flatten()
        b2 = pd.read_csv('biases2.csv', header=None).values.flatten()
        
        x = np.array(input_data)
        # คำนวณ Layer 1 (100 Nodes)
        hidden = relu(np.dot(x, w1.T) + b1)
        # คำนวณ Output
        prediction = np.dot(hidden, w2.T) + b2
        return float(prediction[0])
    except Exception as e:
        return f"Error: {str(e)} (Check if CSV files exist)"