# Toshe Save File Converter
# Updates 0.0-2.1 characters to 3.0

import pickle
import sys

from TUACharacter import Character
from TUAWeapon import Weapon
from TUAArmour import Armour
from TUAShield import Shield
from TUAMiscellaneousItem import MiscellaneousItem
from TUASkill import Skill
from TUAQuest import Quest

from TUAAdriaticSea import AdriaticSea
from TUABoat import Boat
from TUAKismet import Kismet
from TUABayOfKotor import BayOfKotor
from TUAHercegNovi import HercegNovi
from TUAHercegBluffs import HercegBluffs
from TUAIgalo import Igalo
from TUAHercegFields import HercegFields
from TUABlackMountain import BlackMountain
from TUAMojkovacSummit import MojkovacSummit
from TUAMojkovacValley import MojkovacValley
from TUATheWatchmakingFacility import TheWatchmakingFacility
from TUACemetery import Cemetery
from TUAScutariPeninsula import ScutariPeninsula
from TUAWesternKosovo import WesternKosovo
from TUATheSecretLaboratory import TheSecretLaboratory
from TUAPec import Pec
from TUAAlbanianDesert import AlbanianDesert
from TUAEasternKosovo import EasternKosovo
from TUAPristina import Pristina
from TUATrafCafe import TrafCafe
from TUAPresidentialPath import PresidentialPath
from TUAOldRuins import OldRuins
from TUARomadanVillage import RomadanVillage
from TUARomadanHideout import RomadanHideout
from TUAGambinoCastle import GambinoCastle
from TUAHiddenPassage import HiddenPassage
from TUAGreece import Greece
from TUAAthens import Athens
from TUAColiseum import Coliseum
from TUAThessaloniki import Thessaloniki
from TUAGreekFortress import GreekFortress
from TUAMacedonia import Macedonia
from TUACredits import Credits
from TUAGolemCavern1 import GolemCavern1
from TUAGolemCavern2 import GolemCavern2
from TUAGolemCavern3 import GolemCavern3
from TUASimelliermPit import SimelliermPit
from TUAGalijula import Galijula
from TUAFartooqHold import FartooqHold
from TUAYaouwVolcano import YaouwVolcano
from TUADuneHotsPeak import DuneHotsPeak
from TUALairOfTheMagi import LairOfTheMagi
from TUAIgaloCathedral import IgaloCathedral
from TUALitochoro import Litochoro
from TUAMountOlympus import MountOlympus
from TUALabyrinthOfDaedalus import LabyrinthOfDaedalus

def updateChangedAreaNames(character):
    changed = False
    changedAreas = [
        ("Herceg Fields",
         "Frolicking Fields"),
        ("Herceg Bluffs",
         "Billowing Bluffs"),
        ("Mojkovac Summit",
         "Summit of Presage"),
    ]
    for area in changedAreas:
        if area[0] in character.flags['Discovered Areas']:
            if area[1] not in character.flags['Discovered Areas']:
                character.flags['Discovered Areas'][area[1]] = character.flags['Discovered Areas'][area[0]]
                character.flags['Marked Areas'][area[1]] = character.flags['Marked Areas'][area[0]]
            del character.flags['Discovered Areas'][area[0]]
            del character.flags['Marked Areas'][area[0]]
            changed = True
    return changed

def update(gameFile, path):
    changed = False
    character = pickle.load(gameFile)
    if "Discovered Areas" not in character.flags:
        character.flags['Discovered Areas'] = {}
        changed = True
    if "Marked Areas" not in character.flags:
        character.flags['Marked Areas'] = {}
        changed = True
    if ( "Config" not in character.flags or
         "Automap On" not in character.flags['Config'] or
         "Mission Log Open" not in character.flags['Config']):
        character.flags['Config'] = dict()
        character.flags['Config']['Automap On'] = 1
        character.flags['Config']['Mission Log Open'] = 0
        changed = True
    for area in character.flags['Discovered Areas']:
        if area not in character.flags['Marked Areas']:
            character.flags['Marked Areas'][area] = set()
            changed = True
    if not hasattr(character, "LIVING"):
        setattr(character, "LIVING", 1)
        changed = True
    if not hasattr(character, "mercenaries"):
        return "error"
    else:
        for mercenary in character.mercenaries:
            setattr(mercenary, "LIVING", 1)
    if not hasattr(character, "potions"):
        setattr(character, "potions", 0)
        for mercenary in character.mercenaries:
            setattr(mercenary, "potions", 0)
        changed = True
    if not hasattr(character, "checkpoint"):
        setattr(character, "checkpoint", None)
        changed = True
    if not hasattr(character, "quests"):
        setattr(character, "quests", [])
        changed = True
    if not hasattr(character, "_specialization"):
        setattr(character, "_specialization", None)
        setattr(character, "mastery", 1)
        setattr(character, "sp", 0)
        setattr(character, "_maxHp", max(character.level * 20 + 80, character.hp))
        setattr(character, "_maxEp", max(character.level * 20 + 80, character.ep))
        for mercenary in character.mercenaries:
            setattr(mercenary, "_specialization", None)
            setattr(mercenary, "_maxHp", max(mercenary.level * 20 + 80, mercenary.hp))
            setattr(mercenary, "_maxEp", max(mercenary.level * 20 + 80, mercenary.ep))
        changed = True
    if "Dark Voice 4" in character.flags and "Giacomo Macedonia 1" not in character.flags:
        del character.flags['Dark Voice 4']
        changed = True
    if not hasattr(character, "portrait"):
        character.portrait = "Toshe"
        character.mode = "Hard"
        character._euros = 420
        for mercenary in character.mercenaries:
            mercenary.portrait = None
            mercenary.mode = None
            mercenary._euros = 0
        changed = True
    itemsToCheck = character.items + [character.blankWeapon, character.blankArmour, character.blankShield]
    if "Buyback Items" in character.flags:
        itemsToCheck += character.flags['Buyback Items']
    for mercenary in character.mercenaries:
        itemsToCheck.append(mercenary.equippedWeapon)
        itemsToCheck.append(mercenary.equippedArmour)
        itemsToCheck.append(mercenary.equippedShield)
    for item in filter(lambda item: item is not None, itemsToCheck):
        if item is None or item == "Chasmic Rucksack":
            continue
        if item.CATEGORY != "Miscellaneous" and not hasattr(item, "upgradeCount"):
            item.upgradeCount = 0
            changed = True
        if item.CATEGORY == "Club":
            item.CATEGORY = "Bludgeon"
            changed = True
    for skill in filter(lambda skill: skill is not None, character.skills):
        if skill.ELEMENT == "Electricity":
            skill.ELEMENT = "Lightning"
            changed = True
        if "Club" in skill.PERMITTED_WEAPONS:
            skill.PERMITTED_WEAPONS.add("Bludgeon")
            skill.PERMITTED_WEAPONS.remove("Club")
            changed = True
    changed = updateChangedAreaNames(character) or changed
    if changed:
        with open(path, "w") as gameFile:
            pickle.dump(character, gameFile)
        
    return changed

if __name__ == "__main__":
    try:
        print ("This program will update your character file from" +
               " version 0.0 or later to 3.0.")
        fileName = raw_input("What's the name of the character to update? ")

        try:
            path = "resources/saves/"+fileName+".tq"
            with open(path, "r") as gameFile:
                changed = update(gameFile, path)
        except (IOError):
            try:
                path = "resources/saves/"+fileName+".toshe"
                with open(path, "r") as gameFile:
                    changed = update(gameFile, fileName)
            except (IOError):
                raw_input("No .tq or .toshe file named %s was found." % fileName)
                sys.exit()
        print
        if changed == "error":
            raw_input(fileName+" could not be updated. The file format is probably too old.")
        elif changed:
            raw_input(fileName+" got updated!")
        else:
            raw_input(fileName+" is already up to date.")

    except (IndexError, EOFError, KeyError):
        raw_input("\nThere was an error processing the character data." +
                  "\nYour savefile is probably corrupt.")
        raise
