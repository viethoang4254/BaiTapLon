# Trình thu thập tin tức VnExpress

## Tổng quan

Dự án này là một trình thu thập dữ liệu web được viết bằng Python, được thiết kế để thu thập các bài báo từ mục "Kinh doanh Quốc tế" của VnExpress (https://vnexpress.net/kinh-doanh/quoc-te). Trình thu thập sẽ lấy tiêu đề bài báo, tóm tắt, nội dung và hình ảnh, sau đó lưu dữ liệu vào file CSV. Dự án cũng bao gồm chức năng lập lịch để chạy tự động hàng ngày vào lúc 06:00 sáng.

## Tính năng

- **Thu thập dữ liệu web**: Thu thập dữ liệu từ nhiều trang của mục Kinh doanh Quốc tế trên VnExpress.
- **Trích xuất dữ liệu**: Lấy tiêu đề, tóm tắt, nội dung đầy đủ và URL hình ảnh của bài báo.
- **Lưu trữ dữ liệu**: Lưu dữ liệu thu thập được vào file CSV (`tech_news_data.csv`) với mã hóa UTF-8.
- **Lập lịch**: Tự động chạy trình thu thập hàng ngày vào lúc 06:00 sáng bằng thư viện `schedule`.
- **Xử lý lỗi**: Xử lý các lỗi HTTP, các yếu tố bị thiếu và gián đoạn từ người dùng một cách nhẹ nhàng.

## Yêu cầu

Để chạy trình thu thập, bạn cần Python 3.x và các thư viện sau:

- `requests`: Để gửi yêu cầu HTTP.
- `beautifulsoup4`: Để phân tích nội dung HTML.
- `pandas`: Để xử lý và lưu dữ liệu vào file CSV.
- `schedule`: Để lập lịch chạy hàng ngày.

Cài đặt các thư viện cần thiết bằng lệnh:

```bash
pip install requests beautifulsoup4 pandas schedule
```

## Cấu trúc dự án

- **Tệp chính**: `BaiTapLon.py` (hoặc mã Python được cung cấp) chứa logic thu thập dữ liệu và lập lịch.
- **Tệp đầu ra**: `tech_news_data.csv` lưu trữ dữ liệu đã thu thập (mặc định lưu tại `E:\TDH\BaiTapLonRPA\`).

## Cách hoạt động

1. **Quy trình thu thập**:

   - Script gửi yêu cầu HTTP đến mục Kinh doanh Quốc tế của VnExpress, bắt đầu từ trang 1.
   - Sử dụng BeautifulSoup để phân tích HTML và lấy liên kết bài báo từ các thẻ `<h2 class="title-news">`.
   - Với mỗi liên kết bài báo, script trích xuất:
     - **Tiêu đề**: Từ thẻ `<h1 class="title-detail">`.
     - **Tóm tắt**: Từ thẻ `<p class="description">`.
     - **Nội dung**: Từ tất cả các thẻ `<p class="Normal">` trong thẻ `<article class="fck_detail">`.
     - **Hình ảnh**: Thuộc tính `src` của thẻ `<img>` đầu tiên trong nội dung bài báo.
   - Dữ liệu được lưu vào một DataFrame của pandas và ghi vào file CSV sau khi xử lý xong mỗi trang.

2. **Lập lịch**:

   - Thư viện `schedule` được sử dụng để chạy hàm `crawl_vnexpress` hàng ngày vào lúc 06:00 sáng.
   - Script chạy vô thời hạn, kiểm tra các tác vụ đã lập lịch mỗi giây.

3. **Xử lý lỗi**:
   - Bỏ qua các bài báo có yếu tố bị thiếu hoặc yêu cầu thất bại.
   - Dừng thu thập khi không còn bài báo nào hoặc nếu yêu cầu HTTP thất bại.
   - Xử lý gián đoạn từ người dùng (ví dụ: Ctrl+C) một cách nhẹ nhàng.

## Hướng dẫn sử dụng

1. **Cài đặt**:

   - Đảm bảo tất cả các thư viện cần thiết đã được cài đặt.
   - Cập nhật đường dẫn tệp đầu ra trong script nếu cần (mặc định: `E:\TDH\BaiTapLonRPA\tech_news_data.csv`).

2. **Chạy script**:

   ```bash
   python BaiTapLon.py
   ```

   - Script sẽ bắt đầu thu thập ngay lập tức và in tiến độ lên console.
   - Script cũng sẽ lập lịch chạy hàng ngày vào 06:00 sángynu

3. **Dừng script**:
   - Nhấn `Ctrl+C` để dừng chương trình. Chương trình sẽ thoát một cách nhẹ nhàng.

## Đầu ra

- **Tệp CSV**: `tech_news_data.csv` chứa các cột sau:
  - `title`: Tiêu đề bài báo.
  - `summary`: Tóm tắt bài báo.
  - `content`: Nội dung đầy đủ của bài báo.
  - `image`: URL của hình ảnh chính trong bài báo.
- Tệp này sẽ bị ghi đè bằng dữ liệu mới sau khi mỗi trang được thu thập.

## Lưu ý

- **Đường dẫn tệp**: Đảm bảo thư mục đầu ra (`E:\TDH\BaiTapLonRPA\`) tồn tại và có quyền ghi.
- **Tần suất yêu cầu**: Script tạm dừng 1 giây giữa các trang để tránh quá tải máy chủ.
- **Mã hóa**: File CSV sử dụng mã hóa `utf-8-sig` để hỗ trợ tiếng Việt.

## Giải quyết sự cố

- **Lỗi thiếu thư viện**: Cài đặt các thư viện cần thiết bằng lệnh `pip install` như hướng dẫn ở trên.
- **Lỗi truy cập trang web**: Kiểm tra kết nối internet hoặc thử lại sau, vì máy chủ VnExpress có thể tạm thời không phản hồi.
- **Lỗi đường dẫn tệp**: Đảm bảo đường dẫn đến `tech_news_data.csv` hợp lệ và ổ đĩa có đủ dung lượng.
