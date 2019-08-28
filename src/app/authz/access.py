import requests
import json
from src.app.authz import opa as opa

def is_access_allowed(input, policy):
  print('--is_access_allowed--')
  url = "http://opa:8181/v1/data/authz/product_policy/" +  policy
  resp = requests.post(url, 
    json =input)
  print(resp.json())
  return resp.json().get('result',{})

def compile(input):
  result = opa.compile(q=input['query'], 
              input=input['input'], 
              unknowns=input['unknowns'])
  print(repr(result))
  sql = opa.splice(SELECT='products.*', FROM='products', decision=result)
  return sql
  

