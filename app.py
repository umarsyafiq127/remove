from flask import Flask, request, jsonify, send_file
from rembg import remove
from PIL import Image
import io
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Remove BG API is running!"})

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    try:
        # Pastikan ada file dalam request
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        # Ambil gambar dari request
        image_file = request.files['image']
        image_pil = Image.open(image_file)

        # Hapus background
        image_bytes = io.BytesIO()
        image_pil.save(image_bytes, format="PNG")
        output_bytes = remove(image_bytes.getvalue())
        
        # Simpan hasil ke buffer
        output_image = Image.open(io.BytesIO(output_bytes))
        output_io = io.BytesIO()
        output_image.save(output_io, format="PNG")
        output_io.seek(0)

        # Kirim hasil sebagai file
        return send_file(output_io, mimetype="image/png")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Handler untuk Vercel
def handler(request):
    return app(request)
