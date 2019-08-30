package authz.product_policy
import data.products
import data.roles

default allow_static = false
default allow = false
default allow_list = false
default test_policy = false

allow_static {
  some user_name
  input.method == "GET"
  roles["StaticResource"].names[_]=input.user_name
  ["api","products", user_name] = input.path 
  user_name == input.user_name
}

allow_list_check{
  input.method == "POST"
  input.user_name == input.resource_name
}

allow_list_check{
  input.method == "POST"
  roles["Admin"].names[_] == input.user_name
}

allow_list {
  input.method == "POST"
  products[_].category_assistant = input.resource_name
}





