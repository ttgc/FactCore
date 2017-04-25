#!usr/bin/env python3.4
#-*-coding:utf-8-*-
#Fact Core For Citranium by ttgc and Indianajaune

import discord
import asyncio
import logging
from random import *
from INIfiles import *
import time
import os

global prefixes,statut,config
prefixes = {}
statut = discord.Game(name="Facts")

logger = logging.getLogger('discord')
logging.basicConfig(level=logging.INFO)
handler = logging.FileHandler(filename='Logs/discord.log',encoding='utf-8',mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

def convert_str_into_dic(string):
    if string == "{}": return {}
    string = string.replace("{","")
    string = string.replace("}","")
    string = string.replace("'","")
    #string = string.replace(" ","")
    ls = string.split(", ")
    dic = {}
    for i in range(len(ls)):
        temp = ls[i].split(": ")
        dic[temp[0]] = temp[1]
    return dic

def convert_str_into_ls_spe(string):
    if string == "{}": return []
    string = string.replace("{","")
    string = string.replace("}","")
    string = string.replace("'","")
    ls = string.split(", ")
    return ls

def convert_ls_into_str_spe(ls):
    string = str(ls)
    string = string.replace("[","{")
    string = string.replace("]","}")
    return string

def save_data():
    global config,prefixes
    config.key_add("main","prefix",str(prefixes))
    config.save("config")

client = discord.Client()

@client.event
@asyncio.coroutine
def on_ready():
    global statut
    yield from client.change_presence(game=statut)

@client.event
@asyncio.coroutine
def on_message(message):
    global prefixes,statut
    if message.server == None: return
    owner = admin = False
    #check permissions
    if message.author == message.server.owner:
        owner = admin = True
    perms = message.channel.permissions_for(message.author)
    hierarchy = message.server.role_hierarchy
    admin = perms.administrator
    #get prefix
    prefix = prefixes[str(message.server.id)]
    #commands
    if message.content.startswith(prefix+'roll'):
        value = int(message.content.replace(prefix+'roll ',""))
        dice = randint(1,value)
        yield from client.send_message(message.channel,":game_die: You scored "+str(dice)+"/"+str(value)+" ! :game_die:")
    if message.content.startswith(prefix+'yay'):
        f = open("YAY.PNG","rb")
        yield from client.send_file(message.channel,f,content="YAY !")
        f.close()
    if message.content.startswith(prefix+'invite'):
        url = discord.utils.oauth_url(str(client.user.id),discord.Permissions().all())
        embd = discord.Embed(title="FactCore",description="Invite FactCore to your server !",colour=discord.Color(randint(0,int('ffffff',16))),url=url)
        embd.set_footer(text="FactCore developed by Aperture Science",icon_url=client.user.avatar_url)
        embd.set_image(url=client.user.avatar_url)
        embd.set_thumbnail(url="http://cdn.themis-media.com/media/global/images/library/deriv/1298/1298055.jpg")
        embd.set_author(name="Aperture Science",icon_url="http://eiden.yolasite.com/resources/logown6.png",url=url)
        embd.add_field(name="FactCore is currently on :",value=str(len(prefixes))+" Server(s)",inline=False)
        yield from client.send_message(message.channel,embed=embd)
    if message.content.startswith(prefix+'prefix'):
        newpre = message.content.replace(prefix+'prefix ',"")
        prefixes[str(message.server.id)] = newpre
        yield from client.send_message(message.channel,"Prefix has been changed for : "+newpre)
    if message.content.startswith(prefix+'randomfact'):
        fact = choice([
                "The billionth digit of Pi is 9.",
                "Humans can survive underwater. But not for very long.",
                "A nanosecond lasts one billionth of a second.",
                "Honey does not spoil.",
                "The atomic weight of Germanium is seven two point six four.",
                "An ostrich's eye is bigger than its brain.",
                "Rats cannot throw up.",
                "Iguanas can stay underwater for twenty-eight point seven minutes.",
                "The moon orbits the Earth every 27.32 days.",
                "A gallon of water weighs 8.34 pounds.",
                "According to Norse legend, thunder god Thor's chariot was pulled across the sky by two goats.",
                "Tungsten has the highest melting point of any metal, at 3,410 degrees Celsius.",
                "Gently cleaning the tongue twice a day is the most effective way to fight bad breath.",
                "The Tariff Act of 1789, established to protect domestic manufacture, was the second statute ever enacted by the United States government.",
                "The value of Pi is the ratio of any circle's circumference to its diameter in Euclidean space.",
                "The Mexican-American War ended in 1848 with the signing of the Treaty of Guadalupe Hidalgo.",
                "In 1879, Sandford Fleming first proposed the adoption of worldwide standardized time zones at the Royal Canadian Institute.",
                "Marie Curie invented the theory of radioactivity, the treatment of radioactivity, and dying of radioactivity.",
                "At the end of The Seagull by Anton Chekhov, Konstantin kills himself.",
                "Hot water freezes quicker than cold water.",
                "The situation you are in is very dangerous.",
                "Polymerase I polypeptide A is a human gene. The shortened gene name is POLR1A",
                "Cellular phones will not give you cancer. Only hepatitis.",
                "In Greek myth, Prometheus stole fire from the Gods and gave it to humankind. The jewelry he kept for himself.",
                "The Schrodinger's cat paradox outlines a situation in which a cat in a box must be considered, for all intents and purposes, simultaneously alive and dead. Schrodinger created this paradox as a justification for killing cats.",
                "In 1862, Abraham Lincoln signed the Emancipation Proclamation, freeing the slaves. Like everything he did, Lincoln freed the slaves while sleepwalking, and later had no memory of the event.",
                "The plural of surgeon general is surgeons general. The past tense of surgeons general is surgeonsed general",
                "Contrary to popular belief, the Eskimo does not have one hundred different words for snow. They do, however, have two hundred and thirty-four words for fudge.",
                "Halley's Comet can be viewed orbiting Earth every seventy-six years. For the other seventy-five, it retreats to the heart of the sun, where it hibernates undisturbed.",
                "The first commercial airline flight took to the air in 1914. Everyone involved screamed the entire way.",
                "Edmund Hillary, the first person to climb Mount Everest, did so accidentally while chasing a bird.",
                "We will both die because of your negligence.",
                "This is a bad plan. You will fail.",
                "He will most likely kill you, violently.",
                "He will most likely kill you.",
                "You will be dead soon.",
                "You are going to die in this room.",
                "The Fact Sphere is a good person, whose insights are relevant.",
                "The Fact Sphere is a good sphere, with many friends.",
                "Dreams are the subconscious mind's way of reminding people to go to school naked and have their teeth fall out.",
                "The occupation of court jester was invented accidentally, when a vassal's epilepsy was mistaken for capering.",
                "Before the Wright Brothers invented the airplane, anyone wanting to fly anywhere was required to eat 200 pounds of helium.",
                "Before the invention of scrambled eggs in 1912, the typical breakfast was either whole eggs still in the shell or scrambled rocks.",
                "During the Great Depression, the Tennessee Valley Authority outlawed pet rabbits, forcing many to hot glue-gun long ears onto their pet mice.",
                "This situation is hopeless."",
                "Diamonds are made when coal is put under intense pressure. Diamonds put under intense pressure become foam pellets, commonly used today as packing material."
                ])
        yield from client.send_message(message.channel,fact)
    if client.user in message.mentions and message.author != client.user:
        yield from client.add_reaction(message,"\U0001F44D")
    #save data
    save_data()

@client.event
@asyncio.coroutine
def on_server_join(server):
    global prefixes
    prefixes[str(server.id)] = '/'
    save_data()

@client.event
@asyncio.coroutine
def on_server_remove(server):
    global prefixes
    del(prefixes[str(server.id)])
    save_data()

@asyncio.coroutine
def main_task():
    yield from client.login("MjM0NjM5NTIwMzM3ODg3MjMy.C-Cj6A.2twfX3KzQKtmcIX5KMCvIfMjBg4")
    yield from client.connect()
    yield from client.wait_until_ready()

def launch():
    global config,prefixes
    config = INI()
    config.load("config")
    prefixes = convert_str_into_dic(config.section["main"]["prefix"])

launch()
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main_task())
except:
    loop.run_until_complete(client.logout())
finally:
    loop.close()
