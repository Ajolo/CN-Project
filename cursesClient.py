import sys, os, socket, select
import curses

# removes default delay in escape for quicker app closing
os.environ.setdefault('ESCDELAY', '25')

'''
Server connection logic
'''
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) != 3: 
    print("Correct usage: script, IP address, port number")
    exit() 
IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2]) 
server.connect((IP_address, Port)) 



'''
Curses menu rendering
'''
def draw_menu(stdscr):
    k = 0
    # cursor_x = 0
    # cursor_y = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Loop where k is the last character pressed
    while (k != 27):  # 27 being the escape key code

        # curses init
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Declaration of strings
        title = "Welcome to Cash Grab!"[:width-1]
        subtitle = "CSC 4750 Final Project for Alex Lopez."[:width-1]
        keystr = "{}".format(k)[:width-1]
        statusbarstr = "Press 'esc' to exit | STATUS BAR | Key: {}".format(keystr)

        # Centering calculations
        center_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        # center_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        # center_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
        center_y = int((height // 2) - 2)


        # Rendering some text
        # whstr = "Width: {}, Height: {}".format(width, height)
        stdscr.addstr(0, 0, (subtitle), curses.color_pair(1))
        # stdscr.addstr(0, 0, subtitle, curses.color_pair(1))

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

        
        # maintains a list of possible input streams 
        sockets_list = [sys.stdin, server] 
        read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 

        # move all strings up (y+1)
        '''
        for (x = 0; x < height; x++)                
            message = (stdscr.getstr(, )).decode()
        '''
        
        for socks in read_sockets: 
            if socks == server: 
                message = socks.recv(1024).decode('utf-8') 
                stdscr.addstr(height-3, 0, message);
            else: 
                stdscr.addstr(height-2, 0, "> ")

                message = (stdscr.getstr(height-2, 2)).decode()
                
                server.send(bytes(message + '\n', 'utf8'))

                stdscr.addstr(height-3, 0, ("<You> " + message))
 
                # sys.stdout.write(message) 
                # sys.stdout.flush() 
        
        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

        
    
    # while loop ended, close server connection
    # server.close()


def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()