import grpc

import api_pb2
import api_pb2_grpc


channel = implementations.insecure_channel('grpc.trongrid.io', 50051)
stub  = api_pb2_grpc.WalletStub(point)
response = stub.GetNowBlock(api_pb2.EmptyMessage())
print(response)