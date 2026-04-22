# Highway Quiz Flask App

เว็บข้อสอบแบบทีละ 1 ข้อ
- ตอบแล้วรู้ผลทันที
- มีคำอธิบาย
- มีสรุปคะแนนและข้อที่ตอบผิด
- ใช้รหัสยืนยันก่อนเข้า

## วิธีรัน
1. เปิด terminal ในโฟลเดอร์โปรเจกต์
2. ติดตั้งแพ็กเกจ
   pip install -r requirements.txt
3. รันแอป
   python app.py
4. เปิดเบราว์เซอร์ที่
   http://127.0.0.1:5000

## รหัสเริ่มต้น
HIGHWAY2026

## ไฟล์สำคัญ
- app.py
- highway_exam_1_20.json
- templates/
- static/style.css

## หมายเหตุ
- เปลี่ยน secret_key ใน app.py ก่อนใช้งานจริง
- เปลี่ยน ACCESS_CODE ใน app.py ได้ตามต้องการ
