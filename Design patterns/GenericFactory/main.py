import os
from importlib import import_module

def myfactory(moduleName):
    return getattr(import_module("plugins."+moduleName), moduleName.capitalize())

def printGreeting(pet):
    print(pet.name(), " pozdravlja: ", pet.greet(), sep='')


def printMenu(pet):
    print(pet.name(), " voli: ", pet.menu(), sep='')


def test():
  pets=[]
  for mymodule in os.listdir('zad1.2/plugins'):
    moduleName, moduleExt = os.path.splitext(mymodule)
    if moduleExt=='.py':
      ljubimac=myfactory(moduleName)('Ljubimac '+str(len(pets)))
      pets.append(ljubimac)

  for pet in pets:
    printGreeting(pet)
    printMenu(pet)


def main():
  test()

if __name__ == '__main__':
    main()