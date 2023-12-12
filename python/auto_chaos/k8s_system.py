"""
☸️
K8s system
☸️
"""
from kubernetes import client, config

from auto_chaos.base_system import BaseSystem


class K8sSystem(BaseSystem):
    """
    K8s actions classe
    """

    def __init__(self, namespace: str = None) -> None:
        """
        Init

        Args:
            namespace (str, optional): Namespace in which to do things. Defaults to None => cluster scope.
        """
        # Configs can be set in Configuration class directly or using helper utility
        config.load_kube_config()
        self.client = client.CoreV1Api()
        self.namespace = namespace
        super().__init__()

    def describe(self, args: list[str] = None):
        """
        Describe a k8s cluster

        Args:
            args (list[str], optional): Not used. Defaults to None.
        """
        result = {"pods": {}, "services": {}, "nodes": {}}

        # List cluster nodes
        ret = self.client.list_node()
        for node in ret.items:
            result["nodes"][node.metadata.name] = {
                "ip": node.status.addresses[0].address,
                "status": node.status.phase,
            }
            print("%s" % (node.metadata.name))

        # List namespaced pods or cluster scope
        if self.namespace:
            ret = self.client.list_namespaced_pod(self.namespace)
        else:
            ret = self.client.list_pod_for_all_namespaces(watch=False)
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

        # List namespaced services or cluster scope
        if self.namespace:
            ret = self.client.list_namespaced_service(
                namespace=self.namespace, watch=False
            )
            for i in ret.items:
                result["services"][i.metadata.name] = {
                    "name": i.metadata.name,
                }
                print("%s" % (i.metadata.name))
        else:
            for namespace in self.client.list_namespace().items:
                ret = self.client.list_namespaced_service(
                    namespace=namespace.metadata.name, watch=False
                )
                for i in ret.items:
                    result["services"][i.metadata.name] = {
                        "name": i.metadata.name,
                    }
                    print("%s" % (i.metadata.name))

        # Add result to results
        self.results.append(result)

    def kill(self, args: list[str] = None):
        """
        Kill a k8s ressource (pod, service, node)

        Args:
            args (list[str], optional): Resource type and name. Defaults to None.
        """
        resource_type = args[0]
        resource_name = args[1]

        result = None
        try:
            # Delete ressource
            if resource_type == "pod":
                result = self.client.delete_namespaced_pod(
                    name=resource_name, namespace=self.namespace, grace_period_seconds=0
                )
            if resource_type == "service":
                result = self.client.delete_namespaced_service(
                    name=resource_name, namespace=self.namespace, grace_period_seconds=0
                )
            if resource_type == "node":
                result = self.client.delete_node(
                    name=resource_name, grace_period_seconds=0
                )
            # Add result to results
            self.results.append(result.status.phase)
        except Exception as error:
            self.errors.append(error)
