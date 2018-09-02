"""IRC app for reading and sending messages
"""
___name___         = "IRC"
___license___      = "WTFPL"
___dependencies___ = ["app", "dialogs", "ugfx_helper", "buttons"]
___categories___   = ["EMF"]
___bootstrapped___ = True


from app import *
from dialogs import *
import ugfx
import ugfx_helper
import socket
import buttons
import wifi
from tilda import Buttons

ugfx_helper.init()
ugfx.clear()


wifi.connect(show_wait_message=True)

nick = prompt_text("Nickname (enter or add number)", init_text="emfbadge")

ugfx.clear()

conn = None

remoteaddr = "chat.freenode.net"
remoteport = 6697

ircchan = "#emfcamp"

addr = socket.getaddrinfo("chat.freenode.com", 6667)


with WaitingMessage(title="IRC", text="Please wait...") as message:
    conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0)
    conn.connect(addr)

    conn.send("PASS seecretpassword\r\n")
    conn.send("NICK {}\r\n".format(nick))
    conn.send("USER {} 0 * :An EMF camp Badge\r\n".format(nick))

    conn.send("JOIN {}\r\n".format(ircchan))

conn.setTimeout(None)

ugfx.clear()
notice("Connected!")

while True:
    data = ""
    try:
      data = conn.readline()
    except Exception as e:
      # TODO: Notify of exception
      notify("ERROR")
      app.restart_to_default()
    if not data == None and not data == "":
      if data.split(" ", 1)[1].startswith("PRIVMSG"):
        unameEOS = data.indexof("!")
        username = data[1:unameEOS]
        mesg = data.split(":", 2)[2]
        message = (uname, mesg)
        ugfx.clear()
        notify("{}:\r\n{}".format(message))
      elif data.split(" ", 1)[1].startswith("PING"):
        conn.send("PONG\r\n")
    if Buttons.is_pressed(Buttons.BTN_A):
      ugfx.clear()
      mesg = prompt_text("Message to Send", init_text="")
      if not mesg == "":
        conn.send("PRIVMSG {} :{}\r\n".format(ircchan, mesg))
    elif Buttons.is_pressed(Buttons.BTN_B):
      app.restart_to_default()
    sleep(1)
