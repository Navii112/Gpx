# RostoGPX

이 프로젝트는 ROS Simulator(Gazebo)에서 시뮬레이터 차량 구동을 위한 맵 파일을 index.html 프로그램에 삽입하여 좌표를 얻어 작동하게 하기 위한 GPX파일 생성 프로그램입니다.

## 주요 기능, 사용 방법 설명

- 마우스 좌 클릭시 점이 생성되며 2번 이상 클릭 시 점과 점을 잇는 선이 나오게 됩니다. 선을 이어 경로를 작성하고 GPX 다운로드 버튼을 누르게 되면, 파일내에 GPX 파일이 생성됩니다.

## 실행 방법

1. App.py 실행 시 터미널이 켜지며 실행됩니다.
2. Running on http://~~~.~.~.~:~~~~ 을 실행시켜 GPX다운로드 웹앱을 엽니다.
3. 선을 이어 경로를 지정해 GPX경로를 만들고 다운로드 합니다.

# Parsing

Parsing 부분에서는 ROS Simulator(Gazebo)에서 작동하는 로컬 데이터 좌표에 맞게 GPX생성 시 나오게 되는 좌표를 시뮬레이터 좌표에 맞게 변환하여 csv파일로 변환해주는 프로그램입니다.

## 주요 기능, 사용 방법 설명

- 외부 터미널이 아닌 parsing 파일 내에서 터미널을 실행시킵니다. 터미널 실행후 "python convert.py" 라고 입력합니다. 그러면 gpx좌표에서 시뮬레이터에 사용할 수 있도록 알맞게 변환 된 'waypoints.csv' 라고 저장 된 csv파일이 생성됩니다.

## 주의사항

1. 저장된 gpx가 parsing 파일 내에 같은 경로에 있어야 csv파일로 저장됩니다. 경로가 다를 경우 변환에 실패합니다.
2. 변환 하기 전 convert.py에서 gpx_file = 'your_name_gpx.gpx' your_name_gpx 부분을 변환하려는 gpx의 이름에 맞게 설정해주고 수동으로 수정한 후에 실행시켜야 변환이 됩니다.

# csv_path_publisher 기능

- CSV로부터 x, y, z 좌표를 읽어와 Path 메시지 생성
- 해당 경로를 ROS 토픽 /path_from_csv로 지속적으로 발행
- SLAM 또는 경로 추적 알고리즘 등에서 활용 가능
