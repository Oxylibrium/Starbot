import plugin
import command
import message
import main
import time
from libs import readableTime

import os
import platform
import psutil
import sys

from libs import readableTime
import git

def detectDuplicateCommands():
    duplicates = []
    commandsL = []
    for plugin in main.plugins:
        for command in plugin.commands:
            commandsL.append(command.name)

    for command in commandsL:
        commandOccurances = 0
        for command2 in commandsL:
            if command == command2:
                commandOccurances += 1
        if commandOccurances > 1:
            duplicates.append(command)

    return list(set(duplicates))

def onInit(plugin_in):
    plugins_command    = command.command(plugin_in, 'plugins',    shortdesc='Print a list of plugins')
    commands_command   = command.command(plugin_in, 'commands',   shortdesc='Print a list of commands')
    help_command       = command.command(plugin_in, 'help',       shortdesc='Redirects to !commands')
    info_command       = command.command(plugin_in, 'info',       shortdesc='Print some basic bot info')
    plugintree_command = command.command(plugin_in, 'plugintree', shortdesc='Print a tree of plugins and commands')
    uptime_command     = command.command(plugin_in, 'uptime',     shortdesc='Print the bot\'s uptime')
    hostinfo_command   = command.command(plugin_in, 'hostinfo',   shortdesc='Prints information about the bots home')
    return plugin.plugin(plugin_in, 'botutils', [plugins_command, commands_command, help_command, info_command, plugintree_command, uptime_command, hostinfo_command])

def onCommand(message_in):
    if message_in.command == 'plugins':
        pluginList = []
        for plugin in main.plugins:
            pluginList.append(plugin.name)
        return message.create(body='```{}```'.format(', '.join(pluginList)))

    if message_in.command == 'commands' or message_in.command == 'help':
        commandNames = []
        commandDescs = []
        for command in main.commands:
            commandNames.append(command.name)
            commandDescs.append(command.shortdesc)
        commandList = []
        padLength = len(max(commandNames, key=len))
        for i in range(len(commandNames)):
            commandList.append('{} - {}'.format(commandNames[i].ljust(padLength), commandDescs[i]))
        return message.create(body='```{}```'.format('\n'.join(commandList)))

    if message_in.command == 'info':
        repo = git.Repo(search_parent_directories=True)
        sha = repo.head.object.hexsha
        return message.create(body='```Project StarBot v0.0.1-{}\nDeveloped by CorpNewt and Sydney Erickson```'.format(sha[:7]))

    if message_in.command == 'plugintree':
        dups = detectDuplicateCommands()
        pluginString = '```\n'
        for plugin in main.plugins:
            pluginString += '{}\n'.format(plugin.name)
            commandsInPlugin = len(plugin.commands)
            currentCommand = 0
            for command in plugin.commands:
                currentCommand += 1
                if commandsInPlugin != currentCommand:
                    if command.name in dups:
                        pluginString += '├ {} <-- duplicate\n'.format(command.name)
                    else:
                        pluginString += '├ {}\n'.format(command.name)
                else:
                    if command.name in dups:
                        pluginString += '└ {} <-- duplicate\n'.format(command.name)
                    else:
                        pluginString += '└ {}\n'.format(command.name)
        pluginString += '```'
        return message.create(body=pluginString)

    if message_in.command == 'uptime':
        currentTime = int(time.time())
        timeString = readableTime.getReadableTimeBetween(main.startTime, currentTime)
        return message.create(body='I\'ve been up for *{}*.'.format(timeString))

    if message_in.command == 'hostinfo':
        cpuThred = os.cpu_count()
        cpuUsage = psutil.cpu_percent(interval=1)
        memStats = psutil.virtual_memory()
        memPerc = memStats.percent
        memUsed = memStats.used
        memTotal = memStats.total
        memUsedGB = "{0:.1f}".format(((memUsed / 1024) / 1024) / 1024)
        memTotalGB = "{0:.1f}".format(((memTotal / 1024) / 1024) / 1024)
        currentOS = platform.platform()
        system = platform.system()
        release = platform.release()
        version = platform.version()
        processor = platform.processor()
        currentTime = int(time.time())
        timeString = readableTime.getReadableTimeBetween(main.startTime, currentTime)
        pythonMajor = sys.version_info.major
        pythonMinor = sys.version_info.minor
        pythonMicro = sys.version_info.micro
        pythonRelease = sys.version_info.releaselevel

        msg = '***{}\'s*** **Home:**\n'.format('StarBot')
        msg += '```Host OS       : {}\n'.format(currentOS)
        msg += 'Host Python   : {}.{}.{} {}\n'.format(pythonMajor, pythonMinor, pythonMicro, pythonRelease)
        if cpuThred > 1:
            msg += 'Host CPU usage: {}% of {} ({} threads)\n'.format(cpuUsage, processor, cpuThred)
        else:
            msg += 'Host CPU usage: {}% of {} ({} thread)\n'.format(cpuUsage, processor, cpuThred)
        msg += 'Host RAM      : {}GB ({}%) of {}GB\n'.format(memUsedGB, memPerc, memTotalGB)
        msg += 'Hostname      : {}\n'.format(platform.node())
        msg += 'Host uptime   : {}```'.format(readableTime.getReadableTimeBetween(psutil.boot_time(), time.time()))

        return message.create(body=msg)