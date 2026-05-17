# 23020272_NguyenMinhHieu_CaroAI_DeGiuaKi
**Giới thiệu**

Đây là project xây dựng trò chơi Cờ Caro sử dụng trí tuệ nhân tạo (AI) bằng ngôn ngữ Python và thư viện pygame.

**Chương trình hỗ trợ:**

- Người chơi đấu với AI
- Người chơi đấu với người chơi
- Thuật toán Minimax
- Thuật toán Alpha-Beta Pruning
- Chọn độ sâu tìm kiếm của AI
- Undo nước đi
- Replay ván mới
- Hiển thị số trạng thái đã xét

Game được xây dựng với giao diện đồ họa trực quan, dễ sử dụng và có khả năng mô phỏng hoạt động của các thuật toán tìm kiếm đối kháng trong trí tuệ nhân tạo.

**Mục tiêu project**

Mục tiêu của project là:

- Tìm hiểu cách xây dựng AI cho trò chơi hai người
- Cài đặt thuật toán Minimax
- Cải tiến bằng Alpha-Beta pruning
- So sánh hiệu quả giữa hai thuật toán
- Đánh giá ảnh hưởng của độ sâu tìm kiếm đến chất lượng nước đi và thời gian chạy
**Luật chơi**
Bàn cờ có kích thước 15x15
Người chơi sử dụng quân X
Máy tính sử dụng quân O
Hai bên đánh luân phiên
Không được đánh vào ô đã có quân
Người thắng là người có 4 quân liên tiếp theo:
hàng ngang
hàng dọc
đường chéo
Nếu bàn cờ đầy mà không có người thắng thì kết quả là hòa

(Chèn ảnh giao diện bàn cờ lúc bắt đầu trận đấu ở chế độ AI Mode)

Công nghệ sử dụng
Python 3
pygame
Cấu trúc chương trình
Project/
│
├── main.py
├── README.md
├── requirements.txt
└── report.pdf

Trong đó:

main.py: chứa toàn bộ source code chương trình
README.md: hướng dẫn cài đặt và chạy chương trình
requirements.txt: danh sách thư viện cần cài đặt
report.pdf: báo cáo phân tích và thực nghiệm
Chức năng chương trình
1. Chế độ chơi

Chương trình hỗ trợ:

Người chơi vs AI
Người chơi vs Người chơi (PvP)

Người dùng có thể chuyển đổi chế độ trực tiếp trên giao diện.

(Chèn ảnh giao diện đang chọn AI Mode và P v P)

2. Chọn độ khó AI

AI hỗ trợ 3 mức độ:

Easy (Depth = 1)
Medium (Depth = 2)
Hard (Depth = 3)

Độ sâu tìm kiếm càng lớn:

AI đánh càng tốt
thời gian xử lý càng lâu
số trạng thái phải duyệt càng nhiều

(Chèn ảnh giao diện đang chọn Hard mode)

3. Thuật toán Minimax

Thuật toán Minimax được sử dụng để mô phỏng các nước đi trong tương lai.

Nguyên lý hoạt động:

AI đóng vai trò MAX
Người chơi đóng vai trò MIN
MAX cố gắng chọn giá trị lớn nhất
MIN cố gắng chọn giá trị nhỏ nhất

Thuật toán sẽ:

Sinh các nước đi hợp lệ
Duyệt cây trạng thái
Đánh giá các trạng thái lá
Chọn nước đi tốt nhất

Trong chương trình:

Hàm minimax() được sử dụng để cài đặt thuật toán
Có sử dụng giới hạn độ sâu tìm kiếm

(Chèn ảnh trạng thái giữa trận đấu khi AI sử dụng Minimax)

Thuật toán Alpha-Beta Pruning

Alpha-Beta là phiên bản cải tiến của Minimax nhằm giảm số trạng thái cần duyệt.

Ý nghĩa:

alpha: giá trị tốt nhất của MAX
beta: giá trị tốt nhất của MIN

Nếu:

beta <= alpha

thì nhánh hiện tại sẽ bị cắt bỏ.

Ưu điểm:

giảm số node phải xét
tăng tốc độ phản hồi
cho kết quả giống Minimax nhưng hiệu quả hơn

Trong chương trình:

Hàm alphabeta() được sử dụng để cài đặt thuật toán
Có sử dụng cắt nhánh Alpha-Beta

(Chèn ảnh trạng thái AI đang sử dụng Alpha-Beta)

Hàm đánh giá trạng thái

Chương trình sử dụng hàm heuristic để đánh giá trạng thái bàn cờ khi chưa đạt trạng thái kết thúc.

Các tiêu chí đánh giá:

AI có 3 quân liên tiếp → cộng điểm lớn
Người chơi có 3 quân liên tiếp → trừ điểm lớn
AI có 2 quân liên tiếp → cộng điểm vừa
Người chơi có 2 quân liên tiếp → trừ điểm vừa

Ví dụ trong code:

if ai_c == 3 and em_c == 1:
    score += 500

elif pl_c == 3 and em_c == 1:
    score -= 900

Ý nghĩa:

AI ưu tiên tạo thế thắng
AI ưu tiên chặn đối thủ trước khi thua

(Chèn ảnh tình huống người chơi sắp thắng và AI thực hiện chặn)

Sinh nước đi hợp lệ

Chương trình chỉ xét các ô:

đang trống
nằm gần các quân đã đánh

Điều này giúp:

giảm không gian tìm kiếm
tăng tốc thuật toán

Hàm:

get_ordered_moves()

được sử dụng để:

tìm nước đi hợp lệ
sắp xếp nước đi ưu tiên
Kiểm tra trạng thái thắng

Chương trình kiểm tra thắng theo:

hàng ngang
hàng dọc
chéo chính
chéo phụ

Hàm:

check_win()

được sử dụng để kiểm tra trạng thái thắng/thua.

(Chèn ảnh một ván thắng theo đường chéo)

Undo và Replay

Chương trình hỗ trợ:

Undo nước đi
Replay để chơi ván mới

Undo:

PvP: hoàn tác 1 lượt
AI Mode: hoàn tác cả lượt người và AI

(Chèn ảnh sau khi sử dụng Undo)

Kết quả thực nghiệm

Chương trình cho phép so sánh:

Minimax
Alpha-Beta

Thông qua:

số trạng thái đã xét
chất lượng nước đi
thời gian chạy

Kết quả cho thấy:

Alpha-Beta xét ít trạng thái hơn
tốc độ xử lý nhanh hơn
vẫn chọn được nước đi tương đương Minimax

(Chèn ảnh log hiển thị số trạng thái đã xét)

Hướng phát triển

Một số hướng cải tiến trong tương lai:

Tăng độ sâu tìm kiếm
Tối ưu hàm đánh giá
Move Ordering nâng cao
Iterative Deepening
Transposition Table
Zobrist Hashing
AI vs AI
Lưu lịch sử trận đấu
Thêm âm thanh và hiệu ứng
Hướng dẫn cài đặt
1. Cài Python

Cài đặt Python 3.x:
https://www.python.org/downloads/

2. Cài thư viện

Mở terminal và chạy:

pip install -r requirements.txt
Hướng dẫn chạy chương trình

Chạy file:

python main.py
Tài liệu tham khảo
https://github.com/husus/gomokuAI-py
https://github.com/MonHauVD/Caro_AI
Giáo trình Trí tuệ nhân tạo
Tài liệu về Minimax và Alpha-Beta Pruning
Tác giả

Họ và tên: Nguyễn Minh Hiếu

MSSV: xxxxxxxxx

Môn học: Trí tuệ nhân tạo / Game AI
