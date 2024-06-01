Here is a smart contract with Right-To-Left Override Control Character vulnerability:

```solidity
pragma solidity ^0.8.0;

contract RTLOVulnerable {
    string public message;

    function setMessage(string memory _message) public {
        message = _message;
    }
}
```

In this vulnerable smart contract, the `setMessage` function allows users to set the `message` variable to any string value. An attacker can exploit this vulnerability by using Right-To-Left Override Control Characters to manipulate the appearance of the string displayed in the `message` variable.

For example, an attacker could set the message to a string that includes Right-To-Left Override Control Characters to make the displayed message appear different from what is actually stored in the variable.

### Remediation:

To mitigate the Right-To-Left Override Control Character vulnerability, you can sanitize the input string to remove any control characters that may alter the appearance of the text. One way to sanitize the input is to use a function that checks for and removes any control characters before setting the message variable.

Here is an updated version of the smart contract with a sanitization function to prevent the vulnerability:

```solidity
pragma solidity ^0.8.0;

contract RTLOSecure {
    string public message;

    function setMessage(string memory _message) public {
        message = sanitizeString(_message);
    }

    function sanitizeString(string memory _str) internal pure returns (string memory) {
        bytes memory strBytes = bytes(_str);
        uint len = strBytes.length;
        bytes memory result = new bytes(len);
        uint resultIndex = 0;

        for (uint i = 0; i < len; i++) {
            if ((strBytes[i] & 0xFF) < 128) {
                result[resultIndex] = strBytes[i];
                resultIndex++;
            }
        }

        bytes memory finalResult = new bytes(resultIndex);
        for (uint j = 0; j < resultIndex; j++) {
            finalResult[j] = result[j];
        }

        return string(finalResult);
    }
}
```

In this updated smart contract, the `setMessage` function now calls the `sanitizeString` function before setting the `message` variable. The `sanitizeString` function removes any control characters that may be used for malicious purposes, ensuring that the displayed message is safe from Right-To-Left Override Control Character attacks.