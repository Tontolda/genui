"""
base

Created by: Martin Sicho
On: 18-12-19, 11:32
"""
from abc import ABC, abstractmethod

from django.db import IntegrityError, transaction
from molvs import Standardizer
from rdkit import Chem
from rdkit.Chem import AllChem

from compounds.initializers.exceptions import SMILESParsingError, StandardizationError
from compounds.models import MolSet, Molecule


class MolSetInitializer(ABC):

    def __init__(self, instance : MolSet, progress_recorder=None):
        self._instance = instance
        self.standardizer = Standardizer()
        self.progress_recorder = progress_recorder
        self.unique_mols = 0
        self.errors = []

    def addMoleculeFromSMILES(self, smiles : str, molecule_class=Molecule, constructor_kwargs=None):
        # TODO: check if molecule_class is a subclass of Molecule
        if not constructor_kwargs:
            constructor_kwargs = dict()

        mol = Chem.MolFromSmiles(smiles, sanitize=False)
        if not mol:
            raise SMILESParsingError(smiles, f"Failed to create molecule during initialization of molecule set {repr(self._instance)} from SMILES: {smiles}")
        try:
            smol = self.standardizer.standardize(mol)
        except Exception as exp:
            raise StandardizationError(exp, "Error while standardizing molecule: ", smiles)
        canon_smiles = Chem.MolToSmiles(smol, isomericSmiles=True, canonical=True, allHsExplicit=True)
        inchi_key = Chem.MolToInchiKey(smol)
        params = {
            "canonicalSMILES" : canon_smiles
            , "inchiKey" : inchi_key
        }
        params.update(constructor_kwargs)

        instance = self.getInstance()
        if molecule_class.objects.filter(**params).count():
            ret = molecule_class.objects.get(**params)
            # TODO: add a callback or something to check if there are no issues (like two CHMEBL molceules that are the same but have different ID)
        else:
            try:
                with transaction.atomic():
                    params["molObject"] = smol
                    ret = molecule_class.objects.create(**params)
                    ret.providers.add(self._instance)
                    ret.morganFP2 = AllChem.GetMorganFingerprintAsBitVect(ret.molObject, radius=2, nBits=512)
                    ret.save()
                    instance.save()
            except IntegrityError as exp:
                # TODO: analyze the error and provide more details to the caller
                raise exp

        ret.providers.add(instance)
        instance.save()
        self.unique_mols = instance.molecules.count()
        return ret

    @abstractmethod
    def populateInstance(self):
        pass

    @abstractmethod
    def updateInstance(self):
        pass

    def getInstance(self):
        return self._instance

