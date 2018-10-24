import requests
import jose.jws
import json
try:
    import flask
except:
    pass

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

def verify_flask_request_token():
    """Extracts a Bearer authentication token from the current flask
    request and verifies it using verify(). Returns the parsed token
    or None."""
    
    header = flask.request.headers.get('Authorization')
    if header is None: return None
    if not header.startswith("Bearer "): return None
    token = header[len("Bearer "):]
    return verify(token)
