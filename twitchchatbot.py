from twitchio.ext import commands
import time


class Bot(commands.Bot):

    def __init__(self):  #YOU HAVE TO USE OAUTH TOKEN FROM TWITCH TO USE THE API!!!
        super().__init__(token="", prefix='!', initial_channels=[''])
        self.cd = Cooldown()

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        if message.echo:
            return
        await self.handle_commands(message) #Checks if a prefixed command is invoked. If not...

        contents = message.content.upper() #Stores each message from chat.
        await self.chat_trigger_text('HELLO', 'Hello there!', contents, message)

    #Messages from chat will trigger user-defined events when called in event_message function.
    async def chat_trigger_text(self, trigger, message, contents, ctx):
        if not self.cd.check():                         #Checks if cooldown is up
            if trigger in contents:                     #Check if trigger word is in the message
                    await ctx.channel.send(message)     #Send user defined chat message
                    self.cd.reset()                     #Reset cooldown

    #Commands that utilize the prefix from the super().__init__ of the bot.
    @commands.command()
    async def test(self, ctx: commands.Context): #The name of the function is called after prefix chr.
        await ctx.send(f'TESTING...')            #Instructions you wish to send the bot.


#MY CLASSES
class Cooldown():

    def __init__(cls):
        cls.defaultcooldown = 8  #<------ Change this to whatever you want the global cooldown in seconds.
        cls.timer = time.time()
        cls.checkcooldown = cls.defaultcooldown
        cls.result = False

    def check(self) -> False:
        self.checkcooldown = time.time() - self.timer
        if self.checkcooldown >= self.defaultcooldown:
            self.result = False
        else:
            self.result = True
        return self.result

    def reset(self):
        self.timer = time.time()
        self.checkcooldown = 0


# bot.run() is blocking and will stop execution of any below code here until stopped or closed.
if __name__ == "__main__":

    bot = Bot()
    bot.run()
