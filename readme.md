# Scenario 2

Kế hoạch thực hiện:
- Chuyển lỗ hổng thành file markdown
- Gom tất cả các lỗ hổng vào 1 context (KB)
- Lần lượt lặp qua tên của các lỗ hổng (theo thứ tự ngẫu nhiên) và query. Nhớ cho câu query vào output json
- Các giai đoạn thực hiện:
    1. 10 lỗ hổng - 10 lần (có những lần hỏi những lỗ hổng ngoài KB) => đánh giá xem có thể biết được pattern lỗ hổng của Solidity hay không
    2. 20 lỗ hổng - 10 lần (tiêu chí và đánh giá tương tự)
    3. all - 10 lần
- Không dùng KB và lặp lại giai đoạn 1 và 3 (đánh giá độ chính xác bằng tay) => so sánh được hiệu quả của KB