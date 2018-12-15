from conf import twitch_instance, twitch_channel, streamer, welcome_msg, is_bot_admin, bot_name
import asyncio
from obs_ctrl import change_scene, get_scene
from twitch_permissions import is_bot, is_mod
import time
import random
import api_integrations


# config ze bot!
twitch_bot = twitch_instance

# global vars
emote_count = 0
emotes_this_raid = 0
attacker_score = 0
defender_score = 0
raid_status = False
raid_defenders = []
raid_attackers = []

# ─── CLASSES ────────────────────────────────────────────────────────────────────

# defenders = RaidDefenders(current_members)
# attackers = RaidAttackers(raid_members)
# new_raid = Raid(current_members, raid_members)

class Raid:
    'Keeps track of the status and history of raids'

    raiders = {}

    def __init__(self, attackers, defenders):
        self.status = True
        self.time = time.time() # TODO format this better kthx
        self.attackers = attackers
        self.defenders = defenders


class RaidDefenders:
    'Everyone that was in the channel before the raid started.'

    def __init__(self, defenders):
        self.members = defenders
        self.hp = 100
        self.emotes = 0
        # healing vs attacking emotes?
        # emote dmg/weight??


class RaidAttackers:
    'Everyone that entered the channel after the raid started.'

    def __init__(self, attackers):
        self.members = attackers
        self.hp = 100
        self.emotes = 0
        # healing vs attacking emotes?
        # emote dmg/weight??


# ─── RAID SEQUENCE ──────────────────────────────────────────────────────────────
 
def raid_is_happening():
    global raid_status
    return raid_status

def count_emotes(message):
    global emote_count
    emote_count += len(message.emotes)
    return emote_count


#trigger teh start of a raid
def raid_start(message):
    # chk the message or webhooks for raid triggers
    if "trigger raid" in message.content.lower():
        return True


def raid_event(message):
    success_msg = "raid triggered successfully"
    print(success_msg)
    # lock all other reacts
    # say who's raiding & with how many pplz
    # say who won last raid
    # start counting emotes


def emotes_spammed():
    global emotes_this_raid
    return emotes_this_raid


def keep_score(message):
    global attacker_score
    global defender_score
    global raid_attackers
    global raid_defenders

    if message.author.name.lower() in raid_attackers:
        attacker_score += len(message.emotes)
        
    if message.author.name.lower() in raid_defenders:
        defender_score += len(message.emotes)


def split_chatters(chatters):
    # random.shuffle(chatters)
    # index = len(chatters)//2
    # return chatters[:index]
    return random.sample(chatters, len(chatters)//2)

def who_raided():
    """
    Returns a list of who just raided. For now, this randomly splits the current
    members of the room between attackers & defenders.

    Eventually, this will be a difference of who was in the room before the raid,
    and who was in the room after the raid webhook dropped.
    """
    global raid_defenders
    global raid_attackers 

    # DEBUG: shuffle the list & split the chatters in two
    attackers = split_chatters(raid_defenders) # returns half of a shuffled list
    
    # take a diff of the list (attackers)
    for member in attackers:
        raid_defenders.remove(member)

    return attackers


def assign_teams(): 
    'Determines attackers & defenders for the raid'

    global raid_attackers
    global raid_defenders
  
    raid_defenders = api_integrations.get_chatters()    # TODO: eventually this will happen periodically
    raid_attackers = who_raided() # DEBUG

    # make the lits legible
    attackers_printable = raid_attackers
    attackers_printable = '[%s]' % ', '.join(map(str, attackers_printable))
    attackers_printable = attackers_printable.strip('[]')
    defenders_printable = raid_defenders
    defenders_printable = '[%s]' % ', '.join(map(str, defenders_printable))
    defenders_printable = defenders_printable.strip('[]')

    # print out who we gots
    print('attackers: {} \n'.format(attackers_printable))
    print('defenders: {}'.format(defenders_printable))



# def keep_score(message):
    # global emotes_this_raid
    # emotes_this_raid += len(message.emotes)


def reset_emote_count():
    global emote_count
    emote_count = 0


def reset_raid_score():
    global attacker_score
    global defender_score
    global raid_attackers
    global raid_defenders

    attacker_score = 0
    defender_score = 0
    raid_attackers[:] = []
    raid_defenders[:] = []

# def reset_raid_score():
#     global emotes_this_raid
#     emotes_this_raid = 0

# debug
def get_attacker_score():
    return attacker_score

# debug
def get_defender_score():
    return defender_score
        

#start counting emotes & keep score

#report score (emote count)



@twitch_bot.command('raid')
async def raid(message):
    if is_mod(message) or message.author.name == "streamelements":
        await asyncio.sleep(4)
        await twitch_bot.say(message.channel, "!redalert")  # RED LIGHTS

        await asyncio.sleep(5)  # 9s BSOD
        change_scene('BSOD')
        
        await asyncio.sleep(6)  # 15s
        msg = 'ATTENTION, NINJAS! We\'ve been RAIDED! Our networks are vulnerable!!'
        await twitch_bot.say(message.channel, msg)
        
        await asyncio.sleep(10)  # 25s Switch to HackerTyper
        change_scene('RAID')
        
        await asyncio.sleep(4) 
        msg = 'Type defendNetwork(); to harness avilable blockchains and boost our firewall\'s signal.'
        await twitch_bot.say(message.channel, msg)

        await asyncio.sleep(10) 
        msg = 'Network defenses are failing. Initiate all protocols! Pizza! Donuts! Bacon!! THROW ALL WE\'VE GOT AT THEM!!'
        await twitch_bot.say(message.channel, msg)

        await asyncio.sleep(5) # 40s Pizza
        await twitch_bot.say(message.channel, "pizzaProtocol();")

                
@twitch_bot.command('raidover')
async def raidover(message):
    if is_mod(message):
        msg = "!disabled3"
        await twitch_bot.say(message.channel, msg)
        change_scene('RAID2')
        await twitch_bot.say(message.channel, "Keepo")
        await asyncio.sleep(2) #
        change_scene('MAIN')

   

# ─── DEBUG COMMANDS ─────────────────────────────────────────────────────────────

@twitch_bot.command('debugreacts')
async def debugreacts(message):
    """
    DEBUG: change msg var to print whatever var u tryin'a lern gooder
    """
    msg = bot_name().lower()   
    await twitch_bot.say(message.channel, msg)

def raid_in_progress(message):
    # chk the message or webhooks for raid triggers
    if "trigger raid" in message.content.lower():
        print("raid in progress")
        return True

# switch scene to GAMES    
@twitch_bot.command('emote')
async def emote(message):
    # print(message.content.emotes)
    print(message.emotes)
    count = 0
    for emote in message.emotes:
        count = count + 1
    await twitch_bot.say(message.channel, str(count)) 
    # except:
    #     msg = "no emotes"
    #     await twitch_bot.say(message.channel, msg) 


@twitch_bot.command('testraid')
async def testraid(message):
    global raid_status

    assign_teams()

    # flip the bool bit thing so on_message can process emotes
    raid_status = True

    msg = 'raid in progress. spam a few emotes for teh test! kthx <3'
    await twitch_bot.say(message.channel, msg)


@twitch_bot.command('endraidtest')
async def endraidtest(message):
    global raid_status
    global emotes_this_raid

    # flip the bool bit thing again
    raid_status = False

    # report the score
    msg = 'raid ended. {} emotes were spammeded. Attackers: {}, Defenders: {}'.format(
        attacker_score + defender_score, attacker_score, defender_score
        )
    await twitch_bot.say(message.channel, msg) 

    reset_raid_score()


# @twitch_bot.command('endraidtest')
# async def endraidtest(message):
#     # flip the bool bit thing again
#     global raid_status
#     global emotes_this_raid
#     raid_status = False
#     # spit out the count of emotes that were dropped during the raid
#     msg = 'raid ended. {} emotes were spammeded.'.format(emotes_this_raid)
#     await twitch_bot.say(message.channel, msg) 
#     msg = 'state={}'.format(raid_status)
#     await twitch_bot.say(message.channel, msg) 
#     reset_raid_score()


@twitch_bot.command('raidstate')
async def raidstate(message):
    # flip the bool bit thing
    global raid_status
    if raid_status:
        msg = 'raid in progress.'
        await twitch_bot.say(message.channel, msg)
    else:
        msg = 'not in a raid rn'
        await twitch_bot.say(message.channel, msg)

# command registers that it needs to start counting emotes
    # do the bool thing

# count emotes every message
    """
    This is going to have to happen in a "on message" (twitch_chat.py) and somehow have
    access to the bool in *this* script. 0_o
    """

# command that stops counting 
    # report & of emotes during period