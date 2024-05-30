# Immutable Bugs 

## Mô tả

Smart contract sau khi được triển khai lên mạng blockchain thì không thể được chỉnh sửa, kể cả khi có lỗi. Các lỗi này có thể bị khai thác bởi kẻ tấn công và thiệt hại gây ra là không thể khôi phục #footnote[The DAO là ngoại lệ duy nhất].

## Cách khắc phục

Có thể sử dụng các mẫu thiết kế giúp "nâng cấp" smart contract chẳng hạn như mẫu Proxy #footnote[@proxy-pattern[Phụ lục]] @transparent-proxy-pattern.

