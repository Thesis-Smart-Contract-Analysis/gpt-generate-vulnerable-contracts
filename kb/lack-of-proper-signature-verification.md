# Lack of Proper Signature Verification

## Mô tả

Xảy ra khi smart contract không thực hiện kiểm tra tính hợp lệ của chữ ký khi thực hiện những thao tác nhạy cảm. Kẻ tấn công có thể lợi dụng điều này để vượt qua xác thực nhằm thực hiện những hành vi không được phép.

## Cách khắc phục

Không sử dụng các cách kiểm tra tính hợp lệ của chữ ký mà không thông qua hàm `ecrecover`.
