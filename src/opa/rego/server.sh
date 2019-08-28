opa run -w -s opa/rego/product_policy_data.json opa/rego/product_policy.rego
opa test  product_policy_data.json product_policy.rego product_policy_test.rego