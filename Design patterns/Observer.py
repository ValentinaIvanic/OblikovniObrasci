import ast
from abc import ABC, abstractmethod
import re

def is_numeric(exp):
    try:
        int(exp)
        return True
    except ValueError:
        return False


def eval_expression(exp, variables={}):
    def _eval(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Name):
            return variables[node.id]
        elif isinstance(node, ast.BinOp):
            return _eval(node.left) + _eval(node.right)
        else:
            raise Exception('Unsupported type {}'.format(node))

    node = ast.parse(exp, mode='eval')
    return _eval(node.body)


class Observer(ABC):
    @abstractmethod
    def update(self):
        pass

class CellObserver(Observer):
    def __init__(self, cell):
        self.cell = cell

    def update(self):
        self.cell.sheet.evaluate(self.cell)

class Cell: 
    def __init__(self, sheet, exp):
        self.sheet = sheet
        self.exp = exp
        self.observers = set()
        self.visited = False
        self.value = sheet.evaluate(self)
        

    def add_observer(self, observer: Observer):
        self.observers.add(observer)

    def del_observer(self, observer: Observer):
        self.observers.remove(observer)

    def notify(self):
        for observer in self.observers:
            observer.update()
        
    def find_other_cells(self):
        other_cells = []

        pattern = r'[A-Z][0-9]'
        other_cells = re.findall(pattern, self.exp)
        return other_cells


class Sheet:
    def __init__(self, n_rows, n_col):
        self.rows = n_rows
        self.cols = n_col
        self.table = [[Cell(self, '0') for j in range(n_col)] for i in range (n_rows)]

    def set(self, position_name, expresion):
        row, col = self.determine_position(position_name)

        if self.table[row][col].value != None:
            other_cells = self.table[row][col].find_other_cells()
            for ref in other_cells:
                self.cell(ref).del_observer(CellObserver(self.table[row][col]))

        self.table[row][col].exp = expresion

        other_cells = self.table[row][col].find_other_cells()
        for ref in other_cells:
                self.cell(ref).add_observer(CellObserver(self.table[row][col]))
        self.evaluate(self.table[row][col])
        self.table[row][col].notify()

    def cell(self, ref):
        row, col = self.determine_position(ref)
        
        return self.table[row][col]
    
    def determine_position(self, ref):
        col = ord(ref[0].upper()) - ord('A')
        row = int(ref[1:]) - 1

        return row, col
    
    def getrefs(self, cell):
        referenced_cells = cell.find_other_cells()
        cells = list()
        for ref in referenced_cells:
            cells.append(self.cell(ref))
        return cells

    def evaluate(self, cell):
        if cell.visited:
            raise RuntimeError
        
        if is_numeric(cell.exp):
            cell.value = int(cell.exp)
            return
        D = dict()
        other_cells = cell.find_other_cells()
        
        for ref in other_cells:
            D[ref] = self.cell(ref).value
        
        cell.visited = True
        cell.value = eval_expression(cell.exp, D)
        cell.notify()
        cell.visited = False
        return cell.value
    
    def print(self):
        for i in range (self.rows):
            for j in range (self.cols):
                value = self.table[i][j].value
                if value != None:
                    print(f"{value:4}  ", end="")
                else:
                    print(value, " ", end="")
            print()
    
def main():
    s=Sheet(5,5)
    print()

    s.set('A1','2')
    s.set('A2','5')
    s.set('A3','A1+A2')
    s.set('D2','5')
    s.print()
    print()

    s.set('A1','4')
    s.set('A4','A1+A3')
    s.print()
    print()

    try:
        s.set('A1','A3')
    except RuntimeError as e:
        print("Caught exception:",e)
    s.print()
    print()


if __name__ == "__main__":
    main()