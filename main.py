import discord
from discord.ext import commands
from config import token
from logic import Pokemon
import random
from logic import Wizard
from logic import Fighter   # Botun tokenini config.py dosyasından içe aktarma

intents = discord.Intents.default()  # Botun niyetlerini belirlemek için bir intents nesnesi oluşturma
intents.members = True  # Botun kullanıcılarla çalışmasına ve onları banlamasına izin veren bayrağı ayarlama
intents.message_content = True  # Botun mesajların içeriğiyle çalışmasına izin veren bayrağın ayarlanması

bot = commands.Bot(command_prefix='!', intents=intents)  # "!" komut önekiyle bir bot örneği oluşturun ve intents nesnesini ona aktarın

@bot.event  # Bot başarıyla başlatıldığında tetiklenecek olayı tanımlama
async def on_ready():
    print(f'Giriş yapıldı:  {bot.user.name}')  # Discord'da başarılı oturum açma hakkında konsolda bir mesaj görüntüleyin

@bot.command()  # Kullanıcı "!start" girdiğinde çağrılacak "start" komutunu tanımlayın
async def start(ctx):
    await ctx.send("Merhaba! Ben bir sohbet yöneticisi botuyum!")  # Sohbet odasına geri mesaj gönderme

@bot.command()  # Kullanıcının banlanma haklarına sahip olmasını gerektiren "ban" komutunun tanımlanması
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None):
    if member:  # Komutun banlanması gereken kullanıcıyı belirtip belirtmediğinin kontrol edilmesi
        if ctx.author.top_role <= member.top_role:
            await ctx.send("Eşit veya daha yüksek rütbeli bir kullanıcıyı yasaklamak mümkün değildir!")
        else:
            await ctx.guild.ban(member)  # Bir kullanıcıyı sunucudan banlama
            await ctx.send(f" Kullanıcı {member.name} banlandı.")  # Başarılı bir banlama hakkında mesaj gönderme
    else:
        await ctx.send("Bu komut banlamak istediğiniz kullanıcıyı işaret etmelidir. Örneğin: `!ban @user`")

@ban.error  # "ban" komutu için bir hata işleyicisi tanımlayın
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Bu komutu çalıştırmak için yeterli izniniz yok.")  # Kullanıcıyı erişim hakları hatası hakkında bilgilendiren bir mesaj gönderme
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Kullanıcı bulunamadı.")  # Belirtilen kullanıcı bulunamazsa bir hata mesajı gönderme

bot.run(token)  # Kimlik doğrulama için token kullanarak botu başlatma


print("Hello Umut Hocam:)")
print("Hello İhsan")
# Bot için niyetleri (intents) ayarlama
intents = discord.Intents.default()  # Varsayılan ayarların alınması
intents.messages = True              # Botun mesajları işlemesine izin verme
intents.message_content = True       # Botun mesaj içeriğini okumasına izin verme
intents.guilds = True                # Botun sunucularla (loncalar) çalışmasına izin verme

# Tanımlanmış bir komut önekine ve etkinleştirilmiş amaçlara sahip bir bot oluşturma
bot = commands.Bot(command_prefix='!', intents=intents)

# Bot çalışmaya hazır olduğunda tetiklenen bir olay
@bot.event
async def on_ready():
    print(f'Giriş yapıldı:  {bot.user.name}')  # Botun adını konsola çıktı olarak verir

# '!go' komutu
@bot.command()
async def go(ctx):
    author = ctx.author.name  # Mesaj yazarının adını alma
    # Kullanıcının zaten bir Pokémon'u olup olmadığını kontrol edin. Eğer yoksa, o zaman...
    if author not in Pokemon.pokemons.keys():
        chance = random.randint(1, 3)
        if chance == 1:
            pokemon = Pokemon(author)
        elif chance == 2:
            pokemon = Wizard(author)
        elif chance == 3:
            pokemon = Fighter(author)
        pokemon = Pokemon(author)  # Yeni bir Pokémon oluşturma
        await ctx.send(await pokemon.info())  # Pokémon hakkında bilgi gönderilmesi
        image_url = await pokemon.show_img()  # Pokémon resminin URL'sini alma
        if image_url:
            embed = discord.Embed()  # Gömülü mesajı oluşturma
            embed.set_image(url=image_url)  # Pokémon'un görüntüsünün ayarlanması
            await ctx.send(embed=embed)  # Görüntü içeren gömülü bir mesaj gönderme
        else:
            await ctx.send("Pokémonun görüntüsü yüklenemedi!")
    else:
        await ctx.send("Zaten kendi Pokémonunuzu oluşturdunuz!")  # Bir Pokémon'un daha önce yaratılıp yaratılmadığını gösteren bir mesaj
# Botun çalıştırılması


@bot.command()
async def attack(ctx):
    target = ctx.message.mentions[0] if ctx.message.mentions else None
    if target:
        if target.name in Pokemon.pokemons and ctx.author.name in Pokemon.pokemons:
            enemy = Pokemon.pokemons[target.name]
            attacker = Pokemon.pokemons[ctx.author.name]
            result = await attacker.attack(enemy)
            await ctx.send(result)
        else:
            await ctx.send("Savaşmak için her iki katılımcının da Pokemon'a sahip olması gerekir!")
    else:
        await ctx.send("Saldırmak istediğiniz kullanıcıyı etiketleyerek belirtin.")


bot.run(token)

