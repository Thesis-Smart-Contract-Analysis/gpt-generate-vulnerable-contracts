# Signature Malleability

## Thuật toán chữ ký số trên đường cong elliptic (ECDSA)

Ethereum sử dụng thuật toán chữ ký số trên đường cong elliptic (ECDSA). Đường cong mà thuật toán này sử dụng là secp256k1 có phương trình như sau:

$
y^2 = x^3 + 7
$

#figure(
  image("imgs/secp256k1.png"),
  caption: [Đồ thị của đường cong Elliptic]
)

Có thể thấy, đồ thị đối xứng qua trục x. Đây là một tính chất quan trọng góp phần tạo ra lỗ hổng.

Trong ECDSA, chữ ký được biểu diễn bằng cặp số $(r, s)$. Quá trình tạo ra chữ ký @what-is-the-ecdsa:
- Thuật toán sẽ chọn một con số nguyên $k$ ngẫu nhiên với $1 < k < n$ và $n$ là số lượng điểm có trong đường cong secp256k1 (là một số nguyên tố).
- Sau đó, tạo ra điểm $R$ với $R = k * G$ (G là phần tử sinh của đường cong secp256k1). Giá trị $r$ là tọa độ x của điểm $R$.
- Tính toán bằng chứng chữ ký $s$ với công thức sau: $s = k^-1 * (h + d * r) mod n$ với $h$ là giá trị băm của thông điệp cần ký và $d$ là khóa riêng tư.

Quy trình xác thực chữ ký:
- Tính toán giá trị băm của thông điệp và nghịch đảo modulo của $s$ (ta gọi là $s'$).
- Khôi phục điểm $R$ được sinh ra trong qua trình ký bằng công thức sau: $R' = (h * s') * G + (r * s') * e$ với $e$ là khóa công khai.
- So sánh tọa độ x của $R'$ với tọa độ x của $R$ (giá trị $r$). Nếu hai giá trị này bằng nhau thì tức là chữ ký hợp lệ.

Do tính đối xứng, nếu $(r, s)$ là một chữ ký hợp lệ thì $(r, -s \mod n)$ cũng là một chữ ký hợp lệ.

## Mô tả

Các hệ thống chữ ký mật mã của Ethereum được hiện thực với giả định rằng chữ ký số là duy nhất. Smart contract hoạt động dựa trên giả định này có thể bị tấn công vì kẻ tấn công có thể chỉnh sửa các giá trị v, r và s của một chữ ký để tạo ra một chữ ký hợp lệ khác mà không cần biết khóa riêng tư (dựa vào tính đối xứng). 

Ví dụ bên dưới minh họa cho quá trình xác thực chữ ký trong Solidity:

```sol
// source: https://medium.com/draftkings-engineering/signature-malleability-7a804429b14a
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SignatureMalleability{

  function verify(bytes32 _messageHash, bytes memory _sig, address _expectedSigner) 
  public pure returns (bool) {
    bytes32 ethSignedHash = keccak256(
      abi.encodePacked("\x19Ethereum Signed Message:\n32", _messageHash)
    );
    address signer = recoverSigner(ethSignedHash, _sig);
    return signer == _expectedSigner;
  }

  function recoverSigner(bytes32 _ethSignedHash, bytes memory _sig) 
  public pure returns (address) {
    require(_sig.length == 65, "Invalid signature length");
    bytes32 r;
    bytes32 s;
    uint8 v;
    assembly {
      r := mload(add(_sig, 32))
      s := mload(add(_sig, 64))
      v := byte(0, mload(add(_sig, 96)))
    }
    if (v < 27) {
      v += 27;
    }
    require(v == 27 || v == 28, "Invalid signature v value");
    return ecrecover(_ethSignedHash, v, r, s);
  }

}
```

Trong ví dụ trên, hàm `verify` băm giá trị `_messageHash` theo chuẩn được nêu trong EIP-191 @eip-191 rồi gọi hàm `recoverSigner` để khôi phục địa chỉ người ký từ giá trị băm và chữ ký.

Các dòng mã hợp ngữ trong hàm `recoverSigner` được dùng để tách giá trị `_sig` thành các giá trị $r$, $s$ và $v$. Với $v$ là giá trị giúp việc khôi phục địa chỉ người ký dễ dàng hơn. Nếu địa chỉ trả về từ hàm `ecrecover` khớp với đối số truyền vào tham số `_expectedSigner` của hàm `verify` thì chữ ký là hợp lệ.

Kẻ tấn công có thể xây dựng smart contract như sau:

```sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Attack{

  function manipulateSignature(bytes memory signature) public pure returns(bytes memory) {
    (uint8 v, bytes32 r, bytes32 s) = splitSignature(signature);

    uint8 manipulatedV = v % 2 == 0 ? v - 1 : v + 1;
    uint256 manipulatedS = modNegS(uint256(s));
    bytes memory manipulatedSignature = abi.encodePacked(r, bytes32(manipulatedS), manipulatedV);

    return manipulatedSignature;
  }

  function splitSignature(bytes memory sig) public pure returns (uint8 v, bytes32 r, bytes32 s) {
    require(sig.length == 65, "Invalid signature length");
    assembly {
      r := mload(add(sig, 32))
      s := mload(add(sig, 64))
      v := byte(0, mload(add(sig, 96)))
    }
    if (v < 27) {
      v += 27;
    }
    require(v == 27 || v == 28, "Invalid signature v value");
  }

  function modNegS(uint256 s) public pure returns (uint256) {
    uint256 n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141;        
    return n - s;
  }

}
```

Có thể thấy, hàm `manipulateSignature` tách các thành phần $r$, $s$ và $v$ từ `signature` thông qua hàm `splitSignature`. Sau đó, nó chỉnh sửa giá trị của $v$ sao cho nếu $v$ là chẵn thì trừ đi 1 còn nếu $v$ là lẻ thì cộng thêm 1. Giá trị $s$ sẽ được chỉnh sửa thành $-s mod n$ (được tính thông qua hàm `modNegS`). Cuối cùng, ba giá trị $r$, $s$ và $v$ được ghép lại thành chữ ký thông qua hàm `abi.encodePacked`.

Như vậy, nếu kẻ tấn công biết được một chữ ký hợp lệ thì có thể dùng hàm `manipulateSignature` để tạo ra một chữ ký hợp lệ khác.

## Cách khắc phục

Không dùng chữ ký số để xây dựng định danh của giao dịch dùng để chống tấn công lặp lại chữ ký số (@signature-replay). Lý do là vì kẻ tấn công có thể tạo ra một định danh khác sử dụng một chữ ký số khác dựa trên tính dễ uốn của chữ ký số nhưng vẫn thỏa được quá trình xác thực.

Cũng có thể sử dụng smart contract `ECDSA` của OpenZeppelin @openzeppelin-cryptography-ecdsa.
