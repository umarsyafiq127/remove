from flask import Flask, render_template, request, send_from_directory
import os
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

# Direktori untuk menyimpan gambar yang diunggah dan hasilnya
UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "Tidak ada file yang diunggah"

        file = request.files["file"]
        if file.filename == "":
            return "Pilih file terlebih dahulu"

        if file:
            # Simpan gambar yang diunggah
            input_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(input_path)

            # Proses hapus background
            output_filename = "no_bg_" + file.filename
            output_path = os.path.join(RESULT_FOLDER, output_filename)

            with open(input_path, "rb") as inp_file:
                image = inp_file.read()
            
            output_image = remove(image)

            with open(output_path, "wb") as out_file:
                out_file.write(output_image)

            return render_template("index.html", input_image=input_path, output_image=output_path)

    return render_template("index.html", input_image=None, output_image=None)

if __name__ == "__main__":
    app.run(debug=True)
