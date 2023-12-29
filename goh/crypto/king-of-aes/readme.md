- pre-requisite: `guess the algorithm`

- ciphertext: `hUgusplc65XYsNoPDc7DbJsmfa2ZQwuEtclNmUQPn6RwGtnVoL4sE75fygV2wah1`
- key: `LicielaWasHere` (from previous chall, `guess the algorithm`)
- chall description gives hint on IV which does not make sense to me
    > the IV is a combination of 2 ascii characters but when combined and convert into digit it becomes 16 digit
- fortunately on `aes-256-cfb`, the `IV` is only used for the first block, while the rest rely on the key

- not sure why only this website worked for me: `https://encode-decode.com/aes-256-cfb-encrypt-online/`
- obtained plaintext: `�>��U�)��t�k��ce0FFNV8xc19OMFRfVGg0dF9INEFSRH0=`
- as can be seen, the beginning is not decoded properly, but the trailing seems to be a base64 string
- since 4 chars of b64 when decoded equals to 1 char, we keep taking a set of 4 chars from the end that has no gibberish chars
- the valid b64 string: `e0FFNV8xc19OMFRfVGg0dF9INEFSRH0=` -> `{AE5_1s_N0T_Th4t_H4ARD}`
- i guess i am lucky to get just enough substring of the flag to submit :p
