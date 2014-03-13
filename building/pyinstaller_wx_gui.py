#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
wxPython interface for PyInstaller

TODO
----
1. DropTarget for ComboCtrls; Adds Paths to History.
2. Validate all history paths.
3. Build all history paths.
4. Pickle save the PyInstaller Paths and History Paths.

License And Version
===================

pyinstaller-wx-gui is distributed under the wxPython license.

Author: Edward Greig @ 3 May 2013

Latest Revision: Edward Greig @ 22 Feb 2014
Version: 2.1.0-rev1

"""

import os
import sys
import subprocess

import wx
import wx.lib.filebrowsebutton as filebrowse
from wx.lib.embeddedimage import PyEmbeddedImage

pyinstaller_console16 = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwY"
    "AAAABGdBTUEAALGOfPtRkwAAACBjSFJNAAB6JQAAgIMAAPn/AACA6QAAdTAAAOpgAAA6mAAA"
    "F2+SX8VGAAABmklEQVR42mL8//8/g6CgwH9GRiYGDw8PBmLAzp07GN6+fccIYgMEEAMzM9N/"
    "fn4+MI6MjPyPDmBiyLS4uNh/MTExEJcBIIBYeHh4GP7+/Qs0iBls4NevXzFshInB6C9fvjBw"
    "c/MAMfd/gABi+fnzJwMHBwdc8uPHjwyMjIwMINNhACSGTLOzszP8/v0LrA4ggBhB/gcJglzh"
    "7e1DVBhs2LAeohkYbgABxADyT2BgIMgQkjBIDy8v73+AAGKUkBD//+LFS4YpizsYSAE5sRUM"
    "nJwcDAABxMLFxQUX3LZuD1GavYJcwDRIL0AAsSAHFliwgYdBgkGcgQsKhYGQG0ivaVjDkNaQ"
    "xjCrYRZcLSjmAAKIhZOTkyhbYxtiwXQDiIC6FBR7AAEEjMZfGIrvNdzFa1gDlAa5HiCAWJiY"
    "GDEUKDUoY3iBEwpBXjgFCoP1exjY2NgYAAKIBRSfyOBbwxeGewxfsNoMCgNUwMgAEEBAFzAR"
    "FYgg29EByG6AAGJhZWUlOQxg4M+fPwwAAcTy6dNnksMABn79+sUAEGAAxCqqx8Y+ijoAAAAA"
    "SUVORK5CYII=")

pyinstaller_console48 = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAACXBIWXMAAAsTAAALEwEAmpwY"
    "AAAABGdBTUEAALGOfPtRkwAAACBjSFJNAAB6JQAAgIMAAPn/AACA6QAAdTAAAOpgAAA6mAAA"
    "F2+SX8VGAAAHVklEQVR42sSOKRLAMAzEdku645f5z82XUmzgsXvg8AgJCIjdDTNr6QRJfFTV"
    "6wfcHTsY44IkRAQy8/+a8+aqfQQQCx8f338Ghv9ghWxsbAx///5lYGVlBdPYwLJly0hyTFRU"
    "FFY9+MR5eHgYQAHLzMzMwM7OzvD161cGUVGR/69fv8HwBEAAMTExMYIdC2SAFYJCH6T558+f"
    "DAMFQIEJcsOvX7/AfGAKAQcuDw/3f3S1AAHEBCK4ubnBHgCFPEgTSDNIw0ABUNIBuQHkLpBn"
    "vnz5AuaDYoOLixPFEwABBPYASBKkCeR4kG9BfBAeKABK/6CUAMmLjOCkBGKzsLCC5YSEBOGO"
    "AwggJpDvQJKg0AcpBDkclKQG0gOwQAW56/v372C3QZwDCWgWFhZg7HCBRQACiAWUYUBpH0TD"
    "Mi6IBnkGGwCpJRXg0oNL/Nev38Ck8xteqIACmZubB+x4WAYHxQQwif0HCCAWEAckCAKcnJzw"
    "GGBiwu6Bjx8/wotb9BDDBUB6SBFnZmYC2sEKLkhADv327RswNv6CPQSKFWR1AAHEBCrvYTkf"
    "BECaQJkFFF0DBUAhDk4ewKQCCixQvgS5CxZjoMACeQqUvAACiAVSB/wFK4YlH+QibCAAyC3/"
    "/v2HZ2KQW0ChD8kL/xl+//4NFgfFDkAAMYEYIAmQ70AY5FuQGKhYHSgACtn//yGO//z5M0rd"
    "BHIjyG2gVPLjx08GgABiAmUMkEJQPgB5BMQHAZAvBwrAMioomYACFBbyoFiABTDIfSBPAAQQ"
    "o6CgwH/kNhDIA6DMDEpK3t4+A+KB3bt3gfMByLGwGAG5EZRPYWKQ2pqBASAAjeWuBFAEQ0EK"
    "Sv7/N9PcymtzZzVkxsTBOlLnHMfah6vxUyPWlUgmUtgrY/hz47oDfXL5HKz3lvN0jbV2YkEu"
    "UPjfXH1rfRkjTKHo8UDlH8Hks1ajRUS5AhBVbykAgCAQRaH979k4xa2vmGxsFB8L4JQwZIKd"
    "1ni94A3cHcdNrZYfQb/s5vDYfH53yrzGq1wFhEM8n2yN4xKZ2BIHK62C3gIwWQcpAIQwDEVh"
    "ds79D6wP/EVBBLUm0mjzufVxpEO8AtYv9GZCoztA4jwo85nALLBYHRCCWRNHJFOjtbX+KWrp"
    "/MXCCYeyfe3/7NkCMF3HOgCDIBBAO3Rvwv9/aK0d6oMQOzgYg94dh+iy0JV/gfaaxa6BiMhD"
    "MN/9YTetLqQ536XMmVlAgkoGMMAShYUQgsNe9fqtuWzWrXJnzL9RwoEcQcQ5u+08xnN8AohB"
    "XFzsv4SEOBxLSUn+X7du3f/BBEDuAbkLlF+Bgf1fQID/Pzs7239eXt7/AAHECHI0yEegfAAK"
    "QSkpKYbLl68wTF3SyTBYQHZMOYOurg7D8+fP4c0LWLIDCCAWUBSBogckCPLAQPYD8AGQu2Cl"
    "JKxpzc7OwQAQQCygtAdLUwPdkSHkAVBeAeUtkON//foJLoYBAogJVlTC8EB2JfEBkLtAqQUS"
    "E4xAmh1MAwQQC6iEgBWdoKiBlTToYNu6PXR1sFeQCwof5C5Q/QEKcFitDIoBgABiAoU6KA+A"
    "aFAewOWBgQbodQIoRkClLUAAscDKVZAgqHWHrbOCDLgaeBgkGMQxxaEQHQgDITcW8TUNa1D4"
    "aQ1pYHpWwyys9oLcBQpgWLMfVuEBBBATrNMASkYsLMzwJgI9AczxhIZaIP2Ef9A+MTfYzQAB"
    "xAJKPiAO8mgAPUBsQywDJxASC0DugrWFYBkaVBMDBBALzNEgj8CaAAMJGmAMaKFxCpqZQe6C"
    "JXVYJgbxAQKICVY5wEYlODg4B2UmBrkLlGQgQ6Ds0GY7EwNAADHBmrightxgrcRgANJ65QQ3"
    "zWHNf4AAYgGlI3jTFFypMZJk6L2Gu7RNSvBBXEZ4CQTrg4AwQACxcHFxwiVg6YsUoNSgTBNP"
    "nEKryEDuAtUFyB0eUBICCCAWWDUNa+GR6gGYJ0itBzihEB3gqwdgg26gAAe1REH5ASCAmEDV"
    "McjxsLGWwQxg/WHYKAoIAAQQE8jNsCoa16TGYAGw4hMWG6CABwggcJ8YNi46GEal8Y1WwwZ7"
    "YRkZBAACiAU52cAyMz7wreELwz2GL3RrQqB7AlKMwvrljAwAAcQCy7yg8dGfP3/QbUQO1JQg"
    "tQ6ABTasFgZxAQIIHOSg0QKQz2DjM/RojZIKYO6CDTeCaBAACCAm8PAc0CsggYEckSY2CcG6"
    "v7B+C0AAMcE4oEwB8gCumZmBBjD3wSozWIwABBDT79+/wGkKNgI3WOsCWCsBlkpg/RaAAGKB"
    "ta9hnQVS+wO0agvh6g/AxrBAFRko2QMEENO3b9+hjThm+Pwsqc0IeqV/mEdgY6OgWRyAAGKB"
    "CYJSDrkdenq0hZC7laDkDpkaZmEACCAmdnY2+Lg7bEh7MAKQu2CdL1CSh8xp/GMACCAWWOsO"
    "FhPE1MYDAUDuQk7ekP7APwaAAGIBDaUwM/9mgMm9evVqUHoA5C7YfB4Iv3//HpykAAIMALsD"
    "lyXvrhjcAAAAAElFTkSuQmCC")

overlay_dlines1 = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAAEUAAABFCAYAAAAcjSspAAAACXBIWXMAAAsTAAALEwEAmpwY"
    "AAAABGdBTUEAALGOfPtRkwAAACBjSFJNAAB6JQAAgIMAAPn/AACA6QAAdTAAAOpgAAA6mAAA"
    "F2+SX8VGAAACBklEQVR42mJgYGBw+P//PwMIj7IhbIAAYhgNBEw2QACNBgIWNkAAjQYCFjZA"
    "AI1mHyxsgAAaDQQsbIAAGg0ELGyAABrNPljYAAE0GghY2AABNBoIWNgAATSafbCwAQJoNBCw"
    "sAECaDQQsLABAmg0+2BhAwTQaCBgYQME0GggYGEDBNBo9sHCBgig0UDAwgYIoNFAwMIGCKDR"
    "7IOFDRBAo4GAhQ0QQKOBgIUNEECj2QcLGyCARgMBCxsggEYDAQsbIIBGsw8WNkAAjQYCFjZA"
    "AI0GAhY2QACNZh8sbIAAop9FCEAWm56BAxBAQyJAYGx6pRaAAGKgV8gPmQABsgECaDT7YGED"
    "BNBo9sHCBgig0eyDhQ0QQKPZBwsbIIBGsw8WNkAAjWYfLGyAABrNPljYAAE0mn2wsAECaDT7"
    "YGEDBNBo9sHCBgig0eyDhQ0QQKPZBwsbIIBGsw8WNkAAjWYfLGyAABodecPCBgig0UDAwgYI"
    "oNFAwMIGCKDR7IOFDRBAo4GAhQ0QQKOBgIUNEECj2QcLGyCARgMBCxsggEYDAQsbIIBGsw8W"
    "NkAAjQYCFjZAAI0GAhY2QACNZh8sbIAAGg0ELGyAABoNBCxsgAAazT5Y2AABNBoIWNgAATQa"
    "CFjYAAE0mn2wsAECaDQQsLABAmg0ELCwAQJoNPtgYQME0GggYGEDBBgA0Qda7gFwD6oAAAAA"
    "SUVORK5CYII=")



# Define a translation function.
_ = wx.GetTranslation


try:
    gAppDir = os.path.dirname(os.path.abspath(__file__))
except Exception as exc:
    gAppDir = os.path.dirname(os.path.abspath(sys.argv[0]))


class PyInstallerBuilderPanel(wx.Panel):
    """
    A wxPython Panel GUI to specify PyInstaller Specs before building.
    """
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.TAB_TRAVERSAL | wx.NO_BORDER,
                 name='gradientoverlaypanel',
                 gradientDirection=wx.NORTH,
                 color1='#666666', color2='#FFFFFF', overlayPngBmp=None):
        """Default class constructor."""
        wx.Panel.__init__(self, parent, id, pos, size, style, name)

        self._isInitialized = False
        self.color1 = color1
        self.color2 = color2
        self.overlayPngBmp = overlayPngBmp or overlay_dlines1.GetBitmap()
        self.gradientDirection = gradientDirection

    def Initialize(self):
        """
        Create everything that goes in the pane.
        """
        # self.SetDoubleBuffered(True)
        if wx.VERSION_STRING.startswith('2.8.'):
            self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        else:
            self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer1 = wx.BoxSizer(wx.VERTICAL)
        hsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer3 = wx.BoxSizer(wx.HORIZONTAL)

        self.iconpath = None
        self.icon = wx.BitmapButton(self, wx.ID_ANY, pyinstaller_console48.GetBitmap())
        self.icon.SetToolTip(wx.ToolTip(u''))
        self.icon.Bind(wx.EVT_BUTTON, self.OnSetIcon)

        self.getPyInstallerPathButton = filebrowse.FileBrowseButtonWithHistory(self,
            wx.ID_ANY, labelText=_(u'pyinstaller.py Path ...'),
            dialogTitle=_(u'Locate pyinstaller.py...'),
            fileMask=_(u'Python source (*.py;*.pyc;*.pyw)|*.py;*.pyc;*.pyw'),
            changeCallback=self.getPyInstallerPathButtonCallback,
            style=wx.BORDER_SIMPLE)

        hsizer2.Add(self.getPyInstallerPathButton, 1, wx.ALIGN_CENTRE_VERTICAL | wx.EXPAND | wx.ALL, 3)
        if os.path.exists(gAppDir + os.sep + 'pyinstaller.py'):
            self.getPyInstallerPathButton.SetValue(
                '%s' % (gAppDir + os.sep + 'pyinstaller.py'))

        self.getFileButton = filebrowse.FileBrowseButtonWithHistory(self,
            wx.ID_ANY, labelText=_(u'Script to bundle ...'),
            dialogTitle=_(u'Locate Script...'),
            fileMask=_(u'Python source (*.py;*.pyc;*.pyw)|*.py;*.pyc;*.pyw'),
            changeCallback=self.getFileButtonCallback,
            style=wx.BORDER_SIMPLE)
        self.getFileButton.GetHistoryControl().Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self.getFileButton.SetDoubleBuffered(True)
        hsizer3.Add(self.getFileButton, 1, wx.ALIGN_CENTRE_VERTICAL | wx.EXPAND | wx.ALL, 3)

        vsizer1.Add(hsizer2, 1, wx.EXPAND | wx.ALL, 3)
        vsizer1.Add(hsizer3, 1, wx.EXPAND | wx.ALL, 3)
        hsizer1.Add(self.icon, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 3)
        hsizer1.Add(vsizer1, 1, wx.EXPAND | wx.ALL, 2)
        vsizer.Add(hsizer1, 0, wx.EXPAND | wx.ALL, 2)

        hsizerName = wx.BoxSizer(wx.HORIZONTAL)
        self.nameCB = wx.CheckBox(self, wx.ID_ANY, _(u'Name'))
        self.nameTextCtrl = wx.TextCtrl(self, wx.ID_ANY, u'')
        hsizerName.Add(self.nameCB, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 2)
        hsizerName.Add(self.nameTextCtrl, 1, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 2)
        vsizer.Add(hsizerName, 0, wx.EXPAND | wx.ALL, 5)

        b = 8
        self.filetypeCB = wx.CheckBox(self, wx.ID_ANY, _(u'One Executable File Package'))
        self.filetypeCB.SetToolTip(wx.ToolTip(_(u'Check if you want to create a single file deployment. (Stand-alone Executable))')))
        self.asciiCB = wx.CheckBox(self, wx.ID_ANY, _(u'Do NOT include decodings'))
        self.asciiCB.SetToolTip(wx.ToolTip(_(u'Do NOT include unicode encodings (default: included if available)')))
        self.debugCB = wx.CheckBox(self, wx.ID_ANY, _(u'Use debug versions'))
        self.debugCB.SetToolTip(wx.ToolTip(_(u'Use the debug (verbose) build of the executable for\npackaging. This will make the packaged executable be\nmore verbose when run.')))
        vsizer.Add(self.filetypeCB, 0, wx.LEFT | wx.TOP, b)
        vsizer.Add(self.asciiCB, 0, wx.LEFT | wx.TOP, b)
        vsizer.Add(self.debugCB, 0, wx.LEFT | wx.TOP, b)

        if sys.platform.startswith('win'):
            self.noconsoleCB = wx.CheckBox(self, wx.ID_ANY, _(u'No console (Windows only)'))
            vsizer.Add(self.noconsoleCB, 0, wx.LEFT | wx.TOP, b)
        else:
            self.noconsoleCB = None
        try:
            self.noconsoleCB.SetToolTip(wx.ToolTip(_(u'Use a windowed subsystem executable, which on Windows\ndoes not open the console when the program is\nlaunched. On Mac OS X it allows running gui\napplications and also creates an .app bundle. Mandatory for gui applications on Mac OS X.')))
        except AttributeError: # NoneType
            pass

        if not sys.platform.startswith('win'):
            self.stripCB = wx.CheckBox(self, wx.ID_ANY, _(u'Strip the exe and shared libs'))
            self.stripCB.SetToolTip(wx.ToolTip(_(u'Strip the exe and shared libs (don\'t try this on Windows)')))
            vsizer.Add(self.stripCB, 0, wx.LEFT | wx.TOP, b)
        else:
            self.stripCB = None

        hsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.buildButton = wx.Button(self, wx.ID_ANY, _(u'Build Exe'))
        self.buildButton.Bind(wx.EVT_BUTTON, self.OnBuildPackage)
        self.helpButton = wx.Button(self, wx.ID_ANY, _(u'Help'))
        self.helpButton.Bind(wx.EVT_BUTTON, self.OnHelp)
        hsizer2.Add(self.buildButton, 0,  wx.ALL, 6)
        hsizer2.Add(self.helpButton, 0,  wx.ALL, 6)

        vsizer.Add(hsizer2, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(vsizer)

        self.fin = ''
        self.fout = ''

        self.SetSizer(vsizer)

        self.SendSizeEvent() # Force sizer to refresh.
        self._isInitialized = True


    def OnKeyUp(self, event):
        print(event.GetKeyCode())
        comboTextCtrl = event.GetEventObject()
        value = comboTextCtrl.GetValue()
        if os.path.exists(value) and os.path.isfile(value) and value.endswith(('.py', '.pyw', '.pyc', '.pyo', '.pyd')):
            comboTextCtrl.SetBackgroundColour('#C1FFC1')
        elif not value:
            comboTextCtrl.SetBackgroundColour('#FFFFFF')
        else:
            comboTextCtrl.SetBackgroundColour('#FFC4C4')
        comboTextCtrl.SetForegroundColour('#000000')
        comboTextCtrl.Refresh()
        if event.GetKeyCode() == wx.WXK_RETURN:
            if event.GetEventObject().GetParent() == self.getPyInstallerPathButton:
                print('RETURN/ENTER getPyInstallerPathButton')
                self.getPyInstallerPathButtonCallback(
                    evtObj=event.GetEventObject().GetParent(),
                    returnPressed=True)
            elif event.GetEventObject().GetParent() == self.getFileButton:
                print('RETURN/ENTER getFileButton')
                self.getFileButtonCallback(
                    evtObj=event.GetEventObject().GetParent(),
                    returnPressed=True)
        event.Skip()

    def getPyInstallerPathButtonCallback(self, event=None, evtObj=None, returnPressed=False):
        # value = event.GetString()
        print(event)
        value = self.getPyInstallerPathButton.GetValue()
        if not value:
            return
        if not returnPressed:
            return
        if not os.path.exists(value):
            wx.MessageBox(_(u'Path Doesn\'t Exist!')
                          + '\n' + '%s' % value, _(u'ERROR'), wx.ICON_ERROR)
        print('FileBrowseButtonWithHistory: %s\n' % value)
        history = self.getPyInstallerPathButton.GetHistory()
        if value not in history:
            history.append(value)
            self.getPyInstallerPathButton.SetHistory(history)
            self.getPyInstallerPathButton.GetHistoryControl().SetStringSelection(value)

    def getFileButtonCallback(self, event=None, evtObj=None, returnPressed=False):
        # print(event)
        # value = event.GetString()
        # value = self.getFileButton.GetValue()
        if returnPressed and not event:
            value = evtObj.GetValue()
        # elif event:
            # value = event.GetString()
        else:
            return

        if not value:
            return

        if not os.path.exists(value):
            wx.MessageBox(_(u'Path Doesn\'t Exist!')
                          + '\n' + '%s' % value, _(u'ERROR'), wx.ICON_ERROR)
            return
        print('getFileButton: %s\n' % value)
        history = self.getFileButton.GetHistory()
        if value not in history:
            history.append(value)
            self.getFileButton.SetHistory(history)
            self.getFileButton.GetHistoryControl().SetStringSelection(value)

    def OnBuildPackage(self, event):
        commands = ['python',
                    '-OO',
                    self.getPyInstallerPathButton.GetValue().strip()]
                    # 'pyinstaller.py']

        if self.filetypeCB.GetValue():
            # commands.append('--onefile')
            commands.append('-F')

        try:
            if self.noconsoleCB.GetValue():
                commands.append('--noconsole')
                ## commands.append('-w')
        except AttributeError: # NoneType
            pass

        if not self.getFileButton.GetValue():
            wx.Bell()
            wx.MessageBox('No Script To Bundle', 'ERROR', wx.ICON_ERROR)
            return

        if not self.nameCB.GetValue():
            commands.append('--name')
            ## commands.append('-n')
            # Just the script name minus the ext.
            commands.append('%s' %(
                os.path.splitext(os.path.basename(self.getFileButton.GetValue()))[0])
                )
        else:
            commands.append('--name')
            ## commands.append('-n')
            commands.append('%s' %(self.nameTextCtrl.GetValue()))

        if not self.iconpath == None:
            commands.append('--icon')
            ## commands.append('-i')
            commands.append('%s' %(self.iconpath))

        if self.asciiCB.GetValue():
            commands.append('--ascii')
            ## commands.append('-a')
        if self.debugCB.GetValue():
            commands.append('--debug')
            ## commands.append('-d')
        try:
            if self.stripCB.GetValue():
                commands.append('--strip')
                ## commands.append('-s')
        except AttributeError:
            pass

        commands.append(self.getFileButton.GetValue())
        print('commands = %s' %commands)
        subprocess.Popen(commands)

        # retcode = subprocess.Popen(commands)
        # sys.exit(retcode)

    def Getpyinstaller_pyPath(self, event):
        dialog = wx.FileDialog(self, 'Locate pyinstaller.py...', os.getcwd(), '', 'Python source (*.py;*.pyc;*.pyw)|*.py;*.pyc;*.pyw')
        if (dialog.ShowModal() == wx.ID_OK):
            filename = dialog.GetFilename()
            dirname = dialog.GetDirectory()
            filepath = dialog.GetPath()
            self.ptinstallerPathTextCtrl.SetValue(filepath)
        dialog.Destroy()

    def GetFile(self, event):
        dialog = wx.FileDialog(self, 'Locate Script...', os.getcwd(), '', 'Python source (*.py;*.pyc;*.pyw)|*.py;*.pyc;*.pyw')
        if (dialog.ShowModal() == wx.ID_OK):
            filename = dialog.GetFilename()
            dirname = dialog.GetDirectory()
            filepath = dialog.GetPath()
            self.fin = filepath
            self.filein.SetValue(self.fin)
        dialog.Destroy()

    def OnSetIcon(self, event):
        dialog = wx.FileDialog(self, 'Locate Icon...', os.getcwd(), '', 'Windows Icon(*.ico)|*.ico')
        if (dialog.ShowModal() == wx.ID_OK):
            filepath = dialog.GetPath()
            self.icon.SetBitmap(wx.Bitmap(filepath))
            self.icon.SetToolTip(wx.ToolTip(filepath))
            self.iconpath = filepath
        dialog.Destroy()
        self.SendSizeEvent()
        # wx.CallAfter(self.Fit)
        if __name__ == '__main__':
            frameSz = gMainWin.GetSize()
            gMainWin.SetSizerAndFit(gMainWin.vbSizer)
            gMainWin.SetSize((frameSz[0], gMainWin.GetSize()[1])) # Maintain the width

    def OnEraseBackground(self, event):
        pass # Reduce flicker trick with buffered paint.

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        x, y = 0, 0
        w, h = self.GetSize()

        dc.GradientFillLinear(rect=(x, y, w, h), 
                              initialColour=self.color1, 
                              destColour=self.color2, 
                              nDirection=self.gradientDirection)

        sz = self.GetClientSize()
        if self.overlayPngBmp:
            w = self.overlayPngBmp.GetWidth()
            h = self.overlayPngBmp.GetHeight()
            for x in range(0, sz.width, w):
                for y in range(0, sz.height, h):
                    dc.DrawBitmap(self.overlayPngBmp, x, y, True)

    def OnHelp(self, event):
        # Add the help from the version we are building for,
        # and inject the default dirs into it.
        HELP = """
Usage: pyinstaller.py [opts] <scriptname> [ <scriptname> ...] | <specfile>

Options:
  -h, --help            show this help message and exit
  -v, --version         Show program version info and exit.
  --distpath=DIR        Where to put the bundled app (default: %s%sdist)
  --workpath=WORKPATH   Where to put all the temporary work files, .log, .pyz
                        and etc. (default: %s%sbuild)
  -y, --noconfirm       Replace output directory (default:
                        SPECPATH\dist\SPECNAME) without asking for
                        confirmation
  --upx-dir=UPX_DIR     Path to UPX utility (default: search the execution
                        path)
  -a, --ascii           Do not include unicode encoding support (default:
                        included if available)
  --clean               Clean PyInstaller cache and remove temporary files
                        before building.
  --log-level=LOGLEVEL  Amount of detail in build-time console messages
                        (default: INFO, choose one of DEBUG, INFO, WARN,
                        ERROR, CRITICAL)

  What to generate:
    -F, --onefile       Create a one-file bundled executable.
    -D, --onedir        Create a one-folder bundle containing an executable
                        (default)
    --specpath=DIR      Folder to store the generated spec file (default:
                        current directory)
    -n NAME, --name=NAME
                        Name to assign to the bundled app and spec file
                        (default: first script's basename)

  What to bundle, where to search:
    -p DIR, --paths=DIR
                        A path to search for imports (like using PYTHONPATH).
                        Multiple paths are allowed, separated by ';', or use
                        this option multiple times
    --hidden-import=MODULENAME
                        Name an import not visible in the code of the
                        script(s). This option can be used multiple times.
    --additional-hooks-dir=HOOKSPATH
                        An additional path to search for hooks. This option
                        can be used multiple times.
    --runtime-hook=RUNTIME_HOOKS
                        Path to a custom runtime hook file. A runtime hook is
                        code that is bundled with the executable and is
                        executed before any other code or module to set up
                        special features of the runtime environment. This
                        option can be used multiple times.

  How to generate:
    -d, --debug         Tell the bootloader to issue progress messages while
                        initializing and starting the bundled app. Used to
                        diagnose problems with missing imports.
    -s, --strip         Apply a symbol-table strip to the executable and
                        shared libs (not recommended for Windows)
    --noupx             Do not use UPX even if it is available (works
                        differently between Windows and *nix)

  Windows and Mac OS X specific options:
    -c, --console, --nowindowed
                        Open a console window for standard i/o (default)
    -w, --windowed, --noconsole
                        Windows and Mac OS X: do not provide a console window
                        for standard i/o. On Mac OS X this also triggers
                        building an OS X .app bundle.This option is ignored in
                        *NIX systems.
    -i FILE.ico or FILE.exe,ID or FILE.icns, --icon=FILE.ico or FILE.exe,ID or FILE.icns
                        FILE.ico: apply that icon to a Windows executable.
                        FILE.exe,ID, extract the icon with ID from an exe.
                        FILE.icns: apply the icon to the .app bundle on Mac OS
                        X

  Windows specific options:
    --version-file=FILE
                        add a version resource from FILE to the exe
    -m FILE or XML, --manifest=FILE or XML
                        add manifest FILE or XML to the exe
    -r FILE[,TYPE[,NAME[,LANGUAGE]]], --resource=FILE[,TYPE[,NAME[,LANGUAGE]]]
                        Add or update a resource of the given type, name and
                        language from FILE to a Windows executable. FILE can
                        be a data file or an exe/dll. For data files, at least
                        TYPE and NAME must be specified. LANGUAGE defaults to
                        0 or may be specified as wildcard * to update all
                        resources of the given TYPE and NAME. For exe/dll
                        files, all resources from FILE will be added/updated
                        to the final executable if TYPE, NAME and LANGUAGE are
                        omitted or specified as wildcard *.This option can be
                        used multiple times.

  Obsolete options (not used anymore):
    -X, -K, -C, -o, --upx, --tk, --configfile, --skip-configure, --out, --buildpath
                        These options do not exist anymore.
""" % (gAppDir, os.sep, gAppDir, os.sep)

        dlg = wx.Dialog(self, -1, title='PyInstaller Help', size=(600, 600),
                        style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        dlg.txtCtrl = wx.TextCtrl(dlg, -1, u'%s' % HELP, style=wx.TE_DONTWRAP | wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_RICH2)
        dlg.txtCtrl.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT,
                                        wx.FONTSTYLE_NORMAL,
                                        wx.FONTWEIGHT_NORMAL,
                                        False,
                                        'Courier' # Mono Font Face
                                        ))
        # Color it like the command prompt.
        dlg.txtCtrl.SetBackgroundColour(wx.BLACK)
        dlg.txtCtrl.SetForegroundColour(wx.LIGHT_GREY)
        dlg.SetDoubleBuffered(True) # Reduce Flicker
        vbSizer = wx.BoxSizer(wx.VERTICAL)
        vbSizer.Add(dlg.txtCtrl, 1, wx.EXPAND | wx.ALL, 5)
        vbSizer.Add(dlg.CreateSeparatedButtonSizer(wx.OK), 0, wx.EXPAND | wx.ALL, 10)
        dlg.SetSizer(vbSizer)
        dlg.Centre()
        dlg.SetMinSize((200, 200))
        dlg.ShowModal()
        dlg.Destroy()


class MainFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title=_(u'wxPyInstallerGUI 2.1'),
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE
                     | wx.FRAME_EX_CONTEXTHELP
                     | wx.SUNKEN_BORDER,
                     name='frame',
                     log=None):
        wx.Frame.__init__(self, parent, id, title, pos, size, style, name)
        
        global gMainWin
        gMainWin = self

        gradpanel = PyInstallerBuilderPanel(self, gradientDirection=wx.NORTH, color1='#666666', color2='#FFFFFF',
                                            overlayPngBmp=overlay_dlines1.GetBitmap())
        gradpanel.Initialize()
        self.vbSizer = wx.BoxSizer(wx.VERTICAL)
        self.vbSizer.Add(gradpanel, 1, wx.EXPAND | wx.ALL, 0)
        self.SetSizerAndFit(self.vbSizer)
        # self.SetMinSize(self.GetSize())


class wxPyInstallerGUIApp(wx.App):
    def OnInit(self):
        frame = MainFrame(parent=None)
        frameSz = frame.GetSize()
        if frameSz[0] < 600:
            frame.SetSize((600, frameSz[1]))
        frame.SetDoubleBuffered(True)
        frame.Centre()
        frame.SetIcon(pyinstaller_console16.GetIcon())
        self.SetTopWindow(frame)
        frame.Show(True)

        return True


if __name__ == '__main__':
    app = wxPyInstallerGUIApp(0)
    app.MainLoop()
