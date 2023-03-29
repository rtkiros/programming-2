class Atom:

    def __init__(self, symbol, atomic_number, neutrons):
        self.symbol = symbol
        self.atomic_number = atomic_number 
        self.neutrons=neutrons
    
    def protone_number(self):
        return self.atomic_number 
    
    def mass_number(self):
        return self.atomic_number  + self.neutrons
    
    #isotops
    def isotope(self, new_neutron):
        self.neutrons = new_neutron
        

        
    if A.proton_number() == 


protium = Atom('H', 1, 1)
deuterium = Atom('H', 1, 2)
oxygen = Atom('O', 8, 8)
tritium = Atom('H', 1, 2)




print(oxygen.symbol)

print(oxygen.atomic_number )

print(oxygen.neutrons)

print(oxygen.mass_number())
print(tritium.isotope(3))






