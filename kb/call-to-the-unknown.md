# Call to the Unknown

## Mô tả

Lỗ hổng này xảy ra khi hàm fallback của một smart contract được thực thi theo một cách không mong đợi khi smart contract gọi hàm với signature không tồn tại hoặc gửi ETH.

Kẻ tấn công có thể cài đặt mã độc ở trong hàm fallback chẳng hạn như gọi đệ quy để gây ra lỗ hổng re-entrancy (@re-entrancy) hoặc cố tình hoàn trả giao dịch để làm smart contract rơi vào trạng thái từ chối dịch vụ.

Ví dụ:

```sol
pragma solidity 0.6.12;

contract CallToTheUnknown {

  function call(address _addr) {
    (bool success, bytes memory data) = _addr.call{
    	value: msg.value,
    	gas: 5000
    }(abi.encodeWithSignature("foo(string,uint256)", "call foo", 123));
  }
  
}
```

Nếu smart contract ở địa chỉ `_addr` không có hàm với signature là `"foo(string,uint256)"` thì hàm fallback của nó sẽ được gọi. 

Việc gọi hàm thông qua thực thể của smart contract cũng xảy ra vấn đề tương tự nếu giao diện của smart contract được định nghĩa trong mã nguồn không khớp với smart contract đã được triển khai trên blockchain.

Ví dụ:

```sol
contract Alice {
  
    function ping(uint) returns (uint256);
    
}

contract Bob {
  
    function pong(Alice a) {
        a.ping(42);
    }
    
}
```

Trong ví dụ trên, nếu signature của hàm `ping` không được khai báo đúng (chẳng hạn như sai kiểu dữ liệu của tham số) thì có thể dẫn đến việc thực thi hàm fallback một cách không mong muốn.

Các hàm chuyển ETH chẳng hạn như `send` hoặc `transfer` cũng có thể gọi hàm `receive` hoặc `fallback` (là `function()` đối với các phiên bản trước 0.6.0) của smart contract nhận ETH trong một số trường hợp.

## Cách khắc phục <call-to-the-unknown-remediation>

Cẩn trọng khi gọi đến các smart contract bên ngoài, đặc biệt là các smart contract được đánh dấu là không an toàn. Có thể triển khai mẫu thiết kế Check-Effect-Pattern như đã được đề cập trong @re-entrancy-remediation.
