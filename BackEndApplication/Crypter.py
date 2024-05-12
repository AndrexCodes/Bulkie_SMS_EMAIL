import rsa
import base64
import json

def PassEncrypter(password):
    password = str(password)
    private_key, public_key = rsa.newkeys(512)
    cypher_text = rsa.encrypt(password.encode('utf-8'), public_key)
    private_key = base64.b64encode(public_key.save_pkcs1()).decode('utf-8')
    cypher_text = base64.b64encode(cypher_text).decode('utf-8')
    return {
        "cypher_text": cypher_text,
        "privateKey": private_key
    }

def PassDecrypter(cypher_text, private_key):
    privateKey = rsa.PrivateKey.load_pkcs1(base64.b64decode(private_key))
    cypher_text = base64.b64decode(cypher_text)
    actual_text = rsa.decrypt(cypher_text, privateKey).decode()
    return str(actual_text)

