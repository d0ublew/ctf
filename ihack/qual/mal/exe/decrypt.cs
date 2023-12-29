using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Reflection;
using System.Resources;
using System.Security.Cryptography;
using System.Text;
using System.Threading;

public class C {
    static void Main() {
        Console.WriteLine("Hello");
        C.DecryptFile("./flag.txt.1337ransom", "hektheplanet");
        Console.WriteLine("Done");
    }

    public static void DecryptFile(string string_0, string string_1) {
        byte[] bytesToBeDecrypted = File.ReadAllBytes(string_0);
        byte[] bytes1 = Encoding.UTF8.GetBytes(string_1);
        byte[] hash = SHA256.Create().ComputeHash(bytes1);
        byte[] bytes2 = C.AES_Decrypt(bytesToBeDecrypted, hash);
        File.WriteAllBytes(string_0, bytes2);
        File.Move(string_0, string_0 + ".decrypted");
    }

    public static byte[] AES_Decrypt(byte[] bytesToBeDecrypted, byte[] passwordBytes) {
      byte[] salt = new byte[8] {
        (byte) 1,
        (byte) 2,
        (byte) 3,
        (byte) 4,
        (byte) 5,
        (byte) 6,
        (byte) 7,
        (byte) 8
      };
      using (MemoryStream memoryStream = new MemoryStream()) {
        using (RijndaelManaged rijndaelManaged = new RijndaelManaged()) {
          rijndaelManaged.Padding = PaddingMode.PKCS7;
          rijndaelManaged.KeySize = 256;
          rijndaelManaged.BlockSize = 128;
          Rfc2898DeriveBytes rfc2898DeriveBytes = new Rfc2898DeriveBytes(passwordBytes, salt, 1000);
          rijndaelManaged.Key = rfc2898DeriveBytes.GetBytes(rijndaelManaged.KeySize / 8);
          rijndaelManaged.IV = rfc2898DeriveBytes.GetBytes(rijndaelManaged.BlockSize / 8);
          rijndaelManaged.Mode = CipherMode.CBC;
          using (CryptoStream cryptoStream = new CryptoStream((Stream) memoryStream, rijndaelManaged.CreateDecryptor(), CryptoStreamMode.Write)) {
            cryptoStream.Write(bytesToBeDecrypted, 0, bytesToBeDecrypted.Length);
            cryptoStream.FlushFinalBlock();
          }
          return memoryStream.ToArray();
        }
      }
    }
}
