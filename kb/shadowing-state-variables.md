# Shadowing State Variables

## Mô tả

Xảy ra khi một smart contract kế thừa smart contract khác và cả hai đều cùng khai báo một biến. Vấn đề này cũng xảy ra khi smart contract có một biến toàn cục trùng tên với một biến cục bộ ở trong hàm.

Ví dụ:

```sol
pragma solidity 0.4.24;

contract Tokensale {
  
  uint hardcap = 10000 ether;

  function Tokensale() {}

  function fetchCap() public constant returns(uint) {
    return hardcap;
  }
  
}

contract Presale is Tokensale {
  
  uint hardcap = 1000 ether;

  function Presale() Tokensale() {}
  
}
```

Trong ví dụ trên, giá trị trả về khi gọi hàm `fetchCap` từ smart contract `Presale` là 10,000 ETH thay vì 1,000 ETH. Nói cách khác, biến `hardcap` ở trong `Presale` không ghi đè biến `hardcap` ở trong `Tokensale` và điều này có thể làm ảnh hưởng đến kết quả thực thi của smart contract.

## Cách khắc phục

Nếu muốn ghi đè biến trạng thái của smart contract được kế thừa, ta có thể gán giá trị mới cho nó ở trong hàm tạo của smart contract kế thừa. Ví dụ:

```sol
contract Presale is Tokensale {
  
  // uint hardcap = 1000 ether;
  
  function Presale() Tokensale() {
    hardcap = 1000 ether;
  }
  
}
```

Kể từ phiên bản 0.6.0 @solidity-v0.6.0-breaking-changes, việc shadowing các biến trạng thái sẽ được phát hiện bởi trình biên dịch.
