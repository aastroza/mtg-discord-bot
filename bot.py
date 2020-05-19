from utils import hypergeom_cdf
from discord.ext import commands
import os
import random

TOKEN = os.environ.get('TOKEN', None)

def getProbability(N, A, n, t):
    #Probability of having at least t cards
    p1 = hypergeom_cdf(N, A, n, t, min_value=t, max_value=n)

    #Probability of having exactly t cards
    p2 = hypergeom_cdf(N, A, n, t, min_value=t)

    #Probability of having at most t cards
    p3 = hypergeom_cdf(N, A, n, t)

    return round(100*p1,2), round(100*p2,2), round(100*p3,2)


bot = commands.Bot(command_prefix='!')
with open('rap.txt') as f:
    rap = f.readlines()
rap = [x.strip() for x in rap] 


@bot.command(name='odds', help='What are the odds of drawing X copies of a card?\n Example: !odds ncards_deck ntargetcards_in_deck ncards_draw ntargetcards_wanted')
async def odds(ctx, *args):

    if (len(args) == 4):
        ncards_deck = int(args[0])
        ntargetcards_in_deck = int(args[1])
        ncards_draw = int(args[2])
        ntargetcards_wanted = int(args[3])

        if(ntargetcards_wanted == 1):
            text_copies = 'copy'
        else:
            text_copies = 'copies'
        
        probs = getProbability(ncards_deck, ntargetcards_in_deck, ncards_draw, ntargetcards_wanted)
        response = 'Probability of drawing **at least** '+str(ntargetcards_wanted)+' '+text_copies+' of the card is: '+str(probs[0])+' %.\n'+'Probability of drawing **exactly** '+str(ntargetcards_wanted)+' '+text_copies+' of the card is: '+str(probs[1])+' %.\n'+'Probability of drawing **at most** '+str(ntargetcards_wanted)+' '+text_copies+' of the card is: '+str(probs[2])+' %.'
        
    else:
        response = "What are the odds of drawing X copies of a card?\n Example: !odds ncards_deck ntargetcards_in_deck ncards_draw ntargetcards_wanted"

    await ctx.send(response)

@bot.command(name='thiago', help='El rap de Thiaaaago Silvaaaa')
async def odds(ctx, *args):

    response = random.choice(rap)
    await ctx.send(response)



bot.run(TOKEN)