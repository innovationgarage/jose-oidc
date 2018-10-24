import requests
import jose.jws
import json

def verify(token):
    """Verifies a JWS token, returning the parsed token if the token has a
    valid signature by the key provided by the key of the OpenID
    Connect server stated in the ISS claim of the token. If the
    signature does not match that key, None is returned.
    """

    unverified_token_data = json.loads(jose.jws.get_unverified_claims(token))
    jwks_uri = requests.get("%s/.well-known/openid-configuration" % unverified_token_data["iss"]).json()["jwks_uri"]
    keys = requests.get(jwks_uri).json()["keys"]

    for key in keys:
        try:
            verified_token_data = json.loads(
                jose.jws.verify(token, key, [key["alg"]]))
        except:
            pass
    else:
        return verified_token_data
    return None
