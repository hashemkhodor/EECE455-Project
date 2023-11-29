""""""
# Rabin Miller test for reducibility
# https://en.wikipedia.org/wiki/Factorization_of_polynomials_over_finite_fields#Rabin.27s_test_of_irreducibility
# from sage.all import *
import requests

url = "https://sagecell.sagemath.org/"
code = "2 + 2"
data = {"code": code}

response = requests.post(url, data=data)

print("Status Code:", response.status_code)
print("Response Content:", response.text)
