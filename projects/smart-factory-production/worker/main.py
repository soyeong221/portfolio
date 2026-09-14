import sys
import json
from datetime import datetime
import requests

from PyQt5 import uic
from PyQt5.QtCore import QTimer, pyqtSignal, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame
)
import paho.mqtt.client as mqtt

API_BASE_URL = "http://<SERVER_HOST>:<PORT>"

# MQTT 설정
MQTT_BROKER = "<MQTT_BROKER_HOST>"
MQTT_PORT = 1883
MQTT_USERNAME = "<MQTT_USERNAME>"
MQTT_PASSWORD = "<MQTT_PASSWORD>"

# MQTT Topic
TOPIC_PRODUCTION_STATUS = "smart_sorting/production/status"
TOPIC_LINE_STATUS = "smart_sorting/line/status"
TOPIC_ALERT = "smart_sorting/alert"
TOPIC_COMPONENT_STATUS = "smart_sorting/component/status"
TOPIC_LINE_CONTROL = "smart_sorting/line/control"

form_class = uic.loadUiType("ui/worker_main.ui")[0]

class AlertDialog(QDialog):
    def __init__(self, alerts, parent=None):
        super().__init__(parent)

        self.setWindowTitle("알림")
        self.setFixedSize(460, 400)

        self.setStyleSheet("""
            QDialog {
                background-color: #F8FAFB;
            }

            QLabel#titleLabel {
                font-size: 22px;
                font-weight: bold;
                color: #263238;
            }

            QLabel#descriptionLabel {
                font-size: 15px;
                color: #607D8B;
            }

            QPushButton {
                background-color: #16A6B6;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
                padding: 10px 25px;
            }

            QPushButton:pressed {
                background-color: #128C99;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(10)

        # 제목
        title = QLabel("알림")
        title.setObjectName("titleLabel")
        main_layout.addWidget(title)

        description = QLabel("시스템에서 발생한 알림을 확인하세요.")
        description.setObjectName("descriptionLabel")
        main_layout.addWidget(description)

        # 알림 목록
        for alert in alerts:
            alert_type = alert["type"]
            message = alert["message"]

            if alert_type == "INFO":
                color = "#3B82F6"
                type_text = "정보"

            elif alert_type == "WARNING":
                color = "#F59E0B"
                type_text = "주의"

            else:
                color = "#EF4444"
                type_text = "오류"

            alert_frame = QFrame()

            alert_frame.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border: 1px solid #E1E7EA;
                    border-radius: 8px;
                }
            """)

            alert_layout = QVBoxLayout(alert_frame)
            alert_layout.setContentsMargins(14, 10, 14, 10)
            alert_layout.setSpacing(4)

            type_label = QLabel(f"● {type_text}")

            type_label.setStyleSheet(f"""
                QLabel {{
                    color: {color};
                    border: none;
                    font-size: 13px;
                    font-weight: bold;
                }}
            """)

            message_label = QLabel(message)
            message_label.setWordWrap(True)

            message_label.setStyleSheet("""
                QLabel {
                    color: #37474F;
                    border: none;
                    font-size: 14px;
                }
            """)

            alert_layout.addWidget(type_label)
            alert_layout.addWidget(message_label)

            main_layout.addWidget(alert_frame)

        main_layout.addStretch()

        # 확인 버튼
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        btn_confirm = QPushButton("확인")
        btn_confirm.setFixedSize(100, 42)
        btn_confirm.setFocusPolicy(Qt.NoFocus)
        btn_confirm.clicked.connect(self.accept)

        button_layout.addWidget(btn_confirm)

        main_layout.addLayout(button_layout)

class InfoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setFixedSize(340, 180)
        self.setModal(True)

        self.setStyleSheet("""
            QDialog {
                background-color: #F8FAFB;
            }

            QLabel#titleLabel {
                font-size: 18px;
                font-weight: bold;
                color: #263238;
            }

            QLabel#messageLabel {
                font-size: 15px;
                color: #607D8B;
            }

            QPushButton {
                background-color: #16A6B6;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
            }

            QPushButton:pressed {
                background-color: #128C99;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(10)

        title = QLabel("알림")
        title.setObjectName("titleLabel")

        message = QLabel("새로운 알림이 없습니다.")
        message.setObjectName("messageLabel")
        message.setAlignment(Qt.AlignCenter)

        btn_confirm = QPushButton("확인")
        btn_confirm.setFixedHeight(42)
        btn_confirm.setFocusPolicy(Qt.NoFocus)
        btn_confirm.clicked.connect(self.accept)

        layout.addWidget(title)
        layout.addWidget(message)
        layout.addStretch()
        layout.addWidget(btn_confirm)

class LogoutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setFixedSize(360, 210)
        self.setModal(True)

        self.setStyleSheet("""
            QDialog {
                background-color: #F8FAFB;
            }

            QLabel#titleLabel {
                font-size: 20px;
                font-weight: bold;
                color: #263238;
            }

            QLabel#messageLabel {
                font-size: 15px;
                color: #546E7A;
            }

            QPushButton {
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
            }

            QPushButton#btnCancel {
                background-color: #E9EEF0;
                color: #37474F;
                border: none;
            }

            QPushButton#btnConfirm {
                background-color: #EF4444;
                color: white;
                border: none;
            }

            QPushButton#btnConfirm:pressed {
                background-color: #DC2626;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)

        title = QLabel("로그아웃")
        title.setObjectName("titleLabel")

        message = QLabel(
            "로그아웃하시겠습니까?\n현재 생산 작업이 종료됩니다."
        )
        message.setObjectName("messageLabel")
        message.setAlignment(Qt.AlignCenter)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        btn_cancel = QPushButton("취소")
        btn_cancel.setObjectName("btnCancel")
        btn_cancel.setFixedHeight(44)
        btn_cancel.setFocusPolicy(Qt.NoFocus)
        btn_cancel.clicked.connect(self.reject)

        btn_confirm = QPushButton("로그아웃")
        btn_confirm.setObjectName("btnConfirm")
        btn_confirm.setFixedHeight(44)
        btn_confirm.setFocusPolicy(Qt.NoFocus)
        btn_confirm.clicked.connect(self.accept)

        button_layout.addWidget(btn_cancel)
        button_layout.addWidget(btn_confirm)

        layout.addWidget(title)
        layout.addWidget(message)
        layout.addStretch()
        layout.addLayout(button_layout)

class MainWindow(QMainWindow, form_class):

    production_signal = pyqtSignal(dict)
    line_status_signal = pyqtSignal(dict)
    alert_signal = pyqtSignal(dict)
    component_status_signal = pyqtSignal(dict)
    connection_signal = pyqtSignal(bool)

    def __init__(
        self,
        user_name=None,
        session=None,
        token=None,
        logout_callback=None
    ):
        super().__init__()
        self.setupUi(self)

        # 장비별 현재 상태 저장
        self.component_statuses = {}

        # 로그인 정보
        self.user_name = user_name
        self.token = token
        self.logout_callback = logout_callback

        # 로그인한 작업자 표시
        if self.user_name:
            self.lblWorkerName.setText(
                f"작업자 : {self.user_name}"
            )

        # MQTT 수신 데이터 → Qt UI 처리 연결
        self.production_signal.connect(self.update_production_ui)
        self.line_status_signal.connect(self.update_line_status_ui)
        self.alert_signal.connect(self.show_alert)
        self.component_status_signal.connect(self.update_component_status_ui)
        self.connection_signal.connect(self.update_connection_ui)   

        # MQTT 클라이언트 생성
        self.mqtt_client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2
        )

        # MQTT 로그인 정보 설정
        self.mqtt_client.username_pw_set(
            MQTT_USERNAME,
            MQTT_PASSWORD
        )

        # MQTT 연결 콜백 등록
        self.mqtt_client.on_connect = self.on_mqtt_connect
        self.mqtt_client.on_disconnect = self.on_mqtt_disconnect
        self.mqtt_client.on_message = self.on_mqtt_message

        # MQTT 재연결 대기시간 설정
        self.mqtt_client.reconnect_delay_set(
            min_delay=1,
            max_delay=30
        )

        # MQTT 네트워크 루프 시작
        self.mqtt_client.loop_start()

        # MQTT 서버 연결 시도
        try:
            self.mqtt_client.connect_async(
                MQTT_BROKER,
                MQTT_PORT,
                60
            )

        except Exception as e:
            print(f"MQTT 서버 연결 시도 오류 : {e}")
            self.connection_signal.emit(False)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)  # Update every second

        self.update_datetime()  # Initial update

        self.speed_level = 5
        self.speed = 500
        self.isRunning = False

        # 현재 생산 세션 정보
        self.session_id = None
        self.production_status = None

        # 생산 현황 초기 UI
        self.lblChocolateCurrent.setText("0개")
        self.lblChocolateTarget.setText("0개")
        self.lblChocolateSet.setText("0세트")
        self.lblChocolateTargetSet.setText("(0세트)")
        self.progressChocolate.setValue(0)
        self.lblChocolatePercent.setText("0%")

        self.lblCandyCurrent.setText("0개")
        self.lblCandyTarget.setText("0개")
        self.lblCandySet.setText("0세트")
        self.lblCandyTargetSet.setText("(0세트)")
        self.progressCandy.setValue(0)
        self.lblCandyPercent.setText("0%")

        # 로그인 시 조회한 생산 세션 반영
        if session:
            self.apply_session_data(session)

        self.lblSpeed.setText(str(self.speed_level))

        # 버튼 연결
        self.btnSpeedUp.clicked.connect(self.speed_up)
        self.btnSpeedDown.clicked.connect(self.speed_down)
        self.btnStart.clicked.connect(self.start_conveyor)
        self.btnStop.clicked.connect(self.stop_conveyor)
        self.btnLogout.clicked.connect(self.logout)

        # 알림 버튼
        self.btnAlert.clicked.connect(self.show_alert_list)

        # 알림 숫자 배지도 터치 가능
        self.lblAlertCount.mousePressEvent = self.on_alert_badge_clicked

        # 초기 상태
        self.btnSpeedUp.setEnabled(False)
        self.btnSpeedDown.setEnabled(False)
        self.btnStop.setEnabled(False)

        # 알림 초기화
        self.alert_count = 0
        self.alert_messages = []
        self.lblAlertCount.hide()

        self.set_server_disconnected()
        

    def apply_session_data(self, session):
        chocolate_count = session["chocolateCount"]
        candy_count = session["candyCount"]

        # 현재 작업자의 세션 목표 세트 수
        chocolate_target_set = session["targetChocolateSetCount"]
        candy_target_set = session["targetCandySetCount"]

        # 초콜릿 : 10개 = 1세트
        chocolate_current_set = chocolate_count // 10
        chocolate_target_count = chocolate_target_set * 10

        # 사탕 : 1개 = 1세트
        candy_current_set = candy_count
        candy_target_count = candy_target_set

        # 초콜릿
        self.lblChocolateCurrent.setText(f"{chocolate_count}개")
        self.lblChocolateSet.setText(f"{chocolate_current_set}세트")
        self.lblChocolateTarget.setText(f"{chocolate_target_count}개")
        self.lblChocolateTargetSet.setText(
            f"({chocolate_target_set}세트)"
        )

        # 사탕
        self.lblCandyCurrent.setText(f"{candy_count}개")
        self.lblCandySet.setText(f"{candy_current_set}세트")
        self.lblCandyTarget.setText(f"{candy_target_count}개")
        self.lblCandyTargetSet.setText(
            f"({candy_target_set}세트)"
        )

        # 진행률 계산
        chocolate_progress = int(
            chocolate_count / chocolate_target_count * 100
        ) if chocolate_target_count > 0 else 0

        candy_progress = int(
            candy_count / candy_target_count * 100
        ) if candy_target_count > 0 else 0

        # ProgressBar 반영
        self.progressChocolate.setValue(chocolate_progress)
        self.lblChocolatePercent.setText(f"{chocolate_progress}%")

        self.progressCandy.setValue(candy_progress)
        self.lblCandyPercent.setText(f"{candy_progress}%")

    def on_mqtt_connect(self, client, userdata, flags, reason_code, properties):

        if reason_code == 0:
            print("MQTT 서버 연결 성공")

            self.connection_signal.emit(True)

            client.subscribe(TOPIC_PRODUCTION_STATUS)
            client.subscribe(TOPIC_LINE_STATUS)
            client.subscribe(TOPIC_ALERT)
            client.subscribe(TOPIC_COMPONENT_STATUS)

            print("MQTT Topic 구독 완료")

        else:
            print(f"MQTT 서버 연결 실패 : {reason_code}")
            self.connection_signal.emit(False)

    def on_mqtt_disconnect(
        self,
        client,
        userdata,
        disconnect_flags,
        reason_code,
        properties
    ):
        print(f"MQTT 서버 연결 끊김 : {reason_code}")
        self.connection_signal.emit(False)

    def on_mqtt_message(self, client, userdata, msg):
        try:
            message = msg.payload.decode("utf-8")
            data = json.loads(message)

            print(f"MQTT 메시지 수신 [{msg.topic}]")
            print(data)

            if msg.topic == TOPIC_PRODUCTION_STATUS:
                self.production_signal.emit(data)

            elif msg.topic == TOPIC_LINE_STATUS:
                self.line_status_signal.emit(data)

            elif msg.topic == TOPIC_ALERT:
                self.alert_signal.emit(data)

            elif msg.topic == TOPIC_COMPONENT_STATUS:
                self.component_status_signal.emit(data)

        except json.JSONDecodeError:
            print(f"JSON 형식 오류 [{msg.topic}]")
            print(f"수신 데이터 : {msg.payload}")

        except Exception as e:
            print(f"MQTT 메시지 처리 오류 : {e}")

    def update_production_ui(self, data):
        try:
            # 생산 세션 정보
            self.session_id = data["sessionId"]
            self.production_status = data["status"]

            # 초콜릿
            chocolate_count = data["chocolate"]["currentCount"]
            chocolate_target = data["chocolate"]["targetCount"]
            chocolate_unit_per_set = data["chocolate"]["unitPerSet"]
            chocolate_set = data["chocolate"]["setCount"]
            chocolate_progress = data["chocolate"]["progress"]

            # 사탕
            candy_count = data["candy"]["currentCount"]
            candy_target = data["candy"]["targetCount"]
            candy_unit_per_set = data["candy"]["unitPerSet"]
            candy_set = data["candy"]["setCount"]
            candy_progress = data["candy"]["progress"]

            # unitPerSet 값 검사
            if chocolate_unit_per_set <= 0 or candy_unit_per_set <= 0:
                print("생산 현황 오류 : unitPerSet은 1 이상이어야 합니다.")
                return

            # 목표 세트 수 계산
            chocolate_target_set = chocolate_target // chocolate_unit_per_set
            candy_target_set = candy_target // candy_unit_per_set

            # 초콜릿 UI
            self.lblChocolateCurrent.setText(f"{chocolate_count}개")
            self.lblChocolateTarget.setText(f"{chocolate_target}개")
            self.lblChocolateSet.setText(f"{chocolate_set}세트")
            self.lblChocolateTargetSet.setText(
                f"({chocolate_target_set}세트)"
            )
            self.progressChocolate.setValue(chocolate_progress)
            self.lblChocolatePercent.setText(f"{chocolate_progress}%")

            # 사탕 UI
            self.lblCandyCurrent.setText(f"{candy_count}개")
            self.lblCandyTarget.setText(f"{candy_target}개")
            self.lblCandySet.setText(f"{candy_set}세트")
            self.lblCandyTargetSet.setText(
                f"({candy_target_set}세트)"
            )
            self.progressCandy.setValue(candy_progress)
            self.lblCandyPercent.setText(f"{candy_progress}%")

        except KeyError as e:
            print(f"생산 현황 Payload 필드 누락 : {e}")

        except (TypeError, ValueError) as e:
            print(f"생산 현황 Payload 값 오류 : {e}")

        except Exception as e:
            print(f"생산 현황 UI 처리 오류 : {e}")

    def update_line_status_ui(self, data):
        try:
            line_status = data["status"]
            speed_level = data["speedLevel"]
            speed = data["speed"]

            # 상태값 검사
            if line_status not in ["RUNNING", "STOPPED"]:
                print(f"라인 상태 오류 : 알 수 없는 상태값 {line_status}")
                return

            # 속도 레벨 검사
            if not 1 <= speed_level <= 10:
                print(f"라인 상태 오류 : 잘못된 속도 레벨 {speed_level}")
                return

            self.speed_level = speed_level
            self.speed = speed
            self.lblSpeed.setText(str(self.speed_level))

            if line_status == "RUNNING":
                self.isRunning = True

                self.btnStart.setEnabled(False)
                self.btnStop.setEnabled(True)

                # 최대 속도(10)에서는 + 비활성화
                self.btnSpeedUp.setEnabled(self.speed_level < 10)

                # 최소 속도(1)에서는 - 비활성화
                self.btnSpeedDown.setEnabled(self.speed_level > 1)

            elif line_status == "STOPPED":
                self.isRunning = False

                self.btnStart.setEnabled(True)
                self.btnStop.setEnabled(False)
                self.btnSpeedUp.setEnabled(False)
                self.btnSpeedDown.setEnabled(False)

        except KeyError as e:
            print(f"라인 상태 Payload 필드 누락 : {e}")

        except (TypeError, ValueError) as e:
            print(f"라인 상태 Payload 값 오류 : {e}")

        except Exception as e:
            print(f"라인 상태 UI 처리 오류 : {e}")  

    def update_component_status_ui(self, data):
        try:
            component_code = data["componentCode"]
            status = data["status"]

            # 허용된 상태값 확인
            if status not in ["NORMAL", "WARNING", "ERROR", "OFFLINE"]:
                print(
                    f"Component 상태 오류 : "
                    f"알 수 없는 status {status}"
                )
                return

            # 변경 전 상태 확인
            previous_status = self.component_statuses.get(component_code)

            print(
                f"Component 이전 상태 : "
                f"{component_code} → {previous_status}"
            )

            # 현재 상태 저장
            self.component_statuses[component_code] = status

            print(
                f"Component 상태 변경 : "
                f"{component_code} → {status}"
            )

            # WARNING / ERROR / OFFLINE 상태에서
            # NORMAL로 바뀐 경우에만 정상 복귀 알림
            if (
                status == "NORMAL"
                and previous_status in ["WARNING", "ERROR", "OFFLINE"]
            ):
                component_names = {
                    "CAMERA": "카메라",
                    "ARDUINO": "Arduino",
                    "IR_SENSOR": "IR 센서",
                    "CONVEYOR": "컨베이어",
                    "SORTING_SERVO": "분류 Servo",
                    "BUZZER": "부저",
                    "WORKER_DISPLAY": "작업자 Display"
                }

                component_name = component_names.get(
                    component_code,
                    component_code
                )

                recovery_message = f"{component_name} 정상 복귀"

                # 정상 복귀 알림 저장
                self.alert_messages.append({
                    "alertId": None,
                    "type": "INFO",
                    "priority": "LOW",
                    "componentCode": component_code,
                    "errorCode": None,
                    "message": recovery_message
                })

                # 미확인 알림 증가
                self.alert_count += 1

                self.lblAlertCount.setText(str(self.alert_count))
                self.lblAlertCount.show()

                print(
                    f"Component 정상 복귀 : "
                    f"{recovery_message}"
                )

        except KeyError as e:
            print(f"Component 상태 Payload 필드 누락 : {e}")

        except Exception as e:
            print(f"Component 상태 처리 오류 : {e}")

    def show_alert(self, data):
        try:
            alert_type = data["alertType"]
            alert_message = data["shortMessage"]

            if alert_type not in ["INFO", "WARNING", "ERROR"]:
                print(
                    f"알림 Payload 오류 : "
                    f"알 수 없는 alertType {alert_type}"
                )
                return

            # Alert 추가 정보
            priority = data.get("priority")
            component_code = data.get("componentCode")
            error_code = data.get("errorCode")
            alert_id = data.get("alertId")

            # 동일한 alertId 중복 수신 방지
            if alert_id is not None:
                for alert in self.alert_messages:
                    if alert.get("alertId") == alert_id:
                        print(f"중복 알림 무시 : alertId={alert_id}")
                        return

            # 알림 저장
            self.alert_messages.append({
                "alertId": alert_id,
                "type": alert_type,
                "priority": priority,
                "componentCode": component_code,
                "errorCode": error_code,
                "message": alert_message
            })

            # 미확인 알림 개수 증가
            self.alert_count += 1

            self.lblAlertCount.setText(str(self.alert_count))
            self.lblAlertCount.show()

            

            print(
                f"알림 수신 [{alert_type}] "
                f"{alert_message}"
            )

            # ERROR만 즉시 팝업
            if alert_type == "ERROR":
                QMessageBox.critical(
                    self,
                    "오류 알림",
                    alert_message
                )

        except KeyError as e:
            print(f"알림 Payload 필드 누락 : {e}")

        except Exception as e:
            print(f"알림 UI 처리 오류 : {e}")

    def show_alert_list(self):
        # 저장된 알림이 없는 경우
        if not self.alert_messages:
            dialog = InfoDialog(self)
            dialog.exec_()
            return

        # 전용 알림창 표시
        dialog = AlertDialog(
            self.alert_messages,
            self
        )

        dialog.exec_()

        # 알림 확인 후 미확인 알림 초기화
        self.alert_count = 0
        self.alert_messages.clear()
        self.lblAlertCount.hide()

        # Component 상태 저장
        self.component_statuses = {}

        self.set_server_disconnected()

    def on_alert_badge_clicked(self, event):
        self.show_alert_list()    

    def update_datetime(self):
        now = datetime.now()

        self.lblDate.setText(now.strftime("%Y-%m-%d"))
        self.lblTime.setText(now.strftime("%H:%M:%S"))

    def speed_up(self):
        if self.speed_level < 10:
            new_speed_level = self.speed_level + 1
            new_speed = new_speed_level * 100

            message = {
                "command": "SET_SPEED",
                "speedLevel": new_speed_level,
                "speed": new_speed
            }

            self.publish_line_control(message)

    def speed_down(self):
        if self.speed_level > 1:
            new_speed_level = self.speed_level - 1
            new_speed = new_speed_level * 100

            message = {
                "command": "SET_SPEED",
                "speedLevel": new_speed_level,
                "speed": new_speed
            }

            self.publish_line_control(message)

    def publish_line_control(self, message):
        # MQTT 연결 상태 확인
        if not self.mqtt_client.is_connected():
            print("라인 제어 명령 전송 실패 : MQTT 서버 연결 안됨")
            return False

        result = self.mqtt_client.publish(
            TOPIC_LINE_CONTROL,
            json.dumps(message)
        )

        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"라인 제어 명령 전송 : {message}")
            return True
        else:
            print(f"라인 제어 명령 전송 실패 : {result.rc}")
            return False

    def start_conveyor(self):
        message = {
            "command": "START"
        }

        self.publish_line_control(message)

    def stop_conveyor(self):
        message = {
            "command": "STOP"
        }

        self.publish_line_control(message)

    def logout(self):

        # 컨베이어 동작 중에는 로그아웃 방지
        if self.isRunning:
            QMessageBox.warning(
                self,
                "로그아웃",
                "컨베이어를 먼저 정지해 주세요."
            )
            return

        # 로그아웃 확인창
        dialog = LogoutDialog(self)

        if dialog.exec_() != QDialog.Accepted:
            return

        url = f"{API_BASE_URL}/api/production-sessions/finish"

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        try:
            response = requests.patch(
                url,
                headers=headers,
                timeout=5
            )

            print("생산 세션 종료:", response.status_code)
            print(response.text)

            if 200 <= response.status_code < 300:
                print("로그아웃 완료")

                if self.logout_callback:
                    self.logout_callback()

                self.close()

            else:
                QMessageBox.warning(
                    self,
                    "로그아웃 실패",
                    "생산 작업을 종료할 수 없습니다."
                )

        except requests.exceptions.ConnectionError:
            QMessageBox.critical(
                self,
                "서버 연결 실패",
                "서버에 연결할 수 없습니다."
            )

        except requests.exceptions.Timeout:
            QMessageBox.critical(
                self,
                "서버 응답 없음",
                "생산 작업 종료 요청 시간이 초과되었습니다."
            )

        except Exception as e:
            print(f"로그아웃 처리 오류 : {e}")

            QMessageBox.critical(
                self,
                "오류",
                "로그아웃 처리 중 오류가 발생했습니다."
            )

    def update_connection_ui(self, connected):
        if connected:
            self.set_server_connected()
        else:
            self.set_server_disconnected()

    def set_server_connected(self):
        self.lblServerStatus.setText("서버 연결 성공")
        self.lblServerIcon.setStyleSheet(
            "background-color: #22C55E;"
            "border-radius: 6px;"
        )

        # 현재 라인 상태를 받기 전까지 제어 버튼 비활성화
        self.btnStart.setEnabled(False)
        self.btnStop.setEnabled(False)
        self.btnSpeedUp.setEnabled(False)
        self.btnSpeedDown.setEnabled(False)

    def set_server_disconnected(self):
        self.lblServerStatus.setText("서버 연결 실패")
        self.lblServerIcon.setStyleSheet(
            "background-color: #EF4444;"
            "border-radius: 6px;"
        )

        # MQTT 연결이 끊기면 제어 버튼 비활성화
        self.btnStart.setEnabled(False)
        self.btnStop.setEnabled(False)
        self.btnSpeedUp.setEnabled(False)
        self.btnSpeedDown.setEnabled(False)

    def closeEvent(self, event):
        print("프로그램 종료")

        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()

        event.accept()


if __name__ == "__main__":
    print("작업자 HMI는 login.py에서 실행해 주세요.")