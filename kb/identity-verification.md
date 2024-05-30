# Identity Verification

## Mô tả

Một số smart contract kiểm tra xem một địa chỉ có phải là smart contract hay không thông qua opcode `extcodesize`.

```sol
contract OnlyForHuman {
  
  function isContract(address addr) returns (bool) {
    uint size;
    assembly { size := extcodesize(addr) }
    return size > 0;
  }
  
}
```

Cụ thể, opcode này giúp trả về kích thước bytecode của địa chỉ ở trên blockchain. Việc kiểm tra này có thể đến từ nhu cầu chỉ cho phép các địa chỉ không phải là của smart contract thực thi hàm.

Tuy nhiên, kẻ tấn công có thể thực thi hàm ở trong hàm tạo và vượt qua được cách kiểm tra trên. Lý do là vì trong quá trình hàm tạo thực thi, giá trị trả về của `extcodesize` sẽ là 0.

Ví dụ @how-does-a-contract-find-out-if-another-address-is-a-contract:

```sol
pragma solidity 0.4.25;

contract Victim {

  function isContract() public view returns(bool){
    uint32 size;
    address a = msg.sender;
    assembly {
      size := extcodesize(a)
    }
    return (size > 0);
  }

}

contract Attacker {
    
  bool public iTrickedIt;
  Victim v;
  
  constructor(address _v) public {
    v = Victim(_v);
    // addrss(this) doesn't have code, yet
    iTrickedIt = !v.isContract();
  }
}
```

Trong ví dụ trên, sau khi smart contract `Attacker` được triển khai ở trên blockchain, giá trị của `iTrickedIt` sẽ là `true` do giá trị trả về từ `v.isContract()` trong quá trình hàm tạo của `Attacker` đang thực thi là `false`.

## Cách khắc phục

Để nhận biết một địa chỉ không phải là smart contract, có thể so sánh giá trị `tx.origin` với giá trị `msg.sender`.

```sol
contract OnlyForHuman {
  
  modifier isHuman() {
    require(tx.origin == msg.sender, "sorry humans only");
    _;
  }
  
}
```

Tuy nhiên, việc sử dụng `tx.origin` để xác thực có thể dẫn đến lỗ hổng Authorization through tx.origin ở @authorization-through-tx-origin.

