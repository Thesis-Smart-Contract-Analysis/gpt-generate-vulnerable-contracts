# Function or State Variable Default Visibility

## Mô tả

Trạng thái hiển thị (visibility) mặc định của các hàm là `public`. Việc không khai báo trạng thái hiển thị một cách tường minh có thể gây ra các hành vi không mong muốn trong smart contract. Ví dụ, các hàm vốn chỉ được dùng trong nội bộ bên trong smart contract có thể bị gọi sử dụng một cách công khai bởi bất kỳ ai.

```sol
/*
 * @source: https://github.com/sigp/solidity-security-blog#visibility
 * @author: SigmaPrime 
 * Modified by Gerhard Wagner
 */

pragma solidity ^0.4.24;

contract HashForEther {

  function withdrawWinnings() {
    // Winner if the last 8 hex characters of the address are 0. 
    require(uint32(msg.sender) == 0);
    _sendWinnings();
  }
  
  function _sendWinnings() {
    msg.sender.transfer(this.balance);
  }
     
}
```

Trong ví dụ trên, bất kỳ ai cũng có thể gọi hàm `_sendWinnings` để rút ETH từ hợp đồng thông minh mà không cần phải tạo ra một địa chỉ có 8 ký tự cuối là `0`.

Đối với các biến trạng thái, mặc dù trạng thái hiển thị mặc định của chúng là `internal`, việc khai báo trạng thái hiển thị một cách tường minh có thể giúp tránh được những nhầm lẫn về quyền truy cập.

## Cách khắc phục

Kể từ phiên bản 0.5.0 @solidity-v0.5.0-breaking-changes, việc khai báo tường minh trạng thái hiển thị cho hàm là bắt buộc nên lỗ hổng này chỉ tồn tại ở các phiên bản trước đó của Solidity.

Mặc dù vậy, lập trình viên cũng nên xem xét cẩn thận việc sử dụng trạng thái hiển thị của từng hàm. Đặc biệt là những hàm có trạng thái hiển thị là `public` hoặc `external`.

Đối với ví dụ của smart contract `HashForEther` ở trên, có thể thêm vào các visibility như sau:

```sol
/*
 * @source: https://github.com/sigp/solidity-security-blog#visibility
 * @author: SigmaPrime
 * Modified by Gerhard Wagner
 */

pragma solidity ^0.4.24;

contract HashForEther {
  
  function withdrawWinnings() public {
    // Winner if the last 8 hex characters of the address are 0.
    require(uint32(msg.sender) == 0);
    _sendWinnings();
  }
  
  function _sendWinnings() internal {
     msg.sender.transfer(this.balance);
  }

}
```
