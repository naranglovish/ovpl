import unittest
import json
import requests

from src.adapters.AWSAdapter import AWSAdapter


class TestAWSAdapter(unittest.TestCase):
    def setUp(self):
        # hardcoded paths are not flexible. this will only work if I run it from
        # the top-level of ovpl directory..
        self.lab_spec = json.loads(open("scripts/labspec.json").read())
        self.adapter = AWSAdapter()

    def test_create_vm(self):
        vm_id = self.adapter.create_vm(self.lab_spec)
        vm_ip = self.adapter.get_vm_ip(vm_id)
        instance = self.adapter.get_instance(vm_id)
        print vm_ip
        print vm_id
        print instance
        print instance.state_code
        print "state code represents that instance is pending"

        self.assertIn(instance.state_code, (0, 16))

    def test_init_vm(self):
     #   vm_id = self.adapter.create_vm(self.lab_spec)
        lab_repo_name =  'ovpl'
        result = self.adapter.init_vm(self.vm_id, lab_repo_name)
        vm_ip = result[1]['vm_ip']
        vmmanager_port = result[1]['vmm_port']
    
        response = requests.get("http://" + vm_ip + ":" + vmmanager_port)
        self.assertEqual(response.status_code, 200)



if __name__ == "__main__":
    unittest.main()
