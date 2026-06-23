from App.ui.Dashboard.dashboard import main
if __name__ =="__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n=======================================")
        print("You Terminated the Project.")
        print("Good Bye. Have a nice day. Exiting...")
        print("=============================================\n\n")
