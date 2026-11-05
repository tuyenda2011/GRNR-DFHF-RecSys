# Nhật ký công việc báo cáo

Phiên làm việc ngày 05/11/2026. Nhật ký ghi theo thứ tự thời gian: đã làm gì, vì sao, và kết quả nằm ở đâu. Muốn biết việc tiếp theo, đọc [../planning/README.md](../planning/README.md).

Ký hiệu đường dẫn: `report/...` là bên trong thư mục được bàn giao; `repo/...` là thư mục gốc của repository, không nằm trong gói bàn giao.

---

## 1. Đổi tên hai mô hình trong hình và bảng

- **Bối cảnh.** Hai mô hình đề xuất trước đây tên là SGKR và SPHR, nay đổi thành GRNR và DFHF. Mã nguồn đã dùng tên mới; các thư mục kết quả cũ vẫn mang tên cũ (`repo/results/sgkr`, `repo/results/sphr`) và được ánh xạ qua `repo/src/utils/model_names.py`.
- **Đã làm.** Sinh lại toàn bộ 39 hình trong `repo/reports/figures` và 14 bảng CSV trong `repo/reports/tables` bằng `make_report.py` rồi `make_closed_form_report.py`.
- **Kết quả.** Không còn nhãn SGKR/SPHR trong hình hay bảng.

## 2. Lập kế hoạch viết báo cáo

- **Đã làm.** Đọc các tệp có sẵn trong `report/planning`, đối chiếu với bảng số liệu, mã nguồn và config, rồi viết kế hoạch chi tiết.
- **Phát hiện khi đối chiếu:**
  - Tên đầy đủ của hai mô hình có sẵn trong docstring: **Graph-Regularized Neighborhood Regression (GRNR)** và **Diffusion-Filtered History Factorization (DFHF)**.
  - Bìa `main.tex` vẫn là đề tài cũ (kho hàng, LNS/ALNS). Nguyễn Chí Tài và Phạm Văn Sự trùng MSSV 23010523; bìa chính ghi 2 tác giả, bìa lót ghi 3.
  - Mọi giá trị p = 0,0001 trong bảng kiểm định là mức thấp nhất bootstrap 10.000 lần đo được, không phải p chính xác. Phải viết "p ≤ 10⁻⁴".
  - Model huấn luyện được chọn checkpoint trên chính tập validation dùng để báo cáo, nên điểm bị nâng lạc quan. DirectAU đạt điểm cao nhất ở epoch 200/200, có thể chưa hội tụ.
  - Config GRNR ghi được chọn trên "selection half", nhưng thư mục nhật ký chứng minh việc này (`task_codex/`, `results/experiments/`) không có trong repo.
- **Kết quả.** Kế hoạch cũ đã lỗi thời được chuyển vào `report/log/`; kế hoạch mới là `report/planning/KE_HOACH_BAO_CAO.md`.

## 3. Chốt mục lục

Các quyết định của tác giả, theo thứ tự:

| Quyết định | Lý do / hệ quả |
|---|---|
| Bỏ phụ lục | Demo đưa vào Chương 4 thành mục riêng |
| Phần dữ liệu thành mục 4.1 gồm 5 tiểu mục | Pipeline tiền xử lý đủ phức tạp để trình bày kỹ |
| **GRNR và DFHF là hai mô hình độc lập, mỗi mô hình chỉ so với nhóm của nó** | Nhóm giải trực tiếp: GRNR so với EASE đầy đủ, EASE top-128, GF-CF. Nhóm cần huấn luyện: DFHF so với LightGCN, XSimGCL, DirectAU. **Không so GRNR với DFHF** trong văn bản, bảng hay hình |
| Tiêu đề 4.3, 4.4 dạng "… so với các mô hình …" | Tên cũ "Nhóm …: tên mô hình" bị chê nhàm |
| Mục lục và tiêu đề dùng tên đầy đủ, không viết tắt | Quy ước của báo cáo |

Mục lục chốt nằm ở mục 9 của kế hoạch và đã được hiện thực trong PDF.

## 4. Khóa bằng chứng: các phân tích bổ sung

Mọi tệp nằm trong `report/planning/phan_tich_bo_sung/`. Các script cần chạy trong repo đầy đủ, với Python `D:\Miniconda\envs\AML\python.exe` (PATH không có `python`).

| Việc | Script / kết quả | Kết luận |
|---|---|---|
| Kiểm kê tập test | `test_exposure/` | Không tệp kết quả nào lưu điểm test. Điều này không chứng minh tập test chưa từng được xem |
| Kiểm định DFHF trong nhóm | `t4_dfhf_significance.py` → `T4_dfhf_significance.csv`; khai báo family trước khi chạy ở `T4_family_declaration.md` | DFHF hơn cả 3 baseline ở cả 4 mức d; KTC 95% không chứa 0; p Holm ≤ 3×10⁻⁴. Phân tích làm sau khi đã xem kết quả, nên mang tính khám phá. Các tệp `dfhf_d*.json` là lần chạy đầu bị ngược chiều, **không dùng** |
| Chẩn đoán | `t6_diagnostics.py` → `t6_diagnostics.json` | Tỉ lệ người dùng chỉ còn 1 tương tác: 0% / 6,2% / 26,6% / **68,0%** ở d = 1 / 0,75 / 0,5 / 0,25. GRNR không có điểm âm trong top-20, nên hệ số giảm độ phổ biến không bị đảo chiều. Baseline không dùng hard negative |
| Tách kết quả theo số tương tác còn lại | `t6f_degree_split.py` → `.json` | Ở d25, DFHF trên người dùng 1 tương tác đạt 0,01787 |
| Mốc MostPop | `t6g_mostpop.py`, `t6h_vs_mostpop.py` → `.json`, `.csv` | Xem mục 5 bên dưới |
| Hình riêng cho nhóm huấn luyện | `repo/scripts/make_trained_group_report.py` → `report/image/` | 10 hình không chứa GRNR |

## 5. Phát hiện quan trọng nhất: mốc MostPop

- **MostPop** xếp sản phẩm theo số tương tác trong tập huấn luyện. Mốc này đạt NDCG@20 ≈ 0,018 ở mọi mức d.
- Ở **d = 0,25, không mô hình nào vượt MostPop**:
  - DFHF ngang MostPop (Δ = −0,00005, KTC [−0,00029; 0,00018]);
  - mọi mô hình khác, kể cả GRNR, thấp hơn rõ.
- **Lý do:** 68% người dùng chỉ còn 1 tương tác. Với những người dùng này, DFHF chỉ dùng item bias, tức gần như xếp theo độ phổ biến.
- **Hệ quả cho báo cáo.** Câu "DFHF cao nhất nhóm ở d25" vẫn đúng, nhưng **không** được hiểu là DFHF học cá nhân hóa tốt hơn khi dữ liệu thưa. Báo cáo đã viết đúng như vậy ở mục 4.6 và Chương 5.
- MostPop là mốc tham chiếu chung, không thuộc nhóm nào, nên không vi phạm quy tắc "không so GRNR với DFHF".

## 6. Viết báo cáo

| Phần | Tệp | Ghi chú |
|---|---|---|
| Tài liệu tham khảo | `report/section/ref.tex` | 17 nguồn. Metadata kiểm qua arXiv API và Crossref; chưa ghi số trang hay số phương trình được trích |
| Chương 1–5 | `report/section/section1.tex` … `section5.tex` | Bản thảo đầy đủ theo mục lục đã chốt |
| Bìa và dàn trang | `report/main.tex` | Đề tài mới; bỏ macro của đề tài cũ; thông tin chưa xác nhận để `[CẦN XÁC NHẬN]` |
| PDF | `report/main.pdf` | 45 trang, build không lỗi |

Nguyên tắc đã áp dụng khi viết:
- Mỗi con số đều lấy từ bảng hoặc tệp phân tích.
- Kết quả bất lợi nằm trong thân bài: EASE thắng GRNR ở d50, DirectAU có thể chưa hội tụ, DFHF phụ thuộc mạnh vào checkpoint.
- Giả thuyết cơ chế được ghi rõ là giả thuyết, vì chưa có thí nghiệm loại bỏ thành phần.

## 7. Chỉnh sửa trình bày theo yêu cầu

- **Đặt lại tên 13 hình, 18 bảng và 2 thuật toán.** Danh mục chỉ hiện tên ngắn, không viết tắt; phần chi tiết nằm dưới hình/bảng qua `\caption[tên ngắn]{tên + chi tiết}`.
- **Bỏ mọi tên file và đường dẫn khỏi thân bài.** Chỉ giữ tên các trường dữ liệu gốc của Amazon (`reviewerID`, `asin`, `overall`, `unixReviewTime`). Nguồn của từng số tra trong `report/planning/evidence_map.csv`.
- **Thêm hình NDCG@20 theo d có đường MostPop** cho mỗi nhóm. Hình do `repo/scripts/make_mostpop_reference_figures.py` sinh ra, lưu `report/image/H9_mostpop_*.png`, và thay cho hình cột cũ.
- **Thêm sơ đồ hoạt động** của GRNR (Hình 3.1) và DFHF (Hình 3.2), vẽ bằng TikZ ngay trong `section3.tex`.
- **Căn trái Bảng 3.1.**

## 8. Chuẩn bị bàn giao

- Kế hoạch được chuyển từ `report/` vào `report/planning/`.
- `main.tex` chỉ lấy hình trong `report/image/`. Bốn hình closed-form trước đây lấy từ `repo/reports/figures` đã được kiểm tra hash là trùng với bản trong `report/image/`.
- Vì vậy chỉ cần nén thư mục `report/` là build được.
- Đã viết nhật ký này và `report/planning/README.md`.

## Các tệp đã tạo hoặc sửa ngoài `report/`

Người nhận cần các tệp này nếu muốn chạy lại phân tích:
- `repo/scripts/make_trained_group_report.py` (mới)
- `repo/scripts/make_mostpop_reference_figures.py` (mới)
- `repo/reports/figures/*`, `repo/reports/tables/*` (sinh lại)

Chưa có commit git nào cho các thay đổi trong phiên này.

## 9. Dọn gọn thư mục `report/` trước khi bàn giao

- Xóa 10 tệp build phụ ở gốc (`main.aux`, `main.log`, `main.xdv`…); chúng tự sinh lại khi build.
- `image/` chỉ giữ 11 hình báo cáo dùng và logo. Đã xóa 35 hình không dùng, đều là bản sao giống hệt (đã so nội dung) của `repo/reports/figures`; và 5 hình không dùng của nhóm huấn luyện, sinh lại được bằng script. Thư mục con `image/trained/` được gộp vào `image/`.
- `planning/w1/` đổi tên thành `planning/phan_tich_bo_sung/`. Đã xóa 4 tệp `dfhf_d*.json` của lần chạy kiểm định bị ngược chiều; kết quả đúng là `T4_dfhf_significance.csv`.
- Kế hoạch cũ chuyển từ `planning/archive/` sang `log/KE_HOACH_CU_20261105.md`.
- README chuyển ra gốc `report/` và viết lại theo cấu trúc mới.
- `planning/figure_inventory.csv` viết lại, chỉ liệt kê các hình thực sự có trong báo cáo.
- Đường dẫn trong `evidence_map.csv`, kế hoạch và hai script `repo/scripts/make_*` đã được cập nhật theo cấu trúc mới. `make_trained_group_report.py` giờ chỉ sinh các hình báo cáo dùng.

## 10. Đưa số liệu gốc vào `report/`

- Vấn đề: PDF đã có đủ 15 hình và 18 bảng, nhưng các file số liệu gốc mà những con số đó lấy ra (`repo/reports/tables/*.csv`, `repo/results/*/metrics.json`, manifest và audit dữ liệu) nằm ngoài `report/`. Người nhận gói zip không kiểm tra lại được.
- Đã chép 47 file (176 KB) vào `report/planning/so_lieu_goc/`; nguồn gốc và sha256 từng file ghi trong `so_lieu_goc/NGUON_GOC.csv`. Thư mục `sgkr`/`sphr` cũ được đặt tên lại theo tên mô hình mới trong tên file bản sao (`grnr_d100_metrics.json`, `dfhf_d100_metrics.json`...).
- `evidence_map.csv` có thêm cột `path_in_report`, trỏ tới bản sao; thêm E29 (MostPop) và E30 (sổ lọc dữ liệu). Các dòng còn ghi "(chỉ có trong repo)" là mã nguồn dùng để đối chiếu công thức, không phải nguồn số liệu.
