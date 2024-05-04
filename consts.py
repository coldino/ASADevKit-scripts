from typing import Optional, TypedDict


STAT_COUNT = 12
NUM_REGIONS = 6
IS_PERCENT_STAT = (0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1)


SKIP_SPECIES_ROOTS = [
    '/cfeditor',
    '/Game/PrimalEarth/CoreBlueprints/Dino_Character_BP_', # a whole bunch of bases
]

SKIP_SPECIES = [
    '/Game/Aberration/Boss/Rockwell/Rockwell_Character_BP',
    '/Game/Aberration/Boss/RockwellTentacle/RockwellTentacle_Character_BP',
    '/Game/EndGame/Dinos/Endboss/EndBoss_Character',
    '/Game/EndGame/Dinos/Endboss/EndbossDragon/EndBossDragon_Character_BP',
    '/Game/EndGame/Dinos/Endboss/EndbossGorilla/EndBossGorilla_Character_BP',
    '/Game/EndGame/Dinos/Endboss/EndbossSpider/EndBossSpiderL_Character_BP',
    '/Game/Extinction/Dinos/Corrupt/Raptor/BabyRaptor_Character_BP_Corrupt',
    '/Game/Extinction/Dinos/Enforcer/Enforcer_Character_BP_Malfunctioned',
    '/Game/Genesis/Dinos/Bots/Bot_Character_BP.Bot_Character_BP',
    '/Game/Genesis/Dinos/EelBoss/EelBoss_Character_BP',
    '/Game/Genesis/Dinos/EelBoss/EelMinion_Character_BP',
    '/Game/LostIsland/Boss/BossDinopithecus_Character_BP',
    '/Game/PrimalEarth/Dinos/CrystalWyvern/CrystalWyvern_Character_BP_Base.CrystalWyvern_Character_BP_Base',
    '/Game/PrimalEarth/Dinos/Dodo/TurkeyBase_Character_BP.TurkeyBase_Character_BP',
    '/Game/PrimalEarth/Dinos/Dragon/Dragon_Character_BP_Boss',
    '/Game/PrimalEarth/Dinos/Dragon/Dragon_Character_BP',
    '/Game/PrimalEarth/Dinos/Giganotosaurus/BionicGigant_Character_BP_Malfunctioned',
    '/Game/PrimalEarth/Dinos/Giganotosaurus/Gigant_Character_BP_Base.Gigant_Character_BP_Base',
    '/Game/PrimalEarth/Dinos/Gorilla/Gorilla_Character_BP.Gorilla_Character_BP',
    '/Game/PrimalEarth/Dinos/Gorilla/Gorilla_Character_BP',
    '/Game/PrimalEarth/Dinos/Para/BionicPara_Character_BP_Malfunctioned',
    '/Game/PrimalEarth/Dinos/Quetzalcoatlus/BionicQuetz_Character_BP_Malfunctioned',
    '/Game/PrimalEarth/Dinos/Raptor/BionicRaptor_Character_BP_Malfunctioned',
    '/Game/PrimalEarth/Dinos/Rex/BionicRex_Character_BP_Malfunctioned_Adolescent',
    '/Game/PrimalEarth/Dinos/Rex/BionicRex_Character_BP_Malfunctioned',
    '/Game/PrimalEarth/Dinos/Spider-Large/SpiderL_Character_BP',
    '/Game/PrimalEarth/Dinos/Stego/BionicStego_Character_BP_Malfunctioned',
    '/Game/PrimalEarth/Dinos/Trike/BionicTrike_Character_BP_Malfunctioned',
    '/Game/ScorchedEarth/Dinos/Manticore/Manticore_Character_BP',
    '/Game/PrimalEarth/Dinos/Dimorphodon/Dimorph_Character_BP_Aggressive',
    '/Game/Aberration/Dinos/Nameless/Xenomorph_Character_BP_Female_CheatImpregnate',
    '/Game/Aberration/Dinos/Nameless/Xenomorph_Character_BP_Male_InitialBuryOnly',
    '/Game/Genesis/Dinos/VRMainBoss/VRMainBoss_Character_FORTESTING',
    '/Game/PrimalEarth/Dinos/CrystalWyvern/CrystalWyvern_Character_BP_Base',
    '/Game/PrimalEarth/Dinos/Dodo/TurkeyBase_Character_BP',
    '/Game/PrimalEarth/Dinos/Giganotosaurus/Gigant_Character_BP_Base',
    '/Game/PrimalEarth/Dinos/Tusoteuthis/Tusoteuthis_Character_BP_CaveBase',
    '/Game/ScorchedEarth/Dinos/Wyvern/Wyvern_Character_BP_ZombieBase',
    '/Game/ScorchedEarth/Dinos/Wyvern/Wyvern_Character_BP_Base',
    '/Game/ScorchedEarth/Dinos/JugBug/Jugbug_Character_BaseBP',
    '/Game/Mods/FjordurOfficial/Assets/Dinos/FenrirBoss/Hati/Hati_Character_BP',
    '/Game/Mods/FjordurOfficial/Assets/Dinos/FenrirBoss/Skoll/Skoll_Character_BP',
    '/Game/Genesis/Weapons/CruiseMissile/TekCruiseMissile_Character_BP',
    '/Game/Genesis2/Structures/RemoteCamera/RemoteCamera_Character_BP',
    '/Game/Mek_Character_Base_BP.Mek_Character_Base_BP',
    '/Game/SpaceWhale_Character_Base_BP',
]

VARIANT_OVERRIDES = {
    "/Game/Packs/Frontier/Dinos/Oasisaur/TamingDinos/Vulture_Character_BP_OasisaurTaming": {
        "Minion": True,
        "ScorchedEarth": True,
    },
    "/Game/ASA/Dinos/Fasolasuchus/Fasola_Character_BP": {
        "ScorchedEarth": True,
    },
    "/Game/Packs/Frontier/Dinos/Oasisaur/Oasisaur_Character_BP": {
        "ScorchedEarth": True,
    },
}

TAMING_OVERRIDES = {
    '/Game/PrimalEarth/Dinos/Rhyniognatha/Rhynio_Character_BP': {
        'violent': False,
        'nonViolent': True,
    },
    '/Game/Aberration/Dinos/Nameless/Xenomorph_Character_BP': {
        'violent': False,
        'nonViolent': False,
    },
    '/Game/Aberration/Dinos/Nameless/Xenomorph_Character_BP_Male': {
        'violent': False,
        'nonViolent': False,
    },
    '/Game/Genesis/Dinos/Shapeshifter/Shapeshifter_Large/Shapeshifter_Large_Character_BP': {
        'violent': False,
        'nonViolent': False,
    },
    '/Game/Genesis/Dinos/Shapeshifter/Shapeshifter_Small/Shapeshifter_Small_Character_BP': {
        'violent': False,
        'nonViolent': True,
    },
    '/Game/Genesis2/Dinos/SpaceDolphin/SpaceDolphin_Character_BP': {
        'violent': False,
        'nonViolent': True,
    },
    '/Game/Genesis2/Dinos/TekStrider/TekStrider_Character_BP': {
        'violent': False,
        'nonViolent': True,
    },
}

OUTPUT_OVERRIDES = {
    '/Game/ASA/Dinos/Fasolasuchus/Fasola_Character_BP': {
        "immobilizedBy": [ "Chain Bola", "Large Bear Trap", "Plant Species Y" ],
    },
    '/Game/Packs/Frontier/Dinos/Oasisaur/Oasisaur_Character_BP': {
        "taming": {
            "violent": False,
            "nonViolent": True,
        }
    },
    '/Game/PrimalEarth/Dinos/Mosasaurus/Mosa_Character_BP_Cave': {
        "name": 'Mosasaurus', # consistency (was Mosasaur)
    },
    '/Game/PrimalEarth/Dinos/IceGolem/IceGolem_Character_BP': {
        "name": 'Ice Golem',
    },
    '/Game/Mods/Valguero/Assets/Dinos/RockGolem/IceGolem/IceGolem_Character_BP': {
        "name": 'Ice Golem',
    },
    '/Game/Mods/Valguero/Assets/Dinos/RockGolem/ChalkGolem/ChalkGolem_Character_BP': {
        "name": 'Chalk Golem',
    },
    '/Game/PrimalEarth/Dinos/Purlovia/Purlovia_Character_BP_Polar': {
        "name": 'Polar Purlovia',
    },
    '/Game/PrimalEarth/Dinos/Coelacanth/Coel_Character_BP_Aberrant': {
        "name": 'Aberrant Coelacanth', # fixes in-game typo
    },
    '/Game/PrimalEarth/Dinos/Coelacanth/Coel_Character_BP_VDay_Aberrant': {
        "name": 'Aberrant Coelacanth', # fixes in-game typo
    },
    '/Game/ScorchedEarth/Dinos/Jerboa/Bone_Jerboa_Character_BP': {
        "name": 'Skeletal Jerboa', # was just Jerboa
    },
    '/Game/PrimalEarth/Dinos/Dragon/Dragon_Character_BP_Boss_Easy': {
        "name": 'Dragon',
    },
    '/Game/PrimalEarth/Dinos/Dragon/Dragon_Character_BP_Boss_Medium': {
        "name": 'Dragon',
    },
    '/Game/PrimalEarth/Dinos/Dragon/Dragon_Character_BP_Boss_Hard': {
        "name": 'Dragon',
    },
    '/Game/PrimalEarth/Dinos/Gorilla/Gorilla_Character_BP_Easy': {
        "name": 'Megapithecus',
    },
    '/Game/PrimalEarth/Dinos/Gorilla/Gorilla_Character_BP_Medium': {
        "name": 'Megapithecus',
    },
    '/Game/PrimalEarth/Dinos/Gorilla/Gorilla_Character_BP_Hard': {
        "name": 'Megapithecus',
    },
    '/Game/PrimalEarth/Dinos/Spider-Large/SpiderL_Character_BP_Easy': {
        "name": 'Broodmother Lysrix',
    },
    '/Game/PrimalEarth/Dinos/Spider-Large/SpiderL_Character_BP_Medium': {
        "name": 'Broodmother Lysrix',
    },
    '/Game/PrimalEarth/Dinos/Spider-Large/SpiderL_Character_BP_Hard': {
        "name": 'Broodmother Lysrix',
    },
    '/Game/ScorchedEarth/Dinos/Manticore/Manticore_Character_BP_Easy': {
        "name": 'Manticore',
    },
    '/Game/ScorchedEarth/Dinos/Manticore/Manticore_Character_BP_Medium': {
        "name": 'Manticore',
    },
    '/Game/ScorchedEarth/Dinos/Manticore/Manticore_Character_BP_Hard': {
        "name": 'Manticore',
    },
    '/Game/EndGame/Dinos/Endboss/EndbossDragon/EndBossDragon_Character_BP_Easy': {
        "name": 'Dragon',
    },
    '/Game/EndGame/Dinos/Endboss/EndbossDragon/EndBossDragon_Character_BP_Medium': {
        "name": 'Dragon',
    },
    '/Game/EndGame/Dinos/Endboss/EndbossDragon/EndBossDragon_Character_BP_Hard': {
        "name": 'Dragon',
    },
    '/Game/EndGame/Dinos/Endboss/EndbossGorilla/EndBossGorilla_Character_BP_Easy': {
        "name": 'Megapithecus',
    },
    '/Game/EndGame/Dinos/Endboss/EndbossGorilla/EndBossGorilla_Character_BP_Medium': {
        "name": 'Megapithecus',
    },
    '/Game/EndGame/Dinos/Endboss/EndbossGorilla/EndBossGorilla_Character_BP_Hard': {
        "name": 'Megapithecus',
    },
    '/Game/EndGame/Dinos/Endboss/EndbossSpider/EndBossSpiderL_Character_BP_Easy': {
        "name": 'Broodmother Lysrix',
    },
    '/Game/EndGame/Dinos/Endboss/EndbossSpider/EndBossSpiderL_Character_BP_Medium': {
        "name": 'Broodmother Lysrix',
    },
    '/Game/EndGame/Dinos/Endboss/EndbossSpider/EndBossSpiderL_Character_BP_Hard': {
        "name": 'Broodmother Lysrix',
    },
}

MANUAL_SPECIES = {
    '/Gigantoraptor/Gigantoraptor/Gigantoraptor_Character_BP.Gigantoraptor_Character_BP': {
			"name": "Gigantoraptor",
			"blueprintPath": "/Gigantoraptor/Gigantoraptor/Gigantoraptor_Character_BP.Gigantoraptor_Character_BP",
			"skipWildLevelStats": 512,
			"fullStatsRaw": [
				[ 770, 0.2, 0.27, 0.5, 0 ],
				[ 350, 0.1, 0.1, 0, 0 ],
				[ 950, 0.06, 0, 0.5, 0 ],
				[ 150, 0.1, 0.1, 0, 0 ],
				[ 3000, 0.1, 0.1, 0, 0.15 ],
				None,
				None,
				[ 320, 0.02, 0.04, 0, 0 ],
				[ 1, 0.05, 0.1, 0.5, 0.4 ],
				[ 1, 0, 0.01, 0, 0 ],
				None,
				None
			],
			"colors": [
				{ "name": "Body Main" },
				{ "name": "Neck Main" },
				{ "name": "Feather Tips" },
				{ "name": "Feather Highlights" },
				{ "name": "Legs And Beak" },
				{ "name": "Feather Pattern" }
			],
			"immobilizedBy": [ "Chain Bola", "Large Bear Trap", "Plant Species Y" ],
			"breeding": {
				"gestationTime": 0,
				"incubationTime": 5999.52004,
				"eggTempMin": 26,
				"eggTempMax": 32,
				"maturationTime": 166666.667,
				"matingCooldownMin": 64800,
				"matingCooldownMax": 172800
			},
			"taming": {
				"nonViolent": True,
				"violent": False,
				"tamingIneffectiveness": 0.06,
				"affinityNeeded0": 6800,
				"affinityIncreasePL": 160,
				"torporDepletionPS0": 2.8333332,
				"foodConsumptionBase": 0.002314,
				"foodConsumptionMult": 180.0634,
				"babyFoodConsumptionMult": 510
			},
			"displayedStats": 927
		},
}

COLOR_REGION_WHITELIST = {
    '/Game/ASA/Dinos/Fasolasuchus/Fasola_Character_BP',
    '/Game/Packs/Frontier/Dinos/Oasisaur/Oasisaur_Character_BP',
    '/Gigantoraptor/Gigantoraptor/Gigantoraptor_Character_BP',
    # '/Game/ScorchedEarth/Dinos/Jerboa/Jerboa_Character_BP',
    '/Game/ScorchedEarth/Dinos/Wyvern/Wyvern_Character_BP_Lightning',
}

COLOR_REGION_BAD_NAMES = set(map(str.lower, [
    # '**ignore**nothing**',
]))


class RegionInfo(TypedDict):
    name: Optional[str]
    colors: Optional[list[str]]


COLOR_OVERRIDES: dict[str, dict[int, Optional[RegionInfo]]] = {
    '/Game/ASA/Dinos/Fasolasuchus/Fasola_Character_BP': {
        0: { "name": "Body Main" },
        1: { "name": "Body Spots" },
        2: { "name": "Spikes" },
        3: None,
        4: { "name": "Body Rings" },
        5: { "name": "Head/Back Highlights" },
    },
} # type: ignore


VALUE_DEFAULTS = {
    'TamedBaseHealthMultiplier': 1,
}
