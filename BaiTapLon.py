import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import schedule

def business_vnexpress():
    print("Bắt đầu thu thập dữ liệu từ VnExpress")
    
    # Tạo danh sách để lưu dữ liệu
    data = []
    
    page = 1
    while True:
        # 1. Gửi HTTP request đến trang web
        if page == 1:
            response = requests.get("https://vnexpress.net/kinh-doanh/quoc-te")
        else:
            response = requests.get(f"https://vnexpress.net/kinh-doanh/quoc-te-p{page}")
        
        # 2. Kiểm tra nếu request thành công
        if response.status_code == 200:
            print(f"Đã truy cập trang {page}")
            # 3. Sử dụng BeautifulSoup để phân tích HTML
            soup = BeautifulSoup(response.content, "html.parser")
        
            # 4. Tìm kiếm các bài báo có thẻ h2 và class="title-news"
            news = soup.find_all('h2', class_='title-news')
            if not news:
                print("Đã lấy tất cả bài viết.")
                break
        
            # Lấy link của tất cả các bài viết
            links = []
            for link in news:
                try:
                    url = link.find('a').attrs["href"]
                    links.append(url)
                except:
                    continue
            
            print(f"Tìm thấy {len(links)} bài viết trên trang {page}")
        
            # 5. Đối với mỗi bài báo, lấy tiêu đề, mô tả, hình ảnh, nội dung bài viết
            for link in links:
                try:
                    i_news = requests.get(link)
                    i_soup = BeautifulSoup(i_news.content, "html.parser")
                
                    try:
                        title = i_soup.find("h1", class_="title-detail").text
                    except:
                        title = ""
                    
                    try:
                        summary = i_soup.find("p", class_="description").get_text(strip=True)
                    except:
                        summary = ""
                    
                    body = i_soup.find("article", class_="fck_detail")
                
                    try:
                        # Lấy nội dung từ tất cả các thẻ <p class="Normal">
                        paragraphs = body.find_all("p", class_="Normal") if body else []
                        content = " ".join(p.get_text(strip=True) for p in paragraphs)
                    except:
                        content = " "

                    try:
                        image = body.find("img").attrs["src"]
                    except:
                        image = " "
                
                    item = [title, summary, content, image]
                    data.append(item)
                    print(f"Đã thu thập bài viết: {title}")
                except Exception as e:
                    print(f"Lỗi khi lấy bài viết {link}: {e}")
                    continue
        
            # 6. Lưu dữ liệu vào file CSV
            if data:
                df = pd.DataFrame(data, columns=["title", "summary", "content", "image"])
                # Nếu là trang đầu tiên, ghi mới file; nếu không, nối thêm
                mode = 'w' if page == 1 else 'a'
                header = True if page == 1 else False
                df.to_csv(r"E:\TDH\BaiTapLonRPA\tech_news_data.csv", index=False, encoding='utf-8-sig', mode=mode, header=header)
                print(f"Đã lưu {len(data)} bài viết từ trang {page} vào file tech_news_data.csv")
                
            page += 1
            time.sleep(1)
        else:
            print(f"Không thể truy cập trang {page}, mã lỗi: {response.status_code}")
            break

# Lập lịch chạy
schedule.every().day.at("06:00").do(business_vnexpress)
print("Đã lên lịch chạy hàng ngày lúc 06:00 sáng")

try:
    business_vnexpress()
except KeyboardInterrupt:
    print("Chương trình bị gián đoạn bởi người dùng.")

# Chạy scheduler
if __name__ == "__main__":
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Chương trình đã bị dừng bởi người dùng.")