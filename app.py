from flask import Flask, render_template, request, Response
import http.client
import io

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/help')
def help():
    return render_template('help.html')
@app.route('/download', methods=['POST'])
def handle_download():
    uuid = request.form.get('uuid')
    jsessionid = request.form.get('jsessionid')

    conn = http.client.HTTPSConnection("student.dominic.tas.edu.au")
    headers = {'Cookie': f'JSESSIONID={jsessionid}'}
    url = f"/seqta/student/photo/get?uuid={uuid}&format=high"
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()

    if res.status == 200:
        # Create an in-memory file-like object
        file_stream = io.BytesIO(data)
        file_stream.seek(0)

        # Set the content disposition header for download
        headers = {'Content-Disposition': f'attachment; filename=photo_{uuid}.jpg'}
        return Response(file_stream, mimetype='image/jpeg', headers=headers)

    return "Failed to download the photo."

if __name__ == '__main__':
    app.run()
