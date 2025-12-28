from upi_app.ui.app import UPIApp

if __name__ == "__main__":
    try:
        app = UPIApp()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication stopped by user (Ctrl+C). Exiting safely...")
        try:
            app.quit()
        except: 
            pass
