from flask import Flask, render_template, request
import qrcode
from barcode import EAN13
from barcode.writer import ImageWriter
import io
import base64

app = Flask(__name__)

@app.route('/barcode', methods=['GET', 'POST'])
def barcode_page():
    barcode_image = None
    error_message = None
    if request.method == 'POST':
        number = request.form.get('barcode_data')
        if not number:
            error_message = "กรุณากรอกข้อมูล Barcode"
        elif len(number) != 13 or not number.isdigit():
            error_message = "กรุณากรอกตัวเลข 13 หลักให้ถูกต้อง"
        else:
            try:
                rv = io.BytesIO()
                EAN13(number, writer=ImageWriter()).write(rv)
                barcode_base64 = base64.b64encode(rv.getvalue()).decode('utf-8')
                barcode_image = barcode_base64
            except Exception as e:
                error_message = f"เกิดข้อผิดพลาดในการสร้างบาร์โค้ด: {e}"
    return render_template('barcode.html', barcode_image=barcode_image, error_message=error_message)

@app.route('/qrcode', methods=['GET', 'POST'])
def qrcode_page():
    qrcode_image = None
    error_message = None
    if request.method == 'POST':
        data = request.form.get('qrcode_data')
        if not data:
            error_message = "กรุณากรอกข้อมูลสำหรับ QR Code"
        else:
            try:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(data)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                buffer = io.BytesIO()
                img.save(buffer, format="PNG")
                qrcode_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                qrcode_image = qrcode_base64
            except Exception as e:
                error_message = f"เกิดข้อผิดพลาดในการสร้าง QR Code: {e}"
    return render_template('qrcode.html', qrcode_image=qrcode_image, error_message=error_message) # บรรทัดนี้สำคัญมาก

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)