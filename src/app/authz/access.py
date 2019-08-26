import requests
import json
from src.app.authz import opa as opa

def is_access_allowed(input):
  
  resp = requests.post("http://opa:8181/v1/data/authz/product_policy/allow", 
    json =input)
  print(resp.json())
  return resp.json().get('result',{})

def compile(input):
  result = opa.compile(q=input['query'], 
              input=input['input'], 
              unknowns=input['unknowns'])
  sql = opa.splice(SELECT='products.*', FROM='products', decision=result)
  return sql
  

