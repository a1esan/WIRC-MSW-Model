import numpy as np
import pandas as pd
import os

def relu(x):
    return np.maximum(0, x)

def predict_hhv(input_data):
    try:
        # 1. โหลด Weights และ Biases (อย่าลืม Export จาก MATLAB อันใหม่มาทับไฟล์เดิมด้วยนะ!)
        w1 = pd.read_csv('weights1.csv', header=None).values
        w2 = pd.read_csv('weights2.csv', header=None).values
        b1 = pd.read_csv('biases1.csv', header=None).values.flatten()
        b2 = pd.read_csv('biases2.csv', header=None).values.flatten()
        
        # 2. ค่า Mu และ Sigma ใหม่ (7 ตัว)
        means = np.array([8411.8, 1255.1, 7587.3, 817.341, 493.3067, 250.025, 62.8009])
        sigmas = np.array([1441.6, 912.857, 2592.5, 651.1486, 419.2049, 337.2, 5.9013])
        
        # 3. Standardization (Input ต้องส่งมา 7 ตัว รวม Moisture)
        x = np.array(input_data)
        x_scaled = (x - means) / sigmas
        
        # 4. Neural Network Calculation
        hidden = relu(np.dot(x_scaled, w1.T) + b1)
        prediction = np.dot(hidden, w2.T) + b2
        
        return float(prediction[0]) # นี่คือ HHV Dry Basis จากโมเดลใหม่
    except Exception as e:
        return f"Error: {str(e)}"