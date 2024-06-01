# Denial of Service with Block Gas Limit

## Mô tả

Mỗi block trong Ethereum sẽ có một giới hạn gas nhất định #footnote[Tại thời điểm tháng 5 năm 2024 thì giới hạn này là 30 triệu gas @a2023_gas-and-fees.] Lỗ hổng này xảy ra khi lượng gas mà smart contract tiêu thụ vượt quá giới hạn gas của block.

Các thao tác tiêu thụ nhiều gas chẳng hạn như chỉnh sửa mảng có kích thước tăng theo thời gian có thể gây ra từ chối dịch vụ.

## Cách khắc phục

Thay vì chỉnh sửa mảng trong một block, có thể chia việc chỉnh sửa này ra nhiều block. Tổng quát hơn, cần xem xét lượng gas sử dụng trong smart contract một cách cẩn thận.
