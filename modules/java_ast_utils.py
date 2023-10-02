import os
import javalang
from javalang.tree import CompilationUnit, ClassDeclaration


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
                    if annotation.name == "RestController":
                        return True
        return False


if __name__ == '__main__':
    from modules.git import git_manager

    project_path = git_manager.get_repo("git@github.com:PlayEdu/PlayEdu.git", "main")
    file = "/tmp/repo_cache/295d695a3ef9114fcdc32ccb72ac6ad2/playedu-api/src/main/java/xyz/playedu/api/controller/frontend/UserController.java"
    ast = JavaAstUtils.get_java_file_ast(file)
    print(ast)
    print(JavaAstUtils.is_controller(ast.types[0]))
