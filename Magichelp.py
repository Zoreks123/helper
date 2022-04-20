1# meta developer: @zxc_dfr3ddy

import logging 
import inspect 
 
from telethon.tl.functions.channels import JoinChannelRequest 
 
from .. import loader, utils, main, security 
 
logger = logging.getLogger(__name__) 
 
 
@loader.tds 
class HelpMod(loader.Module): 
    """Help""" 
    strings = {"name": "Dfr3ddyHelp", 
               "bad_module": '<b>Модуля</b> "<code>{}</code>" <b>нету! Очень жаль :( </b>', 
               "single_mod_header": "<b>Информация о </b> <u>{}</u>:\n", 
               "single_cmd": "\n👉 {}\n", 
               "undoc_cmd": "...", 
               "all_header": 'У вас  <code>{}</code> модулей [@zxc_dfr3ddy]:\n\n', 
               "mod_tmpl": '\n [🇩🇪]<code>{}</code>', 
               "first_cmd_tmpl": " 👉 [ {}", 
               "cmd_tmpl": " | {}",} 
 
    @loader.unrestricted 
    async def helpcmd(self, message): 
        """.help [модуль] creator [@zxc_dfr3ddy]""" 
        args = utils.get_args_raw(message) 
        if args: 
            module = None 
            for mod in self.allmodules.modules: 
                if mod.strings("name", message).lower() == args.lower(): 
                    module = mod 
            if module is None: 
                await utils.answer(message, self.strings("bad_module", message).format(args)) 
                return 
            try: 
                name = module.strings("name", message) 
            except KeyError: 
                name = getattr(module, "name", "ERROR") 
            reply = self.strings("single_mod_header", message).format(utils.escape_html(name), 
                                                                      utils.escape_html((self.db.get(main.__name__, 
                                                                                                     "command_prefix", 
                                                                                                     False) or ".")[0])) 
            if module.__doc__: 
                reply += "\n"+"\n".join("  " + t for t in utils.escape_html(inspect.getdoc(module)).split("\n")) 
            else: 
                logger.warning("Module %s is missing docstring!", module) 
            commands = {name: func for name, func in module.commands.items() 
                        if await self.allmodules.check_security(message, func)} 
            for name, fun in commands.items(): 
                reply += self.strings("single_cmd", message).format(name) 
                if fun.__doc__: 
                    reply += utils.escape_html("\n".join("  " + t for t in inspect.getdoc(fun).split("\n"))) 
                else: 
                    reply += self.strings("undoc_cmd", message) 
        else: 
            count = 0 
            for i in self.allmodules.modules: 
                if len(i.commands) != 0: 
                    count += 1 
            reply = self.strings("all_header", message).format(count) 
             
            for mod in self.allmodules.modules: 
                if len(mod.commands) != 0: 
                    try: 
                        name = mod.strings("name", message) 
                    except KeyError: 
                        name = getattr(mod, "name", "ERROR") 
                    reply += self.strings("mod_tmpl", message).format(name) 
                    first = True 
                    commands = [name for name, func in mod.commands.items() 
                                if await self.allmodules.check_security(message, func)] 
                    for cmd in commands: 
                        if first: 
                            reply += self.strings("first_cmd_tmpl", message).format(cmd) 
                            first = False 
                        else: 
                            reply += self.strings("cmd_tmpl", message).format(cmd) 
                    reply += " ]" 
        await utils.answer(message, reply) 
         
    async def client_ready(self, client, db): 
        self.client = client 
        self.is_bot = await client.is_bot() 
        self.db = db
     async def supportcmd(self, message):
    await message.edit("<b> Support as : @FoxDfr3ddy </b>

