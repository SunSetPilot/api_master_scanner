import os
import javalang
from typing import List

from models.api_info import ApiInfo, ApiParamsInfo
from javalang.tree import CompilationUnit, ClassDeclaration, MethodDeclaration


class JavaAstUtils(object):

    @staticmethod
    def get_all_java_files(project_path: str) -> list:
        """
        Get all java files in the project
        :param project_path:
        :return: java files path list
        """
        java_files = []
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith(".java"):
                    java_files.append(os.path.join(root, file))
        return java_files

    @staticmethod
    def get_java_file_ast(java_file_path: str) -> CompilationUnit:
        """
        Get java file ast
        :param java_file_path:
        :return: java file ast
        """
        try:
            with open(java_file_path, "r") as f:
                content = f.read()
            ast = javalang.parse.parse(content)
            return ast
        except Exception as e:
            raise Exception(f"Failed to get java file ast: {e}")

    @staticmethod
    def is_controller(ast_node: ClassDeclaration) -> bool:
        """
        Is given ast node a controller
        :param ast_node: ast node
        :return: is controller
        """
        if isinstance(ast_node, ClassDeclaration):
            if hasattr(ast_node, "annotations"):
                for annotation in ast_node.annotations:
                    if annotation.name == "RestController" or annotation.name == "Controller":
                        return True
        return False

    @staticmethod
    def __is_api_method(ast_node: MethodDeclaration) -> bool:
        """
        Is given ast node a api method
        :param ast_node: ast node
        :return: is api method
        """
        if isinstance(ast_node, MethodDeclaration):
            if hasattr(ast_node, "annotations"):
                for annotation in ast_node.annotations:
                    if annotation.name.endswith("Mapping"):
                        return True
        return False

    @staticmethod
    def get_api_info(method: MethodDeclaration) -> ApiInfo:
        """
        Get api info from method
        :param method: api method
        :return: api info
        """
        api_info = ApiInfo(
            path="",
            method="",
            params=[]
        )
        for annotation in method.annotations:
            if annotation.name.endswith("Mapping"):
                api_info.method = annotation.name.replace("Mapping", "").upper()
                api_info.path = annotation.children[1].value.strip("\"")
                break
        # todo get params
        return api_info

    @staticmethod
    def get_api_info_list(controller: ClassDeclaration) -> List[ApiInfo]:
        """
        Get api info from controller
        :param controller: api controller
        :return: api info list
        """
        base_path = ""
        for annotation in controller.annotations:
            if annotation.name == "RequestMapping":
                base_path = annotation.children[1].value.strip("\"")
                break

        api_info_list = []
        for method in controller.methods:
            if JavaAstUtils.__is_api_method(method):
                api_info = JavaAstUtils.get_api_info(method)
                api_info.path = f"{base_path}{api_info.path}"
                api_info_list.append(api_info)
        return api_info_list


if __name__ == '__main__':
    from modules.git import git_manager
    project_path = git_manager.get_repo("git@github.com:PlayEdu/PlayEdu.git", "main")
    java_files = JavaAstUtils.get_all_java_files(project_path)
    for file in java_files:
        try:
            ast = JavaAstUtils.get_java_file_ast(file)
        except Exception:
            continue
        for path, node in ast:
            if isinstance(node, ClassDeclaration):
                if JavaAstUtils.is_controller(node):
                    api_info_list = JavaAstUtils.get_api_info_list(node)
                    for api_info in api_info_list:
                        print(api_info)
