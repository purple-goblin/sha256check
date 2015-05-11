# sha256check

Checks whether the HTTP and FTP mirrors for OpenBSD are reporting the same 
sha256 for the 32-bit and 64-bit versions of `install.iso`. 

Output looks like this:

```
Searching ftp://mirrors.ucr.ac.cr/OpenBSD/
  Match for 32-bit in ftp://mirrors.ucr.ac.cr/OpenBSD/5.6/i386/SHA256
  Match for 64-bit in ftp://mirrors.ucr.ac.cr/OpenBSD/5.6/amd64/SHA256
```

Two defective mirrors are excluded:
* mirrors.isu.net.sa/pub/ftp.openbsd.org
* www.obsd.si/pub/OpenBSD

Of course, a clever attacker might be running `s/<actual sha256>/<evil sha256>/g`
on all your traffic. 
