# Weak Sources of Randomness from Chain Attributes

## Mô tả

Nhu cầu sinh số ngẫu nhiên là rất cần thiết cho một số ứng dụng, đặc biệt là các trò chơi cần sử dụng bộ sinh số giả ngẫu nhiên (pseudo-random number generator) để quyết định người chiến thắng. Tuy nhiên, việc tạo ra một hạt giống sinh số ngẫu nhiên đủ mạnh trong Ethereum là rất khó khăn.

Cụ thể, việc sử dụng giá trị `block.timestamp` làm hạt giống có thể không bảo mật vì giá trị này có thể được chỉnh sửa bởi miner (như trong @timestamp-dependency). 

Việc sử dụng `blockhash` hoặc `block.difficulty` cũng tương tự vì các giá trị này được kiểm soát bởi miner. Nếu thời gian để đào một block là ngắn, miner có thể đào thật nhiều block và chọn block có giá trị băm thỏa mãn điều kiện chiến thắng của smart contract rồi bỏ các block còn lại.

Ví dụ:

```sol
/*
 * @source: https://capturetheether.com/challenges/lotteries/guess-the-random-number/
 * @author: Steve Marx
 */

pragma solidity ^0.4.21;

contract GuessTheRandomNumberChallenge {
  
  uint8 answer;

  function GuessTheRandomNumberChallenge() public payable {
    require(msg.value == 1 wei);
    answer = uint8(keccak256(block.blockhash(block.number - 1), now));
  }

  function isComplete() public view returns (bool) {
    return address(this).balance == 0;
  }

  function guess(uint8 n) public payable {
    require(msg.value == 1 wei);

    if (n == answer) {
        msg.sender.transfer(2 wei);
    }
  }
  
}
```

Thông tin về số block (`block.number`) và thời gian của mà block được tạo ra (`now` - tương ứng với `block.timestamp` ở các phiên bản sau này của Solidity) đều được công khai nên kẻ tấn công có thể dễ dàng tái tạo được giá trị của `answer`.

## Cách khắc phục <weak-sources-of-randomness-from-chain-attributes-remediation>

Một số giải pháp sinh số ngẫu nhiên/giả ngẫu nhiên:

*Verifiable Random Function (VRF)*

Sử dụng các VRF @introduction-to-chainlink-vrf để tạo số ngẫu nhiên có thể xác thực. Với mỗi yêu cầu sinh số ngẫu nhiên, sẽ có một hoặc nhiều số ngẫu nhiên được tạo ra off-chain (bên ngoài blockchain) và đi kèm với chúng là các bằng chứng mật mã (cryptographic proof) cho biết cách mà các số ngẫu nhiên được hình thành. 

Bằng chứng mật mã sẽ được công khai và được xác thực on-chain trước khi các ứng dụng có thể sử dụng. Điều này đảm bảo các giá trị ngẫu nhiên không bị giả mạo hoặc thao túng bởi một thực thể nào đó.

*Commit-Reveal Scheme*

Cũng có thể dùng mô hình commit-reveal @atzei_2017_a. Mô hình này hoạt động như sau: mỗi thành viên tham gia vào việc tạo số ngẫu nhiên sẽ sinh ra một con số bí mật và công khai giá trị băm của số bí mật này kèm với một khoảng tiền đặt cọc. 
    
Sau một thời gian nhất định, các thành viên này sẽ phải công khai con số bí mật tương ứng với giá trị băm đã công khai trước đó. Số giả ngẫu nhiên sẽ được tính toán dựa trên những con số bí mật này. Nếu có một thành viên không công khai số bí mật, thành viên đó sẽ bị mất khoản tiền đặt cọc.

Một hiện thực của mô hình này trong thực tế là RANDAO @a2020_randao.

*Bitcoin Hashes*

Giá trị hash của Bitcoin cũng có thể được dùng làm hạt giống sinh số ngẫu nhiên bởi vì các block trong Bitcoin thường khó để đào hơn.
