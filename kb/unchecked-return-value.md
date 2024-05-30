# Unchecked Return Value

## Mô tả

Một smart contract có thể giao tiếp với smart contract khác thông qua các cách sau:
- Sử dụng các hàm ở mức thấp (opcode) chẳng hạn như `call`, `delegatecall` và `staticcall` để gọi hàm hoặc gửi ETH.
- Sử dụng hàm `send` để gửi ETH.

Nếu có ngoại lệ xảy ra trong smart contract khác thì các hàm trên sẽ trả về giá trị luận lý cho biết thao tác không được thực hiện thành công thay vì lan truyền ngoại lệ. Nếu không kiểm tra giá trị luận lý này thì có thể làm ảnh hưởng đến kết quả thực thi của smart contract.

Ví dụ bên dưới dùng hàm `call` để gọi hàm `foo` của smart contract có địa chỉ là `_addr` với hai đối số lần lượt là `"call foo"` và `123`:

```sol
contract UsingCall {
  
  function invokeFunction(address payable _addr) public payable {
  	(bool success, bytes memory data) = _addr.call{
    	value: msg.value,
    	gas: 5000
    }(abi.encodeWithSignature("foo(string,uint256)", "call foo", 123));
  }
  
}
```

Nếu hàm `foo` xảy ra ngoại lệ, biến `success` sẽ có giá trị là `false` cho biết việc gọi hàm thất bại. Tuy nhiên, việc xảy ra ngoại lệ trong một smart contract khác không làm dừng quá trình thực thi của contract `UsingCall` cũng như là không hủy bỏ các sự thay đổi lên các biến trạng thái.

Trong trường hợp sử dụng hàm `send`, ngoại lệ có thể xảy ra trong (các) hàm fallback của smart contract nhận ETH một cách tình cờ hoặc có chủ đích. 

## Cách khắc phục

Luôn kiểm tra giá trị của biến luận lý được trả về từ các hàm dùng để giao tiếp với smart contract khác mà không lan truyền ngoại lệ.

Ví dụ:

```sol
pragma solidity 0.4.25;

contract ReturnValue {
  
  function callchecked(address callee) public {
    require(callee.call());
  }

  function callnotchecked(address callee) public {
    callee.call();
  }
  
}
```


