# Nhật ký tài liệu cho kế hoạch báo cáo

Ngày truy cập: 05/11/2026. Loại công việc: tìm kiếm sơ bộ có mục tiêu và kiểm tra record gốc. Không phải systematic review, chưa sàng lọc đầy đủ và chưa đánh giá full text toàn bộ.

## 1. Nguồn đã mở

Trạng thái “record đã mở” chỉ có nghĩa định vị metadata/abstract. Các claim công thức, khác biệt thuật toán và tính mới còn cần full text, locator và xác nhận của tác giả. Không có người xác minh là con người được tự điền.

| ID | Nguồn | Nơi dùng dự kiến | Trạng thái |
|---|---|---|---|
| L01 | He và cộng sự, LightGCN: Simplifying and Powering Graph Convolution Network for Recommendation, 2020. [arXiv record](https://arxiv.org/abs/2002.02126) | Truyền lan user–item và baseline | Record đã mở; chưa trích xuất full text |
| L02 | Yu và cộng sự, XSimGCL: Towards Extremely Simple Graph Contrastive Learning for Recommendation. [arXiv record](https://arxiv.org/abs/2209.02544) | Nhóm contrastive; phân biệt preprint 2022 và bản xuất bản | Record có sửa năm 2023; cần kiểm tra metadata publisher trước bibliography cuối |
| L03 | Wang và cộng sự, Towards Representation Alignment and Uniformity in Collaborative Filtering, KDD 2022. [Record](https://arxiv.org/abs/2206.12811), DOI [10.1145/3534678.3539253](https://doi.org/10.1145/3534678.3539253) | DirectAU; phân biệt objective với encoder | Record đã mở; full text còn thiếu |
| L04 | Steck, Embarrassingly Shallow Autoencoders for Sparse Data, WWW 2019. [Record](https://arxiv.org/abs/1905.03375), DOI [10.1145/3308558.3313710](https://doi.org/10.1145/3308558.3313710) | EASE và nền tảng hồi quy item–item | Record đã mở; cần đọc phép suy ra closed-form |
| L05 | Shen và cộng sự, How Powerful is Graph Convolution for Recommendation?, 2021. [Record](https://arxiv.org/abs/2108.07567) | GF-CF và lọc tín hiệu đồ thị | Record đã mở; cần đối chiếu chuẩn hóa, SVD và code tác giả |
| L06 | Kabbur, Ning, Karypis, FISM: Factored Item Similarity Models for Top-N Recommender Systems, KDD 2013. [Record của trường tác giả](https://ohiostate.elsevierpure.com/en/publications/fism-factored-item-similarity-models-for-top-n-recommender-system/), DOI [10.1145/2487575.2487589](https://doi.org/10.1145/2487575.2487589) | Đối chiếu biểu diễn user bằng lịch sử, source/target và target exclusion của DFHF | Metadata/abstract đã mở; chưa đủ để xác lập tính mới |
| L07 | [Amazon product data, SNAP/Julian McAuley](https://snap.stanford.edu/data/amazon/productGraph/) | Phiên bản dữ liệu, bản chất review và metadata | Trang gốc đã mở; dùng đúng URL Electronics trong common.yaml |
| L08 | Kassis, T.; Agarwal, V.; He, Y.; Patel, D.; Brueckner, A. M. (2026). Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents. [Record](https://arxiv.org/abs/2609.00065), DOI [10.48550/arXiv.2609.00065](https://doi.org/10.48550/arXiv.2609.00065) | Nguồn hỗ trợ quy trình ideation, appraisal, review và writing | Record đã mở; bản sửa hiện ghi 02/09/2026, không có journal reference trong record đã xem |

L08 được ghi nhận trong kế hoạch này vì các skill hỗ trợ đáng kể quy trình. Không dùng L08 làm bằng chứng cho chất lượng GRNR/DFHF. ref.tex hiện chưa bị sửa.

## 2. Nhật ký truy vấn đã thực hiện

Công cụ: web search và mở trực tiếp record, không có export database đầy đủ. Không coi số kết quả hiển thị của web là tổng số record trong database. Các truy vấn dưới đây là nguyên văn; chưa có số sàng lọc hoặc số bài được đưa vào một review hoàn chỉnh.

| ID | Truy vấn hoặc thao tác | Kết quả xử lý |
|---|---|---|
| Q01 | Mở trực tiếp record L01, L02, L08 | Dùng định vị metadata/abstract |
| Q02 | "Towards Representation Alignment and Uniformity in Collaborative Filtering" arxiv | Định vị L03; sau đó mở record gốc |
| Q03 | "Embarrassingly Shallow Autoencoders for Sparse Data" arxiv | Định vị L04; sau đó mở record gốc |
| Q04 | "How Powerful is Graph Convolution for Recommendation" arxiv | Định vị L05; sau đó mở record gốc |
| Q05 | site.cseweb.ucsd.edu jmcauley datasets amazon Electronics 2014 | Kết quả nhiều phiên bản; dùng URL SNAP trong config để mở L07 |
| Q06 | "FISM" "Factored Item Similarity Models" Kabbur 2013 | Định vị L06; mở record trường tác giả |
| Q07 | "On the Bias of Offline Evaluation Methods for Recommender Systems" 2020 | Chưa chọn được nguồn đủ kiểm tra cho báo cáo; cần tìm tiếp |
| Q08 | "Bayesian Personalized Ranking from Implicit Feedback" arxiv 2009 | Có nguồn ứng viên BPR/UAI và preprint; chưa mở full report, chưa đưa vào danh sách nguồn đã đọc |

Một URL arXiv dự kiến cho DirectAU dẫn tới bài không cùng tiêu đề đã bị loại; record đúng L03 được tìm lại bằng tiêu đề. Không sử dụng identifier dự đoán làm citation.

Giới hạn: chỉ tìm bài nền và bài liên quan trực tiếp, chưa tìm phủ các nghiên cứu đến 05/11/2026, chưa citation chaining, chưa tìm đầy đủ negative results, chưa kiểm tra corrections/retractions của mọi bài và chưa quyết định novelty. Không tải nội dung project chưa công bố lên truy vấn web.

## 3. Kế hoạch tìm tiếp khi viết Chương 2

Chạy trên nguồn bổ sung phù hợp như ACM Digital Library/IEEE Xplore, arXiv và OpenAlex hoặc Semantic Scholar; lưu truy vấn thực tế theo cú pháp mỗi dịch vụ và ghi ngày/số lượng/phạm vi. Bảng này là query dự kiến, chưa phải tìm kiếm đã chạy.

| Chủ đề | Query khái niệm dự kiến | Câu hỏi trích xuất |
|---|---|---|
| Lịch sử và phân rã item | ("history-based" OR "factored item similarity" OR FISM) AND recommendation | Thành phần DFHF nào kế thừa, thành phần nào cần so sánh mới? |
| Ridge cục bộ và đồ thị | ("item-item" OR "neighborhood") AND ("ridge" OR "graph regularization") AND recommendation | Mối liên hệ với GRNR; prior/support/boundary/target exclusion đã có ở đâu? |
| Đánh giá thời gian | ("temporal split" OR "timestamp ties" OR "data leakage") AND recommender evaluation | Giao thức hiện tại hỗ trợ loại claim nào? |
| Sai lệch offline | ("offline evaluation" AND recommendation) AND (bias OR selection OR "candidate sampling") | Bias do dữ liệu quan sát, filtering và candidate có thể ảnh hưởng thế nào? |
| Thống kê so sánh | ("recommender systems" AND "statistical significance") OR ("paired bootstrap" AND ranking) | Đơn vị bootstrap, dependence, multiple comparisons và giới hạn một seed |

Tiêu chí đưa vào: bài gốc hoặc tài liệu phương pháp đáng tin cậy có liên hệ trực tiếp; mô tả được dữ liệu/protocol; ưu tiên full text hợp pháp. Không loại chỉ vì citation thấp hay kết quả trái với hướng đề xuất. Gộp preprint/journal của cùng công trình khi tổng hợp, giữ dấu vết phiên bản.

Bảng trích xuất sẽ gồm: source ID, tiêu đề/tác giả/năm/identifier, loại nguồn, phiên bản, chủ đề, objective, biểu diễn user/item, dữ liệu/giao thức, kết quả liên quan, hạn chế, trang/phương trình, quan hệ với claim, trạng thái đọc, người xác minh và ngày. Metadata đúng chưa đồng nghĩa claim được nguồn hỗ trợ.
