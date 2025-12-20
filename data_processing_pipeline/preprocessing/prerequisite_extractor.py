import pandas as pd
import re
import Levenshtein
from typing import List, Optional


def parse_credit_points(raw_credit: str) -> Optional[int]:
    """
    Parse 'Credit points' kiểu '3 Credits (4.5 ECTS)' → 3.
    Nếu không tìm được số nguyên nào thì trả về None.
    """
    if not raw_credit:
        return None
    m = re.search(r'(\d+)', raw_credit)
    if not m:
        return None
    return int(m.group(1))


class PrerequisiteExtractor:
    def __init__(self, filtered_tables: List[List[List[str]]]):
        self.filtered_tables = filtered_tables
        self.mapping_course_name_origin_list = []
        self.mapping_course_name_lower_list = []
        self.result_dict = {}

    def _normalize_key(self, raw: str) -> str:
        """
        Chuẩn hoá key trong cột 0 của bảng:
        - Gộp tất cả loại whitespace (space, \n, \t, ...) thành 1 space
        - Strip 2 đầu
        """
        return " ".join(str(raw).split()).strip()

    def extract_dataframe(self):
        """
        Duyệt từng bảng, lấy đủ 12 trường:

          0  course_name
          1  semester
          2  lecturer
          3  course_type
          4  prerequisites
          5  learning_outcomes
          6  content
          7  teaching_methods
          8  credits (int hoặc None)
          9  exam_forms
          10 reading_list
          11 passing_conditions

        self.result_dict[course_id] = [ ... 12 phần tử ... ]

        DataFrame trả về để fuzzy match prerequisites vẫn chỉ cần:
          - course_id
          - course_name
          - prerequisites (clean)
          - answer (sẽ điền sau)
        """

        data = []
        for table in self.filtered_tables:
            if not table or len(table) < 2:
                continue

            course_id = str(table[0][1]).strip()

            # Khởi tạo 12 trường (trừ course_id - dùng làm key)
            course_name = ""
            semester = ""
            lecturer = ""
            course_type = ""
            prerequisites = ""
            learning_outcomes = ""
            content = ""
            teaching_methods = ""
            raw_credits = ""
            exam_forms = ""
            reading_list = ""
            passing_conditions = ""

            # Duyệt từng row còn lại trong bảng
            for row in table[1:]:
                if len(row) < 2:
                    continue
                key = self._normalize_key(row[0])
                value = str(row[1]).strip()

                if key == "Module designation":
                    course_name = value
                elif key == "Semester(s) in which the module is taught":
                    semester = value
                elif key == "Person responsible for the module":
                    lecturer = value
                elif key == "Relation to curriculum":
                    course_type = value
                elif key.startswith("Required and recommended prerequisites for joining the module"):
                    prerequisites = value
                elif key.startswith("Module objectives/intended learning outcomes"):
                    learning_outcomes = value
                elif key == "Content":
                    content = value
                elif key == "Teaching methods":
                    teaching_methods = value
                elif key == "Credit points":
                    raw_credits = value
                elif key == "Examination forms":
                    exam_forms = value
                elif key.startswith("Study and examination requirements"):
                    passing_conditions = value
                elif key == "Reading list":
                    reading_list = value

            # Parse credits → số đầu tiên
            credit_points = parse_credit_points(raw_credits)

            # Cập nhật result_dict theo thứ tự 8 field cũ + 5 field mới (không còn workload)
            self.result_dict[course_id] = [
                course_name,        # 0
                semester,           # 1
                lecturer,           # 2
                course_type,        # 3
                prerequisites,      # 4
                learning_outcomes,  # 5
                content,            # 6
                teaching_methods,   # 7
                credit_points,      # 8 (int hoặc None)
                exam_forms,         # 9
                reading_list,       # 10
                passing_conditions  # 11
            ]

            # Chuẩn hoá prerequisites để đưa vào DataFrame fuzzy match
            prereq_clean = re.sub(r'\([^)]*\)', '', prerequisites.lower()).strip()
            data.append({
                "course_id": course_id,
                "course_name": course_name,
                "prerequisites": prereq_clean,
                "answer": None
            })

        return pd.DataFrame(data)

    def split_prerequisites(self, df):
        """
        Tách cột 'prerequisites' thành nhiều dòng theo ',' / ';' / xuống dòng.
        BỎ các token chỉ là header kiểu 'required prerequisites:', 'prerequisite courses', ...
        """
        header_like_patterns = [
            "required prerequisites",
            "required prerequisites:",
            "recommended prerequisites",
            "recommended prerequisites:",
            "course requirements",
            "course requirements:",
            "prerequisite courses",
            "prerequisite courses:",
        ]

        new_rows = []
        for _, row in df.iterrows():
            raw = str(row['prerequisites'])
            parts = [
                p.strip() for p in
                raw.replace('\n', ',').replace(';', ',').split(',')
            ]

            # nếu không tách được gì → giữ nguyên 1 dòng
            if not parts:
                new_rows.append(row)
                continue

            kept_any = False
            for p in parts:
                p_clean = p.strip()
                if not p_clean:
                    continue
                p_lower = p_clean.lower()

                # BỎ header kiểu "required prerequisites:", "course requirements", ...
                if any(h in p_lower for h in header_like_patterns):
                    continue

                new_row = row.copy()
                new_row['prerequisites'] = p_clean
                new_rows.append(new_row)
                kept_any = True

            # nếu tất cả parts đều bị bỏ (toàn header) → giữ 1 dòng gốc
            if not kept_any:
                new_rows.append(row)

        return pd.DataFrame(new_rows)
    
    def standardize_roman_numerals(self, df):
        def replace_arabic_with_roman(text):
            text = re.sub(r'\bgeneral biology 1\b', 'general biology I', text, flags=re.IGNORECASE)
            text = re.sub(r'\bgeneral biology 2\b', 'general biology II', text, flags=re.IGNORECASE)
            return text
        
        df['prerequisites'] = df['prerequisites'].apply(replace_arabic_with_roman)
        return df

    def create_mappings(self):
        mapping = {}
        for table in self.filtered_tables:
            course_id = table[0][1].strip()
            # Module designation là tên môn
            if len(table) > 1 and len(table[1]) > 1:
                course_name = table[1][1].strip()
            else:
                course_name = ""
            mapping[course_id] = {
                "origin": course_name,
                "lower": course_name.lower()
            }
        self.mapping_course_name_origin_list = [v["origin"] for v in mapping.values()]
        self.mapping_course_name_lower_list = [v["lower"] for v in mapping.values()]

    def levenshtein_distance(self, s1: str, s2: str) -> int:
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i  # xóa toàn bộ ký tự
        for j in range(n + 1):
            dp[0][j] = j  # chèn toàn bộ ký tự

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1

                dp[i][j] = min(
                    dp[i - 1][j] + 1,      # xóa
                    dp[i][j - 1] + 1,      # chèn
                    dp[i - 1][j - 1] + cost  # thay thế
                )

        return dp[m][n]

    def match_fuzzy(self, df):
        def match(row):
            prereq = row["prerequisites"].lower().strip()

            if prereq == "none" or prereq == "":
                row["answer"] = "none"
                return row

            distances = [self.levenshtein_distance(prereq, cand) for cand in self.mapping_course_name_lower_list]
            if not distances:
                return row

            min_idx = min(range(len(distances)), key=lambda i: distances[i])
            row["answer"] = self.mapping_course_name_origin_list[min_idx]
            return row

        df = df.apply(match, axis=1)
        return df.drop_duplicates().reset_index(drop=True)

    @staticmethod
    def adjust_answer_column(df: pd.DataFrame):
        df['prerequisites'] = df['prerequisites'].astype(str)
        df.loc[df['prerequisites'].str.lower().str.contains('credits'), 'answer'] = df['prerequisites']
        
        df.loc[df['course_id'] == 'MTH10616', 'answer'] = df['prerequisites']
    
        return df
