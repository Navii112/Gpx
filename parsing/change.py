import xml.etree.ElementTree as ET

def parse_gpx(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    namespace = {'default': 'http://www.topografix.com/GPX/1/1'}

    waypoints = []
    for trkpt in root.findall('.//default:trkpt', namespace):
        lat = float(trkpt.get('lat'))
        lon = float(trkpt.get('lon'))
        waypoints.append((lat, lon))

    return waypoints
