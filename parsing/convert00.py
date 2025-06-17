import xml.etree.ElementTree as ET
import math
import csv
import os

# 기준 좌표 (Gazebo world 파일의 <spherical_coordinates> 정보)
LAT0 = 0.0
LON0 = 0.0
ALT0 = 0.0
R = 6378137  # 지구 반지름 (m)

def wgs84_to_gazebo(lat, lon, alt, lat0=LAT0, lon0=LON0, alt0=ALT0):
    """WGS84 → Gazebo 좌표 변환"""
    x = R * math.radians(lon - lon0) * math.cos(math.radians(lat0))
    y = R * math.radians(lat - lat0)
    z = alt - alt0
    return x, y, z

def convert_gpx_to_csv(gpx_file, output_csv):
    tree = ET.parse(gpx_file)
    root = tree.getroot()

    ns = {'default': 'http://www.topografix.com/GPX/1/1'}
    trkpts = root.findall('.//default:trkpt', ns)

    if not trkpts:
        print("경로 포인트가 없습니다.")
        return

    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['x', 'y', 'z'])  # 헤더

        for pt in trkpts:
            lat = float(pt.attrib['lat'])
            lon = float(pt.attrib['lon'])
            ele = float(pt.find('default:ele', ns).text) if pt.find('default:ele', ns) is not None else 0.0
            x, y, z = wgs84_to_gazebo(lat, lon, ele)
            writer.writerow([x, y, z])
    
    print(f"변환 완료: {output_csv}")

if __name__ == '__main__':
    # 테스트 실행
    gpx_file = '23ce154c-919b-4f60-a575-42445d08e3f2.gpx'  # 변환할 GPX 파일명
    output_csv = 'waypoints.csv'  # 저장할 CSV
    convert_gpx_to_csv(gpx_file, output_csv)
