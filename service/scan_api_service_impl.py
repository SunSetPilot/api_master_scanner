from rpc.api_scanner_pb2_grpc import ScanApiServiceServicer
from rpc.api_scanner_pb2 import ScanApiResponse
import threading

from models.api_entity import ApiEntity
from modules.logger import logger
from modules.git_utils import git_manager
from modules.java_ast_utils import JavaAstUtils
from database.mysql import get_db_session


def scan_and_save_api(project_id, git_address, git_branch):
    db_session = get_db_session()
    try:
        logger.info(f"start to download repo: {git_address}, branch: {git_branch}")
        repo_path = git_manager.get_repo(git_address, git_branch)
        logger.info(f"start to scan repo: {git_address}, branch: {git_branch}")
        java_files = JavaAstUtils.get_all_java_files(repo_path)
        for file in java_files:
            try:
                ast = JavaAstUtils.get_java_file_ast(file)
            except Exception as e:
                logger.error(f"Failed to get java file ast: {e}")
                continue
            for path, node in ast:
                if JavaAstUtils.is_controller(node):
                    api_info_list = JavaAstUtils.get_api_info_list(node)
                    for api_info in api_info_list:
                        api_entity = ApiEntity()
                        api_entity.project_id = project_id
                        api_entity.description = f"[AUTO IMPORT] {api_info.path}"
                        api_entity.method = api_info.method
                        api_entity.protocol = "http"
                        api_entity.path = api_info.path
                        api_entity.header_params = api_info.header_params
                        api_entity.query_params = api_info.query_params
                        api_entity.body_params = api_info.body_params
                        api_entity.response = api_info.response

                        exist_api = db_session.query(ApiEntity).filter(
                            ApiEntity.project_id == project_id,
                            ApiEntity.path == api_info.path,
                            ApiEntity.method == api_info.method
                        ).first()
                        if exist_api:
                            logger.info(f"api already exist: {exist_api.path}, {exist_api.method}")
                            continue
                        else:
                            db_session.add(api_entity)
                            db_session.commit()
        logger.info(f"scan repo: {git_address}, branch: {git_branch} finished")
    except Exception as e:
        logger.error(f"Failed to scan repo: {e}")
    finally:
        git_manager.delete_repo(git_address, git_branch)
        db_session.close()


class ScanApiServiceImpl(ScanApiServiceServicer):
    def Scan(self, request, context):
        logger.info(f"receive scan request: {request}")
        project_id = request.project_id
        git_address = request.git_address
        git_branch = request.git_branch
        threading.Thread(target=scan_and_save_api, args=(project_id, git_address, git_branch)).start()
        return ScanApiResponse(success=True, message="success")
