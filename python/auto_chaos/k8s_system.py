"""
K8s actions
"""
from kubernetes import client, config

from auto_chaos.chaos import BaseSystem


class K8sSystem(BaseSystem):
    """
    K8s actions classe
    """
    def __init__(self) -> None:
        # Configs can be set in Configuration class directly or using helper utility
        config.load_kube_config()
        self.v1 = client.CoreV1Api()

    def do_action(self, data):
        """
        Do the action defined in message

        Args:
            message (_type_): _description_
        """
        getattr(self, data.split(" ")[0].lower())(data.split(" ")[1:])

    def describe(self, message=None):
        """_summary_

        Args:
            message (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        result = {"pods": {}, "services": {}, "nodes": {}}

        ret = self.v1.list_node()
        for node in ret.items:
            result["nodes"][node.metadata.name] = {
                "ip": node.status.addresses[0].address,
                "status": node.status.phase
            }
            print("%s" % (node.metadata.name))

        ret = self.v1.list_pod_for_all_namespaces(watch=False)
        for i in ret.items:
            result["pods"][i.metadata.name] = {
                "ip": i.status.pod_ip,
                "namespace": i.metadata.namespace,
                "name": i.metadata.name,
                "status": i.status.phase
            }
            print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
        
        for namespace in self.v1.list_namespace().items:
            ret = self.v1.list_namespaced_service(namespace=namespace.metadata.name, watch=False)
            for i in ret.items:
                result["services"][i.metadata.name] = {
                    "name": i.metadata.name,
                }
                print("%s" % (i.metadata.name))
        return result


    def availability_request(self, message):
        return 200


    def kill(self, message):
        resource_type = message[0]
        resource_name = message[1]
        namespace = message[2]

        if resource_type == "pod":
            self.v1.delete_namespaced_pod(
                name=resource_name,
                namespace=namespace,
            )
        if resource_type == "service":
            self.v1.delete_namespaced_service(
                name=resource_name,
                namespace=namespace,
            )
        if resource_type == "node":
            self.v1.delete_node(
                name=resource_name,
            )
        return 200


    def stress_api(self, message):
        return [200, 400, 404, 500, 200, 400]
