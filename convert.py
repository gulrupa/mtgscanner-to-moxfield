#!/usr/bin/env python3

import argparse
import csv
from dataclasses import dataclass
from os import PathLike
from os.path import exists
from collections import defaultdict
from pathlib import Path


condition_map = defaultdict(
    lambda: '',
    Mint="M",
    NearMint="NM",
    Excellent="NM",
    Good="LP",
    LightPlayed="MP",
    Played="HP",
    Poor="D"
    )

moxfield_headers = [
    "Count",
    "Name",
    "Edition",
    "Condition",
    "Language",
    "Foil",
    "Collector Number"
    ]


@dataclass(frozen=True, slots=True)
class CardData:
    quantity: str
    name: str

    def get_output_dict(self) -> dict[str, str]:
        return str(self.quantity) + " " + self.name + "\n"
            

def generate_cards(csv_path: PathLike) -> list[CardData]:
    retval: list[CardData] = []

    with open(csv_path, 'r') as csv_file:
        # The first line is a seperator definition
        seperator = ","
        csv_reader = csv.DictReader(csv_file, delimiter=seperator)

        data_row: dict
        for data_row in csv_reader:
            # Dragon Shield adds a junk data row at the end
            if data_row['Quantity'] == '':
                continue

            card = CardData(
                data_row['Quantity'],
                data_row['Name'],
                )

            retval.append(card)

    return retval


def convert(in_path: PathLike, out_path: PathLike) -> None:
    if not exists(in_path):
        raise FileNotFoundError(
            f'{in_path} not found. Place file in root folder.')

    card_data = generate_cards(in_path)

    with open(out_path, 'w', newline='') as out_file:
        print("Copy path following text to moxfield or use the moxfield.txt genrated file.")
        for card in card_data:
            print(card.get_output_dict(), end="")
            out_file.write(card.get_output_dict())


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
                    prog='MTGScanner to Moxfield',
                    description='Generate a moxfield .txt deck list for moxfield import using a MTG Scanner : DragonShied .csv export',
                    epilog='Have Fun')
    arg_parser.add_argument('infile')           # positional argument
    arg_parser.add_argument('outfile')           # positional argument
    args = arg_parser.parse_args()
    input_path = Path(args.infile)
    output_path = Path(args.outfile)
    convert(input_path, output_path)
