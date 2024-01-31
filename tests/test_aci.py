import requests
import pytest
from pprint import pprint


def test_tenants_exist(aci_session, instance_data, aci_data):
    """
    Validate tenants provided in the aci_data exist in the topology
    """
    for tenant_name, tenant_values in aci_data.get("tenants").items():
        url = f'https://{instance_data["aci_ip"]}/api/class/fvTenant.json?query-target-filter=eq(fvTenant.name, "{tenant_name}")'
        current_tenants = aci_session.get(url).json()
        imdata = current_tenants.get("imdata")[0].get(
            'fvTenant').get('attributes')
        assert current_tenants.get("totalCount") == '1'
        assert tenant_values.get("description") == imdata.get("descr")


def test_vrf_tenant_valid(aci_data):
    """
    Check to see if the tenants provided in vrfs exist in aci_data 
    """
    for vrfvalues in aci_data.get("vrfs").values():
        assert any(tenant_key for tenant_key in aci_data.get("tenants").keys()
                   if vrfvalues.get("tenant") == tenant_key)


def test_vrfs_exist(aci_session, instance_data, aci_data):
    """
    Validates specific VRFs set in specific tenants are defined
    """
    for vrf_values in aci_data.get("vrfs").values():
        url = f'https://{instance_data["aci_ip"]}/api/class/fvTenant.json?rsp-subtree-include=no-scoped&rsp-subtree=children&query-target-filter=eq(fvTenant.name, "{vrf_values["tenant"]}")&rsp-subtree-filter=eq(fvCtx.name, "{vrf_values["name"]}")&rsp-subtree-class=fvCtx'
        current_vrfs = aci_session.get(url).json()
        assert current_vrfs.get("totalCount") == "1"
        assert current_vrfs.get("imdata", {})[0].get("fvCtx", {}).get(
            "attributes", {}).get("name") == vrf_values["name"]


def test_bd_vrf_valid(aci_data):
    """
    Validate bds are assoicated to an existing VRF
    """
    for bd_values in aci_data.get("bridge_domains").values():
        assert any(vrf for vrf in aci_data.get("vrfs").values() if vrf.get(
            'name') == bd_values.get('vrf'))
        assert any(tenant_key for tenant_key in aci_data.get("tenants").keys()
                   if bd_values.get('tenant') == tenant_key)


def test_bds_exist(aci_session, instance_data, aci_data):
    """
    Validate the bd is created in aci
    """
    for bd_values in aci_data.get("bridge_domains").values():
        url = f'https://{instance_data["aci_ip"]}/api/mo/uni/tn-{bd_values.get("tenant")}.json?query-target=self&rsp-subtree=full&rsp-subtree-filter=and(eq(fvCtx.name, "{bd_values.get("vrf")}")eq(fvBD.name, "{bd_values.get("name")}")&rsp-subtree-class=fvBD&rsp-subtree-include=no-scoped'
        current_bds = aci_session.get(url).json()
        assert current_bds.get("totalCount") == "1"


def test_subnets_exist(aci_session, aci_data, instance_data):
    """
    Validate provided subnets exist with correct attributes
    """
    for subnet_values in aci_data.get("subnets").values():
        bd = aci_data.get("bridge_domains").get(subnet_values.get("bridge_domain_id"))
        url = f'https://{instance_data["aci_ip"]}/api/mo/uni/tn-{bd.get("tenant")}.json?query-target=self&rsp-subtree=full&rsp-subtree-filter=eq(fvCtx.name, "{bd.get("vrf")}")&rsp-subtree-filter=eq(fvBD.name, "{bd.get("name")}")&rsp-subtree-filter=eq(fvSubnet.ip, "{subnet_values.get("ip")}")&rsp-subtree-class=fvSubnet&rsp-subtree-include=no-scoped'
        current_subnets = aci_session.get(url).json()
        assert current_subnets.get("totalCount") == "1"

def test_contracts_exist(aci_session, aci_data, instance_data):
    """
    Validate provided contracts are configured
    """
    for contract_values in aci_data.get("contracts").values():
        url = f'https://{instance_data["aci_ip"]}/api/mo/uni/tn-{contract_values.get("tenant")}.json?rsp-subtree=full&rsp-subtree-filter=eq(vzBrCP.name, "{contract_values.get("name")}")&rsp-subtree-include=no-scoped&rsp-subtree-class=vzBrCP'
        current_contracts = aci_session.get(url).json()
        # print(current_contracts)
        assert current_contracts.get("totalCount") == "1"

def test_filters_exist(aci_session, aci_data, instance_data):
    """
    Validated provided filters exist and configured with valid entries
    """
    for filter_values in aci_data.get("filters").values():
        url = f'https://{instance_data["aci_ip"]}/api/mo/uni/tn-{filter_values.get("tenant")}.json?rsp-subtree=full&rsp-subtree-include=no-scoped&rsp-subtree-class=vzFilter&rsp-subtree-filter=eq(vzFilter.name, "{filter_values.get("name")}")'
        current_filters = aci_session.get(url).json()
        # pprint(current_filters)
        assert current_filters.get("totalCount") == "1"
        filter_dn = current_filters.get("imdata")[0].get("vzFilter").get("attributes").get("dn")
        for entry in filter_values.get("entries"):
            url = f'https://{instance_data["aci_ip"]}/api/mo/{filter_dn}.json?&rsp-subtree=children&rsp-subtree-include=no-scoped&rsp-subtree-class=vzEntry'
            url += '&rsp-subtree-filter=and('
            url += f'eq(vzEntry.prot, "{entry.get("l4_protocol")}"),'
            url += f'eq(vzEntry.etherT, "{entry.get("ip_protocol")}"),'
            url += f'eq(vzEntry.dFromPort, "{entry.get("source_port")}"),'
            url += f'eq(vzEntry.dToPort, "{entry.get("destination_port")}")'
            url += ')'

            current_entries = aci_session.get(url).json()
            assert current_entries.get("totalCount") == "1"


def test_app_profiles_exist(aci_session, aci_data, instance_data):
    for app_pro_values in aci_data.get("app_profiles").values():
        url = f'https://{instance_data["aci_ip"]}/api/mo/uni/tn-{app_pro_values.get("tenant")}.json'
        url += f'?rsp-subtree=children&rsp-subtree-include=no-scoped&rsp-subtree-class=fvAp'
        url += f'&rsp-subtree-filter=eq(fvAp.name, "{app_pro_values.get("name")}")'
        current_apps = aci_session.get(url).json()
        assert current_apps.get("totalCount") == "1"

def test_epgs_exist(aci_session, aci_data, instance_data):
    for epg_values in aci_data.get("epgs").values():
        tenant_name = aci_data.get("app_profiles").get(epg_values.get("app_profile_id")).get("tenant")
        app_profile_name = aci_data.get("app_profiles").get(epg_values.get("app_profile_id")).get("name")
        contract_name = aci_data.get("contracts").get(epg_values.get("contract_id")).get("name")
        bridge_domain_name = aci_data.get("bridge_domains").get(epg_values.get("bridge_domain_id")).get("name")
        url = f'https://{instance_data["aci_ip"]}/api/mo/uni/tn-{tenant_name}.json'
        url += f'?rsp-subtree=full&rsp-subtree-include=no-scoped&rsp-subtree-class=fvAEPg'
        url += f'&rsp-subtree-filter=and(eq(fvAEPg.name, "{epg_values.get("name")}"))'

        current_epgs = aci_session.get(url).json()
        assert current_epgs.get("totalCount") == "1"
        epg_dn = current_epgs.get("imdata")[0].get("fvAEPg").get("attributes").get("dn")
        url = f'https://{instance_data["aci_ip"]}/api/mo/{epg_dn}.json'
        url += f'?query-target=children'
        url += f'&query-target-filter=and(eq(fvRsBd.tRn, "BD-{bridge_domain_name}"))'
        
        bd_check = aci_session.get(url).json()
        assert bd_check.get("totalCount") == "1"
