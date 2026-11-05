# Bàn giao báo cáo — đọc tệp này trước

Báo cáo bài tập lớn: **"Hai mô hình khuyến nghị dựa trên lịch sử tương tác và đánh giá trên Amazon Electronics"**.

Trạng thái ngày 05/11/2026: **đã có bản thảo đầy đủ 5 chương, PDF 45 trang**. Còn thiếu thông tin hành chính và một vòng rà soát nội bộ (xem mục 5).

## 1. Thư mục này có gì

```text
report/
├── README.md                Tệp này
├── main.tex                 Tệp LaTeX chính (bìa, mục lục, nạp các chương)
├── main.pdf                 Bản PDF hiện tại
├── section/                 Nội dung: section1.tex … section5.tex (5 chương), ref.tex (tài liệu tham khảo)
├── image/                   Đúng 11 hình báo cáo dùng + logo
├── planning/                Kế hoạch và bằng chứng
│   ├── KE_HOACH_BAO_CAO.md      Kế hoạch chi tiết: sổ claim, vấn đề phản biện, checklist rà soát
│   ├── evidence_map.csv         Mỗi con số trong báo cáo lấy từ tệp nào
│   ├── figure_inventory.csv     Hình nào trong báo cáo ứng với tệp ảnh nào, sinh bằng script nào
│   ├── LITERATURE_LOG.md        Nhật ký tìm tài liệu
│   ├── phan_tich_bo_sung/       Script và kết quả các phân tích làm thêm cho báo cáo
│   └── so_lieu_goc/             Bản sao các file số liệu gốc mà báo cáo lấy số từ đó
│       ├── bang_ket_qua/            Bảng tổng hợp B1–B6 (CSV)
│       ├── ket_qua_tung_run/        metrics.json của 28 lần chạy (7 mô hình × 4 mức d)
│       ├── du_lieu/                 Manifest và audit của bộ dữ liệu
│       └── NGUON_GOC.csv            Mỗi bản sao lấy từ đâu trong repo, kèm sha256
└── log/                     Lịch sử
    ├── NHAT_KY_CONG_VIEC.md     Đã làm gì, theo thứ tự, vì sao
    └── KE_HOACH_CU_20261105.md  Kế hoạch đầu tiên, đã lỗi thời, chỉ để tra lại
```

Thứ tự đọc gợi ý: tệp này → `main.pdf` → `log/NHAT_KY_CONG_VIEC.md` → `planning/KE_HOACH_BAO_CAO.md` (khi cần tra cứu).

## 2. Cách build PDF

Chạy trong thư mục `report/` (đã kiểm tra với MiKTeX, XeLaTeX, font Times New Roman):

```text
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

- Xong thì dọn tệp phụ bằng `latexmk -c`; lệnh này giữ lại `main.pdf`.
- Nếu gặp lỗi lạ như `Missing \begin{document}`, chạy `latexmk -c` rồi build lại.

## 3. Quy tắc phải giữ khi sửa

1. **GRNR và DFHF không bao giờ được so với nhau.**
   - GRNR chỉ so với EASE đầy đủ, EASE top-128, GF-CF (nhóm giải trực tiếp).
   - DFHF chỉ so với LightGCN, XSimGCL, DirectAU (nhóm cần huấn luyện).
   - Mỗi hình và mỗi bảng chỉ chứa một nhóm.
   - MostPop là mốc tham chiếu chung, được phép xuất hiện ở cả hai nhóm.
2. **Mục lục, tiêu đề và tên hình/bảng dùng tên đầy đủ**, không viết tắt. Dùng dạng `\caption[tên ngắn]{tên ngắn. Chi tiết.}`.
3. **Không đưa tên file hay đường dẫn vào báo cáo.** Nguồn số liệu ghi trong `planning/evidence_map.csv`; cột `path_in_report` chỉ tới bản sao nằm ngay trong thư mục này để kiểm tra lại.
4. **Mỗi con số phải truy được** về `evidence_map.csv`. Không thêm số mới vào Chương 5.
5. **Cách viết thống kê:**
   - viết "p ≤ 10⁻⁴", không viết "p = 0,0001";
   - kết quả không có ý nghĩa thì viết "chưa đủ bằng chứng", không viết "tương đương";
   - kết quả bất lợi vẫn để trong thân bài.
6. **Giải thích cơ chế** (vì sao mô hình tốt hay kém) chỉ là giả thuyết, vì chưa có thí nghiệm loại bỏ thành phần.

## 4. Kết quả chính cần nắm

Số liệu đo trên validation, seed 42, 107.215 người dùng. Chi tiết ở Chương 4.

- **GRNR:**
  - cao nhất nhóm ở d = 1 (NDCG@20 0,03829) nhưng chưa đủ bằng chứng hơn EASE đầy đủ;
  - **thua EASE rõ ràng ở d = 0,5**;
  - ưu điểm là chi phí thấp (2,5 phút, 40,5 MiB, so với EASE 11,2 phút và ma trận khoảng 7,5 GiB).
- **DFHF:**
  - cao nhất nhóm ở cả 4 mức d, khoảng tin cậy không chứa 0;
  - chậm nhất nhóm (37,9 giây/epoch);
  - kết quả phụ thuộc mạnh vào việc chọn checkpoint.
- **MostPop** (xếp theo độ phổ biến) ở d = 0,25:
  - không mô hình nào vượt được; DFHF chỉ ngang mốc này, vì 68% người dùng chỉ còn 1 tương tác và được xếp hạng bằng độ phổ biến;
  - phát hiện này phải giữ trong báo cáo.

## 5. Việc còn lại

| # | Việc | Mức | Cách làm |
|---|---|---|---|
| 1 | Điền tên học phần (header, bìa chính, bìa lót) | **Bắt buộc** | Tìm `[CẦN XÁC NHẬN` trong `main.tex` |
| 2 | Sửa MSSV trùng 23010523 (Nguyễn Chí Tài và Phạm Văn Sự); thống nhất số tác giả giữa bìa chính (2 người) và bìa lót (3 người) | **Bắt buộc** | `main.tex`, phần `titlepage` |
| 3 | Điền bảng phân công công việc và tỉ lệ đóng góp | **Bắt buộc** | Tìm `[CẦN NHÓM ĐIỀN` trong `main.tex` |
| 4 | Kiểm tra giới hạn số trang và quy định khai báo dùng AI | **Bắt buộc** | Nếu phải khai báo AI, thêm một đoạn cuối mục 1.3 |
| 5 | Rà soát nội bộ: một người đọc Chương 3 (công thức có khớp mã nguồn không), một người đọc Chương 4 (số có khớp bảng không) | Nên làm | Checklist ở mục 12 của `planning/KE_HOACH_BAO_CAO.md` |
| 6 | Tìm nhật ký chọn cấu hình GRNR/DFHF trên máy cũ hoặc Kaggle | Không bắt buộc | Nếu có, kiểm tra được kết quả trên phần validation chưa dùng để chọn |
| 7 | Giải thích bất thường của GF-CF | Không bắt buộc | Báo cáo hiện ghi "chưa giải thích" |
| 8 | Ghi số trang hoặc số phương trình được trích cho từng tài liệu tham khảo | Không bắt buộc | — |
| 9 | Cải thiện trình bày: ví dụ gợi ý thật cho một người dùng, khung "Phát hiện chính", ảnh chụp demo | Tùy chọn | Cần repo đầy đủ |

## 6. Muốn chạy lại số liệu hoặc sinh lại hình

Thư mục `report/` đủ để **đọc, sửa văn bản và build PDF**. Muốn **chạy lại phân tích** thì cần repository đầy đủ (`data/`, `results/`, `scripts/`) và Python env `AML` (`D:\Miniconda\envs\AML\python.exe`).

Chạy từ thư mục gốc repo:

```text
python scripts/make_closed_form_report.py         # hình nhóm giải trực tiếp -> reports/figures (chép H4, H5, H7a, H7c sang report/image)
python scripts/make_trained_group_report.py       # hình nhóm cần huấn luyện -> report/image
python scripts/make_mostpop_reference_figures.py  # hình có đường MostPop -> report/image
```

Script phân tích bổ sung nằm trong `planning/phan_tich_bo_sung/`, chạy từ gốc repo, ví dụ:

```text
python report/planning/phan_tich_bo_sung/t6g_mostpop.py
```

Sau khi sinh lại hình, cập nhật cột `sha256` trong `planning/figure_inventory.csv`.
