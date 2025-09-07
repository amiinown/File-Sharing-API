def folder_path(folder):
    if folder.parent:
        return f'{folder_path(folder.parent)}/{folder.name}'
    return folder.name

def create_file_path(instance, filename):
        file = instance
        folder = file.folder
        folder_path_str = folder_path(folder) if folder else ''

        if file.group:
            group_name = file.group.name
            if folder:
                if folder.parent:
                    return f'group_{group_name}/{folder_path_str}/{filename}'
                else:
                    return f'group_{group_name}/{folder_path_str}/{filename}'
            else:
                 return f'group_{group_name}/{filename}'
        
        owner_name = file.owner.username

        if folder:
            if folder.parent:
                return f'user_{owner_name}/{folder_path_str}/{filename}'
            else:
                return f'user_{owner_name}/{folder_path_str}/{filename}'
        else:
            return f'user_{owner_name}/{filename}'