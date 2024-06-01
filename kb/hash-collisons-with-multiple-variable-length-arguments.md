# Hash Collisions with Multiple Variable Length Arguments

## Hàm `abi.encodePacked`

Được dùng để đóng gói và ABI encode @abi-specification nhiều giá trị. Hàm này khác hàm `abi.encode` ở chỗ nó không thêm các số 0 vào giá trị đầu ra.

Giả sử dùng hàm `abi.encodePacked` để encode các giá trị sau: 
- `int16(-1)`
- `bytes1(0x42)`
- `uint16(0x03)` 
- `string("Hello, world!")`

Hàm này sẽ trả về giá trị `0xffff42000348656c6c6f2c20776f726c6421`, là sự kết hợp của các giá trị được encode:

```txt
0xffff42000348656c6c6f2c20776f726c6421
  ^^^^                                 int16(-1)
      ^^                               bytes1(0x42)
        ^^^^                           uint16(0x03)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^ string("Hello, world!") without a length field
```

## Mô tả

Việc sử dụng hàm `abi.encodePacked` với đối số là các mảng có kích thước không cố định có thể gây ra đụng độ giá trị băm (hash collision). Lý do là vì hàm này đóng gói các phần tử mà không quan tâm đến việc chúng có thuộc một mảng nào đó hay không. Cụ thể, hai dòng sau đây sẽ cho ra kết quả tương đương:

```sol
abi.encodePacked([addr1, addr2], [addr3, addr4]);
abi.encodePacked([addr1, addr2, addr3], [addr4]);
```

Nếu smart contract sử dụng giá trị của hàm `abi.encodePacked` để xác thực thì kẻ tấn công có thể vượt qua xác thực bằng cách di chuyển một hoặc nhiều phần tử từ mảng này sang mảng khác.

Ví dụ:

```sol
/*
 * @author: Steve Marx
 * Modified by Kaden Zipfel
 */
pragma solidity ^0.5.0;

import "./ECDSA.sol";

contract AccessControl {
  
  using ECDSA for bytes32;
  mapping(address => bool) isAdmin;
  mapping(address => bool) isRegularUser;
  // Add admins and regular users.
  function addUsers(
    address[] calldata admins,
    address[] calldata regularUsers,
    bytes calldata signature
  )
      external
  {
    if (!isAdmin[msg.sender]) {
      // Allow calls to be relayed with an admin's signature.
      bytes32 hash = keccak256(abi.encodePacked(admins, regularUsers));
      address signer = hash.toEthSignedMessageHash().recover(signature);
      require(isAdmin[signer], "Only admins can add users.");
    }
    for (uint256 i = 0; i < admins.length; i++) {
      isAdmin[admins[i]] = true;
    }
    for (uint256 i = 0; i < regularUsers.length; i++) {
      isRegularUser[regularUsers[i]] = true;
    }
  }
    
}
```

Người dùng có thể được thêm vào smart contract thông qua hàm `addUsers` bằng cách truyền vào mảng các admin, mảng các người dùng thông thường cùng với chữ ký của admin:

```sol
addUsers([addr1, addr2], [addr3, <attacker's address>, addr4], sig)
```

Kẻ tấn công có thể gọi hàm `addUsers` như sau:

```sol
addUser([addr1, addr2, addr3, <attacker's address>], [addr4], sig)
```

Như đã biết, việc di chuyển `addr3` và `<attacker's address>` sang mảng đầu tiên không làm thay đổi giá trị trả về của hàm `abi.encodePacked`. Nhờ đó, kẻ tấn công có thể tạo ra được chữ ký hợp lệ và trở thành admin.

## Cách khắc phục

Chỉ dùng hàm `abi.encodePacked` với đối số có kích thước cố định. 

Trong ví dụ của smart contract `AccessControl` trên, chỉ cho phép thêm vào $n$ ($n in N^*$) người dùng cố định đối với mỗi lần gọi hàm.

Ví dụ thêm 1 người dùng:

```sol
/*
 * @author: Steve Marx
 * Modified by Kaden Zipfel
 */
pragma solidity ^0.5.0;

import "./ECDSA.sol";

contract AccessControl {
  
  using ECDSA for bytes32;
  mapping(address => bool) isAdmin;
  mapping(address => bool) isRegularUser;
  // Add a single user, either an admin or regular user.
  function addUser(
    address user,
    bool admin,
    bytes calldata signature
  )
      external
  {
    if (!isAdmin[msg.sender]) {
      // Allow calls to be relayed with an admin's signature.
      bytes32 hash = keccak256(abi.encodePacked(user));
      address signer = hash.toEthSignedMessageHash().recover(signature);
      require(isAdmin[signer], "Only admins can add users.");
    }
    if (admin) {
      isAdmin[user] = true;
    } else {
      isRegularUser[user] = true;
    }
  }

}
```

Ví dụ thêm 3 người dùng:

```sol
/*
 * @author: Steve Marx
 * Modified by Kaden Zipfel
 */
pragma solidity ^0.5.0;

import "./ECDSA.sol";

contract AccessControl {
  
  using ECDSA for bytes32;
  mapping(address => bool) isAdmin;
  mapping(address => bool) isRegularUser;
  // Add admins and regular users.
  function addUsers(
    // Use fixed length arrays.
    address[3] calldata admins,
    address[3] calldata regularUsers,
    bytes calldata signature
  )
      external
  {
    if (!isAdmin[msg.sender]) {
      // Allow calls to be relayed with an admin's signature.
      bytes32 hash = keccak256(abi.encodePacked(admins, regularUsers));
      address signer = hash.toEthSignedMessageHash().recover(signature);
      require(isAdmin[signer], "Only admins can add users.");
    }
    for (uint256 i = 0; i < admins.length; i++) {
      isAdmin[admins[i]] = true;
    }
    for (uint256 i = 0; i < regularUsers.length; i++) {
      isRegularUser[regularUsers[i]] = true;
    }
  }
    
}
```
