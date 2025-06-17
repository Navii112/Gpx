import xml.etree.ElementTree as ET
import math
import csv

R = 6378137  # 지구 반지름 (m)

def wgs84_to_gazebo(lat, lon, alt, lat0, lon0, alt0=0.0):
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

    # 경로 평균 좌표 계산
    lat_sum = lon_sum = ele_sum = 0.0
    for pt in trkpts:
        lat_sum += float(pt.attrib['lat'])
        lon_sum += float(pt.attrib['lon'])
        ele = float(pt.find('default:ele', ns).text) if pt.find('default:ele', ns) is not None else 0.0
        ele_sum += ele

    n = len(trkpts)
    lat0 = lat_sum / n
    lon0 = lon_sum / n
    alt0 = ele_sum / n

    print(f"기준 위도/경도/고도: {lat0}, {lon0}, {alt0}")

    # 좌표 변환 및 CSV 저장
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['x', 'y', 'z'])  # 헤더

        for pt in trkpts:
            lat = float(pt.attrib['lat'])
            lon = float(pt.attrib['lon'])
            ele = float(pt.find('default:ele', ns).text) if pt.find('default:ele', ns) is not None else 0.0
            x, y, z = wgs84_to_gazebo(lat, lon, ele, lat0, lon0, alt0)
            writer.writerow([x, y, z])

    print(f"변환 완료: {output_csv}")

if __name__ == '__main__':
    gpx_file = '186cccae-f4da-4355-b4fd-015e6f198700.gpx'
    output_csv = 'waypoints.csv'
    convert_gpx_to_csv(gpx_file, output_csv)
