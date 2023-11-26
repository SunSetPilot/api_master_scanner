import grpc
from concurrent import futures
from service.scan_api_service_impl import ScanApiServiceImpl

from modules.logger import logger

import config.settings
from rpc.api_scanner_pb2_grpc import add_ScanApiServiceServicer_to_server

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
add_ScanApiServiceServicer_to_server(ScanApiServiceImpl(), server)
server.add_insecure_port(f"[::]:{config.settings.grpc_port}")
server.start()
logger.info(f"ApiScannerService started at port {config.settings.grpc_port}")
server.wait_for_termination()