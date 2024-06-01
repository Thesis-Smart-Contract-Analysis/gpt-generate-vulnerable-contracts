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
