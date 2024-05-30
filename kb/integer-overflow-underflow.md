# Integer Overflow/Underflow <integer-overflow-underflow>

## Mô tả

Các kiểu dữ liệu lưu trữ số nguyên (bao gồm có dấu và không dấu) ở trong Solidity có kích thước là các lũy thừa cơ số 2 từ 8 đến 256. Khi thực hiện tính toán, dữ liệu có thể mang giá trị vượt ra ngoài phạm vi lưu trữ của kiểu dữ liệu. Vấn đề này được gọi là tràn số (overflow/underflow).

Trong ví dụ dưới, nếu ta gọi hàm `run` với `input` là `2` thì giá trị của biến `count` sẽ là $1 -2 = -1 = 2^{256} - 1$ (kiểu `uint` thực chất là `uint256`).

```sol
//Single transaction overflow
//Post-transaction effect: overflow escapes to publicly-readable storage

pragma solidity ^0.4.19;

contract IntegerOverflowMinimal {
  
    uint public count = 1;

    function run(uint256 input) public {
        count -= input;
    }
    
}
```

## Cách khắc phục

Cẩn thận khi thực hiện các tính toán trên số nguyên bằng cách so sánh các toán hạng trước khi thực hiện toán tử.

Sử dụng các thư viện chẳng hạn như SafeMath của OpenZeppelin @openzeppelin-math. Về bản chất, thư viện này sử dụng các câu lệnh `assert` hoặc `require` để đảm bảo các thao tác tính toán sẽ không gây ra tràn số.

Ngoài ra, kể từ phiên bản 0.8.0 @solidity-v0.8.0-breaking-changes của Solidity, lỗi tràn số được tự động phát hiện và giao dịch sẽ được hoàn trả trước khi thao tác tính toán được thực thi.



