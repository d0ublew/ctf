#!/usr/bin/env python3

"""
com/secure/itsonfire/MessageWorker.java
```
            String str = remoteMessage.getData().get(getString(R.string.key));
            if (str != null) {
                NotificationManager notificationManager = (NotificationManager) getSystemService("notification");
                NotificationChannel notificationChannel = new NotificationChannel(getString(R.string.oc), getString(R.string.mc), 4);
                notificationChannel.setDescription(getString(R.string.nc));
                Intrinsics.checkNotNull(notificationManager);
                notificationManager.createNotificationChannel(notificationChannel);
                NotificationCompat.Builder builder = new NotificationCompat.Builder((Context) this, getString(R.string.oc));
                builder.setSmallIcon(17301595);
                builder.setContentTitle(getString(R.string.title));
                builder.setWhen(System.currentTimeMillis());
                builder.setContentText(getString(R.string.bd));
                builder.setAutoCancel(true);
                builder.setFullScreenIntent(C1188c.f529a.mo21026a(this, str), true); // <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                startForeground(2102, builder.build());
                return;
            }
```
"""

from binascii import crc32

from Crypto.Cipher import AES

raw_path = "./ItsOnFire/res/raw"

with open(f"{raw_path}/iv.png", "rb") as f:
    data1 = f.read()

with open(f"{raw_path}/ps.png", "rb") as f:
    data2 = f.read()


iv = b"abcdefghijklmnop"
c2 = b"https://flare-on.com/evilc2server/report_token/report_token.php?token="
w1 = b"wednesday"
s = c2[4:10] + w1[2:5]
key = (str(crc32(s)) * 2).encode()[:16]

cipher1 = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)

with open("./iv.png", "wb") as f:
    f.write(cipher1.decrypt(data1))

cipher2 = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
with open("./ps.png", "wb") as f:
    f.write(cipher2.decrypt(data2))
