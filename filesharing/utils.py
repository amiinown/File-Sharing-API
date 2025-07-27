def create_file_path(instance, filename):
        file = instance.file
        folder = file.folder

        if file.group:
            group_id = file.group.id
            if folder:
                if folder.parent:
                    return f'group_{group_id}/folder_{folder.parent.id}/subfolder_{folder.id}/{filename}'
                else:
                    return f'group_{group_id}/folder_{folder.id}/{filename}'
            else:
                 return f'group_{group_id}/{filename}'
        
        owner_id = file.owner.id

        if folder:
            if folder.parent:
                return f'user_{owner_id}/folder_{folder.parent.id}/subfolder_{folder.id}/{filename}'
            else:
                return f'user_{owner_id}/folder_{folder.id}/{filename}'
        else:
            return f'user_{owner_id}/{filename}'