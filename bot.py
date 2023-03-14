from lang import *
from words import *
from weather import *
from countries import *
from trivia import *
from discord.ext import commands
import discord
import logging
import asyncio
from datetime import datetime
import random
import youtube_dl
import os
from googletrans import Translator
import requests
import json

logging.basicConfig(level=logging.INFO)
bot = commands.Bot(command_prefix = '.', activity = discord.Game(name = 'Mos ramolit | .ajutor'), status = discord.Status.idle)
TOKEN = 'zulul'

@bot.event
async def on_ready():
    print('Bot {0.user} online'.format(bot))

@bot.command() # REPARA ARG MAI MULTE CUVINTE
async def spam(ctx, arg, arg2):
    for i in range(int(arg2)):
        await ctx.send(arg)

@bot.command() # REPARA CIND PUNE CINEVA RAHAT IN LOC DE CIFRE
async def ghici(ctx):
    win = 0
    number = random.randint(1, 10)
    await ctx.send('Ma gandesc la un numar intre 1 si 10, ai 3 incercari sa il ghicesti!')
    for i in range(1, 4):
        try:
            answer = await bot.wait_for('message', timeout = 60.0)
        except asyncio.TimeoutError:
            return await ctx.send('De ce ma pui sa incep jocul degeaba? Pula Marian are si alte treburi sa stii.')
        guess = int(answer.content)
        if guess > number:
            await ctx.send('Numarul tau este mai MARE decat numarul meu, mai ai {} incercari!'.format(str(3 - i)))
        elif guess < number:
            await ctx.send('Numarul tau este mai MIC decat numarul meu, mai ai {} incercari!'.format(str(3 - i)))
        else:
            await ctx.send('Da, da, da! Nu imi vine sa cred! Sunt absolut socat! Incredibil! Pula Marian te felicita personal! Ai ghicit numarul din {} incercari!'.format(str(i)))
            win = 1
    if win == 0:
        await ctx.send('Hahaha ai pierdut! Ma gandeam la numarul {}.'.format(number))

@bot.command()
async def cauta(ctx, *args):
    await ctx.send('Pula Marian cauta... ' + ' '.join(args[:]))
    await ctx.send('https://www.pornhub.com/video/search?search={}'.format('+'.join(args[:])))
    await ctx.send('Ce ai zis? Nu voiai sa cauti pe PornHub? Vina mea...')

@bot.command()
async def wiki(ctx, arg, *args):
    await ctx.send('Pula Marian cauta... ' + ' '.join(args[:]))
    await ctx.send('https://{}.wikipedia.org/wiki/{}'.format(arg, '_'.join(args[:])))

@bot.command()
async def vot(ctx, *args):
    embed = discord.Embed(
        title = ' '.join(args[:]),
        timestamp = datetime.now(),
        color = 0xFFFFFF
    )
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('✅')
    await msg.add_reaction('❌')

@bot.command() # ADAUGA SISTEM DE SALVARE A CASTIGULUI
async def paca(ctx, arg):
    totalWinnings = 0
    symbols = []
    emojiList = ['7️⃣', '🐴', '💎', '🍌', '🔔', '🍒', '🍊', '🍋', '🍇', '🍉']
    bet = arg
    for i in range(3):
        symbols.append(random.choice(emojiList))
    await ctx.send(' | '.join(symbols))
    if symbols[0] == symbols[1] == symbols[2]:
        await ctx.send('Dumnezeule mare! Ne-ai imbogatit pe toti! Ai luat jackpot nebun in valoare de {} lei.'.format(int(bet) * 10))
        totalWinnings += int(bet) * 10
    elif symbols[0] == symbols[1] or symbols[0] == symbols[2] or symbols[1] == symbols[2]:
        await ctx.send('Ooo bine pe pacanea, ai obtinut {} lei.'.format(int(bet) * 2))
        totalWinnings += int(bet) * 2
    else:
        await ctx.send('Mai baga o fisa, sigur vei castiga ceva!')

@bot.command()
async def sterge(ctx, arg):
    await ctx.send('Pula Marian va sterge {} mesaje...'.format(arg))
    await ctx.channel.purge(limit = (int(arg) + 2))

@bot.command()
async def pula(ctx):
    await ctx.send('A spus cineva pula? Sunt Pula Marian si imi place sa sug pula!')

@bot.command() # REPARA CAND SUNT 2 LITERE IN CUVANT!
async def wordle(ctx):
    randomWordle = random.choice(POSSIBLE_WORDS)
    randomWordleSplit = list(randomWordle)
    wordleLights = []
    await ctx.send('''Reguli: 
    VERDE - Litera este in pozitia corecta; 
    GALBEN - Litera este in cuvant, dar nu in pozitia corecta; 
    NEGRU - Litera nu este in cuvant.''')
    await ctx.send('Am inceput Wordle! Ai 6 incercari sa ghicesti cuvantul englezesc format din 5 litere!')
    attempts = 6
    while attempts > 0:
        answer = await bot.wait_for('message')
        guess = answer.content.lower()
        if guess not in ALLOWED_WORDS:
            await ctx.send('Pula Marian a zis clar, un cuvant in englesa din 5 litere!')
            continue
        guessSplit = list(guess)
        for i in range(5):
            if guess == randomWordle:
                return await ctx.send('Wow! Incredibil! Bravo! Ce socat sunt! Ai ghicit cuvantul: {}!'.format(randomWordle))
            if guessSplit[i] == randomWordleSplit[i]:
                wordleLights.append('🟩')
            elif guessSplit[i] in randomWordleSplit:
                wordleLights.append('🟨')
            else:
                wordleLights.append('⬛')
        attempts -= 1
        await ctx.send('{}/6 incercari ramase: '.format(attempts) + ' | '.join(wordleLights))
        wordleLights = []
    await ctx.send('Ai ramas fara incercari! Cuvantul era {}.'.format(randomWordle))

@bot.command()
async def marian(ctx):
    await ctx.send(file=discord.File('C:\\Users\\ADY\\Desktop\\bot\\marian.jpg'))

@bot.command()
async def re(ctx, url : str, chan):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name = chan)
    await voiceChannel.connect()
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)

    opts = {
        'format': '249/250/251',
        'outtmpl': 'C:\\Users\\ADY\\Desktop\\bot\\music\\song.webm'
    }

    with youtube_dl.YoutubeDL(opts) as ytdl:
        ytdl.download([url])
    voice.play(discord.FFmpegOpusAudio('C:\\Users\\ADY\\Desktop\\bot\\music\\song.webm'))

@bot.command()
async def pa(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    os.remove('C:\\Users\\ADY\\Desktop\\bot\\music\\song.webm')
    if voice.is_connected():
        await voice.disconnect()

@bot.command()
async def st(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    if voice.is_playing():
        voice.pause()

@bot.command()
async def co(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    if voice.is_paused():
        voice.resume()

@bot.command()
async def op(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    voice.stop()

@bot.command()
async def trad(ctx, arg, *args):
    translator = Translator()
    translated = translator.translate(str(args[:]), dest=str(arg))
    shitText = str(translated.text)
    text = ''.join(char for char in shitText if char not in '(\',")')
    embed = discord.Embed(
        title='Tradus din {}:'.format(LANGUAGES[translated.src]),
        description='{}'.format(str(text)),
        color=0xFFFFFF
    )
    await ctx.send(embed=embed)
    
@bot.command()
async def rand(ctx, arg: discord.Member):
    allMessages = []
    for chan in ctx.guild.text_channels:
        async for msg in chan.history(limit=200):
            if str(msg.author) == str(arg):
                allMessages.append(msg)
    
    messageToSend = random.choice(allMessages)
    guildId = messageToSend.guild.id
    chanId = messageToSend.channel.id
    msgId = messageToSend.id
    link = 'https://discordapp.com/channels/{}/{}/{}'.format(guildId, chanId, msgId)

    embed = discord.Embed(
        title='Mesaj random trimis de {}:'.format(messageToSend.author),
        description='{}'.format(messageToSend.system_content),
        url=link,
        color=0xFFFFFF
    )
    await ctx.send(embed=embed)

@bot.command()
async def vreme(ctx, arg): # REPARA ORAS CU 2 CUVINTE
    completeUrl = BASE_URL + '?q=' + str(arg) + PARAM + '&appid=' + API_KEY
    response = requests.get(completeUrl)
    cityData = json.loads(response.text)
    try:
        currentWeather = cityData['weather'][0]['description']
        currentTemp = cityData['main']['temp']
        currentPres = cityData['main']['pressure']
        currentHum = cityData['main']['humidity']
        currentWind = cityData['wind']['speed']
        currentCountry = cityData['sys']['country'] 
        currentCity = cityData['name']
    except KeyError:
        return await ctx.send('Hopa! Pula Marian nu a gasit orasul acela!')
    embed = discord.Embed(
        title='👏🌞 Vremea in {}:'.format(arg),
        description='''**Vreme**: {}
        **Temperatura**: {} °C
        **Presiune atmosferica**: {} hPa
        **Umiditate**: {} %
        **Viteza vantului**: {} m/s
        **Tara**: {}
        **Oras**: {}'''.format(currentWeather, currentTemp, currentPres, currentHum, currentWind, COUNTRY_CODES[currentCountry], currentCity),
        url=str(completeUrl),
        timestamp=datetime.now(),
        color=0xFFFFFF
    )
    await ctx.send(embed=embed)

@bot.command()
async def urban(ctx, *args):
    await ctx.send('Pula Marian cauta...')
    await ctx.send('https://www.urbandictionary.com/define.php?term={}'.format('%20'.join(args[:])))

@bot.command()
async def trivia(ctx, arg):
    triviaUrl = 'https://api.gazatu.xyz/trivia/questions?count={}&include={}'.format(arg, CATEGORIES)
    response = requests.get(triviaUrl)
    triviaData = json.loads(response.text)
    for i in range(int(arg)):
        question = triviaData[i]['question']
        answer = triviaData[i]['answer']
        category = triviaData[i]['category']
        embed = discord.Embed(
            title='Intrebare:',
            description='''**{}**
            Categorie: {}
            Scrie **skip** pentru a trece la urmatoarea intrebare!
            Scrie **stop** pentru a incheia trivia!
            **{}/{}**'''.format(question, category, i, arg),
            url='https://api.gazatu.xyz/trivia/questions',
            timestamp=datetime.now(),
            color=0xFFFFFF
        )
        await ctx.send(embed=embed)
        thing = 0
        for i in range(1, 6):
            try:
                msg = await bot.wait_for('message', timeout = 40.0)
            except asyncio.TimeoutError:
                await ctx.send('Nu a raspuns corect nimeni, raspunsul era {}'.format(answer))
                thing = 1
                break
            guess = msg.content.lower()
            if str(guess) == 'stop':
                return await ctx.send('Am incheiat trivia!')
            if str(guess) == 'skip':
                await ctx.send('LOW IQ SKIP')
                break
            if str(guess) == str(answer.lower()):
                await ctx.send('{} a raspuns corect!'.format(msg.author))
                thing = 1
                break
            else:
                await ctx.send('Raspuns gresit! {}/5 greseli.'.format(i))
        if thing == 0:
            await ctx.send('Nu a raspuns corect nimeni, raspunsul era {}'.format(answer))

@bot.command()
async def b(ctx):
    await ctx.send(file=discord.File('C:\\Users\\ADY\\Desktop\\bot\\bani.jpg'))

@bot.command()
async def p(ctx):
    await ctx.send(file=discord.File('C:\\Users\\ADY\\Desktop\\bot\\peste.jpg'))

@bot.command()
async def z(ctx):
    await ctx.send('https://freerobuxgeneratorworking2012.download/​‌‌‌​​​‌​‌​​‌​‌​​‌‌​‌​‌​​‌​​‌​​‌​​‌‌​‌‌‌​‌​​‌‌‌‌​‌‌​‌​‌‌​‌‌​‌‌​‌')

@bot.command()
async def weeb(ctx):
    n = random.randint(1, 3)
    f = 'C:\\Users\\ADY\\Desktop\\bot\\weeb{}.png'.format(n)
    await ctx.send('Average weeb:')
    await ctx.send(file=discord.File(f))

@bot.command()
async def ru(ctx):
    await ctx.send(file=discord.File('C:\\Users\\ADY\\Desktop\\bot\\ru.png'))

@bot.command()
async def ajutor(ctx):
    await ctx.send('''Comenzile lui Pula Marian:
    .ajutor - afiseaza acest text
    .b - bani
    .cauta [TEXT] - cauta TEXT online
    .ghici - joaca ghiceste numarul
    .marian - afiseaza o poza cu Pula Marian
    .p - peste
    .paca [N] - joaca pacanele pe suma N pariata
    .pula - afiseaza un fapt interesant despre Pula Marian
    .rand [@USER] - afiseaza un mesaj random de la [@USER]
    .ru - afiseaza un fapt interesant despre rubla ruseasca
    .spam [TEXT] [N] - repeta TEXT de N ori
    .sterge [N] - sterge N mesaje
    .trad [LIMBA] [TEXT] - traduce [TEXT] in [LIMBA] dorita
    .trivia [N] - joaca trivia cu [N] intrebari
    .urban [TEXT] - cauta [TEXT] pe urbandictionary.com
    .vot [TEXT] - initiaza un vot cu subiect TEXT
    .vreme [ORAS] - afiseaza vremea din [ORAS]
    .weeb - afiseaza un fapt curios despre Luca/weebs
    .wiki [LIMBA] [TEXT] - cauta TEXT in LIMBA dorita pe wikipedia.org
    .wordle - joaca wordle cu buguri
    .z - VI VON

    MUZICA:
    .re [URL] [VOICE CHANNEL] reda muzica de pe [URL] pe [VOICE CHANNEL]
    .pa - paraseste voice channel
    .st - pune stop melodiei
    .co - continue melodia
    .op - opreste pe Pula Marian
    ''')

bot.run(TOKEN)