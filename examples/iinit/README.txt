This OpenID plugin hashes the tokens if they are larger than 1024 bytes to avoid an irods limitation (packstruct error).
The same limitation applies to iinit, so after a successful iinit, the token needs to be hashed to enable subsequent i-commands to run successfully.
Run postiinit.py to fix .irodsA when needed.

If you have a pre-validated token and would like to avoid the interactive authentification using iinit -> retrieve URL -> authentificate -> hash
then modify your irods_environment.json with the irods_user_name provided by the token, save .irodsA with the content act=<token> and run hash_token.py.

