package authz.product_policy
import data.products

default allow = false

allow {
  some user_name
  input.method == "POST"
  # use unification: user_name is copied from input. path
  ["api","products", user_name] = input.path 
  input.user_name == user_name
  
  #products[user_name].category_assistant == input.user_name
  #products[user_name].category_name = input.category_name
}

allow_list {
  input.method == "POST"
  products[_].category_assistant == input.user_name
}





