import requests
from pprint import pprint
requests.packages.urllib3.disable_warnings()

APIC_URL = "https://192.168.1.251"

LOGIN_DATA = {
    "aaaUser": {
        "attributes": {
            "name": "admin",
            "pwd": "345751D3"
        }
    }
}
r = requests.Session()

login_data = r.post(f"{APIC_URL}/api/aaaLogin.json", json=LOGIN_DATA, verify=False).json()

# cookies = {"APIC-cookie": login_data['imdata'][0]['aaaLogin']['attributes']['token']}
# url = f'https://192.168.1.251/api/mo/uni/tn-test_tenant1/flt-FILTER001.json?&rsp-subtree=children&rsp-subtree-include=no-scoped&rsp-subtree-class=vzEntry&rsp-subtree-filter=eq(vzEntry.prot, "tcp")&rsp-subtree-filter=eq(vzEntry.etherT, "ip")&rsp-subtree-filter=eq(vzEntry.dFromPort, "443")&rsp-subtree-filter=eq(vzEntry.dToPort, "443")'
# url = f'https://192.168.1.251/api/mo/uni/tn-test_tenant1/flt-FILTER001.json?&rsp-subtree=children&rsp-subtree-include=no-scoped&rsp-subtree-class=vzEntry&rsp-subtree-filter=eq(vzEntry.dFromPort, "443")&rsp-subtree-filter=eq(vzEntry.dToPort, "443")'
# url += '&rsp-subtree-filter=and(eq(vzEntry.dToPort, "443"), eq(vzEntry.dFromPort, "443"))'
url = 'https://192.168.1.251/api/mo/uni/tn-test_tenant1/flt-FILTER001.json?&rsp-subtree=children&rsp-subtree-include=no-scoped&rsp-subtree-class=vzEntry'
url += '&rsp-subtree-filter=and(eq(vzEntry.prot, "tcp"),eq(vzEntry.etherT, "ip"),eq(vzEntry.dFromPort, "80"),eq(vzEntry.dToPort, "80"))'
# test = r.get(f"{APIC_URL}/api/node/mo/uni/tn-Test-t.json?query-target=self&rsp-subtree=no", verify=False).text
test = r.get(url,verify=False)
pprint(test.json())

"""
?query-target-filter=and(not(wcard(aaaDomain.dn,"__ui_")),and(ne(aaaDomain.name,"common"),ne(aaaDomain.name,"all"),ne(aaaDomain.name,"mgmt")))
and(eq(vzEntry.prot, "tcp"),and(eq(vzEntry.etherT, "ip"),eq(vzEntry.dFromPort, "443"),eq(vzEntry.dToPort, "443")))
"""
# import json
# import yamland
#(not(wcard(fvTenant.dn,"__ui_")),eq(fvTenant.dn,"uni/tn-test_tenant2"))


# out = yaml.dump_all(open("aci_data.json", "r").read())
# with open("out_yaml.yml", "w") as file:
#     file.write(out)
# print(out)