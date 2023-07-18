from typing import Dict, List, Tuple
from atom import Atom


class Molecule:
    """
    Class represents a molecule composed of multiple atoms.
    """
    def __init__(self, atom_pairs: List[Tuple[Atom, int]]):
        """
        Initializes a Molecule instance with the given list of atom pairs.
        Each atom pair is a tuple of an Atom instance and a count.

        Args:
            atom_pairs (List[Tuple[Atom, int]]): The list of atom pairs.
        """
        self.atom_pairs = atom_pairs

    def count_atoms(self) -> Dict[str, int]:
        """
        Counts the number of each atom in the molecule and returns a dictionary.

        Returns:
            Dict[str, int]: The dictionary with atom symbols as keys and their counts as values.
        """
        atom_counts = {}
        for atom, count in self.atom_pairs:
            atom_counts[atom.symbol] = atom_counts.get(atom.symbol, 0) + count
        return atom_counts

    def __str__(self) -> str:
        """
        Returns a string representation of the molecule.
        The string consists of atom symbols and their counts.

        Returns:
            str: The string representation of the molecule.
        """
        formula = ""
        atom_counts = self.count_atoms()
        for symbol, count in atom_counts.items():
            formula += symbol
            if count > 1:
                formula += str(count)
        return formula

    def __add__(self, other) -> 'Molecule':
        """
        Combines two molecules by concatenating their atom pairs.
        Returns a new Molecule instance.

        Args:
            other (Molecule): The other molecule to combine.

        Returns:
            Molecule: The new Molecule instance.
        """
        if not isinstance(other, Molecule):
            raise ValueError("Only Molecule objects can be added together")

        combined_atom_pairs = self.atom_pairs + other.atom_pairs
        return Molecule(combined_atom_pairs)