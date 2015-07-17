# generate csr
openssl genrsa -des3 -out example.org.key 2048

# generate key
openssl req -new -key example.org.key -out example.org.csr

# drop passphrase
cp example.org.key example.org.key.orig example.org.key.bak
openssl rsa -in example.org.key.orig -out example.org.key
rm example.org.key.orig