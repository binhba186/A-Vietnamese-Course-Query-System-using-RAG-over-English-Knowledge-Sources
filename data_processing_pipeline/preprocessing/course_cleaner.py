import re
from typing import List

class CourseCleaner:
    TITLES_TO_REMOVE = ["Assoc. Prof. ", "Dr. ", "MSc. ", "Prof. ", "M.S. ", "M.Sc. ", "Ms. "]
    SPECIAL_CASES = [" Sciences", " University of Science"]
    REPLACEMENT_TEXT = "Assigned lecturers at University of Science"
    PREREQUISITE_PATTERN = r"Recommended prerequisites?:.*|Recommendation:.*|Course requirements:.*|Prerequisite courses:*"

    def __init__(self, filtered_tables: List[List[List[str]]]):
        self.filtered_tables = filtered_tables

    def clean_course_ids(self):
        for table in self.filtered_tables:
            table[0][1] = table[0][1].strip()[-8:]

    def normalize_semesters(self):
        """
        Bản cũ: đổi sang 'odd' / 'even'.
        Bản mới: đổi sang SỐ học kỳ (1,2,3,...) dựa trên chữ số trong chuỗi.

        Ví dụ:
        - '1st semester' -> '1'
        - '3rd semester' -> '3'
        - 'Semester 2'   -> '2'
        Nếu không tìm thấy số -> giữ nguyên.
        """
        for table in self.filtered_tables:
            raw = str(table[2][1])
            digits = [int(ch) for ch in raw if ch.isdigit()]
            if digits:
                # lấy số đầu tiên tìm được
                new_value = str(digits[0])
                table[2][1] = new_value
            else:
                # fallback: odd/even nếu không có số
                lower = raw.lower()
                if "odd" in lower:
                    table[2][1] = "1"
                elif "even" in lower:
                    table[2][1] = "2"
                else:
                    # giữ nguyên nếu không đoán được
                    table[2][1] = raw

    def normalize_course_type(self):
        for table in self.filtered_tables:
            table[4][1] = table[4][1].lower().strip()

    def clean_teacher_names(self):
        def clean(name):
            name = name.strip()
            for title in self.TITLES_TO_REMOVE:
                if name.startswith(title):
                    name = name.replace(title, '')
            if any(s in name for s in self.SPECIAL_CASES):
                return self.REPLACEMENT_TEXT
            return name

        for table in self.filtered_tables:
            raw = table[3][1].replace('\n', ',')
            names = [clean(n) for n in raw.split(',') if n.strip()]
            unique = []
            seen = set()
            for name in names:
                if name not in seen:
                    seen.add(name)
                    unique.append(name)
            table[3][1] = ', '.join(unique)

    def clean_course_titles_and_prerequisites(self):
        """
        Bản cũ: giả định
            - table[1][1] = Module name
            - table[5][1] = Prerequisites
        → bị sai khi giữ thêm các dòng như Workload,...

        Bản mới: tìm theo KEY để không lệ thuộc index.
        """

        for table in self.filtered_tables:
            # --- Clean Module designation (course name) ---
            for row in table:
                key = str(row[0]).strip()
                if key == "Module designation":
                    value = row[1]
                    if '(' in value:
                        value = value.split('(')[0].strip()
                    row[1] = value
                    break  # đã xử lý xong tên học phần

            # --- Clean prerequisites ---
            for row in table:
                key = str(row[0]).strip()
                if key.startswith("Required and recommended prerequisites for joining the module"):
                    value_5 = row[1]
                    if ': ' in value_5:
                        value_5 = value_5.split(': ', 1)[1].strip()
                    # Apply regex cleanup
                    value_5 = re.sub(self.PREREQUISITE_PATTERN, "", value_5).strip()
                    row[1] = value_5
                    break
