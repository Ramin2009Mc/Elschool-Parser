import requests
from bs4 import BeautifulSoup
import jwt # type: ignore
import openpyxl
import os


LOGIN_URL = "https://elschool.ru/logon/index"
HOME_WORK_URL = "https://elschool.ru/users/diaries"
MARKS_URL = "https://elschool.ru/users/diaries/grades"


class Parser:
    def __init__(self, data=None):
        self.data = data
        try:
            self.session = requests.Session()
            response = self.session.post(LOGIN_URL, data=data, timeout=10)
            response.raise_for_status()
            self.DIARY_PARAMS = self.get_diary_params()
        except requests.exceptions.Timeout:
            print("~ Womp: the server did not respond in time. Try again later.")
            self.session = None
            self.DIARY_PARAMS = None
        except requests.RequestException as e:
            print(f"Connection or authentication error: {e}")
            self.session = None
            self.DIARY_PARAMS = None
        except Exception as e:
            print(f"Unknown error during ElsParser initialization: {e}")
            self.session = None
            self.DIARY_PARAMS = None


    def get_diary_params(self) -> dict:
        try:
            token = self.session.cookies["JWToken"]
            decoded = jwt.decode(token, options={"verify_signature": False})
            role = decoded.get("role", "")
            role_parts = role.split(",")
            rooId = role_parts[3] if len(role_parts) > 3 and role_parts[3] else None
            instituteId = role_parts[4] if len(role_parts) > 4 and role_parts[4] else None
            departmentId = role_parts[5] if len(role_parts) > 5 and role_parts[5] else None
            pupilId = decoded.get("Id")
            params = {
                "rooId": rooId,
                "instituteId": instituteId,
                "departmentId": departmentId,
                "pupilId": pupilId,
                "week": None
            }
            return params
        except Exception as e:
            print(f"~ Womp: error while getting diary parameters: {e}")
            return None


    def get_marks(self):
        try:
            marks_response = self.session.get(MARKS_URL, params=self.DIARY_PARAMS, timeout=10)
            marks_response.raise_for_status()
            soup = BeautifulSoup(marks_response.text, 'lxml')
            grades_table = soup.find('div', class_ = "DivForGradesTable")
            all_lessons = grades_table("tr", lesson = True)
            result = {}  # { 'Алгебра' : {1: ["4,52", "4, 5, 4, 5"], , ,}}

            for lesson in all_lessons:
                current_name = lesson.find("td", "grades-lesson").text.strip()

                if current_name in ["Разговор о важном", "Классный час"]:
                    continue

                marks = lesson.find_all("td", class_="grades-marks")
                avg_marks = lesson.find_all("td", class_ = ["grades-average mark5", "grades-average mark4", "grades-average mark3", "grades-average mark2", "grades-average mark1", "grades-average"])
                
                if current_name not in result:
                    result[current_name] = {}

                for m in range(len(marks)):
                    if marks[m].text.strip() != "" and avg_marks[m].text.strip() != "":
                        spMarks = marks[m].find_all("span", class_="mark-span")
                        formatted_marks = ", ".join([i.get_text(strip=True) for i in spMarks])
                        result[current_name][m+1] = [avg_marks[m].text.strip(), formatted_marks]

            return result
        except requests.exceptions as e:
            print(f"~ Womp: while getting marks: {e}")
            return None
        except Exception as e:
            print(f"~ Womp: while getting marks: {e}")
            return None
        
    
    def get_name_for_xlsx(self):
        filename = f"marks/{self.data['login']}_marks.xlsx"
        return filename
    

    def save_marks_xlsx(self, marks):
        if not marks:
            print("~ Womp (marks is None or empty)")
            return
        
        filename = self.get_name_for_xlsx()

        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        wb = openpyxl.Workbook()
        ws = wb.active

        max_quarters = 0
        for subject, marks_dict in marks.items():
            max_quarters = max(max_quarters, len(marks_dict))

        headers = ["ПРЕДМЕТ"]
        for i in range(1, max_quarters + 1):
            headers.append("СРЕДНИЙ БАЛЛ")
            headers.append(f"{i} ЧЕТВЕРТЬ")
        ws.append(headers)

        for subject, marks_dict in marks.items():
            row = [subject]

            for q in range(1, max_quarters + 1):
                if q in marks_dict:
                    row.append(marks_dict[q][0])
                    row.append(marks_dict[q][1])
                else:
                    row.append("")
                    row.append("")
            ws.append(row)
                
        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            ws.column_dimensions[column].width = max_length + 2 
    
        wb.save(filename)


    def get_home_work(self):
        if not self.session or not self.DIARY_PARAMS:
            return None
        
        try:
            home_work_response = self.session.get(HOME_WORK_URL, params=self.DIARY_PARAMS, timeout=10)
            home_work_response.raise_for_status()
            soup = BeautifulSoup(home_work_response.text, 'lxml')
            all_lessons = soup.find_all("tr", class_ = "diary__lesson")
            
            result = {} # {"Понедельник": {"Алгебра": "Домашнее задание"}}
            day = None
            for lesson in all_lessons:
                current_day = lesson.find("td", class_ = "diary__dayweek")
                if current_day:
                    day = ' '.join(current_day.text.upper().strip().split())
                    if day not in result:
                        result[day] = {}
                name = lesson.find("div", class_ = "flex-grow-1")
                if name:
                    current_name = ' '.join(name.text.upper().strip().split())
                    hw = lesson.find("div", class_="diary__homework-text")
                    homework_text = hw.text.strip() if hw else ""
                    if day:
                        result[day][current_name] = homework_text

            result = {d: s for d, s in result.items() if any(hw.strip() for hw in s.values())}
            return result
        except requests.RequestException as e:
            print(f"~ Womp: request error while getting homework: {e}")
            return None
        except Exception as e:
            print(f"~ Womp: unknown error while getting homework: {e}")
            return None
