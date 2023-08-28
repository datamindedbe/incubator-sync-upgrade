class GitFolderNotFound(FileNotFoundError):
    def __init__(self, message=".git folder not found in this project. Use --no-git flag"):
        super().__init__(message)


class UpdateMethodNotFound(AttributeError):
    def __init__(self, message="Refactoring file must implement the update() function"):
        super().__init__(message)


class RefactoringFileNotFound(FileNotFoundError):
    def __init__(self, file_path, error_message=""):
        super().__init__(f"Couldn't load refactoring file {file_path}. {error_message}")


class MissingTransformationMethod(ModuleNotFoundError):
    def __init__(self, message="No refactoring method was used"):
        super().__init__(message)


class LoadingCodmodsFailed(ModuleNotFoundError):
    def __init__(self, message="Failed to load codmods"):
        super().__init__(message)


class RefactoringFilesFolderMissing(ModuleNotFoundError):
    def __init__(self, message="Refactoring files must be inside refactoring_files folder"):
        super().__init__(message)


class CloneRemoteRegistryFailed(Exception):
    def __init__(self, message="Cloning remote registry failed"):
        super().__init__(message)


class RestCallFailed(Exception):
    def __init__(self, message, status_code):
        super().__init__(f"Rest call to git failed with status code {status_code}, {message}")
