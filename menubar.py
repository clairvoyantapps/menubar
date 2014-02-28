#!/usr/bin/env python
# -*- coding: utf-8 -*-

import objc, re, os
from Foundation import *
from AppKit import *
from PyObjCTools import NibClassBuilder, AppHelper
import urllib,json,datetime, webbrowser

# poach one of the iSync internal images to get things rolling
status_images = {'idle':'images/bitcoin.png'}
COINBASE_API_URL = 'https://coinbase.com/api/v1/prices/spot_rate'

start_time = NSDate.date()

class Timer(NSObject):
  images = {}
  statusbar = None
  state = 'idle'

  def applicationDidFinishLaunching_(self, notification):
    self.coinbase_last = json.loads(urllib.urlopen(COINBASE_API_URL).read())['amount']
    self.update_every = '1 Min'

    statusbar = NSStatusBar.systemStatusBar()
    # Create the statusbar item
    self.statusitem = statusbar.statusItemWithLength_(NSVariableStatusItemLength)
    # Load all images
    for i in status_images.keys():
      self.images[i] = NSImage.alloc().initByReferencingFile_(status_images[i])
    # Set initial image
    self.statusitem.setTitle_('$' + self.coinbase_last)
    self.statusitem.setImage_(self.images['idle'])
    tool_tip = 'Coinbase Price $' + self.coinbase_last + '. Last updated: ' + str(datetime.datetime.now().strftime('%I:%M:%S %p')) + '. Updating every ' + self.update_every + '.'
    self.statusitem.setToolTip_(tool_tip)

    # Let it highlight upon clicking
    self.statusitem.setHighlightMode_(1)
    # Set a tooltip
    # self.statusitem.setToolTip_('Latest Coinbase Price!')

    # Build a very simple menu
    self.menu = NSMenu.alloc().init()
    # Sync event is bound to sync_ method
    menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('1 Min', 'time1min:', '1')
    self.menu.addItem_(menuitem)

    menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('10 Mins', 'time10min:', '2')
    self.menu.addItem_(menuitem)

    menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('30 Mins', 'time30min:', '3')
    self.menu.addItem_(menuitem)

    menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Update Now', 'updatenow:', '0')
    self.menu.addItem_(menuitem)

    menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Buy At Coinbase', 'buycoinbase:', 'b')
    self.menu.addItem_(menuitem)

    menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Sell At Coinbase', 'sellcoinbase:', 's')
    self.menu.addItem_(menuitem)

    # Default event
    menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', 'q')
    self.menu.addItem_(menuitem)
    # Bind it to the status item
    self.statusitem.setMenu_(self.menu)


    # Get the timer going
    self.timer = NSTimer.alloc().initWithFireDate_interval_target_selector_userInfo_repeats_(start_time, 60.0, self, 'tick:', None, True)
    NSRunLoop.currentRunLoop().addTimer_forMode_(self.timer, NSDefaultRunLoopMode)
    # self.timer.fire()

  def sync_(self, notification):
    print notification
    print notification.title

  def time1min_(self, notification):
    print 'in 1 min'
    self.update_every = '1 Min'
    self.timer.invalidate()
    st = NSDate.date()
    self.timer = NSTimer.alloc().initWithFireDate_interval_target_selector_userInfo_repeats_(st, 60.0, self, 'tick:', None, True)
    NSRunLoop.currentRunLoop().addTimer_forMode_(self.timer, NSDefaultRunLoopMode)
    self.timer.fire()

  def time10min_(self, notification):
    print 'in 10 min'
    self.update_every = '10 Mins'
    self.timer.invalidate()
    st = NSDate.date()
    self.timer = NSTimer.alloc().initWithFireDate_interval_target_selector_userInfo_repeats_(st, 600.0, self, 'tick:', None, True)
    NSRunLoop.currentRunLoop().addTimer_forMode_(self.timer, NSDefaultRunLoopMode)
    self.timer.fire()

  def time30min_(self, notification):
    print 'in 30 min'
    self.update_every = '30 Mins'
    self.timer.invalidate()
    st = NSDate.date()
    self.timer = NSTimer.alloc().initWithFireDate_interval_target_selector_userInfo_repeats_(st, 1800.0, self, 'tick:', None, True)
    NSRunLoop.currentRunLoop().addTimer_forMode_(self.timer, NSDefaultRunLoopMode)
    self.timer.fire()

  def updatenow_(self, notification):
    self.tick_(None)

  def buycoinbase_(self, notification):
    self.tick_(None)
    url = u"http://www.coinbase.com/buys"
    webbrowser.open(url)

  def sellcoinbase_(self, notification):
    self.tick_(None)
    url = u"http://www.coinbase.com/sells"
    webbrowser.open(url)

  def tick_(self, notification):
    self.coinbase_last = json.loads(urllib.urlopen(COINBASE_API_URL).read())['amount']
    self.statusitem.setTitle_('$' + self.coinbase_last)
    tool_tip = 'Coinbase Price $' + self.coinbase_last + '. Last updated: ' + str(datetime.datetime.now().strftime('%I:%M:%S %p')) + '. Updating every ' + self.update_every + '.'
    self.statusitem.setToolTip_(tool_tip)
    print tool_tip

if __name__ == "__main__":
  app = NSApplication.sharedApplication()
  delegate = Timer.alloc().init()
  app.setDelegate_(delegate)
  AppHelper.runEventLoop()