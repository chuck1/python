
#cat $1 | base64 -d | openssl zlib -d | jsonlint --format
cat $1 | base64 -d | python -c "import zlib,sys;sys.stdout.write(zlib.decompress(sys.stdin.read()))" > $1.decoded

