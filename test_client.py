import grpc
from rpc import api_scanner_pb2_grpc, api_scanner_pb2

channel = grpc.insecure_channel('localhost:50051')
stub = api_scanner_pb2_grpc.ScanApiServiceStub(channel)

stub.Scan(api_scanner_pb2.ScanApiRequest(project_id=1,git_address="git@github.com:PlayEdu/PlayEdu.git",git_branch="main"))

