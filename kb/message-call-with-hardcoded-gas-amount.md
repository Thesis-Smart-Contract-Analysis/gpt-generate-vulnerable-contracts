# Message Call with Hardcoded Gas Amount

## Mô tả

Hàm `transfer` và hàm `send` đã từng được sử dụng để giải quyết lỗ hổng re-entrancy (@re-entrancy) vì chúng chỉ cung cấp cho smart contract nhận ETH 2300 gas (hoặc nhỏ hơn) #footnote[Dưới phiên bản 0.4.0 thì hàm `send` có gas là 0 nếu lượng ETH chuyển đi là 0 và gas là 2300 nếu lượng ETH chuyển đi khác 0.] - lượng gas này quá nhỏ để thực hiện các thao tác phức tạp chẳng hạn như cập nhật biến trạng thái hoặc gọi hàm.

Tuy nhiên, một số sự thay đổi trong EVM gây ra bởi các lần hard fork có thể làm thay đổi giá gas và làm cho các giả định của các smart contract đã được triển khai về một giá gas cố định không còn đúng. Ví dụ, EIP-1884 @eip-1884 đã tăng giá của một số opcode chẳng hạn như `SLOAD` và làm một số smart contract không còn hoạt động được nữa.

Việc sử dụng hàm `call` với mức gas cố định cũng tương tự.

Ví dụ:

```sol
/*
 * @author: Bernhard Mueller (ConsenSys / MythX)
 */
pragma solidity 0.6.4;

interface ICallable {
  function callMe() external;
}

contract HardcodedNotGood {

  address payable _callable = 0xaAaAaAaaAaAaAaaAaAAAAAAAAaaaAaAaAaaAaaAa;
  ICallable callable = ICallable(_callable);

  constructor() public payable {
  }

  function doTransfer(uint256 amount) public {
    _callable.transfer(amount);
  }

  function doSend(uint256 amount) public {
    _callable.send(amount);
  }

   function callLowLevel() public {
     _callable.call.value(0).gas(10000)("");
   }

   function callWithArgs() public {
     callable.callMe{gas: 10000}();
   }
   
}
```

## Cách khắc phục

Không sử dụng `transfer` và `send` cũng như là chỉ định mức gas cố định khi sử dụng hàm `call`. Để tránh lỗ hổng re-entrancy khi sử dụng hàm `call`, có thể triển khai các mẫu bảo mật đã được đề cập ở @re-entrancy-remediation.
