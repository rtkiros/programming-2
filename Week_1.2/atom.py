class Atom:
    """
    Class represents an atom with a symbol, atomic number, and number of neutrons.
    """

    def __init__(self, symbol: str, atomic_number: int, num_neutrons: int):
        """
        Initializes an Atom instance with the given symbol, atomic number, and number of neutrons.

        Args:
            symbol (str): The symbol of the atom.
            atomic_number (int): The atomic number of the atom.
            num_neutrons (int): The number of neutrons in the atom.
        """

        self.symbol = symbol
        self.atomic_number = atomic_number
        self.num_neutrons = num_neutrons

    def proton_number(self) -> int:
        """
        Returns the atomic number of the atom.
        """
        return self.atomic_number

    def mass_number(self) -> int:
        """
        Returns the mass number of the atom (atomic number + number of neutrons).
        """
        return self.atomic_number + self.num_neutrons 

    def  isotope(self, num_neutrons: int) -> None:
        """
        Sets the number of neutrons for the atom.

        Args:
            num_neutrons (int): The number of neutrons to set.
        """
        self.num_neutrons = num_neutrons

    def __eq__(self, other) -> bool:
        """
        Checks if the atom is equal to another atom based on their mass numbers.

        Args:
            other (Atom): The other atom to compare.

        Returns:
            bool: True if the atoms are equal, False otherwise.
        """
        if isinstance(other, Atom):
            return self.symbol == other.symbol and self.neutrons == other.neutrons
        else:
            raise ValueError("Cannot compare Atom with a different type.")

    def __lt__(self, other) -> bool:
        
        """
        Compares the atom with another atom based on their mass numbers.

        Args:
            other (Atom): The other atom to compare.

        Returns:
            bool: True if the atom is less than the other atom, False otherwise.
        """

        if isinstance(other, Atom):
            if self.symbol != other.symbol:
                raise ValueError("Cannot compare isotopes of different elements.")
                return self.mass_number() < other.mass_number()
            else:
                raise ValueError("Cannot compare Atom with a different type.")


        # if not isinstance(other, Atom):
        #     return NotImplemented
        # return self.mass_number() < other.mass_number()

    def __gt__(self, other) -> bool:
        """
        Compares the atom with another atom based on their mass numbers.

        Args:
            other (Atom): The other atom to compare.

        Returns:
            bool: True if the atom is greater than the other atom, False otherwise.
        """
        return self == other or self < other

    def __le__(self, other) -> bool:
        """
        Compares the atom with another atom based on their mass numbers.

        Args:
            other (Atom): The other atom to compare.

        Returns:
            bool: True if the atom is less than or equal to the other atom, False otherwise.
        """
        if isinstance(other, Atom):
            if self.symbol != other.symbol:
                raise ValueError("Cannot compare isotopes of different elements.")
                return self.mass_number() > other.mass_number()
            else:
                raise ValueError("Cannot compare Atom with a different type.")

    def __ge__(self, other) -> bool:
        """
        Compares the atom with another atom based on their mass numbers.

        Args:
            other (Atom): The other atom to compare.

        Returns:
            bool: True if the atom is greater than or equal to the other atom, False otherwise.
        """
        return self == other or self > other
