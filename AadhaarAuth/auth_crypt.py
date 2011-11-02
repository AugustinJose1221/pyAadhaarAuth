#Copyright (C) 2011 by Venkata Pingali (pingali@gmail.com) & TCS 
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

import sha, md5, os, sys
from M2Crypto import RSA, BIO, Rand, m2, EVP, X509, ASN1
from M2Crypto.ASN1 import ASN1_UTCTIME 
import base64 

class AuthCrypt():
    
    def __init__(self, pub_key, priv_key):
        self._public_key = pub_key
        self._private_key = priv_key
        return 
    
    def get_cert_expiry(self): 
        x509 = X509.load_cert(self._public_key)
        return x509.get_not_after().__str__()  

    # Returns encrypted and base64 encoded data
    def encrypt(self, data):
        if (data == None or data == ""):
            raise Exception("No data to encrypt") 
        
        x509 = X509.load_cert(self._public_key)
        rsa = x509.get_pubkey().get_rsa()
        enc_data=rsa.public_encrypt(data, RSA.pkcs1_padding)
        #res = enc_data.encode('base64') 
        res = base64.b64encode(enc_data)
        #print "\"%s\"" % (res)
        return res 
    
    # Decryption of data requires private key. Assumes the data is 
    # base64 encoded. 
    def decrypt(self, data):

        if (data == None or data == ""):
            raise Exception("No data to encrypt") 
        
        dec_data = base64.b64decode(data)
        rsa = RSA.load_key(self._private_key) 
        res = rsa.private_decrypt(dec_data, RSA.pkcs1_padding)
        #print "\"%s\"" % (res)
        return res 
    
    def test(self, show=True): 
        
        data = "39jsjsfdhdshfd" # some test data
        if show:
            print "Encryption payload: ", data
        enc_data = self.encrypt(data)
        if show:
            print "Encrypted base64 encoded data:" 
            print enc_data 
        dec_data = self.decrypt(enc_data)
        if show:
            print "Decrypted data" 
            print dec_data
        
        if (data != dec_data): 
            raise Exception("Encryption is not functioning correctly")
        else:
            if show:
                print "Encrytion payload and decrypted data matched" 
        return True 

if __name__ == '__main__':
    
    auth = AuthCrypt("fixtures/public.pem", "fixtures/public.pem") 
    print "certificate expiry = ", auth.get_cert_expiry()
    auth.test() 