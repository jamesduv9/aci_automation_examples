# ACI Automation examples

For DevNet Expert studies. Given an input json file, create tenants, vrfs, bds, aps, epgs, contracts, filters. Same output from ACI, Terraform, or direct API requests. Validated with pytest.

The structure of the objects in the json file vary for practice, added complexity is intentional

The actually configuration that this automation applies on cisco ACI is wrong and will produce no meaningful results, the focus of this practice is on the automation, not the correct configuration of ACI