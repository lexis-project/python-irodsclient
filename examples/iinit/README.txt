This OpenID plugin hashes the tokens if they are larger than 1024 bytes to avoid an irods limitation (packstruct error).
The same limitation applies to iinit, so after a successful iinit, the token needs to be hashed to enable subsequent i-commands to run successfully.
Run postiinit.py to fix .irodsA when needed.
