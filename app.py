from flask import Flask, request, send_file, jsonify
import fitz
import io
import zipfile

app = Flask(__name__)

@app.route("/pdf-a-imagen", methods=["POST"])
def pdf_a_imagen():
    if "file" not in request.files:
        return jsonify({"error": "No se envió archivo"}), 400

    file = request.files["file"]
    pdf_bytes = file.read()

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    zip_buffer = io.BytesIO()
    zip_file = zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED)

    for i in range(len(doc)):
        page = doc[i]
        pix = page.get_pixmap(dpi=150)
        img_bytes = pix.tobytes("png")
        zip_file.writestr(f"pagina_{i+1}.png", img_bytes)

    zip_file.close()
    doc.close()

    zip_buffer.seek(0)

    return send_file(
        zip_buffer,
        mimetype="application/zip",
        download_name="imagenes.zip",
        as_attachment=True
    )
