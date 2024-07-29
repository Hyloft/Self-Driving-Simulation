from typing import List
import sys
sys.setrecursionlimit(1500)
from datetime import datetime

class Path:
    def __init__(self,name:str,straight='',left='',right='',back='') -> None:
        self.name = name
        self.straight = straight
        self.left = left
        self.right = right
        self.back = back
        
    def add_forbidden(self,straight=True,left=True,right=True,back=True):
        self.straight = self.straight if straight else ''
        self.left = self.left if left else ''
        self.right = self.right if right else ''
        self.back = self.back if back else ''
    
class Navigator:
    def __init__(self,path:List[Path],aims=[],initial_path='',patience=10) -> None:
        self.paths = path
        self.path_names = self._get_unique_names()
        self.double_paths = self.create_double_paths()
        self.double_path_names = self._get_unique_double_names()
        
        self.patience = patience
        
        self.aims = aims
        self.aim_count = 0
        self.last_path = initial_path
    
    def get_next_path(self):
        if self.aim_count == len(self.aims): return self.last_path
        
        new_path = self.find_path(self.last_path[-2:],self.aims[self.aim_count])
        self.last_path = self.last_path+new_path[2:]
        self.aim_count += 1
        return self.last_path
    
    def create_double_paths(self):
        double_paths = []
        for path in self.paths:
            if path.straight:
                double_paths.append(Path(path.straight+path.name,straight=path.name+path.back if path.back else '',right=path.name+path.left if path.left else '',left=path.name+path.right if path.right else ''))
            if path.back:
                double_paths.append(Path(path.back+path.name,straight=path.name+path.straight if path.straight else '',right=path.name+path.right if path.right else '',left=path.name+path.left if path.left else ''))
            if path.right:
                double_paths.append(Path(path.right+path.name,straight=path.name+path.left if path.left else '',right=path.name+path.straight if path.straight else '',left=path.name+path.back if path.back else ''))
            if path.left:
                double_paths.append(Path(path.left+path.name,straight=path.name+path.right if path.right else '',right=path.name+path.back if path.back else '',left=path.name+path.straight if path.straight else ''))
        self.double_paths = double_paths
        return double_paths
    
    def find_path(self,start:str,aim:str)->str:
        current_double_path = self._get_current_double_path(start)
        path = self._path_finder(current_double_path.name,aim,start,0)
        return path
    
    def forbidden_one(self,name,straight=True,left=True,right=True,back=True):
        try:
            p = self._get_current_path(name)
        except:
            p = self._get_current_double_path(name)
            
        p.add_forbidden(straight,left,right,back)
    
    def _path_finder(self,name,aim,all,tries):
        if tries>self.patience: return 'n'*(self.patience+3)
        path = self._get_current_double_path(name)
        if aim in [n[-1] for n in [p for p in [path.left,path.right,path.straight,path.back] if p]]:
            return all+aim

        left = self._path_finder(path.left,aim,all+path.left[-1],tries+1) if path.left else 'n'*(self.patience+3)
        right = self._path_finder(path.right,aim,all+path.right[-1],tries+1) if path.right else 'n'*(self.patience+3)
        back = self._path_finder(path.back,aim,all+path.back[-1],tries+1) if path.back else 'n'*(self.patience+3)
        straight = self._path_finder(path.straight,aim,all+path.straight[-1],tries+1) if path.straight else 'n'*(self.patience+3)
        
        return min([left,right,back,straight], key=len)
        
    def _get_current_path(self,name:str)->Path:
        if name not in self.path_names:
            raise NameError
            
        for path in self.paths:
            if path.name == name:
                return path
    
    def _get_current_double_path(self,name:str)->Path:
        if name not in self.double_path_names:
            print("NAME NOT FOUND: ",name)
            raise NameError
            
        for path in self.double_paths:
            if path.name == name:
                return path
    
    def _get_unique_names(self):
        unique_names = set()
        for path in self.paths:
            unique_names.add(path.name)
        return unique_names
    
    def _get_unique_double_names(self):
        unique_names = set()
        for path in self.double_paths:
            unique_names.add(path.name)
        print(unique_names)
        return unique_names
    
def main():
    A = Path('A',straight='B',left='H')
    B = Path('B',straight='C',left='O',back='A')
    C = Path('C',back='B',left='D')
    D = Path('D',back='O',left='E',right='C')
    E = Path('E',back='F',right='D')
    F = Path('F',back='G',right='O',straight='E')
    G = Path('G',right='H',straight='F')
    H = Path('H',right='A',straight='O',left='G')
    O = Path('O',right='B',straight='D',left='F',back='H')
    all_paths = [A,B,C,D,E,F,G,H,O]
    start=datetime.now()

    navigator = Navigator(all_paths)
    # navigator.find_path('A','D') # return ABOD or ABCD
    # navigator.find_path('D','G') # return DOHG or DOFG or DEFG
    # navigator.forbidden_one('O',left=False)
    print(navigator.find_path('AB','G')) # return DOHG or DEFG
    navigator.forbidden_one('BO',left=False)
    print(navigator.find_path('AB','G')) # return DOHG or DEFG
    navigator.forbidden_one('BO',straight=False)
    print(navigator.find_path('AB','G')) # return DOHG or DEFG
    navigator.forbidden_one('EF',straight=False)
    print(navigator.find_path('AB','G')) # return DOHG or DEFG
    print(datetime.now()-start)
    

if __name__ == '__main__':
    main()