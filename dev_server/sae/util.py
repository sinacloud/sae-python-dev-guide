
from sae_signature import get_signature, get_signatured_headers

def half_secret(d, k):
    """Hidden part of the secret"""
    l = len(d[k])
    if l > 2:
        d[k] = d[k][:2] + '*' * (l - 2)
    else:
        d[k] = '*' * l

def protect_secret(d):
    for k, v in d.items():
        if 'KEY' in k:
            half_secret(d, k)
