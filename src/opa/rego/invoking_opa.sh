#Run as server
opa run -w -s product_policy_data.json product_policy.rego

#Test policies
opa test  product_policy_data.json product_policy.rego product_policy_test.rego

#Interactive shell
opa run -w  product_policy_data.json product_policy.rego input.rego