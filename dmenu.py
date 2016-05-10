import os
from os.path import expanduser, isdir, join, pathsep
from plumbum.cmd import dmenu
import logging
from recent_runner import RecentRunner


def dmenu_show(title, items):
    from themes import dmenu_defaults
    import shlex
    dmenu_defaults = shlex.split(dmenu_defaults)
    logging.info("DMENU: %s", dmenu_defaults)
    try:
        return (dmenu[
            "-i", "-p", "[%s] >>> " % title
            ] << "\n".join(items))(*dmenu_defaults).strip()
    except Exception as e:
        logging.exception("error running dmenu")


def list_windows(qtile, current_group=False):

    def title_format(x):
        return "[%s] %s" % (
            x.group.name if x.group else '',
            x.name)

    if current_group:
        window_titles = [
            w.name for w in qtile.groupMap[qtile.currentGroup.name].windows
            if w.name != "<no name>"
        ]
    else:
        window_titles = [
            title_format(w) for w in qtile.windowMap.values() if w.name != "<no name>"
        ]
    logging.info(window_titles)

    def process_selected(selected):
        if not current_group:
            group, selected = selected.split(']', 1)
        selected = selected.strip()
        logging.info("Switch to: %s", selected)
        for window in qtile.windowMap.values():
            try:
                #logging.debug("window %s : %s", repr(window.name), repr(selected))
                if window.group and str(window.name) == str(selected):
                    #window.cmd_to_screen(qtile.currentScreen.index)
                    #qtile.cmd_to_screen(window.
                    logging.debug("raise %s:", window.group.screen)
                    if window.group.screen:
                        qtile.cmd_to_screen(window.group.screen.index)
                    else:
                        window.group.cmd_toscreen()
                    floating = window.floating
                    window.cmd_bring_to_front()
                    if not floating:
                        window.cmd_disable_floating()
                    #qtile.currentScreen.cmd_togglegroup(window.group.name)
                    return True
            except Exception as e:
                logging.exception("error in group")
        return True

    process_selected(dmenu_show(
        qtile.currentGroup.name if current_group else "*",
        window_titles,
    ))


def list_windows_group(qtile):
    return list_windows(qtile, current_group=True)


def list_executables():
    paths = os.environ["PATH"].split(pathsep)
    executables = []
    for path in filter(isdir, paths):
        for file_ in os.listdir(path):
            if os.access(join(path, file_), os.X_OK):
                executables.append(file_)
    return set(executables)


def dmenu_run(qtile):
    recent_runner = RecentRunner()
    selected = dmenu_show("Run", recent_runner.list(list_executables()))
    print(selected)
    if not selected:
        return
    logging.debug((dir(qtile)))
    qtile.cmd_spawn(selected)
    recent_runner.insert(selected)
