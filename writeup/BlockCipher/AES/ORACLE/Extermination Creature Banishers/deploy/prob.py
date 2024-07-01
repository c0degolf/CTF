#!/usr/bin/env python3
from os import urandom
from random import random, choice
from typing import Literal
import json
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

CREATURE_NAME_POOL = [
    'Shadowfang',
    'Nightshade',
    'Bloodfiend',
    'Dreadclaw',
    'Bonecrusher',
    'Hellfire',
    'Frostbite',
    'Voidspawn',
    'Soulripper',
    'Cursedspawn',
    'Deathcoil',
    'Venomspitter',
    'Demonlord',
    'Leviathan',
    'Necrotic',
    'Chaosbeast',
    'Abyssal Horror',
    'Deathwing',
    'Behemoth',
    'Krakenbane'
]

class Creature:
    def __init__(self):
        self.name = choice(CREATURE_NAME_POOL)
        self.critical_cmd = "critical_attack_"+urandom(8).hex()
        self.mode: Literal[1,2] = AES.MODE_ECB if random()>0.5 else AES.MODE_CBC
    def get_mode(self) -> Literal[1,2]:
        return self.mode
    def get_name(self) -> str:
        return self.name
    def get_critical_cmd(self) -> str:
        return self.critical_cmd
    def info(self) -> str:
        return json.dumps({"name":self.name,"critical":self.critical_cmd,"aes_mode":self.mode})


class User:
    def __init__(self,name):
        self.name = name
        self.life = 3
        self.stamina = 3000
    def get_name(self) -> str:
        return self.name
    def get_life(self) -> int:
        return self.life
    def get_stamina(self) -> int:
        return self.stamina
    def get_damage(self) -> None:
        self.life -= 1
    def use_stamina(self) -> None:
        self.stamina -= 1
    def reset_stamina(self):
        self.stamina = 3000
    def is_dead(self) -> bool:
        return self.life == 0

class Game:
    def __init__(self) -> None:
        self.win_n = 0
        self.user = self._game_init()

    def _game_init(self) -> User:
        print("\nWelcome to the world of `Extermination: Creature Banishers`!\n")
        print("Greetings adventurer, What is your name?")
        name = input("> ")
        print(f"Nice Name! {name}")
        print("This world is in danger from creatures. \
              Eliminate the creatures and save this world.")
        print("If you slay enough creatures, you will be rewarded!")
        return User(name)

    def print_status(self,status_name, status) -> None:
        print(f'<{status_name}>')
        print(base64.b64encode(status).decode())
        print()

    def play(self) -> None:
        while True:
            print()
            if self.win_n == 10:
                print("Well done!")
                with open("flag", "rb") as flag:
                    print(flag.read().decode())
                break
            if self.user.is_dead():
                print("You Died...")
                break

            creature = Creature()
            creature_info = json.loads(creature.info())
            creature_name = creature.get_name()
            creature_mode = creature.get_mode()

            cipher = AES.new(urandom(16), creature_mode)
            stage_status = json.dumps({"user_name":self.user.get_name(),
                                       "creature_info":creature_info})
            print(stage_status)
            enc_stage_status = cipher.encrypt(pad(stage_status.encode(),16))
            self.print_status("Stage Status", enc_stage_status)

            print(f"Wild {creature_name} appeared!")
            print("1. Fight    2. Run")
            action = int(input("> "))
            if action == 2:
                print("Run away...")
            elif action == 1:
                print(f"Ok! Let's fight with {creature_name}!")
                win = self.fight(creature)
                if win:
                    print(f"You slayed {creature_name}!")
                    self.win_n += 1
                else:
                    print("Ouch!")
                    self.user.get_damage()
            else:
                print('invalid action')
                break

    def fight(self, creature: Creature) -> bool:
        user_cmd = ''
        creature_info = json.loads(creature.info())
        creature_name = creature.get_name()
        creature_mode = creature.get_mode()
        critical_cmd = creature.get_critical_cmd()
        while True:
            print()
            cipher = AES.new(urandom(16), creature_mode)
            fight_status = json.dumps({'user_cmd':user_cmd,"creature_info":creature_info})
            enc_fight_status = cipher.encrypt(pad(fight_status.encode(),16))
            print(fight_status)
            self.print_status("Fight Status", enc_fight_status)

            print(f"Fight with {creature_name}")
            user_cmd = input("Attack Command: ")
            if user_cmd == critical_cmd:
                print("Critical attack!")
                win = True
                break
            print("Nothing happend...")
            self.user.use_stamina()

            if self.user.get_stamina() == 0:
                print("Run out of stamina.... ")
                win = False
                break
        return win

if __name__ == '__main__':
    while True:
        print("[+] Starting Game ... ")
        game = Game()
        game.play()
        again = input("[+] Do you want to play again? (y/n) ")
        if again == "y":
            continue
        break
