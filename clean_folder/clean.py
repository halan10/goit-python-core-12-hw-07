import sys
from pathlib import Path
import shutil
import os
from .normalize import normalize

CATEGORIES = {'audio':['.mp3','.aiff','.wav','.amr','.ogg'],
'images':['.png','.jpg','.jpeg','.svg'],
'video':['.avi','.mp4','.mov','.mkv'],
'documents':['.doc','.docx','.txt','.pdf','.xls','.pptx','.xlsx'],
'archives':['.zip','.gz','.tzr','.rar']}

def move_file(file:Path, root_dir:Path, category:str):
    normalize_name_file =  f"{normalize(file.stem)}{file.suffix}"
    if category == 'unknown':
        return file.replace(root_dir / normalize_name_file)
    
    target_dir = root_dir / category
    
    if category == 'archives': 
         archive_dir = target_dir / os.path.splitext(os.path.basename(normalize_name_file))[0]
         return [shutil.unpack_archive(file, archive_dir), file.replace(target_dir / normalize_name_file)]  

    if not target_dir.exists():
        target_dir.mkdir()
    return file.replace(target_dir / normalize_name_file)



def get_categories(file:Path):
    extension = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if extension in exts:
            return cat
    return 'unknown'    

def sort_dir(root_dir:Path, current_dir:Path ):
    for item in [f for f in current_dir.glob('*') if f.name not in CATEGORIES.keys()]:
        if not item.is_dir():
            category = get_categories(item)
            new_path =  move_file(item, root_dir,category)
            print(new_path)
        else:
             sort_dir(root_dir, item)
             item.rmdir()

def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder. Take as parameter"
    
    if not path.exists():
        return f"Sorry, this path: {path} is not exist"
    sort_dir(path, path)
    return f"{path} has been sorted"
    
if __name__ == "__main__":
    print(main())    