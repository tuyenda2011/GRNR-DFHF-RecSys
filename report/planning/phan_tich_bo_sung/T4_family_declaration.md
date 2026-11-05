# T4 — Khai báo family trước khi chạy (05/11/2026)

- Mục đích: kiểm định DFHF với các baseline cùng nhóm cần huấn luyện (R14, R23).
- Family: mỗi mức d ∈ {1,0; 0,75; 0,5; 0,25} là một family gồm 3 so sánh: DFHF − LightGCN, DFHF − XSimGCL, DFHF − DirectAU.
- Chỉ số chính: NDCG@20. Kiểm định: bootstrap ghép cặp theo user, 10.000 lần, seed 42, một phía (DFHF > baseline). Hiệu chỉnh Holm trong từng family.
- Tình trạng: **post hoc**. Điểm trung bình của từng model ở mọi d đã được xem trước khi khai báo, nên kết quả chỉ mang tính khám phá.
- Dữ liệu: validation, toàn cohort warm (`--half all`).

Ghi chú thực hiện: lần chạy đầu bằng `compare_val_runs.py` cho hiệu theo chiều baseline − DFHF (kiểm định baseline > DFHF), nên không dùng; các tệp `dfhf_d*.json` chỉ giữ để tham khảo (có thêm coverage@20 và độ phổ biến). Kết quả chính được tính bằng `t4_dfhf_significance.py`, cùng hàm `paired_bootstrap`/`holm_adjust` mà B6 dùng, family không đổi so với khai báo ở trên.
