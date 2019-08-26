
package authz.product_policy
product_policy_data := {
  
    "Aidan": {"sub_category": ["Ready meals", "Fresh soup", "Dairy & eggs"],"category_name": "Dairy"},
    "Anne": {"sub_category": ["Ready meals", "Fresh soup", "Dairy & eggs"],"category_name": "Bakery"},
    "Claire":{"sub_category": ["Cider", "Wine", "Beer"],"category_name": "Beer"}
}

test_not_allow_with_anne_dairy {
    not allow_cat_assistant_resource with input as {
        "category_name": "Dairy",
        "path" :["api","products","Anne"],
        "user_name": "Anne",
        "method": "POST"
        }  
        with data.product_policy_data as product_policy_data
}

test_allow_with_anne_bakery {
    product_policy.allow_cat_assistant_resource with input as {
        "category_name": "Bakery",
        "path" :["api","products","Anne"],
        "user_name": "Anne",
        "method": "POST"
        }  
      with data.product_policy_data as product_policy_data
}

test_allow_with_anne_calling_jim_bakery {
    not allow_cat_assistant_resource with input as {
        "category_name": "Bakery",
        "path" :["api","products","Jim"],
        "user_name": "Jim",
        "method": "POST"
        }  
      with data.product_policy_data as product_policy_data
}

# 