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
    cursor_x = 0
    cursor_y = 0

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

        # cursor movement
        if k == curses.KEY_DOWN:
            cursor_y = cursor_y + 1
        elif k == curses.KEY_UP:
            cursor_y = cursor_y - 1
        elif k == curses.KEY_RIGHT:
            cursor_x = cursor_x + 1
        elif k == curses.KEY_LEFT:
            cursor_x = cursor_x - 1

        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)

        # Declaration of strings
        title = "Welcome to Cash Grab!"[:width-1]
        subtitle = "CSC 4750 Final Project for Alex Lopez."[:width-1]
        keystr = "Last key pressed: {}".format(k)[:width-1]
        statusbarstr = "Press 'esc' to exit | STATUS BAR | Pos: {}, {}".format(cursor_x, cursor_y)
        if k == 0:
            keystr = "No key press detected..."[:width-1]

        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
        start_y = int((height // 2) - 2)

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
        stdscr.addstr(start_y, start_x_title, title)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
        stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
        stdscr.addstr(start_y + 5, start_x_keystr, keystr)
        stdscr.move(cursor_y, cursor_x)


        # maintains a list of possible input streams 
        sockets_list = [sys.stdin, server] 
        read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 
        
        for socks in read_sockets: 
            if socks == server: 
                message = socks.recv(1024).decode('utf-8') 
                print(message) 
            else: 
                message = sys.stdin.readline() 
                # server.send(message) 
                server.send(bytes(message + '\n', 'utf8'))

                sys.stdout.write("<You>") 
                sys.stdout.write(message) 
                sys.stdout.flush() 


        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

        
    
    # while loop ended, close server connection
    server.close()


def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()