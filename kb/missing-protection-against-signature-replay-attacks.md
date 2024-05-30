# Missing Protection against Signature Replay Attacks <signature-replay>

## Mô tả

Lỗ hổng này xảy ra khi smart contract thực hiện xác thực chữ ký nhưng không kiểm tra xem chữ ký đã được sử dụng hay chưa. Kẻ tấn công có thể tái sử dụng chữ ký nhiều lần để vượt qua xác thực và thực thi hàm.

Ví dụ @signature-replay-ref:

```sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "./ECDSA.sol";

contract MultiSigWallet {
  
  using ECDSA for bytes32;

  address[2] public owners;

  constructor(address[2] memory _owners) payable { owners = _owners; }

  function deposit() external payable { }

  function transfer(address _to, uint256 _amount, bytes[2] memory _sigs)
    external
  {
    bytes32 txHash = getTxHash(_to, _amount);
    require(_checkSigs(_sigs, txHash), "invalid sig");

    (bool sent,) = _to.call{value: _amount}("");
    require(sent, "Failed to send Ether");
  }

  function getTxHash(address _to, uint256 _amount)
    public
    view
    returns (bytes32)
  {
    return keccak256(abi.encodePacked(_to, _amount));
  }

  function _checkSigs(bytes[2] memory _sigs, bytes32 _txHash)
    private
    view
    returns (bool)
  {
    bytes32 ethSignedHash = _txHash.toEthSignedMessageHash();

    for (uint256 i = 0; i < _sigs.length; i++) {
      address signer = ethSignedHash.recover(_sigs[i]);
      bool valid = signer == owners[i];

      if (!valid) {
        return false;
      }
    }

    return true;
  }
  
}
```

Trong ví dụ trên, hàm `transfer` có các tham số sau:
- Địa chỉ nhận ETH: `_to`.
- Lượng ETH cần chuyển: `_amount`.
- Hai chữ ký của hai chủ sở hữu ví: `memory _sigs`.

Hàm `transfer` xây dựng văn bản sẽ được ký bằng cách băm giá trị `txHash` theo chuẩn được nêu trong EIP-191 @eip-191. Sau đó, nó gọi hàm `_checkSigs` để kiểm tra xem địa chỉ được khôi phục từ hai chữ ký có khớp với địa chỉ của các chủ sở hữu ví hay không.

Do smart contract không kiểm tra sự giống nhau của các chữ ký trong những lần gọi hàm khác nhau, kẻ tấn công có thể dùng lại các chữ ký cũ (lấy được thông qua các giao dịch trước đó) để chuyển tiền đến địa chỉ `_to` với lượng ETH là `_amount` (giả sử `_to` là một địa chỉ mà kẻ tấn công sở hữu).

## Cách khắc phục

Có thể lưu lại danh sách các chữ ký đã được sử dụng và thêm một giá trị dùng một lần (nonce) vào văn bản cần ký để các chữ ký sử dụng trong những lần gọi hàm khác nhau là khác nhau. Kẻ tấn công dù biết được giá trị nonce này cũng không có khóa riêng tư của các chủ sở hữu ví để tạo ra các chữ ký hợp lệ.

Ví dụ @signature-replay-ref:

```sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "./ECDSA.sol";

contract MultiSigWallet {
  
  using ECDSA for bytes32;

  address[2] public owners;
  mapping(bytes32 => bool) public executed;

  constructor(address[2] memory _owners) payable { owners = _owners; }

  function deposit() external payable {}

  function transfer(
    address _to,
    uint256 _amount,
    uint256 _nonce,
    bytes[2] memory _sigs
  ) external {
    bytes32 txHash = getTxHash(_to, _amount, _nonce);
    require(!executed[txHash], "tx executed");
    require(_checkSigs(_sigs, txHash), "invalid sig");

    executed[txHash] = true;

    (bool sent,) = _to.call{value: _amount}("");
    require(sent, "Failed to send Ether");
  }

  function getTxHash(address _to, uint256 _amount, uint256 _nonce)
    public
    view
    returns (bytes32)
  {
    return keccak256(abi.encodePacked(address(this), _to, _amount, _nonce));
  }

  // ...
  
}
```

Trong ví dụ trên, smart contract sử dụng biến `executed` để lưu lại những chữ ký đã được sử dụng. Ngoài ra, văn bản được ký có thêm giá trị `_nonce`. Giá trị này có thể là một số nguyên ngẫu nhiên hoặc tăng dần tùy thuộc vào chủ sở hữu ví.



