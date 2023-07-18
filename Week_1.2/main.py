from atom import Atom
from molecule import Molecule
from chloroplast import Chloroplast

def testingCloropl():
    """function to test chloroplast class"""
    
    # Create Atom instances
    hydrogen = Atom('H', 1, 1)
    oxygen = Atom('O', 8, 8)
    carbon = Atom('C', 6, 6)

    # Set hydrogen as an isotope with 8 neutrons
    hydrogen.isotope(8)

    # Create a water molecule with 2 hydrogen atoms and 1 oxygen atom
    water = Molecule([(hydrogen, 2), (oxygen, 1)])

    # Create a carbon dioxide molecule with 1 carbon atom and 2 oxygen atoms
    co2 = Molecule([(carbon, 1), (oxygen, 2)])

    # Add water and carbon dioxide to create a new molecule
    new_molecule = water + co2
    demo = Chloroplast()
    #tesing 3b assignment
    els = [water, co2, oxygen, co2]
    for m in els:
        try:
            demo.add_molecule(m)
        except ValueError as e:
            print(str(e)) 
    print(f"demo for assignment 3b: {demo}\n") 

    print(f"----start assignment 3c------") 
    #testing 3c assignment 
    els = [water, co2]
    while (True):
        print ('\nWhat molecule would you like to add?')
        print ('[1] Water')
        print ('[2] carbondioxyde')
        print ('Please enter your choice: ', end='')
        try:
            choice = int(input())
            res = demo.add_molecule(els[choice-1])
            if (len(res)==0):
                print(f"status {demo}")
            else:
                print ('\n=== Photosynthesis!')
                print (f"released molecules: {res}")
                print(f"status {demo}")
        except Exception as e:
            print(str(e))
            print ('\n=== That is not a valid choice.')


def testingAtom():
    """"function to test atom class"""

    protium = Atom('H', 1, 1)
    deuterium = Atom('H', 1, 2)
    oxygen = Atom('O', 8, 8)
    tritium = Atom('H', 1, 2)
    tritium.isotope(3)

    assert tritium. num_neutrons == 3
    assert tritium.mass_number() == 4
    assert protium < deuterium
    assert deuterium <= tritium
    assert tritium >= protium

    try:
        print(oxygen > tritium)
    except ValueError as e:
        print(str(e))


if __name__ == "__main__":
    testingCloropl()
    testingAtom()

