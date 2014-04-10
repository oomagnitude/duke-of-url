duke-of-url
===========

Predicting next URLs from browsing history using NuPIC

# Dataset

## Chrome on Mac

Export chrome history into pipe-delimited data file called history.log

```
/usr/bin/sqlite3 ~/Library/Application\ Support/Google/Chrome/Default/History > history.log <<EOF
> select * from urls;
> EOF
```

Names of fields in URLs table can be grabbed like this, once in sqlite:

```
/usr/bin/sqlite3 ~/Library/Application\ Support/Google/Chrome/Default/History
> PRAGMA table_info(urls);
```

## TLDs

Original source:
https://mxr.mozilla.org/mozilla/source/netwerk/dns/src/effective_tld_names.dat?raw=1