# gunny-game-
Hello, this is my first project after 2 weeks learning IT and Python foundations. I created a game called "Gunny" with the assistance of Copilot, using Python and README file.

# Game bắn gà trong chuồng 
Game bắn gà đơn giản được phát triển bằng Python và thư viện Pygame

## Ý tưởng game
- Bắn gà trong chuồng để giết thịt
- Gà càng béo, điểm càng cao
- Thắng khi bắn hết gà trong chuồng
- Thua khi để 5 con gà xổng chuồng
- Có 50 cấp độ với độ khó tăng dần

## Cách cài đặt

1. Đảm bảo bạn đã cài đặt Python (phiên bản 3.6 trở lên)
2. Cài đặt thư viện pygame bằng lệnh:


  pip install pygame

## Cách chơi

1. Chạy file `main.py` để bắt đầu game
2. Di chuyển chuột để nhắm mục tiêu
3. Nhấn chuột trái để bắn
4. Bắn trúng gà để ghi điểm (gà càng béo điểm càng cao)
5. Cẩn thận đừng để gà xổng chuồng quá 5 con
6. Hoàn thành 50 cấp độ để chiến thắng trò chơi

## Các tính năng trong game

- Gà có kích thước khác nhau (càng lớn càng béo, điểm càng cao)
- Gà béo di chuyển chậm hơn gà gầy
- Gà có thể xổng chuồng nếu chạy ra khỏi màn hình
- Đạn có giới hạn, cần phải sử dụng hợp lý
- Vật phẩm rơi ra khi bắn trúng gà:
  - Đạn bổ sung
  - Tăng tốc độ bắn

## Hướng dẫn cho người mới học lập trình

Game này được thiết kế để người mới học lập trình có thể hiểu và mở rộng. Các khái niệm cơ bản được sử dụng:

- Lập trình hướng đối tượng (OOP) với các lớp như Gun, Chicken, Bullet
- Xử lý sự kiện chuột và bàn phím
- Vòng lặp game và cập nhật trạng thái
- Phát hiện va chạm giữa các đối tượng
- Quản lý cấp độ và điểm số

## Mở rộng

Bạn có thể mở rộng game bằng cách:
- Thêm hiệu ứng âm thanh
- Thêm nhiều loại gà với đặc tính khác nhau
- Thêm nhiều loại vũ khí
- Thêm boss ở các cấp độ đặc biệt
- Thêm hệ thống lưu điểm cao
