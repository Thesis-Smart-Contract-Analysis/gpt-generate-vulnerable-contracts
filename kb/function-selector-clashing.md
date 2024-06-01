# Function Selector Clashing

## Mô tả

EVM sẽ dựa vào 4 byte đầu tiên trong dữ liệu của một giao dịch gọi hàm để thực thi hàm tương ứng. Tuy nhiên, 4 byte này dễ bị đụng độ giá trị băm và có thể dẫn đến việc smart contract thực thi một hàm nào đó mà người dùng không mong muốn.

Xét proxy contract ở @proxy-pattern[phụ lục] với logic contract có dạng như sau @a2019_beware-of-the-proxy-learn-how-to-exploit-function-clashing:

```sol
pragma solidity ^0.5.0;

import "openzeppelin-eth/contracts/token/ERC20/ERC20Burnable.sol";
import "openzeppelin-eth/contracts/token/ERC20/ERC20Detailed.sol";
import "zos-lib/contracts/Initializable.sol";

contract BurnableToken is Initializable, ERC20Burnable, ERC20Detailed {

  function initialize(
    string memory name,
    string memory symbol,
    uint8 decimals,
    uint256 initialSupply
  ) 
    public 
    initializer
  {
    super.initialize(name, symbol, decimals);
    _mint(msg.sender, initialSupply);
  }
  
}
```

Smart contract `ERC20Burnable` @openzeppelin-contracts-token-erc20-extensions-erc20-burnable.sol có hàm `burn` như sau:

```sol
import {ERC20} from "../ERC20.sol";
import {Context} from "../../../utils/Context.sol";

abstract contract ERC20Burnable is Context, ERC20 {

    // ...
    function burn(uint256 value) public virtual {
      _burn(_msgSender(), value);
    }
    // ...
    
}
```

Kẻ tấn công có thể thiết lập một hàm backdoor giúp rút ETH của người dùng ở trong proxy contract như sau @a2019_beware-of-the-proxy-learn-how-to-exploit-function-clashing:

```sol
pragma solidity ^0.5.0;

contract Proxy {

  address public proxyOwner;
  address public implementation;

  // ...
  function collate_propagate_storage(bytes16) external {
    implementation.delegatecall(abi.encodeWithSignature(
        "transfer(address,uint256)", proxyOwner, 1000
    ));
  }
    
}
```

Giả sử có một người dùng sử dụng smart contract `Proxy` của kẻ tấn công để gọi hàm `burn` của `ERC20Burnable`. Khi người dùng gọi hàm `burn`, 4 byte đầu tiên trong giao dịch gọi hàm `burn` sẽ là `0x42966c68`. Tuy nhiên, 4 byte đầu tiên trong giá trị băm của hàm `collate_propagate_storage` cũng là `0x42966c68`. 

Theo nguyên tắc, EVM sẽ thực thi hàm có giá trị băm của signature khớp với 4 byte này ở trong proxy contract. Dẫn đến, hàm `collate_propagate_storage` sẽ được thực thi thay vì hàm fallback.

## Cách khắc phục

Điều kiện của lỗ hổng là phải có sự tồn tại của proxy contract bởi vì trình biên dịch sẽ phát hiện ra hai hàm trong cùng một smart contract có 4 byte đầu trong giá trị băm trùng nhau.

Ngoài ra, có thể sử dụng một số công cụ phân tích chẳng hạn như Slither @slither-upgradeability để phát hiện lỗ hổng này.

Người dùng cũng nên xem xét mã nguồn của proxy contract một cách cẩn thận trước khi sử dụng.
