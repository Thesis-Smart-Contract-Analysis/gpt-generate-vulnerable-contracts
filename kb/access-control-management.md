# Access Control Management

## Mô tả

Việc không kiểm soát quyền truy cập của hàm có thể khiến cho bất kỳ ai không có quyền cũng có thể thực thi hàm, đặc biệt là các hàm rút ETH hoặc gọi các hàm nguy hiểm chẳng hạn như `selfdestruct` #footnote[`selfdestruct` là một hàm dùng để xóa bytecode của smart contract ở trên blockchain và chuyển hết ETH còn lại trong smart contract đến địa chỉ được chỉ định.].

Ví dụ:

```sol
pragma solidity ^0.4.22;

contract SimpleEtherDrain {

  function withdrawAllAnyone() {
    msg.sender.transfer(this.balance);
  }

  function () public payable {
  }
  
}
```

Trong ví dụ trên, hàm `withdrawAllAnyone` không áp dụng các biện pháp kiểm soát quyền truy cập nên bất kỳ ai cũng có thể gọi hàm và rút hết ETH từ smart contract.

Một ví dụ khác:

```sol
pragma solidity ^0.4.22;

contract SimpleSuicide {

  function sudicideAnyone() {
    selfdestruct(msg.sender);
  }
  
}
```

Với ví dụ này, do không kiểm soát quyền truy cập nên bất kỳ ai cũng có thể gọi hàm `sudicideAnyone` và rút hết ETH thông qua hàm `selfdestruct`.

## Cách khắc phục

Cần giới hạn lại quyền truy cập của hàm cho một số địa chỉ nhất định. Có thể sử dụng các biện pháp kiểm soát quyền truy cập chẳng hạn như smart contract Ownable của OpenZeppelin @openzeppelin-ownership.

Ví dụ:

```sol
import "./Ownable.sol"

contract MyContract is Ownable {
  INumberInterface numberContract;
  
  function setNumberContractAddress(address _address) external onlyOwner {
    numberContract = INumberInterface(_address);
  }
  
  function someFunction() public {
    uint num = numberContract.getNum(msg.sender);
  }
}
```

Trong ví dụ trên, `onlyOwner` là một modifier giúp giới hạn quyền truy cập đến hàm. Cụ thể, nó ngăn không cho các địa chỉ không phải là chủ sở hữu smart contract thực thi hàm.

Cân nhắc không dùng hàm `selfdestruct` trong smart contract hoặc nếu có dùng thì sử dụng mô hình đa chữ ký để đảm bảo rằng có nhiều tổ chức đồng thuận với việc xóa bytecode của smart contract.

Ngoài ra, kể từ phiên bản 0.8.18 @eip-4758, Solidity không còn hỗ trợ hàm `selfdestruct`.


