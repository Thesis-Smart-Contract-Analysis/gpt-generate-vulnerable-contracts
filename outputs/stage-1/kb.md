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



# Outdated Compiler Version

## Mô tả

Sử dụng một phiên bản trình biên dịch đã cũ có thể gây ra các vấn đề, đặc biệt là khi phiên bản đó có các lỗi và sự cố đã được tiết lộ công khai.

## Cách khắc phục

Sử dụng phiên bản trình biên dịch của Solidity gần đây nhất.
# Floating Compiler Version

## Mô tả

Một contract có thể được biên dịch bởi nhiều phiên bản của trình biên dịch khác nhau. 

Ví dụ:

```sol
pragma solidity >=0.4.0 < 0.6.0;
pragma solidity >=0.4.0<0.6.0;
pragma solidity >=0.4.14 <0.6.0;
pragma solidity >0.4.13 <0.6.0;
pragma solidity 0.4.24 - 0.5.2;
pragma solidity >=0.4.24 <=0.5.3 ~0.4.20;
pragma solidity <0.4.26;
pragma solidity ~0.4.20;
pragma solidity ^0.4.14;
pragma solidity 0.4.*;
pragma solidity 0.*;
pragma solidity *;
pragma solidity 0.4;
pragma solidity 0;

contract SemVerFloatingPragma { }
```

Trong ví dụ trên, smart contract khai báo rất nhiều phiên bản của trình biên dịch theo kiểu SemVer (Semantic Versoning). Điều này có thể dẫn đến việc phiên bản được sử dụng lúc kiểm thử và lúc triển khai smart contract khác nhau. Nếu smart contract được triển khai bởi một phiên bản của trình biên dịch có chứa lỗi thì có thể làm ảnh hưởng đến tính đúng đắn của nó.

## Cách khắc phục

Cần phải cố định phiên bản của trình biên dịch được sử dụng cho smart contract, ví dụ:

```sol
pragma solidity 0.4.25;
// or
pragma solidity =0.4.25;

contract SemVerFloatingPragmaFixed { }
```
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
# Uninitialized Storage Pointer

## Bố cục lưu trữ của Solidity <storage-layout>

Trước khi phân tích lỗ hổng, ta cần hiểu về cách Solidity lưu các biến `storage`. Nói một cách đơn giản, các biến `storage` được Solidity lưu liên tiếp ở trong các khe lưu trữ (slot). Có tổng cộng $2^{256}$ khe lưu trữ, mỗi khe lưu trữ có kích thước 32 byte và được đánh số từ 0 đến $2^{256} - 1$ @voitier_2023_exploring-the-storage-layout-in-solidity-and-how-to-access-state-variables, @a2018_understanding-ethereum-smart-contract-storage. 

Xét ví dụ sau:

```sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8;

contract StorageLayout {
  uint256 x = 1; // slot 0
  uint256 y = 2; // slot 1
  uint256 z = 3; // slot 2
}
```

Do mỗi biến `x`, `y` và `z` đều có kích thước là 32 byte nên chúng được lưu trong từng slot riêng biệt. 

Trong trường hợp kích thước của các biến là nhỏ và vừa đủ một slot, chúng sẽ được đặt cạnh nhau. Ví dụ:

```sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8;

// contract address: 0xeBa088B4182EC4261FA4fd2526F58995Dc1Ec117

contract StorageLayout {
    uint16 x = 1;
    uint16 y = 2;
    uint16 z = 3;
}
```

Khi dùng hàm `web3.eth.getStorageAt(contractAddress, slotPosition)` của thư viện web3.js để truy vấn giá trị được lưu ở slot 0, ta thu được giá trị sau:

```sol
slot[0] = 0x0000000000000000000000000000000000000000000000000000000300020001
```

Có thể thấy, ba biến `x`, `y` và `z` được đặt cạnh nhau. Ngoài ra, giá trị lưu ở slot 0 cũng được ABI-encode @abi-specification bằng cách đệm thêm các số 0.

Trong trường hợp các biến không thể lưu vừa trong một slot, chúng sẽ được lưu vào nhiều slot. Ví dụ:

```sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8;

contract StorageLayout {
    uint16 x = 1;
    uint256 y = 2;
    uint16 z = 3;
}
```

Giá trị của các biến lưu trong các slot là:

```sol
slot[0] = 0x0000000000000000000000000000000000000000000000000000000000000001
slot[1] = 0x0000000000000000000000000000000000000000000000000000000000000002
slot[2] = 0x0000000000000000000000000000000000000000000000000000000000000003
```

## Mô tả

Các biến cục bộ có vị trí dữ liệu (data location) là `storage` bên trong hàm nếu không được khởi tạo có thể trỏ đến các biến trạng thái có vị trí dữ liệu là `storage` trong smart contract. Điều này có thể dẫn đến việc giá trị của các biến trạng thái bị sửa đổi thông qua các biến cục bộ. 

Xét smart contract sau:

```sol
// A Locked Name Registrar
contract NameRegistrar {

  bool public unlocked = false;  // registrar locked, no name updates
  
  struct NameRecord { // map hashes to addresses
    bytes32 name;
    address mappedAddress;
  }
  
  mapping(address => NameRecord) public registeredNameRecord; // records who registered names
  mapping(bytes32 => address) public resolve; // resolves hashes to addresses
  
  function register(bytes32 _name, address _mappedAddress) public {
    // set up the new NameRecord
    NameRecord newRecord;
    newRecord.name = _name;
    newRecord.mappedAddress = _mappedAddress;
    
    resolve[_name] = _mappedAddress;
    registeredNameRecord[msg.sender] = newRecord;
    
    require(unlocked); // only allow registrations if contract is unlocked
  }
}
```

Smart contract này có duy nhất một hàm là `register`. Khi biến trạng thái `unlocked` có giá trị là `true`, smart contract cho phép người dùng đăng ký tên và địa chỉ tương ứng với tên đó vào mapping `registeredNameRecord`. Câu lệnh `require` ở cuối hàm giúp hoàn trả giao dịch nếu `unlocked` có giá trị là `false`.

Dựa trên cơ chế lưu các biến `storage` của Solidity thì slot 0 sẽ lưu biến `unlocked`, slot 1 lưu biến `registeredNameRecord` và slot 2 lưu biến `resolve` #footnote[Ta bỏ qua việc mapping không thực sự được lưu ở một slot mà thay vào đó là các phần tử của nó được lưu ở các slot không liền kề nhau.].

Như đã biết, vị trí dữ liệu mặc định cho các biến có kiểu tham chiếu chẳng hạn như struct, mảng hoặc mapping là `storage`. Việc không khai báo vị trí dữ liệu cho biến `newRecord` bên trong hàm `register` làm cho nó có vị trí dữ liệu là `storage`. Do là một biến `storage` và không được khởi tạo, `newRecord` sẽ đóng vai trò là một con trỏ và trỏ đến slot 0. 

Cụ thể hơn, trường `name` và `mappedAddress` sẽ lần lượt trỏ đến biến `unlocked` và biến `registeredNameRecord`. Việc gán giá trị cho trường `name` khi đó cũng sẽ làm thay đổi giá trị của biến `unlocked`. Bằng cách chọn giá trị `_name` sao cho có bit cuối là 1, kẻ tấn công có thể gọi thực thi hàm `register` để thay đổi biến `unlocked` thành `true`.

## Cách khắc phục

Kiểm tra xem biến cục bộ thuộc kiểu tham chiếu có nhất thiết phải là `storage` hay không (thường là không vì điều này làm tăng chi phí thực hiện smart contract do việc ghi vào biến `storage` tiêu thụ rất nhiều gas). Nếu cần thiết thì nên khai báo vị trí dữ liệu tường minh là `storage`. Nếu không thì nên sử dụng vị trí dữ liệu là `memory`.

Kể từ phiên bản 0.5.0, vấn đề này đã được giải quyết do các biến `storage` chưa được khởi tạo sẽ không được biên dịch.


# Use of Deprecated Solidity Functions

## Mô tả

Với các phiên bản mới của trình biên dịch, việc sử dụng các định danh (identifier) cũ đã bị loại bỏ có thể dẫn đến các lỗi biên dịch hoặc các hành vi không mong muốn.

Ví dụ bên dưới có chứa các định danh cũ không còn sử dụng trong các phiên bản trình biên dịch sau này:

```sol
contract DeprecatedSimple {

  function DeprecatedSimple() public { }

  function useDeprecated() public constant {
    bytes32 blockhash = block.blockhash(0);
    bytes32 hashofhash = sha3(blockhash);

    uint gas = msg.gas;

    if (gas == 0) {
      throw;
    }

    address(this).callcode();

    var a = [1,2,3];

    var (x, y, z) = (false, "test", 0);

    suicide(address(0));
  }

  function () public {}
}
```

## Cách khắc phục

Sử dụng các định danh thay thế trong smart contract.

#figure(
  table(
    columns: (auto, auto),
    align: horizon,
    table.header("Cũ", "Thay thế"),
    `suicide(address)`, `selfdestruct(address)`,
    `block.blockhash(uint)`,	`blockhash(uint)`,
    `sha3(...)`, `keccak256(...)`,
    `callcode(...)`, `delegatecall(...)`,
    `throw`,	`revert()`,
    `msg.gas`,	`gasleft`,
    `constant`,	`view`,
    `var`,	[tên kiểu dữ liệu tương ứng],
    [`function ()`], [`receive()` hoặc `fallback()`],
    [Hàm tạo trùng tên với smart contract], `constructor()`
  ),
  caption: [Các định danh cũ và định danh thay thế tương ứng]
)

Đối với ví dụ của smart contract `DeprecatedSimple` ở trên, có thể sửa lại như sau:

```sol
contract DeprecatedSimpleFixed {

  constructor() { }
  
  function useDeprecatedFixed() public view {
    bytes32 bhash = blockhash(0);
    bytes32 hashofhash = keccak256(bhash);

    uint gas = gasleft();

    if (gas == 0) {
      revert();
    }

    address(this).delegatecall();

    uint8[3] memory a = [1,2,3];

    (bool x, string memory y, uint8 z) = (false, "test", 0);

    selfdestruct(address(0));
  }

  receive() external payable { }

}
```
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

