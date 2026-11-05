# Kế hoạch viết báo cáo hệ thống khuyến nghị

> **Đọc [../README.md](../README.md) trước.** Tệp này là kế hoạch gốc (mục 1–14) cộng nhật ký triển khai (mục 15). Một số dòng trong mục 2, 7, 10, 13 mô tả trạng thái *trước khi* triển khai; trạng thái hiện tại nằm ở [../README.md](../README.md) và [../log/NHAT_KY_CONG_VIEC.md](../log/NHAT_KY_CONG_VIEC.md).

Cập nhật: 05/11/2026. Trạng thái: **đề xuất, cần tác giả duyệt**. Đây là kế hoạch duy nhất còn hiệu lực. Bản cũ đã lỗi thời được lưu tại [archive/](archive/) chỉ để tra lại.

Tài liệu đi kèm:
- [evidence_map.csv](evidence_map.csv): sổ bằng chứng.
- [figure_inventory.csv](figure_inventory.csv): kiểm kê hình và hash.
- [LITERATURE_LOG.md](LITERATURE_LOG.md): nhật ký tài liệu.

Nhãn dùng trong tệp:
- **[BC]**: bằng chứng đã định vị trong tệp.
- **[GT]**: giả thuyết hoặc giải thích chưa kiểm chứng.
- **[QĐ]**: quyết định biên tập.
- **[CẦN]**: việc phải làm trước khi viết claim liên quan.

---

## 1. Phạm vi và quy ước

**Phạm vi.** Báo cáo bài tập lớn bằng tiếng Việt cho repository này.
- Giữ khung [main.tex](../main.tex): class article, không dùng `\chapter`.
- Nội dung viết vào `section/section1.tex` … `section5.tex`; tài liệu tham khảo vào `section/ref.tex`. Không có phụ lục.
- Hình lấy từ `../reports/figures` và `image/`; số liệu lấy từ `../reports/tables` và `planning/phan_tich_bo_sung/`.
- Ngân sách 38–47 trang nội dung, cho tới khi biết giới hạn của học phần.

**Ngôn ngữ.**
- Giữ nguyên tên gốc tiếng Anh của thuật toán, mô hình và phương pháp; không dịch thành tên tiếng Việt thay thế.
- Phần diễn giải viết bằng tiếng Việt. Có thể giải nghĩa ngắn khi thuật ngữ xuất hiện lần đầu.

**Viết tắt.**
- Mục lục và tiêu đề dùng tên đầy đủ, không dùng dạng viết tắt.
- Lần đầu trong thân bài ghi tên đầy đủ kèm viết tắt trong ngoặc; các lần sau chỉ dùng viết tắt.

**Tên hai mô hình.** [BC] Lấy từ docstring:
- `src/models/grnr.py:1`: **Graph-Regularized Neighborhood Regression (GRNR)**.
- `src/models/dfhf.py:1`: **Diffusion-Filtered History Factorization (DFHF)**.

Thư mục kết quả cũ vẫn mang tên `results/sgkr`, `results/sphr`; ánh xạ tên nằm trong `src/utils/model_names.py`. Báo cáo không nhắc tới tên cũ.

**Hai nhóm so sánh** [QĐ, tác giả chốt 05/11/2026]. GRNR và DFHF là hai mô hình độc lập thuộc hai nhóm khác nhau. Mỗi mô hình chỉ được so với các baseline cùng nhóm. **Không đặt GRNR và DFHF đối đầu nhau**, cũng không kể chuyện “đánh đổi giữa hai mô hình”. Cách nhóm này khớp với hai tab “Nhóm giải trực tiếp” và “Nhóm cần huấn luyện” trong app.

| Nhóm | Mô hình đề xuất | Baseline cùng nhóm | Đặc điểm chung |
|---|---|---|---|
| Nhóm giải trực tiếp | GRNR | EASE đầy đủ, EASE top-128, GF-CF | Có nghiệm đóng hoặc lọc tuyến tính; không có epoch; không cần optimizer |
| Nhóm cần huấn luyện | DFHF | LightGCN, XSimGCL, DirectAU | Học bằng gradient trong 200 epoch; lưu checkpoint tốt nhất theo validation NDCG@20 |

**Thứ tự tin cậy của nguồn.**
1. metrics và prediction của run đã khóa;
2. snapshot mã nguồn và config của chính run đó;
3. mã nguồn hiện tại;
4. bảng và hình dẫn xuất;
5. README.

Khi các nguồn mâu thuẫn, ghi vào mục 4 thay vì chọn con số thuận tiện.

**Cách kết hợp skill.**

| Skill | Dùng để làm gì | Mục |
|---|---|---|
| scientific-brainstorming | Chọn trục lập luận, sinh giải thích cạnh tranh | 3, 11 |
| scientific-critical-thinking | Tìm thiên lệch, đối chiếu claim với giao thức | 4 |
| scientific-writing | Lập sổ claim, viết đề cương đến cấp đoạn, đặt quy tắc hình/bảng | 5, 9, 10 |
| literature-review | Tìm và trích xuất tài liệu, định vị tính mới có giới hạn | 8 |
| peer-review | Thiết kế vòng rà soát nội bộ và checklist | 12 |

## 2. Hiện trạng tài nguyên

| Tài nguyên | Hiện trạng [BC] | Việc cần làm |
|---|---|---|
| main.tex | Đã có bìa, bìa lót, mục lục, danh mục hình/bảng. Đề tài và học phần vẫn của bài cũ (kho hàng, LNS/ALNS). Bìa chính ghi 2 tác giả, bìa lót ghi 3. **Nguyễn Chí Tài và Phạm Văn Sự trùng MSSV 23010523** | Sửa theo W0 |
| section1–5, ref, guided.tex | Cả 7 tệp đang trống. guided.tex chưa được nạp | Viết theo mục 9 |
| reports/figures | 39 PNG, sinh lại ngày 05/11/2026 với nhãn GRNR/DFHF. Bộ `*_closed_form_*` đúng nhóm giải trực tiếp. Bộ H1/H4/H5/H3/H7 chính **gộp cả GRNR lẫn nhóm huấn luyện**, nên không dùng trực tiếp được | Sinh bộ hình riêng cho nhóm huấn luyện (T8) |
| reports/tables | 14 CSV. B5/B6 thuộc nhóm giải trực tiếp. B2a/B2b/B4 có cả hai nhóm, phải lọc. B3/B3b dùng family Holm 6 so sánh có cả GRNR (R23) | Lọc và tính lại (T4) |
| results | 7 mô hình × 4 mức d, đều seed 42, split validation | Khóa provenance (W1) |
| report_manifest.json | Còn đường dẫn máy cũ D:/advanced-machine | Bổ sung ở T7 |
| data/processed | Có `test.parquet` | Không dùng nếu chưa có Q4 |
| Python | PATH không có `python`; dùng `D:\Miniconda\envs\AML\python.exe` | — |

## 3. Trục lập luận và câu hỏi nghiên cứu

**Các hướng đã cân nhắc** [QĐ]:

| ID | Hướng | Quyết định |
|---|---|---|
| I01 | Một mô hình thắng mọi baseline ở mọi điều kiện | Loại: GRNR thua EASE ở d50 |
| I02 | Hai mô hình độc lập; mỗi mô hình được đánh giá trong nhóm phương pháp của nó | **Chọn** |
| I03 | Hệ khuyến nghị đa phương thức | Loại: các mô hình không dùng text/metadata để xếp hạng |
| I04 | Demo và giải thích gợi ý | Mục 4.5, là phần triển khai; không thay benchmark |
| I05 | So sánh trực tiếp GRNR với DFHF, kể chuyện đánh đổi giữa hai mô hình | **Loại** theo quyết định của tác giả: hai mô hình thuộc hai nhóm khác nhau |

**Tên đề tài đề xuất:** “Hai mô hình khuyến nghị dựa trên lịch sử tương tác và đánh giá trên Amazon Electronics”.

**Luận điểm:** dự án đề xuất hai mô hình. Cả hai biểu diễn người dùng hoàn toàn bằng lịch sử tương tác, không có vector user riêng.
- Graph-Regularized Neighborhood Regression thuộc nhóm giải trực tiếp.
- Diffusion-Filtered History Factorization thuộc nhóm cần huấn luyện.

Mỗi mô hình được đánh giá so với các phương pháp cùng nhóm, trên cùng dữ liệu và giao thức. Kết luận chỉ đúng trong cấu hình đã chạy.

| ID | Câu hỏi | Mục trả lời | Bằng chứng |
|---|---|---|---|
| RQ1 | Trong nhóm của mình, mỗi mô hình đề xuất xếp hạng tốt đến đâu so với các baseline cùng nhóm? | 4.3.1, 4.4.1 | B5, B6 (GRNR); B2a đã lọc và T4 (DFHF) |
| RQ2 | Khi giữ 100/75/50/25% tương tác train, chất lượng của mỗi mô hình thay đổi thế nào so với baseline cùng nhóm? | 4.3.2, 4.4.2 | B5, B6, H*_closed_form_*; B2b đã lọc, T4, hình T8 |
| RQ3 | Chi phí tính toán của mỗi mô hình so với nhóm của nó ra sao? | 4.3.3, 4.4.3 | B5, H7a/H7c closed-form; B4 đã lọc, hình T8 |
| RQ4 | Hệ thống phục vụ lịch sử mới và giải thích gợi ý như thế nào? | 4.5 | app/recommender.py, app/streamlit_app.py |

Kết quả đã có trước khi đặt câu hỏi, nên các RQ và mọi diễn giải đều mang tính hồi cứu/khám phá, không phải giả thuyết đăng ký trước.

## 4. Vấn đề phản biện cần xử lý

### P0 — chặn claim liên quan

| ID | Quan sát [BC] | Hành động |
|---|---|---|
| R1 | Mọi p trong B3/B3b/B6 bằng 0,0001. Đây là **sàn Monte Carlo** (0+1)/(10⁴+1) của bootstrap, không phải p chính xác | Viết “p ≤ 10⁻⁴” |
| R2 | Trong nhóm huấn luyện, mọi mô hình đều lưu checkpoint tốt nhất trong 200 lần đánh giá trên **chính tập validation dùng để báo cáo**. Cách chọn đồng nhất trong nhóm, nhưng điểm tuyệt đối bị nâng lạc quan. Trong nhóm giải trực tiếp, GRNR được tuning (R12) còn EASE/GF-CF dùng cấu hình cố định (R15) | Nêu ở 4.2 và 4.6, riêng cho từng nhóm |
| R3 | DirectAU tốt nhất ở epoch 200/200 (d100), 195 (d50), 181 (d25) | Baseline có thể chưa hội tụ. Ghi là giới hạn của so sánh DFHF; thêm epoch là nhánh mở rộng (Q6) |
| R4 | GRNR − EASE đầy đủ ở d50: Δ = −0,00202, CI [−0,00237; −0,00167] | Kết quả bất lợi, đưa vào thân bài 4.3.2 |
| R5 | Catalog có 44.843 item nhưng chỉ 44.803 là candidate. Validation có 107.274 tương tác nhưng chỉ 107.215 warm user | Viết đủ bộ lọc và mẫu số |
| R6 | Timestamp ở mức ngày; 45.431 user hòa giữa train và validation | Mô tả là thứ tự “không giảm”, không phải dự đoán tương lai nghiêm ngặt |
| R7 | Chỉ một seed. Bootstrap chỉ lấy mẫu lại user trên một model cố định | Không gọi CI là độ ổn định giữa các lần huấn luyện |
| R8 | GRNR − EASE đầy đủ ở d100: p Holm = 0,051 | Viết “chưa đủ bằng chứng”; không suy ra tương đương |
| R23 | B3/B3b dùng family Holm 6 so sánh (GRNR và DFHF so với 3 baseline neural) và chỉ có d100 | Không dùng các dòng GRNR−neural. Tính lại family 3 so sánh cho DFHF ở cả 4 mức d (T4) |

### P1 — cần chẩn đoán hoặc ghi nhận

| ID | Quan sát [BC] | Hành động |
|---|---|---|
| R9 | DFHF giảm 24–37% từ epoch tốt nhất tới epoch cuối (d100: 0,03519 → 0,02658). XSimGCL ở d25 tốt nhất tại epoch 6 | Bảng best-vs-last có cột % giảm, cho cả 4 mô hình trong nhóm |
| R10 | `dfhf.py:164-166, 201-207`: user có đúng 1 tương tác giữ lại có q_u = 0 **cả khi suy luận**, nên chỉ được xếp hạng bằng item bias | T6a; mô tả trong 3.3; đọc nhóm user ở 4.4.2 kèm lưu ý này |
| R11 | `grnr.py:362`: popularity tilt nhân lên điểm thô; nếu điểm âm thì chiều tilt bị đảo | T6b |
| R12 | `configs/grnr.yaml` ghi khóa ở “Gate B, selection half” nhưng `task_codex/` và `results/experiments/` không có trong repo. Config DFHF ghi 0,03546, còn run báo cáo cho 0,03519 | T1. Không truy được thì không nhắc chuyện chia nửa |
| R13 | GF-CF: NDCG@20 ở d50 (0,00384) ≈ d25 (0,00385); thời gian train không đơn điệu theo d | T6c. Chưa rõ thì ghi “bất thường chưa giải thích” |
| R14 | Chưa có kiểm định DFHF với từng baseline cùng nhóm ở d25, d50, d75 | T4, gắn nhãn post hoc |
| R15 | EASE/GF-CF dùng cấu hình cố định; ngân sách tuning không cân bằng trong nhóm giải trực tiếp | Công bố cấu hình; giới hạn claim |
| R16 | Phần cứng, batch và cách đo thời gian khác nhau giữa các run | Bảng phần cứng; không kết luận “nhanh hơn về bản chất” |
| R17 | Chưa có ablation | Thành phần chỉ là lựa chọn thiết kế; cơ chế ghi là [GT] |
| R18 | Audit và manifest không chứng minh tập test chưa từng bị xem | T2; không gọi test là “untouched” |
| R21 | Thuật toán giảm tương tác dùng lõi phủ nên không ngẫu nhiên đều; mỗi d chỉ lấy mẫu một lần | Mô tả ở 4.1.4; T6d |
| R22 | Có 65.854 tương tác bị chê (rating < 4) và `trainer.py` hỗ trợ hard negative; chưa rõ baseline nào dùng | T6e |

### P2

| ID | Quan sát | Hành động |
|---|---|---|
| R19 | Cột “Checkpoint (MB)” thực chất chia cho 2²⁰. Con số 7.671 của EASE đầy đủ là kích thước dense ước tính, không phải file đã lưu | Đổi nhãn thành MiB; tách dung lượng đĩa với dense lý thuyết |
| R20 | H5 nhiều panel, nhãn nhỏ; H2 trùng byte với H1 | Xem ở khổ in 15,5 cm; bỏ H2 |

## 5. Sổ claim

Mọi số lấy từ `reports/tables/`: validation, seed 42, n = 107.215 warm user. Mỗi câu kết quả trong báo cáo phải trỏ về một dòng ở đây. Không có claim nào so GRNR với DFHF.

### Nhóm giải trực tiếp (GRNR)

| ID | Claim | Số liệu và nguồn | Câu được phép | Không được viết |
|---|---|---|---|---|
| C01 | GRNR có NDCG@20 cao nhất nhóm ở d100 | GRNR 0,03829; EASE đầy đủ 0,03796; EASE top-128 0,03679; GF-CF 0,01886 (B5) | “cao nhất về giá trị điểm trong nhóm” | “vượt trội EASE” |
| C02 | Chưa đủ bằng chứng GRNR hơn EASE đầy đủ ở d100 | Δ +0,00033 [−0,00007; +0,00073], p Holm 0,051 (B6) | “chưa đủ bằng chứng theo phép so sánh này” | “tương đương EASE” |
| C03 | GRNR hơn EASE top-128 và GF-CF ở d100 | Δ +0,00150 [0,00111; 0,00189]; Δ +0,01943 [0,01874; 0,02010]; p Holm ≤ 3×10⁻⁴ (B6) | “chênh lệch dương, CI không chứa 0” | “tốt hơn nói chung” |
| C04 | EASE đầy đủ hơn GRNR ở d50 | Δ −0,00202 [−0,00237; −0,00167] (B6) | Nêu thẳng là kết quả bất lợi | Bỏ qua |
| C05 | Kết quả của GRNR theo mức d không đơn điệu so với EASE | d25: Δ +0,00124 [0,00095; 0,00154]; d50: C04; d75: Δ −0,00011 [−0,00049; 0,00028]; d100: C02. So với top-128: hơn ở d25/d75/d100, thua ở d50 (B6) | Nêu theo từng d | “luôn tốt hơn khi dữ liệu thưa” |
| C06 | Tỉ lệ giữ chất lượng (NDCG@20 d25/d100) trong nhóm | GRNR 20,8%; GF-CF 20,4%; EASE đầy đủ 17,8%; EASE top-128 13,5% | Luôn kèm điểm tuyệt đối | “bền với cold-start” |
| C07 | Chi phí của GRNR trong nhóm | GRNR 2,5 phút, 40,5 MiB; EASE 11,2 phút (top-128 31,9 MiB; dense ~7.671 MiB ước tính); GF-CF 45,2 phút, 43,2 MiB (B5, d100) | Ghi phần cứng của từng run | “nhanh hơn về bản chất” |

### Nhóm cần huấn luyện (DFHF)

| ID | Claim | Số liệu và nguồn | Câu được phép | Không được viết |
|---|---|---|---|---|
| C08 | DFHF hơn cả ba baseline cùng nhóm ở d100 | Δ so với XSimGCL +0,00228 [0,00172; 0,00284]; so với DirectAU +0,00314 [0,00251; 0,00378]; so với LightGCN +0,00864 [0,00802; 0,00928]; p một phía ≤ 10⁻⁴ (B3). Holm phải tính lại trên family 3 (T4) | “chênh lệch dương, CI không chứa 0”, kèm R2, R3 | “tốt hơn nói chung” |
| C09 | DFHF có NDCG@20 cao nhất nhóm ở cả 4 mức d | d100 0,03519 so với 0,03292; d75 0,02901 so với 0,02759; d50 0,02266 so với 0,0205; d25 0,01766 so với 0,01117 (B2b) | “cao nhất về điểm”; thêm CI sau T4 | “có ý nghĩa thống kê” khi chưa có T4 |
| C10 | Tỉ lệ giữ chất lượng trong nhóm | d25/d100: DFHF 50,2%; XSimGCL 33,9%; DirectAU 32,1%; LightGCN 31,7%. **d50/d100: LightGCN 69,3% > DFHF 64,4%** > DirectAU 64,0% > XSimGCL 58,7% | Nêu đủ cả hai mức, kèm điểm tuyệt đối | “DFHF luôn bền nhất” |
| C11 | DFHF phụ thuộc mạnh vào checkpoint | Epoch tốt nhất 71/200; NDCG@20 ở epoch cuối thấp hơn 24,5% (B4) | Nêu kèm R2 | Mô tả là dừng sớm |
| C12 | Chi phí của DFHF trong nhóm | 37,9 s/epoch, chậm nhất nhóm (DirectAU 24,1; XSimGCL 17,7; LightGCN 11,2); tổng ~127 phút ở d100 (B4) | Ghi phần cứng | “chậm về bản chất” |

### Chung

| ID | Claim | Câu được phép | Không được viết |
|---|---|---|---|
| C13 | Thành phần của mô hình có ích | Lựa chọn thiết kế kèm động cơ [GT] (chưa có ablation) | “nhờ khuếch tán nên…” |
| C14 | Phân rã đóng góp điểm của GRNR (`score_parts`) | “phân rã đại số” | “giải thích nhân quả” |

## 6. Lộ trình

```text
W0 chốt thông tin ──────────────────────────────────────────┐
W1 khóa bằng chứng (T1–T8) ──► W3 Chương 3 ──► W4 Chương 4 ──┤
W2 đọc tài liệu ───────────────────────────► W5 Ch.2 → Ch.1 → Ch.5 → tóm tắt
                                                             └► W6 LaTeX ► W7 rà soát ► W8 PDF
```

Đường găng là W1 → W3 → W4. W2 làm song song.

### W0 — Quyết định cần tác giả

| # | Câu hỏi | Mặc định nếu chưa trả lời |
|---|---|---|
| Q1 | Tên học phần, mã lớp, GVHD | Giữ chỗ `[CẦN XÁC NHẬN]` |
| Q2 | Danh sách tác giả, MSSV đúng, phân công | Không điền bảng phân công |
| Q3 | Giới hạn trang, hạn nộp, quy định về AI và trích dẫn | 38–47 trang; khai báo AI (nếu bắt buộc) đặt ở cuối 1.3 |
| Q4 | Có được dùng `test.parquet` không? | **Không**; chạy T2 để kiểm kê |
| Q5 | Xác nhận tên đầy đủ GRNR/DFHF | Dùng tên trong docstring |
| Q6 | Có làm nhánh mở rộng không (thêm epoch cho DirectAU, ablation, nhiều seed)? | Không; thu hẹp claim tương ứng |

## 7. W1 — Khóa bằng chứng

Output ghi vào `report/planning/phan_tich_bo_sung/` (số liệu) và `report/image/` (hình). **Không** ghi vào `reports/`, vì `make_report.py` xóa thư mục đó mỗi lần chạy.

| ID | Việc | Lệnh hoặc cách làm | Tiêu chí xong |
|---|---|---|---|
| T1 | Tìm provenance của Gate B (R12) | Tìm `task_codex/` và `results/experiments/` trên máy cũ hoặc Kaggle; đối chiếu 0,03546 với 0,03519 | Biết cấu hình được chọn trên nửa nào và đã thử bao nhiêu cấu hình; hoặc ghi rõ “không truy được” |
| T2 | Kiểm kê tiếp xúc với test (R18) | `python scripts/audit_test_exposure.py --output-dir report/planning/phan_tich_bo_sung/test_exposure` | Biết run nào có `test_metrics` |
| T3 | Tái kiểm các model ở d100 | `python scripts/verify_results.py --output report/planning/phan_tich_bo_sung/validation_recheck.json --device cpu` | Sai khác so với bảng < 1e-5, hoặc có ghi chép |
| T4 | Kiểm định DFHF trong nhóm huấn luyện (R14, R23) | Với mỗi d: `scripts/compare_val_runs.py <DFHF> <LightGCN> <XSimGCL> <DirectAU> --sparsity d --holm --output report/planning/phan_tich_bo_sung/dfhf_d{d}.json` | Family 3 so sánh mỗi d, ghi vào tệp **trước** khi chạy; có Δ, CI, p, p Holm, n; giống cấu trúc B6 của GRNR |
| T5 | Chạy `--half confirmation`, chỉ khi T1 xác nhận có chia nửa | Như T4 và B6, thêm `--half confirmation` | Gọi đúng tên “nửa xác nhận cho lựa chọn cấu hình” |
| T6 | Chẩn đoán R10, R11, R13, R21, R22 | Script nhỏ trong `planning/phan_tich_bo_sung/`: (a) tỉ lệ warm user bậc 1 theo d; (b) tỉ lệ điểm GRNR âm trong top-20; (c) config và env của GF-CF; (d) phân phối bậc user/item trước và sau giảm; (e) baseline nào dùng hard negative | Mỗi R có kết luận, hoặc ghi “chưa giải thích” |
| T7 | Cập nhật evidence_map và manifest | Thêm E23+; dùng đường dẫn tương đối và hash | Mọi claim đều có evidence ID |
| T8 | Sinh bộ hình riêng cho nhóm huấn luyện | Viết `scripts/make_trained_group_report.py` theo mẫu `make_closed_form_report.py`, dùng `bar_figure(..., order=("dfhf","lightgcn","xsimgcl","directau"))`. Sinh H1/H4/H5 (NDCG@20, Recall@20), H3 learning curve không có đường GRNR, H7a/H7b. Ghi vào `report/image/` | Hình không chứa GRNR; cập nhật figure_inventory |

## 8. W2 — Tổng quan tài liệu

Đã mở record L01–L08 (xem LITERATURE_LOG). Các record này mới chỉ xác nhận metadata/abstract; muốn dẫn công thức phải mở full text và ghi trang hoặc số phương trình. Danh sách dưới đây là **ứng viên chưa xác minh**.

| Ưu tiên | Ứng viên | Vì sao cần | Dùng ở |
|---|---|---|---|
| A | Hu, Koren, Volinsky — Collaborative Filtering for Implicit Feedback Datasets (ICDM 2008) | Mục tiêu của GRNR là bình phương tối thiểu có trọng số trên dữ liệu ngầm | 2.1, 3.2.2 |
| A | Ning, Karypis — SLIM (ICDM 2011) | Hồi quy item–item thưa; cùng nhóm với EASE và GRNR | 2.2 |
| A | Steck — EASE (L04); EDLAE và các biến thể closed-form | Baseline chính của nhóm giải trực tiếp | 2.2 |
| A | Koren — Factorization Meets the Neighborhood (KDD 2008); Paterek — NSVD (2007); FISM (L06) | Biểu diễn user bằng tổng embedding lịch sử, tiền thân của DFHF | 2.3, 3.3 |
| A | Liang và cộng sự — Mult-VAE (WWW 2018) | Softmax trên toàn catalog, giống loss của DFHF | 2.3, 3.3.2 |
| A | Krichene, Rendle — On Sampled Metrics (KDD 2020) | Lý do dùng full ranking | 4.2 |
| A | Ferrari Dacrema và cộng sự — Are We Really Making Much Progress? (RecSys 2019) | Tuning baseline không cân bằng (R3, R15) | 4.6 |
| B | Rendle và cộng sự — BPR (UAI 2009) | Loss của LightGCN | 2.3 |
| B | Sun và cộng sự (RecSys 2020); Ji và cộng sự (TOIS 2023) | Temporal split, leakage (R6) | 4.1, 4.6 |

Quy trình cho mỗi nguồn: mở record → điền bảng trích xuất → đánh dấu `support`/`challenge` cho claim → đặt khóa `tacgiaNam` trong `ref.tex` (thebibliography). Về tính mới, chỉ được viết: “trong phạm vi tài liệu đã kiểm tra, chưa thấy …”.

Tiêu chí xong W2: mỗi thành phần được ghi là “kế thừa từ [nguồn]” hoặc “lựa chọn của dự án”.
- GRNR: láng giềng theo excess co-occurrence, WLS, prior cho bias, phạt theo support, Laplacian kèm boundary, tilt.
- DFHF: hai bảng nguồn/đích không buộc, bộ lọc ½I + ¼T + ¼T², chuẩn hóa n^-½, softmax trên context leave-one-out.

## 9. W3–W5 — Đề cương đến cấp đoạn

### Mục lục

```text
1. Giới thiệu
   1.1. Đặt vấn đề
   1.2. Mục tiêu và phạm vi nghiên cứu
   1.3. Đóng góp của dự án
2. Cơ sở lý thuyết và nghiên cứu liên quan
   2.1. Khuyến nghị từ phản hồi ngầm
   2.2. Nhóm mô hình giải trực tiếp
   2.3. Nhóm mô hình cần huấn luyện
   2.4. Tổng hợp và định hướng đề xuất
3. Phương pháp và thuật toán đề xuất
   3.1. Mô hình bài toán
   3.2. Graph-Regularized Neighborhood Regression
        3.2.1. Lựa chọn láng giềng và đồ thị sản phẩm
        3.2.2. Hàm mục tiêu và phương pháp giải
        3.2.3. Thuật toán huấn luyện và suy luận
   3.3. Diffusion-Filtered History Factorization
        3.3.1. Biểu diễn lịch sử và bộ lọc khuếch tán
        3.3.2. Hàm mục tiêu và phương pháp tối ưu
        3.3.3. Thuật toán huấn luyện và suy luận
   3.4. Phân tích tính chất và chi phí tính toán
4. Thực nghiệm và phân tích kết quả
   4.1. Dữ liệu và tiền xử lý
        4.1.1. Nguồn dữ liệu
        4.1.2. Quy trình tiền xử lý
        4.1.3. Chia tập theo thời gian
        4.1.4. Tạo các mức giảm tương tác
        4.1.5. Vai trò của từng phần dữ liệu
   4.2. Thiết lập và giao thức đánh giá
   4.3. Graph-Regularized Neighborhood Regression so với các mô hình giải trực tiếp
        4.3.1. Chất lượng xếp hạng
        4.3.2. Ảnh hưởng của mức độ thưa và nhóm người dùng
        4.3.3. Chi phí tính toán
   4.4. Diffusion-Filtered History Factorization so với các mô hình cần huấn luyện
        4.4.1. Chất lượng xếp hạng
        4.4.2. Ảnh hưởng của mức độ thưa và nhóm người dùng
        4.4.3. Quá trình huấn luyện và chi phí tính toán
   4.5. Hệ thống demo
   4.6. Thảo luận và hạn chế
5. Kết luận và hướng phát triển
   5.1. Kết luận
   5.2. Hướng phát triển
Tài liệu tham khảo
```

Ký hiệu: ¶ = đoạn văn. Thứ tự viết: Chương 3 → 4 → 2 → 1 → 5 → tóm tắt.

### Chương 3 — section3.tex (10–13 trang)

**3.1. Mô hình bài toán (1,5 tr)**
- ¶1 Ký hiệu: U, I, X ∈ {0,1}^{|U|×|I|}, H_u, n_u, c_i, K.
- ¶2 Phân biệt bốn thực thể:
  - train gốc, dùng làm mask;
  - train giữ lại theo d, dùng làm đầu vào;
  - tập candidate;
  - cohort warm.
- ¶3 Phân biệt tỉ lệ giữ d với mật độ tuyệt đối.
- ¶4 Giới thiệu hai mô hình như **hai đề xuất độc lập** thuộc hai nhóm (bảng nhóm ở mục 1). Điểm chung duy nhất: không có vector user riêng, nên chấm được lịch sử mới mà không cần huấn luyện lại.

**3.2. Graph-Regularized Neighborhood Regression (4–5 tr)** — viết từ `grnr.py` và `configs/grnr.yaml`

*3.2.1 Láng giềng và đồ thị sản phẩm*
- p_i = (c_i+1)/(|U|+2).
- e_ij = C_ji − c_j·p_i.
- lift_ij = e_ij/(c_j+α), với α = 10.
- Giữ tối đa 128 nguồn có lift > 0, xếp theo e giảm dần.
- Đồ thị item: đối xứng hóa bằng max; L = I − D^-½WD^-½.

*3.2.2 Hàm mục tiêu và phương pháp giải*
- Đặc trưng: φ_u = [X_{u,N_i}/√max(n_u − X_ui, 1); 1].
- WLS: positive có trọng số w = 10; user còn lại nhận nhãn 0 với trọng số 1.
- Phạt: (θ−θ₀)ᵀ M P (θ−θ₀), trong đó:
  - M = |U|;
  - P = diag(η_lin·s_j) ⊕ η_bias + λ_g(L_NN − (1−β)B);
  - s_j = min((c_j/(c_j+α_s))^-2, 10);
  - θ₀ chỉ có thành phần bias, bằng w·p_i/(1+(w−1)·p_i).
- Giải phương trình chuẩn bằng Cholesky; sai số dư tương đối < 10⁻⁸.

*3.2.3 Thuật toán huấn luyện và suy luận*
- Giả mã fit: cache ma trận Gram, thay chính xác các hàng positive; item không có tương tác dùng prior.
- Giả mã score.
- Tilt (1+c_i)^-0,1 chỉ áp dụng khi xếp hạng (R11).
- Phân rã điểm (C14).
- Bảng siêu tham số.

**3.3. Diffusion-Filtered History Factorization (3,5–4,5 tr)** — viết từ `dfhf.py` và `configs/dfhf.yaml`

*3.3.1 Biểu diễn lịch sử và bộ lọc khuếch tán*
- T = D_I^-1 Xᵀ D_U^-1 X.
- Bộ lọc F = ½I + ¼T + ¼T², áp lên bảng S và V; số chiều d = 64.
- q_u = n_u^-½ Σ S̃_j.
- s(u,i) = q_u·Ṽ_i + b_i.
- Nếu n_u = 1 thì q_u = 0 (R10).

*3.3.2 Hàm mục tiêu và phương pháp tối ưu*
- Context leave-one-out.
- Cross-entropy trên toàn catalog, có mask.
- Ridge theo exposure (0,1); phạt bias 10⁻⁴; chiếu về bán kính 100.

*3.3.3 Thuật toán huấn luyện và suy luận*
- Adam, lr 3·10⁻⁴, 200 epoch; lưu checkpoint tốt nhất theo validation NDCG@20 (không phải dừng sớm).
- Train dùng context LOO; suy luận dùng toàn bộ lịch sử giữ lại.
- Bảng siêu tham số.

**3.4. Tính chất và chi phí (1,5 tr)**
- So **mỗi mô hình với đại diện cùng nhóm**, không đặt hai mô hình đề xuất cạnh nhau.
- GRNR với EASE:
  - tham số ≤ 129·|I| so với |I|²;
  - giải |I| hệ k×k (k ≤ 129) so với nghịch đảo một ma trận |I|×|I|.
- DFHF với LightGCN:
  - tham số 128·|I| + |I|, không phụ thuộc |U|, so với 64·(|U|+|I|);
  - chi phí mỗi epoch do softmax trên toàn catalog.
- Chỉ là phân tích lý thuyết; số đo thực tế nằm ở 4.3.3 và 4.4.3.

Tiêu chí xong Chương 3: ký hiệu khớp mã nguồn; chỉ dẫn `scripts/verify/` khi script đã chạy thành công.

### Chương 4 — section4.tex (16–19 trang)

Số thứ tự bảng/hình do LaTeX tự đánh; trong kế hoạch, tham chiếu theo tên tệp nguồn.

**4.1. Dữ liệu và tiền xử lý (3,5–4 tr)** — viết từ `configs/common.yaml`, `src/data/preprocessing.py`, `src/data/splitter.py`, `src/data/sparsity.py`, `data/processed/manifest.json` (build `bed0f5b7…`) và `audit_report.json`

*4.1.1 Nguồn dữ liệu (0,5 tr)*
- ¶ Amazon product data (SNAP): `reviews_Electronics_5.json.gz` (bản 5-core của nguồn) và `meta_Electronics.json.gz` (L07).
- ¶ Các trường được dùng: reviewerID, asin, overall, unixReviewTime; metadata gồm title, brand, categories.
- ¶ Đây là review công khai, không phải log mua hàng; rating ≥ 4 chỉ là proxy cho sở thích.

*4.1.2 Quy trình tiền xử lý (1 tr)*
- Hình sơ đồ pipeline (cần vẽ, lưu `report/image/`).
- Bảng sổ lọc:

| Bước | Còn lại | Bị loại |
|---|---|---|
| Review thô | 1.689.188 | — |
| Giữ rating ≥ 4 | 1.356.067 | 333.121 |
| Khử trùng (user, item), giữ bản mới nhất rồi rating cao nhất | 1.356.067 | 0 |
| K-core hai phía ≥ 5, hội tụ sau 13 vòng | 1.072.740 | 283.327 |

- ¶ Phải chạy lại K-core vì lọc theo rating làm nhiều user/item rơi xuống dưới 5 (riêng vòng 1 loại 213.614 tương tác).
- ¶ Đánh lại chỉ số theo thứ tự ID gốc, nên tái lập được.
- Bảng thống kê toàn bộ: 124.895 user; 44.843 item; 1.072.740 tương tác; mật độ 0,0192%; trung bình 8,59 tương tác/user (trung vị 6, lớn nhất 354); 23,9 tương tác/item. Tách riêng với B1, vốn là thống kê của train (trung bình 6,87, trung vị 5).

*4.1.3 Chia tập theo thời gian (1 tr)*
- ¶ Sắp lịch sử theo timestamp; hòa thì theo hash có seed của (user, item), rồi theo item ID.
- ¶ Chọn ngẫu nhiên (seed 42) 107.274 user có ≥ 3 tương tác. Với mỗi user: tương tác cuối vào test, tương tác áp cuối vào validation. 17.621 user chỉ có trong train.
- ¶ Tỉ lệ 80/10/10 tính trên tổng số tương tác (858.192 / 107.274 / 107.274), không phải chia theo từng user.
- ¶ Không có cặp trùng giữa các tập; 0 vi phạm thứ tự. Tuy vậy 100% timestamp nằm đúng nửa đêm: 45.431 user hòa giữa train và validation, 42.592 user hòa giữa validation và test (R6).
- ¶ 40 item không có trong train; 59 mục tiêu validation và 187 mục tiêu test vì vậy bị loại khỏi metric warm.
- Bảng tổng hợp Train / Validation / Test.

*4.1.4 Tạo các mức giảm tương tác (0,75 tr)*
- ¶ Thuật toán `create_sparse_train_set` (seed 42), chỉ áp lên train:
  1. gán mỗi cạnh một số ngẫu nhiên;
  2. lõi phủ: một cạnh cho mỗi item, sau đó một cạnh cho mỗi user chưa được phủ;
  3. thêm các cạnh còn lại theo thứ tự ngẫu nhiên cho tới đủ số cạnh.
- Bảng số cạnh: 858.192 / 643.644 / 429.096 / 214.548 tương ứng d = 1; 0,75; 0,5; 0,25. Mọi mức đều đúng số yêu cầu và giữ đủ user/item.
- ¶ Ở d25 chỉ còn trung bình ~1,72 cạnh/user (T6a, R10). Cách lấy mẫu này không ngẫu nhiên đều (R21). Mỗi d chỉ lấy mẫu một lần và dùng chung cho mọi model.

*4.1.5 Vai trò của từng phần dữ liệu (0,5 tr)*

| Thành phần | Dùng cho | Không dùng cho |
|---|---|---|
| Train giữ lại theo d | Đầu vào của mọi model; tập candidate | — |
| Train gốc | Mask khi đánh giá; định nghĩa nhóm user | Đầu vào khi d < 1 |
| Validation | Chọn checkpoint/cấu hình **và** báo cáo (R2) | — |
| Test | Không dùng (Q4, R18) | — |
| Metadata | Hiển thị trong demo (4.5) | Xếp hạng |
| Text embedding MiniLM 384 chiều | Không dùng | Xếp hạng |
| Tương tác bị chê (65.854) | [CẦN] T6e | GRNR/DFHF |

- ¶ Metadata: 888 item thiếu title (2,0%); 7.351 item thiếu brand (16,4%). Chỉ ảnh hưởng tới demo.

**4.2. Thiết lập và giao thức đánh giá (2 tr)**
- Bảng thành viên hai nhóm (mục 1), kèm cấu hình, phần cứng, số epoch. Ghi rõ DirectAU dùng encoder LightGCN; phân biệt EASE đầy đủ với EASE top-128.
- ¶ Metric NDCG@10/20 và Recall@10/20; candidate và mask giống nhau cho mọi model.
- ¶ Nguyên tắc: mỗi mô hình chỉ so với baseline cùng nhóm; không so giữa hai nhóm.
- ¶ Chọn cấu hình và checkpoint, viết riêng cho từng nhóm (R2, R3, R12, R15).
- ¶ Thống kê: bootstrap ghép cặp theo user, 10⁴ lần, một phía. Family Holm gồm 3 so sánh mỗi d, áp dụng cho cả hai nhóm (B6 cho GRNR, T4 cho DFHF). Viết p ≤ 10⁻⁴; CI chưa hiệu chỉnh đồng thời.

**4.3. Graph-Regularized Neighborhood Regression so với các mô hình giải trực tiếp (3,5 tr)**
- *4.3.1 Chất lượng xếp hạng* (RQ1): bảng B5 ở d100; ¶ C01, C02, C03.
- *4.3.2 Mức độ thưa và nhóm người dùng* (RQ2):
  - H1_closed_form_density_ndcg20, H4_closed_form_retention_ndcg20, bảng B6 cho cả 4 mức d.
  - ¶ C04 (kết quả bất lợi), C05, C06.
  - H5_closed_form_user_groups_ndcg20, ghi n của từng nhóm.
- *4.3.3 Chi phí tính toán* (RQ3): H7a_closed_form_train_time, H7c_closed_form_checkpoint_size; ¶ C07 kèm R16, R19.

**4.4. Diffusion-Filtered History Factorization so với các mô hình cần huấn luyện (4 tr)**
- *4.4.1 Chất lượng xếp hạng* (RQ1): B2a d100 chỉ gồm 4 mô hình; bảng T4 ở d100; ¶ C08 kèm R2, R3.
- *4.4.2 Mức độ thưa và nhóm người dùng* (RQ2):
  - Hình T8 (H1, H4); B2b đã lọc kèm cột % giữ lại; bảng T4 cho 4 mức d.
  - ¶ C09, C10 (nêu cả mức d50, nơi LightGCN giữ tỉ lệ tốt hơn).
  - Hình T8 H5, kèm lưu ý R10.
  - ¶ d25 không phải cold-start.
- *4.4.3 Quá trình huấn luyện và chi phí* (RQ3): B4 đã lọc, thêm cột % giảm; hình T8 H3 learning curve, H7a, H7b; ¶ C11, C12 kèm R9, R16.

**4.5. Hệ thống demo (1,5–2 tr)** (RQ4) — viết từ `app/recommender.py` và `app/streamlit_app.py`
- ¶ Luồng: fit offline → checkpoint → `Ranker` → top-K.
- Hình sơ đồ luồng (cần vẽ, lưu `report/image/`).
- ¶ Ba tab của app:
  - “Gợi ý cho khách”;
  - “Khách mới”: chấm lịch sử mới bằng `score_history`;
  - “Đánh giá mô hình”: tách “Nhóm cần huấn luyện” và “Nhóm giải trực tiếp”.
- ¶ Giải thích gợi ý: chỉ GRNR có, liệt kê các item lịch sử có đóng góp dương (C14).
- Hình chụp tab “Khách mới”.
- ¶ Giới hạn: chưa đánh giá người dùng thật; tab “Khách mới” không phải benchmark cold-start.

**4.6. Thảo luận và hạn chế (2,5 tr)**
- ¶ Trả lời RQ1–RQ3 riêng cho từng nhóm, mỗi nhóm một đoạn ngắn.
- ¶ Giải thích cạnh tranh (mục 11).
- ¶ Hạn chế theo thứ tự ảnh hưởng: R2 → R7 → một dataset → R3 → R6 → R15 → R16 → R13.

### Chương 2 — section2.tex (7–9 trang)

Mỗi phương pháp viết theo khuôn: nguyên lý → liên hệ với mô hình đề xuất cùng nhóm → điểm khác biệt → giới hạn.

- **2.1 (1,5 tr):** ma trận tương tác, phản hồi ngầm, WMF, top-K.
- **2.2 Nhóm mô hình giải trực tiếp (2,5 tr):** láng giềng item–item, SLIM, EASE, GF-CF. Đây là nền cho GRNR.
- **2.3 Nhóm mô hình cần huấn luyện (2,5 tr):** BPR/MF, FISM, NSVD/Asymmetric SVD, LightGCN, XSimGCL, DirectAU, Mult-VAE. Đây là nền cho DFHF. Tách encoder với objective.
- **2.4 (1 tr):** hai bảng so sánh, mỗi nhóm một bảng. Cột: biểu diễn user, tham số học, objective, đầu vào khi suy luận, chi phí bộ nhớ, nguồn. Kèm đoạn định vị tính mới có giới hạn cho từng mô hình.

### Chương 1 — section1.tex (3–4 trang)

- **1.1:** bối cảnh, độ thưa, bài toán.
- **1.2:** RQ1–RQ4; hai nhóm so sánh; phạm vi (validation, warm user, một seed).
- **1.3:** ba đóng góp:
  1. hai mô hình độc lập, mỗi mô hình thuộc một nhóm, đều không cần vector user;
  2. giao thức đánh giá trong từng nhóm trên 4 mức giảm tương tác, có kiểm định ghép cặp;
  3. pipeline truy nguyên và demo.
- Đoạn cuối: cấu trúc báo cáo.

### Chương 5 — section5.tex (2 trang)

- **5.1:** một đoạn cho nhóm giải trực tiếp (GRNR), một đoạn cho nhóm cần huấn luyện (DFHF), một đoạn cho demo. Dùng câu đã chốt trong sổ claim; không thêm số mới.
- **5.2:** hướng phát triển:
  1. provenance;
  2. nửa xác nhận hoặc tập test;
  3. nhiều seed;
  4. ablation;
  5. tuning baseline cân bằng;
  6. thêm dataset.
- Tóm tắt 150–250 từ, viết sau cùng.

## 10. Hình và bảng

| Vị trí | Tài nguyên | Ghi chú caption |
|---|---|---|
| 4.1 | Sơ đồ pipeline (cần vẽ); bảng sổ lọc, thống kê, chia tập, các mức d, vai trò dữ liệu; B1 | Số liệu từ manifest/audit |
| 4.3.1 | B5 (d100) | Ghi rõ nhãn biến thể EASE |
| 4.3.2 | H1_closed_form_density_ndcg20; H4_closed_form_retention_ndcg20; H5_closed_form_user_groups_ndcg20; B6 | Δ, CI, p, family, n |
| 4.3.3 | H7a_closed_form_train_time; H7c_closed_form_checkpoint_size | Phần cứng; đơn vị MiB |
| 4.4.1 | B2a d100 (đã lọc); bảng T4 d100 | Chỉ gồm DFHF và 3 baseline |
| 4.4.2 | Hình T8: H1, H4, H5 (`report/image/`); B2b đã lọc; bảng T4 | Lưu ý R10 |
| 4.4.3 | B4 đã lọc; hình T8: H3, H7a, H7b | Latency là trung bình theo user trong batch |
| 4.5 | Sơ đồ luồng và ảnh chụp tab “Khách mới” (cần tạo) | Ghi mức d |
| Không dùng | H1_density, H4_retention, H5_user_groups, H3, H7a, H7b, H8, H6 bản gộp; bốn H2 | Bản gộp đặt GRNR cạnh nhóm huấn luyện; H2 trùng byte với H1 |

Mỗi caption cần ghi: nhóm, model hoặc biến thể, split validation, seed, d, metric, cohort hoặc định nghĩa nhóm, file nguồn và script sinh. Bảng viết bằng LaTeX, không dùng ảnh chụp CSV.

## 11. Giải thích cạnh tranh (đưa vào 4.6, đều là [GT])

| Quan sát | Giải thích A | Giải thích B | Phép phân biệt |
|---|---|---|---|
| DFHF cao nhất nhóm huấn luyện ở d25 (C09, C10) | Bộ lọc khuếch tán lan tín hiệu sang item ít tương tác | Softmax toàn catalog cộng việc chọn checkpoint sớm (epoch 32) đóng vai trò regularization | Ablation với F = I; cố định số epoch |
| Khoảng cách DFHF với baseline neural | Biểu diễn bằng lịch sử phù hợp với dữ liệu thưa | Baseline chưa tối ưu (R3: DirectAU chưa hội tụ; R15) | Thêm epoch; tuning cân bằng |
| GRNR hơn EASE ở d25 nhưng thua ở d50 (C05) | Giới hạn 128 láng giềng và phạt theo support có lợi khi rất thưa, nhưng bó hẹp ở mức trung bình | Nhiễu do chỉ lấy mẫu một lần ở mỗi d (R21) | Nhiều seed lấy mẫu; đếm \|N_i\| theo d |
| GRNR ≈ EASE ở d100 (C02) | Cùng là hồi quy item–item; 128 láng giềng gần như không mất thông tin | Trùng hợp của một seed và một cohort | T5; thêm dataset |

## 12. Rà soát nội bộ (peer-review)

Người rà soát không được là người đã viết phần đó. AI tự rà soát không được gọi là phản biện độc lập. Issue ghi vào `planning/review_log.md` theo mẫu `ID | tệp:dòng | quan sát | evidence/claim ID | ảnh hưởng | hành động | P0/P1/P2 | trạng thái`.

**Vòng 1 (sau W4):**
- Thành viên A đọc Chương 3: công thức có khớp mã nguồn không; ký hiệu có thống nhất không.
- Thành viên B đọc Chương 4: mọi số có trỏ về sổ claim không; R1–R23 đã được xử lý chưa; C04 có trong thân bài không.

**Vòng 2 (sau W6), checklist:**
- [ ] **Không có so sánh trực tiếp GRNR với DFHF**, trong văn bản, bảng và hình.
- [ ] Mỗi RQ có kết quả cho cả hai nhóm; tiêu đề và tóm tắt không mạnh hơn bằng chứng.
- [ ] Mọi con số truy được về run hoặc bảng; metric, d, seed, split thống nhất.
- [ ] Công thức đúng phiên bản model đã khóa.
- [ ] Các baseline đặt tên rõ; không gộp EASE đầy đủ với top-128.
- [ ] Mô tả đúng việc lấy mẫu, timestamp trùng, coverage, loại cold, mask, candidate.
- [ ] Không còn “p = 0,0001”; family Holm 3 so sánh mỗi d cho cả hai nhóm.
- [ ] Kết quả T4/T5 có nhãn post hoc hoặc nửa xác nhận.
- [ ] Có nêu: một seed, một dataset, chọn trên validation, tuning không cân bằng.
- [ ] Không gọi phân rã đại số là giải thích nhân quả.
- [ ] Citation hỗ trợ đúng mệnh đề; có locator.
- [ ] Hình đọc được ở khổ in; hình dùng cả màu lẫn hatch.
- [ ] Thông tin tác giả và chính sách AI đã được xác nhận.

## 13. Dàn trang và build (W6–W8)

1. `main.tex`:
   - thêm `\graphicspath{{../reports/figures/}{image/}{image/trained/}}`;
   - sửa bìa, bìa lót, `pdftitle`, header/footer theo W0;
   - xóa macro của đề tài cũ.
2. Ví dụ chèn hình:

~~~tex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{H1_closed_form_density_ndcg20.png}
  \caption{Nhóm giải trực tiếp: NDCG@20 trên validation theo tỉ lệ tương tác train
  được giữ lại (seed 42, 107.215 warm user). Nguồn: reports/tables/B5\_closed\_form.csv.}
  \label{fig:closed-form-density-ndcg20}
\end{figure}
~~~

3. Đặt nhãn theo nội dung, ví dụ `fig:closed-form-…`, `fig:trained-…`, `tab:dfhf-significance`.
4. Build từ `report/`: `latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex`. Sau đó xem toàn bộ PDF; exit code 0 chưa đủ.
5. Sinh lại hình theo thứ tự `make_report.py` → `make_closed_form_report.py` → `make_trained_group_report.py` (T8), rồi cập nhật hash trong figure_inventory.

## 14. Ngân sách thời gian (ước lượng, không phải deadline)

| Bước | Buổi làm việc |
|---|---|
| W0 | 0,5 |
| W1 (gồm T8) | 2–2,5 |
| W2 | 1,5–2 (song song với W1) |
| W3 | 2 |
| W4 | 2 |
| W5 | 1,5 |
| W6–W8 | 1,5 |
| **Tổng** | **≈ 10,5–11,5** |

Nguồn hỗ trợ quy trình (L08): Kassis, T., Agarwal, V., He, Y., Patel, D., & Brueckner, A. M. (2026). Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents. arXiv:2609.00065. Nếu học phần yêu cầu, khai báo trong phần công cụ hỗ trợ; không dùng nguồn này làm bằng chứng cho kết quả.

## 15. Nhật ký triển khai (05/11/2026)

Sườn được chốt như mục 9. Đã thực hiện:

| Việc | Trạng thái | Kết quả / tệp |
|---|---|---|
| T2 kiểm kê test | Xong | 0 tệp kết quả lưu điểm test (`planning/phan_tich_bo_sung/test_exposure/`). Không chứng minh test chưa từng được xem |
| T4 kiểm định DFHF trong nhóm | Xong | `planning/phan_tich_bo_sung/T4_dfhf_significance.csv`; khai báo family ở `T4_family_declaration.md`. DFHF hơn cả 3 baseline ở cả 4 mức d, p Holm ≤ 3×10⁻⁴. Lần chạy đầu bằng `compare_val_runs.py` có chiều ngược (baseline − DFHF), không dùng |
| T6 chẩn đoán | Xong | `planning/phan_tich_bo_sung/t6_diagnostics.json`. R10: tỉ lệ warm user bậc 1 là 0% / 6,2% / 26,6% / 68,0% (d = 1 / 0,75 / 0,5 / 0,25). R11 **đã giải quyết**: 0 điểm âm trong top-20 GRNR (3.000 user, d100). R22 **đã giải quyết**: baseline không dùng hard negative. R13 vẫn chưa giải thích (cùng cấu hình ở mọi d) |
| T6f tách theo bậc user | Xong | `t6f_degree_split.json` |
| T6g/T6h mốc MostPop | Xong | `t6g_mostpop.json`, `T6h_vs_mostpop.csv` (xem R24) |
| T8 hình nhóm huấn luyện | Xong | `scripts/make_trained_group_report.py` → `report/image/` (10 hình) |
| T1, T3, T5 | Chưa làm | T1 cần máy cũ/Kaggle; T3, T5 không chặn bản thảo |
| W2 tài liệu | Xong cho bản thảo | 17 nguồn trong `section/ref.tex`, metadata kiểm qua arXiv API và Crossref |
| W3–W5 viết chương | Bản thảo đầu | `section/section1–5.tex` |
| W6 dàn trang | Một phần | `main.tex`: đề tài mới, graphicspath, bỏ macro cũ; thông tin học phần và bảng phân công để `[CẦN XÁC NHẬN]` |
| W8 build | Xong | 46 trang, không lỗi, 2 hộp tràn lề < 6pt |
| W7 rà soát nội bộ | Chưa làm | Cần thành viên nhóm theo mục 12 |

**Phát hiện mới R24 (P0).** Mốc MostPop (xếp theo số tương tác trong train giữ lại) đạt NDCG@20 ≈ 0,018 ở mọi d. Ở d25 **không model nào vượt MostPop**: DFHF ngang MostPop (Δ −0,00005, KTC [−0,00029; 0,00018]), mọi model khác thấp hơn rõ. Ở d50, GRNR thấp hơn MostPop một chút (Δ −0,00092). GF-CF chỉ ngang MostPop ở d100. Hệ quả: ưu thế của DFHF ở d25 chủ yếu là do rơi về item bias cho 68% user bậc 1. Claim C09/C10 đã được viết lại trong `section4.tex` (mục Thảo luận) và `section5.tex`. MostPop là mốc tham chiếu chung, không thuộc nhóm nào, nên không vi phạm quy tắc “không so GRNR với DFHF”.

**Còn chờ tác giả:** Q1 (học phần), Q2 (tác giả, MSSV trùng 23010523, bảng phân công), Q3 (giới hạn trang; bản hiện tại 46 trang tính cả bìa và mục lục), Q6.
