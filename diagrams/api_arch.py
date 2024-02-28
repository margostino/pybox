from diagrams import Cluster, Diagram
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.network import ELB, Route53

with Diagram("Cluster", show=False):
    dns = Route53("dns")
    lb = ELB("lb")

    with Cluster("Services"):
        svc_group = [EC2("api-1"), EC2("api-2"), EC2("api-N")]

    with Cluster("DB Cluster"):
        db_primary = Dynamodb("lookup")
        # db_primary - [Dynamodb("lookup")]

    lambda_1 = Lambda("lambda-data-provider-1")
    lambda_2 = Lambda("lambda-data-provider-2")
    http_1 = EC2("http-data-provider-1")

    dns >> lb >> svc_group
    svc_group >> db_primary
    svc_group >> lambda_1
    svc_group >> lambda_2
    svc_group >> http_1
