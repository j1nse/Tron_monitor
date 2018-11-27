#coding:utf-8
import grpc

import api_pb2
import api_pb2_grpc


channel = grpc.insecure_channel('grpc.trongrid.io:50051')
stub  = api_pb2_grpc.WalletStub(channel)
response = stub.GetNowBlock(api_pb2.EmptyMessage())
print(type(response))
print(response)