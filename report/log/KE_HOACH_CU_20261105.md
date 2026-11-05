# Kế hoạch viết báo cáo hệ thống khuyến nghị

Ngày lập: 05/11/2026 (Asia/Saigon). Trạng thái: **đề xuất kế hoạch viết, chưa phải bản báo cáo hoàn chỉnh**.

Quy ước ngôn ngữ theo yêu cầu người dùng: giữ nguyên tên gốc tiếng Anh của thuật toán, mô hình và phương pháp; không tự dịch thành tên tiếng Việt thay thế. Phần diễn giải viết bằng tiếng Việt, có thể giải nghĩa ngắn khi thuật ngữ xuất hiện lần đầu. Dùng nhất quán tên gốc trong tiêu đề, công thức, giả mã, bảng và hình.

Quy ước viết tắt: mục lục và các tiêu đề được đưa vào mục lục dùng tên đầy đủ, không dùng dạng viết tắt, kể cả dạng viết tắt trong ngoặc. Trong thân bài, lần đầu ghi tên đầy đủ kèm dạng viết tắt trong ngoặc; các lần sau mới dùng dạng viết tắt. Danh mục từ viết tắt là công cụ tra cứu bổ sung, không thay việc giới thiệu lần đầu. Với tên chưa xác minh được cách viết đầy đủ, nêu rõ đây là nhãn mã nguồn, không tạo một tên mở rộng để gán cho nó.

Kết quả tra cứu tên mô hình (đính chính 05/11/2026, xem planning/KE_HOACH_THUC_THI.md mục 0): docstring hiện tại ghi **Graph-Regularized Neighborhood Regression (GRNR)** trong src/models/grnr.py và **Diffusion-Filtered History Factorization (DFHF)** trong src/models/dfhf.py. Dùng hai tên này làm tiêu đề và khi giới thiệu lần đầu; tác giả cần xác nhận đây là tên chính thức.

Phạm vi: báo cáo bài tập lớn bằng tiếng Việt cho repository này. Giữ khung trình bày trong [main.tex](main.tex), viết vào năm tệp hiện có trong *section/*, dùng hình từ [../reports/figures](../reports/figures) và số liệu từ [../reports/tables](../reports/tables). Độ dài dự kiến 35–45 trang nội dung, chỉ là ngân sách biên tập khi chưa có giới hạn của học phần.

## 1. Cách kết hợp năm skill

| Skill | Công việc trong kế hoạch | Đầu ra và giới hạn |
|---|---|---|
| scientific-brainstorming | Xây dựng các hướng kể chuyện, câu hỏi nghiên cứu và cách giải thích cạnh tranh | Quyết định bố cục ở mục 3; ý tưởng giải thích chưa được coi là kết quả |
| scientific-critical-thinking | Đối chiếu kết luận với giao thức, độ bất định, thiên lệch và phạm vi dữ liệu | Danh sách vấn đề ở mục 7; dùng tiêu chí phù hợp nghiên cứu ML |
| literature-review | Lập tổng quan theo chủ đề, tìm bài gốc, ghi truy vấn và trạng thái đọc | [Nhật ký tài liệu](planning/LITERATURE_LOG.md); đây là tổng quan có mục tiêu, chưa phải systematic review |
| scientific-writing | Tổ chức năm chương từ bằng chứng, thống nhất ký hiệu, số liệu và nguồn | Đề cương ở mục 4 và [bản đồ bằng chứng](planning/evidence_map.csv) |
| peer-review | Thiết kế vòng đọc phản biện nội bộ và yêu cầu sửa có vị trí, căn cứ, hành động | Checklist ở mục 9; chưa thực hiện phản biện chính thức hay quyết định của hội đồng |

Người dùng đã yêu cầu lập kế hoạch cho project và chỉ định thư mục nguồn. Chưa có venue hoặc chính sách AI của học phần trong tài liệu đã đọc. Vì vậy, bước này khảo sát tài nguyên dự án và lập kế hoạch; không tuyên bố đã hoàn tất intake phản biện, thẩm định độc lập hay xác minh của tác giả. Trước phản biện chính thức hoặc nộp bài, hoàn thành các thông tin chính sách còn thiếu. Không tự áp dụng GRADE, RoB hay checklist thử nghiệm lâm sàng cho benchmark khuyến nghị.

## 2. Hiện trạng và thứ tự tin cậy của nguồn

### 2.1. Tài nguyên đã kiểm kê

| Tài nguyên | Hiện trạng quan sát được | Việc cần làm khi viết |
|---|---|---|
| main.tex | Có bìa, bìa lót, mục lục, danh mục hình/bảng và lời gọi năm phần | Giữ thiết kế, thay thông tin còn thuộc đề tài cũ |
| section1.tex … section5.tex; ref.tex; guided.tex | Cả bảy tệp đang trống | Viết năm chương và tài liệu tham khảo; guided.tex chưa được main.tex nạp |
| Bìa, header/footer, bảng phân công | Còn tên môn Thuật toán ứng dụng, đề tài kho hàng, thuật toán LNS/ALNS và thông tin nhóm | Xác nhận học phần, GVHD, tác giả và đóng góp; không suy diễn từ mẫu cũ |
| reports/figures | 39 PNG; đã xem trực tiếp H1_density_ndcg20 và H5_user_groups_ndcg20 | Chọn hình theo câu hỏi, không đưa toàn bộ vào thân bài |
| reports/tables | 14 CSV, gồm B1–B6 và các biến thể | Chuyển thành bảng LaTeX có nguồn và nhãn; giữ CSV làm nguồn |
| results | Có metrics.json của 7 mô hình × 4 tỉ lệ, đều seed 42 | Khóa nguồn theo run, checkpoint, bundle và mã nguồn |
| reports/report_manifest.json | Ghi validation, 20 run của nhóm chính; còn đường dẫn máy cũ D:/advanced-machine | Bổ sung provenance cho nhóm EASE/GF-CF; đường dẫn cũ chưa đủ kết luận sai số liệu |
| README | Có tóm tắt và hạn chế hữu ích | Dùng để định hướng; đối chiếu lại với artifact trước khi đưa vào báo cáo |

Ưu tiên nguồn theo loại phát biểu: kết quả lấy từ metrics/prediction của run đã khóa; phương pháp thực thi lấy từ snapshot mã nguồn và cấu hình của chính run; nguồn hiện tại giúp đọc và kiểm tra khác biệt; bảng/hình là sản phẩm dẫn xuất. Nếu mâu thuẫn, ghi vào danh sách cần giải quyết thay vì chọn con số thuận tiện.

### 2.2. Số liệu mốc đã tìm thấy, chưa chạy tái đánh giá

- B1: 124.895 người dùng; catalog 44.843 sản phẩm; 858.192 tương tác train; 107.274 tương tác validation.
- Plan của GRNR d100: 44.803 candidate item có trong train; 107.215 người dùng warm được đánh giá; 59 mục tiêu cold bị loại. Không viết rằng tất cả 44.843 sản phẩm đều là candidate hợp lệ.
- Audit có sẵn ghi timestamp ở độ phân giải ngày; 45.431 người dùng có timestamp trùng qua train–validation. Dữ liệu có thứ tự thời gian không giảm, không bảo đảm thứ tự nghiêm ngặt trong ngày.
- B2b: NDCG@20 ở d100 của GRNR = 0,03829; DFHF = 0,03519. DFHF đạt giá trị cao nhất trong các cấu hình được báo cáo ở d25 và d50 khi đối chiếu thêm B5.
- B6 ở d100: GRNR − EASE đầy đủ = +0,00033; CI95% = [−0,00007; +0,00073]; p một phía sau Holm = 0,05079. Chưa đủ bằng chứng cho ưu thế theo phép so sánh này; không kết luận tương đương.
- Cả bốn cặp H1_density/H2 theo NDCG@10/20 và Recall@10/20 đều có SHA-256 trùng theo từng cặp. Bộ 39 PNG có 35 nội dung phân biệt theo hash; chỉ giữ H1 trong thân bài.

Các mốc trên là **bằng chứng đã định vị trong tệp**, không phải kết quả mới được tái lập trong phiên lập kế hoạch. Sổ bằng chứng để trạng thái cần tác giả xác nhận; không gán tên người xác minh khi chưa có.

## 3. Trục lập luận và câu hỏi nghiên cứu

### 3.1. Các hướng đã cân nhắc

Tiêu chí lựa chọn: bám câu hỏi học máy, truy nguyên được đến artifact, phân biệt được đóng góp với nền tảng cũ, thể hiện cả kết quả bất lợi và vừa sức viết từ nguồn hiện có. Không chấm điểm số giả định.

| ID | Ý tưởng do AI hỗ trợ đề xuất | Bằng chứng thuận/nghịch | Quyết định biên tập |
|---|---|---|---|
| I01 | Kể câu chuyện một mô hình thắng ở mọi điều kiện | GRNR giảm mạnh ở d25/d50 và không hơn EASE đầy đủ rõ ràng ở d100 | Loại; không phù hợp số liệu |
| I02 | Đánh giá hai cách biểu diễn người dùng từ lịch sử: hồi quy cục bộ và phân rã có khuếch tán | Có hai model, cấu hình, bốn mức giữ tương tác và bảng chi phí | Chọn làm trục chính |
| I03 | Xem đây là hệ khuyến nghị đa phương thức | Pipeline có metadata/text embedding nhưng chưa có bằng chứng hai mô hình khóa dùng chúng để xếp hạng | Không dùng làm đóng góp; metadata có thể phục vụ demo |
| I04 | Tập trung vào hệ thống demo và giải thích gợi ý | Có app và checkpoint; chưa có nghiên cứu người dùng | Dùng làm phần triển khai, không thay benchmark |

Tên đề tài đề xuất: **“Hai mô hình khuyến nghị dựa trên lịch sử tương tác và đánh giá trên Amazon Electronics”**.

Luận điểm dự kiến: hai cách mô hình hóa có đánh đổi khác nhau về chất lượng xếp hạng, độ bền khi giảm tương tác và chi phí tính toán. Đây là kết luận giới hạn trong cấu hình và giao thức được đánh giá, chưa phải tuyên bố mới nhất hoặc tốt nhất toàn lĩnh vực.

### 3.2. Câu hỏi dẫn dắt

| ID | Câu hỏi | Bằng chứng cần trình bày |
|---|---|---|
| RQ1 | GRNR/DFHF đạt chất lượng xếp hạng thế nào so với các cấu hình LightGCN, XSimGCL, DirectAU, EASE và GF-CF? | B2a, B2b, B3, B5, B6; tách nhóm so sánh chính/bổ sung |
| RQ2 | Chất lượng thay đổi ra sao khi giữ 100%, 75%, 50%, 25% tương tác train? | H1, H4, H5; nêu thuật toán lấy mẫu bảo toàn coverage |
| RQ3 | Chất lượng đánh đổi thế nào với thời gian fit, suy luận và dung lượng lưu? | H7a, H7b, H7c và metadata môi trường từng run |
| RQ4 | Hệ thống phục vụ lịch sử mới và giải thích gợi ý như thế nào? | Mã app, mô tả luồng suy luận, ví dụ minh họa có nguồn; chưa là đánh giá cold-start |

Vì kết quả đã có trước kế hoạch này, các câu hỏi và diễn giải bổ sung mang tính hồi cứu/khám phá. Không gọi chúng là giả thuyết đăng ký trước. Giải thích “DFHF bền hơn do khuếch tán” hoặc “GF-CF yếu do chuẩn hóa” chỉ là giả thuyết cơ chế cho đến khi có ablation hoặc phân tích phân biệt.

## 4. Đề cương năm chương gắn với tệp hiện có

### Mục lục đề xuất sau rà soát cấu trúc

Đây là cấu trúc làm việc để triển khai báo cáo. Chia mục theo câu hỏi và khối lập luận, không ấn định số mục bằng nhau cho mọi chương. Một mục riêng cần có nội dung đủ để giải thích hoặc đánh giá một vấn đề; ý ngắn viết thành đoạn trong mục liên quan. Mục lục tổng thể hiển thị chương và mục chính; sáu mục con trong hai thuật toán giúp tổ chức phần toán dài và có thể hiển thị ở cấp sâu hơn nếu bản thảo thực tế cần.

| Chương | Các mục chính |
|---|---|
| 1. Giới thiệu | 1.1. Đặt vấn đề; 1.2. Mục tiêu và phạm vi nghiên cứu; 1.3. Đóng góp của dự án |
| 2. Cơ sở lý thuyết và nghiên cứu liên quan | 2.1. Khuyến nghị từ phản hồi ngầm; 2.2. Mô hình dựa trên quan hệ sản phẩm và lịch sử tương tác; 2.3. Mô hình đồ thị và học biểu diễn; 2.4. Tổng hợp và định hướng đề xuất |
| 3. Phương pháp và thuật toán đề xuất | 3.1. Mô hình bài toán và định hướng thiết kế; 3.2. Graph-Regularized Neighborhood Regression; 3.3. Diffusion-Filtered History Factorization; 3.4. Phân tích tính chất và chi phí tính toán |
| 4. Thực nghiệm và phân tích kết quả | 4.1. Dữ liệu và tiền xử lý; 4.2. Thiết lập và giao thức đánh giá; 4.3. So sánh chất lượng xếp hạng; 4.4. Ảnh hưởng của mức độ thưa và nhóm người dùng; 4.5. Quá trình huấn luyện và chi phí tính toán; 4.6. Thảo luận và hạn chế |
| 5. Kết luận và hướng phát triển | 5.1. Kết luận; 5.2. Hướng phát triển |

Trong mỗi mục GRNR/DFHF, tách ba khối: biểu diễn, hàm mục tiêu/cách học, thuật toán/suy luận. Động lực thiết kế nằm cùng thành phần cần giải thích; độ phức tạp và tính chất được tổng hợp ở 3.4. Kết quả có các mục riêng theo câu hỏi đánh giá, không chia riêng cho từng metric hoặc từng hình. Hạn chế được phân tích ở 4.6; Chương 5 chỉ tổng kết ngắn. Demo nằm ở phụ lục, có dẫn chiếu từ nội dung chính khi trả lời RQ4.

### Chương 1 — Giới thiệu: section/section1.tex, khoảng 3–4 trang

**1.1. Đặt vấn đề.** Giới thiệu bối cảnh khuyến nghị top-N từ phản hồi ngầm, khó khăn khi tương tác thưa và nhiệm vụ xếp hạng sản phẩm chưa thấy từ lịch sử.

**1.2. Mục tiêu và phạm vi nghiên cứu.** Nêu RQ1–RQ4, phân biệt chất lượng offline với giá trị kinh doanh; xác định phạm vi Amazon Electronics, đánh giá warm trên validation và một seed.

**1.3. Đóng góp của dự án.** Giới thiệu hai cách mô hình hóa, pipeline đánh giá, demo và khả năng truy nguyên kết quả. Kết thúc chương bằng một đoạn ngắn giới thiệu cấu trúc báo cáo.

Nguồn: E01, E02, E03, E04, E05; tài liệu nền L01–L07 trong nhật ký. Viết chương này sau khi chốt phương pháp và kết quả; không lấy tính mới từ tên mô hình.

### Chương 2 — Cơ sở lý thuyết và nghiên cứu liên quan: section/section2.tex, khoảng 7–9 trang

**2.1. Khuyến nghị từ phản hồi ngầm.** Trình bày ma trận tương tác, lịch sử user, sản phẩm chưa quan sát, hàm tính điểm và top-K. Đánh giá tích cực là proxy sở thích, không đồng nhất với giao dịch mua được xác nhận. Phát biểu nhiệm vụ ở mức khái niệm; định nghĩa toán cụ thể của hai thuật toán ở 3.1.

**2.2. Mô hình dựa trên quan hệ sản phẩm và lịch sử tương tác.** Giải thích láng giềng, ridge/regularization, phân rã và tổng hợp lịch sử bằng embedding; lồng ghép EASE và FISM để làm nền cho GRNR/DFHF. Nêu công thức lõi, cách dùng và điểm liên quan đến project; không diễn giải toàn bộ kiến trúc mỗi baseline.

**2.3. Mô hình đồ thị và học biểu diễn.** Giải thích chuẩn hóa, truyền lan/lọc đồ thị và các mục tiêu học liên quan qua LightGCN, GF-CF, XSimGCL và DirectAU. Phân biệt encoder với objective; chọn kiến thức được dùng để hiểu thiết kế hoặc phép so sánh ở chương sau.

**2.4. Tổng hợp và định hướng đề xuất.** Dùng bảng so sánh để chỉ ra thành phần kế thừa, khác biệt cần khảo sát và lý do xem xét hai hướng thiết kế. Không khẳng định khoảng trống/tính mới khi tìm kiếm tài liệu còn chưa đầy đủ. Nguyên tắc đánh giá được dẫn khi bàn giới hạn của paper; chỉ số và giao thức project trình bày tập trung ở 4.2.

Mỗi nhóm trình bày: nguyên lý → liên hệ với project → điểm khác biệt → giới hạn. Bảng so sánh cần các cột: biểu diễn user, tham số học, objective, cần optimizer, đầu vào suy luận, chi phí bộ nhớ và nguồn. Không coi khả năng xử lý lịch sử mới là giải quyết cold-item hoặc người dùng không có lịch sử.

Tài liệu bắt buộc đọc trước khi nhận định tính mới: EASE, FISM, LightGCN, XSimGCL, DirectAU, GF-CF và nguồn dataset. Các record đã mở mới xác nhận metadata/abstract, chưa đủ để dẫn mọi công thức. Phải mở full text, ghi trang/phương trình và người xác minh.

### Chương 3 — Phương pháp và thuật toán đề xuất: section/section3.tex, khoảng 10–13 trang

**3.1. Mô hình bài toán và định hướng thiết kế.** Thống nhất X, số user/item, H_u, d, K, tập candidate và ma trận đồ thị. Phân biệt tỉ lệ giữ tương tác d với density tuyệt đối |E|/(|U||I|). Phân biệt đầu vào huấn luyện đã giảm với mask từ train gốc. Giải thích ngắn hai hướng thiết kế và các vấn đề chúng hướng đến.

**3.2. Graph-Regularized Neighborhood Regression.** Đối chiếu E03 và snapshot của run:

**3.2.1. Biểu diễn lịch sử và lựa chọn láng giềng.** Trình bày tối đa 128 láng giềng theo excess co-occurrence, điều kiện lift dương, quy tắc hòa và vector lịch sử chuẩn hóa. Giải thích cách loại target trong các hàng positive khi fit.

**3.2.2. Hàm mục tiêu và phương pháp giải.** Trình bày weighted ridge có bias/prior, regularization theo support, năng lượng đồ thị và boundary; suy ra normal equation và cách giải bằng Cholesky. Điều kiện khả nghịch và sai số dư cần được kiểm chứng.

**3.2.3. Thuật toán huấn luyện và suy luận.** Cung cấp giả mã fit/score, fallback và phân rã đóng góp. Tách popularity tilt khi xếp hạng khỏi objective khi fit. Giải thích đóng góp là đại số, chưa phải quan hệ nhân quả.

**3.3. Diffusion-Filtered History Factorization.** Đối chiếu E04 và snapshot:

**3.3.1. Biểu diễn lịch sử và khuếch tán trên đồ thị.** Trình bày hai bảng embedding nguồn/đích không buộc bằng nhau, không học embedding riêng cho user; toán tử T = D_I^−1 X^T D_U^−1 X, bộ lọc 0,5I + 0,25T + 0,25T² và tổng hợp lịch sử chuẩn hóa.

**3.3.2. Hàm mục tiêu và phương pháp tối ưu.** Trình bày context leave-one-out, full softmax sau mask, regularization, bias, chiếu bán kính và xử lý lịch sử đơn theo cấu hình khóa.

**3.3.3. Thuật toán huấn luyện và suy luận.** Giả mã Adam, huấn luyện đủ 200 epoch và lưu checkpoint tốt nhất theo validation NDCG@20. Phân biệt context bỏ positive khi train với retained history đầy đủ khi suy luận; không mô tả như đã dừng sớm.

**3.4. Phân tích tính chất và chi phí tính toán.** Tổng hợp điều kiện áp dụng, tính chất toán có thể chứng minh và thời gian/bộ nhớ theo các bước của hai thuật toán. So sánh tham số, nhu cầu tối ưu và đầu vào khi phục vụ. Tách suy diễn lý thuyết với kỳ vọng hiệu năng; số đo thực tế trình bày ở 4.5.

Ghi chú triển khai cho phụ lục: mô tả offline fit → checkpoint → app/recommender → top-K; ba tab demo và giới hạn của từng nhánh. Chỉ thêm sơ đồ pipeline hoặc ảnh demo khi giúp người đọc hiểu, ghi rõ là tài nguyên cần tạo ở giai đoạn viết.

Đưa phép biến đổi dài, bảng siêu tham số đầy đủ và kiểm chứng toán vào phụ lục nếu cần. Các script trong scripts/verify là nguồn kiểm tra dự kiến; sự tồn tại của script chưa chứng minh chúng đã chạy thành công.

### Chương 4 — Thực nghiệm và phân tích kết quả: section/section4.tex, khoảng 12–15 trang

**4.1. Dữ liệu và tiền xử lý.** Trình bày nguồn và phiên bản, quy trình lọc, thống kê sau xử lý, chia tập và tạo các mức giảm tương tác:

- Dữ liệu và tiền xử lý: nêu đúng phiên bản Electronics từ URL cấu hình; không lẫn Amazon 2018/2023. Mô tả rating ≥ 4, khử trùng user–item, K-core và thống kê sau xử lý. B1 bổ sung số warm user, candidate và mục tiêu bị loại từ E02.
- Chia tập: tỉ lệ toàn cục 80/10/10; tập con user được chọn có hai tương tác cuối làm val/test. Không phải mỗi user đều chia 80/10/10 hoặc dùng global time cutoff. Giải thích tie-break và timestamp đồng ngày.
- Giảm tương tác: chỉ tác động train, giữ coverage user/item; báo cáo số thực giữ vì có coverage floor.

**4.2. Thiết lập và giao thức đánh giá.** Trình bày cấu hình baseline/đề xuất, môi trường, metric, candidate/mask, chọn checkpoint và quy trình thống kê. Dùng bảng cho các tham số dài:

- Đánh giá: candidate có support trong retained train; mask train gốc; cùng cohort giữa model. Nêu cách dùng NDCG@10/20, Recall@10/20, MRR và NDCG@20 để chọn checkpoint/cấu hình. Tách selection/confirmation chỉ khi có artifact và nhật ký chứng minh.
- Baseline và môi trường: ghi profile DirectAU dùng encoder LightGCN, phân biệt EASE đầy đủ/top-128, kiểm tra config từng run, phần cứng và phạm vi timing.
- Thống kê: mô tả bootstrap ghép cặp theo user, 10.000 lần, một phía; Holm trên sáu so sánh NDCG@20 ở d100 cho B3, family NDCG@10 riêng cho B3b, ba so sánh mỗi d cho B6. Nhóm B6 được lập sau khi xem kết quả. CI95% chưa hiệu chỉnh đồng thời; CI hai phía và p một phía không có cùng quy tắc quyết định.

**4.3. So sánh chất lượng xếp hạng.** Đối chiếu B2a_d100 và H1 với các baseline neural, tiếp theo B5/B6 cho nhóm closed-form. Trình bày delta/CI/p đúng family cùng kết quả tương ứng; không tạo thêm một mục chỉ để liệt kê p-value. Giữ kết quả bất lợi và phân biệt EASE đầy đủ/top-128.

**4.4. Ảnh hưởng của mức độ thưa và nhóm người dùng.** Phân tích B2b, H1 theo các mức giữ tương tác, H4 và H5. Điểm retention tương đối đi cùng điểm tuyệt đối; nhóm H5 dùng lịch sử train gốc. D25/d50 không phải cold-start benchmark. Không chia thêm một mục riêng cho từng chỉ số hoặc từng tỉ lệ.

**4.5. Quá trình huấn luyện và chi phí tính toán.** H3/B4 cho best-vs-last; loss chỉ đọc trong từng objective. H7 cho thời gian fit, latency và dung lượng; đối chiếu phân tích ở 3.4. Latency là trung bình theo user trong batch, chưa là p95 dịch vụ; tách dung lượng file nén, dense lý thuyết và peak RAM.

**4.6. Thảo luận và hạn chế.** Tổng hợp câu trả lời RQ và liên hệ động lực ở Chương 3, tập trung giải thích cạnh tranh và giới hạn thay vì lặp số liệu. H6 có thể hỗ trợ thảo luận mô tả về popularity/coverage; chưa chứng minh công bằng, hài lòng hay doanh thu. Nếu chưa có ablation, diễn giải cơ chế là giả thuyết. Phân tích một dataset/seed, lựa chọn trên validation, temporal ties, tuning baseline và khác biệt phần cứng.

### Chương 5 — Kết luận và hướng phát triển: section/section5.tex, khoảng 2–3 trang

**5.1. Kết luận.** Trả lời RQ1–RQ4 ngắn gọn, khớp với phạm vi Chương 1 và bằng chứng Chương 4; nhắc giới hạn quan trọng trong một đoạn thay vì lặp phần thảo luận.

**5.2. Hướng phát triển.** Ưu tiên: xác minh provenance → kết quả confirmation độc lập nếu hợp lệ → nhiều seed → tuning công bằng/ablation → dataset bổ sung và đánh giá lịch sử mới có thiết kế riêng.

Không bổ sung số liệu hoặc claim mới ở kết luận. Viết tóm tắt/abstract sau cùng, khoảng 150–250 từ nếu quy định học phần cho phép.

## 5. Kế hoạch hình và bảng

Bản kiểm kê đầy đủ, hash và nơi dùng dự kiến nằm trong [figure_inventory.csv](planning/figure_inventory.csv). Không thay tên hay chuyển ảnh sang report/image; thư mục này hiện chứa logo.

| Vị trí | Tài nguyên ưu tiên trong reports | Mục đích và lưu ý caption |
|---|---|---|
| 4.1 | B1_dataset.csv | Bảng dữ liệu; thêm warm/candidate từ plan, không trộn mẫu số |
| 4.3–4.4 | B2a_metrics_d100.csv; H1_density_ndcg20.png; H1_density_recall20.png | So sánh chính và bốn tỉ lệ; validation, seed 42 |
| 4.3–4.4 | B5_closed_form.csv; H1_closed_form_density_ndcg20.png | GRNR/EASE đầy đủ/EASE top-128/GF-CF; nhãn biến thể rõ |
| 4.4 | B2b_by_density.csv; H4_retention_ndcg20.png | Giữ chất lượng tương đối so với d100 của chính model |
| 4.4 | H5_user_groups_ndcg20.png | Nhóm theo lịch sử train gốc; giữ n của từng nhóm |
| 4.5 | B4_training_d100.csv; H3_learning_curves_ndcg20.png | Best-vs-last, đủ 200 epoch; marker chọn checkpoint nếu cần |
| 4.5 | H7a_train_time.png; H7b_inference_latency.png | Đánh đổi fit/suy luận; không suy tốc độ thuật toán từ máy khác nhau |
| 4.5 | H7c_closed_form_checkpoint_size.png | EASE đầy đủ là kích thước dense float32 ước tính; đơn vị thực dùng MiB |
| 4.3–4.4 | B3_significance_ndcg20.csv; B6_closed_form_significance.csv | Delta, CI, p, family và n; không dùng dấu sao thay số liệu |
| 4.6 | H6a_popularity_trajectory.png; H6b_coverage.png | Tùy dung lượng; mô tả thay đổi popularity/coverage và thảo luận |
| Phụ lục | NDCG@10, Recall@10, H8, H3c và các biến thể closed-form còn lại | Bổ sung kiểm tra; không lặp cùng thông điệp quá nhiều |
| Không đưa lặp | Bốn H2 cùng metric với H1 | Đã kiểm tra hash cả bốn cặp và xác nhận trùng byte |

Mỗi caption phải đủ: model/biến thể, validation, seed, d, metric/đơn vị, cohort hoặc định nghĩa nhóm, ý nghĩa error bar nếu có, file nguồn và script sinh. Hình không có uncertainty thì không tự mô tả là mean ± CI. Thân bài dẫn hình trước và giải thích quan sát sau; bảng phải là văn bản LaTeX thay vì ảnh chụp CSV.

Đã xem trực tiếp hai hình, chưa kiểm tra thị giác toàn bộ 39 hình. Bước xuất bản phải xem mọi hình được chọn ở khổ in thực tế, đặc biệt H5 nhiều panel.

## 6. Kế hoạch tổng quan tài liệu và quản lý nguồn

Nhật ký ở [LITERATURE_LOG.md](planning/LITERATURE_LOG.md) ghi nguồn đã mở, giới hạn tìm kiếm và truy vấn cần chạy tiếp. Chọn tổng quan theo chủ đề phù hợp bài tập lớn; không tự tạo số PRISMA hay tuyên bố tìm kiếm đầy đủ.

1. Hoàn thiện bộ bài gốc của năm baseline và nguồn dataset.
2. Đọc FISM và các phương pháp lịch sử liên quan để đánh giá mức mới của DFHF; phân biệt thành phần kế thừa và lựa chọn thiết kế của project.
3. Tìm phương pháp item–item có regularization đồ thị/local ridge để định vị GRNR; không suy rằng ghép các thành phần tạo ra một nguyên lý mới.
4. Bổ sung nguồn về đánh giá offline, temporal split và thiên lệch; truy vấn có ghi ngày, database, số record và lý do chọn.
5. Lập bảng trích xuất: ID, DOI/arXiv, phiên bản, model/objective, protocol, bằng chứng hỗ trợ/chống, vị trí full text, điểm liên quan, hạn chế, người xác minh và ngày.
6. Viết theo nhóm phương pháp; không so trực tiếp điểm từ paper gốc với điểm của project nếu khác dataset/split/candidate.

Hiện ref.tex trống. Giai đoạn viết có thể dùng môi trường thebibliography trong tệp này để giữ cấu trúc hiện có; dùng khóa ổn định như lightgcn2020, ease2019. Nếu chuyển sang BibTeX, thực hiện thống nhất cả main.tex và pipeline build. Không trộn hai danh mục hoặc chép metadata chưa kiểm chứng.

Nguồn phương pháp hỗ trợ đã được mở: Timothy Kassis, Vinayak Agarwal, Yuhuan He, Darshil Patel, Aubrey M. Brueckner (2026), [Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents](https://arxiv.org/abs/2609.00065), DOI [10.48550/arXiv.2609.00065](https://doi.org/10.48550/arXiv.2609.00065). Record hiện hiển thị bản sửa ngày 02/09/2026; không gắn hậu tố phiên bản vào DOI. Đã ghi nguồn này trong kế hoạch/nhật ký vì năm skill đóng góp vào quy trình; chưa thay ref.tex của báo cáo.

## 7. Các điểm cần giải quyết trước khi viết kết luận mạnh

| Mức | Vị trí/quan sát và hệ quả | Hành động cụ thể, tương xứng |
|---|---|---|
| P0 | main.tex còn chủ đề và phân công kho hàng; chưa có xác nhận thông tin tác giả | Sửa bìa/header/footer/PDF metadata sau khi chốt thông tin; xóa macro số liệu kho không còn dùng |
| P0 | Catalog 44.843 khác candidate 44.803; validation raw khác warm 107.215 | Viết đầy đủ bộ lọc cohort/candidate và mẫu số; tránh mô tả full ranking không kèm điều kiện |
| P0 | Audit ghi 45.431 tie train–val; không có thứ tự chính xác trong ngày | Nêu chronology không giảm và quy tắc hòa; không khẳng định dự đoán tương lai nghiêm ngặt |
| P0 | Chọn checkpoint/cấu hình trên validation; B3 xuất toàn cohort | Gọi kết quả là validation có lựa chọn; kiểm tra nhật ký trước khi gọi confirmation độc lập |
| P0 | EASE p > 0,05 không chứng minh tương đương | Viết “chưa đủ bằng chứng GRNR hơn EASE theo phép so sánh”; giữ delta và CI |
| P0 | Một seed; bootstrap chỉ resample người dùng trên model cố định | Nêu giới hạn bất định; không gọi CI là độ ổn định giữa lần train |
| P1 | EASE/GF-CF dùng cấu hình cố định; tuning budget không cân bằng | Công bố cấu hình/ngân sách, giới hạn claim ở các cấu hình đã chạy; tuning bổ sung là nhánh mở rộng |
| P1 | Chi phí CPU/GPU, batch và phép đo khác nhau | Bảng phần cứng/phạm vi timing; không kết luận nhanh hơn về bản chất hoặc latency production |
| P1 | Kích thước EASE đầy đủ 7.671 “MB” do code chia 2²⁰, không là file đã lưu | Đổi nhãn dẫn xuất sang MiB; phân biệt memory dense lý thuyết, disk compressed và peak RAM |
| P1 | Chưa có ablation chứng minh từng thành phần hữu ích | Mô tả thành phần như thiết kế; đưa nguyên nhân giả định và ablation vào hướng phát triển |
| P1 | Existing audit/manifest không chứng minh test chưa từng được xem | Có thể chạy audit_test_exposure để kiểm kê mà không đọc nhãn; không gọi holdout “untouched” khi chưa có provenance |
| P1 | reports manifest còn đường dẫn cũ, thiếu run bổ sung | Ghi ledger dùng path tương đối/hash, bundle ID và provenance EASE đầy đủ/top-128 |
| P2 | H1/H2 lặp; H5 nhiều nhãn nhỏ | Loại trùng, xem bản in ở textwidth 15,5 cm; không ép ghép hai hình rộng thành nhãn khó đọc |

## 8. Lộ trình thực hiện và điều kiện hoàn thành từng bước

Đây là ước lượng công việc, không phải deadline đã được người dùng cam kết. Bước mở rộng thí nghiệm không nằm trên đường bắt buộc để viết trung thực từ dữ liệu hiện có.

| Bước | Công việc và sản phẩm | Phụ thuộc | Tiêu chí xong |
|---|---|---|---|
| W0 — Chốt yêu cầu | Tên môn/lớp, GVHD, tác giả, vai trò, giới hạn trang, hạn nộp, quy định AI | Thông tin học phần | Không tái dùng danh tính/đóng góp từ mẫu khi chưa xác nhận |
| W1 — Khóa bằng chứng | Ledger run, hash nguồn, đối chiếu model/config/cohort; hoàn thiện evidence_map | Hiện có thể bắt đầu | Mọi bảng chính có nguồn; mọi mâu thuẫn được ghi hoặc xử lý |
| W2 — Đọc tài liệu | Full text, bảng trích xuất, khóa citation | Song song công việc độc lập với W1; không yêu cầu thêm agent | Claim lý thuyết có locator; phạm vi novelty được giới hạn |
| W3 — Viết phương pháp | Chương 3, ký hiệu, pseudocode, bảng tham số | W1 + nguồn lý thuyết cần thiết | Công thức khớp phiên bản chạy; train/inference/mask được phân biệt |
| W4 — Viết thực nghiệm | Chương 4, bảng LaTeX và chọn hình | W1, W3 | Kết quả gồm cả trường hợp bất lợi; protocol/mẫu số/uncertainty rõ |
| W5 — Hoàn thiện câu chuyện | Chương 2 → Chương 1 → Chương 5 → abstract | W2–W4 | RQ/đóng góp/kết luận khớp; không thêm fact ngoài ledger |
| W6 — Dàn trang | Cập nhật main.tex, bìa, hình, ref.tex và phụ lục nếu cần | W0, W3–W5 | Build được; metadata/chủ đề cũ được loại khỏi bản nộp |
| W7 — Rà soát | Checklist mục 9; sửa theo issue có vị trí | W6 | Không còn lỗi khoa học quan trọng hoặc giới hạn bị che |
| W8 — Kiểm bản PDF | Build và xem toàn trang; tác giả xác nhận nội dung cuối | W7 | Hình/bảng/citation rõ, không thiếu nguồn hay placeholder |

Ngân sách tham khảo: W0–W2 khoảng 1–2 buổi; W3–W5 khoảng 3–5 buổi; W6–W8 khoảng 1–2 buổi. Cần điều chỉnh theo số nguồn chưa đọc và yêu cầu môn học.

Nhánh nâng độ mạnh bằng chứng nếu có tài nguyên: nhiều seed cho model stochastic và lấy mẫu thưa; ablation thành phần GRNR/DFHF; tuning baseline với ngân sách chung; thêm dataset; đánh giá lịch sử user mới; kết quả xác nhận trên tập chưa tham gia quyết định khi tính độc lập được bảo đảm. Nếu không thực hiện, thu hẹp kết luận thay vì bịa hoặc suy ra kết quả.

## 9. Vòng rà soát nội bộ theo peer-review

Sử dụng cho bản thảo làm việc, chưa phải phản biện tạp chí. Trước một quy trình phản biện chính thức, hoàn thành intake của peer-review về ủy quyền, chính sách venue/AI, xung đột lợi ích, người chịu trách nhiệm và lưu giữ dữ liệu. Không khai READY chỉ để vượt validator.

Mỗi issue có: ID → vị trí → quan sát → evidence ID/tiêu chí → ảnh hưởng đến claim → hành động yêu cầu → mức ưu tiên → trạng thái sửa. Tách “không thấy báo cáo” với “đã chứng minh không thực hiện”.

Nếu có người đọc thứ hai, giao phần phương pháp/kết quả cho người không trực tiếp soạn phần đó, ghi rõ vai trò và giới hạn. Việc tự rà soát của người viết hoặc AI hỗ trợ không được gọi là phản biện độc lập.

- [ ] Mỗi RQ có kết quả tương ứng; tiêu đề và abstract không mạnh hơn bằng chứng.
- [ ] Mọi con số truy về run/table; tỷ lệ, mẫu số, metric, d, seed và split thống nhất.
- [ ] Công thức đúng phiên bản model; không đưa nhánh kernel/option DFHF đã bỏ vào mô hình khóa.
- [ ] Kiểm chứng đại số không bị gọi là bằng chứng về ưu thế thực nghiệm.
- [ ] Tất cả baseline/biến thể được đặt tên rõ; không gộp EASE đầy đủ với top-128.
- [ ] Mô tả sampling, temporal ties, coverage/cold exclusion, train mask và candidate chính xác.
- [ ] P-value/CI/family đúng chiều và phạm vi; không suy tương đương từ không có ý nghĩa.
- [ ] Thảo luận một seed, một dataset, lựa chọn trên validation và tuning không cân bằng.
- [ ] Không gọi giải thích đại số là causal explanation; không suy hài lòng từ coverage.
- [ ] Citation hỗ trợ đúng mệnh đề; metadata và locator được tác giả xác nhận.
- [ ] Các hình dùng màu lẫn ký hiệu/hatch; nhãn đọc được ở khổ in; nguồn bảng rõ.
- [ ] Thông tin tác giả/đóng góp/chính sách AI là thông tin thực, được người có trách nhiệm xác nhận.

## 10. Tích hợp LaTeX và kiểm tra kỹ thuật dự kiến

Đường dẫn hình tính từ thư mục report khi build main.tex. Có thể thêm vào preamble:

~~~tex
\graphicspath{{../reports/figures/}{image/}}
~~~

Ví dụ dùng hình có sẵn, caption còn phải hoàn thiện theo ledger:

~~~tex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{H1_density_ndcg20.png}
  \caption{NDCG@20 trên validation theo tỉ lệ tương tác train được giữ lại.
  Mỗi cấu hình dùng seed 42; đánh giá trên nhóm người dùng warm.}
  \label{fig:ranking-density-ndcg20}
\end{figure}
~~~

Nhãn ổn định theo nội dung, không đặt tên kiểu fig:hinh1. Giữ ký hiệu d/K nhất quán; dùng section/subsection với class article hiện có, không dùng lệnh chapter chưa được hỗ trợ. Phụ lục có thể thêm tệp riêng và lời gọi sau năm phần nếu cần.

Lệnh kiểm tra dành cho giai đoạn thực thi, **chưa chạy trong bước lập kế hoạch**:

~~~powershell
# Từ thư mục gốc; kiểm tra điều kiện artifact/môi trường trước khi chạy.
python scripts/verify_results.py --output report/planning/validation_recheck.json --device cpu
# Script trên chỉ kiểm tra 5 model chính ở d100, không phải cả 28 run hoặc EASE đầy đủ.
python scripts/audit_test_exposure.py --output-dir report/planning/test_exposure

# Từ thư mục report.
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
~~~

Đã tìm thấy xelatex và latexmk trên máy; chưa xác minh package/font đầy đủ và chưa build lại PDF. Kiểm tra cảnh báo undefined reference/citation, nhãn trùng, overfull box, font tiếng Việt, bảng dài, công thức và vị trí float. Sau build phải xem toàn bộ PDF thực tế; không coi exit code 0 là đủ.

Nếu cần sinh lại hình/bảng, lưu ý scripts/make_report.py xóa toàn bộ PNG/PDF trong output figures và CSV/TEX trong output tables trước khi dựng lại. Ưu tiên output nháp riêng qua --output; script closed-form hiện ghi cố định vào reports và phải chạy sau main report nếu tái sinh tại đó. Không đặt hình vẽ tay hoặc bảng LaTeX biên tập vào thư mục dẫn xuất dễ bị xóa.

## 11. Những điểm còn để mở

Tên học phần chính xác, lớp/mã học phần, GVHD, tác giả và đóng góp; giới hạn trang và deadline; quy định trích dẫn/AI của học phần; tài liệu full text và locator cho novelty; nhật ký chọn cấu hình/confirmation; provenance đủ để nói về độ độc lập của test; kết quả tái đánh giá từ checkpoint.

Những mục này không ngăn lập đề cương và viết phần có bằng chứng. Chúng phải được xác nhận trước khi điền thông tin hành chính hoặc đưa ra kết luận phụ thuộc vào chúng.
