from firebase_admin import credentials, initialize_app


def initialize_firebase():
    config = {
    "type": "service_account",
    "project_id": "medic-4c92e",
    "private_key_id": "638b71edb3666e59ce93fa29f65fe31f73fda328",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCKDNHso0n6Qyyn\nNznnpA4LPN8tm0+z4NOEBcV3F+xCkYNAxTZ9V+XeDUFEtHMg1AZu40EPdOKxHl1v\nyLY9WgoKNDeKches6iAduQXfOBWGwA3fXIWzEfVx+tdpg0QfNwK+vw2wDYVyaDzy\n1RQQ7Jqd9N2RVFO0JALSYJElI2l+BZ8ukrcisVefkt3WTsT7vRYfn08+lnkMc3AB\nOdn2DUMyYkR7jHRPET9cfg2W+bbDTi11gWUoJnW3/r98IedF/PYQm9/zaGXf4WNk\n69Uo6bI3Js+e9KoKmr/NhdxLkjKxSPaTCce333PLFza6zzppoqtYhzgJF38gl1t9\nhk3V+bLNAgMBAAECggEAOU+kMPkDQ8XyekMXo358pBaz0oO5XYR3W0ZoGY6Rc3tk\ngZW+DuBYWkynbYX6i8TqHMv0nR2Z5Q0lnjw1yBeitmTCMBQ4lv0lsyE2elqWuTfv\nKm0HRnWsr5KDLlckB093sMexP4cFgR8cOnXSXEpV0ECxYV2gWFdg4oTbjQ78Ayhn\nL/0Cs14TGD6ULSpu7mb/KdoeMfPEkFMTc2h2zTOXzKSgtY0hYKP+gtmCRp/pr3mN\nlS38RsTbQAx016HelslIJex+qA4x65xIQS9z4zEQ+ktAb1daoxSiXH7SMW4QntDr\nqOo2I1w21fhv8Ewn7yUTcCnpQ1SFR8B1b6K+jVOrAwKBgQDAlT03XMpEk75bsFZT\n9UVn2aeJnjAdQBa14Af0MaivEO0c+9C1bSH7xy9IgbxZdT67Vebsp0A8+nClasct\naUKYBtRb1aTZH+Hcx7VddPiO1k1FUbSAa5tkH7/9dBqOjLI3h/BxhyOUKtJvgsN9\ng556wZUtAd0/lGA6fuZjyJHPqwKBgQC3gnQnBHr92o/jV75zriFT1XNKWNHmilPM\nxPZatR0GzrRlDB/ZuDwA9ovsb4E62rOgOLOkAlXWdmpEnX9Oii2ID/SDwhxMHZM8\nqb03M6EonaeE2ShWuXyIl54I9Gq8bKYKhUOe+W2cZVKFaed2nlsk1KNcDZN4Ow8a\n7ynoSsxvZwKBgCcHl+p6cbvIPZITgMtvL+vGHsAzQQkMjg26I6KH1en1AjkXh8rd\nHUALtDd7o5J1worw8+YOV2SEVQQRSeCYLpjk+XDLMaeXYI0AJG+WXzGDmRFtZ6mH\nJWz7SkuxlhhBx3Sdpks72igTLabP15K+dAXo6bS/ZfmWtpHkWgjrAzIVAoGAIRdr\nLqYGL8S78bke5OlfpSh2k8+UekgzeFeEPTMvusyHhzk6fR5V466R6N7qpNxPS/Mt\nocOyCuxrmVf1XwpXz5Ng+mmEhM1IgcXyEwRCaXqUfMZUGd9074S3wNGidbv57Se+\n2+oKtAspaFmCncdMlEWr96uTDjlILgk2u2bRmr0CgYAoeSbEW9Y0msyzBLzbaFWB\n1za0OvBEvIqzP1xyClAEa7I+nt7lRHnGvix40Fvbfm29yX0fMc0cUt+8IAkiHIBT\nEv8QhbOeJshvGHpwqlmCCJQtqGI1XQv+xzzgYR9XBODBNnl2u/JWTOw6atzQaOAK\nayM6snG58vQfQQu/OshogA==\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-fbsvc@medic-4c92e.iam.gserviceaccount.com",
    "client_id": "117144840079574525632",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40medic-4c92e.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
    }
    cred = credentials.Certificate(config)
    initialize_app(cred)
