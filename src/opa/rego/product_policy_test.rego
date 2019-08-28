
package authz.product_policy

import data.authz.product_policy as product_policy
import data.roles
# Allow access to static resource for Anne
test_allow_static_with_anne{
    product_policy.allow_static with input as {
        "user_name": "Anne",
        "method": "GET",
        "path": ["api","products","Anne"]
        }  
      with data.roles as roles
}
# Allow access to static resource for Rhys
test_allow_static_with_rhys{
    product_policy.allow_static with input as {
        "user_name": "Rhys",
        "method": "GET",
        "path": ["api","products","Rhys"]
        }  
      with data.roles as roles
}
# Allow access to static resource for Jimmy
test_allow_static_with_jimmy{
    product_policy.allow_static with input as {
        "user_name": "Jimmy",
        "method": "GET",
        "path": ["api","products","Jimmy"]
        }  
      with data.roles as roles
}

# Don't allow access to static resource for others
test_not_allow_static_with_Others{
    not product_policy.allow_static with input as {
        "user_name": "Others",
        "method": "GET",
        "path": ["api","products","Others"]
        }  
      with data.roles as roles
}