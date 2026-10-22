
# A-Vietnamese-Course-Query-System-using-RAG-over-English-Knowledge-Sources

Hệ thống tra cứu khóa học tiếng Việt sử dụng RAG trên các nguồn kiến ​​thức tiếng Anh

Ánh xạ thực thể khóa học · Tạo ứng viên đa ngôn ngữ · Truy xuất kết hợp (FTS + Mờ + Ngữ nghĩa)

## Mô tả cấu trúc dữ liệu đầu vào
Mỗi môn học trong bộ dữ liệu được biểu diễn dưới dạng một bản ghi có cấu trúc, bao gồm mã định danh duy nhất và phần mô tả chi tiết về môn học. Mã môn học (ví dụ: GEO00002) đóng vai trò là khóa chính, giúp xác định chính xác và tránh nhầm lẫn giữa các học phần. Trường văn bản đi kèm tổng hợp toàn bộ thông tin học thuật liên quan thành một tài liệu đã được chuẩn hóa, bao gồm loại học phần (tự chọn hoặc bắt buộc), học kỳ tổ chức, khoa phụ trách, số tín chỉ, phương pháp giảng dạy, cơ cấu đánh giá và các yêu cầu tiên quyết.

Bên cạnh các thông tin hành chính, phần mô tả còn bao hàm nội dung chuyên môn và định hướng đào tạo của môn học, chẳng hạn như mục tiêu môn học, chuẩn đầu ra dự kiến, các chủ đề trọng tâm và tài liệu học tập được khuyến nghị. Dữ liệu cũng thể hiện cụ thể các tiêu chí đánh giá, bao gồm yêu cầu về chuyên cần, ngưỡng điểm đạt và tỷ trọng của các bài kiểm tra, bài thi.

Cách biểu diễn này tạo ra một đơn vị dữ liệu thống nhất, cho phép các mô hình xử lý ngôn ngữ tự nhiên khai thác đồng thời thông tin ngữ nghĩa và các ràng buộc mang tính quy định của nhà trường. Đây là cơ sở quan trọng cho quá trình truy xuất thông tin, đối sánh câu hỏi với dữ liệu môn học và sinh câu trả lời trong các hệ thống hỏi đáp học thuật.
## Đóng góp kỹ thuật cốt lõi: Kết nối truy vấn ngôn ngữ tự nhiên với dữ liệu học thuật có cấu trúc
Đóng góp cốt lõi của dự án không chỉ nằm ở việc xây dựng thành công một ứng dụng hỏi đáp, mà còn ở việc triển khai và tối ưu hóa một quy trình xử lý ngôn ngữ tự nhiên tiếng Việt phục vụ nhu cầu truy xuất tri thức học thuật nội bộ.

Nghiên cứu tập trung giải quyết vấn đề không tương thích về ngữ nghĩa (semantic misalignment) giữa cách sinh viên diễn đạt câu hỏi bằng ngôn ngữ tự nhiên đa dạng, linh hoạt và không theo khuôn mẫu với cấu trúc chuẩn hóa, chặt chẽ của các quy định đào tạo và dữ liệu môn học.

Để giải quyết vấn đề này, hệ thống đề xuất kiến trúc kết hợp giữa Retrieval-Augmented Generation (RAG) và HippoRAG. Sự kết hợp này hướng đến việc duy trì ngữ cảnh và các mối quan hệ giữa những thực thể trong quá trình truy xuất, qua đó hỗ trợ chuẩn hóa thực thể môn học, nhận diện chính xác các khái niệm học thuật và cải thiện khả năng liên kết giữa câu hỏi của người dùng với nguồn tri thức chính thức.

Kiến trúc được thiết kế nhằm hạn chế hiện tượng mô hình ngôn ngữ lớn tạo ra thông tin không có căn cứ (hallucination). Đây là yêu cầu quan trọng đối với các hệ thống tư vấn học thuật, trong đó độ chính xác của mã môn học, điều kiện tiên quyết và quy định đào tạo có ảnh hưởng trực tiếp đến quyết định của sinh viên.
3. Tác động thực tiễn: Trợ lý học vụ ảo đáng tin cậy cho giáo dục đại học
Về phương diện ứng dụng, hệ thống hướng đến việc xây dựng một trợ lý học vụ ảo có khả năng hỗ trợ sinh viên 24/7, cung cấp thông tin nhanh chóng, thuận tiện và có căn cứ từ dữ liệu học thuật chính thức.

Hệ thống có tiềm năng giảm tải các công việc hành chính và giải đáp những câu hỏi lặp lại cho đội ngũ cán bộ học vụ tại Khoa Toán – Tin học, đồng thời giúp sinh viên chủ động tiếp cận thông tin liên quan đến chương trình đào tạo, nội dung môn học và các yêu cầu học tập.

Khác với những chatbot thông thường chủ yếu dựa vào khả năng sinh ngôn ngữ của mô hình, giải pháp này hướng đến việc ràng buộc câu trả lời với các bản ghi học thuật chính thức. Những thông tin quan trọng như mã môn học, điều kiện tiên quyết và chuẩn đầu ra cần được đối chiếu với nguồn dữ liệu tương ứng, thay vì chỉ dựa vào kiến thức có sẵn của mô hình ngôn ngữ.

Nhờ đó, hệ thống tạo nền tảng cho việc cung cấp thông tin học thuật nhất quán, minh bạch và có khả năng kiểm chứng. Khi được đánh giá và kiểm soát chất lượng đầy đủ, giải pháp có thể được tích hợp vào quy trình hỗ trợ sinh viên của nhà trường mà vẫn duy trì tính toàn vẹn của dữ liệu.
## Ý nghĩa phương pháp luận: RAG tăng cường đồ thị tri thức cho ngôn ngữ ít tài nguyên
Ngoài phạm vi của một dự án học thuật cụ thể, nghiên cứu còn hướng đến việc xây dựng một khung phương pháp có khả năng mở rộng cho các hệ thống RAG tăng cường đồ thị tri thức (Knowledge Graph–enhanced RAG) trong những ngôn ngữ ít tài nguyên, chẳng hạn như tiếng Việt.

Nghiên cứu nhấn mạnh vai trò của việc kết hợp tri thức có cấu trúc thuộc một lĩnh vực chuyên biệt với các mô hình ngôn ngữ lớn trong quá trình xử lý những nguồn dữ liệu nội bộ có yêu cầu cao về độ chính xác.

Trong bối cảnh tiếng Việt, người dùng có thể đặt câu hỏi bằng nhiều cách diễn đạt khác nhau, trong khi dữ liệu nguồn thường được tổ chức theo các thuật ngữ, tên gọi và quy tắc chuẩn hóa. Việc khai thác đồ thị tri thức cùng các phương pháp truy xuất ngữ nghĩa có thể hỗ trợ hệ thống xác định các thực thể liên quan, duy trì mối quan hệ giữa những khái niệm và cải thiện khả năng truy xuất thông tin trong các tình huống phức tạp.

Về lâu dài, khung phương pháp này có tiềm năng được mở rộng sang các lĩnh vực chuyên biệt khác như y tế, pháp lý và quản lý quy trình doanh nghiệp. Đây đều là những lĩnh vực đòi hỏi sự cân bằng giữa khả năng tương tác bằng ngôn ngữ tự nhiên, tính linh hoạt trong truy vấn và độ chính xác của thông tin được cung cấp.
## I. Executive Summary

### 1.1. Tổng quan

**HCMUS-RAG** là hệ thống hỏi–đáp và truy xuất tri thức học phần được thiết kế để tiếp nhận câu hỏi bằng **tiếng Việt**, trong khi nguồn tri thức có thể được chuẩn hóa hoặc lưu trữ bằng **tiếng Anh**. Dự án hướng đến bài toán thường gặp trong môi trường đại học: sinh viên diễn đạt tên môn học bằng ngôn ngữ tự nhiên, từ viết tắt hoặc biến thể không chuẩn, còn danh mục học phần và đề cương sử dụng tên tiếng Anh có cấu trúc.

Thay vì phụ thuộc hoàn toàn vào so khớp từ khóa hoặc câu trả lời từ tri thức tham số của mô hình ngôn ngữ lớn (Large Language Model — LLM), hệ thống xây dựng một pipeline gồm xử lý truy vấn, chuẩn hóa thực thể học phần, truy xuất thông tin từ nguồn tri thức và tạo câu trả lời dựa trên ngữ cảnh được truy hồi. Module ánh xạ tên môn học giúp kết nối cách diễn đạt tiếng Việt với tên học phần tiếng Anh đã chuẩn hóa. Đây là lớp tiền xử lý quan trọng để hạn chế lỗi truy xuất do khác biệt ngôn ngữ và cách viết.

Theo định hướng nghiên cứu, hệ thống xem xét cả **RAG cơ bản** và hướng mở rộng **HippoRAG-2**, trong đó đồ thị tri thức hỗ trợ khai thác quan hệ giữa các thực thể và phục vụ các truy vấn cần kết nối thông tin qua nhiều bước. Phạm vi dữ liệu nghiên cứu gồm chương trình đào tạo của ba ngành: **Toán Tin, Toán Ứng dụng và Khoa học Dữ liệu**, với đề cương môn học theo mẫu ASIIN.

### 1.2. Bài toán và mục tiêu

- **Đầu vào:** câu hỏi tự do bằng tiếng Việt, có thể chứa tên môn học, từ viết tắt hoặc cách diễn đạt không chuẩn.
- **Nguồn tri thức:** danh mục học phần và tài liệu đào tạo, trong đó tên học phần hoặc nội dung có thể được trình bày bằng tiếng Anh.
- **Đầu ra:** thực thể học phần được ánh xạ, các tài liệu liên quan được truy hồi và câu trả lời được tạo sinh dựa trên bằng chứng phù hợp.
- **Mục tiêu kỹ thuật:** tăng khả năng truy xuất xuyên ngôn ngữ, giảm phụ thuộc vào khớp từ vựng chính xác và tạo cơ sở đánh giá định lượng cho từng thành phần của pipeline.

### 1.3. Điểm nổi bật

| Thành phần | Giá trị kỹ thuật |
|---|---|
| Vietnamese-first query processing | Tiếp nhận cách diễn đạt tự nhiên, từ viết tắt và biến thể tên học phần tiếng Việt. |
| LLM-based entity normalization | Sử dụng LLM để trích xuất thực thể và đề xuất các cách diễn đạt tiếng Anh phù hợp với ngữ cảnh học thuật. |
| Hybrid Retrieval | Kết hợp tín hiệu từ vựng, tương đồng chuỗi và tương đồng ngữ nghĩa thay vì dựa vào một độ đo duy nhất. |
| Explicit thresholding | Có thể từ chối ánh xạ khi điểm không đạt ngưỡng, thay vì luôn ép chọn một kết quả. |
| RAG grounding | Dùng tài liệu truy hồi làm ngữ cảnh cho câu trả lời, giúp tăng khả năng kiểm chứng nguồn thông tin. |
| Graph-based extension | Định hướng tích hợp HippoRAG-2 để khai thác liên kết giữa các thực thể và hỗ trợ truy vấn nhiều bước. |
| Evaluation-oriented design | Tách quy trình ánh xạ và đánh giá để có thể kiểm tra lỗi, so sánh cấu hình và theo dõi chất lượng. |

> **Phạm vi tuyên bố:** các trọng số, ngưỡng, lệnh CLI và schema JSON trong README này mô tả cấu hình mục tiêu theo đặc tả dự án. Hãy đối chiếu chúng với mã nguồn hiện tại trước khi xem là hành vi đã được xác nhận. Không có số liệu benchmark nào được giả định trong tài liệu này.

## II. Architecture & Methodology

### 2.1. Kiến trúc tổng thể

Hệ thống có thể được mô tả qua hai luồng liên kết: (1) **Course Mapping Pipeline** chuẩn hóa truy vấn tiếng Việt thành tên học phần tiếng Anh; và (2) **RAG Pipeline** dùng thực thể đã chuẩn hóa để truy xuất tài liệu và tạo câu trả lời. Module ánh xạ giúp giảm khoảng cách giữa ngôn ngữ truy vấn và ngôn ngữ của kho tri thức.

<p align="center">
    <img width="777" height="452" alt="image" src="https://github.com/user-attachments/assets/5673681f-d143-44e6-bd24-61a7c82f4f36" />
<br>
  <em></b> Kiến trúc hệ thống RAG</em>
</p>

<p align="center">
    <img width="785" height="447" alt="image" src="https://github.com/user-attachments/assets/a0457cde-a4a6-4ed9-afa0-83c202988366" />

<br>
  <em></b> Kiến trúc hệ thống HippoRAG</em>
</p>



### 2.2. Phase 1 — Input Processing & Term Extraction

Mục tiêu của giai đoạn này là xác định thực thể học phần hoặc thuật ngữ đào tạo được nhắc đến trong câu hỏi tiếng Việt. Người dùng có thể nhập tên đầy đủ, viết tắt hoặc mô tả gần nghĩa, chẳng hạn “môn XSTK”, “xác suất thống kê” hoặc một câu hỏi có chứa tên học phần trong ngữ cảnh dài hơn.

LLM được dùng như một bộ phân tích ngôn ngữ để xác định cụm từ có khả năng đại diện cho thực thể cần tra cứu. Kết quả nên được chuẩn hóa thành trường dữ liệu rõ ràng để các bước sau xử lý nhất quán.

**Các tình huống cần xử lý:**

- **Term extracted:** phát hiện được một hoặc nhiều thuật ngữ có khả năng là tên học phần.
- **Ambiguous term:** cụm từ có thể chỉ nhiều học phần; hệ thống nên giữ thông tin mơ hồ hoặc yêu cầu làm rõ.
- **No term extracted:** câu hỏi không chứa thực thể học phần có thể ánh xạ; không nên tự động chọn một môn học tùy ý.

Việc trích xuất thực thể không đồng nghĩa với việc đã xác nhận học phần tồn tại trong danh mục. Xác nhận cuối cùng cần dựa trên bước truy xuất và ngưỡng quyết định.

### 2.3. Phase 2 — Multilingual Candidate Generation

Sau khi trích xuất thuật ngữ tiếng Việt, LLM đề xuất các biến thể tiếng Anh có khả năng tương ứng với tên học phần chuẩn. Các biến thể cần ưu tiên cách dùng trong bối cảnh giáo dục đại học, giữ nguyên ý nghĩa chuyên ngành và tránh dịch từng từ một cách máy móc.

Ví dụ minh họa:

```json
{
  "vi_term": "xác suất thống kê",
  "candidates_en": [
    "Probability and Statistics",
    "Probability Theory and Statistics"
  ]
}
```

Ví dụ trên chỉ minh họa cấu trúc dữ liệu; danh sách ứng viên thực tế phụ thuộc vào phản hồi của mô hình và danh mục học phần đang dùng. Các ứng viên do LLM sinh ra được xem là **candidate queries**, không phải sự thật đã xác minh. Chúng phải được so sánh với catalog trước khi chấp nhận ánh xạ.

### 2.4. Phase 3 — Hybrid Retrieval & Scoring Pipeline

Hybrid Retrieval kết hợp ba tín hiệu bổ trợ nhau:

1. **FTS / Token Overlap:** đo mức độ trùng lặp từ hoặc token giữa truy vấn và tên học phần.
2. **Fuzzy String Matching:** đo mức tương đồng bề mặt giữa các chuỗi, hữu ích với lỗi chính tả, biến thể hoặc khác biệt nhỏ trong cách viết.
3. **Semantic Embedding Vector Search:** biểu diễn truy vấn và tên học phần thành vector, sau đó so sánh mức tương đồng ngữ nghĩa. Thành phần này giúp xử lý trường hợp hai chuỗi khác nhau về từ vựng nhưng gần nhau về ý nghĩa.

Theo cấu hình mục tiêu của đặc tả, các trọng số được đặt như sau:

| Thành phần | Ký hiệu | Trọng số |
|---|---:|---:|
| FTS / Token Overlap | \(S_{FTS}\) | \(W_{FTS}=0.35\) |
| Fuzzy String Matching | \(S_{Fuzzy}\) | \(W_{Fuzzy}=0.25\) |
| Semantic Embedding Similarity | \(S_{Sem}\) | \(W_{Sem}=0.40\) |

#### Weighted Hybrid Score

Với các thành phần điểm đã được chuẩn hóa về cùng miền giá trị, điểm kết hợp được định nghĩa:

\[
S_{\text{hybrid}} =
W_{FTS}S_{FTS}
+ W_{Fuzzy}S_{Fuzzy}
+ W_{Sem}S_{Sem}
\]

Thay các trọng số theo cấu hình mục tiêu:

\[
S_{\text{hybrid}} =
0.35S_{FTS}
+ 0.25S_{Fuzzy}
+ 0.40S_{Sem}
\]

Trong đó:

- \(S_{FTS}\): điểm truy xuất dựa trên token overlap hoặc kết quả FTS đã chuẩn hóa.
- \(S_{Fuzzy}\): điểm tương đồng chuỗi đã chuẩn hóa.
- \(S_{Sem}\): điểm tương đồng vector ngữ nghĩa đã được chuyển về thang đo tương thích với các thành phần còn lại.
- \(W_{FTS}\), \(W_{Fuzzy}\), \(W_{Sem}\): trọng số của từng tín hiệu.

**Lưu ý triển khai:** công thức có ý nghĩa so sánh khi các thành phần điểm nằm trên thang đo tương thích, thường là \([0,1]\). Nếu FTS hoặc fuzzy matcher trả về thang điểm khác, cần chuẩn hóa trước khi cộng trọng số. Không nên mặc định cosine similarity luôn nằm trong \([0,1]\) nếu chưa kiểm tra mô hình embedding và phép biến đổi được dùng.

#### Exact-match Bonus

Một kết quả trùng khớp chính xác với tên học phần chuẩn có thể được ưu tiên bằng một bonus. Một dạng công thức tổng quát có thể dùng là:

\[
S_{\text{final}} =
\min\left(1,\ S_{\text{hybrid}} + \lambda I_{\text{exact}}\right)
\]

Trong đó:

- \(I_{\text{exact}}=1\) nếu điều kiện exact match được thỏa mãn; ngược lại \(I_{\text{exact}}=0\).
- \(\lambda\) là hệ số bonus được cấu hình trong chương trình.
- Hàm \(\min(1,\cdot)\) giới hạn điểm cuối tối đa bằng \(1\).

Đây là **định nghĩa tham chiếu** để mô tả logic bonus, không khẳng định mã nguồn hiện tại dùng đúng công thức này. Khi triển khai, cần xác định rõ exact match áp dụng cho chuỗi gốc, chuỗi đã chuẩn hóa, tên chuẩn trong catalog hay mã học phần. Nếu bonus được sử dụng, cần kiểm tra nó không khiến một ứng viên sai vượt ngưỡng chỉ vì chuẩn hóa chuỗi quá rộng.

### 2.5. Phase 4 — Thresholding & Decision Making

Sau khi tính điểm cho các ứng viên, hệ thống xếp hạng theo điểm cuối và xem xét ứng viên đứng đầu. Theo cấu hình mục tiêu, ngưỡng chấp nhận là:

\[
\tau = 0.85
\]

Quy tắc quyết định:

\[
\text{retrieved} =
\begin{cases}
\text{true}, & S_{\text{final}} \geq 0.85 \\
\text{false}, & S_{\text{final}} < 0.85
\end{cases}
\]

- **Accepted mapping:** điểm đạt hoặc vượt ngưỡng; hệ thống có thể trả về tên học phần chuẩn.
- **Threshold rejection:** không có ứng viên đạt ngưỡng; hệ thống nên báo chưa đủ tin cậy thay vì ép chọn top-1.
- **Out-of-catalog:** thuật ngữ có thể hợp lệ nhưng không tồn tại trong danh mục hiện tại. Đây là vấn đề khác với lỗi chính tả hoặc điểm số thấp và nên được thống kê riêng.

Ngưỡng \(0.85\) là tham số vận hành cần được hiệu chỉnh trên tập validation có nhãn. Ngưỡng cao thường giúp giảm các ánh xạ sai nhưng có thể làm tăng tỷ lệ từ chối; ngưỡng thấp có thể tăng coverage nhưng chấp nhận nhiều kết quả không chính xác hơn.

### 2.6. Từ ánh xạ học phần đến RAG

Sau khi tên học phần được ánh xạ, hệ thống sử dụng thực thể đó làm tín hiệu để truy xuất đề cương hoặc tài liệu liên quan. Trong RAG cơ bản, retriever lấy các đoạn văn phù hợp, sau đó generator tạo câu trả lời dựa trên câu hỏi và ngữ cảnh truy hồi. Về mặt khái niệm:

\[
p(y \mid x) = \sum_{z \in Z} p(y \mid x,z)\,p(z \mid x)
\]

Trong đó \(x\) là truy vấn, \(z\) là chứng cứ truy hồi và \(y\) là câu trả lời được sinh. Chất lượng câu trả lời phụ thuộc đáng kể vào mức độ liên quan và độ đầy đủ của chứng cứ truy hồi.

Hướng mở rộng HippoRAG-2 bổ sung cấu trúc đồ thị để biểu diễn liên hệ giữa các thực thể và tài liệu. Điều này đặc biệt có ý nghĩa với câu hỏi cần tổng hợp thông tin từ nhiều môn học hoặc lần theo quan hệ giữa các khái niệm. Đồ thị không thay thế việc kiểm chứng bằng văn bản nguồn; nó bổ sung một cơ chế tổ chức và truy hồi quan hệ.

## III. Data Specification

### 3.1. Input Data

#### `catalog.json`

Catalog chứa danh mục học phần chuẩn hóa. Schema tối thiểu theo đặc tả:

```json
[
  {
    "course_id": "COURSE_001",
    "name_en": "Probability and Statistics"
  },
  {
    "course_id": "COURSE_002",
    "name_en": "Linear Algebra"
  }
]
```

| Trường | Kiểu | Ý nghĩa |
|---|---|---|
| `course_id` | `string` | Định danh duy nhất của học phần. |
| `name_en` | `string` | Tên học phần tiếng Anh đã chuẩn hóa. |

Các trường bổ sung như `department`, `credits`, `prerequisites` hoặc `document_path` chỉ nên được thêm nếu pipeline thực tế hỗ trợ và có quy tắc kiểm tra dữ liệu tương ứng.

#### `queries.json`

Tập truy vấn kiểm thử có thể lưu dưới dạng danh sách đối tượng:

```json
[
  {
    "query_id": "Q001",
    "query": "Môn xác suất thống kê có nội dung gì?",
    "expected_course_id": "COURSE_001"
  },
  {
    "query_id": "Q002",
    "query": "Cho mình xem thông tin môn đại số tuyến tính",
    "expected_course_id": "COURSE_002"
  }
]
```

`expected_course_id` là nhãn tham chiếu phục vụ đánh giá offline; trường này không bắt buộc với truy vấn người dùng trực tiếp. Khi xây dựng benchmark, cần ghi rõ cách tạo nhãn, quy tắc xử lý nhiều đáp án hợp lệ và cách phân chia dữ liệu để tránh đánh giá thiên lệch.

### 3.2. Output Data

Một bản ghi kết quả ánh xạ có thể được chuẩn hóa theo schema sau:

```json
{
  "query_id": "Q001",
  "query": "Môn xác suất thống kê có nội dung gì?",
  "vi_term": "xác suất thống kê",
  "candidates_en": [
    "Probability and Statistics",
    "Probability Theory and Statistics"
  ],
  "predicted_en_top1": "Probability and Statistics",
  "score": 0.91,
  "breakdown": {
    "fts": 0.88,
    "fuzzy": 0.93,
    "semantic": 0.92
  },
  "retrieved": true
}
```

**Các giá trị số trong ví dụ chỉ mang tính minh họa**, không phải kết quả benchmark thực tế.

| Trường | Ý nghĩa |
|---|---|
| `vi_term` | Thuật ngữ tiếng Việt được trích xuất. |
| `candidates_en` | Danh sách biến thể tiếng Anh do bước candidate generation tạo ra. |
| `predicted_en_top1` | Ứng viên được xếp hạng cao nhất; có thể là `null` nếu không có kết quả hợp lệ. |
| `score` | Điểm cuối dùng cho quyết định, sau khi áp dụng quy tắc kết hợp điểm được triển khai. |
| `breakdown` | Điểm thành phần của FTS, fuzzy và semantic. |
| `retrieved` | Trạng thái chấp nhận ánh xạ theo ngưỡng. |

Tên trường và cách xử lý trường hợp thất bại cần thống nhất với code. Nếu output còn lưu `course_id`, `error_type`, `latency_ms` hoặc `raw_response`, nên mô tả rõ các trường đó trong schema chính thức.

### 3.3. `evaluation_report.json`

File báo cáo đánh giá nên lưu cấu hình chạy, số lượng mẫu và kết quả tổng hợp để đảm bảo khả năng tái lập. Ví dụ schema tham khảo:

```json
{
  "run_config": {
    "threshold": 0.85,
    "weights": {
      "fts": 0.35,
      "fuzzy": 0.25,
      "semantic": 0.40
    }
  },
  "summary": {
    "total_queries": 100,
    "retrieved_queries": 82,
    "retrieval_rate": 0.82,
    "top1_accuracy_at_threshold": 0.95
  },
  "error_analysis": {
    "no_term_extracted": 5,
    "out_of_catalog": 8,
    "threshold_rejection": 5
  }
}
```

Toàn bộ số liệu trong ví dụ trên là **dữ liệu giả lập để minh họa schema**, không đại diện cho hiệu năng hệ thống. Cần xác định chính xác mẫu số của từng metric trước khi diễn giải báo cáo.

## IV. Installation & Usage

### 4.1. Prerequisites

- Python **3.9+** (nên dùng đúng phiên bản đã được kiểm thử với các dependency của repository).
- Git.
- Gemini API key có quyền truy cập model được cấu hình trong code, ví dụ `gemini-2.5-flash`.
- Catalog và tập truy vấn ở định dạng mà script hỗ trợ.
- Kết nối mạng khi gọi Gemini API hoặc tải model embedding lần đầu.

### 4.2. Clone repository

```bash
git clone https://github.com/binhba186/A-Vietnamese-Course-Query-System-using-RAG-over-English-Knowledge-Sources.git
cd A-Vietnamese-Course-Query-System-using-RAG-over-English-Knowledge-Sources
```

### 4.3. Tạo môi trường ảo

**Windows PowerShell**

```powershell
py -3.9 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

**Linux / macOS**

```bash
python3.9 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

### 4.4. Cài đặt dependencies

Nếu repository có `requirements.txt`:

```bash
pip install -r requirements.txt
```

Nếu repository cung cấp `pyproject.toml` hoặc tệp quản lý dependency khác, hãy dùng tệp đó làm nguồn cài đặt chính. Tránh cài các phiên bản thư viện tùy ý khi dự án chưa có khóa phiên bản, vì khác biệt API có thể làm thay đổi hành vi của model hoặc pipeline.

Các thư viện thuộc phạm vi công nghệ của dự án có thể bao gồm:

- `google-genai` hoặc SDK Gemini đang được script sử dụng.
- `sentence-transformers` cho semantic embeddings.
- `scikit-learn` cho các tiện ích xử lý hoặc đánh giá nếu có dùng.
- `rapidfuzz` cho fuzzy matching.
- `torch` làm backend cho các mô hình embedding.

Danh sách trên là gợi ý theo công nghệ được mô tả; **`requirements.txt` của repository mới là nguồn chuẩn** về dependency thực tế.

### 4.5. Cấu hình API key

Đặt API key trong biến môi trường thay vì ghi trực tiếp vào mã nguồn.

**Windows PowerShell**

```powershell
$env:GEMINI_API_KEY = "YOUR_API_KEY"
```

**Linux / macOS**

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

Tên biến môi trường cần khớp với tên mà script đọc. Nếu mã nguồn dùng tên khác, hãy điều chỉnh theo triển khai thực tế. Không commit API key, file `.env` hoặc log có chứa thông tin xác thực lên Git.

### 4.6. Chạy module ánh xạ

Theo tên script trong đặc tả dự án, lệnh chạy cơ bản có thể là:

```bash
python mapping_LLm.py
```

Nếu script hỗ trợ các tham số CLI được yêu cầu, một lệnh chạy với input/output tường minh có thể là:

```bash
python mapping_LLm.py \
  --catalog data/catalog.json \
  --queries data/queries.json \
  --sleep 1.0 \
  --out outputs/mapping_results.json
```

Ý nghĩa tham số dự kiến:

| Tham số | Ý nghĩa |
|---|---|
| `--catalog` | Đường dẫn tới catalog học phần. |
| `--queries` | Đường dẫn tới tập truy vấn đầu vào. |
| `--sleep` | Khoảng nghỉ giữa các lần gọi API nếu script triển khai cơ chế này. |
| `--out` | Đường dẫn ghi kết quả ánh xạ. |

Hãy kiểm tra giao diện CLI thực tế bằng:

```bash
python mapping_LLm.py --help
```

Nếu script không định nghĩa một trong các tham số trên, hãy dùng đúng cú pháp mà `--help` hiển thị; không nên coi lệnh minh họa là giao diện CLI đã được xác minh.

### 4.7. Chạy đánh giá

Nếu repository có script đánh giá `mapping_eval.py`, có thể kiểm tra cú pháp trước:

```bash
python mapping_eval.py --help
```

Một lệnh tham khảo theo các tham số trong đặc tả:

```bash
python mapping_eval.py \
  --catalog data/catalog.json \
  --queries data/queries.json \
  --out outputs/evaluation_report.json
```

Đảm bảo tập queries có nhãn tham chiếu nếu metric yêu cầu đáp án đúng. Không dùng chính dữ liệu đã dùng để tinh chỉnh trọng số và ngưỡng làm bằng chứng duy nhất cho khả năng tổng quát hóa. Nên tách train/validation/test hoặc ít nhất tách tập hiệu chỉnh ngưỡng khỏi tập báo cáo cuối.

### 4.8. Thực hành vận hành tốt

- Ghi lại phiên bản Python, dependency, model embedding, tên model LLM và thời điểm chạy.
- Lưu cấu hình trọng số và ngưỡng trong báo cáo để có thể tái lập.
- Thực hiện retry có giới hạn và exponential backoff khi gặp rate limit hoặc lỗi tạm thời.
- Không ghi API key hoặc dữ liệu nhạy cảm vào log.
- Lưu lại trường hợp bị từ chối và lý do để phục vụ phân tích lỗi.
- Khi cập nhật catalog, chạy lại benchmark để kiểm tra các ánh xạ cũ có bị thay đổi hay không.

## V. Evaluation Metrics & Benchmark

### 5.1. Nguyên tắc đánh giá

Đánh giá nên phân biệt hai câu hỏi:

1. **Mapping quality:** hệ thống có xác định đúng học phần chuẩn từ truy vấn tiếng Việt hay không?
2. **RAG answer quality:** sau khi ánh xạ và truy hồi, câu trả lời có đúng, đủ và bám sát tài liệu nguồn hay không?

Điểm ánh xạ cao không tự động chứng minh câu trả lời RAG chính xác. Tương tự, một câu trả lời trôi chảy không chứng minh retriever đã lấy đúng bằng chứng. Nên đánh giá riêng từng tầng và bổ sung đánh giá end-to-end.

### 5.2. Retrieval Rate

Với \(N\) truy vấn đánh giá và \(N_{\text{accepted}}\) truy vấn được chấp nhận theo ngưỡng:

\[
\text{Retrieval Rate} =
\frac{N_{\text{accepted}}}{N}
\]

Metric này đo tỷ lệ truy vấn được hệ thống chấp nhận ánh xạ. Nó **không đo trực tiếp độ chính xác**: hệ thống có thể có Retrieval Rate cao nhưng chấp nhận nhiều ánh xạ sai.

### 5.3. Top-1 Accuracy @ Threshold

Đặt \(A_{\tau}\) là tập truy vấn được chấp nhận tại ngưỡng \(\tau\). Nếu đánh giá độ chính xác trong số các kết quả được chấp nhận:

\[
\text{Top-1 Accuracy @ Threshold} =
\frac{\sum_{i \in A_{\tau}}
\mathbb{1}[\hat{c}_i = c_i^*]}
{|A_{\tau}|}
\]

Trong đó \(\hat{c}_i\) là học phần dự đoán, \(c_i^*\) là nhãn tham chiếu và \(\mathbb{1}[\cdot]\) là hàm chỉ báo. Nếu không có truy vấn nào được chấp nhận, metric này không xác định; nên báo `null` thay vì gán bằng 0 một cách tùy tiện.

Để đánh giá đầy đủ hơn, nên báo thêm:

- **Coverage / Acceptance Rate:** tỷ lệ truy vấn được hệ thống đưa ra kết quả.
- **Precision among accepted mappings:** tỷ lệ ánh xạ được chấp nhận mà thực sự đúng.
- **End-to-end answer correctness:** độ đúng của câu trả lời cuối dựa trên rubric có nhãn.
- **Recall@k:** tỷ lệ truy vấn mà tài liệu liên quan xuất hiện trong top-k kết quả truy hồi.
- **Latency:** thời gian xử lý trung bình và các phân vị như p50/p95.
- **API usage / cost:** số lần gọi và chi phí ước tính nếu có thể đo được.

### 5.4. Summary Table

Điền số liệu sau khi chạy benchmark thực tế; không nên công bố các ô chưa đo như kết quả dự án.

| Metric | Giá trị | Ghi chú |
|---|---:|---|
| Number of test queries | — | Số truy vấn có nhãn hợp lệ. |
| Retrieval Rate | — | Tỷ lệ truy vấn được chấp nhận theo ngưỡng. |
| Top-1 Accuracy @ Threshold | — | Độ chính xác trên các kết quả được chấp nhận; ghi rõ mẫu số. |
| Precision among accepted mappings | — | Tỷ lệ mapping được chấp nhận và đúng. |
| Recall@k | — | Đánh giá retriever trên tài liệu liên quan. |
| Mean / Median latency | — | Cần ghi rõ có tính thời gian gọi API hay không. |
| Rejected queries | — | Số truy vấn bị từ chối do điểm dưới ngưỡng. |

### 5.5. Error Analysis

| Nhóm lỗi | Mô tả | Hướng xử lý |
|---|---|---|
| `no_term_extracted` | Không trích xuất được thuật ngữ học phần từ truy vấn. | Cải thiện prompt, bổ sung ví dụ, cho phép hỏi lại hoặc trích xuất nhiều thực thể. |
| `out_of_catalog` | Thuật ngữ có ý nghĩa nhưng học phần không tồn tại trong catalog. | Cập nhật catalog, báo không tìm thấy hoặc đề xuất kết quả gần nhất kèm cảnh báo. |
| `threshold_rejection` | Có ứng viên nhưng điểm thấp hơn ngưỡng. | Phân tích phân phối điểm, hiệu chỉnh ngưỡng trên validation và kiểm tra từng thành phần điểm. |
| `wrong_top1` | Có ứng viên đúng nhưng hệ thống xếp hạng sai. | Phân tích trọng số, chuẩn hóa điểm, bổ sung hard negatives hoặc re-ranking. |
| `ambiguous_query` | Truy vấn có thể chỉ nhiều học phần. | Trả về lựa chọn làm rõ thay vì khẳng định một đáp án. |
| `retrieval_miss` | Ánh xạ đúng nhưng tài liệu cần thiết không xuất hiện trong top-k. | Cải thiện indexing, chunking, metadata filtering và retriever. |
| `generation_error` | Tài liệu đã truy hồi nhưng câu trả lời sai hoặc không bám nguồn. | Tăng chất lượng context, yêu cầu trích dẫn chứng cứ và đánh giá faithfulness. |

### 5.6. Benchmark protocol khuyến nghị

1. Xây dựng tập truy vấn có nhãn gồm tên đầy đủ, viết tắt, biến thể diễn đạt, lỗi chính tả và câu hỏi không thuộc catalog.
2. Tách tập hiệu chỉnh và tập kiểm thử. Chỉ dùng validation để lựa chọn trọng số hoặc ngưỡng.
3. Đánh giá baseline riêng lẻ: FTS, fuzzy matching và semantic similarity.
4. So sánh từng baseline với Hybrid Retrieval để xác định đóng góp của từng tín hiệu.
5. Báo cáo cả độ chính xác và coverage; không chỉ báo một con số accuracy.
6. Đánh giá RAG bằng các câu hỏi có đáp án tham chiếu, nguồn tài liệu và tiêu chí chấm nhất quán.
7. Lưu lỗi theo nhóm để hỗ trợ phân tích định tính và tái lập kết quả.

## VI. Directory Structure

Cấu trúc dưới đây là **cấu trúc tham khảo logic**, không phải bản chụp đã xác minh của repository. Giữ nguyên các tên file thực tế nếu dự án hiện tại tổ chức khác.

```text
A-Vietnamese-Course-Query-System-using-RAG-over-English-Knowledge-Sources/
├── README.md
├── requirements.txt                 # Dependencies (nếu repository có)
├── mapping_LLm.py                   # Vietnamese-to-English course mapping
├── mapping_eval.py                  # Mapping evaluation (nếu có)
├── data/
│   ├── catalog.json                 # Canonical course catalog
│   └── queries.json                 # Evaluation/user queries
├── documents/                       # Course outlines and source documents
├── outputs/
│   ├── mapping_results.json         # Mapping predictions
│   └── evaluation_report.json       # Evaluation summary
├── notebooks/                       # Exploratory experiments (nếu có)
└── .gitignore
```

| Thành phần | Vai trò |
|---|---|
| `mapping_LLm.py` | Module ánh xạ truy vấn tiếng Việt sang tên học phần tiếng Anh theo pipeline triển khai. |
| `mapping_eval.py` | Chạy đánh giá offline và tổng hợp metric nếu script này tồn tại trong repository. |
| `data/catalog.json` | Danh mục tên học phần chuẩn để xác nhận ứng viên. |
| `data/queries.json` | Bộ truy vấn kiểm thử; nên có nhãn tham chiếu để tính metric có giám sát. |
| `documents/` | Tài liệu nguồn dùng cho retrieval/RAG, nếu được lưu trực tiếp trong repo. |
| `outputs/` | Kết quả chạy và báo cáo đánh giá; cần cân nhắc không commit dữ liệu lớn hoặc nhạy cảm. |

Để README phản ánh chính xác mã nguồn, hãy thay cây thư mục tham khảo bằng kết quả thực tế từ `tree` hoặc `find` sau khi kiểm tra repository.

## VII. Limitations & Future Work

### 7.1. Hạn chế

**1. Rate limit và độ trễ của LLM API**

Việc gọi LLM để trích xuất thực thể và tạo candidate có thể tăng độ trễ, chi phí và nguy cơ lỗi khi vượt giới hạn API. Nên có retry có giới hạn, backoff, cache cho các truy vấn lặp và cơ chế ghi log để phân biệt lỗi dịch vụ với lỗi nội dung.

**2. Out-of-Vocabulary (OOV) và catalog coverage**

Hybrid Retrieval chỉ có thể ánh xạ chính xác tới học phần hiện diện trong catalog hoặc có metadata đủ để nhận diện. Học phần mới, tên viết tắt chưa biết hoặc thuật ngữ ngoài miền có thể bị từ chối hoặc ánh xạ nhầm sang một mục gần nghĩa.

**3. Candidate generation có thể tạo biến thể sai**

LLM có thể tạo tên tiếng Anh không chuẩn, dịch quá sát mặt chữ hoặc sinh thuật ngữ nghe hợp lý nhưng không tồn tại trong chương trình đào tạo. Vì vậy, candidate generation chỉ nên tạo ứng viên; catalog mới là nguồn xác nhận tên học phần chuẩn.

**4. Điểm của các retriever không đồng nhất**

FTS, fuzzy matching và cosine similarity có phân phối điểm khác nhau. Nếu không chuẩn hóa đúng cách, trọng số có thể không phản ánh đóng góp thực tế của từng thành phần. Exact-match bonus cũng cần được kiểm thử để tránh làm tăng điểm giả tạo.

**5. Threshold phụ thuộc dữ liệu**

Ngưỡng \(0.85\) không phải hằng số phổ quát. Hiệu quả của nó phụ thuộc catalog, cách chuẩn hóa, embedding model và phân phối truy vấn. Cần hiệu chỉnh trên validation và báo cáo cả accuracy lẫn coverage.

**6. Lỗi truy hồi có thể lan truyền sang câu trả lời**

Trong RAG, tài liệu không liên quan hoặc thiếu thông tin có thể khiến LLM tạo ra câu trả lời không có căn cứ. Hệ thống cần phân biệt “không tìm thấy bằng chứng” với “đã tìm thấy và có thể trả lời”, đồng thời ưu tiên trích dẫn nguồn hoặc dẫn chiếu tới tài liệu gốc.

**7. Đánh giá cần bao phủ cả retrieval lẫn generation**

Metric ánh xạ tên học phần không thể đại diện cho toàn bộ chất lượng RAG. Các câu hỏi đa bước còn cần đánh giá khả năng kết nối quan hệ, độ đầy đủ của bằng chứng và tính trung thực của câu trả lời.

### 7.2. Future Work

**1. Fine-tuning hoặc domain adaptation cho embedding**

Xây dựng tập positive/negative pairs từ truy vấn tiếng Việt và tên học phần tiếng Anh để đánh giá khả năng fine-tuning embedding theo miền. So sánh với mô hình multilingual baseline trên tập test cố định và báo cáo Recall@k, MRR hoặc nDCG khi phù hợp.

**2. Vector database và ANN indexing**

Khi số lượng tài liệu tăng, có thể sử dụng FAISS hoặc Milvus để lập chỉ mục vector và tìm kiếm láng giềng gần hiệu quả hơn. Việc lựa chọn cần dựa trên quy mô dữ liệu, yêu cầu cập nhật, latency và tài nguyên triển khai; với catalog nhỏ, tìm kiếm trực tiếp có thể vẫn đủ đơn giản và dễ kiểm soát.

**3. Re-ranking**

Sau bước lấy ứng viên top-k, bổ sung một reranker để đánh giá tương tác giữa truy vấn và từng ứng viên. Có thể so sánh reranking với việc chỉ dùng weighted score, đồng thời đo mức cải thiện về top-1 accuracy và latency.

**4. Knowledge Graph và HippoRAG-2**

Mô hình hóa các thực thể như học phần, chương trình đào tạo, tín chỉ, điều kiện tiên quyết và tài liệu; biểu diễn quan hệ dưới dạng cạnh có nhãn. Hướng HippoRAG-2 có thể được đánh giá trên câu hỏi multi-hop, chẳng hạn câu hỏi cần nối quan hệ giữa học phần và điều kiện tiên quyết. Cần so sánh công bằng với RAG cơ bản trên cùng corpus và bộ câu hỏi.

**5. Query rewriting và clarification**

Phân loại truy vấn thành câu hỏi tra cứu tên môn, nội dung đề cương, điều kiện tiên quyết hoặc câu hỏi chưa đủ rõ. Với truy vấn mơ hồ, hệ thống có thể hỏi người dùng chọn một trong các học phần gần nhất thay vì tự quyết định.

**6. Observability và reproducibility**

Ghi lại cấu hình model, phiên bản catalog, thời gian xử lý, điểm từng thành phần, quyết định threshold và lỗi API. Kết hợp versioning cho dữ liệu và tập benchmark để so sánh các lần cập nhật có thể tái lập.

**7. Đánh giá chất lượng câu trả lời RAG**

Bổ sung đánh giá answer correctness, faithfulness, context relevance và completeness bằng nhãn tham chiếu, đánh giá của con người hoặc LLM-as-a-judge có rubric rõ ràng. Các kết quả đánh giá bằng AI nên được kiểm tra chéo trên một mẫu bởi người đánh giá để hạn chế thiên lệch của giám khảo.

## Reproducibility & Research Notes

Để tăng tính minh bạch học thuật, một bản phát hành hoặc báo cáo thực nghiệm nên lưu:

- Phiên bản dữ liệu catalog và tài liệu nguồn.
- Phiên bản Python, dependency và embedding model.
- Tên model LLM, ngày chạy và cấu hình sinh nếu được phép công bố.
- Trọng số Hybrid Retrieval, định nghĩa exact match và threshold.
- Định nghĩa metric, mẫu số, quy tắc xử lý truy vấn bị từ chối và các trường hợp nhiều nhãn đúng.
- Kết quả baseline, kết quả Hybrid Retrieval và phân tích lỗi.
- Các giới hạn đã biết cùng điều kiện tái lập.

Không đưa API key, thông tin cá nhân hoặc tài liệu không được phép chia sẻ vào repository công khai.

## References

1. Lewis, P., et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. Advances in Neural Information Processing Systems (NeurIPS). https://arxiv.org/abs/2005.11401
2. Karpukhin, V., et al. (2020). *Dense Passage Retrieval for Open-Domain Question Answering*. EMNLP. https://arxiv.org/abs/2004.04906
3. Zhang, et al. *HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models*. Thông tin thư mục và phiên bản cần được xác nhận theo tài liệu HippoRAG cụ thể mà dự án sử dụng.
4. Tài liệu seminar của dự án: *Xây dựng hệ thống gợi ý môn học bằng tiếng Việt*, Khoa Toán – Tin học, Trường Đại học Khoa học Tự nhiên, ĐHQG-HCM (2026).

## Thành viên nhóm
- Trương Bình Ba (Truong Binh Ba)
- Lê Nguyễn Thành Tân (Le Nguyen Thanh Tan)
