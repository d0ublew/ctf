# solution

arrow key: `LLURULDUL`
question: `gimme flag pls?`


function snippet
```c
  if ( *(_BYTE *)(v1 + 345) )
  {
    v14 = v5[5];
    v15 = v5;
    if ( v14 >= 0x10 )
      v15 = (_BYTE *)*v5;
    if ( *v15 == 'L' )
    {
      v16 = v5;
      if ( v14 >= 0x10 )
        v16 = (_BYTE *)*v5;
      if ( v16[1] == 'L' )
      {
        v17 = v5;
        if ( v14 >= 0x10 )
          v17 = (_BYTE *)*v5;
        if ( v17[2] == 'U' )
        {
          v18 = v5;
          if ( v14 >= 0x10 )
            v18 = (_BYTE *)*v5;
          if ( v18[3] == 'R' )
          {
            v19 = v5;
            if ( v14 >= 0x10 )
              v19 = (_BYTE *)*v5;
            if ( v19[4] == 'U' )
            {
              v20 = v5;
              if ( v14 >= 0x10 )
                v20 = (_BYTE *)*v5;
              if ( v20[5] == 'L' )
              {
                v21 = v5;
                if ( v14 >= 0x10 )
                  v21 = (_BYTE *)*v5;
                if ( v21[6] == 'D' )
                {
                  v22 = v5;
                  if ( v14 >= 0x10 )
                    v22 = (_BYTE *)*v5;
                  if ( v22[7] == 'U' )
                  {
                    v23 = v5;
                    if ( v14 >= 0x10 )
                      v23 = (_BYTE *)*v5;
                    if ( v23[8] == 'L' )
                    {
                      v24 = (const char *)(v1 + 248);
                      if ( *(_DWORD *)(v1 + 268) >= 0x10u )
                        v24 = *(const char **)v24;
                      if ( !strncmp(v24, (const char *)(v1 + 92), 0xFu) ) // v1[92] = "gimme flag pls?"
                      {
                        sub_271220(&v25, v5);
                        sub_271A10((char *)v1, v25, v26, v27, v28, (int)v29, v30);
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```
