# Delegatecall to Untrusted Callee

## Hàm `delegatecall`

Là một hàm low-level tương tự với hàm `call` (đều được dùng để gọi hàm của smart contract khác hoặc gửi ETH đến smart contract khác). 

Tuy nhiên, khi một smart contract A gọi thực thi hàm của smart contract B bằng `delegatecall`, hàm của smart contract B sẽ thực thi với các biến trạng thái của smart contract A.

Ví dụ:

```sol
// NOTE: Deploy this contract first
contract B {
  
    // NOTE: storage layout must be the same as contract A
    uint256 public num;
    address public sender;
    uint256 public value;

    function setVars(uint256 _num) public payable {
      num = _num;
      sender = msg.sender;
      value = msg.value;
    }
    
}

contract A {
  
    uint256 public num;
    address public sender;
    uint256 public value;

    function setVars(address _contract, uint256 _num) public payable {
      // A's storage is set, B is not modified.
      (bool success, bytes memory data) = _contract.delegatecall(
          abi.encodeWithSignature("setVars(uint256)", _num)
      );
    }
    
}
```

Trong ví dụ trên, hàm `setVars(address,uint256)` của smart contract `A` gọi thực thi hàm `setVars(uint256)` của smart contract `B` thông qua hàm `delegatecall`.

Ta gọi thực thi hàm `setVars(address,uint256)` với các đối số lần lượt là:
- Địa chỉ của contract `B` (`0xd2184e03fC9a5deB782691e41fAB0Ba77F52202e`)
- Giá trị `1`

Sau khi thực thi, giá trị của hai biến `num` và `sender` của smart contract `A` sẽ bị thay đổi. Cụ thể:
- `num` bị thay đổi thành `1`.
- `sender` bị thay đổi thành địa chỉ gọi hàm `setVars`.

## Mô tả

Việc sử dụng hàm `delegatecall` để gọi hàm của các smart contract không tin cậy là rất nguy hiểm bởi vì các smart contract này có thể thay đổi các giá trị của các biến trạng thái hoặc chiếm quyền sở hữu của smart contract hiện tại.

Ví dụ, cho smart contract `Proxy` như sau:

```sol
contract Proxy {

  address owner;

  constructor() {
    owner = msg.sender;  
  }

  function getOwner() public view returns (address) {
    return owner;
  }

  function forward(address callee, bytes memory _data) public {
    (bool success, ) = callee.delegatecall(_data);
    require(success);
  }

}
```

Hàm `forward` sẽ gọi đến hàm của smart contract có địa chỉ là `callee` thông qua hàm `delegatecall`. Kẻ tấn công có thể xây dựng một smart contract như sau để tấn công:

```sol
contract Attacker {
    
  address owner;

  fallback() external { 
    owner = 0xB514b2e847116c7B57e0BFac3a180eB049cd395c;
  }

}
```

Với `0xB514b2e847116c7B57e0BFac3a180eB049cd395c` là một địa chỉ mà kẻ tấn công sở hữu.

Kẻ tấn công có thể gọi hàm `forward` với:
- Đối số của `callee` là địa chỉ của smart contract `Attacker` (giả sử là `0xaB35F973D99176552d49030c65B6cB4A82F9254e`).
- Đối số của `_data` là giá trị rỗng chẳng hạn như `0x00000000000000000000000000000000` nhằm gọi hàm `fallback` của smart contract `Attacker`.

Sau khi thực thi, giá trị của `owner` trong smart contract `Proxy` sẽ là: `0xB514b2e847116c7B57e0BFac3a180eB049cd395c`

## Cách khắc phục

Cần đảm bảo rằng hàm `delegatecall` không bao giờ gọi đến các smart contract không tin cậy. Nếu địa chỉ của smart contract được gọi hàm là giá trị truyền vào của người dùng thì cần đảm bảo địa chỉ này nằm trong một danh sách các địa chỉ được phép sử dụng (whitelist).

