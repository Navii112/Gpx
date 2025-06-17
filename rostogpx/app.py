import os
import math
import uuid
import xml.etree.ElementTree as ET
from flask import Flask, render_template, request, send_file, jsonify

app = Flask(__name__)

# app.py가 있는 폴더 절대 경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def gazebo_to_wgs84(x, y, z, lat0=0.0, lon0=0.0, alt0=0.0):
    R = 6378137
    lat = lat0 + (y / R) * (180 / math.pi)
    lon = lon0 + (x / (R * math.cos(lat0 * math.pi / 180))) * (180 / math.pi)
    alt = alt0 + z
    return lat, lon, alt

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_gpx', methods=['POST'])
def save_gpx():
    try:
        data = request.get_json()
        points = data.get('points', [])

        # 네임스페이스 포함
        gpx = ET.Element(
            'gpx',
            version='1.1',
            creator='MapGPX',
            xmlns='http://www.topografix.com/GPX/1/1'
        )
        trk = ET.SubElement(gpx, 'trk')
        trkseg = ET.SubElement(trk, 'trkseg')

        for point in points:
            x, y = point['x'], point['y']
            gz_x = x
            gz_y = 500 - y
            lat, lon, _ = gazebo_to_wgs84(gz_x, gz_y, 0)
            ET.SubElement(trkseg, 'trkpt', lat=str(lat), lon=str(lon))

        filename = f"{uuid.uuid4()}.gpx"
        filepath = os.path.join(BASE_DIR, filename)

        tree = ET.ElementTree(gpx)
        tree.write(filepath, encoding='utf-8', xml_declaration=True)

        return jsonify({'filename': filename})
    except Exception as e:
        return jsonify({'error': f'GPX 저장 중 오류 발생: {str(e)}'}), 500

@app.route('/download/<filename>')
def download(filename):
    filepath = os.path.join(BASE_DIR, filename)
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
