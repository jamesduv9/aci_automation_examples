provider "aci" {
  username = "expert"
  password = "1234QWer!"
  url = "https://192.168.1.251"
}

resource "aci_tenant" "my-tenants" {
  for_each = {for key, value in var.data.tenants: key => value}
  name = "${each.key}"
  description = "${each.value.description}"
}

resource "aci_vrf" "my-vrfs" {
  for_each = {for key, value in var.data.vrfs: "${value.name}_${value.tenant}" => value}
  name = each.value.name
  tenant_dn = aci_tenant.my-tenants["${each.value.tenant}"].id
}

resource "aci_bridge_domain" "my-bridge_domains" {
  for_each = {for key, value in var.data.bridge_domains: key => value}
  name = each.value.name
  tenant_dn = aci_tenant.my-tenants["${each.value.tenant}"].id
  relation_fv_rs_ctx = aci_vrf.my-vrfs["${each.value.vrf}_${each.value.tenant}"].id
}

resource "aci_subnet" "my-subnets" {
  for_each = {for key, value in var.data.subnets: key => value}
  parent_dn = aci_bridge_domain.my-bridge_domains["${each.value.bridge_domain_id}"].id
  ip = "${each.value.ip}"
}

resource "aci_contract" "my-contracts" {
  for_each = {for key, value in var.data.contracts: key => value}
  tenant_dn = aci_tenant.my-tenants["${each.value.tenant}"].id
  name = "${each.value.name}"
}

resource "aci_filter" "my-filters" {
  for_each = {for key, value in var.data.filters: key => value }
  name = each.value.name
  tenant_dn = aci_tenant.my-tenants["${each.value.tenant}"].id
}

resource "aci_filter_entry" "my-filter-entries" {
  for_each = {for filter in local.filter_entries: filter.key => filter.value}
  filter_dn = aci_filter.my-filters["${split("_", each.key)[0]}"].id
  name = "${each.value.name}"
  d_to_port = "${each.value.destination_port}"
  d_from_port = "${each.value.source_port}"
  ether_t = "${each.value.ip_protocol}"
  prot = "${each.value.l4_protocol}"
}

resource "aci_application_profile" "my-app-profiles" {
  for_each = {for app_key, app_value in var.data.app_profiles: app_key => app_value}
  tenant_dn = aci_tenant.my-tenants["${each.value.tenant}"].id
  name = "${each.value.name}"
}

resource "aci_application_epg" "my-epgs" {
  for_each = {for epg_key, epg_values in var.data.epgs: epg_key => epg_values}
  application_profile_dn = aci_application_profile.my-app-profiles["${each.value.app_profile_id}"].id
  name = "${each.value.name}"
  relation_fv_rs_bd = aci_bridge_domain.my-bridge_domains["${each.value.bridge_domain_id}"].id
}

//Looks like the aci_epg_to_contract requires the contract to have a subject with the associated provider_to_consumer or consumer to provider block

resource "aci_contract_subject" "my-subjects" {
  for_each = {for subject_key, subject_value in var.data.contract_subjects: subject_key => subject_value}
  contract_dn = aci_contract.my-contracts["${each.value.contract_id}"].id
  name = "${each.value.name}"
  # apply_both_directions = "${each.value.apply_both_directions}"
  relation_vz_rs_subj_filt_att = toset([aci_filter.my-filters["${each.value.filter_id}"].id])
}
//Bug in 0.7, not sure how to proceed.
//unknown property value uni/tn-test_tenant1/ap-APP_PROFILE001/rscons-CONTRACT001, name dn, class fvRsCons [(Dn0)] Dn0=, 

# resource "aci_epg_to_contract" "my-epg-contract-relation" {
#   for_each = {for epg_key, epg_value in var.data.epgs: epg_key => epg_value}
#   application_epg_dn = aci_application_profile.my-app-profiles["${each.value.app_profile_id}"].id
#   contract_dn = aci_contract.my-contracts["${each.value.contract_id}"].id
#   contract_type = "consumer"
# }