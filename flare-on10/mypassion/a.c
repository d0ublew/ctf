__int64 __fastcall sub_140002C00(BYTE *pbData) {
    __int64 v2;               // r8
    unsigned int v3;          // ebx
    DWORD LastError;          // eax
    MACRO_CRYPT_MODE pbDataa; // [rsp+48h] [rbp+10h] BYREF
    HCRYPTHASH phHash;        // [rsp+50h] [rbp+18h] BYREF

    phHash = 0i64;
    if (!CryptAcquireContextW(&hProv, 0i64, 0i64, 0x18u, 0u) &&
        !CryptAcquireContextW(&hProv, 0i64, 0i64, 0x18u, 8u))
        goto LABEL_12;
    if (!CryptCreateHash(hProv, CALG_SHA_256, 0i64, 0, &phHash))
        goto LABEL_12;
    v2 = -1i64;
    do
        ++v2;
    while (pbData[v2]);
    if (!CryptHashData(phHash, pbData, v2, 0) ||
        !CryptDeriveKey(hProv, CALG_AES_256, phHash, 0, &hKey) ||
        (pbDataa = CRYPT_MODE_CBC,
         (v3 = CryptSetKeyParam(hKey, KP_MODE, (const BYTE *)&pbDataa, 0)) ==
             0)) {
    LABEL_12:
        LastError = GetLastError();
        ExitProcess(LastError);
    }
    if (phHash)
        CryptDestroyHash(phHash);
    return v3;
}
