<div align="center">
# A-Vietnamese-Course-Query-System-using-RAG-over-English-Knowledge-Sources

Hệ thống tra cứu khóa học tiếng Việt sử dụng RAG trên các nguồn kiến ​​thức tiếng Anh

Ánh xạ thực thể khóa học · Tạo ứng viên đa ngôn ngữ · Truy xuất kết hợp (FTS + Mờ + Ngữ nghĩa)

</div>
## 1. Mô tả cấu trúc dữ liệu đầu vào
Mỗi môn học trong bộ dữ liệu được biểu diễn dưới dạng một bản ghi có cấu trúc, bao gồm mã định danh duy nhất và phần mô tả chi tiết về môn học. Mã môn học (ví dụ: GEO00002) đóng vai trò là khóa chính, giúp xác định chính xác và tránh nhầm lẫn giữa các học phần. Trường văn bản đi kèm tổng hợp toàn bộ thông tin học thuật liên quan thành một tài liệu đã được chuẩn hóa, bao gồm loại học phần (tự chọn hoặc bắt buộc), học kỳ tổ chức, khoa phụ trách, số tín chỉ, phương pháp giảng dạy, cơ cấu đánh giá và các yêu cầu tiên quyết.

Bên cạnh các thông tin hành chính, phần mô tả còn bao hàm nội dung chuyên môn và định hướng đào tạo của môn học, chẳng hạn như mục tiêu môn học, chuẩn đầu ra dự kiến, các chủ đề trọng tâm và tài liệu học tập được khuyến nghị. Dữ liệu cũng thể hiện cụ thể các tiêu chí đánh giá, bao gồm yêu cầu về chuyên cần, ngưỡng điểm đạt và tỷ trọng của các bài kiểm tra, bài thi.

Cách biểu diễn này tạo ra một đơn vị dữ liệu thống nhất, cho phép các mô hình xử lý ngôn ngữ tự nhiên khai thác đồng thời thông tin ngữ nghĩa và các ràng buộc mang tính quy định của nhà trường. Đây là cơ sở quan trọng cho quá trình truy xuất thông tin, đối sánh câu hỏi với dữ liệu môn học và sinh câu trả lời trong các hệ thống hỏi đáp học thuật.
## 2. Đóng góp kỹ thuật cốt lõi: Kết nối truy vấn ngôn ngữ tự nhiên với dữ liệu học thuật có cấu trúc
Đóng góp cốt lõi của dự án không chỉ nằm ở việc xây dựng thành công một ứng dụng hỏi đáp, mà còn ở việc triển khai và tối ưu hóa một quy trình xử lý ngôn ngữ tự nhiên tiếng Việt phục vụ nhu cầu truy xuất tri thức học thuật nội bộ.

Nghiên cứu tập trung giải quyết vấn đề không tương thích về ngữ nghĩa (semantic misalignment) giữa cách sinh viên diễn đạt câu hỏi bằng ngôn ngữ tự nhiên đa dạng, linh hoạt và không theo khuôn mẫu với cấu trúc chuẩn hóa, chặt chẽ của các quy định đào tạo và dữ liệu môn học.

Để giải quyết vấn đề này, hệ thống đề xuất kiến trúc kết hợp giữa Retrieval-Augmented Generation (RAG) và HippoRAG. Sự kết hợp này hướng đến việc duy trì ngữ cảnh và các mối quan hệ giữa những thực thể trong quá trình truy xuất, qua đó hỗ trợ chuẩn hóa thực thể môn học, nhận diện chính xác các khái niệm học thuật và cải thiện khả năng liên kết giữa câu hỏi của người dùng với nguồn tri thức chính thức.

Kiến trúc được thiết kế nhằm hạn chế hiện tượng mô hình ngôn ngữ lớn tạo ra thông tin không có căn cứ (hallucination). Đây là yêu cầu quan trọng đối với các hệ thống tư vấn học thuật, trong đó độ chính xác của mã môn học, điều kiện tiên quyết và quy định đào tạo có ảnh hưởng trực tiếp đến quyết định của sinh viên.
3. Tác động thực tiễn: Trợ lý học vụ ảo đáng tin cậy cho giáo dục đại học
Về phương diện ứng dụng, hệ thống hướng đến việc xây dựng một trợ lý học vụ ảo có khả năng hỗ trợ sinh viên 24/7, cung cấp thông tin nhanh chóng, thuận tiện và có căn cứ từ dữ liệu học thuật chính thức.

Hệ thống có tiềm năng giảm tải các công việc hành chính và giải đáp những câu hỏi lặp lại cho đội ngũ cán bộ học vụ tại Khoa Toán – Tin học, đồng thời giúp sinh viên chủ động tiếp cận thông tin liên quan đến chương trình đào tạo, nội dung môn học và các yêu cầu học tập.

Khác với những chatbot thông thường chủ yếu dựa vào khả năng sinh ngôn ngữ của mô hình, giải pháp này hướng đến việc ràng buộc câu trả lời với các bản ghi học thuật chính thức. Những thông tin quan trọng như mã môn học, điều kiện tiên quyết và chuẩn đầu ra cần được đối chiếu với nguồn dữ liệu tương ứng, thay vì chỉ dựa vào kiến thức có sẵn của mô hình ngôn ngữ.

Nhờ đó, hệ thống tạo nền tảng cho việc cung cấp thông tin học thuật nhất quán, minh bạch và có khả năng kiểm chứng. Khi được đánh giá và kiểm soát chất lượng đầy đủ, giải pháp có thể được tích hợp vào quy trình hỗ trợ sinh viên của nhà trường mà vẫn duy trì tính toàn vẹn của dữ liệu.
## 4. Ý nghĩa phương pháp luận: RAG tăng cường đồ thị tri thức cho ngôn ngữ ít tài nguyên
Ngoài phạm vi của một dự án học thuật cụ thể, nghiên cứu còn hướng đến việc xây dựng một khung phương pháp có khả năng mở rộng cho các hệ thống RAG tăng cường đồ thị tri thức (Knowledge Graph–enhanced RAG) trong những ngôn ngữ ít tài nguyên, chẳng hạn như tiếng Việt.

Nghiên cứu nhấn mạnh vai trò của việc kết hợp tri thức có cấu trúc thuộc một lĩnh vực chuyên biệt với các mô hình ngôn ngữ lớn trong quá trình xử lý những nguồn dữ liệu nội bộ có yêu cầu cao về độ chính xác.

Trong bối cảnh tiếng Việt, người dùng có thể đặt câu hỏi bằng nhiều cách diễn đạt khác nhau, trong khi dữ liệu nguồn thường được tổ chức theo các thuật ngữ, tên gọi và quy tắc chuẩn hóa. Việc khai thác đồ thị tri thức cùng các phương pháp truy xuất ngữ nghĩa có thể hỗ trợ hệ thống xác định các thực thể liên quan, duy trì mối quan hệ giữa những khái niệm và cải thiện khả năng truy xuất thông tin trong các tình huống phức tạp.

Về lâu dài, khung phương pháp này có tiềm năng được mở rộng sang các lĩnh vực chuyên biệt khác như y tế, pháp lý và quản lý quy trình doanh nghiệp. Đây đều là những lĩnh vực đòi hỏi sự cân bằng giữa khả năng tương tác bằng ngôn ngữ tự nhiên, tính linh hoạt trong truy vấn và độ chính xác của thông tin được cung cấp.
## 5. Thách thức cốt lõi
### 5.1. Cân bằng giữa tương tác tự nhiên và độ chính xác của dữ liệu
Thách thức lớn nhất khi triển khai hệ thống hỏi đáp trong bối cảnh tiếng Việt là duy trì sự cân bằng giữa trải nghiệm hội thoại tự nhiên và độ chính xác của thông tin.

Người dùng mong muốn có thể đặt câu hỏi một cách linh hoạt, thân thiện và không cần tuân theo một cấu trúc cố định. Tuy nhiên, hệ thống vẫn phải bảo đảm rằng câu trả lời được tạo ra phù hợp với dữ liệu đã được xác minh và các quy định chính thức của cơ sở đào tạo.

Mâu thuẫn này trở nên đặc biệt quan trọng trong lĩnh vực tư vấn học vụ, bởi ngay cả những sai lệch nhỏ về mã môn học, điều kiện đăng ký hoặc yêu cầu tiên quyết cũng có thể dẫn đến những quyết định học tập không phù hợp.

Do đó, hệ thống không chỉ cần hiểu đúng ý định của người dùng mà còn phải kiểm soát chặt chẽ nguồn thông tin được sử dụng để tạo câu trả lời.
### 5.2. Sự bất đối xứng giữa đầu vào và đầu ra trong hệ thống hỏi đáp học thuật tiếng Việt
Ở phía đầu vào, sinh viên thường diễn đạt câu hỏi bằng tiếng Việt tự nhiên với nhiều hình thức khác nhau. Câu hỏi có thể sử dụng ngôn ngữ không trang trọng, từ viết tắt, cách gọi môn học theo thói quen hoặc những cụm từ chưa đầy đủ về mặt ngữ pháp và ngữ nghĩa.

Ngược lại, ở phía đầu ra, hệ thống phải đáp ứng các yêu cầu chuẩn hóa nghiêm ngặt. Tên môn học cần được đối chiếu chính xác với mã môn học chính thức; các thông tin về chuẩn đầu ra, điều kiện tiên quyết và quy định đào tạo phải phản ánh đúng nội dung trong tài liệu của nhà trường.

Sự khác biệt giữa đầu vào linh hoạt và đầu ra yêu cầu tính chuẩn xác cao tạo ra một thách thức đáng kể đối với những hệ thống chỉ dựa trên mô hình ngôn ngữ lớn hoặc phương pháp truy xuất văn bản truyền thống.

Vì vậy, hệ thống cần kết hợp các cơ chế hiểu ngữ nghĩa, chuẩn hóa thực thể và truy xuất dữ liệu phù hợp để chuyển đổi câu hỏi tự nhiên thành nhu cầu thông tin cụ thể, sau đó ánh xạ kết quả truy xuất trở lại thành câu trả lời dễ hiểu nhưng vẫn bảo toàn tính chính xác của dữ liệu gốc.
### 5.3. Nguy cơ tạo thông tin sai lệch và nhu cầu kiểm soát ngữ nghĩa
Khoảng cách giữa cách diễn đạt tự do của người dùng và yêu cầu chuẩn hóa của dữ liệu học thuật làm gia tăng nguy cơ mô hình ngôn ngữ tạo ra những câu trả lời nghe có vẻ hợp lý nhưng không chính xác về mặt thực tế.

Nếu thiếu các cơ chế kiểm soát ngữ nghĩa phù hợp, mô hình có thể nhầm lẫn giữa các môn học có nội dung tương tự, suy diễn sai điều kiện tiên quyết hoặc cung cấp thông tin không tồn tại trong tài liệu chính thức.

Để hạn chế những rủi ro này, hệ thống cần bảo đảm quá trình sinh câu trả lời được neo vào nguồn tri thức có thể kiểm chứng (semantic grounding). Đồng thời, cần có cơ chế kiểm tra tính nhất quán giữa câu hỏi, kết quả truy xuất và nội dung phản hồi trước khi cung cấp thông tin cho người dùng.

Việc kết hợp RAG với HippoRAG được định hướng nhằm tăng cường khả năng truy xuất và liên kết tri thức, qua đó hỗ trợ kiểm soát nội dung được sinh ra. Tuy nhiên, để đạt được độ tin cậy cần thiết, hệ thống vẫn cần được đánh giá thực nghiệm về độ chính xác truy xuất, mức độ trung thực của câu trả lời và khả năng xử lý các truy vấn mơ hồ.

Mục tiêu cuối cùng là xây dựng một hệ thống hỏi đáp học thuật tiếng Việt có khả năng tương tác tự nhiên nhưng vẫn bảo đảm tính chính xác, nhất quán và khả năng truy xuất nguồn gốc của thông tin.
## Thành viên nhóm
- Trương Bình Ba (Truong Binh Ba)
- Lê Nguyễn Thành Tân (Le Nguyen Thanh Tan)
