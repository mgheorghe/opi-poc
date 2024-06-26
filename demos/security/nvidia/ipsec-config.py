import grpc
from pydpu.proto.v1 import ipsec_pb2
from pydpu.proto.v1 import ipsec_pb2_grpc

channel = grpc.insecure_channel('10.36.78.168:50151')
stub = ipsec_pb2_grpc.IPsecServiceStub(channel)

stub.IPsecVersion(ipsec_pb2.IPsecVersionRequest())

stub.IPsecStats(ipsec_pb2.IPsecStatsRequest())


tun1_0_0 = ipsec_pb2.IPsecLoadConnRequest(
    connection=ipsec_pb2.Connection(
        name='tun1_0_0',
        version='2',
        local_addrs=[ipsec_pb2.Addrs(addr='200.0.0.1')],
        remote_addrs=[ipsec_pb2.Addrs(addr='200.0.0.2')],
        local_auth=ipsec_pb2.LocalAuth(
            auth=ipsec_pb2.AUTH_TYPE_PSK,
            id='200.0.0.1'
        ),
        remote_auth=ipsec_pb2.RemoteAuth(
            auth=ipsec_pb2.AUTH_TYPE_PSK,
            id='200.0.0.2'
        ),
        children=[ipsec_pb2.Child(
            name='tun1_0_0',
            esp_proposals=ipsec_pb2.Proposals(
                crypto_alg=[ipsec_pb2.CRYPTO_ALGORITHM_AES128],
                integ_alg=[ipsec_pb2.INTEG_ALGORITHM_SHA1]
            ),
            remote_ts=ipsec_pb2.TrafficSelectors(
                ts=[ipsec_pb2.TrafficSelectors.TrafficSelector(
                    cidr='40.0.0.0/24'
                )]
            ),
            local_ts=ipsec_pb2.TrafficSelectors(
                ts=[ipsec_pb2.TrafficSelectors.TrafficSelector(
                    cidr='201.0.0.0/24'
                )]
            ),
        )],
        proposals=ipsec_pb2.Proposals(
            crypto_alg=[ipsec_pb2.CRYPTO_ALGORITHM_AES128],
            integ_alg=[ipsec_pb2.INTEG_ALGORITHM_SHA384],
            dhgroups=[ipsec_pb2.DH_GROUPS_MODP1536]
        )
    )
)

tun1_0_1 = ipsec_pb2.IPsecLoadConnRequest(
    connection=ipsec_pb2.Connection(
        name='tun1_0_1',
        version='2',
        local_addrs=[ipsec_pb2.Addrs(addr='200.0.0.1')],
        remote_addrs=[ipsec_pb2.Addrs(addr='200.0.0.3')],
        local_auth=ipsec_pb2.LocalAuth(
            auth=ipsec_pb2.AUTH_TYPE_PSK,
            id='200.0.0.1'
        ),
        remote_auth=ipsec_pb2.RemoteAuth(
            auth=ipsec_pb2.AUTH_TYPE_PSK,
            id='200.0.0.3'
        ),
        children=[ipsec_pb2.Child(
            name='tun1_0_1',
            esp_proposals=ipsec_pb2.Proposals(
                crypto_alg=[ipsec_pb2.CRYPTO_ALGORITHM_AES128],
                integ_alg=[ipsec_pb2.INTEG_ALGORITHM_SHA1]
            ),
            remote_ts=ipsec_pb2.TrafficSelectors(
                ts=[ipsec_pb2.TrafficSelectors.TrafficSelector(
                    cidr='40.0.1.0/24'
                )]
            ),
            local_ts=ipsec_pb2.TrafficSelectors(
                ts=[ipsec_pb2.TrafficSelectors.TrafficSelector(
                    cidr='201.0.0.0/24'
                )]
            ),
        )],
        proposals=ipsec_pb2.Proposals(
            crypto_alg=[ipsec_pb2.CRYPTO_ALGORITHM_AES128],
            integ_alg=[ipsec_pb2.INTEG_ALGORITHM_SHA384],
            dhgroups=[ipsec_pb2.DH_GROUPS_MODP1536]
        )
    )
)




connection_1 = stub.IPsecLoadConn(tun1_0_0)
connection_2 = stub.IPsecLoadConn(tun1_0_1)

list_conn = ipsec_pb2.IPsecListConnsRequest(ike = 'tun1_0_0')
stub.IPsecListConns(list_conn)

list_sa = ipsec_pb2.IPsecListSasRequest(ike = 'tun1_0_1')
stub.IPsecListSas(list_sa)

list_cert = ipsec_pb2.IPsecListCertsRequest()
stub.IPsecListCerts(list_cert)


# init_conn = stub.IPsecInitiate(
#     ipsec_pb2.IPsecInstallReq(ike='tun1_0_0', child='tun1_0_0')
# )


# init_conn = stub.IPsecInitiate(
#     ipsec_pb2.IPsecInitiateReq(ike='tun1_0_0', child='tun1_0_0')
# )