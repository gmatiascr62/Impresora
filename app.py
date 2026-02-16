from flask import Flask, request, send_file, jsonify
import fitz
import io

app = Flask(__name__)

@app.route("/pdf-a-imagen", methods=["POST"])
def pdf_a_imagen():
    if "file" not in request.files:
        return jsonify({"error": "No se envió archivo"}), 400

    file = request.files["file"]
    pdf_bytes = file.read()

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    page = doc[0]  # primera página
    
    # 🔥 Acá está el DPI
    pix = page.get_pixmap(dpi=150)

    img_bytes = pix.tobytes("png")
    doc.close()

    return send_file(
        io.BytesIO(img_bytes),
        mimetype="image/png",
        download_name="pagina.png"
    )

if __name__ == "__main__":
    app.run(debug=True)