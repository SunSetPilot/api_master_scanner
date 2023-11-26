from javalang.tree import ClassDeclaration
from java_ast_utils import JavaAstUtils
from modules.git_utils import git_manager

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