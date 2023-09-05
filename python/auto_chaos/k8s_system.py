"""
K8s system
"""
from kubernetes import client, config

from auto_chaos.chaos import BaseSystem


class K8sSystem(BaseSystem):
    """
    K8s actions classe
    """

    def __init__(self, namespace: str = None) -> None:
        # Configs can be set in Configuration class directly or using helper utility
        config.load_kube_config()
        self.v1 = client.CoreV1Api()
        self.namespace = namespace
        super().__init__()

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
                "status": node.status.phase,
            }
            print("%s" % (node.metadata.name))

        if self.namespace:
            ret = self.v1.list_namespaced_pod(self.namespace)
        else:
            ret = self.v1.list_pod_for_all_namespaces(watch=False)
        for i in ret.items:
            result["pods"][i.metadata.name] = {
                "ip": i.status.pod_ip,
                "namespace": i.metadata.namespace,
                "name": i.metadata.name,
                "status": i.status.phase,
            }
            print(
                "%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name)
            )
        if self.namespace:
            ret = self.v1.list_namespaced_service(namespace=self.namespace, watch=False)
            for i in ret.items:
                result["services"][i.metadata.name] = {
                    "name": i.metadata.name,
                }
                print("%s" % (i.metadata.name))
        else:
            for namespace in self.v1.list_namespace().items:
                ret = self.v1.list_namespaced_service(
                    namespace=namespace.metadata.name, watch=False
                )
                for i in ret.items:
                    result["services"][i.metadata.name] = {
                        "name": i.metadata.name,
                    }
                    print("%s" % (i.metadata.name))
        self.results.append(result)

    def kill(self, data):
        resource_type = data[0]
        resource_name = data[1]

        result = None
        try:
            if resource_type == "pod":
                result = self.v1.delete_namespaced_pod(
                    name=resource_name, namespace=self.namespace, grace_period_seconds=0
                )
            if resource_type == "service":
                result = self.v1.delete_namespaced_service(
                    name=resource_name, namespace=self.namespace, grace_period_seconds=0
                )
            if resource_type == "node":
                result = self.v1.delete_node(name=resource_name, grace_period_seconds=0)
            self.results.append(result.status.phase)
        except Exception as error:
            self.errors.append(error)
