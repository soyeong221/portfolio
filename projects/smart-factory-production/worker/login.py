import sys
import requests
import socket

from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QLineEdit,
    QDialog,
    QGridLayout,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)

# 기존 메인 HMI 가져오기
from main import MainWindow


API_BASE_URL = "http://<SERVER_HOST>:<PORT>"

class NumericKeypad(QDialog):
    def __init__(self, current_value="", password_mode=False, parent=None):
        super().__init__(parent)

        self.setWindowTitle("숫자 입력")
        self.setFixedSize(360, 500)
        self.setModal(True)

        # 전체 스타일
        self.setStyleSheet("""
            QDialog {
                background-color: #F7F9FA;
            }

            QLineEdit {
                background-color: white;
                border: 2px solid #B8C5C8;
                border-radius: 8px;
                padding: 8px;
                font-size: 28px;
                font-weight: bold;
            }

            QPushButton {
                background-color: white;
                border: 1px solid #C5D0D2;
                border-radius: 8px;
                font-size: 24px;
                font-weight: bold;
            }

            QPushButton:pressed {
                background-color: #DDEBED;
            }

            QPushButton#btnConfirm {
                background-color: #3E8E93;
                color: white;
                border: none;
            }

            QPushButton#btnCancel {
                background-color: #E8ECEE;
                color: #333333;
            }
        """)

        # 입력값 표시
        self.input = QLineEdit()
        self.input.setReadOnly(True)
        self.input.setFixedHeight(65)
        self.input.setText(current_value)
        self.input.setAlignment(Qt.AlignCenter)

        # 비밀번호 입력이면 숫자 숨기기
        if password_mode:
            self.input.setEchoMode(QLineEdit.Password)

        # 숫자 버튼 영역
        grid = QGridLayout()
        grid.setSpacing(8)

        number_buttons = [
            ("1", 0, 0), ("2", 0, 1), ("3", 0, 2),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2),
            ("지우기", 3, 0), ("0", 3, 1), ("←", 3, 2)
        ]

        for text, row, col in number_buttons:
            button = QPushButton(text)
            button.setMinimumSize(95, 65)
            button.setFocusPolicy(Qt.NoFocus)

            if text.isdigit():
                button.clicked.connect(
                    lambda checked, n=text: self.add_number(n)
                )

            elif text == "←":
                button.clicked.connect(self.delete_number)

            elif text == "지우기":
                button.clicked.connect(self.clear_number)

            grid.addWidget(button, row, col)

        # 취소 / 확인
        self.btnCancel = QPushButton("취소")
        self.btnCancel.setObjectName("btnCancel")
        self.btnCancel.setMinimumHeight(60)
        self.btnCancel.setFocusPolicy(Qt.NoFocus)
        self.btnCancel.clicked.connect(self.reject)

        self.btnConfirm = QPushButton("확인")
        self.btnConfirm.setObjectName("btnConfirm")
        self.btnConfirm.setMinimumHeight(60)
        self.btnConfirm.setFocusPolicy(Qt.NoFocus)
        self.btnConfirm.clicked.connect(self.accept)

        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(8)
        bottom_layout.addWidget(self.btnCancel)
        bottom_layout.addWidget(self.btnConfirm)

        # 전체 배치
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        layout.addWidget(self.input)
        layout.addLayout(grid)
        layout.addLayout(bottom_layout)

        self.setLayout(layout)

    def add_number(self, number):
        # 최대 10자리
        if len(self.input.text()) < 10:
            self.input.setText(
                self.input.text() + number
            )

    def delete_number(self):
        # 마지막 숫자 한 자리 삭제
        self.input.setText(
            self.input.text()[:-1]
        )

    def clear_number(self):
        # 전체 삭제
        self.input.clear()

    def get_value(self):
        return self.input.text()


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 로그인 UI 불러오기
        uic.loadUi("ui/login.ui", self)

        # 직접 키보드 입력 방지
        self.txtLoginId.setReadOnly(True)
        self.txtPassword.setReadOnly(True)

        # 실행 시 입력창에 포커스가 생기지 않도록 설정
        self.txtLoginId.setFocusPolicy(Qt.NoFocus)
        self.txtPassword.setFocusPolicy(Qt.NoFocus)

        # 입력창 터치 시 숫자 키패드 실행
        self.txtLoginId.mousePressEvent = self.open_login_id_keypad
        self.txtPassword.mousePressEvent = self.open_password_keypad

        # 비밀번호 숨김 표시
        self.txtPassword.setEchoMode(QLineEdit.Password)

        # 로그인 버튼
        self.btnLogin.clicked.connect(self.login)

        # 로그인 사용자 정보
        self.token = None
        self.user_id = None
        self.user_name = None
        self.user_role = None

        # 현재 생산 세션
        self.session_id = None
        self.current_session = None

        # 네트워크 상태 초기 표시
        self.lblWifiStatus.setText("Wi-Fi 확인 중")
        self.lblServerStatus.setText("서버 확인 중")

        # 연결 확인 전 아이콘은 회색
        self.lblWifiIcon.setStyleSheet(
            "background-color: #9CA3AF;"
            "border-radius: 6px;"
        )

        self.lblServerIcon.setStyleSheet(
            "background-color: #9CA3AF;"
            "border-radius: 6px;"
        )

        # 연결 상태 확인
        self.check_connection_status()

        # 5초마다 연결 상태 다시 확인
        self.network_timer = QTimer(self)
        self.network_timer.timeout.connect(self.check_connection_status)
        self.network_timer.start(5000)

    def open_login_id_keypad(self, event):
        keypad = NumericKeypad(
            current_value=self.txtLoginId.text(),
            password_mode=False,
            parent=self
        )

        if keypad.exec_() == QDialog.Accepted:
            self.txtLoginId.setText(
                keypad.get_value()
            )

    def open_password_keypad(self, event):
        keypad = NumericKeypad(
            current_value=self.txtPassword.text(),
            password_mode=True,
            parent=self
        )

        if keypad.exec_() == QDialog.Accepted:
            self.txtPassword.setText(
                keypad.get_value()
            )
    def check_connection_status(self):
        # 1. 네트워크 연결 확인
        network_ok = False

        try:
            socket.create_connection(
                ("210.119.12.62", 5051),
                timeout=2
            ).close()

            network_ok = True

        except OSError:
            network_ok = False

        # 2. REST 서버 확인
        server_ok = False

        if network_ok:
            try:
                requests.get(
                    f"{API_BASE_URL}/",
                    timeout=2
                )

                # HTTP 응답이 왔으면 서버 접근 가능
                server_ok = True

            except requests.exceptions.RequestException:
                server_ok = False

        # -------------------------
        # Wi-Fi / 네트워크 UI
        # -------------------------
        if network_ok:
            self.lblWifiStatus.setText("Wi-Fi 연결됨")

            self.lblWifiIcon.setStyleSheet(
                "background-color: #22C55E;"
                "border-radius: 6px;"
            )

        else:
            self.lblWifiStatus.setText("Wi-Fi 연결 안됨")

            self.lblWifiIcon.setStyleSheet(
                "background-color: #EF4444;"
                "border-radius: 6px;"
            )

        # -------------------------
        # REST 서버 UI
        # -------------------------
        if server_ok:
            self.lblServerStatus.setText("서버 연결됨")

            self.lblServerIcon.setStyleSheet(
                "background-color: #22C55E;"
                "border-radius: 6px;"
            )

            # 서버 연결됨 → 로그인 가능
            self.btnLogin.setEnabled(True)

        else:
            self.lblServerStatus.setText("서버 연결 안됨")

            self.lblServerIcon.setStyleSheet(
                "background-color: #EF4444;"
                "border-radius: 6px;"
            )

            # 서버 연결 안됨 → 로그인 불가
            self.btnLogin.setEnabled(False)

    def login(self):
        login_id = self.txtLoginId.text().strip()
        password = self.txtPassword.text()

        # 빈 값 검사
        if not login_id or not password:
            QMessageBox.warning(
                self,
                "로그인",
                "아이디와 비밀번호를 입력해 주세요."
            )
            return

        # 로그인 중 중복 클릭 방지
        self.btnLogin.setEnabled(False)

        url = f"{API_BASE_URL}/api/auth/login"

        data = {
            "loginId": login_id,
            "password": password
        }

        try:
            response = requests.post(
                url,
                json=data,
                timeout=5
            )

            if response.status_code == 200:
                result = response.json()

                # 로그인 정보 저장
                self.token = result["token"]
                self.user_id = result["userId"]
                self.user_name = result["name"]
                self.user_role = result["role"]

                print("로그인 성공")
                print("사용자:", self.user_name)
                print("역할:", self.user_role)

                # 현재 생산 세션 조회
                self.get_current_session()

            else:
                # 로그인 실패 시 버튼 다시 활성화
                self.btnLogin.setEnabled(True)

                print(
                    f"로그인 실패 : "
                    f"{response.status_code} / {response.text}"
                )

                QMessageBox.warning(
                    self,
                    "로그인 실패",
                    "아이디 또는 비밀번호를 확인해 주세요."
                )

        except requests.exceptions.ConnectionError:
            self.btnLogin.setEnabled(True)

            print("REST 서버 연결 실패")

            QMessageBox.critical(
                self,
                "서버 연결 실패",
                "서버에 연결할 수 없습니다."
            )

        except requests.exceptions.Timeout:
            self.btnLogin.setEnabled(True)

            print("REST 서버 응답 시간 초과")

            QMessageBox.critical(
                self,
                "서버 응답 없음",
                "서버 응답 시간이 초과되었습니다."
            )

        except Exception as e:
            self.btnLogin.setEnabled(True)

            print(f"로그인 처리 오류 : {e}")

            QMessageBox.critical(
                self,
                "오류",
                "로그인 처리 중 오류가 발생했습니다."
            )

    def get_current_session(self):
        url = f"{API_BASE_URL}/api/production-sessions/current"

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=5
            )

            print("현재 생산 세션 조회:", response.status_code)
            print(response.text)

            if response.status_code == 200:
                session = response.json()

                self.current_session = session
                self.session_id = session["sessionId"]

                print("현재 생산 세션 사용")
                print("세션 ID:", self.session_id)

                self.open_main_window()

            elif response.status_code == 404:
                print("현재 생산 세션 없음")
                self.start_production_session()

            else:
                self.btnLogin.setEnabled(True)

                print(
                    f"현재 생산 세션 조회 실패 : "
                    f"{response.status_code} / {response.text}"
                )

                QMessageBox.warning(
                    self,
                    "생산 작업 조회 실패",
                    "현재 생산 작업을 확인할 수 없습니다."
                )

        except requests.exceptions.ConnectionError:
            self.btnLogin.setEnabled(True)
            print("생산 세션 조회 중 서버 연결 실패")

            QMessageBox.critical(
                self,
                "서버 연결 실패",
                "생산 작업 정보를 불러올 수 없습니다."
            )

        except requests.exceptions.Timeout:
            self.btnLogin.setEnabled(True)
            print("생산 세션 조회 중 서버 응답 시간 초과")

            QMessageBox.critical(
                self,
                "서버 응답 없음",
                "생산 작업 조회 시간이 초과되었습니다."
            )

        except Exception as e:
            self.btnLogin.setEnabled(True)
            print(f"생산 세션 조회 오류 : {e}")

            QMessageBox.critical(
                self,
                "오류",
                "생산 작업 조회 중 오류가 발생했습니다."
            )

    def start_production_session(self):
        url = f"{API_BASE_URL}/api/production-sessions/start"

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                timeout=5
            )

            print("생산 세션 시작:", response.status_code)
            print(response.text)

            if 200 <= response.status_code < 300:
                session = response.json()

                self.current_session = session
                self.session_id = session["sessionId"]

                print("새 생산 세션 생성")
                print("세션 ID:", self.session_id)

                self.open_main_window()

            else:
                self.btnLogin.setEnabled(True)

                QMessageBox.warning(
                    self,
                    "생산 작업 시작 실패",
                    "생산 작업을 시작할 수 없습니다."
                )

        except requests.exceptions.ConnectionError:
            self.btnLogin.setEnabled(True)
            QMessageBox.critical(
                self,
                "서버 연결 실패",
                "생산 작업을 시작할 수 없습니다."
            )

        except requests.exceptions.Timeout:
            self.btnLogin.setEnabled(True)
            QMessageBox.critical(
                self,
                "서버 응답 없음",
                "생산 작업 시작 요청 시간이 초과되었습니다."
            )

        except Exception as e:
            self.btnLogin.setEnabled(True)
            print(f"생산 세션 시작 오류 : {e}")

            QMessageBox.critical(
                self,
                "오류",
                "생산 작업 시작 중 오류가 발생했습니다."
            )

    def open_main_window(self):
        self.main_window = MainWindow(
            user_name=self.user_name,
            session=self.current_session,
            token=self.token,
            logout_callback=self.return_to_login
        )

        self.main_window.show()
        self.hide()

    def return_to_login(self):
        # 로그인 정보 초기화
        self.token = None
        self.user_id = None
        self.user_name = None
        self.user_role = None
        self.session_id = None
        self.current_session = None

        # 로그인 버튼 다시 활성화
        self.btnLogin.setEnabled(True)

        # 입력창 초기화
        self.txtLoginId.clear()
        self.txtPassword.clear()

        # 로그인 화면 다시 표시
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = LoginWindow()
    window.show()

    sys.exit(app.exec_())