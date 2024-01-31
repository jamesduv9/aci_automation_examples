variable "data" {
  type = object({
    tenants = map(object({
      description = string
    }))
    vrfs = map(object({
      tenant = string
      name   = string
    }))
    bridge_domains = map(object({
      tenant = string
      name   = string
      vrf    = string
    }))
    subnets = map(object({
      bridge_domain_id = string
      ip               = string
    }))
    contracts = map(object({
      tenant = string
      name   = string
    }))
    filters = map(object({
      tenant = string
      name   = string
      entries = list(object({
        destination_port = string
        source_port      = string
        ip_protocol      = string
        l4_protocol      = string
        name             = string
      }))
    }))
    app_profiles = map(object({
      tenant = string
      name   = string
    }))
    epgs = map(object({
      app_profile_id   = string
      contract_id      = string
      bridge_domain_id = string
      name             = string
    }))
    contract_subjects = map(object({
        contract_id = string
        name = string
        apply_both_directions = string
        filter_id = string
    }))
  })
}

locals {
  filter_entries = flatten([
    for filter_key, filter_value in var.data.filters : [
      for entry in filter_value.entries : {
        key   = "${filter_key}_${entry.name}"
        value = entry
      }
    ]
  ])
}