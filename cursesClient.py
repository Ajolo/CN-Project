import sys, os, socket, select, curses

'''
Server connection logic
'''
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) != 3: 
    print("Correct usage: script, IP address, port number")
    exit() 
IP_ADDR = str(sys.argv[1]) # for when specifying leia.cs.spu.edu
PORT = int(sys.argv[2]) 
server.connect((IP_ADDR, PORT)) 


'''
Curses menu rendering
'''
def draw_menu(stdscr):

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()
    height, width = stdscr.getmaxyx()

    # subwindow for text
    textWindow = stdscr.subwin(height-2, 60, 1, 0)
    textHeight, textWidth = textWindow.getmaxyx()
    textWindow.clear()
    textWindow.refresh()

    # subwindow for text input
    inputWindow = stdscr.subwin(1, 60, height-2, 0)
    inputHeight, inputWidth = inputWindow.getmaxyx()
    inputWindow.addstr(0, 0, "> ")
    inputWindow.clear()
    inputWindow.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    text_to_render = []

    try: 
        #  static curses init
        stdscr.clear()

        # Declaration of strings
        title = "Welcome to Cash Grab!"[:width-1]
        subtitle = "CSC 4750 Final Project for Alex Lopez."[:width-1]
        statusbarstr = "Ctrl+C to exit | STATUS BAR "

        # Centering calculations
        center_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        center_y = int((height // 2) - 2)

        # Rendering some text
        # whstr = "Width: {}, Height: {}".format(width, height)
        stdscr.addstr(0, 0, subtitle, curses.color_pair(1))

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Rendering title
        stdscr.addstr(center_y-5, center_x_title, title)
        # stdscr.addstr(center_y - 2, center_x_title, title)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Render moneybag
        stdscr.addstr(center_y-4, (width // 2) - 2, '-' * 5)
        stdscr.addstr(center_y-3, (width // 2) - 2, "\\   /")
        stdscr.addstr(center_y-2, (width // 2) - 1, "***")
        stdscr.addstr(center_y-1, (width // 2) - 3, "/     \\")
        stdscr.addstr(center_y, (width // 2) - 5, "/         \\")
        stdscr.addstr(center_y+1, (width // 2) - 7, "/      $      \\")
        stdscr.addstr(center_y+2, (width // 2) - 8, "|      $$$      |")
        stdscr.addstr(center_y+3, (width // 2) - 7, "\\      $      /")
        stdscr.addstr(center_y+4, (width // 2) - 5, "\\         /")
        stdscr.addstr(center_y+5, (width // 2) - 4, '-' * 8)

        # refresh to show changes
        stdscr.refresh()

        # enable character echo for chat input
        curses.echo() 

        inputWindow.erase()
        inputWindow.addstr(0, 0, "> ")
        inputWindow.refresh()

        while 1: 
 
            # maintains a list of possible input streams 
            sockets_list = [sys.stdin, server] 
            read_sockets, write_socket, error_socket = select.select(sockets_list,[],[]) 
  
            for socks in read_sockets: 
                if socks == server: 
                    message = socks.recv(1024).decode('utf-8')
                    # once message recv'd, need to separate out consecutive messages by newline
                    message.splitlines()
                    for line in message
                        text_to_render.insert(0, line)
                else: 
                    message = (inputWindow.getstr(0, 2)).decode()
                    server.send(bytes(message, 'utf8'))
                    prependMessage = ("<You> " + message)
                    text_to_render.insert(0, prependMessage)

            # if length of text_to_render is larger than render area, then 
            while len(text_to_render) > textHeight:
                text_to_render.pop()
    
            # render all previously saved text
            for i in range(0, len(text_to_render)):
                try:
                    textWindow.clrtoeol() # do this to clear any previous input 
                    textWindow.addstr((textHeight-2) - i, 0, text_to_render[i])
                except:
                    break
            
            # Refresh the screen
            textWindow.refresh()
            stdscr.refresh()
            inputWindow.erase()
            inputWindow.addstr(0, 0, "> ")
            inputWindow.refresh()

    # handle ctrl+c
    except KeyboardInterrupt:
        pass


    # close server connection and clear curses formatting
    stdscr.clear()
    server.close()


def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()