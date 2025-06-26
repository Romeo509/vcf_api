from flask import Flask, request, send_from_directory, jsonify
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'vcards'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "✅ VCF Hosting API is live!"

# Upload VCF file
@app.route('/upload', methods=['POST'])
def upload_vcf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    file_url = f"{request.url_root}vcards/{file.filename}"
    return jsonify({'message': 'Upload successful', 'url': file_url})

# Serve VCF file
@app.route('/vcards/<filename>')
def serve_vcf(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, mimetype='text/vcard')

if __name__ == '__main__':
    app.run(debug=True)
