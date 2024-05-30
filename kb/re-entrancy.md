# Re-entrancy <re-entrancy>

## Mô tả <re-entrancy-description>

Là một kiểu tấn công đệ quy tương hỗ xảy ra giữa smart contract của nạn nhân và smart contract của kẻ tấn công. Cụ thể hơn, kẻ tấn công sẽ liên tục gọi lại một hàm trong smart contract của nạn nhân trước khi lời gọi trước đó được thực thi xong.

Ví dụ bên dưới là phiên bản đơn giản của smart contract được dùng để vận hành DAO #footnote[DAO (Decentralized Autonomous Organizations) là một tập các smart contract hoạt động như một quỹ đầu tư tự động.]:

```sol
/*
 * @source: http://blockchain.unica.it/projects/ethereum-survey/attacks.html#simpledao
 * @author: Atzei N., Bartoletti M., Cimoli T
 * Modified by Josselin Feist
 */
pragma solidity 0.4.24;

contract SimpleDAO {
  
  mapping (address => uint) public credit;

  function donate(address to) payable public{
    credit[to] += msg.value;
  }

  function withdraw(uint amount) public {
    if (credit[msg.sender]>= amount) {
      require(msg.sender.call.value(amount)());
      credit[msg.sender]-=amount;
    }
  }  

  function queryCredit(address to) view public returns(uint){
    return credit[to];
  }
  
}
```

Trong ví dụ trên, smart contract cho phép quyên góp một lượng `msg.value` wei đến cho địa chỉ `to` thông qua hàm `donate`. Để rút ETH, người dùng có thể gọi hàm `withdraw` và truyền vào tham số `amount` lượng ETH cần rút.

Kẻ tấn công có thể xây dựng một smart contract dùng để tấn công như sau:

```sol
pragma solidity 0.4.24;

contract Attacker {
  
  SimpleDAO public simpleDAO;

  constructor(address _simpleDAOAddress) {
    simpleDAO = SimpleDAO(_simpleDAOAddress);
  }

  function attack() {
    simpleDAO.donate.value(1)(this);
    simpleDAO.withdraw(1 ether);
  }
  
  function() {
    simpleDAO.withdraw(1 ether);
  }
  
}
```

Khi kẻ tấn công gọi hàm `attack`, smart contract `Attacker` sẽ chuyển 1 ETH đến cho `SimpleDAO` thông qua hàm `donate` với đối số của `to` là địa chỉ của `Attacker`. Sau đó, hàm `attack` gọi đến hàm `withdraw` của `SimpleDAO` với đối số của `amount` là 1 ETH.

Lúc này, hàm `withdraw` của `SimpleDAO` sẽ gọi lại hàm fallback của `Attacker`. Tuy nhiên, hàm fallback của `Attacker` lại gọi đến hàm `withdraw` của `SimpleDAO`. Việc gọi hàm này ngăn cho biến trạng thái `credit[msg.sender]` bị giảm giá trị và dẫn đến điều kiện `if (credit[msg.sender]>= amount)` là luôn đúng đối với các lời gọi đệ quy sau.

Việc gọi đệ quy sẽ tiếp diễn đến khi:
1. Xảy ra ngoại lệ hết gas (out-of-gas exception).
2. Chạm đến giới hạn của stack.
3. Smart contract `SimpleDAO` không còn ETH nào.

## Cách khắc phục <re-entrancy-remediation>

Sử dụng các mẫu bảo mật chẳng hạn như Check-Effect-Interaction hoặc Mutex @wohrer_2018_smart.

Mẫu bảo mật Check-Effect-Interaction xếp lời gọi đến smart contract khác ở cuối và sau khi cập nhật biến trạng thái. 

Ví dụ:

```sol
pragma solidity 0.4.24;

contract SimpleDAO {
  
  mapping (address => uint) public credit;

  function donate(address to) payable public{
    credit[to] += msg.value;
  }

  function withdraw(uint amount) public {
    // 1. Check
    if (credit[msg.sender]>= amount) {
      // 2. Effect
      credit[msg.sender]-=amount;
      // 3. Interaction
      require(msg.sender.call.value(amount)());
    }
  }  

  function queryCredit(address to) view public returns(uint){
    return credit[to];
  }
  
}
```

Trong ví dụ trên, biến trạng thái `credit` được cập nhật trước khi hàm `call` được thực thi.

Ngoài ra, cũng có thể sử dụng smart contract ReentrancyGuard của OpenZeppelin @openzeppelin-reentrancy-guard để ngăn chặn các lời gọi đệ quy. Cụ thể, smart contract này cung cấp modifier `nonReentrant` để ngăn cản một smart contract gọi lại chính nó một cách trực tiếp hoặc gián tiếp.
