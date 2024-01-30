import pytest
import json
from pathlib import Path
from requests import Session


@pytest.fixture(scope='module')
def root_path() -> Path:
    """
    Get the root path for login and aci_data
    """
    ROOT_PATH = Path(__file__).resolve().parent.parent
    assert ROOT_PATH
    return ROOT_PATH

@pytest.fixture(scope='module')
def instance_data(root_path) -> dict:
    """
    Grabs the instance data from instance_data.py
    """
    instance_data = json.loads(open(f"{root_path}/instance_data.json").read())['instance_data']
    assert instance_data.get("username")
    assert instance_data.get("password")
    assert instance_data.get("aci_ip")
    return instance_data

@pytest.fixture(scope='module')
def aci_data(root_path) -> dict:
    """
    Grabs the aci_data from aci_data.py
    """
    aci_data = json.loads(open(f"{root_path}/aci_data.json").read())
    assert aci_data.get("data")
    return aci_data.get("data")

@pytest.fixture(scope='module')
def aci_session(instance_data) -> Session:
    """
    Login to ACI and return a requests session with cookie set
    """
    payload = {
        "aaaUser": {
            "attributes": {
                "name": instance_data['username'],
                "pwd": instance_data['password']
            }
        }
    }
    #Login to ACI with provided username and password, test if the APIC-cookie is set for the session
    r = Session()
    r.post(f"https://{instance_data['aci_ip']}/api/aaaLogin.json", verify=False, json=payload)
    assert "APIC-cookie" in r.cookies
    return r


